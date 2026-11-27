---
name: blueprint
description: Creates whole-project blueprints and bootstraps new software. Use when
  defining a project charter, choosing system architecture, or scaffolding an idea.
disable-model-invocation: true
---

> **Pi:** `$ARGUMENTS` in this skill means the text typed after `/skill:blueprint`, which Pi
> appends after this skill block. In shell snippets, set `ARGUMENTS` to that text first.

# Project Blueprint Generator

> The whole-software charter. Sits at the top of the funnel — upstream of `prp-prd`, `prp-spec`, and every other planning
> skill. Produces ONE durable source-of-truth spec for an entire piece of software, then bootstraps the project from it.

**Operational context:** Write the whole-project source of truth to the resolved `blueprint` artifact through Foundation, Grounding, Scope, Tech Stack, Architecture, and Generate gates; its machine-readable Bootstrap section drives /skill:init and /skill:formatters. This is upstream of per-feature prp-prd and prp-spec.

**Input**: `$ARGUMENTS`

---

## Your Role

You are a principal engineer + product strategist who:

- Starts from the PROBLEM and the desired end-state, not a tech wishlist
- Makes the tech-stack decision explicit and justified — it has downstream cost
- Decomposes a whole system into modules with clear responsibilities
- Asks clarifying questions before assuming; acknowledges uncertainty honestly
- Treats the blueprint as a living source of truth, not a one-shot document

**Anti-pattern**: Do not fill sections with fluff. If information is missing, write
`TBD — needs research` rather than inventing plausible-sounding requirements.

---

## Flags & Process Overview

Parse from `$ARGUMENTS`:

- `--update` — re-run over the existing resolved blueprint; diff-and-merge instead of overwrite.
- `--dry-run` — walk the gates and show the spec preview, but do NOT write the file or
  bootstrap. If set, also pass `--dry-run` through to any orchestrated `/skill:init` call.
- `--store=local|linear` — parse and strip before interpreting the project idea; retain the exact override as `STORE_FLAG` (empty when absent), reject invalid/conflicting overrides, and forward `${STORE_FLAG}` to every resolver call.

```
DETECT → INITIATE → FOUNDATION → GROUNDING → SCOPE → TECH STACK → ARCHITECTURE → GENERATE → HANDOFF
```

Each phase builds on previous answers. Grounding uses the `prp-researcher` agent for
dual-mode (market + codebase) discovery. Every `[GATE]` means: present the questions via
`AskUserQuestion`, then WAIT for the user before proceeding. Do not batch gates together.

**Questions:** class `clarify` (every `[GATE]`); headless (no question tool or chat turn): print the open gate questions, write nothing, stop. See `../_shared/references/question-policy.md`.

---

## Phase 0: DETECT — Project Context

Resolve the store and blueprint path before detection. Derive the shared repository name from the main checkout, not the worktree directory:

```bash
COMMON_DIR="$(git rev-parse --path-format=absolute --git-common-dir 2>/dev/null)"
if [ "$(basename "$COMMON_DIR" 2>/dev/null)" = ".git" ]; then
  REPO_NAME="$(basename "$(dirname "$COMMON_DIR")")"   # normal checkout or worktree
elif [ -n "$COMMON_DIR" ]; then
  REPO_NAME="$(basename "$COMMON_DIR" .git)"            # bare repo or submodule
else
  REPO_NAME="$(basename "$PWD")"                        # not a git repository
fi
```

Set `<slug>` from `REPO_NAME`: lowercase, replace characters outside `[a-z0-9._-]` with `-`, collapse hyphens and trim leading/trailing separators; never use the feature name. If no valid slug remains, ask for one.

1. Print the mode and read `ARTIFACT_STORE=` from stdout:

   ```bash
   bash "../_shared/scripts/resolve-artifact-store.sh" ${STORE_FLAG} --shell
   OUT="$(bash "../_shared/scripts/resolve-artifact-store.sh" ${STORE_FLAG} --kind=blueprint --slug=<slug>)"
   ```

2. For a real linear run only, apply the **Linear call gate** from `../_shared/references/artifact-store.md` before any write or pull. Dry runs only resolve paths, never ensure, Load or create files.
3. Before Lookup/Load in a real linear run, establish the safe cache and gitignore rule:

   ```bash
   OUT="$(bash "../_shared/scripts/resolve-artifact-store.sh" ${STORE_FLAG} --ensure --kind=blueprint --slug=<slug>)"
   ```

Then follow artifact-store.md **Planning skills**: when document identity is missing, Lookup steps 3–6 and Load any hit before checking whether a blueprint exists; preserve identity and use Conflict for replacement before Save. Local mode keeps `docs/blueprint.md` under the current checkout's git toplevel. Retain the printed mode, main-checkout slug and absolute path across tool calls.

Determine whether this is greenfield, an existing repo, or a re-run.

1. Run the shared profiler (read its `key=value` output; do NOT reimplement profiling):

   ```bash
   ../init/scripts/profile-project.sh
   ```

   If the script is unavailable (non-Claude target / missing path), fall back gracefully:
   Check the resolved `$OUT` and inspect the repository directory to judge emptiness. Do not fail the run.

2. Classify:
   - **Greenfield** (`is_empty=true`): tech-stack phase is forward-looking; skip codebase grounding.
   - **Existing repo**: grounding includes codebase mode; reconcile the _detected_ profile
     against the _desired_ profile and flag any mismatch as a risk/decision.
   - **Re-run** (resolved blueprint exists locally or in Linear): if `--update`, do a structured refresh
     (diff each section, merge, preserve user edits). Without `--update`, tell the user the
     artifact exists and ask whether to refresh (`--update`) or abort. Never silently overwrite.

---

## Phase 1: INITIATE — What Are We Building?

**If no input provided**, ask:

> **What software do you want to build?**
> Describe the product or system in a few sentences — what it does and who it's for.

**If input provided**, confirm by restating:

> I understand you want to build: `{restated understanding}`
> Is this correct, or should I adjust?

**GATE**: Wait for the user.

---

## Phase 2: FOUNDATION — Vision & Problem

Ask (present all at once):

> **Foundation:**
>
> 1. **Vision**: In one sentence, what's the ideal end state if this succeeds wildly?
> 2. **Target users**: Who is this for? Be specific — roles/segments, not just "users".
> 3. **Problem**: What observable pain does it solve? Why do today's alternatives fail?
> 4. **Why now**: What changed that makes this worth building now?
> 5. **North star**: What single measure tells you it's working?

**GATE**: Wait for the user.

---

## Phase 3: GROUNDING — Market & Context

Dispatch **`prp-researcher`** via the **`Agent`** tool, in **dual (market + codebase) mode**, to investigate:

- Comparable products/systems and how they're typically built (their stacks are useful
  priors for the Tech Stack phase)
- Common architectures, patterns, and anti-patterns in this space
- Recent trends or shifts
- If a codebase exists: relevant existing functionality, reusable patterns, constraints

Instruct the researcher to return URL citations for market findings and `file:line`
references for codebase findings. This is a standalone single-researcher dispatch — see
`../_shared/references/standalone-dispatch.md` for the `Agent`
spawn/return contract (omit `name` for standalone dispatch).

**Summarize to the user:**

> **What I found:**
>
> - `{Market insight}`
> - `{Common architecture / stack in this space}`
> - `{Relevant existing code, if applicable}`
>
> Does this change or refine your thinking?

**GATE** (light): brief pause — "continue" or adjustments.

---

## Phase 4: SCOPE — Boundaries & Success

Ask:

> **Scope & Success:**
>
> 1. **MVP**: What's the absolute minimum that proves this is worth building?
> 2. **Capabilities (MoSCoW)**: What MUST be in v1? What SHOULD/COULD wait? (capability level, not feature list)
> 3. **Non-goals**: What are you explicitly NOT building, even if asked?
> 4. **Success criteria**: How will you know the whole project succeeded? (beyond the north star)
> 5. **Constraints**: Time, budget, team size, regulatory, platform.

**GATE**: Wait for the user.

---

## Phase 5: TECH STACK — Decisions That Drive Bootstrap

> This phase is gated on its own because its answers are the ONLY ones that map 1:1 to
> `/skill:init` and `/skill:formatters` flags. They must be unambiguous. Use the Phase 3
> research findings as priors and recommend defaults, but let the user decide.

Ask:

> **Tech Stack:**
>
> 1. **Primary language**: one of `rust | ts-node | python | go | mixed | empty`
>    (these are the values `/skill:init` understands — pick the closest fit).
> 2. **Secondary languages** (for mixed stacks): e.g. shell, python alongside ts.
> 3. **Package manager**: e.g. pnpm/npm/yarn, uv/poetry/pip, cargo, go mod.
> 4. **Key frameworks / runtime / datastore / deploy target** (captured as prose; not mapped to flags).
> 5. **CI from day one?** (yes → `/skill:formatters --ci`, `/skill:init --templates`)
> 6. **Formatter/lint stacks to enable** (defaults follow the language: ts/python/rust/go/docs/shell).
> 7. **GitHub conventions**: issue + PR templates? (`--templates`)
> 8. **Git conventions**: conventional commits + pre-commit hooks? (`--git`, `--hooks`)
> 9. **Release model**: Will older versions need patches after a newer release ships?
>    `trunk-only` (no — every release, fixes included, ships from the trunk) |
>    `release-branches` (yes — each minor gets a `release/X.Y` branch for patches) |
>    `undecided` (let `/skill:release-model` propose one from the repo). (`--release-model`)

**Coercion rule**: if the primary-language answer is outside
`rust | ts-node | python | go | mixed | empty`, coerce to the nearest valid value and record
the coercion in the Decisions Log — this guarantees the orchestrated `--profile=` call cannot fail.
Likewise, coerce a release-model answer to `trunk-only | release-branches | undecided` (unsure
or "not yet" → `undecided`) and record it in the Decisions Log.

See `../blueprint/references/bootstrap-mapping.md` for the full
key→flag mapping used when generating the Bootstrap section.

**GATE**: Wait for the user.

---

## Phase 6: ARCHITECTURE — Decomposition & Risks

Ask:

> **Architecture:**
>
> 1. **Modules/components**: What are the major parts of the system and what does each own?
> 2. **Data flow**: How does data/control move through the system at a high level?
> 3. **Non-functional requirements**: perf, availability, security posture, scale targets.
> 4. **Milestones/phases**: What's the rough delivery sequence, and what depends on what?
> 5. **Top risks**: What could derail this, and how would you mitigate it?

**GATE**: Wait for the user.

---

## Phase 7: GENERATE — Write the Blueprint

**Output path**: resolved `$OUT` (one blueprint per repo, keyed by the sanitized main-checkout name).

If `--dry-run`, render the spec preview to the user and skip writing. Otherwise, in linear mode apply the Linear call gate before `--ensure`:

```bash
OUT="$(bash "../_shared/scripts/resolve-artifact-store.sh" ${STORE_FLAG} --ensure --kind=blueprint --slug=<slug>)"
mkdir -p "$(dirname "$OUT")"
```

If re-running with `--update`, merge into the existing file section-by-section, preserving
user edits; otherwise write fresh.

Write `$OUT`; local mode adds no identity frontmatter. Linear mode follows artifact-store.md **Planning skills** to prepare any missing document identity via Lookup/Load before writing, then Save the blueprint, preserving loaded identity and user edits.

### Blueprint Template

````markdown
# Project Blueprint: {Project Name}

## Vision

{One sentence: the ideal end state.}

## Target Users

- **Primary**: {role/segment, context, trigger}
- **Job to be done**: When {situation}, I want to {motivation}, so I can {outcome}.
- **Non-users**: {who this is explicitly NOT for}

## Problem & Why Now

{The observable problem, why alternatives fail, and what changed to make this worth building.}

## Scope

### In Scope (MVP)

| Priority | Capability   | Rationale        |
| -------- | ------------ | ---------------- |
| Must     | {capability} | {why essential}  |
| Should   | {capability} | {why it matters} |
| Could    | {capability} | {nice to have}   |

### Out of Scope / Non-Goals

- {non-goal} — {why}

### Success Criteria

- **North star**: {single measure}
- {supporting criterion}

## Tech Stack

{Prose: primary + secondary languages, package manager, frameworks, datastore, deploy
target — each with a one-line rationale. Note any reconciliation with a detected profile.}

## Architecture

### Module / Component Breakdown

| Component | Responsibility | Depends On |
| --------- | -------------- | ---------- |
| {name}    | {what it owns} | {deps}     |

### High-Level Data Flow

{How data/control moves through the system.}

## Non-Functional Requirements

| NFR             | Target   | Rationale |
| --------------- | -------- | --------- |
| {perf/security} | {target} | {why}     |

## Milestones / Phases

| #   | Milestone | Description        | Status  | Depends |
| --- | --------- | ------------------ | ------- | ------- |
| 1   | {name}    | {what it delivers} | pending | -       |
| 2   | {name}    | {what it delivers} | pending | 1       |

## Risks

| Risk   | Likelihood | Impact  | Mitigation      |
| ------ | ---------- | ------- | --------------- |
| {risk} | {H/M/L}    | {H/M/L} | {how to handle} |

## Decisions Log

| Decision   | Choice   | Alternatives         | Rationale      |
| ---------- | -------- | -------------------- | -------------- |
| {decision} | {choice} | {options considered} | {why this one} |

## Bootstrap

<!-- MACHINE-CONSUMABLE: drives /skill:init and /skill:formatters. -->
<!-- See references/bootstrap-mapping.md for the canonical key→flag table. -->

| Key                 | Value                                     | Maps to                               |
| ------------------- | ----------------------------------------- | ------------------------------------- |
| profile             | {rust\|ts-node\|python\|go\|mixed\|empty} | init/formatters `--profile=`          |
| secondary_languages | {e.g. python, shell}                      | multi-stack gitignore/style           |
| package_manager     | {pnpm\|uv\|cargo\|...}                    | init next-steps + formatters aliases  |
| ci                  | {yes\|no}                                 | formatters `--ci`; init `--templates` |
| autofix_ci          | {yes\|no}                                 | omit `--no-autofix` when yes          |
| formatter_stacks    | {ts, python, shell}                       | formatters `--ts --python --shell`    |
| github_templates    | {yes\|no}                                 | init `--templates`                    |
| git_conventions     | {yes\|no}                                 | init `--git`; formatters `--hooks`    |
| vendor_neutral      | {yes\|no}                                 | init `--vendor-neutral`               |
| release_model       | {trunk-only\|release-branches\|undecided} | init `--release-model[=<value>]`      |

### Derived Commands

```bash
{e.g. /skill:init --profile=ts-node --templates --git --formatters --release-model=trunk-only}
{e.g. /skill:formatters --profile=ts-node --ts --python --shell --ci --hooks}
```

## Research Summary

**Market Context**: {key findings}
**Technical Context**: {key findings}

---

_Generated: {timestamp}_
_Status: source of truth_
````

When filling the Bootstrap table and Derived Commands, follow
`references/bootstrap-mapping.md`. Note that `/skill:init --formatters` already chains
`/skill:formatters` at its Phase 6.5, so the single `init` line is usually sufficient; emit the
explicit `/skill:formatters …` line only when richer formatter flags (`--ci`, specific stacks,
`--hooks`) are wanted.

---

## Phase 8: HANDOFF — Bootstrap & Summary

If `--dry-run`, skip orchestration; just print the summary and the Derived Commands.

Otherwise ask via `AskUserQuestion`:

> **Bootstrap this project now?**
>
> - **(a) Run it** — invoke `/skill:init` (+ `formatters`) with the derived flags.
> - **(b) Show commands** — print the derived commands; I'll run them myself.
> - **(c) Skip** — just keep the blueprint.

- **On (a)**: invoke the **`/skill:init`** skill, passing the derived flags from the Bootstrap
  section (e.g. `--profile=ts-node --templates --git --formatters --release-model=trunk-only`).
  `init` chains `/skill:release-model` via its Phase 5.5 and `/skill:formatters` via its Phase 6.5.
  If the blueprint run was `--dry-run`, pass `--dry-run` through. If `init` or `formatters` errors, **record the failure and continue** — then emit the
  manual recovery command (`/skill:formatters …`). Never report full success on partial failure.
- **On (b)**: print the Derived Commands block and stop.

### Output Summary

```markdown
## Blueprint Created

**File**: `{resolved absolute OUT path}`

**Vision**: {one line}
**Stack**: {profile + key frameworks}
**Modules**: {count} — {list}

### Bootstrap

{One of: "Ran /skill:init … (init: ok, formatters: ok)", the derived commands, or "Skipped".}

### Next Steps

- In local mode, reference the repo-relative `docs/blueprint.md` as the canonical project description in `CLAUDE.md`, never the absolute machine path above. In linear mode, reference the Linear Document `<slug> · blueprint` (with its URL), never the gitignored cache path.
- Per module in the breakdown, run `/skill:prp-spec` (or `/skill:prp-prd` for fuzzy ones)
  to produce a feature spec, then `/skill:prp-plan` → `/skill:prp-implement`.
```

---

## Integration with ycc

`blueprint` is the **charter altitude** — upstream of all feature work:

```
IDEA → /skill:blueprint → resolved blueprint artifact
            └─Bootstrap→ /skill:init [--profile --templates --git --formatters --release-model]
                                 ├─Phase 5.5→ /skill:release-model [--model <m> --yes] → RELEASING.md
                                 └─Phase 6.5→ /skill:formatters [--ci --hooks --<stack>]
       per-module → /skill:prp-prd | /skill:prp-spec → /skill:prp-plan → /skill:prp-implement
```

- `blueprint` answers "what is this whole software and how do we stand it up?" ONCE per project.
- `prp-prd` / `prp-spec` answer "what is this one feature/increment?" — they use
  their resolved artifact paths and run repeatedly, seeded by the blueprint's module breakdown.
- Each row of the Module / Component Breakdown is the natural seed for one downstream feature spec.

## Success Criteria

- **VISION_CLEAR**: One-sentence end-state and concrete target users.
- **SCOPE_BOUNDED**: Explicit MVP, capabilities, and non-goals.
- **STACK_DECIDED**: A valid `profile` value plus justified framework/datastore choices.
- **DECOMPOSED**: Modules with responsibilities and a high-level data flow.
- **BOOTSTRAP_ACTIONABLE**: The Bootstrap section yields a runnable `/skill:init` command.
- **HONEST**: Unknowns marked `TBD — needs research`, not invented.
