---
name: wall-guard
description: Use before any commit touching research endpoints, answer schemas, prompts, or retrieval code in Athena (qa.py, find.py, compare.py, router.py, repository.py) — and whenever output could rank, score, or judge companies rather than cite what filings say.
---

# Wall Guard — the Evidence/Judgment Wall

## The rules (verbatim from CLAUDE.md — load-bearing, never compromise)

- The evidence layer (cited QA, change detection, FIND, COMPARE) is
  structurally separate from any future judgment layer.
- **No verdict fields anywhere in evidence-layer schemas.** No buy/sell/hold,
  no price targets, no attractiveness ranking, no evaluative language in
  Athena's own voice (attributed source language, cited, is fine — ADR-0007 §3).
- FIND results are ordered by `match_strength` — a retrieval fact about how
  well filing TEXT matched the query — never by company judgment.
  `apps/api/research/find.py` must never import an answerer module; the
  zero-answer-model path is its contract (ADR-0011 §1).
- COMPARE synthesizes per-column behind a `(filing_id, query)` seam with no
  passage parameter, so cross-company ranking is unrepresentable; no
  superlatives (most/best/least/worst), no computed ordering, caps enforced
  as REFUSALS, never silent truncation (ADR-0012).
- A future judgment layer requires its own ADR, must be labeled as judgment,
  builds only on evidence-layer outputs, and uses read-only market data
  (FMP/Finnhub/Polygon/FRED — never Trading 212).
- **Prefer structural enforcement over test enforcement:** make violations
  impossible by construction (draft/resolved citation split in change
  detection; import boundaries in FIND; the no-passage-parameter seam in
  COMPARE), not merely caught by tests.

## Pre-commit checklist (run for any commit touching research endpoints)

- [ ] No verdict, ranking, score, or attractiveness field added to any
      evidence-layer schema or response model.
- [ ] `find.py` imports no answerer module (`grep -n "answerer\|summarizer" apps/api/research/find.py` → only the docstring).
- [ ] COMPARE's synthesis seam still takes `(filing_id, query)` — no passage
      parameter; entry assembly stays model-free; no model output feeds a
      model call.
- [ ] No most/best/least/worst/stronger/weaker or ordering-by-attractiveness
      language in outputs or prompts; evaluative words appear only as
      attributed source language with a citation.
- [ ] Caps are min()-clamped ceilings and over-cap requests are REFUSED with
      a clear message — never silently truncated.
- [ ] Every emitted claim cites a `source_url` stamped from the database
      (draft labels → resolved provenance), never model-copied URLs.

## The test (ADR-0007 §3 / ADR-0011 §5)

Whose judgment does the answer carry? Stating what each filing says, cited,
is evidence work. The SYSTEM picking "most exposed" or "best positioned" is
judgment — out of scope even when every underlying fact is citable. The
in-scope answer is each company's cited language, ordered by nothing.

| Rationalization | Reality |
|---|---|
| "Every underlying fact is cited, so the ranking is grounded" | A superlative requires Athena to judge across companies; that's the wall. |
| "The user asked which is most exposed" | Answer with each company's cited exposure language and say the verdict is theirs (ADR-0007 §2). |
| "Silently trimming to the cap is friendlier than refusing" | A truncated comparison the user believes complete is silent wrongness. Refuse, name the cap. |
| "A prompt instruction not to rank is enough" | Prompt discipline is the rejected shape (ADR-0012 #6b). Hold walls structurally. |
