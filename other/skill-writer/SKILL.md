---
name: skill-writer
description: Write skills to the library's quality bar — trigger-rich descriptions, checkable rules, self-improvement loop, token-lean. Trigger when creating, reviewing, or improving a skill / SKILL.md.
---

# Skill Writer — Meta-Skill

Every skill added to the library should match one quality bar. This is that bar.

## Self-improvement (do this first and last)
1. **At start:** read `learnings.md` in this skill's folder if it exists. Apply relevant lessons.
2. **At end of every use:** append one dated bullet — a structural choice that made a skill get triggered (or missed), phrasing that models followed well or ignored. Merge instead of duplicating; delete disproven bullets.

## Anatomy of a skill
Location: `.claude/skills/<kebab-name>/SKILL.md` (auto-invocable) — optionally mirror a portable copy elsewhere (e.g. a root `skills/` folder) for reuse across projects.

```markdown
---
name: <kebab-case, matches folder>
description: <see Description rules — this decides whether the skill ever fires>
compat: universal            ← omit for universal (the default); see Tool-compatibility checkpoint
---

# Title — one-line identity
One or two sentences: what failure mode this skill exists to prevent.

## Self-improvement (first and last)   ← every skill gets this loop
## <2–5 content sections>
```

## Tool-compatibility checkpoint (mandatory for any tool-specific mechanism)
Most of this library works on any markdown-reading agent — that's the point of the kit. A skill that depends on a mechanism only one tool has (Claude Code hooks, a specific CLI flag, a vendor-only API) must say so **structurally**, not just in prose, so `install-kit` can detect and flag it rather than every human reader having to notice a sentence buried in the body:
- Add `compat: <tool>-only` to the frontmatter (e.g. `compat: claude-code-only`). Omit the field entirely for universal skills — that is the default, don't write `compat: universal` explicitly except in this template.
- Open the body with one bold line naming the dependency: `**This is <tool>-only: <the specific mechanism it needs>.**`
- State explicitly that any rule this skill assists must remain fully functional without it — a tool-specific skill may *add* mechanical assistance, never be a silent prerequisite for a universal rule.
- `install-kit` reads `compat` at install time (see its Step 2) and flags/skips accordingly — a skill without this field is assumed to work everywhere, so leaving it off a genuinely tool-specific skill silently breaks that gate.

## Description rules (the highest-leverage 2 lines)
The description is the ONLY thing the model sees when deciding to load the skill. It must contain:
1. **What it does** (one clause),
2. **Explicit triggers** — the words/situations that should fire it: "Trigger when …" listing concrete verbs, nouns, and user phrasings,
3. Scope note if relevant ("Project-agnostic" / "any Three.js project").
A beautiful skill with a vague description is dead weight — it never loads.
**Hard cap: ~40 words.** Descriptions load into EVERY session whether the skill fires or not — they are the library's only always-on cost. Spend the budget on trigger words, never on prose ("Use X to its fullest", "Project-agnostic", "self-improvement loop" are padding — cut them).

## Content rules
- **Rules must be checkable.** "Grep before read" is followable; "be efficient" is not. Every imperative should be something you could audit a transcript against.
- **Explain the why in one clause** when a rule is counter-intuitive — models (and humans) follow understood rules better than bare commandments.
- **State goal + constraints, not step-by-step scripts** — over-prescription reduces output quality on strong models. Exception: checklists for genuinely ordered procedures (scaffolding, teardown) are fine.
- **Include the failure mode** each section prevents — "this stops X" makes the rule self-justifying.
- **Hard caps and thresholds** ("3+ files", "≤5 lines", "two failed fixes → stop") beat vague qualifiers ("large", "several").
- **Token-lean:** target under ~120 lines. A skill loads into context every time it fires; bloat is a per-use tax. Put rarely-needed depth in a `references/` file the skill points to.
- **Project-agnostic by default:** no absolute paths, no project names, no assumptions a different repo would break. Discover conventions from the project ("grep an existing file to confirm the prefix") instead of hardcoding them.
- **The self-improvement loop is mandatory:** read `learnings.md` at start, append one dated, concrete, mergeable bullet at end. This is what makes the library compound.

## Review checklist (for existing skills)
- [ ] Description has explicit triggers
- [ ] Every rule checkable; thresholds numeric
- [ ] No project-specific hardcoding
- [ ] Self-improvement loop present
- [ ] Tool-specific mechanism? → has `compat: <tool>-only` in frontmatter + the bold dependency line, and any rule it assists still works without it
- [ ] Under ~120 lines; no section that merely restates another
- [ ] Facts (APIs, prices, versions) verified against current docs, not memory — stale facts are worse than none
- [ ] Renaming or merging a skill? Add a row to `migrations/RENAMES.md` (repo root) in the same change and update every cross-reference (grep the whole library for the old name) — a rename without a ledger row strands existing installs
