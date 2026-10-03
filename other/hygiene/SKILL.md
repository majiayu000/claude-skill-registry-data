---
name: hygiene
description: Audit project structure for convention violations, missing files, template drift, and cross-platform sync gaps; optionally auto-fix
type: analysis
version: v0.0
argument-hint: "[audit|fix] [skills|tasks|docs|codex|all]"
---

# Hygiene - Project Structure Audit

Checks that project files follow established conventions, flags gaps and drift, and optionally fixes mechanical issues. Think of it as a linter for project structure rather than code.

## Process

### 1. Determine Mode and Scope

Parse `$ARGUMENTS`:

- **Mode**: `audit` (default, read-only) or `fix` (apply mechanical fixes)
- **Scope**: `skills`, `tasks`, `docs`, `codex`, or `all` (default)

Read `CLAUDE.md` for project conventions. Read `docs/skills-reference.md` for the canonical skill list. For `docs` scope, also read `references/documentation-templates.md` from this skill directory.

### 2. Audit Skills (`skills` scope)

For each skill directory in `base/claude/*/SKILL.md`, `base/codex/*/SKILL.md`, `packs/*/claude/*/SKILL.md`, and `packs/*/codex/*/SKILL.md`:

**Frontmatter check:**
- Has `name` field — matches directory name
- Has `description` field — non-empty, under 120 characters
- Has `version` field — valid semver (X.Y.Z)
- Has `argument-hint` field (can be empty)

**Section check:**
- Has a top-level `# Heading` that matches the skill's purpose
- Has `## Process` section with numbered steps
- Has `## Output Format` section (or explicit "no files written" note)
- Has `## Constraints` section

**Naming check:**
- Directory name uses kebab-case
- Directory name matches frontmatter `name`

Flag each violation with the file path and what's wrong.

### 3. Audit Tasks (`tasks` scope)

Check expected project files exist based on project phase:

**Always expected:**
- `tasks/roadmap.md` — has content, not just a placeholder
- `tasks/todo.md` — has content with checkable items (`- [ ]` or `- [x]`)
- `tasks/manual-todo.md` — if it exists, has content with checkable human-only external items (`- [ ]` or `- [x]`) and `_(blocks: ...)_` or `_(after: ...)_` annotations
- `tasks/record-todo.md` — if it exists, contains non-blocking condition-gated records with source, condition, non-blocking reason, evidence, and promotion rule fields
- `tasks/recurring-todo.md` — if it exists, contains cadence-based tasks with cadence, owner/agent, last run, next due, evidence/output path, and escalation fields
- `tasks/history.md` — exists

**Expected if specs exist:**
- `tasks/ideas.md` — exists if `specs/*.md` has 2+ files

**Phase archives:**
- If `tasks/roadmap.md` has completed phases (checked-off milestones), `tasks/phases/` should exist with corresponding `phase-N.md` files

**Staleness (informational, not violations):**
- `tasks/todo.md` has all items checked but phase isn't marked complete in `tasks/roadmap.md`
- `tasks/manual-todo.md` has unchecked items that block completed steps in `tasks/todo.md`
- `tasks/manual-todo.md` contains agent-executable work that belongs in `tasks/todo.md`
- `tasks/record-todo.md` has eligible items that may need promotion into `tasks/todo.md`
- `tasks/recurring-todo.md` has due items that may need promotion into `tasks/todo.md`
- `tasks/roadmap.md` references phases that have no corresponding detail

### 4. Audit Docs (`docs` scope)

**Skills reference sync:**
- Every base core directory has a corresponding entry in `docs/skills-reference.md`
- Every pack directory is listed under its pack in `docs/skills-reference.md`
- The base core table and pack skill lists are complete (no missing, no extras)

**Required docs:**
- `CLAUDE.md` exists at project root
- If `AGENTS.md` exists, it should not contradict the workflow/pipeline conventions in `CLAUDE.md`

**Documentation template audit:**
- Classify generated Markdown files by path pattern and validate them against `references/documentation-templates.md`
- Check canonical roots:
  - `tasks/` for roadmap, todo, history, manual tasks, record tasks, recurring tasks, phase archives, handoff, deployment ledgers, and lessons
  - `specs/` for implementation specifications and interview logs
  - `research/` for research docs, interview logs, search logs, experiments, and reconciliation reports
  - `docs/specifications/` only as a fallback spec location
  - `alignment/*.html` for generated browser-review alignment artifacts from planning and prototype workflows
- Check canonical root directories exist:
  - `tasks/` — Warning if absent
  - `research/` — Info if absent; Warning if absent AND research-pattern files (`icp-*.md`, `gtm-*.md`, `competitive-*.md`, `journey-*.md`, `metrics.md`, `monetization.md`, `customer-feedback*.md`) exist elsewhere (e.g., `docs/`)
  - `specs/` — Info if absent; Warning if absent AND spec-pattern files exist elsewhere
  - `alignment/` — Info if present; generated HTML review pages are allowed here and should not be treated as misplaced documentation
- Flag legacy or drifted planning locations such as new `docs/plan.md` or new `docs/phases/` phase archives; current workflows write plans under `tasks/`
- Exempt archived snapshots under `docs/history/archive/**` from template checks
- Treat unknown hand-written docs as Info unless they are clearly generated workflow artifacts

**Universal generated-doc checks:**
- First non-empty Markdown heading is exactly one `#` H1
- Required sections for the file family are present once and in the expected order
- Non-ledger research/spec/task artifacts include a metadata quote block when the template requires it
- Checkable workflow docs use `- [ ]` / `- [x]` items where later skills need task state
- Main research/spec docs end with `## Next Steps`, or explicitly state why no next step exists

**Family-specific checks:**
- `tasks/roadmap.md` has a summary, phase overview, repeated `## Phase N:` sections, phase milestones or acceptance criteria, and cross-phase concerns when multi-phase
- `tasks/todo.md` has checkable work, a priority task queue, or a priority documentation todo, and does not contain the full multi-phase roadmap except during legacy migration
- `tasks/manual-todo.md` has checkable human-only external items, every unchecked item includes `_(blocks: Step N.X)_` or `_(after: Step N.X)_`, and no item is repo/code/config/test/audit/CLI/API work the agent can execute
- `tasks/record-todo.md` has checkable non-blocking record items with source, condition, non-blocking reason, required data/access, measurement/query, target note, revisit cadence/date, completion evidence, and promotion rule
- `tasks/recurring-todo.md` has cadence-based items with task, cadence, owner/agent, scope, trigger, last run, next due, command/skill, evidence/output path, and escalation conditions
- `tasks/history.md` is append-only with dated entries
- `tasks/phases/phase-N.md` has completed steps, milestone or acceptance criteria, and an `## On Completion` or equivalent completion summary
- `specs/*.md`, `specs/{app}/*.md`, and fallback `docs/specifications/*.md` have spec sections for overview, goals, non-goals, detailed design, edge cases, test plan, acceptance criteria, and open questions or explicit `None`
- `*-interview.md` logs include questions, options when presented, responses or decisions, and final deviations or coverage summary
- `research/*.md` and `research/{app}/*.md` have metadata, summary, source/evidence orientation, assumptions or risks when relevant, and next steps
- `research/*-search-log.md` files are clearly marked as supporting context and include queries, findings, and source attribution
- `research/experiments/*.md` has hypothesis, method, success criteria, timeline, budget, decision rules, results, and next steps
- `sync.md` uses `## Dependencies`, `## Conflict Resolution`, `## Custom`, and `## Notifications`
- `tasks/deploys.md` has environment headings with dated deployment ledger entries including branch, commit range, commit count, and status
- `.agents/project.json`, when present, is valid JSON and includes project designation fields used by pack-aware skills

### 5. Audit Codex Mirror (`codex` scope)

Compare Claude and Codex directories within each root:

- Every skill in `base/claude/` should have a corresponding `base/codex/<name>/SKILL.md`
- Every skill in `packs/<pack>/claude/` should have a corresponding `packs/<pack>/codex/<name>/SKILL.md`
- Flag skills that exist in one but not the other
- For skills that exist in both, check that the codex version has:
  - Matching frontmatter `name` and `description`
  - An `agents/openai.yaml` manifest (if the skill is execution-oriented, not display-only)

**Known exceptions** (skills that intentionally only exist in one platform):
- Check for a `# codex-skip` comment in the claude skill's frontmatter — if present, don't flag the missing codex mirror

### 6. Generate Report

Categorize all findings:

| Severity | Meaning |
|----------|---------|
| **Error** | Convention violation that should be fixed (missing required field, naming mismatch) |
| **Warning** | Drift or gap that may be intentional (missing codex mirror, incomplete sections) |
| **Info** | Suggestions for improvement (long descriptions, missing optional sections) |

For documentation templates, use:

- **Error** for automation-breaking structure: missing checkboxes in `tasks/todo.md`, missing manual blocker annotations, executable work misfiled in `tasks/manual-todo.md`, `tasks/record-todo.md`, or `tasks/recurring-todo.md`, malformed phase numbering, multiple H1 headings, invalid `.agents/project.json`, or missing required task/spec sections that downstream skills parse.
- **Warning** for template drift: missing metadata, missing `## Next Steps`, missing spec acceptance criteria, research docs without source/evidence orientation, or legacy roots that should move to canonical locations.
- **Info** for uncertain classifications, old hand-written docs, optional sections, or cleanup suggestions that do not block automation.

### 7. Auto-Fix (if `fix` mode)

Only fix mechanical, unambiguous issues:

- Add missing `argument-hint:` field (empty) to frontmatter
- Fix `name` field to match directory name
- Create missing Codex mirror in the matching root from the Claude version (copy frontmatter + intro, add TODO for Codex-specific content)
- Add missing skill entries to the appropriate base core table or pack list in `docs/skills-reference.md`
- Add missing empty metadata scaffold only when the target generated-doc template explicitly requires metadata and the values can be left blank
- Normalize duplicate blank lines around headings in generated docs when it is purely mechanical

**Never auto-fix:**
- Missing Process/Output/Constraints sections (these need human judgment)
- Content mismatches between claude and codex versions
- Roadmap or todo content
- Summaries, sources, acceptance criteria, research claims, history entries, task status, or next-step recommendations
- Spec/research document rewrites that should use the archive-first replacement policy from the generating skill

After fixing, re-run the audit to show remaining issues.

## Output

Display directly to the user (no files written in audit mode):

```
## Hygiene Report — [scope]

### Errors (X)
- **base/claude/foo/SKILL.md** — missing `version` field in frontmatter
- **packs/business-discovery/claude/bar/SKILL.md** — directory name `bar` doesn't match frontmatter name `baz`

### Warnings (X)
- **packs/example-pack/codex/example-skill/** — missing Codex mirror (exists in Claude only)
- **docs/skills-reference.md** — `$hygiene` not listed in the base core table
- **research/icp.md** — missing `## Next Steps` section required by the research doc template

### Info (X)
- **base/claude/ship/SKILL.md** — no `## Constraints` section (consider adding)
- **docs/architecture.md** — unknown hand-written doc; skipped strict generated-doc template checks

### Summary
- Skills: 48 checked, 2 errors, 1 warning
- Tasks: 4 checked, 0 errors
- Docs: 3 checked, 1 warning
- Codex: 46 checked, 2 warnings
```

In `fix` mode, prepend each fixed item with a checkmark:

```
### Fixed
- [x] Added missing `argument-hint:` to base/claude/foo/SKILL.md
- [x] Created mirror base/codex/hygiene/SKILL.md

### Remaining Errors (X)
...
```

## Constraints

- **Read-only by default.** Only modify files when explicitly invoked with `fix` mode.
- **No content generation.** Auto-fix only adds structural scaffolding, never writes substantive content.
- **Structural docs only.** Template checks validate shape, parseability, and canonical placement; use `$reconcile-dev-docs`, `$reconcile-research`, `$research-roadmap`, or `$spec-drift` for truth, freshness, and contradictions.
- **Show evidence.** Every finding must include the specific file path and what's wrong.
- **No false positives.** If uncertain whether something is a violation, classify it as Info, not Error.
- **Respect exceptions.** Check for `# codex-skip` and similar markers before flagging intentional gaps.
- **Use subagents** to parallelize scanning across skills, tasks, docs, and codex scopes when running `all`.


## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
