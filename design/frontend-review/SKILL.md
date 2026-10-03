---
name: frontend-review
layer: stack
description: Front-end conventions review for Vue surfaces — the component-usage analog of /a11y, pointed at Nuxt UI 4 + crouton conventions instead of WCAG. Reviews just your diff (or a package/file) for v3 component names, the v4 overlay pattern, Options API, raw-HTML re-implementations, and hardcoded colors; rates findings by severity; and either comments inline on the PR (--comment) or applies the safe fixes for you (--fix). Steers the depth-aware `frontend-review` subagent. Use when asked to "check the frontend", "are we using Nuxt UI right", "review component usage", "frontend-review this", or run /frontend-review.
argument-hint: "[quick|standard|deep] [last N | --scope <pkg> | --file <path>] [--comment] [--fix]"
allowed-tools: Bash, Read, Grep, Glob, Edit, Agent, mcp__github__add_comment_to_pending_review, mcp__github__pull_request_review_write, mcp__github__pull_request_read, mcp__github__add_issue_comment
---

# Frontend-review Skill — the steering brain

You drive a front-end **conventions** review. The actual analysis lives in the
**`frontend-review` subagent** (`.claude/agents/frontend-review.md`) — this skill
decides *what scope* and *how deep*, *spawns* the agent (fanning out for 5+ files),
*collates* findings into one severity-rated report, and then offers to **comment**
them on the PR or **fix** the safe ones. Keep the analysis logic in the agent; keep
orchestration here.

This is the front-end-conventions member of the code-cleaning family. It deliberately
**mirrors `.claude/skills/a11y/SKILL.md`** (diff-scoped, 3-level severity, the same
report format, an offer-to-fix step) and the **`red-team` skill/agent split** (depth
ladder, spawn-and-collate) — just for Nuxt UI 4 / crouton component conventions
instead of accessibility or bugs.

## Why a separate skill (not folded into /review)

`/review` is a broad correctness/security/dead-code pass and only carries a *handful*
of Nuxt UI bullets as honor-system reminders. This skill is the **dedicated,
diff-scoped, severity-rated, fixable, CI-gated** front-end-conventions layer — it owns
the full convention checklist, the v3→v4 rename autofix, and the per-PR gate. Exactly
like `/a11y` and `/red-team` sit beside `/review` rather than inside it.

What it does **not** do: visual/layout taste ("this should be a card") — that's the
human `/ui-proposal` sign-off; accessibility — that's `/a11y`; security — that's
`/red-team`. Conventions only.

## 1. Resolve `{ depth, scope, comment, fix }` from the request

**Scope** (mirrors the review skill's modes):

| Invocation | What it reviews | scope passed to agent |
|------------|-----------------|-----------------------|
| `/frontend-review` | All uncommitted `.vue` changes (staged + unstaged) | `"diff"` |
| `/frontend-review last N` | `.vue` files in the last N commits | `"diff"` (vs `HEAD~N`) |
| `/frontend-review --scope <pkg>` | A whole package's `.vue` | `packages/<pkg>` (or `apps/<pkg>`) |
| `/frontend-review --file <path>` | A single `.vue` file | that path |

**Depth** (mirrors red-team's ladder):

| The user said… | depth |
|----------------|-------|
| `/frontend-review` (bare), a PR/diff context, `quick` | `quick` (static, diff-scoped) |
| `/frontend-review --scope <pkg>` / `standard` | `standard` (full static sweep of the scope) |
| `/frontend-review deep` / "check against real Nuxt UI" | `deep` (static + cross-check the real `@nuxt/ui` component set) |

Defaults: a bare `/frontend-review` on a working tree → `quick` + `"diff"`. A
`--scope`/`--file` with no depth → `standard`. Only go `deep` when explicitly asked.

**Flags:** `--comment` → post findings as inline PR comments. `--fix` → apply the safe
remediations (v3→v4 renames, redundant-overlay-`UCard` unwraps) to the working tree.
Both can combine with any scope/depth.

## 2. Severity map (reuse the review skill's 3 levels + format)

| Level | Meaning | Sources |
|-------|---------|---------|
| 🔴 **Critical** | A hard, documented convention break — **blocks** the CI gate | v3 component name (`UDropdown`/`UDivider`/`UToggle`/`UNotification`); `UCard` inside `UModal`/`USlideover`/`UDrawer`; Options API in a `.vue`; overlay clearly missing the `#content="{ close }"` pattern |
| 🟡 **Warning** | Likely off-convention; advisory | raw `<button>`/`<input>`/`<select>`/`<textarea>`/internal `<a>` where a Nuxt UI / crouton component applies; hand-rolled overlay markup; hardcoded brand/semantic color |
| 🔵 **Note** | Polish | bare `export default {}` nit; one-off hardcoded color; minor drift |

Same emoji + report format as `/review` and `/a11y`, so a mixed code-cleaning pass
reads consistently.

## 3. Gather the scope

**Uncommitted** (`/frontend-review`, `--scope`, `--file`):
```bash
git diff --name-only --diff-filter=d | grep -E '\.vue$'          # unstaged
git diff --cached --name-only --diff-filter=d | grep -E '\.vue$' # staged
```
**Recent commits** (`/frontend-review last N`):
```bash
git diff --name-only HEAD~N..HEAD | grep -E '\.vue$'
```
If `--scope` is set, `Glob` `packages/<pkg>/**/*.vue` (or `apps/<pkg>/**/*.vue`).
If the diff has **no** `.vue` files, say so and stop — this skill only reviews templates.

## 4. Spawn the subagent

Spawn `frontend-review` via the `Agent` tool with `{ scope, depth, fix }` in the prompt.

- **< 5 files** → **one** subagent (or just do the static pass inline if it's a single
  small file — agent overhead isn't worth it for one `--file`).
- **5+ files** → **fan out**: split the files into groups (by directory —
  `components/`, `pages/`, `layouts/`), spawn one `frontend-review` subagent per group
  with its file subset as `scope`, and launch them **in parallel** (multiple `Agent`
  calls in one message). Same parallelization rule as `/review`. The agents are
  **synchronous** — you hold their results when they return; never report "running in
  the background".

Pass `fix` through only when the user asked for `--fix` (so a plain review run never
touches files).

## 5. Collate & report

Merge the agents' findings, de-dupe anything the same rule flagged twice, and print
the **review skill's report format**:

```
## Frontend Review Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | X |
| 🟡 Warning | Y |
| 🔵 Note | Z |

### 🔴 Critical

#### [Short title]
**File:** `path/to/file.vue:42`
**Rule:** `v3-name` (or overlay-ucard / overlay-content-slot / options-api / raw-html / hardcoded-color)
**Issue:** [Which convention is broken — "uses the v3 `UDropdown`; v4 is `UDropdownMenu`"]
**Fix:** [The exact rename/component to use]

--- (repeat for 🟡 / 🔵)
```

If nothing found:
```
## Frontend Review: clean ✅
Reviewed N templates, no convention issues found.
```

Mark each finding `confirmed` (a deterministic signal backs it) vs `suspected` (a
reasoned smell), mirroring red-team/a11y — don't present a reasoned raw-`<button>`
call as a confirmed violation.

## 6. `--comment` — inline PR comments

When `--comment` is set and the work is on a PR, post each finding as an **inline
review comment** on the offending `file:line`, dovetailing with the existing
`🎯 Preview feedback` / `♿ A11y` machinery:

1. `mcp__github__pull_request_read` to resolve the PR for the current branch and its
   head SHA.
2. For each finding, `mcp__github__add_comment_to_pending_review` with the file `path`
   and `line`, body = the finding (lead with the 🔴/🟡/🔵 + rule, then Issue/Fix).
   Prefix the body with a `🧩 Frontend` tag so it's distinguishable from
   `🎯 Preview feedback`, `♿ A11y`, and code-review comments.
3. `mcp__github__pull_request_review_write` to submit the pending review as `COMMENT`
   (never auto-`REQUEST_CHANGES` / `APPROVE`).

If there's no PR (local-only), skip inline comments and just print the report — say so
rather than erroring.

## 7. `--fix` — apply safe remediations

When `--fix` is set, the agent applies (or you apply, for a small inline run) **only**
the safe, deterministic rewrites — the same set the agent doc lists:

- v3 → v4 name rename (`UDropdown`→`UDropdownMenu`, `UDivider`→`USeparator`,
  `UToggle`→`USwitch`, `UNotification`→`UToast`) — checking props still map; report
  anything ambiguous instead of guessing.
- Redundant `UCard` inside an overlay (pure wrapper, no card props) → unwrap into the
  `#content` slot's `<div class="p-6">`.

Then **`pnpm typecheck`** the affected app(s)/package — never leave the tree red:
```bash
pnpm -r --filter './apps/*' typecheck   # or the specific package's typecheck
```
Anything needing real judgment (raw `<button>`→`UButton` behaviour, an
Options→`<script setup>` migration, a color→token swap) is **reported, not auto-fixed**.

## 8. Offer to fix (when not already `--fix`)

After printing the report (and any `--comment`s), close with the review skill's offer:

> Want me to fix any of these? (all / critical only / pick by number)

If the user says "all" or "critical only", apply the safe remediations directly — no
per-fix confirmation — then `pnpm typecheck`. Findings that aren't in the safe set get
called out as "needs a human decision" with the reason (e.g. "raw `<button>`→`UButton`
needs prop/slot judgment").

## Relationship to the other entry points

- **`/review`** carries a few Nuxt UI v4 bullets as honor-system reminders;
  `/frontend-review` is the **dedicated, diff-scoped, severity-rated, fixable** layer
  that owns the full convention checklist + the v3→v4 autofix.
- It sits beside **`/a11y`** (accessibility), **`/ui-proposal`** (human design-look
  sign-off), **`/review`** (general code review), and **`/red-team`** (security) —
  same spawn-and-collate shape, different lens. Reach for `/frontend-review` when you
  specifically want "are we on Nuxt UI 4 / crouton components, correctly", with the
  option to comment or fix.
- **CI runs the same engine automatically** (mirroring the red-team/a11y workflows):
  `.github/workflows/frontend-review.yml` runs the subagent at `depth=quick` on a PR
  diff — posts a sticky `<!-- frontend-review -->` comment and **fails the check on a
  🔴 finding** (diff-scoped, so never on the pre-existing backlog). `/frontend-review`
  is the **on-demand** brain and human entry point for the same machinery. The workflow
  MUST follow the **Claude-action workflow standard** in `.claude/agents/CLAUDE.md` —
  notably the `--allowedTools` grant, without which the gate fails open (#834/#1036).
