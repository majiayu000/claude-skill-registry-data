---
name: skills
description: Browse and search all available skills, grouped by workflow stage or activity type
type: ops
version: v0.10
argument-hint: "[list | types | search <keyword>]"
---

# Skills

Discover and search skills visible in the current project plus source-available base and pack skills, grouped by workflow stage or activity type.

## Process

1. **Parse arguments:**
   - If `$ARGUMENTS` is empty or `list` → **list mode** (show all skills grouped by workflow stage).
   - If `$ARGUMENTS` is `types` → **type mode** (show all skills grouped by activity type).
   - If `$ARGUMENTS` starts with `search ` → **search mode** (filter by keyword after `search`).

2. **Discover skills:**
   - Scan base Codex source inventory in `base/codex/*/SKILL.md`; this shows available base skills, not proof that those skills are installed or visible in the active target project/session.
   - If `.agents/project.json` exists, read `enabled_packs` and scan `packs/<pack>/codex/*/SKILL.md` for each enabled pack. Also scan sub-directories like `packs/<pack>/codex/<skill>/frameworks/*/SKILL.md` for sub-skills.
   - Also scan all packs in `packs/*/codex/*/SKILL.md` (and `frameworks/*/SKILL.md` children) to discover available-but-not-installed skills.
   - If `.codex/skills/*/SKILL.md` exists in the current project, include those local skills too.
   - Read the first 10 lines of each file to extract YAML frontmatter fields: `name`, `description`, `type`, `invocation`, `parent`.
   - Track which pack each skill belongs to (if any).
   - Default `invocation` to `primary` when the field is absent.

3. **Group skills by workflow stage** using this static mapping:

   The mapping includes base-source skills and pack-provided skills. Only skills
   discovered in step 2 should be printed, so domain and kanban entries appear
   only when the corresponding project-local pack is enabled, linked, or shown as available-but-not-installed.
   PoketoWork kanban skills are intentionally absent while the kanban packs are hibernated.

   | Stage | Skills |
   |-------|--------|
   | Pack Management | `pack`, `pack list`, `pack status`, `pack recommend`, `npx skillpacks install <pack-or-skill>` (or project shell: `npx skillpacks install <pack-or-skill>`), `pack remove <pack-or-skill>`, `pack which <skill>` |
   | Discovery & Market Fit | `customer-discovery`, `enterprise-icp` |
   | Game Development | `game-workflow`, `game-audience`, `game-fantasy`, `game-genre-map`, `game-comparables`, `game-core-loop`, `game-prototype-test`, `game-store-page-test`, `game-playtest-metrics`, `game-roadmap`, `game-launch` |
   | Devtool Development | `devtool-workflow`, `devtool-user-map`, `devtool-integration-map`, `devtool-dx-journey`, `devtool-adoption`, `devtool-positioning`, `devtool-monetization`, `devtool-docs-audit` |
   | Planning | `brainstorm`, `idea-scope-brief`, `feature-interview`, `user-flow-map`, `spec-interview`, `spec-interview --ideas`, `ui-interview`, `ux-variations`, `consolidate-prototypes`, `experiment`, `clone-spec-store` (project-fleet pack) |
   | Mapping | `journey-map`, `metrics` |
   | Strategize | `roadmap`, `competitive-analysis`, `platform-strategy`, `gtm`, `landing-copy`, `monetization`, `positioning`, `runway-model` |
   | Evaluate | `dogfood`, `mvp-gap`, `scale-audit`, `customer-feedback`, `assumption-tracker`, `cohort-review`, `retro` |
   | Research Health | `research-roadmap`, `reconcile-research`, `reconcile-dev-docs` |
   | Detail | `plan-phase` |
   | Execution | `exec` |
   | Shipping | `ship`, `ship-end` |
   | Code Quality | `expert-review`, `regression-check`, `dead-code` |
   | Debugging | `investigate`, `debug`, `trace`, `session-triage` |
   | Refactoring & Migration | `migrate`, `decommission`, `scaffold` |
   | Monorepo | `affected` |
   | Release & Deploy | `release`, `deploy` |
   | Context & Session | `afps-status`, `codebase-status`, `analyze-sessions`, `handoff`, `sync`, `investor-update` |
   | Git Workflow | `branch-lifecycle` |
   | Utility | `commit-and-push-by-feature`, `init-agentic-skills`, `provision-agentic-config`, `skills`, `risk-register` |

   Skills not found in the mapping go into an **Other** group at the end.

4. **Group skills by activity type** (type mode only) using the `type` field from frontmatter:

   | Type | Description |
   |------|-------------|
   | `research` | Web search + analysis → produces documents |
   | `analysis` | Reads codebase/docs → produces assessments |
   | `planning` | Interactive → produces specs/plans |
   | `execution` | Writes/modifies code |
   | `review` | Reads code → reports issues (no changes) |
   | `debugging` | Investigates + fixes problems |
   | `shipping` | Commits, deploys, session management |
   | `ops` | Manages boards, branches, meta-tooling |

   Display order: research → analysis → planning → execution → review → debugging → shipping → ops.
   Skills with no `type` field go into an **Other** group at the end.

5. **Apply filter (search mode only):**
   - Match the keyword case-insensitively against each skill's `name`, `description`, and `type`.
   - Keep only matching skills. Remove empty groups.

6. **Output results:**
   - Print each non-empty group as a `## Group Name` heading.
   - Under each heading, list active-session/project-local primary and chained skills as `$<name> — <description>  [type]`.
   - Show orchestrator skills with an `⚙` prefix: `⚙ $<name> — <description>  [type]`.
   - Show sub-skills indented under their parent skill (identified by the `parent:` frontmatter field or by living under a `frameworks/` directory). Format: `  ↳ $<name> — <description>  [sub-skill]`. If the parent is not in the same group, place sub-skills in a "Sub-skills" subsection at the end of the parent's group.
   - For available-but-not-installed pack skills, list as `$<name> — <description>  [type]  ⚠ requires \`npx skillpacks install <skill>\` or \`npx skillpacks install <pack>\` from the project shell`.
   - For base-source skills that are not visible in the active session or project-local install state, list as `$<name> — <description>  [type]  ⚠ requires \`npx skillpacks init\` from the project shell`.
   - Omit groups that have no skills (after filtering in search mode).
   - At the bottom, print a total count: `**N skills** installed (M sub-skills), **P skills** available via packs` (or `**N skills** matching "<keyword>"`).

## Output

### List mode (default — grouped by workflow stage)
```
## Discovery & Market Fit
$customer-discovery — Customer discovery interview...  [research]
$enterprise-icp — Enterprise multi-stakeholder discovery...  [research]

## Strategize
⚙ $positioning — Parent router — detect market vs product mode...  [research]
  ↳ $category-design — Play Bigger category design framework  [sub-skill]
  ↳ $jtbd-positioning — Jobs to Be Done positioning framework  [sub-skill]
  ↳ $moore-positioning — Geoffrey Moore positioning framework  [sub-skill]
  ↳ $obviously-awesome — Obviously Awesome positioning framework  [sub-skill]
  ↳ $strategic-canvas — Strategic Canvas positioning framework  [sub-skill]
$competitive-analysis — Research competitors...  [research]
...

## Execution
⚙ $exec — Execute next plan step...  [execution]
...

**N skills** installed (M sub-skills), **P skills** available via packs
```

### Type mode (`$skills types`)
```
## Research
$customer-discovery — Customer discovery interview...
$competitive-analysis — Research competitors...
...

## Analysis
$mvp-gap — Evaluate codebase against customer-discovery evidence...
...

**N skills** found
```

## Constraints

- This is a read-only scan — never modify any files.
- Always read the live frontmatter from SKILL.md files; do not hardcode descriptions.
- Use the static stage mapping for stage grouping; use the `type` frontmatter field for type grouping.
- Keep output compact — one line per skill, no extra detail beyond name, description, and type tag.
- In search mode, if no skills match the keyword, print: `No skills matching "<keyword>"`.


## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
