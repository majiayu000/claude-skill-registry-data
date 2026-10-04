---
name: solution
description: Use when about to produce an implementation plan that will be executed by the orchestrator. Wraps ../_vendored/writing-plans/SKILL.md to produce a plan with YAML frontmatter declaring phases, task DAG, and test commands. Triggers when invoked by the orchestrator OR when user explicitly requests an "epic plan" / plan-with-frontmatter.
---

# Solution Plans

Wrap `../_vendored/writing-plans/SKILL.md` to produce plans suitable for autonomous epic execution.

**Announce at start:** "I'm using the solution skill to create a plan with DAG frontmatter."

## Posture: maximally-detailed plans + technical decision-gates

`solution` owns the **technical / implementation / infrastructure** decisions. Its job is to make
automated delivery *higher-quality* by removing ambiguity before a wave ever runs. Two dials, both
turned up:

1. **Maximally-detailed plans.** The implementer subagent that runs a task sees only the task body
   and its verification block — it does NOT get to interview you. So the plan must be a *contract*,
   not a sketch. For every task, the body must carry the literal artifacts the implementer needs:
   - **Paste literal code / types / signatures / fixtures** the task must produce or match —
     function signatures, type/dataclass definitions, config schema fragments, exact test fixtures,
     expected input/output samples, error-message strings. Do not describe what to write when you
     can paste what "done" looks like.
   - **Complete file allowlists** — every file the task may touch, new files marked `(new)`, plus
     the regression-guard list of files/services it must NOT touch. An incomplete allowlist either
     blocks a legitimate edit or lets drift through.
   - **Explicit per-task verification** — concrete acceptance criteria and the exact test
     command(s), so "did this task succeed?" is decidable without judgment. (Step 2.5.)
   Vague, judgment-heavy task bodies are the top cause of wave rework. A task a competent stranger
   could implement from the body alone is the bar.

2. **Technical decision-gates.** Surface weighty *technical* forks to the human via the
   `asking-questions` skill rather than deciding them silently: cross-cutting architecture choices,
   a new dependency, a data-migration strategy, an irreversible infra/schema commitment, a
   security-sensitive design, or a phase/DAG shape with real trade-offs. Load
   `../asking-questions/SKILL.md`, write the decision prose first (question + why + options'
   pro/con + recommendation), then fire the capture; honor the injected `question_style`. Settled,
   grounding-obvious engineering calls do not need a gate — state the assumption and proceed. A real
   trade-off does.

   **Fleet-context branch (technical decision-gates).** In a fleet-launched run — one whose
   invocation carried the literal `fleet-context: <agent>` marker (see **Execution context**
   below) — a decision-gate never fires the `asking-questions` capture — no human is
   watching it. Write the decision prose exactly as above, then raise it as a registry
   `## Questions` row instead of buttons, with `default:` = the recommendation that prose just
   computed (never a fresh guess). Urgency follows the fork: `advisory` — restating that
   recommendation as the required `assumption:` — when the only artifact is plan text (the plan is
   on disk and editable before any wave runs), and `waiting` when the fork commits something
   irreversible (a data-migration strategy, a schema/infra commitment, a security-sensitive design,
   a newly pinned dependency), which is exactly the class this dial exists to catch. Standalone
   interactive behavior is unchanged.

**Contract invariant (do not violate):** these dials add *detail and process gates only*. The plan's
**output schema is frozen** — valid YAML frontmatter with integer task keys, `phases`, per-task
`deps`, `per_wave_worktrees: true`, and `test_commands` exactly as specified below. Adding detail to
task bodies and verification blocks is required; changing the frontmatter contract is forbidden (the
orchestrator's parser and the acceptance harness depend on it byte-for-structure).

## When to use

- Invoked by `orchestrator` during epic bootstrap
- User explicitly asks for an epic plan or plan-with-frontmatter
- A plan needs YAML frontmatter for the DAG (phases + cross-phase deps)

## When NOT to use

- Single-task plans that don't need a DAG — use `../_vendored/writing-plans/SKILL.md` directly
- Existing plans that already have frontmatter — they're already in the right format

## Execution context (who is the human surface for this run?)

`solution` runs in one of two contexts, and every `AskUserQuestion` gate below — including the
technical decision-gates of Posture dial 2 — branches on which one it is:

- **Standalone interactive** — a human invoked `/project` at the keyboard, or asked for an epic plan
  directly. The human IS the surface: every gate behaves exactly as written, and **nothing below
  changes that path.**
- **Fleet-launched** — a fleet loop's run reached here. Per `<suite_root>/docs/REGISTRY.md`, no loop but
  dev-manager asks the human, so **a fleet-launched run never calls `AskUserQuestion`**. Every site
  that would have asked instead writes a registry `## Questions` row (answered by dev-manager) and
  either proceeds on a stated `default:` or parks for it.

**The mode comes from the caller's marker — `solution` has no `status.md` to inherit from.** Unlike
the orchestrator, `solution` runs once, inside a single invocation: there is no status board and no
self-scheduled wake to re-read the mode from later. Its only signal is the literal line
`fleet-context: <agent>` (e.g. `fleet-context: lead-dev`) in the invocation that called it —
`/project` Step 3 propagates it, and the orchestrator passes its recorded `fleet_context` when it
invokes `solution` directly during bootstrap. No marker in the invocation = standalone interactive.
Never infer fleet mode from anything else (cwd, the spec's `current_state`, who the caller is).

**The canonical description of this contract is `../orchestrator/SKILL.md`, "Fleet invocation
context"** — the marker rule and the "how a fleet-context question works" procedure (raise the row
under the edit-lock with a mandatory `default:` and an urgency per the REGISTRY classification rule;
poll lock-free; map the answer through the SAME canonical-reply mapping the buttons use; flip
`answered -> applied` as the raiser). Follow it verbatim — it is deliberately NOT restated here,
since three copies of one contract is how three copies drift. The one clause that does **not** carry
over is its inherit-the-mode-from-`status.md` rule: `solution` has no status file, so a marker that
was not passed in is simply absent.

**What parking means inside a one-shot skill.** An `advisory` row proceeds immediately on its stated
assumption — no waiting, the plan lands. A `waiting` row means this invocation cannot finish the
plan: report the Q-id to the caller and stop, and let the caller (an orchestrator wake, or the fleet
loop itself) re-invoke `solution` once the row reads `answered`. Do not spin waiting for an answer
inside the invocation.

## Procedure

### Step 1: Invoke writing-plans

Invoke the `../_vendored/writing-plans/SKILL.md` skill with the spec. Wait for it to produce the plan file under `<data_root>/projects/<name>/design/plans/`.

**Require maximal detail in the produced bodies (Posture dial 1).** The plan is executed by
implementer subagents that see only the task body + verification block. Direct writing-plans to make
each `## Task N:` body a self-sufficient contract, and if the returned plan falls short, iterate on
it before proceeding to Step 2. The wave dispatcher reads a body from its `## Task N` or `### Task N`
heading down to the next Task heading or a shallower heading, and refuses to dispatch a task whose
body comes back empty. So keep every section that belongs to a task, `## Files:` included, between
its heading and the next Task heading, at the Task heading's level or deeper. Each task body must carry:

- **Literal artifacts, pasted in** — the exact function/method signatures, type / dataclass / schema
  definitions, config fragments, and test fixtures (input → expected output, error strings) the task
  must produce or conform to. Paste the real text; do not paraphrase "add a function that…".
- **A `## Files:` section** listing every file the task may modify (backtick-quoted paths, `(new)`
  on new files) plus a "do not touch" note naming regression-guard files/services.
- **Discrete, testable acceptance criteria** — one bullet per check, no judgment calls — and the
  exact test command(s) that decide the task.

A task body a competent stranger could implement without asking a question is the bar. Bodies that
are still vague after iteration are the top cause of wave rework — tighten them here, not in-wave.

**Technical decision-gates during authoring.** If writing-plans (or your own DAG analysis) surfaces a
weighty technical fork — a new dependency, a migration strategy, a cross-cutting architecture choice,
an irreversible infra/schema commitment, a security-sensitive design — do NOT resolve it silently.
Load `../asking-questions/SKILL.md` and run a decision-gate (prose first, then capture; honor
`question_style`). Grounding-settled engineering calls proceed without a gate.
**Fleet-context branch:** in a fleet-launched run — one whose invocation carried the literal
`fleet-context: <agent>` marker, see **Execution context** — this gate raises a
registry `## Questions` row instead of firing the capture — same rule as Posture dial 2 (`default:`
= the recommendation the decision prose computed; `advisory` with that recommendation as the
`assumption:` when the fork only changes plan text, `waiting` when it commits something
irreversible). Standalone interactive behavior is unchanged.

### Step 1.5: Inject slug + depends_on into plan frontmatter

After writing-plans produces the plan file, before deriving the DAG:

1. Detect or derive the canonical slug. Read the plan's filename: strip leading `YYYY-MM-DD-` and trailing `-design` if present. Or read an explicit `slug:` field if writing-plans already added one.

2. Detect pre-dependencies by scanning the plan body for explicit "depends on", "after", "blocked by", "requires" phrasing. Capture matching slugs into `<pre_detected_list>`.

3. **Fleet-launched run (`fleet-context` marker present)? Take the fleet-context branch
   below INSTEAD of this call — do not fire the buttons first and read the branch after.**
   Standalone: call `AskUserQuestion` with:
   - **header:** `"Dependencies"`
   - **options:**
     - `{label: "None", description: "This plan does not depend on other epics"}`
     - `{label: "Use pre-detected", description: "Accept the slugs pre-detected from doc body (renders pre-detected list: <pre_detected_list>)"}`
     - `{label: "Specify manually", description: "List slugs via Other (comma-separated)"}`

   The question text must render `<pre_detected_list>` inline so the user sees what was inferred.

   **Fleet-context branch (Dependencies).** In a fleet-launched run — one whose invocation carried
   the literal `fleet-context: <agent>` marker (see **Execution context**) — do NOT call
   `AskUserQuestion`. This gate fires on EVERY plan `solution` authors, so leaving it unbranched
   is what wedges an unattended fleet run. Raise a registry `## Questions` row instead
   (same question text, with `<pre_detected_list>` rendered inline; `--actor <FLEET_CONTEXT>` — the CLI derives `raised_by` from the actor, so name `solution` in the question TEXT rather than hand-writing a composite `raised_by`; `--work <E-NNNN>` — the Queue-row id the dispatching loop is building, or `-` if the invocation did not carry one. **A slug here is rejected (`id_format`, exit 2) and no row is written**, so the branch would silently do nothing) and then **proceed immediately** on
   `default: use the pre-detected slugs — <pre_detected_list>` — the list computed in item 2 above,
   never a list invented here. An empty `<pre_detected_list>` is the "None" answer, i.e.
   `depends_on: []`. Urgency `advisory`, with the required `assumption:` = "proceeding with
   `depends_on: <pre_detected_list>` as detected from the doc body; a wrong list is fixed by editing
   the plan's frontmatter before any wave runs". Take the item-4 branch the default matches, and
   when the row comes back `answered`, fold dev-manager's answer in by editing `depends_on`, then
   flip the row `applied`. Standalone interactive behavior is unchanged.

4. Branch on the response:
   - **If "None":** Set `depends_on: []` in frontmatter.
   - **If "Use pre-detected":** Set `depends_on: <pre_detected_list>` in frontmatter.
   - **If "Specify manually":** Accept the comma-separated slugs from the `Other` field. Parse, strip whitespace, and proceed to slug validation.

5. Validate each provided slug. Check that the slug exists as:
   - a file in `<data_root>/projects/<name>/design/specs/` (after stripping `-design` suffix), OR
   - a file in `<data_root>/projects/<name>/design/plans/` (with or without `.status.md` companion), OR
   - a status.md slug under `<data_root>/projects/<name>/status/`.

   If a slug is not found: **in a fleet-launched run take the fleet-context branch below
   instead of this call**; standalone, call `AskUserQuestion` with:
   - **header:** `"Unknown slug"`
   - **options:**
     - `{label: "Continue (future epic)", description: "Allow the slug; it references a not-yet-created epic"}`
     - `{label: "Correct", description: "Re-prompt for this slug"}`

   If the response is "Continue (future epic)", allow the slug. If "Correct", re-enter the slug-validation loop for that slug (re-prompt the user to provide a corrected slug via `AskUserQuestion` with a text field).

   **Fleet-context branch (Unknown slug).** In a fleet-launched run — one whose invocation carried
   the literal `fleet-context: <agent>` marker (see **Execution context**) — do NOT call
   `AskUserQuestion`. Raise a registry `## Questions` row (question: "dependency slug
   `<slug>` on epic `<epic-slug>` matches no refine / solution / status file — allow it as a future
   epic, or correct it?") and proceed on `default: Continue (future epic)` — the reversible option:
   a wrong allow is fixed by editing `depends_on`, a wrong reject silently loses the dep. Urgency
   `advisory`, with the required `assumption:` = "allowing `<slug>` as a not-yet-created epic;
   correctable in the plan's frontmatter before any wave runs". The "Correct" path's re-prompt (a
   second `AskUserQuestion` with a text field) is unreachable in a fleet-launched run — never
   re-prompt; dev-manager's answer text carries the corrected slug, which you re-run through this
   step's validation before flipping the row `applied`. Standalone interactive behavior is
   unchanged.

6. Write `slug` and `depends_on` into the plan frontmatter alongside the existing fields.

This step makes the plan discoverable by the disk epic-survey (`agentflow.epic_survey`, which globs `<data_root>/projects/*/design/plans/*.md`) the moment it's authored.

### Step 1.6: Author the Use-Case doc of record (`## Use Cases`)

`solution` is Hop 2 of the `epic → use-case → flow-page → code` spine, and it holds the **single
identity** of every use case the epic delivers. `refine` already **minted** each opaque `UC-NNNN`
id and wrote its Hop-1 block (functional story + domain) into the refine design doc. **Solution never
mints** — it *threads* ids that already exist and authors the **technical** story against them. If a
UC you expected isn't in the refine doc, stop and send it back to refine to be minted; do not invent
an id here.

Add a `## Use Cases` section to the produced solution plan (the doc under
`<data_root>/projects/<name>/design/plans/<slug>.md`). It is the **doc of record**: for each UC the epic
implements, carry the functional summary forward from refine, author the new technical story, and
record domain, status, and the owning task(s). One block per UC:

```markdown
## Use Cases

### UC-0147 — <short title>

- **Functional summary:** <carried verbatim from the refine `### UC-0147` block — the "as a <user>
  I can <capability>, so that <value>" story; solution does not rewrite it>
- **Technical story:** <authored here — how this capability is built: the components, data flow,
  and interfaces that realize it. This is solution's contribution; it exists nowhere upstream.>
- **Domain:** <carried from the refine block, e.g. `auth/login`>
- **Status:** backlog
- **Owning tasks:** [3, 5]   <!-- the `## Task N` numbers whose frontmatter carries this UC -->
```

Rules for the block:

- **Single identity.** This block is the one canonical description of the UC's *implementation*. The
  functional summary is copied (never diverged) from refine; the technical story is written once,
  here. Downstream (commits, flow pages) point back at this identity by opaque id, never re-describe.
- **`Status:` pre-ship is derived, not hand-maintained.** The plan *hosts* the field; its value is
  computed from task-done state: `backlog` while none of the UC's owning
  tasks are done, `in-progress` once some-but-not-all are done. Seed it `backlog` at authoring time —
  a derived read can't rot. `completed`/`deprecated` are **post-ship** states owned by
  autodoc-update reconciling against code; never set them here.
- **`Owning tasks:`** lists the `## Task N` numbers whose frontmatter will carry this UC (threaded in
  Step 3). A UC with no owning task is a red flag — either a task is missing or the UC isn't in this
  epic's scope; surface it rather than shipping an orphan.
- **Opaque ids only.** `UC-NNNN` digits carry no domain meaning. Re-parenting a domain later edits
  the `Domain:` string only; the id and every reference to it are untouched.

### Step 2: Analyze the plan to derive the DAG

After writing-plans completes:

1. Read the produced plan file
2. For each `## Task N:` heading, identify:
   - The task number (N)
   - The phase it belongs to (group tasks into 3-6 phases by major component or sequence)
   - Its dependencies (which earlier tasks must complete first — derive from task body's references and from logical sequencing)
   - Optional complexity (default `medium`; mark `low` for trivial mechanical tasks, `high` for tasks requiring design judgment)
   - Optional effort-mode knobs (both default absent = single-shot):
     - `best_of_n: N` — emit for tasks that are genuinely hard or design-ambiguous (N=2 or 3). The orchestrator runs N candidate implementations, test-pre-filters them, and a 3-judge panel picks the winner. Reserve for tasks whose spec marks them high-risk or design-heavy; do NOT apply by default.
     - `adversarial: true` — emit for security-critical or correctness-critical tasks. The orchestrator runs an adversarial refuter panel after implementation. Reserve for tasks explicitly marked as security or invariant-critical; do NOT apply by default.
     - **Default rule:** omit both knobs from the task entry; single-shot is the default. Add `best_of_n`/`adversarial` only when the task spec explicitly flags high-risk, design-heavy, or security-critical work.
3. Identify the test commands by reading the project's test infrastructure (check `pyproject.toml`, `package.json`, README)

### Step 2.5: Derive verification block per task

For each task in the plan, derive a `verification` block that the in-wave verifier subagent will evaluate against the implementer's diff. This block is the per-task contract — get it right and the verifier catches drift before it ships.

Per Posture dial 1, these blocks must be **complete**, not indicative: `acceptance_criteria` covers
every check the task must satisfy (no "etc."), and `file_allowlist` names every file the task may
touch (new files marked) with `regression_guard` naming every file/service it must not. An
incomplete allowlist blocks a legitimate edit or lets drift through; an incomplete criteria list
lets a task pass while under-built.

Read each task's body (acceptance criteria list, `## Files:` section, constraints, "do not touch" notes) and populate:

- **`acceptance_criteria`** — the discrete checks the verifier evaluates. Lift directly from the task body's listed criteria. One bullet per check. Concrete, testable, no judgment calls.
- **`file_allowlist`** — files the wave is permitted to modify. Lift from the task body's `## Files:` section. Mark new files explicitly. Tests for the task code count as in-allowlist.
- **`regression_guard`** — files/services the wave MUST NOT touch. Source: spec's "do not touch" constraints + invariants + adjacent systems the task brushes against. Explicit > implicit. Service-config files (systemd units, docker-compose lockfiles), shared libs not in scope, neighbor modules — list them.
- **`spec_format`** — what format the task body declares. Defaults: detect from the spec doc. Examples: `"sectioned spec (Frontmatter + Story + Contract + Boundary)"`, `"user story (As a / I want / So that)"`, `"acceptance-criteria checklist"`.
- **`failure_modes`** — task-specific known failure modes from the spec. Examples: security tasks → `"an API key leaked into a log line"`; auth tasks → `"signing key logged in error path"`; migration tasks → `"backfill default applied to existing rows under concurrent writes"`. The plan-level `verification.global_failure_modes` covers cross-cutting modes — don't duplicate them here.
- **`test_commands`** — task-specific test commands. Default: the plan-level fast test command plus the test file the task creates (e.g., `pytest path/to/test_<task>.py -v`).

If a task body doesn't have enough information to populate a non-empty `verification` block (typical: scaffolding tasks with no body content yet), emit a WARN to the user and write `verification: null` for that task. The orchestrator will fall back to the existing implementer + spec-reviewer + code-quality-reviewer flow for that task with a WARN entry to the decision log.

Plan-level globals (`verification.global_failure_modes`, `escalation_threshold_pct`, `max_fix_iterations`) are seeded from the template defaults. Defaults are: `escalation_threshold_pct: 15`, `max_fix_iterations: 4`. Don't tighten these in the planner — first-epic baseline tuning happens after rollout.

### Step 3: Inject frontmatter

Open the plan file. If it already has YAML frontmatter, abort and report — caller should use the plan as-is.

Otherwise, prepend the YAML frontmatter block (using the template at `<suite_root>/skills/orchestrator/templates/plan-frontmatter.yaml`) populated with the values from Step 2 and Step 2.5.

The frontmatter goes ABOVE the existing `# <Title>` heading.

Inject:
- Standard frontmatter (epic, spec, phases, tasks with deps + complexity, test_commands, extra_context_files) — from Step 2.
- Per-task `verification` block under each task — from Step 2.5. Tasks without enough info: omit the field (parser treats it as `None`).
- **Per-task `use_cases` list (Phase 4 traceability, additive).** For each task that implements one or
  more use cases, thread the owning UC-ids from the Step 1.6 doc of record into the task's frontmatter
  as a **flat scalar list of opaque ids**:

  ```yaml
  use_cases: ["UC-0147", "UC-0152"]
  ```

  This is Hop 2's machine-readable half — the plan text hosts the identity, the frontmatter makes the
  task→UC edges greppable and lets the orchestrator inject a task's UC-ids into its wave brief (Hop 3).
  Mirror the Step 1.6 `Owning tasks:` mapping exactly: task N appears in a UC's `Owning tasks:` iff
  that UC-id appears in task N's `use_cases`. Rules:
  - **Additive-only / optional.** The plan output schema stays frozen — `use_cases` is an *optional*
    field. Tasks that implement no use case (scaffolding, infra chores, refactors) omit it entirely;
    the parser treats absence as no linked UCs. Never emit an empty `use_cases: []` where the field
    would otherwise be absent, and never let this field's presence change any existing frontmatter
    key. Golden scenarios with no UCs must parse byte-for-structure as before.
  - **Flat opaque scalars, not links.** Just the `UC-NNNN` strings — never wikilinks, never relational
    objects. This keeps them inert to the autodoc graph-check and to any relational validation.
  - **Thread, never mint.** Only ids that already exist in the Step 1.6 doc of record (hence in the
    refine doc) may appear. If a task needs a UC that was never minted, stop — do not fabricate an id.
- Plan-level `verification` globals at the same top level as `test_commands` — seeded from template defaults.
- **`worktree:` field (optional).** Plans that will run inside a dedicated git worktree (the default for new epics) should include the path under the
  configured `worktree_root`, one directory per project:

  ```yaml
  worktree: '<worktree_root>/<project>/<epic-slug>'
  ```

  `worktree_root` comes from `agentflow.config.load_environment()`; do not hard-code a home-relative
  path. **A flat `~/CODE/<repo>-<epic-slug>` form is wrong and must not be emitted** — nothing
  creates a tree at that path, and the field is authoritative rather than advisory (below), so a stale example here becomes a stale path the orchestrator obeys.

  When present, **this field IS the target tree** — the orchestrator's Step 1.1 takes it as
  authoritative even where it disagrees with the computed layout, then pre-flights it for existence
  and identity (`rev-parse --show-toplevel`, and `remote get-url origin` against the canonical repo).
  It is not a cwd comparison. When absent, Step 1.1 falls back to the computed
  `<worktree_root>/<project>/<epic-slug>`; if neither resolves, it escalates and exits rather than
  defaulting to the working directory.

  `/project` creates the worktree before invoking the orchestrator, with the one command and
  placeholder definitions in `/project` Step 5 — this skill carries no copy of it (for a spec whose
  `project:` is not the block's `[project]`, see `/project` Step 0.5, item 1 "Confirm the canonical
  repo"). The existing-path rule is Step 5's too: an existing path fails unless it is a resumed
  epic's own tree, which is reused.

- **`per_wave_worktrees: true`.** Plans authored by `solution` opt in by default. Adds the line:

  ```yaml
  per_wave_worktrees: true
  ```

  Set this on EVERY new plan emitted by `solution`. The orchestrator's Step 7 dispatch reads this and switches to per-wave worktree mode. Legacy plans without this field continue to run on the shared worktree.

### Step 4: Validate

Run:

```bash
python -c "from agentflow.plan_parser import parse_plan; from pathlib import Path; print(parse_plan(Path('<plan-file>')))"
```

Expected: prints the parsed `PlanFrontmatter` without errors.

If parsing fails: fix the frontmatter inline. Common errors:
- Phase listed in `tasks[].phase` but not in `phases:` list → add to phases list
- Dep references nonexistent task → check task numbers
- Cycle in deps → review and break the cycle

### Step 5: Report

**Mirror to wiki (best-effort, feature-detected):** This is one of three mirror-write touchpoints across the skill suite (backlog and project pass a spec, solution passes a plan); see `<vault_root>/CLAUDE.md` "Mirror System" for the vault layout, the `project:` routing rules, and the full touchpoint list.

After Step 4 (Validate) succeeds, before returning the summary, with `$PLAN_PATH` set to the validated plan file's absolute path:

```bash
MIRROR_SCRIPT="<vault.mirror_helper>"
if [[ -x "$MIRROR_SCRIPT" ]]; then
  # All three come from THIS wake's resolved block. The helper falls back to its own
  # literals for every one of them, so omitting any is not a no-op: the vault path decides
  # where documents land, the project list decides which projects route by name rather than
  # to _unsorted/, and the lock dir keeps the lock out of a synced folder where two machines
  # can both believe they hold it.
  mirror_out="$(WIKI_VAULT_PATH="<vault_root>" AGENTFLOW_PROJECTS="<vault_projects>" \
    AGENTFLOW_LOCK_DIR="<lock_dir>" bash "$MIRROR_SCRIPT" "$PLAN_PATH" plan 2>&1)" && \
    echo "MIRROR: $mirror_out" || echo "WARN: mirror-epic.sh failed (non-fatal): $mirror_out"
fi
```

- If `<vault.mirror_helper>` exists and is executable: invoke it with `$PLAN_PATH` and kind `plan`, passing `WIKI_VAULT_PATH=<vault_root>`, `AGENTFLOW_PROJECTS=<vault_projects>` and `AGENTFLOW_LOCK_DIR=<lock_dir>` from this wake's resolved block. Capture its stdout/stderr.
- On success: extract the mirror path from the `OK  mirrored: ... → <wiki-path>` line and include it in the summary.
- On failure: surface a `WARN: mirror-epic.sh failed (non-fatal): <error>` line in the summary. Do NOT abort solution.
- If the script does not exist, or the resolved block says `vault_root = (no vault ...)`: skip silently. No warning needed — vault is simply not installed, and "no" is a first-class answer.

Output a one-screen summary back to the caller:

- Plan file path
- Wiki mirror path (if mirror ran successfully — e.g. `wiki/epics/<project>/<slug>/plan.md`)
- Total task count
- Phase breakdown
- Any cross-phase deps (where a task in phase X depends on a task in phase X-1 — these enable opportunistic parallelism)
- Estimated wall-time (bands: 5–15 min/task sonnet, 10–25 min/task opus TDD — never a flat ×30
  min/task formula, which overshoots several-fold; quote a band, not a point)

## Constraints

- Task-body detail is authored in **Step 1** (via writing-plans, iterating until each body is a
  self-sufficient contract per Posture dial 1). Once you reach **Step 3**, injection is
  **frontmatter-only** — do NOT rewrite task descriptions while injecting the DAG frontmatter. The
  two phases are distinct: enrich bodies in Step 1, inject frontmatter in Step 3.
- Keep the plan **output schema frozen** — valid YAML frontmatter, integer task keys, `phases`,
  per-task `deps`, `per_wave_worktrees: true`, `test_commands`, plus the per-task `verification`
  block. The detail/gate dials never change these fields; the parser and acceptance harness depend
  on them. The per-task `use_cases` list (Step 3) is the one sanctioned extension: strictly
  **additive and optional** — its absence is the default and leaves the frozen shape untouched, so
  golden scenarios with no use cases parse exactly as before.
- Do NOT skip the parse validation in Step 4 — if the orchestrator can't parse it, the epic fails on first wake
- Do NOT invent dependencies — when in doubt, declare the conservative dep (task N depends on task N-1) rather than missing one
- Never fire `AskUserQuestion` in a fleet-launched run (`fleet-context: <agent>` in the invocation). Every gate here has a branch and an already-computed `default:` — the Dependencies gate's is `<pre_detected_list>`, never a dependency list invented at the gate

## Failure modes

| Failure | Action |
|---|---|
| User asks a dependency question (Step 1.5) | Dispatch via button options (primary: "None" / "Use pre-detected" / "Specify manually"), with free-text 'Other' fallback for manual entry. In a fleet-launched run, raise an advisory registry `## Questions` row and proceed on `<pre_detected_list>` (see Step 1.5's `fleet-context` branch). |
| Unknown slug validation fails (Step 1.5) | Dispatch via button options ("Continue (future epic)" / "Correct"), with free-text 'Other' as fallback for slug correction. In a fleet-launched run, raise an advisory registry `## Questions` row and proceed on "Continue (future epic)" (see Step 1.5's `fleet-context` branch). |
| Plan body has insufficient info for verification block (Step 2.5) | Emit WARN, write `verification: null` for that task. Orchestrator falls back to the existing multi-reviewer flow with a decision-log entry. |
| Frontmatter parsing fails at validation (Step 4) | Surface parse error, do not auto-fix. Caller should revise spec or frontmatter and re-invoke. |
| Parse succeeds but task references nonexistent task in deps | Fix the dep (off by one, typo, etc.) and re-run validation. |
