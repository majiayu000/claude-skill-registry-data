---
name: extracting-cobalt-strike-beacon-config
description: 'Extracts and interprets a Cobalt Strike Beacon configuration: decoding the
  encoded config block, recovering C2 servers, malleable profile fields, sleep/jitter,
  watermark, and pipe names to build IOCs and attribution leads. Activates for requests to
  analyze a Cobalt Strike beacon, extract beacon config, or interpret malleable C2 settings.'
domain: cybersecurity
subdomain: malware-analysis
tags:
  - malware
  - cobalt-strike
  - c2
  - beacon-config
  - malleable
  - threat-intel
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1071.001
  - T1573
  - T1027
  - T1090
d3fend:
  - D3-NTA
  - D3-FCR
references:
  - 'Cobalt Strike documentation (malleable C2) — https://www.cobaltstrike.com/'
  - 'SentinelOne / community CS config parsers (concepts) — https://github.com/Sentinel-One/CobaltStrikeParser'
---

# Extracting Cobalt Strike Beacon Config

## When to Use

- You have a suspected Cobalt Strike Beacon (PE, DLL, shellcode, or extracted blob) and need
  its configuration.
- You want C2 servers, the malleable profile shape, sleep/jitter, watermark, and named pipes.
- You are building network IOCs and attribution leads from a beacon.

**Do not use** an extracted config alone for hard attribution — watermarks can be shared or
cracked. Treat it as one signal among several.

## Prerequisites

- The beacon payload (or a memory dump containing it) in neutralized form inside the lab.
- Familiarity with Cobalt Strike's encoded config block (commonly XOR-encoded with 0x2e in
  older versions, 0x69 in others; varies by version).

## Safety & Handling

- Static extraction only; do not run the beacon.
- Defang recovered C2 hosts/URIs before sharing.

## Workflow

### Step 1: Locate the encoded config block

Beacon stores settings as a packed, XOR-encoded table of TLV-like entries. Brute the
single-byte XOR key by scanning for the decoded table's known opening bytes (the first
setting index/type/length pattern).

### Step 2: Decode and parse settings

Once the key is found, walk the entries. Each has an index (setting type), a type
(short/int/string), and a length. The script decodes and maps known indices:

```bash
python scripts/analyst.py parse beacon.bin
```

### Step 3: Recover key fields

Pull the high-value settings:

```text
C2 servers / GET-URI / POST-URI    -> network IOCs
User-Agent                         -> detection signal
Sleep time / jitter                -> beacon cadence
Watermark                          -> license/team grouping lead
Pipe name / process-inject targets -> host IOCs
Spawn-to / DNS settings            -> behavior
```

### Step 4: Interpret the malleable profile

The URIs, headers, and transform settings reveal which malleable C2 profile the operator used
(e.g. masquerading as a known web service) — useful for network detection.

### Step 5: Build IOCs

Emit network IOCs (hosts, URIs, UA), host IOCs (pipe names), and the watermark for tracking.

## Validation

- The recovered C2 host(s) and URIs are well-formed and consistent with the profile.
- Sleep/jitter values are plausible and match any observed beaconing intervals.
- The same config reproduces from an independent extractor or memory copy.

## Pitfalls

- Hardcoding one XOR key — it varies across versions; brute-force per sample.
- Confusing a watermark match with attribution; cracked/leaked kits share watermarks.
- Stopping at the first C2 when the config lists multiple/backup servers.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the config parser.
- Cobalt Strike malleable C2 docs and community parser concepts (linked in frontmatter).
