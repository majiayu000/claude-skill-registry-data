---
name: init-workspace
user-invocable: true
version: 3.2.0
argument-hint: <target-dir>
author: "Gabriel Trabanco <1969593+gtrabanco@users.noreply.github.com>"
license: MIT
description: >
  Adapt the workflow scaffold to a new repository or add only missing substrate
  blocks to an existing install. Every install, hook, and overwrite needs
  explicit consent. Triggers: "init-workspace", "set up agentic workflow",
  "upgrade workflow scaffold".
---

# Init Workspace

Turn an empty or existing repo into one that works with the agentic workflow:
copy the generic scaffold, then **tailor it to this project** instead of leaving
raw placeholders.

## Turn contract — verify before ending the turn

```
✓ The adapted scaffold and repository-state ledger are written (or the merge/abort decision was asked) and remaining placeholders are listed
✓ Nothing was installed or overwritten without an explicit yes
✓ Artifact language: explicit user instruction > the project's declared docs language > English. The CONVERSATION language never decides — a Spanish prompt still produces English PRs/issues/commits/SPECs unless one of the first two says otherwise
✓ The closing `→ Next:` block is printed as the ABSOLUTE last output
```

About to end the turn with any box unchecked? The turn is NOT done — complete
the missing box first (weak models drop end-of-document duties; this list is
first on purpose).

## When to use

- Setting up a repo to use these skills and you want the documentation substrate
  (`AGENTS.md` + `docs/` map + templates) adapted to the project, not just copied.
- Prefer this over a static `npx degit gtrabanco/agentic-workflow/template` when you
  want the gate commands, architecture, and doc domains filled in by interview.

## Step 0 — Discover the project (always first)

Inspect the target dir (`[target-dir]`, default cwd) before touching anything:

- An existing **agent guide** (`AGENTS.md`, or a legacy `CLAUDE.md`), `docs/`,
  `.github/`? If so, **do not clobber** — check first whether it's an
  **agentic-workflow scaffold** (marker: an agent guide present *and* either
  `docs/features/ROADMAP.md` or a `docs/workflow/` dir). If both markers are
  present, offer **upgrade** as the default action, alongside merge /
  adapt-in-place / abort — see **Upgrade mode** below. If an agent guide or
  `docs/` exists but the markers are absent (a foreign scaffold), stay in
  bootstrap and ask merge / adapt in place / abort as before.
- Detect the stack from manifests (`package.json`, `pyproject.toml`, `go.mod`,
  `Cargo.toml`, `Gemfile`, …) to *propose* gate commands and naming conventions.
- Note the git state (is it a repo, what's the default branch, and the **remote
  URL → forge**: github.com → GitHub/`gh`, gitlab → GitLab/`glab`, else ask).


## Progressive loading — bootstrap or upgrade, never both

The reference allowlist is exactly the five linked paths below. Never invent or
read another `references/` path. Step 0 selects exactly one route:

**Hard rule for an existing Claude Code, Cursor, Copilot, or OpenCode
scaffold:** LOAD exactly `references/UPGRADE.md`. A missing committed safety
adapter is upgrade work, not a missing vendor primitive. Do not load bootstrap
or portability unless the runtime platform has no named adapter at all.

- Bare/foreign repository: read
  [bootstrap discovery](references/BOOTSTRAP_DISCOVERY.md), complete its
  interview, then read [bootstrap write](references/BOOTSTRAP_WRITE.md).
  Both the discovery and write routes load
  [SERENA language servers](references/SERENA.md) for stack detection.
- Existing agentic-workflow scaffold: read [upgrade](references/UPGRADE.md)
  only. Its additive-only rule is absolute; do not replay bootstrap.
  The upgrade route loads [SERENA language servers](references/SERENA.md)
  for the additive provisioning step.
- No named adapter exists for the detected runtime platform: add
  [portability](references/PORTABILITY.md) only for that fallback. Claude Code,
  Cursor, Copilot, and OpenCode are named supported adapters; a missing adapter
  file is repaired by upgrade and does not trigger portability.

All resources are one hop from this file. Existing files, hook consent,
installation consent, and residual reporting are fixed contracts. Missing
template/migration evidence is reported by the selected route, never filled by
guessing. An existing OpenCode scaffold with only its safety adapter missing
loads exactly upgrade and skips bootstrap plus portability.

## Guardrails

- **Never overwrite an existing agent guide (`AGENTS.md`, or a legacy
  `CLAUDE.md`) or `docs/` without explicit consent.**
- **One guide, one name.** `AGENTS.md` is the guide; a legacy `CLAUDE.md` is
  retired only in upgrade mode, only with an explicit yes, and only after any
  content unique to it is folded into `AGENTS.md` first. A user whose Claude
  Code release predates `AGENTS.md` support may keep it — that choice is
  reported as a residual, never treated as drift to repair.
- **Additive-only, never clobber (upgrade mode).** Upgrade mode only adds
  blocks the project lacks and fills raw placeholders — it never rewrites or
  deletes a block the project already tailored, even if the current template
  changed that block too. A genuine re-tailor is a separate, explicitly
  requested bootstrap adapt-in-place run, never something upgrade mode does
  on its own. **The urgency label seeding is additive-only the same way:**
  create a missing `urgent`/`fix-next` label, never touch one that already
  exists (name, color, or description a project already customized).
- **Serena convention.** `.serena/project.yml` is committed; `project.local.yml`
  and `cache` stay local. Never write `.serena/` config without consent. LSP
  never verifies documents — false positives happen when a file type's server
  is not listed (markdown/yaml/json are never auto-detected), and a listed
  server that fails to start must be removed (one failure disables every
  server in the project). Document verification is a script's job.
- **Never redefine the urgency label vocabulary here.** `skills/triage-issue
  /SKILL.md` is the sole owner of the `urgent`/`fix-next` names, colors, and
  apply rules — this skill only seeds those two labels into the repo; it never
  invents a third label or changes what the two mean.
- Docs-only scaffolding; no app code, no dependencies installed unprompted.
- Architecture-agnostic: record the project's pattern, don't impose one.
- Honest placeholders over invented specifics; flag what's left to fill.
- Honor the project's **Workflow conventions** once present; on an existing repo,
  don't work on its default branch and never commit/push unless asked.

## Unit document conventions (the adaptive lane)

The adaptive lane (feature 61) replaces the fixed pipeline with a single-unit-
document model. Every NEW unit produces one `SPEC.md` under
`docs/features/<NN>-<slug>/` with 13 sections: Objective, Why, User outcome,
Acceptance criteria, Non-goals, Future cost, Applicable tests, Known pre-existing
issues, Tasks, Evidence, Progress log, Next, References.

Conventions written into the project's AGENTS.md:

- **Triage**: the lane conductor (`/unit-lane` / `workflow-status`) returns a
  deterministic ordered list of steps (research, design, plan, implement,
  tests, evidence, review, docs, release).
- **Guards**: `scripts/diff-guard.mjs` measures `git diff --stat` at boundaries;
  overflow → mandatory re-triage. Anti-gaming: "NEVER shrink a diff by deleting
  comments, blank lines, docs or tests."
- **Evidence rows**: one per AC — what was run, exit/digest, output (≤2 lines),
  verified-by. Verified, not claimed.
- **Progress log**: dated entries (`YYYY-MM-DD HH:MM`) per step taken.
- **Commit format**: `type(scope): description` (conventional commits).
- **Roadmap status**: `idea → defined → planned → in-progress → done`.

These are written by bootstrap (fresh) and upgrade mode (additive-only for pre-
lane installs). A pre-lane project gets only: the lane conventions section in
AGENTS.md, the unit doc template under `docs/features/_TEMPLATE/`, and the
docs-map row for the unit doc.

## Normalized Repository State

Seed `docs/workflow/REPOSITORY_STATE.md` from the template. Explain that
discovery freezes evidence before planning and only the resolver updates facts.

## Architectural invariants

Offer `docs/architecture/ARCHITECTURAL_INVARIANTS.md` as an optional project
contract for long-lived architectural rules. Its entries must name a stable ID,
repository evidence, and the authority that can change the rule. Do not infer a
rule from the implementation or a feature SPEC. A project without this document
remains compatible; record `n/a: no project invariants declared` in later
workflow artifacts rather than creating one silently.


## Portability

The scaffold is vendor-neutral; only hook activation differs. When the detected
agent has no named adapter, follow [portability](references/PORTABILITY.md) and
keep it as an explicit residual. A supported Claude Code, Cursor, Copilot, or
OpenCode adapter does not load this fallback.

## Relationship to other skills

- `npx degit gtrabanco/agentic-workflow/template` — the static copy this skill
  adapts. Use that when you want the raw scaffold and will fill it yourself.
- `docs/workflow/PORTABLE_PROMPT.md` — regenerates the **skills** adapted to a
  project (behavior). This skill adapts the **substrate** (docs). Complementary.
- After init: `discover-repository-state` → `workflow-status` (to see what's
  startable) → `/unit-lane` (the lane conductor); run `audit-docs` to confirm
  the scaffold is coherent.

## Done when

- A tailored `AGENTS.md` + `docs/` scaffold + `.github/` templates exist in the
  target, unused folders pruned, residual placeholders flagged, the platform's
  companion review skills are recorded (and offered), and the `urgent`/
  `fix-next` labels are seeded (scaffold) or additively reconciled (upgrade),
  and every accepted safety adapter is active and fixture-tested — or explicitly
  listed as a residual when its hook API/dependency was unavailable.
  The adaptive lane conventions (unit document, triage, catalog steps, guards,
  evidence, commit formats) are written into AGENTS.md.
- The Serena project config is provisioned (or reported as a residual with the
  reason, and the health check ran).
- **The closing `→ Next:` block is printed** (plus the offer to install the skills):

  ```
  → Next: /discover-repository-state — freeze repository evidence before planning
    · raw idea → /workflow-status → /unit-lane (the lane conductor)
    · next roadmap entry → /unit-lane (tridirection decides catalog steps)
    · confirm the scaffold is coherent → /audit-docs
  ```
