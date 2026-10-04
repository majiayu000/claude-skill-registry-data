---
name: identifying-file-types-and-formats
description: 'Identifies a sample''s true file type independent of its extension: matching magic
  bytes and structural signatures, detecting container/archive formats, and flagging
  extension-content mismatches used to disguise malware. Activates for requests to identify a
  file type, check magic bytes, or detect a disguised/spoofed extension.'
domain: cybersecurity
subdomain: lab-foundations
tags:
  - lab-foundations
  - file-type
  - magic-bytes
  - triage
  - masquerading
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1036.008
  - T1036
d3fend:
  - D3-FCR
references:
  - 'libmagic / file command — https://www.darwinsys.com/file/'
  - 'List of file signatures (magic numbers) — https://en.wikipedia.org/wiki/List_of_file_signatures'
---

# Identifying File Types and Formats

## When to Use

- You receive an unknown sample and must determine what it actually is before choosing tools.
- You suspect masquerading — a `.pdf` or `.jpg` that is really an executable or script.
- You need to detect container formats (ZIP/OLE/ISO) that hide a payload.

**Do not use** the file extension or the OS-reported type as truth — adversaries rename
executables and embed payloads; always confirm by content.

## Prerequisites

- `file`/libmagic or an equivalent magic-byte database; the sample handled inertly in the lab.

## Safety & Handling

- Never open the sample in its associated application during identification; read raw bytes only.
- Keep the disguised extension in mind — a double extension or RTLO trick can mislead the eye.

## Workflow

### Step 1: Read the magic bytes

Inspect the leading bytes and known offset signatures (e.g., `MZ`, `\x7fELF`, `%PDF`, `PK\x03\x04`,
OLE `D0 CF 11 E0`).

```bash
python scripts/analyst.py identify sample.dat
```

### Step 2: Confirm structure

For container formats, confirm internal structure (ZIP central directory, OLE storage, ISO
`CD001` at 0x8001) rather than trusting the header alone.

### Step 3: Compare against the claimed extension

Flag mismatches: a `.jpg` whose content is `MZ`, or a document that is actually a script. These
are strong masquerading indicators.

### Step 4: Route to the right analysis

Use the confirmed type to pick the correct workflow (PE static analysis, document analysis,
archive extraction).

## Validation

- The detected type is confirmed by both magic bytes and structural checks, not magic alone.
- Extension/content mismatches are explicitly reported.
- The result correctly routes the sample to the appropriate analysis skill.

## Pitfalls

- Trusting the first 2 bytes only; some formats need offset or structural confirmation.
- Missing polyglot files that are valid as two formats at once.
- Overlooking nested containers (archive inside archive) that hide the real payload.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the type identifier.
- libmagic and the magic-number reference (linked in frontmatter).
