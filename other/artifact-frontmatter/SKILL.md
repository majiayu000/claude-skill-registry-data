---
name: Artifact Frontmatter
description: Emits the skimmable two-layer skim block at the TOP of every phase artifact — TL;DR, phase + complexity tier, what-changed-since-last-version, decisions locked (and which flipped from a Recommended default), open [VERIFY WITH PM] items, and a one-line reading guide. Goal — a reader answers what / phase / what-changed / what's-open in under 60 seconds without reading the body. Composable; phase agents invoke it as their first output step.
version: 1.0.0
author: Mattermost Design Team
tags: [consumability, skim-layer, two-layer, frontmatter, all-phases]
allowed-tools: Read, Grep, Glob
---

# Artifact Frontmatter — the 60-second skim layer

## Purpose

Every phase artifact opens with a **skim layer** before any prose (conventions.md §6, two-layer outputs). The reader gets the gist in under a minute; the detailed body follows for anyone who needs to dive in. This skill produces that block. The body is the deep layer; this is the skim layer. Never make the reader parse the whole body to find the decision.

**The 60-second test:** a reader who reads ONLY this block can answer four questions —
1. **What** is this artifact about? (TL;DR)
2. **What phase / tier** is it? (header strip)
3. **What changed** since the last version? (what-changed)
4. **What's still open?** (open `[VERIFY WITH PM]` items)

If a reader cannot answer all four from the block alone, the block has failed — compress and re-emit.

## When to invoke

The phase agent invokes this skill as the **first output step**, before writing any body section. The block is mechanically derived from the spec state object — it is not hand-prose. Re-emit it whenever the artifact is regenerated (e.g., a v2 PRD after `[VERIFY]` resolution) so what-changed stays accurate.

## The block (fixed order)

Emit in this order. Keep the whole block to **one screen (~50 lines markdown)**; if it overflows, run the compression pass (below) — the budget is the skim layer only, never the body.

### 1. YAML header strip + title + `[AI DRAFT]` label

```
---
spec: <meta.feature_name slug>
phase: <N> — <Phase name>
tier: <Tier label> · <meta.mission_tier>          # e.g. Tier 2 — Standard Spec · IL5
status: <phase.status> · <gate note if any>
artifact: <artifact name + version>
generated: <ISO 8601 timestamp>
---

# <Feature Name> · <Artifact + version>

> **[AI DRAFT]** — Auto-generated skim layer. <one clause on body provenance, e.g. "Body is the human-curated artifact." or "All N [VERIFY] items from vN-1 resolved.">
```

The `[AI DRAFT]` label is **mandatory** on every block (per the `defense-ux-context` skill's Output Rules — label all AI-generated content until human-reviewed).

### 2. TL;DR (60-second scan)

`## TL;DR (60-second scan)` — **2–3 sentences.** What this artifact decides/scopes, the load-bearing constraint, and (if relevant) what's deliberately out. Plain language; lead with the BLUF. Bold the one phrase the reader must not miss. This is the single highest-leverage line in the artifact — write it last, after the body, so it reflects what the artifact actually says.

### 3. What changed since last version

`## What changed since <prior version>` — a small table or tight bullets. Source: diff against the prior artifact version + resolved `context.open_questions`. For a **first version** with no prior, replace with `## Decisions locked this phase` (below) and state "First version — no prior to diff." Resolved `[VERIFY]` items show their resolution; **dropped** scope shows "**Dropped.**"; flipped decisions show "**Flipped.**".

### 4. Decisions locked (flag flips from Recommended)

`## Decisions locked this phase` — table of the phase's `context.key_decisions[]`. For any decision the user chose **against** the agent's Recommended intake default, tag it **Flipped** (or **Scope expansion** if it widened scope). This is load-bearing: a reviewer needs to see at a glance where the human overrode the default. Example rows:

| # | Decision | Notes |
|---|---|---|
| Q6 | Top of list = highest precedence, fixed (no toggle) | **Flipped** from agent recommendation |
| Q9 | Visual builder AND raw CEL are equal first-class surfaces | **Flipped**, doubles editor scope |
| Q8 | Strict additive inheritance — no child override | matches existing policy stacking |

If the full decision set is long, show the flipped/expansion rows here and point to the body: "Full table in body § Intake Clarifications."

### 5. Open `[VERIFY WITH PM]` items — pinned, never buried

`## Open going into Phase <N+1>` (or `## [VERIFY WITH PM] — pinned, do not bury` when there are several). Scan the body for every `[VERIFY WITH PM]` / `[VERIFY WITH ENG LEAD]` flag and list each as one line: the question + who must decide + what it blocks. If none: `None blocking.` plus any P2 polish item. **Never** let a `[VERIFY]` flag live only in the body — it must surface here (per `defense-ux-context`: flag `[VERIFY WITH PM]` items at the top, not buried).

### 6. Reading guide (one line, or a small time-budget table)

`## Reading guide` — at minimum one line: "If you only have 5 minutes, read this block; for the decision rationale, body § X." A time-budget table is the richer form:

| If you have… | Read |
|---|---|
| 5 min | This block. Stop here for gate sign-off conversation. |
| 20 min | Add body § Executive Summary, § Scope, § Out of Scope |
| Full pass | Body in full (~N words). The grounding in § X is load-bearing. |

### 7. Source artifacts (linked, not restated)

`## Source artifacts` — one bullet per upstream artifact this phase consumed, each a link by phase + anchor. This is the skim-layer companion to the `dedup` skill: the block links sources; the body cites them inline. Never restate an upstream artifact's content here — link it.

## Compression pass (when the block overflows one screen)

If the block exceeds ~50 lines: (a) collapse the decisions table to flipped/expansion rows only, pointing to the body for the rest; (b) drop the time-budget table to a single reading-guide line; (c) tighten TL;DR to 2 sentences. Never drop the `[AI DRAFT]` label, the open-`[VERIFY]` section, or any flipped-decision row — those are load-bearing.

## What this skill does NOT do

- **Does not write the body.** It emits only the skim layer; the agent writes the deep layer below the closing `---`.
- **Does not invent content.** Every line traces to the spec state object or the body. If a field is empty (no decisions, no opens), say so explicitly ("None blocking.") — never fabricate.
- **Does not duplicate upstream content.** Source framing is linked (§7), not restated — that is the `dedup` skill's job, applied in the body.

## Self-resolving references (conventions.md §5)

Inside the block, never emit a bare internal code. Every `FR-`, `EC-`, threat, or control ID carries an inline gloss at the point of use — `FR-10 (admins bulk-assign attributes by policy)`, not `FR-10`. A reader skimming this block must never have to open another file to understand a cited code.
