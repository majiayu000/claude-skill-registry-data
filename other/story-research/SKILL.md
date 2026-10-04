---
name: story-research
description: Research factual, historical, technical, cultural, location, or craft details needed by a story or screenplay, recording source type, confidence, conflicts, contradictions, gaps, and production-relevant implications.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Story Research

Use when a creative decision depends on real-world facts or when the project needs grounded detail it does not yet have.

## Workflow

1. Read `../../references/CORE_CONTRACT.md`, `../../references/RESEARCH_RULES.md`, the brief, and the story assumptions relevant to the question.
2. Write the exact research questions before searching.
3. Prefer primary, official, scholarly, or practitioner sources according to the question. Use current sources when the fact can change.
4. Separate verified fact, supported interpretation, contested claim, anecdotal detail, creative inspiration, and project decision.
5. Record credible disagreements instead of flattening them into one answer.
6. Save `01_story/research/<topic>.md` with: question, usable findings, source notes, confidence, conflicts, contradictions with current story assumptions, gaps, and story implications.
7. Update canon only for facts or creative decisions the project has explicitly adopted.

## Done

Every adopted factual constraint names its source or evidence class, uncertainty is visible, and the writer can use the note without repeating the research.

## Evidence ledger handoff

When research will support documentary narration, historical claims, press materials, social copy, a pitch, a treatment presented as factual, or any other public factual statement, route adopted claims through `evidence-research` and `01_story/research/claims.jsonl`. Research notes may remain richer than the ledger. The ledger exists to make public-use evidence and uncertainty machine-checkable.

