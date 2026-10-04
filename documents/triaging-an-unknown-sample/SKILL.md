---
name: triaging-an-unknown-sample
description: 'Performs fast first-pass triage of an unknown file to decide depth of analysis:
  file type identification, hashing, reputation lookup, packing/entropy check, and string
  review. Activates for requests to triage, classify, or do initial assessment of an unknown
  or suspicious file.'
domain: cybersecurity
subdomain: lab-foundations
tags:
  - malware
  - triage
  - file-identification
  - entropy
  - strings
  - reputation
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1027
  - T1140
d3fend:
  - D3-FA
  - D3-FCR
references:
  - 'file/libmagic — https://man7.org/linux/man-pages/man1/file.1.html'
  - 'VirusTotal API documentation — https://docs.virustotal.com/reference/overview'
---

# Triaging an Unknown Sample

## When to Use

- A suspicious file has arrived and you need to quickly decide whether it warrants deep
  static/dynamic analysis or can be dismissed.
- You want a structured first-pass record (type, hashes, packing, notable strings) before
  committing analyst time.
- You are batch-triaging many files and need to rank them by suspicion.

**Do not use** triage results as a final verdict. A clean string review or unknown reputation
does not mean benign; it means proceed to deeper analysis.

## Prerequisites

- `file` (libmagic) for type identification, or the bundled magic-based detection.
- Optional VirusTotal API key for reputation (hash lookups only — never upload someone
  else's data without authorization).
- The sample in a neutralized, non-executable form inside the lab.

## Safety & Handling

- Triage is **static**: read bytes, never execute. Keep the sample with a neutralized
  extension.
- Submit only the **hash** to reputation services unless you have authorization to upload the
  file itself; uploads can expose sensitive or attributable data.

## Workflow

### Step 1: Identify the true file type

Do not trust the extension. Identify by magic bytes:

```bash
python scripts/analyst.py triage sample.bin
# reports: detected type, magic, hashes, entropy, suspicious strings
```

A `.pdf` that is really a PE, or a `.jpg` that is a script, is itself a finding.

### Step 2: Hash and check reputation

Compute the SHA-256 and look it up (hash-only) to see if it is known:

```bash
python scripts/analyst.py reputation --sha256 <sha256> --vt-key $VT_API_KEY
```

Known-bad with many detections → escalate. Unknown → continue triage; absence of detections
is not exoneration.

### Step 3: Estimate packing via entropy

High, uniform entropy across the whole file or a code section suggests packing or encryption:

```text
entropy ~7.9 / 8.0 over most of the file  -> likely packed/encrypted
mixed entropy with readable strings       -> likely unpacked
```

### Step 4: Skim strings for quick signal

Look for URLs, IPs, registry paths, suspicious API names, and embedded PE headers (`MZ`).
The script extracts and categorizes printable strings.

### Step 5: Decide and record

Classify as: dismiss, deep static, or detonate. Emit a triage record for the case file.

## Validation

- The detected type matches the file's structure (e.g. PE confirmed by `MZ`/`PE\0\0`).
- Entropy reading is consistent with the strings observed (packed files yield few readable
  strings).
- The triage record captures type, hashes, entropy, reputation, and the escalation decision.

## Pitfalls

- Equating "0 detections on VirusTotal" with benign — fresh or targeted malware is often
  unknown.
- Treating high entropy alone as proof of malice; installers and compressed media are also
  high-entropy. Combine signals.
- Uploading samples to third parties without authorization, leaking sensitive data.
- Stopping at triage for a file that is clearly suspicious but "not yet detected."

## References

- See [`references/api-reference.md`](references/api-reference.md) for the triage tool and
  scoring logic.
- libmagic and VirusTotal API documentation (linked in frontmatter).
