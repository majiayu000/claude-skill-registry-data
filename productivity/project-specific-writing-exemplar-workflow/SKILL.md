---
name: project-specific-writing-exemplar-workflow
description: Build and route a manuscript-specific academic-writing exemplar corpus, with a single Core 3 approval gate and anti-copying controls. Use for substantive manuscript drafting, major rewriting, target-journal adaptation, or section restructuring when a project exemplar profile may be missing or stale.
metadata:
  short-description: Select and route project-specific writing exemplars
---

# Per-manuscript writing exemplar workflow

Use this workflow to route a manuscript through a private, isolated exemplar lifecycle and learn reusable scientific argument architecture from verified papers without turning source prose into a copying library. This is an orchestration subskill under the existing `agent-auto-sci-scicomm` writing owner, not a competing writing owner. Manuscript-specific facts, private corpus records, approval decisions, derived patterns, and research decisions belong in that manuscript's private state, not this public skill.

## Trigger and boundary

Trigger for substantive Introduction, Methods, Results, Discussion, Abstract, or major manuscript rewriting. Do not trigger for a typo, one-sentence grammar fix, citation-format change, reference-style change, simple caption correction, or simple translation.

Resolve a stable `MANUSCRIPT_ID` from explicit input, the active project's private state, canonical title/research question, and source-document identity. A filename, title string, or chat title alone is not a stable ID. If uncertain, mark `MANUSCRIPT_IDENTITY_UNCERTAIN`, do not inherit another skill, and seek only the minimum clarification. Read the one authoritative private state record; never infer the 20-paper list from chat memory. Codex and ChatGPT Web use this same record.

Before substantive writing, check whether the matching manuscript has a current project-specific exemplar profile/skill. If absent or stale, start that manuscript's initialization. If active, select 4–5 section-specific exemplars from that manuscript's own Master 20 and freshly read their relevant sections before drafting. Micro-edits bypass heavy workflow; an existing skill's lightweight constraints may be read.

## Lifecycle

`S0_UNINITIALIZED -> S1_MANUSCRIPT_PROFILED -> S2_CANDIDATE_POOL_READY -> S3_MASTER_20_SELECTED -> S4_CORE_3_PENDING_AUTHOR_APPROVAL -> S5_CORE_3_APPROVED -> S6_CORPUS_DEEP_ANALYSIS_COMPLETE -> S7_PROJECT_EXEMPLAR_SKILL_BUILT -> S8_ACTIVE_FOR_WRITING -> S9_REFRESH_REQUIRED`

Each manuscript independently builds a recommended 40–80-paper pool, selects exactly 20 for its own Master Corpus, then recommends Core 3 from that set. Stop in S4 until the author explicitly approves, replaces one/two, or rejects the Core 3 proposal. No deep analysis or major rewrite before approval. Approval is the only author gate and automatically unlocks Phase 2; do not ask again. See [workflow](../../../docs/workflows/PER_MANUSCRIPT_WRITING_EXEMPLAR_WORKFLOW_V1.md) and [state machine](../../../docs/workflows/PER_MANUSCRIPT_EXEMPLAR_STATE_MACHINE_V1.md) for transition, refresh, and storage contracts.

## Selection rules

- Build a broad pool before narrowing; deduplicate by DOI, then authoritative title/author/year checks.
- Prefer original empirical research and the user's verified Zotero/full-text sources. Use reviews sparingly for unusually strong synthesis architecture.
- Rank scientific-question, object, outcome, design, evidence-chain, planning/theoretical, target-journal, writing, and full-text proximity above impact factor.
- Keep `CORE`, `STRONG`, `SUPPORT`, and `EXCLUDE` as categorical states; never invent a pseudo-precise score.
- Core 3 should be scientifically closest and, where compatible, functionally complementary: story/question, evidence chain, and discussion/planning contribution.
- Record missing metadata or unavailable structure explicitly as `NOT_VERIFIED`, `FULLTEXT_NOT_YET_AVAILABLE`, or `PARTIAL`.

## Analysis boundary

Before approval, do not perform paragraph, sentence, lexical, phrase-frequency, or NotebookLM batch analysis. Do not create a project-specific writing Skill and do not modify the manuscript. After approval, analyze four levels: article story; paragraph functions (including what is lost if removed); sentence functions (why each sentence exists); functional lexical/phrase roles. Do not report ordinary word frequency as a learning result. After cross-paper quality review, patterns may be corpus-stable or high-quality/low-frequency. Never store long source passages or distinctive phrases. Explicit author constraints outrank frequency.

## Writing-time safeguards

Build `OUR_EVIDENCE_MAP` and `OUR_ARGUMENT_MAP` before exemplar comparison. For each substantive section, select a fresh set of 4–5 from this manuscript's own Master 20; Core 3 are preferred but not mandatory, and section sets may differ. Reread selected source sections and restore paragraph, sentence-function, and functional-lexicon maps. Follow `OUR_EVIDENCE_MAP -> OUR_ARGUMENT_MAP -> SECTION_EXEMPLAR_REFRESH -> STRUCTURAL_COMPARISON -> OUR_DRAFT_OR_REVISION -> ACADEMIC_PROSE_GUARD -> REDUNDANCY_AUDIT -> FIGURE/TABLE_CITATION_AUDIT -> FACT_PLACEMENT_AUDIT -> FINAL_CONSISTENCY_CHECK`. Do not transfer source claims, causal interpretation, results, citation chains, or distinctive wording. User constraints override frequency.

Detailed schemas and routing rules are in [references/schema.md](references/schema.md) and [references/routing.md](references/routing.md).
