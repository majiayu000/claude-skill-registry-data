---
name: whea-fatal-error-triage
description: "Triage Windows WHEA-Logger \"A fatal hardware error has occurred\" (Event ID 1) records to decide whether they identify a failing component or are firmware boilerplate, before recommending any RAM/CPU/PSU action."
---

# WHEA fatal hardware error triage

Use when Windows logs `Microsoft-Windows-WHEA-Logger` **Event ID 1** — *"A fatal hardware error has occurred"* — and someone is about to blame RAM or a CPU.

## Rule zero: never hand-decode a CPER from printed decimal bytes

Eyeballing `$_.Properties` output and naming section-type GUIDs from memory produces confident, wrong claims (e.g. asserting a "Platform Memory Error Section", or a CPUID implying the wrong CPU vendor). Section-body offsets are the easiest thing to get wrong, and a bad offset is detectable: sanity-check every parsed field against a plausible range. A `LocalAPICID` of 1.3e17 means your offsets are wrong — stop and discard everything derived from that layer.

**Prefer conclusions that need no offsets at all.** See step 3.

## 1. Ask Windows first

```powershell
Get-WinEvent -FilterHashtable @{LogName='System';Id=1;ProviderName='Microsoft-Windows-WHEA-Logger'} |
  ForEach-Object { $_.TimeCreated; $_.Message; $_.FormatDescription() }
wevtutil qe System /q:"*[System[Provider[@Name='Microsoft-Windows-WHEA-Logger']]]" /f:text /c:3
```

For Event ID 1 this returns only the generic sentence, and `EventData` holds just `Length` + `RawData`. **That absence is itself a finding**: Windows did not identify a component.

## 2. Check which WHEA event IDs exist, and the other channel

```powershell
Get-WinEvent -FilterHashtable @{LogName='System';ProviderName='Microsoft-Windows-WHEA-Logger'} |
  Group-Object Id | Select-Object Count,Name
Get-WinEvent -LogName 'Microsoft-Windows-Kernel-WHEA/Errors'   # often has MORE records than System
```

- IDs **17/18/19/20/47** carry decoded PCIe/memory/cache fields from machine checks the OS actually observed. Their presence means real telemetry — go read it.
- **Only ID 1**, logged by `NT AUTHORITY\LOCAL SERVICE` and mirrored at `Level=Information` in `Kernel-WHEA/Errors`, means every record is a BERT (Boot Error Record Table) replay written by firmware at boot.
- `Kernel-WHEA/Errors` frequently retains far more history than the System log. Always check it — it can turn "6 events in 4 months" into "16 events over 17 months".

## 3. The offset-free invariance test (the decisive step)

Export the provider's own `RawData` field, then compare records against each other. Needs **no** GUID names and **no** section layout.

```powershell
$out='.\cper'; New-Item -ItemType Directory -Force $out | Out-Null; $i=0
Get-WinEvent -LogName 'Microsoft-Windows-Kernel-WHEA/Errors' | Sort-Object TimeCreated | ForEach-Object {
  $i++; $x=[xml]$_.ToXml()
  ($x.Event.EventData.ChildNodes | Where-Object Name -eq 'RawData').'#text' |
    Out-File (Join-Path $out ("{0:d2}_{1}.hex" -f $i,$_.TimeCreated.ToString('yyyyMMdd-HHmmss'))) -Encoding ascii -NoNewline
}
```

Then diff every record against a reference and hash the invariant remainder:

```python
import glob, hashlib
recs = {p: bytes.fromhex(open(p).read().strip()) for p in sorted(glob.glob('cper/*.hex'))}
print('distinct lengths:', {len(v) for v in recs.values()})
ref = next(iter(recs.values()))
diff = {i for v in recs.values() for i,(a,b) in enumerate(zip(ref,v)) if a!=b}
print(f'varying {len(diff)} of {len(ref)} bytes')
print('non-zero bytes:', sum(1 for b in ref if b), 'of', len(ref))
hashes = {hashlib.sha256(bytes(b for i,b in enumerate(v) if i not in diff)).hexdigest()[:16] for v in recs.values()}
print('distinct invariant hashes:', len(hashes))   # 1 == all records share one template
```

**Firmware boilerplate looks like:** one distinct length, ~1% of bytes varying (confined to the CPER timestamp at bytes 24–31 and RecordId at 96–103), a single invariant hash across all records, and a record ~90% zeros with a multi-hundred-byte contiguous zero run.

**Real telemetry looks like:** varying lengths, incident-specific payload, populated section bodies.

## 4. Validate any offset you do rely on

The CPER header carries `RecordLength` at bytes 20–23. If it equals the provider's independently-declared `Length`, the *header* layout is externally corroborated — you may then trust signature (0–3), section count (10–11) and severity (12–15). Do **not** extend that trust to section descriptors or bodies.

## 5. Correlate with actual resets — both directions

```powershell
$sys = Get-WinEvent -FilterHashtable @{LogName='System'}
$k41 = $sys | Where-Object { $_.Id -eq 41 -and $_.ProviderName -eq 'Microsoft-Windows-Kernel-Power' }
$e60 = $sys | Where-Object { $_.Id -eq 6008 }
```

Match each WHEA record to Kernel-Power 41 / EventLog 6008 within ±10 min, and **report how far back the System log actually reaches** so uncovered records aren't scored as "no reset".

The two directions mean different things:
- **WHEA ⇒ reset (1:1):** contents are boilerplate but presence reliably marks a real event. *Boilerplate content does not mean nothing happened.* Do not let "firmware junk" soften into "harmless".
- **resets > WHEA records:** some resets leave no record, so record count understates the fault rate.

## 6. Trend and time-of-day before concluding

Compute gaps between consecutive events, compare early mean vs recent mean, and bucket by hour.

- **Shortening intervals = accelerating fault rate = degrading hardware.** Never call a cadence "steady" without computing it.
- **Clustering at idle hours** (sleep disabled, machine idle-but-awake) points at low-frequency/low-voltage operating points, C-states or SoC idle voltage — not thermal or load stress.

## Reporting

Separate cleanly:
- **Verified:** offset-free facts (record count, span, length uniformity, invariant hash, zero density) plus anything corroborated by an external field.
- **Withdrawn/unverified:** every section name, GUID and body-field interpretation that came from recall.
- **Conclusion:** if the records are templated, say the events *do not identify a component* — not that the hardware is fine. Recommend Windows Memory Diagnostic (check whether it has ever run), the newest BIOS pulled from the vendor's own support page (aggregator sites lag and may list versions older than what is installed), and hardware-level diagnosis if it recurs. Keep this stream separate from software repairs done in the same session; no registry or driver fix addresses it.
