---
name: hkust-gz-faculty-intel
description: Crawl and integrate HKUST(GZ) public faculty profile data by Hub and one or more Thrust areas. Use when Codex needs to collect faculty lists, emails, titles, profile URLs, identifiers, jobs, acting heads, or optional profile details from facultyprofiles.hkust-gz.edu.cn for selected HKUST(GZ) hubs/thrusts and export normalized JSON/CSV.
---

# HKUST-GZ Faculty Intel

## Overview

Use this skill to crawl public HKUST(GZ) Faculty Profile data at Hub and Thrust granularity. The default path uses public JSON endpoints behind `facultyprofiles.hkust-gz.edu.cn`, not login cookies, browser automation, or private APIs.

## Quick Start

List supported Hubs and Thrusts:

```powershell
python skills\hkust-gz-faculty-intel\scripts\hkust_gz_faculty.py list-thrusts
```

Crawl one Hub plus one Thrust:

```powershell
python skills\hkust-gz-faculty-intel\scripts\hkust_gz_faculty.py crawl `
  --hub "Information Hub" `
  --thrust "Artificial Intelligence" `
  --output-dir output\hkust_gz\info_ai
```

Crawl several Thrusts under one Hub:

```powershell
python skills\hkust-gz-faculty-intel\scripts\hkust_gz_faculty.py crawl `
  --hub INFOHUB `
  --thrust "Artificial Intelligence" `
  --thrust "Data Science and Analytics" `
  --output-dir output\hkust_gz\info_ai_dsa
```

Crawl every Thrust under a Hub:

```powershell
python skills\hkust-gz-faculty-intel\scripts\hkust_gz_faculty.py crawl `
  --hub "Systems Hub" `
  --all-thrusts `
  --output-dir output\hkust_gz\systems
```

Use official Thrust URL or code directly:

```powershell
python skills\hkust-gz-faculty-intel\scripts\hkust_gz_faculty.py crawl `
  --thrust-url "https://facultyprofiles.hkust-gz.edu.cn/thrust-faculties?code=10011A10000000000H28" `
  --output-dir output\hkust_gz\ai_by_url
```

Preview requests without network crawling:

```powershell
python skills\hkust-gz-faculty-intel\scripts\hkust_gz_faculty.py crawl `
  --hub INFOHUB `
  --thrust "Artificial Intelligence,Data Science and Analytics" `
  --dry-run
```

## Workflow

1. Resolve the user's target into official Hub and Thrust codes. Use `list-thrusts` when the request says "港科广某个 hub/系/学域" but names are abbreviated.
2. Prefer `crawl --hub ... --thrust ...` for exact Hub/Thrust subsets. Use repeated `--thrust` or comma-separated names for multiple Thrusts.
3. Use `--include-details` only when the user needs biography, projects, publications, resumes, or research-interest details. It calls one profile-detail endpoint per person and can produce large JSON.
4. Keep raw API captures separate from normalized exports. Do not commit crawl outputs unless the user explicitly asks.
5. If the public endpoint returns empty data for a known Thrust, retry with `--source page`; report endpoint drift instead of inventing data.

## Output

Each `crawl` run writes:

- `hkust_gz_faculty_manifest.json`: selected Hub/Thrusts, source URLs, counts, and run metadata.
- `hkust_gz_faculty_profiles.json`: normalized person-Thrust rows with selected jobs and source provenance.
- `hkust_gz_faculty_profiles.csv`: flat table for spreadsheet review.
- `raw/*.json`: raw public endpoint captures for audit and reruns.

Read `references/output-schema.md` before merging this output into another dataset.

## Scope

This skill is specialized for HKUST(GZ):

- Main Hubs: Function, Information, Systems, Society.
- Additional public units present in the same profile site may be listed, but Hub/Thrust crawling should default to the four main Hubs unless the user asks otherwise.
- It does not crawl HKU, CUHK, CityU, PolyU, or HKUST Clear Water Bay faculty directories.
- It does not bypass login, CAPTCHA, rate limits, or private data controls.

## Resources

- `scripts/hkust_gz_faculty.py`: standard-library crawler and exporter.
- `references/hub-thrust-map.md`: built-in Hub/Thrust code map and aliases.
- `references/output-schema.md`: normalized fields and merge policy.
