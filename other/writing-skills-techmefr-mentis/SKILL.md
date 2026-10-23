---
name: writing-skills
description: Use when a new skill has to be created (or an existing skill revised) for this framework, applies the single template, checks that no existing block already covers the need, and credits the source if the idea comes from elsewhere.
---

# writing-skills

Cross-cutting (meta) block: this is the skill that explains how to write the other skills.
Applies as soon as a gap is identified in the pipeline or a sourced idea deserves to be
rewritten our way (Rule B).

## When
- A gap is spotted in the pipeline (e.g. "we're missing a model router" → `choose-model`).
- An idea seen elsewhere (market repo, article, aitmpl.com, superpowers) looks useful but doesn't
  exist here yet.
- An existing skill no longer matches real usage and needs revising.

## Steps
1. **Check that no existing block already covers the need**: read `CATALOG.md` and the skills
   table in `README.md` before writing anything. A duplicate costs more than a gap (Rule B,
   adoption checklist).
2. **Isolate the real mechanism**, not the packaging: if the skill is sourced from an external
   repo, read the concept until you can explain it without the source file in front of you.
3. **Write to the single template** (`CONVENTIONS.md`):
   - frontmatter `name` + `description` starting with "Use when..."; `description` is what routes
     the block, and it is **truncated at 1,536 characters in the listing** — that is a platform
     limit, not a style preference, so a description written to summarise instead of to route
     loses its tail silently
   - the optional frontmatter fields, **declared only when the block needs one**: `paths` so a
     stack block doesn't load on another stack's files, `allowed-tools` so an operator isn't
     approving each gate command, `disallowed-tools` to keep an autonomous block out of
     `AskUserQuestion`, `disable-model-invocation` for a step nobody should trigger by accident,
     `context: fork` when the step belongs in a subagent rather than in the conversation. The list
     and what each one costs are in `references/claude-code-platform.md` §2 — including which of
     them make the block Claude Code-only, which is a rule C decision and not a detail
   - `# name`
   - `## When`
   - `## Steps`
   - `## Output / checkpoint`
   - `## Guardrails`
   - `## Origin`: never empty: either an external source credited honestly, or "no external
     source, internal synthesis".
4. **Place the skill in the pipeline** if it has a numbered step (see the `README.md` table), or
   mark it "cross-cutting" if it applies everywhere without being a sequential step (e.g.
   `choose-model`, `dispatch-parallel`).
5. **Update `CATALOG.md`** (registry + source traceability) and the skills table in `README.md`
   in the same move; a skill not referenced in both becomes invisible and gets rewritten twice
   later.
6. **Stay publishable** (Rule C): no real project name, no secret, a generic role ("the Laravel
   backend") never an internal repo name: except in an internal MR-review implementation, which has a different
   status (production evidence, real names owned).
7. **Order within a section by how often the rule fires, not by when it occurred to you.** A block grows one
   real gap at a time (a re-check, a review finding), and appending each addition at the bottom of its
   section is how the load-bearing rule from month one ends up under ten rare-case additions from month six —
   the "lost in the middle" effect applies to a skill file exactly as it does to any other long context. When
   a section passes roughly ten points, that's the signal to re-sort it (common case first) rather than to
   keep appending, not a hard line to enforce mechanically.
8. **A filter block states a positive requirement.** A block that only forbids produces empty output; say
   what the result must contain. Every detection block also carries a mandatory section on what not to
   flag, because a detector without one drifts into false positives.
9. **A rule names the artefact that proves it was applied**, or it becomes a hook. Adding a canon without
   cutting the sources it absorbed reproduces the duplication it was meant to remove.
10. **Every scanner added locks its tiers with a regression test**, so a threshold cannot be loosened by
    editing the scanner alone.

11. **Points 11 to 38 live in a reference file**: gotchas sections, what to put in a skill and what to cut,
    calibrating control, validation patterns and description-writing rules from the open Agent Skills guides,
    then completion criteria, positive steering, no-ops, pointer wording and pruning from a second source.
    Read it when drafting or revising a body or a description:
    [`references/11-authoring-rules.md`](./references/11-authoring-rules.md). Whether a description actually
    triggers is measured with `skill-trigger-evals`, not judged by eye.

## Output / checkpoint
A complete `skills/<name>/SKILL.md` file following the template, referenced in `CATALOG.md` and
in the `README.md` table, with a non-empty `Origin` section.

## Guardrails
- Never a skill without `## Origin`: honesty about the source (internal vs sourced from the
  market vs rewritten from a specific repo) is structural, not optional.
- Never install an external repo as a dependency: we read, we rewrite, we credit (Rule B): never
  a `git submodule` or a runtime import to a third-party repo.
- A skill that duplicates an existing block is a regression, not an addition: check step 1 before
  writing, not after.

## Origin
Rewrite of the `writing-skills` skill from a market skill/agent framework; there it documents
their own template, here it documents ours (the single template in `CONVENTIONS.md`), plus the
Rule B adoption checklist (check for duplicates, credit the source) which doesn't exist as such
on the superpowers side.

Step 7 (ordering by frequency, re-sort past ~10 points) added 2026-08-10 from the "context engineering"
literature's lost-in-middle effect and progressive-disclosure framing (surveyed via a market
context-engineering skill kit while scouting for new market blocks worth adopting; no code or text
copied, the mechanism was already familiar from long-context work and is stated here in our own terms).
Concrete trigger for writing it now rather than leaving it as a general instinct: several blocks in this
repo (`vue-nuxt-vuetify-conventions`, `react-nextjs-conventions`) grew past 10 points per section across
this session's re-checks, each addition appended at the bottom of its list.

Points 11 to 30 (in `references/11-authoring-rules.md`) added 2026-10-19 from the Agent Skills open
specification and its best-practices and description guides, agentskills/agentskills commit 69ef37e (docs
CC BY 4.0, credited, restated in our words), details in [`references/origin.md`](./references/origin.md).

Steps 8 to 10 added 2026-10-02 from a read of public prose-quality and design-quality filters: the
positive-requirement and not-to-flag rules come from how those filters fail, the proof-artefact rule and
the scanner regression test from the corpus's own history of unenforced guarantees.

Points 31 to 38 (completion criteria, steering by the positive, no-ops, pointer wording, the environment as a source of truth, sediment, one meaning one place, leading words) added 2026-10-19 from `writing-for-agents` of `mattpocock/skills` (MIT), wording ours, details and the owner's decision on guardrail style in [`references/origin.md`](./references/origin.md).
