---
name: gaia-ingest
description: >-
  Atomically ingest one already-verified evidence row into one named Gaia skill
  using the CLI, then appraise Trust Magnitude and propose—never silently
  apply—a calibration. Use after /ev-pipeline has verified an approved intake
  source, or whenever a curator says "ingest evidence", "add verified evidence",
  "gaia-ingest", or "turn this source into registry evidence".
version: 1.0.0
argument-hint: "<contributor/skill> <verified-source>"
---

# Gaia Ingest

Safely turn **one verified evidence source** into one CLI-authored evidence row.
This is the mutation bridge after evidence verification; it is not discovery,
source research, or a bulk importer.

## Required inputs

- Named skill ID: `contributor/skill-id`
- Source URL verified by `/ev-pipeline` link validation
- Evidence Type and only the numeric payload that type supports
- Attribution scope: `named`, `generic`, or `suite`
- Factual notes describing exactly what the source proves

Refuse the write when any input is absent, the source is dead, the evidence
belongs to a different capability, or the requested payload would be guessed.

## Preflight

1. Confirm the named skill exists and inspect its current rows:

   ```bash
   gaia dev list --named --json
   sed -n '1,120p' registry/named/<contributor>/<skill-id>.md
   ```

2. Confirm the source was verified by the current evidence run. For GitHub,
   also fetch live facts with `gh api`; for social sources, scrape the source
   and preserve its public view count; for benchmarks, require the complete
   reproducibility payload.

3. Reject duplicate `(Evidence Type, canonical source URL)` rows. Do not use
   a suite-wide source as full-strength component evidence. A component must
   have implementation-specific proof; suite-wide proof belongs on the suite
   capstone or is recorded as scoped supplemental context.

4. Choose only a schema-supported Evidence Type. Never use the obsolete
   `--class` flag. Use `gaia dev evidence --help` if the payload is unclear.

## CLI-only mutation

Run exactly one command for the one evidence row. Always use `--no-build`;
callers such as `/gaia-ingest-batch` perform the single final build.

```bash
GAIA_OPERATOR_OVERRIDE=1 gaia dev evidence <contributor/skill-id> "<source-url>" \
  --type <evidence-type> <supported-numeric-flags> \
  --notes "<factual scope and verification note>" \
  --source-started-at YYYY-MM-DD \
  --no-build
```

Payload examples:

```bash
# Public third-party video; views must be visible on the scraped source.
gaia dev evidence firecrawl/web-scrape-integration "https://www.youtube.com/watch?v=..." \
  --type social-signal --views 8510 \
  --notes "Third-party tutorial explicitly demonstrates Firecrawl page scraping." \
  --source-started-at 2025-07-20 --no-build

# Concrete upstream skill file; use a blob URL, live star count, and real
# number of skills sharing the repository.
gaia dev evidence firecrawl/web-scrape-integration "https://github.com/firecrawl/skills/blob/main/skills/firecrawl-build-scrape/SKILL.md" \
  --type github-stars-own --stars 42 --skill-count-in-repo 5 \
  --notes "Official upstream implementation source; star count verified via GitHub API." \
  --source-started-at 2026-04-08 --no-build
```

For `benchmark-result`, provide every reproducibility flag required by
`gaia dev evidence --help`; never convert a vendor benchmark claim into a
percentile without an independently verifiable benchmark source.

## Appraise, then stop

After the write:

```bash
PYTHONPATH=src python3 scripts/trust_appraise.py --skill <contributor/skill-id>
```

Report the new TM, Overall Trust Grade, per-row score, and whether the source
is implementation-specific. Propose a calibration only when Trust Magnitude clears
the gate and the Star Bar is met (the per-star Evidence Floor is retired under
Yggdrasil II — TM is the sole promotion gate). Do **not** run `gaia dev calibrate` without explicit
operator approval.

## Finalization

For a one-row standalone run, validate without regenerating unrelated artifacts:

```bash
GAIA_OPERATOR_OVERRIDE=1 gaia dev validate
```

For multiple rows, hand back to `/gaia-ingest-batch`, which performs exactly
one `gaia dev build` and final validation.
