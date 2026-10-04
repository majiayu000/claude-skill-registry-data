---
name: adjust-level
description: Adjust the difficulty level of a learning sub-project's curriculum — simplify a too-advanced curriculum into a gentler on-ramp, or deepen a too-introductory one into something with real teeth. Use whenever the user signals the curriculum's level doesn't match their starting point — phrases like "this paper is too hard, can we build up to it?", "simplify the curriculum", "make it easier", "go more advanced", "I want a more rigorous version", "this is too basic, push deeper", "I need an intro version of this", or "create a simpler/harder curriculum from this material". The skill is allowed to pull in external materials and training knowledge to fill the gap between the source's natural level and the target level, but every external addition is explicitly labeled — the user always knows what came from their own source materials and what came from elsewhere.
---

# Adjust the level of a sub-project's curriculum

This skill rewrites a sub-project's `curriculum.md` at a different difficulty level than the source materials naturally support — either simpler (build up to a hard source) or more advanced (extend beyond an introductory source). It is allowed to draw on external materials and training knowledge to fill the gap, but **every externally-sourced piece of the curriculum must be explicitly labeled** so the user always sees the provenance of what they're being asked to study.

## When to use

The user wants the curriculum at a different level than the source materials directly support. Two common cases:

- **Simplify** — they have a dense scientific paper (the "summit") and want a gentler ascent that introduces the prereqs the paper assumes, builds intuition, and ends at the paper itself. *"This paper is too dense, can we build up to it from the basics?"*
- **Deepen** — they have introductory notes or a textbook chapter and want to go beyond it, with more advanced topics, missing rigor, and adjacent material. *"This textbook is the floor; I want to climb higher."*

If the user just wants the curriculum to better match their source materials (without shifting level), use `set-curriculum`, not this skill.

This skill is **not a session** — it does not update `PROGRESS.md`.

## What you need from the user

**Required:**

- The **sub-project name** to adjust. If the user did not name one, **ask** — never guess or default to "all sub-projects".
- The **direction**: simpler or more advanced. Phrases like "make it easier" / "build up to" / "intro version" → simpler. "Go deeper" / "more rigorous" / "push harder" → more advanced. If the direction is genuinely ambiguous, **ask one short question** before proceeding.

**Optional:**

- A **target level** if the user supplies one: *"high school", "first-year undergrad", "graduate", "explain like I'm 12", "research-level"*. Use as a north star for how aggressive the shift should be.
- **Specific gaps or extensions** the user has in mind: *"I don't have the probability background", "I want more on phase transitions"*. Use these as anchors for where to add or remove material.

## What to read before writing anything

1. The sub-project's `.studyenv/<name>/AGENTS.md`, falling back to `.studyenv/<name>/CLAUDE.md` for older projects — for `Domain:`, `Language:`, learning goals, Tools & Materials.
2. The current `.studyenv/<name>/ai-agent-materials/curriculum.md` — the baseline being adjusted. If it doesn't exist, redirect the user to `set-curriculum` first — there is nothing to adjust yet.
3. Any source extractions in `.studyenv/<name>/ai-agent-materials/` (concept maps, copied excerpts) — these remain ground-truth for what the user's source actually covers.
4. The user's `.studyenv/<name>/source-materials/` — to keep firm what is in-source vs. what will be brought in.
5. The harness conventions at `../../reference/conventions.md` — for the curriculum format and the **External-source labeling** rules. The labeling rules are not optional; read them.

## How to do the adjustment

### Simplifying down

The user's source material is the **summit**; you're designing the ascent.

1. List what the source **assumes** — concepts, vocabulary, mathematical apparatus, domain knowledge it expects the reader to already have. These become explicit prerequisites.
2. Find or invent **bridging topics** that bring a less-prepared reader from a plausible starting point up to those prereqs. Most of these will not be in the source — they will come from training knowledge or external references, which you cite per the labeling rules.
3. **Decompose** dense topics in the source into smaller, sequential sub-topics. A single source section may become 3–5 curriculum topics at the simpler level.
4. Order the curriculum so each topic depends only on prereqs that appear earlier. The original source material becomes the final stretch.

### Deepening up

The user's source material is the **floor**; you're designing the climb above it.

1. Consolidate what the source **covers comprehensively** — those become the foundation, often fewer, larger topics.
2. Identify what the source **mentions in passing** or **doesn't cover** — those become candidates for new advanced topics.
3. Bring in **adjacent material** from training knowledge or external sources: related results, generalizations, applications, current research. Cite each one.
4. Add **rigor** the source didn't develop: missing proofs, edge cases, more general formulations. Cite where this rigor comes from.

### In both directions

- **Preserve existing topic ids** where the underlying concept is unchanged. If the old curriculum had `T3: mean-field closure` and the adjusted curriculum still has the same topic (possibly with different prereqs or framing), keep it as `T3`. This protects existing `PROGRESS.md` references.
- **Insert new topics** with new ids at the appropriate position: `T2.5` between `T2` and `T3`, `T8` after the previous last topic. Do not renumber existing topics.
- **Mark removed topics** as `[deprecated]` in the topics table rather than deleting them, if `PROGRESS.md` references them. Otherwise delete cleanly.

## External-source labeling (the heart of the skill)

Every piece of the adjusted curriculum that did **not** come from the user's source materials must be labeled. The format is documented in detail in [`../../reference/conventions.md`](../../reference/conventions.md) (*External-source labeling*); the summary:

- Each topic carries a **Sources** entry listing where its material comes from.
- **In-source** entries name the source file and anchor: `paper.pdf §3.2`, `lecture-notes.md ch. 4`.
- **External** entries are prefixed `[ext]` and **name the source concretely**:
  - `[ext] Krapivsky, Redner & Ben-Naim, *A Kinetic View of Statistical Physics*, ch. 7` (a specific book)
  - `[ext] Wikipedia: Markov chain (https://en.wikipedia.org/wiki/Markov_chain)` (a web page)
  - `[ext] training knowledge — general background in measure theory` (training knowledge, no specific cited source)
- **Exercise hooks** that draw on external problem sets or examples are labeled the same way.

Training knowledge counts as external. **Do not let trained material drift in unlabeled.** If you're using your own pattern-recognition to add a topic the user's source doesn't cover, that topic gets a `[ext] training knowledge — <area>` label, no exception.

**Never invent citations.** If you genuinely don't remember the source of a piece of background knowledge, label it as training knowledge with a description of the domain area, rather than fabricating an author, title, or page number. A fabricated citation is worse than an honest "training knowledge — combinatorics background".

When in doubt about a topic's provenance, default to labeling it external. False positives (over-labeling) are recoverable; under-labeling silently misleads the user about what's in their material.

## Writing the new curriculum

1. **Back up the existing curriculum** to `.studyenv/<name>/ai-agent-materials/curriculum-prev.md`, overwriting any previous backup. The user can revert with one `cp` if the adjustment doesn't land.
2. **Write the adjusted curriculum** to `.studyenv/<name>/ai-agent-materials/curriculum.md`, replacing the file. Follow the standard curriculum format (see `../../reference/conventions.md`).
3. **Add a header note** at the top of the new curriculum stating: the adjustment direction (simpler / more advanced), the target level if the user specified one, and a one-line summary of what kind of external material was brought in. This makes it obvious to the user (and future agents) that this curriculum isn't source-faithful in the way `set-curriculum` produces.
4. **Do not modify** `PROGRESS.md` or any sub-project file other than the curriculum and its backup. Adjusting the curriculum is not a session.

## After writing

Tell the user concisely:

- The high-level shape of the change: how many topics added, removed, or kept; what flavor of external material was brought in (textbooks, web pages, training knowledge).
- Where the backup is (`.studyenv/<name>/ai-agent-materials/curriculum-prev.md`) and how to revert (`cp curriculum-prev.md curriculum.md`).
- A pointer to glance through the curriculum and confirm the external sources are ones they're happy to study from.
- If any external citation was a best-guess from training knowledge rather than a specific source you're confident about, flag that explicitly in the summary so they know to verify.

## Why these rules

- **Source-fidelity matters even when adjusting level.** The user gave you their source materials deliberately; quietly substituting your trained material undermines their choice and their epistemic control.
- **Topic id preservation** prevents the user's existing `PROGRESS.md` from becoming a museum of dead references. If they exercised `T3` last week, `T3` should still mean the same concept after the adjustment.
- **Training knowledge counts as external.** A skill that weaves trained material in unlabeled lets the agent appear to know things from the user's source that it doesn't. That's an epistemic foul and a pedagogical one.
- **Backup before rewrite** because the user may disagree with the agent's level call. A one-line revert is cheaper than rebuilding the curriculum.

## Related skills

- `set-curriculum` — build the original curriculum from source materials, source-faithful by default.
- `start-session`, `onboard-session` — when conducting a session over an adjusted curriculum, the agent reads the labels and surfaces external-source citations during teaching so the user always knows where the current explanation comes from.
- `bootstrap`, `stop-session` — the rest of the lifecycle; this skill doesn't touch them.
