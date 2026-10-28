---
name: apify-local-maps-lead-enrichment
description: Build checkpointed Google Maps lead lists for any local industry with Apify, then enrich websites, phones, emails, named contacts, and email verification results into outreach-ready exports. Use when creating, auditing, or resuming local-business lead generation workflows with cost controls.
---

# Apify Local Maps Lead Enrichment

Use this workflow to discover local businesses by industry and location, enrich their contact fields, and make the list outreach-ready.

## Procedure

1. Configure `config/example_industry.json` with industry search terms and include/exclude filters.
2. Prepare `locations.csv` with `geo_text` or city/county/state fields.
3. Run `src/maps_discovery.py --dry-run`, then one real batch with `--max-batches 1`.
4. Inspect `outputs/maps_discovery/checkpoint.json`, raw JSON, and parsed CSV.
5. Enrich rows that have official websites with `src/contact_enrichment.py`.
6. Verify candidate emails with `src/email_verify.py`.
7. Resume by rerunning the same command; succeeded batches are skipped.

## Guardrails

- Keep API tokens only in `.env` or runtime environment variables.
- Publish only synthetic examples.
- Do not rerun succeeded batches; recover or reparse raw outputs instead.
- Use small initial batches before overnight runs.

