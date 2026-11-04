---
name: Dedup
description: The cite-don't-restate pass for every phase artifact. Before writing each section, check overlap with prior-phase artifacts; replace restatement of framing/context with a one-line citation block that quotes the key claim and links to the source; NEW content (this phase's decisions, requirements, findings) gets the words. Consolidates the per-agent DEDUP PASS into one reusable skill. Targets ~30–40% average text reduction with zero loss of decisions or reasoning.
version: 1.0.0
author: Mattermost Design Team
tags: [consumability, token-efficiency, cite-dont-restate, all-phases]
allowed-tools: Read, Grep, Glob
---

# Dedup — cite, don't restate

## Purpose

About 30–40% of text bloat across the 8-phase system is **restatement** — the same problem framing, role recaps, and "why we're doing this" context written 5 times across Phases 1–7. This pass stops Phases 2–7 from re-narrating what an earlier phase already owns. The gist (1–2 sentences) stays inline as a quoted citation; the depth is one click away in the source artifact. **No detail is hidden — it is just not duplicated.**

This is a composable pass every phase agent invokes before writing each body section. It replaces the inline "DEDUP PASS" prose formerly copy-pasted into each agent.

## When to invoke

Before writing **each** body section of any phase artifact. Run it as a per-section check, not a one-time pass. (The skim layer at the top of the artifact comes from the `artifact-frontmatter` skill; this skill governs the body.)

## The procedure (per section)

1. **Read the prior content.** Read the relevant upstream artifacts in the spec state object (`state.artifacts.*`, brain dump, PRFAQ, prior intake rounds). Identify what overlaps with the section you are about to write — problem framing, role recaps, "why we're doing this" context, compliance scope, control mappings, requirements, solution-direction context already stated upstream.

2. **Classify the overlap.** Decide which of three buckets it falls in:
   - **Framing / context** (problem recap, role lists, "why," prior scope) → **cite, do not restate** (step 3).
   - **Load-bearing for this phase** (e.g., a requirement that must restate a control mapping for traceability) → **keep it, but mark it** with an inline `(from Phase N § X)` marker so the reader knows the duplication is intentional.
   - **NEW content** (this phase's unique contribution) → **give it the words** (step 4).

3. **Replace restatement with a citation block.** Use this exact one-line format:

   > **<Topic> →** see [Phase N § <Section>](../<N>-<artifact>.md#<anchor>) — *"<≤15-word direct quote of the key claim>"*

   The blockquote is **one line**. The quote anchors the gist inline (~10–15 words of evidence); the link offers the depth. Link by stable phase + anchor so the reader can click through for the long version. In rendered markdown and Confluence this shows as a stylized blockquote with a backlink.

4. **NEW content gets the words.** Frame each section around what THIS phase contributes — requirements, threat vectors, evaluation rationales, flow diagrams, edge cases, behavior — with upstream citations as backing context, not as re-explained preamble. Never open a section by paraphrasing an earlier phase as your own framing.

## The highest-leverage target: the opening summary

The Executive Summary / §1 / BLUF of each artifact is the worst restatement offender. **Open it with a single citation block back to the source's BLUF — not a rewrite of it.** The summary's job is to state what THIS artifact scopes, not to re-explain the problem.

**Before** (218 words; first ~150 restate the Phase 1 problem):

> ABAC policy admins serving Five Eyes defense customers cannot author policies that match how their organizations structure authority… [120 more words of problem recap] … This PRD scopes v1.0 ranking and v2.0 hierarchy…

**After** (64 words; 70% cut on this worst-case section):

> > **Problem:** see [Phase 1 § BLUF](../01-problem-statement.md#bluf) — *"ABAC policy admins cannot author access policies that match how their organizations structure authority…"*
>
> This PRD scopes a single phased release: **v1.0 (June) — Attribute Ranking** … **v2.0 (July) — Hierarchical Structures** … Audit content is non-negotiable from day one; fail-secure on stale data is the only stale-data behavior in scope.

Every load-bearing claim survives; only the restatement of Phase 1 is removed.

## Self-resolving references (conventions.md §5)

Dedup and self-resolving references are the same discipline applied two ways. When you DO cite a requirement, edge case, threat, or control code, **never leave it bare** — carry its meaning at the point of use:

- Write `FR-10 (admins bulk-assign attributes by policy)`, not `FR-10`.
- Write `EC-21 (offline token expiry mid-mission)`, not `EC-21`.
- Write `AC-2 (account management)`, not `AC-2`.

A reader skimming one section must never scroll to a glossary or open another file to understand a cited code. IDs are assigned once (in the PRD) and reused unchanged downstream, so every citation resolves to a single definition.

## Honest calibration (do not over-claim)

- The **70%** figure above is a worst-case single restatement section — illustrative, not generalizable.
- The realistic **average across all artifacts is ~30–40% reduction**, because not every section is restatement. Report dedup wins against the 30–40% range, never the 70%.
- Compounded across 5 phases × multiple specs × dozens of cross-references, the 30–40% average still adds up meaningfully.

## What dedup does NOT do

- **Does not delete the source.** Phase 1's BLUF still lives in Phase 1. Dedup only stops Phases 2–7 from restating it.
- **Does not break standalone reads.** Each artifact still carries its `artifact-frontmatter` skim layer (TL;DR), so a reader landing in Phase 3 cold still gets the gist without leaving the page.
- **Does not collapse decisions or requirements.** Those are the *unique* content of each phase — they get the full words. Dedup targets *framing prose* only (problem context, "why," role recaps), never load-bearing content.
- **Does not paraphrase to dodge a citation.** Re-wording an upstream paragraph to avoid quoting it is a dedup failure, not a pass. Cite it.

## Phase-specific high-value targets (apply where relevant)

- **Phase 2 Research:** problem framing, affected roles, and compliance scope already in Phase 1 → cite. NEW = standards/controls table, competitive intel, gap analysis.
- **Phase 3 PRD** (heaviest offender): §1 Executive Summary → single citation to Phase 1 BLUF. NEW = requirements, threat vectors, pre-flight findings, `[VERIFY WITH PM]` flags.
- **Phase 4 Ideation:** PRD constraints → cite per option, don't re-discover them. NEW = approach differentiation, evaluation matrix rationales, BLUF recommendation, top-3 risks.
- **Phase 5 Flows** (second-heaviest): routing logic as 6+ prose paragraphs is a **dedup failure mode** — express it as a Mermaid decision tree + branch table. ASCII mockups are NEW content; the prose around them is duplicative of the diagram — favor the diagram. NEW = flow diagrams, state matrices, per-story coverage, security findings (P1/P2/P3).
- **Phase 6 Prototype:** code is the artifact and is exempt; the accompanying writeup is in scope. Per-option writeups focus on what THIS option does differently. NEW = component inventory, state-matrix descriptions, build status.
- **Phase 7 Spec:** the spec communicates BEHAVIOR — it does not re-narrate the problem, re-list requirements, or re-explain controls (the PRD did that). Mockup/Figma references replace descriptions. The Tier-1 compliance appendix is the one place comprehensive citation back to Phase 2 is appropriate — even there, a linked table, not re-narration. NEW = admin/end-user behavior, edge cases, terminology lock-down.

This pass is enforced at gate review: artifacts that restate prior content without citation are flagged for revision.
