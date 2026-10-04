---
name: conference-workshop-intel
description: Route AI conference, workshop, CFP, review-policy, accepted-paper, oral/spotlight, award, deadline, and program intelligence collection through public official sources by default. Use when Codex needs to crawl or synthesize NeurIPS, ICML, ICLR, ACL, EMNLP, NAACL, CVPR, ICCV, ECCV, AAAI, IJCAI, KDD, WWW, SIGIR, workshop ecosystems, OpenReview-hosted venues, ai-workshop-tracker data, ACL Anthology, CVF Open Access, PMLR, NeurIPS proceedings, or normalized JSONL/CSV/Markdown reports about conference and workshop trends.
---

# Conference Workshop Intel

## Overview

Use this skill for public-source AI conference and workshop intelligence. The default closure works without private credentials: official conference sites, OpenReview public visibility, ai-workshop-tracker data, ACL Anthology, CVF Open Access, PMLR, NeurIPS proceedings, and source-specific public pages.

## Decision Tree

1. Identify the target:
   - conference/year: `NeurIPS 2025`, `ICML 2026`, `CVPR 2025`, `EMNLP 2025`;
   - workshop ecosystem: workshop list, deadlines, accepted workshop papers, topic tags;
   - policy/CFP: call for papers, review policy, ethics policy, compute policy, reviewer guidance;
   - program signal: accepted papers, oral/spotlight, best paper, award, schedule;
   - OpenReview venue or forum URL;
   - cross-conference trend or monitoring task.
2. Run a route plan before crawling:

```powershell
python skills\conference-workshop-intel\scripts\conference_workshop_intel.py plan `
  --target "NeurIPS 2025 workshops accepted papers CFP review policy" `
  --venue NeurIPS `
  --year 2025 `
  --needs workshops,accepted-papers,cfp,policy,awards,report
```

3. Execute only the needed lane:
   - Workshop list, deadlines, and OpenReview-hosted workshop accepted papers: use `ai-workshop-tracker` first, then official workshop pages.
   - ICLR/ICML/NeurIPS public submissions, decisions, reviews, and workshop venues: use OpenReview public pages or `openreview-py`.
   - ACL/EMNLP/NAACL/COLING proceedings: use ACL Anthology.
   - CVPR/ICCV/ECCV/WACV papers: use CVF Open Access and official conference program pages.
   - ICML/AISTATS/COLT papers: use PMLR plus official conference pages.
   - NeurIPS accepted papers: use NeurIPS proceedings and official `neurips.cc` pages; use OpenReview when the year/venue exposes the needed public fields.
   - AAAI/IJCAI/KDD/WWW/SIGIR: use official venue sites first, then DOI/open metadata enrichment.
   - Best paper/oral/spotlight/award/policy: use official program/blog/CFP pages first; third-party lists are discovery-only until verified.
4. Normalize before synthesis. Reports should cite normalized row IDs and source URLs, not loose browser state.

## Full Local Setup

For the no-secret local setup and a public network smoke test:

```powershell
powershell -ExecutionPolicy Bypass -File skills\conference-workshop-intel\scripts\setup_conference_workshop_intel.ps1 -RunNetworkSmoke
```

For a lightweight smoke without installing dependencies:

```powershell
powershell -ExecutionPolicy Bypass -File skills\conference-workshop-intel\scripts\setup_conference_workshop_intel.ps1 -SkipPythonDeps -RunNetworkSmoke
```

This creates an isolated runtime under `runtime/conference-workshop` when the skill is installed globally or in the repo. It also creates a private `.env` placeholder without storing any secret. Read `references/full-setup.md` before configuring optional credentials.

## External API Closure

Required credentials: none.

Use `$external-api-onboarding` before setting optional credentials such as `OPENREVIEW_USERNAME`, `OPENREVIEW_PASSWORD`, `SEMANTIC_SCHOLAR_API_KEY`, `GITHUB_TOKEN`, `HF_TOKEN`, or `PAPER_SEARCH_MCP_*`. Store them only in private user-level storage such as:

```text
%USERPROFILE%\.codex\skills\conference-workshop-intel\.env
```

For visible provider-page assistance:

```powershell
powershell -ExecutionPolicy Bypass -File skills\conference-workshop-intel\scripts\assist_conference_workshop_auth.ps1 -Provider openreview,semantic-scholar,github
```

The helper opens official provider pages only. The user completes login, MFA, CAPTCHA, key creation, and secret copy. Do not paste secrets into chat.

## Source Routing

Read `references/source-routing.md` before selecting a backend.

- Use `ai-workshop-tracker` for ML workshop editions, deadlines, topic tags, OpenReview venue discovery, and accepted-paper caches.
- Use official venue sites for CFP, review policy, ethics policy, awards, oral/spotlight, schedules, and workshop pages.
- Use OpenReview for public submissions, decisions, reviews, scores, venue groups, and workshop venues when the venue exposes them.
- Use ACL Anthology, CVF Open Access, PMLR, and NeurIPS proceedings for official paper metadata and PDFs.
- Use deadline trackers, best-paper lists, and Paper Copilot-style pages only as secondary discovery seeds unless verified against official pages.

## Common Commands

Classify a URL:

```powershell
python skills\conference-workshop-intel\scripts\conference_workshop_intel.py inspect-url `
  "https://neurips.cc/virtual/2025/events/workshop"
```

Print the normalized artifact contract:

```powershell
python skills\conference-workshop-intel\scripts\conference_workshop_intel.py schema
```

Generate a run scaffold:

```powershell
python skills\conference-workshop-intel\scripts\conference_workshop_intel.py scaffold `
  --output-dir output\conference_workshop\neurips_2025_workshops `
  --target "NeurIPS 2025 workshop ecosystem" `
  --venue NeurIPS `
  --year 2025 `
  --needs workshops,deadlines,accepted-papers,cfp,policy,awards,report
```

Normalize a raw JSON/JSONL/CSV/YAML capture:

```powershell
python skills\conference-workshop-intel\scripts\conference_workshop_intel.py normalize `
  --input output\conference_workshop\neurips_2025_workshops\raw\workshops.json `
  --source ai-workshop-tracker `
  --kind workshops `
  --output-dir output\conference_workshop\neurips_2025_workshops\normalized
```

Run a cheap public-source smoke:

```powershell
python skills\conference-workshop-intel\scripts\conference_workshop_intel.py public-smoke
```

## Output Contract

Use this directory shape for substantial runs:

- `raw/`: untouched API JSON, scraped HTML, YAML, CSV exports, screenshots, PDFs, and logs.
- `normalized/events.jsonl`: conference/year/event rows.
- `normalized/workshops.jsonl`: workshop editions, deadlines, websites, OpenReview venues, topics, and paper-list sources.
- `normalized/papers.jsonl`: accepted paper, submission, proceedings, oral/spotlight, and workshop-paper rows.
- `normalized/policies.jsonl`: CFP, review policy, ethics policy, compute policy, reviewer guidance, and policy-change rows.
- `normalized/awards.jsonl`: best paper, honorable mention, test-of-time, oral, spotlight, and award rows.
- `normalized/artifacts.jsonl`: local files, downloaded assets, screenshots, logs, and generated reports.
- `sources.csv`: source review table with URL, source type, priority, and status.
- `manifest.json`: plan, commands, timestamps, limits, credential policy, and blockers.
- `reports/summary.md`: human-facing synthesis grounded in normalized row IDs.

Read `references/output-schema.md` before merging multiple sources.

## Guardrails

- Default work must remain useful without MCP, paid services, private tokens, cookies, proxies, or login-gated data.
- Prefer official venue pages, official proceedings, and OpenReview public visibility over search snippets and aggregators.
- Do not bypass paywalls, CAPTCHAs, private reviews, login gates, rate limits, robots restrictions, or license controls.
- Keep credentials, cookies, browser storage, proxies, headers, `.env` files, and provider account details out of git and final answers.
- Mark source priority as `primary`, `secondary`, `archive`, or `fallback` for every normalized row.
- Preserve source URL, source ID, fetched timestamp, venue, year, edition, and provenance fields.
- For policy and award claims, capture the exact official page URL and page date or crawl timestamp.
- Run a small public smoke before bulk crawl/download and record blocked or stale sources in `manifest.json`.

## Resources

- `scripts/conference_workshop_intel.py`: planner, URL inspector, run scaffold generator, schema printer, lightweight normalizer, and public-source smoke test.
- `scripts/setup_conference_workshop_intel.ps1`: no-secret local runtime setup, optional ai-workshop-tracker clone, and public smoke tests.
- `scripts/assist_conference_workshop_auth.ps1`: visible provider-page opener and optional secret-storage command guidance.
- `references/full-setup.md`: setup matrix, optional credentials, provider pages, and smoke-test commands.
- `references/source-routing.md`: detailed source routes and fallback policy.
- `references/output-schema.md`: normalized fields and merge policy.
