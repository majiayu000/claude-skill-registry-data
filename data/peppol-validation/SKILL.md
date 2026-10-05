---
name: peppol-validation
description: Validate Peppol BIS 3.0 e-business documents (the UBL formats used for trade across DK and the EU) and tell whether a file is the current standard or an outdated schema. The bundled PowerShell script auto-identifies the document from its root element + cbc:CustomizationID, maps it to the right OpenPeppol ruleset, runs the full official validation (UBL 2.1 XSD + Peppol Schematron) via the OpenPeppol/Helger web service, and reports OK or the exact errors with rule IDs. Covers invoice, credit note (incl. self-billing), order + order response/change/cancellation, order agreement, catalogue + response, despatch advice, MLR, punch out. Use when the user wants to validate/check a Peppol or UBL document, confirm an invoice/order/despatch-advice is valid Peppol BIS 3.0, batch-check a folder of e-invoices, or find out whether a file is the new BIS 3.0 schema or an old one (e.g. CENBII/peppol28a). Do NOT use to CREATE or transform documents — only to validate existing XML.
license: MIT
compatibility: Windows PowerShell 5.1+ or PowerShell 7+. Needs network access to a Peppol validation web service (the public OpenPeppol/Helger instance by default, or a self-hosted phive-ws). The public service receives the document and rate-limits under load — use a self-hosted endpoint for production/PII/batch.
metadata:
  version: "1.0.0"
---

# Peppol BIS 3.0 Validation

> Validates Peppol BIS 3.0 documents and reports **OK or the exact errors**, and tells you
> whether a file is the **current standard** or an **outdated schema**. The bundled script
> `scripts/Invoke-PeppolValidation.ps1` does the work end-to-end (identify → pick ruleset →
> validate → report); you (the agent) interpret the result and guide next steps. Read
> [REFERENCE.md](REFERENCE.md) for the document-type/VESID map, gotchas, and verification.

`SCRIPT` = this skill's `scripts/Invoke-PeppolValidation.ps1`.

## What it does

For every XML file (single file, folder, or wildcard) it:

1. **Auto-identifies** the document from its root element + `cbc:CustomizationID`.
2. **Tells you if it's the standard** — maps to a Peppol BIS 3.0 ruleset, or flags it
   `NOT a recognized Peppol BIS 3.0 document` (e.g. an old CENBII/`peppol28a` order, OIOUBL,
   or UN/CEFACT CII).
3. **Validates** against the full official stack (UBL 2.1 XSD + Peppol Schematron) via the
   OpenPeppol/Helger validation web service.
4. **Reports** `OK` or each error with its Peppol rule ID and the offending element path.

## How to run

Run with `pwsh` (PowerShell 7) or Windows PowerShell 5.1.

```powershell
# One document
pwsh -File SCRIPT invoice.xml

# A whole folder (all *.xml) or a wildcard, keeping the raw validation reports
pwsh -File SCRIPT C:\Peppol\Out -ReportFolder C:\Peppol\Reports

# Pipeline + a self-hosted validator (no data leaves the network, no rate limit).
# Pipe INSIDE a PowerShell session (dot/relative call) — not `| pwsh -File`, which would
# send objects to stdin instead of the -Path pipeline parameter.
Get-ChildItem C:\Peppol\Out\*.xml | & SCRIPT -Endpoint http://phive:8080/wsdvs
```

For several explicit files at once, use a wildcard/folder or an array call
(`& SCRIPT a.xml, b.xml`); `pwsh -File SCRIPT a.xml b.xml` binds only the first.

| Parameter | Purpose |
|-----------|---------|
| `-Path` (pos. 0, pipeline) | File, folder (all `*.xml`), or wildcard. Required. |
| `-Endpoint` | Validation web service. Default = public OpenPeppol/Helger. Point at a self-hosted phive-ws for production/PII/batch. |
| `-VesId` | Force a specific VESID, skipping auto-detection (e.g. to validate against a deprecated ruleset). |
| `-ReportFolder` | Write the raw validation response (`<file>.validation.xml`) per document. |
| `-ConfigPath` | Explicit `config.json` path. If omitted: `~/.peppol-validation/config.json`, then a skill-folder `config.json`, else the Helger default. |

## Self-hosted validator (config.json)

**By default the public OpenPeppol/Helger service is used** — you only get a local validator
if you explicitly ask for one via `config.json`. To validate against a **local phive-ws**
instead (no data leaves the network, no rate limit), copy `config.example.json` → `config.json`
in the skill folder and set the endpoint (rename `_endpoint` → `endpoint`):

```json
{ "endpoint": "http://localhost:8080/wsdvs" }
```

A `config.json` *without* an `endpoint` key still uses Helger — so copying the example verbatim
changes nothing until you deliberately set it.

**Guided setup (like the 7pace skill's auth step):** the installer offers to run
`scripts/Set-PeppolConfig.ps1`, or run it yourself:

```powershell
pwsh -File scripts/Set-PeppolConfig.ps1            # Enter = keep public Helger; or type a URL
pwsh -File scripts/Set-PeppolConfig.ps1 -Endpoint http://localhost:8080/wsdvs   # non-interactive
```

It writes `~/.peppol-validation/config.json` (machine-local, never committed), which the
validator auto-discovers ahead of any skill-folder `config.json`. Pressing Enter writes nothing
and keeps the public Helger default — the install never silently switches you to localhost.

The script auto-loads `config.json` from the skill folder (or `-ConfigPath`). You can also pin
ruleset versions there via `vesByArtifact` (handy when OpenPeppol bumps a release). `config.json`
is gitignored and preserved across skill updates; an explicit `-Endpoint`/`-VesId` still wins.

## Output contract

Per file: `Type` (root + CustomizationID), `Standard` (`[OK] Peppol BIS 3.0 - <type>` or
`[WARN] NOT a recognized Peppol BIS 3.0 document`), `Ruleset` (the VESID used), then
`Result: [OK] valid` or `[FAIL] N error(s)` with each error listed. Ends with a one-line
batch summary. **Exit code** (for automation):

| Code | Meaning |
|------|---------|
| `0` | All documents valid |
| `1` | Validation errors found |
| `3` | Non-standard document detected (not Peppol BIS 3.0 — e.g. an old schema) |
| `2` | Technical/usage problem (file missing, not well-formed, service unreachable) |

Precedence in a mixed batch: **2 > 1 > 3 > 0**.

## What you (the agent) do with the result

1. **Run the script** on the file/folder. Read its per-file lines and the exit code.
2. **Lead with the verdict**: valid, invalid (and *why* — quote the rule IDs and element
   paths), or non-standard (name the schema you detected and that it isn't BIS 3.0).
3. **For errors**, group by Peppol rule ID and translate the rule text into the concrete fix
   (which element to add/remove/correct). Don't dump raw XML — point at the failing path.
4. **For a non-standard file**, say what it actually is (e.g. CENBII `peppol28a` ver1.0 =
   pre-BIS-3 Peppol) and that it can't be auto-validated against BIS 3.0; offer `-VesId` if
   they genuinely need to validate against the old ruleset.
5. **Fail loud on coverage**: if any file hit a technical error (exit 2) or the service
   rate-limited, say so explicitly — never imply a file passed when it wasn't actually checked.

## Gotchas

See [REFERENCE.md](REFERENCE.md#gotchas) — required reading before trusting a result
(the `auto` VESID trap, rate limiting, quarterly ruleset versions, the data-egress note).

## Verification

See [REFERENCE.md](REFERENCE.md#verification) for the before/after checks. In short:
confirm the script parses and reaches the endpoint with a known-good file first, and treat a
result as trustworthy only when the run reports the document was actually validated (XSD +
Schematron artefacts ran) — not skipped or interrupted.

## Errors

- `Validation service problem: ... 429` — the public instance rate-limited you. The script
  retries with backoff; for batch/production self-host phive-ws and use `-Endpoint`.
- `Syntactically invalid VESID` — a forced `-VesId` is malformed, or auto-detection produced
  no ruleset (the document isn't BIS 3.0). Check the CustomizationID.
- `Not well-formed XML` — the input isn't valid XML at all (exit 2), unrelated to Peppol rules.
