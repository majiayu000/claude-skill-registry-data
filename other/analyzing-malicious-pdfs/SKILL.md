---
name: analyzing-malicious-pdfs
description: 'Analyzes malicious PDF documents: parsing the object structure for JavaScript,
  OpenAction/launch triggers, embedded files, and URIs, then extracting and decoding suspicious
  streams without opening the document in a reader. Activates for requests to analyze a malicious
  PDF, inspect PDF JavaScript, or extract embedded payloads from a PDF.'
domain: cybersecurity
subdomain: malware-analysis
tags:
  - malware-analysis
  - pdf
  - document-malware
  - javascript
  - static-analysis
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1204.002
  - T1059.007
  - T1027
d3fend:
  - D3-FCR
  - D3-DA
references:
  - 'PDF 32000-1:2008 (ISO PDF specification) — https://www.pdfa.org/resource/iso-32000-pdf/'
  - 'Didier Stevens PDF tools (pdfid, pdf-parser) — https://blog.didierstevens.com/programs/pdf-tools/'
---

# Analyzing Malicious PDFs

## When to Use

- You have a suspicious PDF (often from phishing) and must determine if it is weaponized.
- You need to find auto-executing actions, embedded JavaScript, launch actions, or embedded files.
- You want to extract and decode suspicious streams safely.

**Do not use** a PDF reader to "just look" — opening in a viewer can trigger the very actions you
are investigating. Parse the structure statically.

## Prerequisites

- A PDF object parser (Python, or pdfid/pdf-parser/peepdf); the sample handled inertly.

## Safety & Handling

- Never open the PDF in a graphical reader; parse the raw object structure only.
- Defang any extracted URLs and store embedded payloads password-protected.

## Workflow

### Step 1: Triage the object inventory

Count high-risk keywords: `/JavaScript`, `/JS`, `/OpenAction`, `/AA`, `/Launch`, `/EmbeddedFile`,
`/URI`, `/RichMedia`. Their presence (especially auto-actions) flags weaponization.

```bash
python scripts/analyst.py triage sample.pdf
```

### Step 2: Locate auto-execution triggers

Resolve `/OpenAction` and `/AA` (additional actions) to see what runs on open, and any `/Launch`
actions that spawn external programs.

### Step 3: Extract and decode streams

Pull JavaScript and suspicious streams, applying filters (`/FlateDecode`, `/ASCIIHexDecode`) to
get the cleartext; deobfuscate layered JS as needed.

### Step 4: Recover payloads and IOCs

Extract embedded files and URIs; hash payloads, defang URLs, and route extracted executables to
PE analysis.

## Validation

- Auto-execution triggers (`/OpenAction`, `/AA`, `/Launch`) are resolved to concrete actions.
- JavaScript/streams are decoded through their filters, not left encoded.
- Embedded payloads and URIs are extracted, hashed, and defanged.

## Pitfalls

- Opening the PDF in a reader and triggering the payload.
- Missing object-stream (`/ObjStm`) compressed objects that hide the malicious content.
- Stopping at the first JS layer when it is multiply obfuscated.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the PDF triage parser.
- ISO 32000 and Didier Stevens' PDF tools (linked in frontmatter).
