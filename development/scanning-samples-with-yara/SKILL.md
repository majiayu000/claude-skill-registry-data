---
name: scanning-samples-with-yara
description: 'Uses YARA to classify and triage samples at scale: applying rule sets, reading
  matches and string offsets, tuning for false positives, and organizing rules for malware
  family identification. Activates for requests to scan files with YARA, apply YARA rules, or
  classify samples by signature.'
domain: cybersecurity
subdomain: malware-analysis
tags:
  - malware
  - yara
  - signatures
  - classification
  - triage
  - detection
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1027
  - T1587.001
d3fend:
  - D3-FCR
  - D3-FA
references:
  - 'YARA documentation — https://yara.readthedocs.io/'
  - 'yara-python — https://github.com/VirusTotal/yara-python'
---

# Scanning Samples with YARA

## When to Use

- You want to classify one or many samples against known malware-family or capability rules.
- You need to confirm a family hypothesis with a targeted rule and read which strings matched.
- You are triaging a directory of files and want to flag the suspicious ones.

**Do not use** a YARA match as proof of family attribution on its own — public rules vary in
quality and can over-match. Corroborate with behavior or code analysis.

## Prerequisites

- `yara` CLI or `yara-python` (`pip install yara-python`).
- A curated rule set (your own plus vetted public rules). Avoid blindly merging large noisy
  collections.
- Samples in neutralized form inside the lab.

## Workflow

### Step 1: Organize rules

Keep rules in categories (family, capability, packer, anomaly) and compile them once for
speed. Tag rules so matches are self-describing.

### Step 2: Scan and read matches

```bash
python scripts/analyst.py scan rules/ sample.bin
# prints matched rule names, tags, and matched strings with offsets
```

The matched **string offsets** matter: they tell you where in the file the signal is (header,
overlay, resource), which guides deeper analysis.

### Step 3: Triage a directory

```bash
python scripts/analyst.py scan rules/ ./samples --recursive --summary
```

Rank files by number/severity of matches to prioritize analyst time.

### Step 4: Tune for false positives

If a rule fires on benign files, tighten it: require multiple strings (`2 of ($a*)`),
anchor to file structure (`uint16(0) == 0x5A4D`), or raise the condition specificity.

### Step 5: Promote good signals to detection

A rule that reliably identifies a family or capability becomes a hunting/detection artifact —
hand it to the detection-engineering workflow.

## Validation

- Matches reproduce across runs and tools (CLI and `yara-python` agree).
- Each kept rule has an acceptable false-positive rate against a known-clean corpus.
- Match offsets correspond to meaningful file regions, not incidental byte coincidences.

## Pitfalls

- Merging huge public rule packs without curation — noise and false positives explode.
- Writing rules on packed bytes that change with every build; prefer unpacked or structural
  features.
- Over-broad strings (common library text) that match unrelated software.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the scanner tool.
- YARA and yara-python documentation (linked in frontmatter).
