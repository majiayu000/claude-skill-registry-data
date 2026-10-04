---
name: project
description: Workflow-aware meta-command for the epic-launch pipeline (brainstorm → plan → orchestrator). Detects what was handed in and resumes from the right point. Use when invoked as `/project [arg]` or when the user says "spin up an epic for X", "kick off a project on Y", "let's project this", "take this from spec to epic", "scaffold a new epic on X", "run /project on this plan/spec", or otherwise asks to push a topic / spec / plan into autonomous execution. Routes by input — empty/topic → fresh full pipeline; spec path → skip brainstorm, start at plan; plan path → skip to dispatch; status path → resume / show board. NOT for one-off bug fixes or interactive (non-orchestrator) plan execution.
---

# Project — workflow-aware meta-command

`/project` is the single command that puts work into the epic-launch pipeline at whatever point matches the input. It does not re-implement any of the underlying behavior — every step delegates to an existing skill:

- `../refine/SKILL.md` — interactive design conversation that produces `<data_root>/projects/<name>/design/specs/YYYY-MM-DD-<slug>-design.md`
- `solution` — wraps `../_vendored/writing-plans/SKILL.md` and adds DAG/verification YAML frontmatter, output under `<data_root>/projects/<name>/design/plans/`
- `orchestrator` — autonomous wave executor paced by `ScheduleWakeup`, with status board persistence

**Announce at start:** "I'm using the project skill — detecting input mode, then resuming the pipeline from there."

## Input modes

| Input | Mode | Entry step | Skipped steps |
|---|---|---|---|
| _no arg_ | `fresh` | Prompt for topic, then Step 1 | — |
| topic string (no `/`, no `.md`) | `fresh` | Step 1 | — |
| `…/design/specs/*-design.md` or any file with spec frontmatter | `from-refine` | Step 1 | Step 2 (brainstorm) |
| `…/design/plans/*.md` with plan frontmatter (`phases:` + `tasks:`) | `from-solution` | Step 4 (gate #1) | Steps 1–3 |
| `…/*.status.md` or status-frontmatter file | `from-status` | Step 6 (resume / show board) | Steps 1–5 |
| ambiguous | — | ask user once, then route | — |

Plan files for `from-solution` MUST have orchestrator-shape frontmatter (top-level `epic:`, `spec:`, `phases:`, `tasks:`). A plain markdown plan without that frontmatter routes to `from-refine` instead so `solution` can wrap it properly.

## Approval gates (unchanged)

The two-gate contract is the same regardless of input mode:

| Gate | Whose | When | Question |
|---|---|---|---|
| **#1** | This skill (Step 4) | After plan exists (either freshly produced OR loaded from disk) | "Dispatch to the orchestrator? (y/N/edit)" |
| **#2** | `orchestrator` (its own Step 5) | During orchestrator bootstrap, before first wake schedules | "Approve plan scope?" |

Both must say yes. Either says no → stop. Do not collapse them. **In `from-solution` mode, gate #1 still fires** — handing in an existing plan does not waive <person.name>'s right to walk away before autonomous execution starts.

In a **fleet-launched** run both gates still exist — they route through registry `## Questions` rows instead of buttons. See **Execution context** below.

## Execution context (who is the human surface for this run?)

`/project` runs in one of two contexts, and every `AskUserQuestion` gate below branches on which
one it is:

- **Standalone interactive** — a human at the keyboard typed `/project`. The human IS the surface:
  every gate behaves exactly as written, and **nothing below changes that path.**
- **Fleet-launched** — a fleet loop (`lead-dev`, `jr-dev-1`, `jr-dev-2`) dispatched this run. Per
  `<suite_root>/docs/REGISTRY.md`, no loop but dev-manager asks the human, so **a fleet-launched run never calls
  `AskUserQuestion`**. Every site that would have asked instead writes a registry `## Questions` row
  (answered by dev-manager) and either proceeds on a stated `default:` or parks and polls for it.

**The mechanism — an explicit marker, never inference.** The launching loop MUST include the
literal line `fleet-context: <agent>` (e.g. `fleet-context: lead-dev`) in the invocation prompt or
arguments. No marker = standalone interactive. Never infer fleet mode from anything else (cwd, the
epic's `current_state`, time of day).

**The canonical description of this contract is `../orchestrator/SKILL.md`, "Fleet invocation
context"** — the marker rule, recording `fleet_context: <agent>` into `status.md` so later
self-scheduled wakes inherit the mode, and the "how a fleet-context question works" procedure
(raise the row through the registry CLI as `<FLEET_CONTEXT>`, never by hand-editing the
registry, with a mandatory `--default` and an urgency per the REGISTRY
classification rule; record the Q-id in the site's `*_prompted` decision marker; poll lock-free;
map the answer through the SAME canonical-reply mapping the buttons use; flip `answered -> applied`
as the raiser). Read it there and follow it verbatim — it is deliberately NOT restated here, since
three copies of one contract is how three copies drift.

**Propagate the marker — this half is load-bearing.** `/project` is a pass-through, so a marker it
swallows is a marker the next hop never sees:

- **Step 3** — pass `fleet-context: <agent>` into the `solution` invocation. `solution` has no
  `status.md` to inherit the mode from, and its Dependencies gate fires on *every* plan it authors.
- **Step 5** — include the literal `fleet-context: <agent>` line in the `/orchestrator` dispatch
  prompt, so the orchestrator records it at bootstrap and gate #2 plus every later wake inherit it.

Drop either propagation and an unattended `AskUserQuestion` still fires downstream, even though
`/project`'s own gates are branched.

## Procedure

### Step 0: Detect mode

Parse the arg the user passed (or its absence). Run this command to classify:

```bash
python - "$ARG" <<'PYEOF'
import sys, os, re, pathlib
arg = (sys.argv[1] if len(sys.argv) > 1 else "").strip()
if not arg:
    print("MODE=fresh"); sys.exit(0)

# Path-shaped?
p = pathlib.Path(os.path.expanduser(arg))
is_path = ("/" in arg or "\\" in arg or arg.endswith(".md")) and p.exists()
if not is_path:
    print("MODE=fresh"); print(f"TOPIC={arg}"); sys.exit(0)

name = p.name
text = p.read_text(encoding="utf-8", errors="replace")
m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
fm = m.group(1) if m else ""

if name.endswith(".status.md") or "paused:" in fm:
    print("MODE=from-status"); print(f"PATH={p}"); sys.exit(0)

# Plan frontmatter check: orchestrator-shape requires phases: AND tasks:
if "phases:" in fm and "tasks:" in fm and "epic:" in fm:
    print("MODE=from-solution"); print(f"PATH={p}"); sys.exit(0)

# Spec heuristics: under design/specs/, -design.md suffix, or spec frontmatter shape
in_refine = "/design/specs/" in str(p).replace("\\", "/")
spec_shape = "slug:" in fm and "title:" in fm and "phases:" not in fm
if in_refine or name.endswith("-design.md") or spec_shape:
    print("MODE=from-refine"); print(f"PATH={p}"); sys.exit(0)

print("MODE=ambiguous"); print(f"PATH={p}")
PYEOF
```

**Bind the context once, here — before any branch reads it.** Set `FLEET_CONTEXT` to the agent named by the invocation's `fleet-context: <agent>` marker, or to `none` when there is no marker. Every fleet branch below and both propagation hops in Steps 3 and 5 read that one variable, so "is this a fleet run" is decided once rather than re-derived per site. This binding must precede the mode branch immediately below, whose `ambiguous` arm already uses it.

Branch on the printed `MODE`:

- **`fresh`** → if `TOPIC=` line present, use it; else prompt: *"What topic? (one sentence is fine)"*. Then **Step 1**.
- **`from-refine`** → record `REFINE_PATH`, jump to **Step 1** (init check still runs because spec authoring may have predated `CLAUDE.md`), then **Step 3**.
- **`from-solution`** → record `SOLUTION_PATH`, **skip Steps 1–3**, jump to **Step 4** (gate #1). Run init check inline as a one-line warning only — the plan already exists, the horse has bolted on `CLAUDE.md`-grounded planning.
- **`from-status`** → **skip Steps 1–5**, jump to **Step 6** (resume mode).
- **`ambiguous`** → **fleet-launched? take the fleet-context branch below INSTEAD of this call.**
  Standalone: Call `AskUserQuestion(header="Routing", options=[{label: "Spec", description: "File is a design spec (e.g., from brainstorming); send to planning step"}, {label: "Plan", description: "File is a plan with phases and tasks; skip planning and go to approval gate"}, {label: "Topic", description: "File is something else; treat its name as the topic for a fresh epic"}])`. The response's label maps: Spec→from-refine, Plan→from-solution, Topic→fresh-with-topic-from-filename. (Free-text 'Other' option is auto-generated by AskUserQuestion; treat any other response as a topic for `fresh` mode.)

  **Fleet-context branch (Routing).** In a fleet-launched run — one whose invocation carried the
  literal `fleet-context: <agent>` marker (see **Execution context**) — do NOT call
  `AskUserQuestion`. Raise a registry `## Questions` row instead (question: "`/project` could
  not classify `<PATH>` — spec, plan, or topic?"; `--actor <FLEET_CONTEXT>` — the CLI derives `raised_by` from the actor, so name the invoking skill in the question TEXT rather than hand-writing a composite `raised_by`) with
  `default:` = **abort this dispatch and re-file the epic** (NOT the standalone fallthrough
  `Topic` → `fresh`, which would open an interactive brainstorm nobody is watching — the same
  reason this branch parks) and urgency `waiting`, then **park**: a fleet loop hands in a real spec
  or plan path, so `ambiguous` means its frontmatter is malformed, and the safe default is to stop
  rather than to guess a mode. On `answered`, map the answer text through the same label mapping as the buttons, take
  that branch, and flip the row `applied`. Standalone interactive behavior is unchanged.

**What "park" means here.** `/project` and `solution` are ONE-SHOT skills — they have no wake
schedule of their own, so they cannot sit and poll for an answer. To park is to **stop this
invocation** after writing the Question row, and report to the caller which row it is waiting on.
The dispatching loop owns the waiting: it parks its own Queue row (`release ... --state parked
--waiting-on Q-NNNN`), and re-invokes `/project` on a later wake once the row is `answered`.
Never poll in-process — that converts a button-wedge into a poll-wedge, which is the same wedge
with a longer name.

### Step 0.5: Grounding preflight (MANDATORY — all modes except `from-status`)

Runs immediately after mode detection, before any planning or dispatch. Not skippable — including
for `current_state: approved-for-autonomous` epics (gateless skips approval gates, never grounding).

1. **Confirm the canonical repo.** Resolve the target repo from the spec/plan/topic's `project:`
   field (or conversation context) and verify that checkout's `origin` points at the
   canonical remote (`git -C <canonical_repo.local_checkout> remote get-url origin`) —
   `<canonical_repo.host_ref>`, NEVER the deprecated `<deprecated_mirror>` mirror. The `-C` is not
   decoration: a bare `git` here resolves against the working directory, which in a fleet-launched
   run is the launch directory and is not a repo, so the check fails in the direction that looks
   like a broken machine rather than a wrong repo. If the
   checkout points elsewhere, stop and surface before planning a single task.
   **When the spec's `project:` differs from the block's `[project]`**, run
   `python -m agentflow.config show --project <name>` and take every placeholder in this skill
   from that output, not from the session block (which is resolved for the session default).

2. **Probe premises against current code** (`from-refine` / `from-solution` modes; `fresh` has no spec
   yet — the brainstorm does this live). Verify the spec/plan's load-bearing claims against the
   code as it exists now: named files/endpoints/components exist, the feature isn't already built,
   the "current behavior" it assumes is still current. Specs go stale in BOTH directions —
   placeholders hide unbuilt work, stale premises hide already-built work.
   Spot-check with Grep/Read — minutes of probing beats a wrong plan.

**On failure: stop.** Surface exactly which premise failed and what the code actually shows. Do not
plan or dispatch around a broken premise — the fix is a spec update, then re-invoke
`/project <spec-path>`.

### Step 1: Init check

Run only in `fresh` and `from-refine` modes. (In `from-solution` mode, just emit a single-line warning if `CLAUDE.md` is missing — do not gate.)

```bash
test -f "<canonical_repo.local_checkout>/CLAUDE.md" && echo present || echo MISSING
```

Name the checkout, never test a bare `CLAUDE.md`: the question is whether the **target** repo is
grounded, and a fleet-launched run's working directory is the launch directory, so a bare test
answers about the harness home instead — reporting `present` for a checkout that has no `CLAUDE.md`
at all.

- **Present** → proceed silently.
- **MISSING** (fresh / from-refine only) → **fleet-launched? take the fleet-context branch below
  INSTEAD of this call.** Standalone: Call `AskUserQuestion(header="Init check", options=[{label: "Run /init first (Recommended)", description: "Stop and run /init to ground the plan in this codebase"}, {label: "Continue anyway", description: "Proceed without CLAUDE.md; expect more spec drift"}])`. 
  
  Default is **Run /init first** (Recommended, safe option). On that selection or empty: stop. On "Continue anyway": continue and record `claude_md_missing` for the Step 6 hand-off.

  **Fleet-context branch (Init check).** In a fleet-launched run — one whose invocation carried the
  literal `fleet-context: <agent>` marker (see **Execution context**) — do NOT call
  `AskUserQuestion`. Raise a registry `## Questions` row (question: "`CLAUDE.md` is missing in
  the target checkout — run `/init` first, or plan `<epic-slug>` ungrounded?") with
  `default: Run /init first (Recommended)` — this site's existing Recommended option, unchanged —
  and urgency `waiting`, then **park**: that default *is* "stop", so there is nothing to proceed on,
  and planning an epic ungrounded burns a whole wave. On `answered`, map "continue"-class answers to
  the "Continue anyway" branch (record `claude_md_missing`) and "init"-class answers to the stop
  branch, then flip the row `applied`. Standalone interactive behavior is unchanged.

(`solution` Step 0 also checks for `CLAUDE.md`. The double-check is intentional in `fresh` mode — catches it before sinking time into a brainstorm.)

### Step 2: Brainstorm phase

**Run only in `fresh` mode.** Skipped in `from-refine`, `from-solution`, `from-status`.

Invoke `../refine/SKILL.md` with `<topic>` as the kickoff prompt. This is a **live, interactive design conversation** — sit through it. Do not autonomously answer the brainstorming skill's clarifying questions on the user's behalf. Do not race ahead.

**Fleet-context branch (Brainstorm).** A `fleet-context` run must never reach this step: an
interactive design conversation has no human in it, and answering the refine skill's questions on
the absent human's behalf is exactly the failure this branch exists to prevent. This step is reachable
only in `fresh` mode, and a fleet loop dispatches an already-approved spec (`from-refine`), so
arriving here in a fleet run means the dispatch was malformed. Raise a registry `## Questions` row
(question: "`/project` reached the interactive brainstorm in a fleet run — the dispatch handed a
topic, not an approved spec"; `default:` = abort the dispatch and re-file the epic through
`dev-manager`; urgency `waiting`), **park, and do NOT invoke the refine skill.** Standalone
interactive behavior is unchanged. (This site calls no `AskUserQuestion` of its own, so no static
gate can see it — the guard in `<suite_root>/skills/_shared/tests/test_human_surface_gates.py` checks for the
marker literal, which is why the branch says `fleet-context` here explicitly.)

Wait until brainstorming has:
1. Produced a spec doc at `<data_root>/projects/<name>/design/specs/YYYY-MM-DD-<slug>-design.md`
2. Completed its Step 7 spec self-review
3. The user has reviewed the spec (brainstorming Step 8)

**Critical handoff seam:** brainstorming's Step 9 will normally invoke `../_vendored/writing-plans/SKILL.md` directly. **You are intercepting that transition.** When brainstorming reaches Step 9, take over instead of letting it chain into raw `writing-plans` — proceed to Step 3, which invokes `solution` instead. The plan must end up with DAG frontmatter for the orchestrator to consume it.

Capture the spec path (`REFINE_PATH`). Pass it to `solution` in Step 3.

**Wiki mirror hand-off (feature-detected):** This is one of three mirror-write touchpoints across the skill suite (backlog and project pass a spec, solution passes a plan); see `<vault_root>/CLAUDE.md` "Mirror System" for the vault layout, the `project:` routing rules, and the full touchpoint list.

> **No DragonScale address for mirror pages.** Epic mirror pages (`wiki/epics/<project>/<slug>/{spec,plan}.md`) are high-churn dashboard artifacts using the `mirror_of`/`kind` schema, NOT durable knowledge pages. Do **not** call `./scripts/allocate-address.sh` for them — they are intentionally address-exempt and orphan-exempt (`wiki-lint` excludes `type: epic` / `wiki/epics/`). Address allocation applies only to durable pages created by `/save` and `wiki-ingest`.

After capturing `REFINE_PATH` and BEFORE proceeding to Step 3, check whether the mirror helper is available:

```bash
test -x "<vault.mirror_helper>" && echo MIRROR_AVAILABLE || echo MIRROR_SKIP
```

If `MIRROR_AVAILABLE`:

1. **Check for `project:` field** in `REFINE_PATH`'s frontmatter:

   ```bash
   python - "$REFINE_PATH" <<'PYEOF'
import sys, re, pathlib
text = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
fm = m.group(1) if m else ""
has_project = bool(re.search(r"^project:\s*\S", fm, re.MULTILINE))
print("HAVE_PROJECT" if has_project else "NEED_PROJECT")
PYEOF
   ```

   If `NEED_PROJECT`: ask the user *once* — "Spec has no `project:` field — which project is this for? (one of your installed `~/.agentflow/config/projects/*.md` names, or `personal` / `other`)". **Fleet-context branch:** in a `fleet-context` run there is no user to ask — this is a free-form ask, not an `AskUserQuestion`, so no static gate catches it. Take `FLEET_CONTEXT`'s own project (the dispatching loop is configured for exactly one) as the `default:`, raise an `advisory` registry `## Questions` row recording the assumption (the CLI refuses an advisory row without `--assumption`), and PROCEED on it — writing a `project:` field is reversible, and stalling a dispatch on a missing metadata line is not worth a park. On reply, prepend `project: <value>` to the spec's YAML frontmatter (insert after the opening `---` line, before the closing `---`). If the user skips or says "skip", proceed without adding the field (mirror will route to `_unsorted/`).

2. **Invoke the mirror** (best-effort):

   ```bash
   # All three come from THIS wake's resolved block. The helper falls back to its own
   # literals for every one of them, so omitting any is not a no-op: the vault path decides
   # where documents land, the project list decides which projects route by name rather
   # than to _unsorted/, and the lock dir keeps the lock out of a synced folder where two
   # machines can both believe they hold it.
   WIKI_VAULT_PATH="<vault_root>" AGENTFLOW_PROJECTS="<vault_projects>" \
     AGENTFLOW_LOCK_DIR="<lock_dir>" bash "<vault.mirror_helper>" "$REFINE_PATH" spec
   ```

   Capture stdout/stderr. If the exit code is non-zero or output contains `ERROR:`, surface a one-line warning: `⚠ Wiki mirror failed: <first error line>` — then continue to Step 3. A mirror failure is never fatal.

   On success (`OK  mirrored: …`), record `WIKI_MIRROR_PATH` from the output (the path after `→ `) for use in Step 4.

If `MIRROR_SKIP`: proceed silently. No warning, no behavior change.

### Step 3: Plan phase

**Run in `fresh` mode (after Step 2) AND `from-refine` mode (entry step from Step 0).** Skipped in `from-solution`, `from-status`.

Invoke `solution` with `REFINE_PATH`. `solution` itself wraps `../_vendored/writing-plans/SKILL.md` and adds:
- YAML frontmatter declaring phases + the task DAG
- Per-task `verification` blocks (acceptance criteria, file allowlist, regression guard)
- Plan-level globals (test commands, escalation thresholds)

**Propagate the execution context.** In a fleet-launched run, include the literal line
`fleet-context: <agent>` in the invocation you hand `solution` (see **Execution context**).
`solution` has no `status.md` to inherit the mode from — the caller's marker is its only signal —
and its Dependencies gate fires on every plan it authors, so dropping the marker here fires
`AskUserQuestion` into an unattended session even though every gate in this skill is branched.

Wait for `solution` to complete. Its Step 5 emits a one-screen summary (epic name, total task count, phase breakdown, est. wall-time, plan path). Capture that summary verbatim — reuse it in Step 4. Capture the produced plan path as `SOLUTION_PATH`.

If `solution` aborts (e.g., parse validation fails, dep cycle detected), surface the error and stop. Do not autonomously fix plan frontmatter — re-invoking `solution` after the user fixes the spec is the right move.

### Step 4: Approval gate #1 — "Dispatch to the orchestrator?"

**Runs in all modes except `from-status`.** In `from-solution` mode, this is the FIRST interactive gate the user hits — no brainstorm or plan-authoring happened, so make the summary punchy.

**Auto-skip for `approved-for-autonomous` epics (gateless autonomous path).** Before showing the summary, read `current_state` from the plan's frontmatter (fall back to the spec's frontmatter via the `spec:` field if the plan lacks it). If `current_state == approved-for-autonomous`, the epic has already been human-greenlit for gateless execution (the fleet autonomy envelope) — **skip the AskUserQuestion**, print one line (`Gate #1 auto-skipped: current_state=approved-for-autonomous`), still render the summary + file-path block for the record, and proceed directly to Step 5 as if `Dispatch` was chosen. This auto-skip fires ONLY for that exact state — every other state (drafted, planning, etc.) still gates normally. Do NOT auto-skip on any other signal (env var, arg, etc.); the frontmatter state is the only trigger.

**This auto-skip is a STATE coincidence, not the `fleet-context` contract.** It happens to cover the
common fleet case — fleet-dispatched epics are `approved-for-autonomous` by construction — but it
keys on frontmatter state, so it says nothing about an unattended run whose epic is in any other
state, and it does nothing at all for the gates in Steps 0, 1 and 6 or for `solution`'s own gates.
The `fleet-context` branch below is what actually guarantees no unattended `AskUserQuestion`.

Show the user a one-screen summary of `SOLUTION_PATH`:
- In `fresh` / `from-refine`: reuse the summary `solution` emitted at its Step 5.
- In all modes: **append the file-path block** after the summary (or at the top in `from-solution` mode):

  ```
  Canonical spec:  <data_root>/projects/<name>/design/specs/<slug>-design.md
  Wiki mirror:     <vault_root>/wiki/epics/<project>/<slug>/spec.md  ← (omit this line if WIKI_MIRROR_PATH was not set or mirror was skipped)
  Plan:            <SOLUTION_PATH>
  ```

  Only include the `Wiki mirror:` line when `WIKI_MIRROR_PATH` was recorded in Step 2 (i.e., the mirror ran and succeeded). If the mirror was skipped or failed, omit the line entirely — do not print a placeholder or "N/A".
- In `from-solution`: synthesize one yourself by parsing the frontmatter:

  ```bash
  python - "$SOLUTION_PATH" <<'PYEOF'
import sys, re, yaml, pathlib
p = pathlib.Path(sys.argv[1])
text = p.read_text(encoding="utf-8")
fm = re.match(r"^---\n(.*?)\n---", text, re.DOTALL).group(1)
d = yaml.safe_load(fm)
tasks = d.get("tasks", {}) or {}
phases = d.get("phases", []) or []
by_phase = {ph: 0 for ph in phases}
for t in tasks.values():
    by_phase[t.get("phase","?")] = by_phase.get(t.get("phase","?"), 0) + 1
print(f"Epic: {d.get('epic','?')}")
print(f"Plan: {p}")
print(f"Tasks: {len(tasks)} across {len(phases)} phases")
for ph in phases:
    print(f"  {ph}: {by_phase.get(ph,0)} task(s)")
PYEOF
  ```

Ask the user with structured options:

> **Note:** The "Edit plan" button requires a desktop environment — mobile cannot open `$EDITOR`. For mobile use, copy the plan path and edit on desktop, then resume with `/project <plan-path>`.

**Fleet-context branch (gate #1).** In a fleet-launched run — one whose invocation carried the
literal `fleet-context: <agent>` marker (see **Execution context**) — do NOT call
`AskUserQuestion`. Reaching this gate at all is an anomaly — the auto-skip above already covers the
normal fleet path, so a fleet-dispatched epic that lands here is NOT `approved-for-autonomous`, i.e.
un-promoted. Raise a registry `## Questions` row (question: "fleet-dispatched epic `<epic-slug>` is
`<current_state>`, not approved-for-autonomous — dispatch to the orchestrator anyway, or stop?";
`--actor <FLEET_CONTEXT>` — the CLI derives `raised_by` from the actor, so name the invoking skill in the question TEXT rather than hand-writing a composite `raised_by`) with `default: Cancel (an un-promoted epic should not run
unattended)` and urgency `waiting`, then **park** — dispatching starts autonomous execution and a
wake schedule, the irreversible half of this skill. On `answered`: `Dispatch`-class → Step 5;
`Cancel`-class → the `Cancel` branch below, verbatim; then flip the row `applied`. The `Edit plan`
option is unreachable in a fleet-launched run (it needs `$EDITOR` on a desktop) — never offer it.
Standalone interactive behavior is unchanged.

Call `AskUserQuestion(header="Dispatch", options=[{label: "Dispatch", description: "Hand to the orchestrator for autonomous execution"}, {label: "Cancel", description: "Plan stays on disk; resume later via /project <plan-path>"}, {label: "Edit plan", description: "Open plan in $EDITOR; re-prompt after editor closes"}])`.

The response's label maps to behavior:

- **`Dispatch`** — proceed to Step 5.
- **`Cancel`** — stop. Print: *"Plan saved at `<SOLUTION_PATH>`. Run `/orchestrator <SOLUTION_PATH>` (or `/project <SOLUTION_PATH>`) when ready."* Done.
- **`Edit plan`** — open the plan in the user's editor (`${EDITOR:-code} <SOLUTION_PATH>`). When the editor closes, re-validate by running:

  ```bash
  python -c "from agentflow.plan_parser import parse_plan; from pathlib import Path; print(parse_plan(Path('<plan-file>')))"
  ```

  If parse fails, surface the error and re-prompt. If parse succeeds, re-prompt. Do not assume `Edit plan` means `Dispatch`.
- **Free-text fallback** (typed 'y', 'N', 'edit'): Preserve backward compatibility. Map 'y' → Dispatch, 'N'/empty → Cancel, 'edit' → Edit plan path. Any other free-text input re-prompts with the structured options.

This is **the user's last chance to walk away with just a plan on disk.** Past Step 5 the orchestrator's bootstrap takes over and a wake schedule will be created.

### Step 5: Dispatch phase

**Runs in all modes except `from-status`.**

**Worktree isolation, by EXPLICIT path (MANDATORY).** The dispatched epic executes in a dedicated
git worktree — never the shared checkout — so it can't clobber (or be clobbered by) parallel
sessions' uncommitted work. Create it by naming both ends off the resolved block, never by
standing somewhere and typing `git`. **This is the one epic-worktree command**; solution and the
orchestrator's recovery point here rather than carrying their own:

```
git -C <canonical_repo.local_checkout> fetch
git -C <canonical_repo.local_checkout> worktree add <worktree_root>/<project>/<epic-slug> -b <epic-branch> --no-track origin/<base-branch>
```

- `<canonical_repo.local_checkout>` is the shared checkout, as the resolved block prints it.
- `<worktree_root>` is the resolved block's `worktree_root`; `<project>` is the spec's `project:`.
- `<epic-slug>` is the epic's slug, the same leaf the plan's `worktree:` field names.
- `<epic-branch>` is the epic's branch: the one name the orchestrator's Step 7 pushes
  (`push -u origin <epic-branch>`) and opens its PR from (`--head <epic-branch>`). In a fleet run
  it is the claimed row's `e<NNNN>-<short>` (the claim contract in `<suite_root>/docs/REGISTRY.md`);
  with no registry row, it is `<epic-slug>`.
- `<base-branch>` is the resolved block's `base-branch` line (`canonical_repo.base_branch`). The
  fetch comes first so `origin/<base-branch>` is current, and the branch starts there rather than
  at whatever HEAD the shared checkout happens to hold. `--no-track` keeps `<epic-branch>` from
  tracking `origin/<base-branch>`, so Step 7's `push -u origin <epic-branch>` sets its upstream.

**An existing path fails, unless it is a resumed epic's own tree** — then reuse it and run no
`worktree add`. When a resumed epic's directory was removed but `<epic-branch>` survives
(`git -C <canonical_repo.local_checkout> rev-parse --verify <epic-branch>` succeeds), run
`git -C <canonical_repo.local_checkout> worktree prune` and re-attach the branch without `-b`:
`git -C <canonical_repo.local_checkout> worktree add <worktree_root>/<project>/<epic-slug> <epic-branch>`.

**Why explicit, and why there is no worktree-entering tool here.** A fleet-launched run starts in
the machine's single launch directory, which is not a repository — so the harness's native
worktree-entering tool and the per-subagent worktree-isolation flag are both off-limits: each binds
to "whatever repo the working directory happens to sit in", and here that is none, which fails as a
confusing no-op rather than as an error.

Consequences: pass that path explicitly into the orchestrator invocation, every subagent prompt,
every test command and every review, and carry `-C` on every other git call (`git -C <worktree>`
for the epic's branch/add/commit/push, `git -C <canonical_repo.local_checkout>` for repo-level
work). Parallel file-MUTATING agents inside the epic each get their OWN worktree from the same
`worktree add` line with a distinct leaf and are TOLD its path; since `<epic-branch>` is already
checked out, each leaf takes its own branch (`-b <epic-branch>-<agent> <epic-branch>`) or
`--detach <epic-branch>` in place of `-b <epic-branch>`. Parallel waves sharing one git
index collide; read-only agents need none. At epic end
the orchestrator removes each one by path
(`git -C <canonical_repo.local_checkout> worktree remove <worktree_root>/<project>/<epic-slug>`,
then `worktree prune`) — left behind they accumulate under `<worktree_root>` and the next epic's
`worktree add` fails on a path that already exists.

**Propagate the execution context.** In a fleet-launched run, include the literal line
`fleet-context: <agent>` in the dispatch prompt (see **Execution context**). The orchestrator
records it as `fleet_context: <agent>` in `status.md` at bootstrap, so gate #2 and every later
self-scheduled wake inherit the mode; without it the orchestrator assumes a human at the keyboard
and fires gate #2 into an unattended session.

Invoke `/orchestrator <SOLUTION_PATH>` with the approved plan. The orchestrator runs its bootstrap:

1. Reads the plan — plan-shaped frontmatter, so bootstrap does not re-run `solution` on it
2. Computes the slug, decides `status.md` location
3. Initializes `status.md` from the template
4. Shows the user **its own one-screen summary** (epic name, task count, phases, wall-time, plan path)
5. Asks: **"Approve plan scope?"** ← **This is approval gate #2.**

The user must approve again here. This is **not** redundant with Step 4 — it's the orchestrator's own contract that nothing autonomous starts without an explicit go-ahead. Do not short-circuit it. Do not pre-answer it on the user's behalf. In a fleet-launched run gate #2 is not skipped either — the orchestrator's own `fleet-context` branch routes it (auto-skipped on `approved-for-autonomous`, otherwise a registry `## Questions` row), which is the orchestrator's call to make, not a pre-answer by this skill.

On user approval at gate #2, the orchestrator:
- Writes `status.md` (the board is that file; nothing else needs starting)
- Sends the initial ntfy
- Runs the first wake-cycle inline (no wait); schedules the next wake (3–4 min after this one completes)
- Begins the wake-cycle algorithm

If the user declines at gate #2, the orchestrator exits cleanly. The plan stays on disk; the user can re-invoke later via `/project <SOLUTION_PATH>`.

### Step 6: Hand-off message OR resume

**`fresh` / `from-refine` / `from-solution`:** After the orchestrator's bootstrap completes (gate #2 approved + first wake scheduled), print a terse status. Two short lines:

> Epic '<epic-name>' bootstrapped + first wave fired inline.
> Subsequent wakes run every ~3–4 min. Reply `paused: true` in `status.md` frontmatter to halt.

If the resolved config carries a non-null `status_board_url_template`, append a status-board line by substituting `{slug}` into it (`Status board: <rendered-url>`); when it's null — the default, no dashboard configured — omit the line entirely.

If `claude_md_missing` was recorded in Step 1, prepend a one-line caveat:

> ⚠ Plan was authored without `CLAUDE.md` — expect more spec drift than usual. Consider running `/init` and re-running this epic's first wave with extra scrutiny.

**`from-status`:** Read the status file. Print a one-screen resume summary:

```bash
python - "$STATUS_PATH" <<'PYEOF'
import sys, pathlib
from agentflow.status_writer import read_status
p = pathlib.Path(sys.argv[1])
s = read_status(p)
# status.md carries no slug field: the board is <slug>.status.md, so the stem is the slug
slug = p.name.removesuffix(".status.md")
done = sum(1 for t in s.tasks.values() if t.state == "done")
print(f"Epic: {s.epic} (slug: {slug})")
print(f"Status: {s.status}  Paused: {s.paused}  Started: {s.started}")
print(f"Waves: {s.total_waves}  Tasks done: {done}/{len(s.tasks)}")
from agentflow.config import load_environment
tpl = load_environment().status_board_url_template
if tpl:  # null (default) ⇒ no dashboard, print nothing; else render the board URL
    print(f"Status board: {tpl.format(slug=slug)}")
PYEOF
```

**Fleet-context branch (Resume).** In a fleet-launched run — one whose invocation carried the
literal `fleet-context: <agent>` marker (see **Execution context**) — do NOT call
`AskUserQuestion`. Raise a registry `## Questions` row (question: "epic `<slug>` is paused at
`<STATUS_PATH>` — resume it, or just report the board?") with `default:` = **just show the board,
do NOT resume**, and urgency `waiting`, then **park**.

Note this default is deliberately NOT the site's standalone first option (`Resume`). An epic is
paused because a human or the orchestrator paused it on purpose; resuming restarts autonomous
execution and a wake schedule, so it is the irreversible direction, while showing the board costs
one wasted wake. `advisory` requires a safe REVERSIBLE default — "resume the run nobody chose to
un-pause" is not one, so this gate waits rather than proceeding. When the row comes back
`answered`, apply it (resume only if the answer says so) and flip the row `applied`. Standalone
interactive behavior is unchanged.

**Standalone only — skip this entire call in a fleet-launched run** (the fleet-context branch
above already resolved the resume decision and proceeded; falling through to the buttons here
would fire them at nobody). Then call `AskUserQuestion` with header `"Resume"` and options:
- `{label: "Resume", description: "Clear paused: true and reschedule next wake"}`
- `{label: "Just show board", description: "Print the status-board URL (or the status.md path if no board is configured); do not resume"}`

The free-text fallback ("Other" option) must remain enabled. Map canonical replies: "Resume" → clears paused-state mutation; "Just show board" → shows the board URL (or the status.md path when no board is configured) only. The orchestrator handles state mutation and `ScheduleWakeup` downstream.

## When to use

- User typed `/project` (any arg or no arg)
- User said "spin up an epic for X", "kick off a project on Y", "take this from spec to epic", "run /project on this plan", "resume that epic", or any phrase signalling *push something into the epic pipeline at whatever stage it's at*

## When NOT to use

- **Single-task work** (one bug, one small feature) — direct edit or `../refine/SKILL.md` then a Task call
- **User asked only to brainstorm** ("help me think through X") — invoke `../refine/SKILL.md` directly
- **User asked only for a plan** ("write me a plan for X") — invoke `solution` directly
- **Interactive (non-orchestrator) plan execution** ("walk me through this plan step by step") — `../_vendored/executing-plans/SKILL.md` directly

## Failure modes

| Failure | Action |
|---|---|
| Mode detection returns `ambiguous` | Ask the user via button options (primary), with free-text 'Other' fallback. Do not guess. In a fleet-launched run, raise a registry `## Questions` row and park (see Step 0's `fleet-context` branch). |
| `CLAUDE.md` missing AND user declines (fresh / from-refine only) | Stop at Step 1, suggest `/init`, exit. |
| Brainstorming aborts (user says "never mind") in `fresh` | Stop at Step 2. No spec produced; nothing to clean up. |
| `solution` aborts on validation in `fresh` / `from-refine` | Surface the parse error. Suggest the user fix the spec and re-invoke `/project <spec-path>`. |
| `from-solution` input doesn't actually parse as a plan | Re-route to `from-refine` and let `solution` wrap it (one-line warning to the user). If still fails, stop. |
| User declines gate #1 | Stop at Step 4. Print plan path and the `/project <plan-path>` resume command. |
| `edit` branch produces an unparseable plan | Loop on Step 4 until parse succeeds OR user declines. Do not auto-fix. |
| User declines gate #2 | Orchestrator exits cleanly. Plan stays on disk. Print the resume command. |
| Orchestrator bootstrap fails | Surface the orchestrator's error verbatim. Do not retry blindly — likely a real environmental issue. |
| `from-status` on a status file that's already terminal (`done`) | Print the final summary + status-board URL. Do not reschedule. |

## Constraints

- **Do not skip the brainstorm in `fresh` mode.** This skill exists because the best epics start with the interactive design conversation. If the user already has a finished spec, they should call `/project <spec-path>` (which routes to `from-refine`).
- **Do not autonomously answer brainstorming questions.** The brainstorm is a live conversation between the user and the brainstorming skill. You orchestrate handoffs, not participate.
- **Do not collapse the two approval gates.** They protect different things. Both fire in every mode that reaches Step 5.
- **Never fire `AskUserQuestion` in a fleet-launched run, and never drop the `fleet-context` marker.** Both gates and both propagation points (Step 3 → `solution`, Step 5 → `orchestrator`) are part of one contract; branching this skill's gates while swallowing the marker just moves the unattended prompt downstream.
- **Never skip Step 0.5 (grounding preflight).** No mode, `current_state`, or urgency waives the canonical-repo check or the premise probe.
- **Never dispatch into the shared checkout, and never create a worktree implicitly.** Epic execution and parallel file-mutating agents get dedicated worktrees, created and addressed by explicit path off the resolved block (Step 5) — the launch directory is not a repository, so anything that binds to the working directory binds to nothing.
- **Do not modify the plan body in the `edit` branch.** The user is the editor. You only re-validate after the editor closes.
- **Do not hand off to anything other than `orchestrator` at Step 5.** This skill is specifically for the autonomous-execution pipeline. Interactive plan execution → `../_vendored/executing-plans/SKILL.md` directly.
- **Do not fall back to `fresh` mode silently when a path arg fails to classify.** Always surface ambiguity and ask.

## Bottom line

`/project [arg]` is one entry point for every stage of the epic pipeline:

| Command | What happens |
|---|---|
| `/project` | Prompts for topic. Full pipeline: brainstorm → plan → gate #1 → orchestrator → gate #2 → board URL |
| `/project some topic string` | Same as above with topic prefilled |
| `/project <data_root>/projects/<name>/design/specs/<spec>.md` | Skip brainstorm. Plan → gate #1 → orchestrator → gate #2 → board URL |
| `/project <data_root>/projects/<name>/design/plans/<plan>.md` | Skip brainstorm + plan. Gate #1 → orchestrator → gate #2 → board URL |
| `/project <data_root>/projects/<name>/status/<x>.status.md` | Resume / show board |

Everything else lives in the underlying skills. Do not re-implement their behavior here. If a step needs to change, change it in the skill that owns the behavior, not in this wrapper.
