---
name: evidence-research
description: Build and validate a durable CLAIM ledger for documentary, historical, technical, educational, press-kit, festival, and campaign facts, preserving sources, uncertainty, disagreement, adoption state, and downstream use.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Evidence Research

1. Read `../../references/RESEARCH_RULES.md` and `../../references/EVIDENCE_RESEARCH.md`.
2. Define the research question and current project assumption.
3. Research with source quality appropriate to the claim.
4. Add or update `CLAIM-###` records in `01_story/research/claims.jsonl`.
5. Preserve disagreement and uncertainty instead of forcing consensus.
6. Connect adopted claims to scenes, narration, documents, or campaign records through `used_by`.
7. Run `scripts/claim_ledger.py PROJECT` before public-facing use.
8. Do not let a research note silently alter canon.

Done when every material public claim has traceable evidence or an explicit unresolved/creative status.
