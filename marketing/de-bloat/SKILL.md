---
name: de-bloat
description: Invoke ONLY on /de-bloat. Audit global + project skill files for bloat and duplication, then simplify via impag. Two passes - content (dedupe/compact) and root-cause (which rules/refs/skills drove the bloat).
---

# De-Bloat Skills

Critique and shrink skill files across `~/.claude/skills/` and any project-level `.claude/skills/`. Output is a plan executed via `impag`; no edits happen in this skill itself.

## Scope

- **Primary targets:** every `SKILL.md` in `~/.claude/skills/*/` and `<project>/.claude/skills/*/` (and any sibling `references/`, `scripts/` they reference).
- **Secondary targets (root-cause pass only):** `~/.claude/rules/*.md`, `~/.claude/references/*.md`, `~/.claude/CLAUDE.md`, project `CLAUDE.md` and `.claude/rules/*.md` - read-only here unless the root-cause pass identifies one as the source of bloat.

## Workflow

### Phase 1 - Discovery (Explore subagent)

Dispatch a single `Explore` subagent (thoroughness: "very thorough"). Brief it with:

- Inventory every `SKILL.md` under `~/.claude/skills/` and `<cwd>/.claude/skills/` (if the project has one). For each: path, frontmatter `name`/`description`, line count, heading outline.
- Flag duplicate or near-duplicate sections **across** skills (same headings, same lists, same examples).
- Flag content inside a `SKILL.md` that duplicates content already in `~/.claude/CLAUDE.md`, a `~/.claude/rules/*.md`, or a `~/.claude/references/*.md` - those should be referenced, not inlined.
- Flag bloat smells: vendor-lift frontmatter (`tokenEstimate`, `agents`, `trust_tier`, `validation`, `tags` arrays >3 items), aspirational sections never invoked (`Agent Coordination Hints`, fictional `FleetManager` blocks), tables that duplicate a paragraph, three-mode/three-level taxonomies where one suffices, ASCII directory diagrams, "Related Skills" link lists, marketing prose ("Remember", "The Contract").
- Flag *verb asymmetry*: rules/skills using enforceable add-verbs (`grep`, `migrate`, `record`, `document`) for additions but judgment-only verbs (`verify`, `link`, `dedupe`) for subtractions. Symmetric verbs are enforceable; asymmetric verbs generate one-way bloat because writers default to the enforceable side.
- Report: per-skill line count, top 3 bloat findings, cross-skill dupes table, secondary-file citations.

Do **not** ask Explore to propose edits or rewrite anything - it returns evidence only.

### Phase 2 - Brutal critique (brutal-honesty-review)

Invoke the `brutal-honesty-review` skill - it's a behavior skill, not an API: paste the Explore report into the current turn as context and let the skill self-apply. Apply **Linus** lens (technical wrong) to inlined-vendor content + dead taxonomies; **Bach** lens (BS detection) to aspirational/cargo-cult sections no caller invokes. Calibration: direct.

Produce, per skill, a concrete cut list:

- Lines/sections to delete outright (with reason).
- Sections to replace with a one-line link to the canonical source (`rules/`, `references/`, or another skill).
- Frontmatter fields to strip.
- Sections that look load-bearing but aren't - verify with `grep -r` across `~/.claude/` + active plugin caches before recommending deletion.

Reject any "rewrite the whole skill" suggestion - edits must be surgical (delta-update discipline: change only what's wrong, never restate the whole file).

### Phase 3 - Root-cause pass

From the Phase 1+2 evidence, identify upstream causes. Distinguish *mechanisms* (write-time vs. archive-time injection points; verb asymmetry; rule-loading dependency) from *symptoms* (line counts, individual duplications). Symptom-fixes recur every few months; mechanism-fixes don't. Prefer mechanisms. Look for:

- A rule or reference file that *should* own a piece of content but doesn't, so each skill re-states it (→ promote to `rules/` or `references/`, link from skills).
- A reference file that's so vague every skill re-derives the same checklist (→ tighten the reference).
- A pattern of vendor-template frontmatter copied across installs (→ note for your skill-installer to strip on entry).
- A skill whose body is ~80% generic preamble that belongs in `CLAUDE.md` once (→ move once, link many).
- A rule whose enforcement depends on the executing skill loading it mid-write - if the skill emits prose without first reading the rule, the rule is theatrical (→ propose **hook-conversion candidate**: rule may be deletable in favor of a `PreToolUse` gate that fires regardless of which skill is executing).

Output a short root-cause list (≤5 items): file, observed symptom, **fix category** (`rule-promotion` / `reference-tighten` / `frontmatter-strip` / `preamble-relocate` / `hook-conversion`), proposed structural fix. Each item becomes one task in Phase 4's plan, section 2. Hook-conversion items defer to a separate `/impag` run since they require `settings.json` wiring outside the de-bloat skill's edit scope.

### Phase 4 - Plan + execute (impag)

Write a plan to a git-tracked `docs/plans/` directory: `<project>/docs/plans/de-bloat-<date>.md` if cwd is a project, otherwise the git repo where your skill files actually live (so the plan is versioned alongside what it edits). Never write the plan to a non-git-tracked location, and never to a permanent-docs `references/` tier - that tier is for durable docs, not run plans. Plan structure:

1. **Per-skill cuts** - one task per skill, listing exact deletions/replacements (Edit-sized chunks, not rewrites). Keep tasks independent so `impag` can parallelize. Each task starts with a backup of the file being edited (e.g. `cp <canonical-path> <backup-dir>/<name>-pre-debloat-<date>.md`) so a bad cut is recoverable.
2. **Root-cause fixes** - one task per upstream change from Phase 3, sequenced *after* the per-skill cuts that depend on them (e.g. promote content to `rules/X.md` first, then strip from skills).
3. **Verification** - tasks dispatch read-only Explore subagents to confirm cuts didn't break cross-references.

Then invoke `impag` with the explicit plan path: `/impag <plan-path>`. Do not let `impag` default to most-recent-plan - there may be unrelated plans in the directory.

## Rules

- **Edit the canonical file, not a symlink.** If your skills are installed via symlinks (e.g. a stowed dotfiles setup), every per-skill cut task in the plan must open with `ls -la <skill-dir>` to resolve the symlink, then edit the real file behind it. Editing a symlink that points into a read-only bind mount can fail - always resolve to the writable canonical path first.
- **Pre-cut grep.** Before deleting a "looks unused" section, `grep -r` the section's distinctive phrase across `~/.claude/` and any plugin caches to confirm no caller depends on it.
- **No new abstractions.** Do not invent a new `references/` file unless ≥3 skills currently inline the same content. Two duplicates is a coincidence; three is a pattern.
- **Frontmatter strip is safe-by-default.** `tokenEstimate`, `agents`, `trust_tier`, `validation`, `priority`, `category`, `dependencies`, `optimization_version`, `last_optimized`, `quick_reference_card`, `implementation_status` - none are read by Claude Code. Drop them unless `grep` shows a hook or script consuming the field.
- **Stop at the brief.** Goal is shrinkage and root-cause repair. Do not "improve" wording, reorganize sections, or add missing examples - those are out of scope and bloat the diff.
- **Out of scope:** `CLAUDE.md` and `rules/*.md` condensation (use `condense` - it covers both); rule-file *restructuring* beyond the ≤5 promotions Phase 3 identifies. Larger rule-file work belongs in its own plan.
