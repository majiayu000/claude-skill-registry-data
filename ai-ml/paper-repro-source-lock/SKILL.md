---
name: paper-repro-source-lock
description: Lock official and trustworthy reproduction sources for an AI/ML paper. Use after a claim map exists, or whenever Codex must verify and record paper version, official code repository, commit/tag/release, dataset version, model checkpoint, license, provenance, access/auth requirements, and source priority before running a reproduction.
---

# Paper Repro Source Lock

## Overview

Use this skill to prevent "it ran on something, but not the paper artifact" failures. The output is a locked source manifest, not a broad literature review.

Read `references/patterns.md` before source selection when multiple repos, forks, model cards, datasets, or benchmark pages exist.

## Inputs

- A `claim_map.md` or `claim_map.json` from `$paper-repro-claim-map`.
- Paper URL/PDF identity, official project page, repository URL, model/data links, benchmark page, or user-provided artifact folder.
- Optional constraints: no login, public-only, official-only, budget, hardware, or license restrictions.

## Source Priority

Use this order unless the user says otherwise:

1. Official paper venue, proceedings, OpenReview, arXiv version, publisher page, DOI, or author project page.
2. Official repository linked by paper/authors/venue/project page.
3. Release, tag, commit, Zenodo DOI, GitHub archive, Hugging Face revision, Kaggle version, OpenML dataset/task ID, or container digest.
4. Official benchmark or dataset host.
5. Maintained third-party implementation or aggregator, clearly marked as `secondary`.
6. Search snippets or blog posts only as discovery hints, never as locked evidence.

Use `$paper-review-source-intel`, `$code-model-benchmark-intel`, `$google-scholar-profile-intel`, or `$external-api-onboarding` only when the selected source route needs their specific evidence or setup. Do not duplicate their full workflows.

## Workflow

1. Start from the claim map and list required artifacts per experiment: code, data, model, config, benchmark evaluator, scripts, and expected outputs.
2. Verify paper identity and version:
   - title, authors, venue/year;
   - arXiv/OpenReview/proceedings version;
   - appendix/supplement availability;
   - date accessed.
3. Lock code sources:
   - official repo URL and owner;
   - default branch;
   - commit SHA, tag, release, or archive hash;
   - subdirectory or script path for target experiments;
   - license and citation if available.
4. Lock data/model/benchmark sources:
   - dataset/model/checkpoint name and host;
   - version, revision, DOI, split, config, or checksum when available;
   - license/terms and access mode;
   - gating/auth/API needs.
5. Record unresolved items as blockers instead of silently substituting alternatives.
6. Produce a lock manifest before environment setup.

## Output Contract

Create `source_lock.md` and, for structured runs, `source_lock.json`.

Required Markdown sections:

- `Paper Version`
- `Locked Code Sources`
- `Locked Data Sources`
- `Locked Model or Checkpoint Sources`
- `Benchmark and Evaluation Sources`
- `License and Access Notes`
- `Auth or API Requirements`
- `Unresolved Sources`
- `Downstream Environment Inputs`

Use this JSON shape:

```json
{
  "paper": {
    "title": "",
    "source_url": "",
    "version": "",
    "fetched_at": ""
  },
  "sources": [
    {
      "id": "S1",
      "kind": "code",
      "priority": "primary",
      "url": "",
      "locked_ref": "",
      "license": "",
      "access": "public",
      "auth_required": false,
      "used_by_experiments": ["E1"],
      "notes": ""
    }
  ],
  "blockers": []
}
```

## Guardrails

- Do not use a fork or reimplementation as official unless the paper or authors point to it.
- Do not download gated/private data or models without user confirmation and valid access.
- Do not store tokens, cookies, private `.env` values, signed URLs, or credentials in the manifest.
- Prefer stable refs over floating branch names. If only a branch is available, record the observed commit SHA.
- Preserve source priority: `primary`, `secondary`, `archive`, or `fallback`.

## Resources

- `references/patterns.md`: source-locking practices distilled from artifact evaluation, Papers with Code completeness, data/model provenance, and reproducibility package conventions.
