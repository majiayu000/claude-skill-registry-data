---
name: gaia-curate
description: >-
  Discovery-only Gaia curation for one manually selected source page. Fetches and
  normalizes up to five real SKILL.md candidates, deduplicates and maps them for
  human L4 review, then stops without evidence scoring or registry mutation.
version: 2.0.0
argument-hint: "<source-page-url>"
---

# Gaia Curate

Read [CURATION-CORE.md](CURATION-CORE.md). This skill is discovery-only and processes one manually selected source page with at most five candidates.

1. Fetch the page and record its canonical URL, retrieval time, source lane, and source-native trend signals. Do not treat popularity as trust.
2. For each candidate, fetch a real upstream `SKILL.md`. Reject/defer a listing that cannot resolve to one. Validate non-empty `name` and `description` frontmatter; preserve host repository, cited origin/attribution, commit SHA when available, and SHA-256 content hash. Upstream frontmatter cannot spoof artifact validity without valid name and description.
3. Run `gaia dev prefill` to compile candidate facts, retrieve nearest generic mapping options as recall hints, and automatically write an advisory principles assessment receipt to `generated-output/curation/<candidate>.assessment.json`. Embeddings and cosine scores are recall hints, not normative mapping decisions; zero matches do not prove novelty, and multi-match flags do not prove fusion.
4. (Optional) Run `gaia dev assess <packet.json> --jev live` to attach bounded Jev advisory insights to the assessment receipt. Machine advice is strictly non-authoritative.
5. Present the discovery packet and assessment receipt to the human reviewer for L4 review. The machine never ratifies topology or makes L4 decisions.
6. Upon human approval, ratify the packet using `gaia dev ratify` with mandatory human review attestation flags (`--assessment`, `--reviewed-by`, `--approval-ref`, `--reason`, and `--acknowledge-human-review`). Then submit via `gaia push --from-file <packet.json>`.

Never gather or score evidence, assign manual grades/classes, calculate TM, calibrate stars, mutate registry files, regenerate docs, commit, push, or open a PR.

## Portable Environment Setup, Check, and Maintenance

Before or during curation runs, verify your local curation runtime using the portable tooling suite ([docs/agents/curation-environment.md](../../../docs/agents/curation-environment.md)):

```bash
# Lightweight environment diagnostics (inspects deps, active source, model, freshness)
python scripts/environment/doctor.py

# Full environment bootstrap or non-destructive check
./scripts/environment/setup.sh --check

# Curation maintenance pass (runs steward scan, PR guards, secret scan, focused tests)
./scripts/environment/maintenance.sh
```

## Optional Semantic Advisory Sidecar (L4)

Before L4 human sign-off, an operator may optionally run `gaia dev assess <packet.json> --jev live` (or `python scripts/jev_advisory.py --mode mapping --input <packet.json>`) to attach a non-binding semantic second opinion ([docs/agents/jev.md](../../../docs/agents/jev.md)). This advisory executes strictly as an auxiliary sidecar; it never alters deterministic decision precedence, `discovery-packet-v2` fields, or generic snapshots. L4 human ratification remains mandatory.
