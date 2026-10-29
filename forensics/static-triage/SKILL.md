---
name: static-triage
description: "Use when you receive a suspicious file and must decide what it is without executing it. Covers the full static triage pipeline in an isolated lab: hashing and file identification, strings and entropy analysis, import and section inspection, YARA scanning, packer detection, and headless Ghidra function listing. Use when an alert, a phish attachment, or a carved binary needs a fast, safe first verdict before deeper analysis."
version: 1.0.0
domain: malware
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [forensics-fundamentals]
tools:
  - name: Ghidra
    version: 12.1.4
  - name: YARA
    version: 4.5.5
  - name: Python
    version: "3.12"
---
Static triage is the discipline of learning everything possible about a file
without running it. It is fast, safe, and usually enough to classify a sample
as benign, known-malicious, or needs-dynamic-analysis. The pipeline in this
skill moves from cheap to expensive: identify, hash, strings, entropy,
structure, YARA, then disassembly, stopping as soon as you have a confident
verdict. Scope: analyze only samples you are authorized to handle (alert
artifacts, your own lab builds, CTF files, client-provided samples). Do all
of it in an isolated analysis VM or sandbox host, never on a production
workstation, and never execute the sample during static triage, that is what
dynamic-sandbox is for.

## Quick Workflow

1. Hash the sample (MD5, SHA1, SHA256) and check it against known-good and
   known-bad sets before spending any more time.
2. Identify the real file type with magic bytes, not the extension.
3. Pull strings at multiple minimum lengths and read them like a story.
4. Measure entropy per section: packed or encrypted regions stand out.
5. Inspect imports, exports, and sections for capability hints.
6. Scan with your YARA rule set and note which rules fire.
7. Detect packers and decide whether static analysis is even viable.
8. Run headless Ghidra for a function list and cross-references on the
   interesting strings.

## 1. Hash and identify

Hashing first serves two purposes: deduplication against your corpus, and a
lookup key for threat intel you are allowed to use.

```bash
# All three hashes in one pass
md5sum sample.bin | tee hashes.txt
sha1sum sample.bin | tee -a hashes.txt
sha256sum sample.bin | tee -a hashes.txt

# Compare against your local known-bad set
grep -i -f hashes.txt known_bad.sha256 && echo 'KNOWN MALICIOUS'

# Real file type from magic bytes, ignoring the extension
file sample.bin
xxd -l 16 sample.bin
```

Common headers to recognize by sight: `MZ` (PE executable), `\x7fELF`
(Linux executable), `PK\x03\x04` (ZIP, which includes Office OOXML and JAR),
`%PDF`, `\x1f\x8b` (gzip), `7z\xbc\xaf\x27\x1c` (7z). A `.pdf` that starts
with `MZ` is not a PDF.

## 2. Strings analysis

Strings are the cheapest window into intent: URLs, IPs, registry keys,
pdb paths, error messages, and ransom notes all surface here.

```bash
# Default and long strings; compare what appears only at length 8+
strings sample.bin > strings_default.txt
strings -n 8 sample.bin > strings_8.txt
wc -l strings_default.txt strings_8.txt

# Hunt for indicators directly
grep -a -o -E 'https?://[^ "]+' strings_default.txt | sort -u | head -30
grep -a -o -E '\b([0-9]{1,3}\.){3}[0-9]{1,3}\b' strings_default.txt | sort -u | head -30
grep -a -i -E '\\\\(SOFTWARE|SYSTEM)\\\\|HKEY_|CurrentVersion\\Run' strings_default.txt | head -20

# Unicode strings (wide-char) are invisible to plain strings
strings -e l sample.bin > strings_unicode.txt
grep -a -i -E 'powershell|cmd\.exe|wscript' strings_unicode.txt | head -20

# PDB paths leak the author's build machine layout
grep -a -o -E '[A-Za-z]:\\[^ ]*\.pdb' strings_default.txt | head -10
```

Read the strings file end to end once, not just the grep hits. The narrative
matters: a binary containing both `CreateRemoteThread` and a ransom note
template tells a different story than one containing only standard library
error strings.

## 3. Entropy and section analysis

Packed or encrypted payloads have high entropy (near 8.0) and few readable
strings. Measure per section to localize the hidden code.

```bash
# Section table with sizes and entropy hints (PE)
python3 - <<'EOF'
import struct
data = open('sample.bin','rb').read()
# e_lfanew -> PE header -> section table walk (simplified triage)
e_lfanew = struct.unpack('<I', data[0x3c:0x40])[0]
assert data[e_lfanew:e_lfanew+4] == b'PE\x00\x00', 'not a PE'
coff = e_lfanew + 4
nsec = struct.unpack('<H', data[coff+2:coff+4])[0]
opt_size = struct.unpack('<H', data[coff+16:coff+18])[0]
sec_off = coff + 20 + opt_size
import math
def entropy(b):
    from collections import Counter
    c = Counter(b)
    n = len(b)
    return -sum((v/n) * math.log2(v/n) for v in c.values()) if n else 0
for i in range(nsec):
    s = data[sec_off+i*40:sec_off+(i+1)*40]
    name = s[:8].rstrip(b'\x00').decode(errors='ignore')
    vsize, vaddr, rawsize, rawptr = struct.unpack('<IIII', s[8:24])
    chunk = data[rawptr:rawptr+rawsize]
    print(f'{name:8} rawsize={rawsize:8} entropy={entropy(chunk):.2f}')
EOF
```

Interpretation: a `.text` section at entropy 7.9 with almost no strings is
packed. A `.rsrc` section at 7.9 may just hold a compressed icon or a
legitimate embedded archive, check its size and content before concluding.
Normal compiled code sits around 6.0 to 6.8.

```bash
# Imports: which APIs the binary needs (capability hints)
# (use rabin2, objdump, or Ghidra; quick PE import names via strings fallback)
grep -a -o -E '[A-Za-z0-9_]+\.dll' strings_default.txt | sort -u | head -30
grep -a -i -E 'VirtualAlloc|WriteProcessMemory|CreateRemoteThread|WinExec|URLDownloadToFile|CryptEncrypt|socket|connect' strings_default.txt | sort -u | head -30
```

## 4. YARA scanning

Run your rule set over the sample. A hit names the family or behavior; no
hits means unknown, not clean.

```bash
# Scan with the lab rule set
yara -r /opt/rules/index.yar sample.bin

# Which rule fired and which strings matched
yara -s -r /opt/rules/index.yar sample.bin | head -40

# Scan with metadata shown for triage notes
yara -m -r /opt/rules/index.yar sample.bin | head -40
```

Keep rules in one indexed file for speed, and version-control the rule set
so a hit is reproducible months later. Writing your own rules is covered in
yara-rules; here you only consume them.

## 5. Packer detection

A packer wraps the real code in a compressed or encrypted layer. Detect it
before you waste hours disassembling the wrapper.

```bash
# Detect It Easy: signature-based packer/compiler identification
diec sample.bin | head -20

# UPX is the common case and trivially reversible (see packer-analysis)
diec sample.bin | grep -i upx

# Entropy + section names corroborate: UPX leaves UPX0/UPX1 sections
python3 - <<'EOF'
data = open('sample.bin','rb').read()
print(b'UPX!' in data, b'UPX0' in data, b'UPX1' in data)
EOF
```

If a packer is confirmed, your static verdict options are: unpack it first
(packer-analysis), or escalate to dynamic analysis. Do not write a report
based on disassembly of the packed stub.

## 6. Headless Ghidra pass

When strings and YARA leave questions, get a function list and
cross-references without opening the GUI.

```bash
# Analyze headless and dump the function list
/opt/ghidra/support/analyzeHeadless /tmp/ghidra_proj Triage \
  -import sample.bin -postScript FunctionList.java 2>/dev/null | head -50

# Lighter alternative: list imported functions via script output
# Save Ghidra's decompiler output for the interesting functions only,
# then read it like source code, not like proof
```

Focus on: functions that reference the suspicious strings from step 2,
imports of process injection and networking APIs, and any function with an
unusually large basic-block count (often the real payload). Ghidra's
decompiler output is an approximation; confirm critical findings with the
disassembly view.

## 7. Writing the triage verdict

A triage note is short and decisive.

```bash
cat > triage_note.txt <<'EOF'
Sample: sample.bin
SHA256: <from hashes.txt>
File type: <from file>
YARA hits: <rule names or none>
Packer: <name or none>
Key strings: <3-5 most telling>
Verdict: BENIGN / MALICIOUS / UNKNOWN-needs-dynamic
Confidence: high/medium/low
Next step: <none | dynamic-sandbox | packer-analysis | yara-rules new rule>
EOF
```

UNKNOWN is a valid verdict. A wrong confident verdict is worse than an
honest unknown, because it stops the investigation.

## Edge cases

- File is a polyglot (valid as two formats): `file` reports one; check
  multiple offsets for headers and treat each embedded format separately.
- Strings are all garbage but entropy is low: the binary may be stripped of
  meaningful strings deliberately (string obfuscation); move to import
  analysis and dynamic.
- .NET assembly: strings and sections look odd; use a .NET-aware tool
  (dnfile, ilspycmd) instead of raw PE logic. YARA has a dotnet module.
- Sample is a script (PowerShell, JS, VBS): static triage is deobfuscation;
  look for `Invoke-Expression`, `eval`, base64 blobs, and download cradles.
- Huge installer or bundle: the malicious part may be one embedded file;
  carve embedded PEs/ZIPs first (binwalk or manual carving), then triage
  each.
- Hash matches known-good (signed Microsoft binary): still check the
  signature and the path; a valid signed binary in the wrong place can be
  living-off-the-land abuse.

## Escalation

- Static verdict is UNKNOWN and the sample is unpacked: escalate to
  dynamic-sandbox for behavior.
- Static verdict is UNKNOWN and the sample is packed: escalate to
  packer-analysis to unpack, then re-triage the unpacked payload.
- YARA fires on a generic rule only: write a family-specific rule
  (yara-rules) from the unique strings you found.
- Need to understand one function deeply: move from headless listing to an
  interactive Ghidra session, or use angr-basics for path exploration.
- Sample targets firmware or a non-x86 architecture: hand the carved
  binaries to firmware-analysis for the right toolchain.

## Detection and defender view

Static triage is the first filter in every malware pipeline: mail gateways,
EDR cloud lookups, and SOC analysts all do some version of hash, file, and
strings before anything heavier. Defenders should feed triage outputs back
into detection: every confirmed-malicious sample should yield YARA rules,
hashes for blocklists, and strings-derived IOCs (IPs, mutexes, registry
keys). Watch for the failure modes: allow-listing by hash alone (attackers
repack), trusting the file extension, and skipping triage because "the AV
said clean". The misuse case is using triage to improve malware rather than
detect it; this skill is for defenders classifying samples they are
authorized to handle, and repurposing it to harden malware against analysis
is out of scope.

## Key references

- MITRE ATT&CK T1027 (Obfuscated Files or Information): what packers and
  string obfuscation look like statically.
- MITRE ATT&CK T1036 (Masquerading): extension and header mismatches.
- MITRE ATT&CK T1204 (User Execution): the delivery context triage supports.
- CWE-506 (Embedded Malicious Code): the finding triage aims to confirm.
- YARA documentation: https://yara.readthedocs.io
- Ghidra documentation: https://ghidra-sre.org
- MITRE ATT&CK: https://attack.mitre.org

## See also

- `malware-static-triage`: Use it instead when the verdict must start from hash reputation lookups and capa capability extraction.
