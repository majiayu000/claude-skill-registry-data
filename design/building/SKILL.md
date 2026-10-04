---
name: superpowers-sage:building
description: >
  Plan-driven implementation in Sage/Acorn — reads docs/plans/ directory, implements
  components from approved sub-plans, runs scaffold generators (lando acorn acf:block),
  commits incrementally, auto-invokes block-scaffolding per ACF block, runs lando flush
  and lando theme-build after changes; full PR workflow with sage-reviewer gate.
  Invoke for: "/building", "implement from the plan", "implement from the plan",
  "build from the plan", "execute the plan", "start building", "code this feature".
  Skip when: there is no approved plan yet — run /architecture-discovery then
  /plan-generator first.
user-invocable: true
argument-hint: "[plan path or component description]"
---

# Building — Plan-Driven Implementation

Implement Sage components by reading from plan directories, consulting design assets, and verifying after each component.

**Announce at start:** "I'm using the building skill to implement from the plan."

## Inputs

$ARGUMENTS

If a plan path is provided, read the plan. Otherwise, check for active plan in `docs/plans/`.

## Procedure

### 0) Load the plan

1. Read `plan.md` frontmatter for strategy, components, design-tool
2. Read `architecture.md` for architectural decisions
3. Read `content-model.md` for data modeling decisions
4. List `components/` for sub-plans
5. List `assets/` for design reference images

If no plan exists, suggest running `/architecture-discovery` then `/plan-generator` first.

### 1) Set up prerequisites

Based on content model:

1. If CPTs needed → configure `config/poet.php`
2. If new packages needed → `lando theme-composer require <package>`
3. If Options Pages needed → create ACF Options class
4. Run `lando flush` after PHP changes

### 2) Implement components (per sub-plan)

**Design system gate (runs once, before the component loop):**

Check that the visual foundation exists:

- `resources/css/design-tokens.css` — must exist and contain real tokens (not placeholder)
- Route `/kitchensink` — must be accessible and visually validated (Playwright screenshot taken)

If either is missing or unvalidated → **invoke `/sage-design-system` and pause** until the kitchensink screenshot confirms all tokens and UI atoms render correctly. Do NOT implement any block without a validated design system.

For each component in order:

#### 0) Pre-fetch design reference, THEN dispatch design-extractor

**CRITICAL:** subagents do NOT inherit MCP tools from the calling session. Dispatching
`design-extractor` without first persisting design data to disk produces fabricated specs
with `VERIFY` placeholders and estimated values.

**Inversion pattern — always pre-fetch in THIS thread before dispatching:**

1. With the MCP tool available in this session, capture reference data to disk:

   | Tool | Commands | Output |
   |---|---|---|
   | Pencil | `batch_get(resolveVariables:true, readDepth:4)` + `get_screenshot` | `assets/section-<name>.nodes.json` + `section-<name>-ref.png` |
   | Figma | `get_design_context` + `get_screenshot` (with nodeId) | `assets/section-<name>.nodes.json` + `section-<name>-ref.png` |
   | Paper | `get_node_info` + `get_computed_styles` + `get_screenshot` + `get_jsx` | `assets/section-<name>.nodes.json` + `section-<name>.styles.json` + `section-<name>-ref.png` + `section-<name>.reference.jsx` |
   | Stitch | `get_screen` | `assets/section-<name>-ref.png` |

2. Confirm all expected files exist on disk (`ls docs/plans/<plan>/assets/`).

3. NOW dispatch the `design-extractor` agent:
   - Mode: SURGICAL
   - Target: this specific component section only
   - Pass the pre-captured paths in the prompt
   - Output: `assets/section-<name>-spec.md`

The subagent reads the pre-captured files as source of truth — the MCP call was already
made here. The subagent's only job is to structure the data into the spec file.

**Verify the output is not fabricated:** open the spec file and check for `VERIFY` markers
or suspiciously round numbers. If found, the extraction failed — re-dispatch with clearer
path references.

**Fallback (no design-extractor agent available — Cursor IDE / single-agent mode):**

If the subagent system is unavailable:

1. Re-read `assets/section-<name>-spec.md` and `assets/section-<name>-ref.png` from disk
2. Pull live design reference via the active MCP tool:
   - Figma: `get_design_context` + `get_metadata` (node geometry)
   - Paper: `get_computed_styles` + `get_node_info`
   - Pencil: `batch_get(resolveVariables: true)` + `batch_get(readDepth: 4)`
   - Stitch: `get_screen`
3. Record `design-extractor: deferred` in the `plan.md` frontmatter
4. Use the values extracted from step 2 as the source of truth

#### a) Re-read design reference (ALWAYS)

- Read `assets/section-{name}.png` or `assets/section-{name}.md` from disk
- **NEVER rely on context memory** — always re-read from disk before each component
- If asset missing, invoke `/designing` to capture it

#### b) Check content model

- Read `content-model.md` for this component's classification
- If not classified, invoke `/modeling` for this component

#### c) Consult reference skills

Auto-discover which reference skills are relevant:

- ACF block → read `@sage-lando` references/acf-composer.md
- Blade view → read `@sage-lando` references/blade-templates.md
- Livewire → read `@acorn-livewire`
- Routes → read `@acorn-routes`
- Tailwind/CSS → read `@sage-lando` references/frontend-stack.md

#### d) Isolation strategy — decide: worktree vs branch-commit

Isolation approach depends on the dev environment:

| Environment | Isolation | Why |
|---|---|---|
| **Lando** (default for Sage) | **Branch + atomic commit per component** | Lando mounts `/app` to a fixed path in `.lando.yml`. Worktrees live at sibling paths and require re-mounting the container for each worktree — high friction, Lando container already knows only one path. |
| **docker-compose / vanilla** | **Worktree per component** | Container mount is flexible; worktrees at `.worktrees/<component>/` are cheap and safe. |
| **Bare-metal / local PHP** | **Worktree per component** | No container constraints. |
| Explicit user override (`--no-worktree` or plan frontmatter `isolation: branch-only`) | Honor the override | |

Detection rule: if `.lando.yml` exists at repo root → use branch-commit strategy unless the user explicitly opts into worktrees.

##### Branch + atomic commit (Lando path)

```bash
# Start on the feature branch recorded in plan.md
FEATURE_BRANCH=$(grep '^branch:' docs/plans/<active-plan>/plan.md | awk '{print $2}')
git checkout "$FEATURE_BRANCH"

# Implement this component's files in place. Commit atomically when done.
# ... edit code ...

git add -A
git commit -m "feat({slug}): implement component per sub-plan"
```

Each component becomes one (or a few) well-scoped commit(s) on the feature branch. Roll back individually by reverting the commit. Lando keeps working without reconfiguration.

##### Worktree (docker-compose / bare-metal path)

```bash
FEATURE_BRANCH=$(grep '^branch:' docs/plans/<active-plan>/plan.md | awk '{print $2}')
COMPONENT_BRANCH="${FEATURE_BRANCH}-<component-name>"

git worktree add .worktrees/<component-name> -b $COMPONENT_BRANCH $FEATURE_BRANCH
```

Example: feature branch `feat/onepage-blocks-2026-03-23`, component `hero`:

```bash
git worktree add .worktrees/hero -b feat/onepage-blocks-2026-03-23-hero feat/onepage-blocks-2026-03-23
```

**Implement inside the worktree.** The worktree mirrors the full repo root. Theme files are at `.worktrees/<component>/content/themes/<theme>/`.

**ZERO ARBITRARY TAILWIND VALUES.**
Every colour, font, spacing value must be a token declared in `@theme`.

```blade
{{-- ✅ Correct — use token names --}}
<section class="bg-bg text-text py-24">

{{-- ❌ Forbidden — arbitrary values are a Critical issue --}}
<section class="bg-[#131313] text-[#e5e2e1] py-[96px]">
```

**For ACF blocks:** After running `lando acorn acf:block {Name} --localize`, invoke `/block-scaffolding` for this block before proceeding. The custom element contract (tag-selector CSS scoped to `block-{slug}`, JS class extending `BaseCustomElement`, selective CSS+JS enqueue, `$spacing`/`$supports`/`$styles`, block README) is that skill's responsibility — do not implement manually.

#### e) Build and verify

After implementing:

1. `lando flush` — clears Acorn/Blade/OPcache (required after PHP changes)
2. `lando theme-build` — compiles Tailwind + JS
   - If exit non-zero: **stop, report build failure. Do NOT proceed to verification.**
3. **Pre-capture live screenshot** in THIS thread (Playwright MCP lives here, not in the subagent):
   - Navigate to the URL from the spec's `Verification Inputs` block
   - Take a screenshot with the canonical viewport width
   - Save to `docs/plans/<plan>/assets/section-<name>-live.png`

   Then dispatch `visual-verifier` agent with:
   - `url`: read from spec `Verification Inputs` block
   - `selector`: read from spec `Verification Inputs` block
   - `spec`: `docs/plans/<plan>/assets/section-<name>-spec.md`
   - `ref`: `docs/plans/<plan>/assets/section-<name>-ref.png`
   - `live`: `docs/plans/<plan>/assets/section-<name>-live.png`

   The subagent reads both images via the Read tool and compares visually. If the subagent
   somehow has Playwright MCP it can also re-capture, but the pre-captured image is the
   fallback when it doesn't.
4. On `MATCH`:

   **Branch-commit strategy (Lando):** already on the feature branch — nothing to merge. Proceed.

   **Worktree strategy:**
   ```bash
   git checkout <feature-branch>
   git merge <component-branch>
   git worktree remove .worktrees/<component-name>
   git branch -d <component-branch>
   ```
5. On `DRIFT` or `FAIL_ARBITRARY_VALUES`: fix in place → re-run `lando theme-build` → re-dispatch `visual-verifier` → commit/merge on MATCH
6. After commit/merge: `git push` to sync the feature branch with the remote

#### f) Strategy gate

- **Interactive strategy**: pause for user approval before next component
- **Autonomous strategy**: proceed to next component if verification passed
- **Mixed strategy**: pause only for complex components

### 3) Parallel delegation

When components are independent (no shared CPTs or services):

- Use `dispatching-parallel-agents` or `subagent-driven-development` base skills
- Each subagent gets: sub-plan path, asset path, content model excerpt
- Review subagent output between batches

### 4) Completion

After all components:

1. Run `lando flush` to clear all caches
2. Run `lando theme-build` for production build
3. **Design-system changelog check:** if any file under `resources/views/components/*.blade.php` or the `@theme` block in `resources/css/app.css` was touched this session, append an entry to `docs/design-system-changelog.md` (see section 5 below).
4. **Commit gate:** `git add -A && git commit -m "feat(blocks): <feature-name> — all components verified" && git push` — required before declaring the build phase complete
5. Suggest `/reviewing` for convention audit
6. Suggest `finishing-a-development-branch` for merge/PR

### 5) Design-system changelog auto-entry

When building touches design-system-level files (atoms, tokens, base typography, layout components), append an entry to `docs/design-system-changelog.md`. Create the file if absent with this structure:

```markdown
# Design System Changelog

Chronological record of changes to the shared visual contract. Automatically appended by /building on completion.

## YYYY-MM-DD — <PR title or commit short summary>

### Atoms
- `<x-component>` **added prop `tone`** — default, backward-compatible
- `<x-button>` **added variant `secondary-dark`** — text-link on dark bg

### Tokens
- `--text-h2-compact: 44px` (new)
- `--container-narrow: 360px` (new)

### Modifier classes
- `h2.hero`, `h2.compact` (new, unlayered, override type selector)

### Breaking changes
- _(none)_
```

**Detection rule:** if `git diff --name-only <session-start>..HEAD` includes:
- `resources/views/components/**/*.blade.php` → inspect for new props, removed props, variant additions
- `resources/css/app.css` (@theme block) → inspect for new/changed/removed tokens
- `resources/css/blocks/**/*.css` → skip (block-scoped, not shared contract)

Generate the entry by diffing the files; don't ask the user to hand-write it.

### 6) Milestones auto-save (post-merge)

When `finishing-a-development-branch` completes (PR merged), append to `docs/milestones.md`:

```markdown
# Milestones

## YYYY-MM-DD — v<version> (PR #<number>)

- **Scope:** <1-line PR title>
- **Components delivered:** <list>
- **Architectural patterns validated:** <list>
- **Decisions recorded in:** <spec path>
- **Known follow-ups:** <list or "none">
```

This survives context compaction and gives future sessions a fast recap of what shipped. Do NOT rely on memory files alone — milestones are commit history with meaning.

## Key Principles

- **Always re-read assets from disk** — context compression will lose design reference
- **Verify after each component** — catch drift early, not at the end
- **Consult reference skills** — don't guess patterns, read the reference
- **Respect the strategy** — autonomous for simple, interactive for complex
- **Hooks handle cache** — post-edit hook auto-runs `lando flush` and `lando theme-build`
- **Worktree per component** — every component is implemented in an isolated branch+worktree, merged to the feature branch only after visual verification passes
- **Zero arbitrary Tailwind values** — all colours, fonts, and spacing must be `@theme` tokens; arbitrary `[#hex]` classes are a Critical issue caught by visual-verifier

## Query First — MCP Integration

Before generating code that references CPTs, fields, routes, or Livewire components:

```
discover-abilities
execute-ability posts/list-types
execute-ability acf/field-groups
```

Never invent slugs or field names — always query first when the stack is available.
See [`sageing/references/mcp-query-patterns.md`](../sageing/references/mcp-query-patterns.md).
