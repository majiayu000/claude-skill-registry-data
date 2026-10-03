---
name: docs-architecture-audit
description: Use when verifying a project's reference docs still match the code — after a refactor or rename, on suspected doc drift, before trusting a doc as current, or as a periodic doc-health pass. Assumes the docs-architecture conventions (a CLAUDE.md router + charter'd reference set).
---

# Docs-architecture audit

Audit reference docs on two axes, judged separately — **placement** (does each section match its
doc's charter?) and **currency** (does each claim still match the live code?) — producing an
evidence-carrying flag list the user adjudicates, then applying the approved fixes. A single
careful pass finds only ~half the real issues, non-deterministically; per-flag judgment is what a
capable agent already does well, so the rules below force what one pass can't give:
**completeness, and a mergeable, consistent output**.

## Discipline — highest priority; violations poison the run
- **R1.** Every currency flag carries a code citation (`file:line` / symbol) **or** the literal
  `unverifiable → ask user`. Never guess stale.
- **R2.** Judge by content, not filename. *(A name only prioritizes what to read first.)*
- **R3.** Edit **documentation only** — never source, first-party or vendored. *(Code findings
  are reports, not fixes.)*
- **R4.** Report-only actions are exactly `flag-code-bug` and `revisit-plan`: handed off (to the
  dev/diagnose flow and `whats-next`), never auto-applied.
- **R27.** Surviving report-only flags are **persisted to the target project's own tiers
  before the run ends** — full flags + evidence in a dated `docs/YYYY-MM-DD-audit-report.md`,
  plus one line per adjudicated-surviving finding in the ROADMAP's open/backlog list,
  deduplicated against lines already there; adjudication deferred → a single open-list line
  pointing at the report. *(A hand-off that lives only in the chat dies with it — the doc
  system is the bug tracker; `whats-next` sweeps both homes.)*

## Currency — claim vs code
- **R5.** Classify modality first. **Descriptive** = how the system *is* (present tense;
  ARCHITECTURE, gotchas, "current status"). **Prescriptive** = how it *should/will* be (future
  tense; ROADMAP "Future", plan docs, open follow-ups).
- **R6.** Descriptive: **code wins** — a mismatch is a stale doc → `fix-doc`.
- **R7.** Exception — contracts: a guarantee the doc asserts (`must` / `always` / `never` /
  aborts-on-X, ideally with rationale, or corroborated by a test or another doc) that the code
  *violates* → `flag-code-bug`; the **code** is the suspect. Never `fix-doc` a contract into
  agreement with suspect code. *(That encodes the bug into the spec.)*
- **R8.** Plain value drift with no guarantee (a count, an intentionally-changed default/path) →
  `fix-doc`; unsure which case → `unverifiable → ask user`.
- **R9.** Prescriptive: **the plan wins** — code-not-matching is expected, never staleness. Plan
  already satisfied by code → `graduate` (an ordinary doc edit once adjudicated: move to
  "Recently shipped" / archive the plan). Plan contradicted by current structure →
  `revisit-plan`. *(Don't edit intent.)*
- **R28.** `fix-doc` on a stale value that is **cheaply derivable** (one grep re-derives it —
  a count, a version, an enumerated list) **and rationale-free** (no why, guarantee, or
  gotcha attached) → the proposed fix **leads with removing or de-valuing the claim** (keep
  the durable statement — "a curated station registry", not "12 stations"), with the
  value-update as the stated alternative. A value carrying rationale, contract force (R7),
  or gotcha weight gets a normal fix. *(Re-caching a rationale-free grep is drift deferred,
  not cured; only the fix-shape changes — flag, evidence, adjudication unchanged.)*

## Placement — section vs charter
- **R10.** Off-charter section → `move-to <doc>`, or `cross-ref+delete`. *(Single-source every
  fact.)*
- **R11.** `extract-cold` (propose a dated `docs/` cold doc + a one-line reference back) only
  when a section is lengthy **and** cold **and** evergreen — all three; a short, warm, or
  code-coupled section stays put.
- **R25.** A reference doc embedding a **growing dated shipped-history** (e.g. inside ROADMAP)
  is **one structural placement flag** → `move-to CHANGELOG.md` — the embedded entries are
  **not** currency-flagged individually. *(The entries are journal-tier; the structural
  misplacement, not per-entry drift, is the finding — per-entry flags bury it.)*
- **R26.** The `CLAUDE.md` router is **itself placement-audited**: reference content embedded
  in it (glossary, contract/API prose, conventions, subsystem mechanics — anything neither
  routing nor a load-bearing gotcha) → **one structural flag per block** → `move-to <charter
  home>`. Never per-fact *placement* flags, and never flag routing lines or gotchas,
  regardless of router size. Currency flags on stale claims inside the block remain
  legitimate — unlike R25's journal-tier entries, router-embedded reference content is
  reference-tier; the two axes stay judged separately.

## Scope
- **R12.** In-scope = what the `CLAUDE.md` router names, ∪ the canonical reference set.
- **R13.** Default-exclude *unrouted* files in vendored trees (`vendor/`, `third_party/`, forked
  upstreams), generated output (`bin/`, `obj/`, `dist/`, `target/`), and tooling (`.claude/`,
  `openspec/`). A router-named leaf inside them *is* in scope.
- **R14.** Never currency-audit the journal (`docs/`, `NOTEBOOK.md`, `CHANGELOG.md`) or
  archives (`archive/`, `openspec/changes/archive/`). *(Append-only, legibly historical.)*
- **R15.** Cold-rationale docs a reference doc cites: follow the citation and run a
  **decision-consistency check only** — does the reasoning still support the decision? A
  code-coupled fact (file / function / flag / value) inside one → flag as a **tier violation**.
  *(Cold docs escape the currency sweep.)* Exception — an archived openspec design doc
  (`openspec/changes/archive/*/design.md`) gets the consistency check **only**: its
  code-coupled facts are design-time values, never tier violations (dense with them by
  design; an immutable change record — never edit it; standing truth inside it is the
  MAINTAIN graduate path's job, not a flag).
- **R16.** A sub-project (own router / `.git`) → flag-and-skip; audit it from its own dir.
- **R17.** Vendored *source* is read-only ground truth — check against it, never edit it.

## Coverage — why this skill exists
- **R18.** Never trust one careful pass — or any fixed N of them. *(Each finds a different
  ~half.)*
- **R19.** Fan out **per-section** workers (forces depth everywhere; whole-doc replicates skim),
  plus **one cross-reference pass** over inbound referrers — routers, other docs, source/UI
  files — for rename-orphans and dangling links.
- **R20.** **Loop until dry**: run rounds until one adds nothing new. *(Even three replicate
  passes each missed real flags; ground truth ran ~30% larger than any single run.)*
- **R21.** A dry round is *that model's* ceiling, not truth — **switch worker model** before
  concluding. **Same-model cross-worker convergence is agreement, not completeness.** *(Two
  models' ~20-of-25 unions shared only ~16; the full union needed both.)*
- **R22.** Worker default: a strong, fast tier at **high** reasoning effort (Claude: Sonnet at
  high) — per-pass parity with a frontier tier, faster convergence, discipline intact. Medium
  effort / the cheapest tier (Claude: Haiku) are a **first sweep only**. *(Medium's ceiling ran
  ~3 real issues below high; cheap tiers skip sections and mislabel actions — iteration doesn't
  fix discipline.)*
- **R23.** **Retry a dead worker once** (a transient API error returns null/empty, and merges
  silently filter it); still dead → name the uncovered span in the coverage note. *(A visible
  gap beats false completeness.)*
- **R24.** Every worker returns flags **in the schema below**. *(Prose doesn't merge across a
  fan-out.)*

## Procedure
1. Fan out per-section workers + the cross-reference pass (R19, R22); collect schema'd flags.
2. Merge + dedup — same location + claim = one flag; log anything dropped.
3. Loop until dry, then diversify the worker model (R20–R21). End with a **coverage note** in
   the adjudication report: any span whose worker died after retry, and what covered it instead
   (R23).
4. **Adjudicate**: present the merged list; the user **approves / amends / defers** each flag's
   proposed action.
5. **Apply** approved doc fixes; re-verify. Report-only flags are never applied to docs —
   **persist them (R27)**, then hand off (R4).

## Flag schema — every flag, every worker
```
- location:  doc § + quoted phrase
- axis:      placement | currency
- modality:  descriptive | prescriptive          (currency flags)
- claim:     what the doc asserts
- finding:   what's wrong, or the off-charter target home
- evidence:  file:line / symbol   OR   "unverifiable → ask user"
- severity:  high | medium | low
- action:    fix-doc | move-to <doc> | cross-ref+delete | graduate | extract-cold | revisit-plan | flag-code-bug | keep
```

Full rationale + RED/GREEN provenance:
https://github.com/Apoplectic1/YetAnotherSkillsRepo/blob/main/docs/docs-architecture-design.md
