---
name: debateclaw-v1
description: >
  Self-contained DebateClaw V1 skill bundle for installing, verifying,
  troubleshooting, configuring, and launching DebateClaw V1 through ClawTeam.
  Use this whenever the user mentions DebateClaw V1, ClawTeam-based debates,
  DebateClaw bootstrap/setup, preset selection, run-plan compilation,
  OpenClaw/Codex/Claude Code debate launches, or asks how to install/copy the
  V1 skill bundle. Prefer this skill over older split DebateClaw bootstrap /
  orchestrator skills when the request is about the V1 layout or operator flow.
---

# DebateClaw V1

This directory is the **installable skill bundle**.

Treat the directory containing this `SKILL.md` as `<skill-root>`.
All agent-facing scripts, references, control metadata, workflows, presets, and
prompt assets needed for DebateClaw V1 live inside this bundle.

Do **not** depend on sibling developer docs or repo-only files when operating
through this skill. If a human cloned the repo and copied only this directory
into their skills folder, your instructions should still work.

## Bundle layout

Within `<skill-root>`:

- `scripts/` — executable helpers and operator entrypoints
- `references/` — agent-facing docs to read as needed
- `control/` — provider/model/profile metadata and persisted run-state surfaces
- `workflows/` — workflow definitions
- `presets/` — V1 preset definitions
- `prompts/` — modular prompt contracts and modules
- `generated/` — runtime-derived command maps, prompt bundles, runtime context, and templates

## Before doing anything else

Choose the track first, then read the relevant references.

### Track A — install / verify / troubleshoot / configure

Read:

- `references/runtime-matrix.md`
- `references/openclaw-env-conventions.md`
- `references/reliability-playbook.md`

Use this track when the user wants to:

- install or refresh `clawteam`
- verify the current machine is ready for DebateClaw V1
- deploy runtime helpers and templates
- inspect OpenClaw env variable names
- provision or verify DebateClaw-managed OpenClaw slots
- verify or apply model profiles
- diagnose why a launch is failing before retrying

### Track B — choose preset / compile / materialize / launch / monitor

Read:

- `references/preset-guide.md`
- `references/reliability-playbook.md`

Use this track when the user wants to:

- choose between `parallel@1` and `review-loop@1`
- turn a problem into a concrete debate motion
- compile a run plan
- materialize launch-ready assets
- launch or relaunch a debate run
- monitor progress and hand back results

## Root rule

Pass `--root <skill-root>` whenever a script accepts a root.

That keeps the bundle self-contained and avoids accidental dependence on a
larger repo layout.

## Bootstrap / verification workflow

Default order:

1. Check machine/runtime readiness.
2. Confirm local `clawteam` syntax with `clawteam ... --help`.
3. For OpenClaw, inspect env **names only**.
4. Install or refresh `clawteam` if needed.
5. Deploy DebateClaw runtime assets.
6. Verify bootstrap / slot / model-profile status.
7. For OpenClaw, provision or reuse slots and run real smoke tests before launch.

### Canonical commands

Check runtime:

```bash
uv run --script <skill-root>/scripts/check_runtime.py --agent openclaw --backend subprocess
```

Inspect env names only:

```bash
uv run --script <skill-root>/scripts/inspect_openclaw_env.py \
  --env-file ~/.openclaw/.env \
  --family qwen \
  --family minimax \
  --family kimi \
  --family glm \
  --json
```

Install or refresh ClawTeam:

```bash
uv run --script <skill-root>/scripts/install_clawteam.py --mode tool --source pypi
```

Deploy runtime helpers and templates:

```bash
uv run --script <skill-root>/scripts/deploy_templates.py
```

Inspect current V1 status:

```bash
python3 <skill-root>/scripts/bootstrap_status.py --root <skill-root>
```

Verify current OpenClaw slot bindings against a model profile:

```bash
python3 <skill-root>/scripts/apply_model_profile.py --root <skill-root> parallel-default --verify
```

Provision or reuse fixed OpenClaw slots:

```bash
uv run --script <skill-root>/scripts/ensure_openclaw_debate.py \
  --proposer-count 4 \
  --family minimax \
  --family kimi \
  --family glm \
  --coordinator-family minimax \
  --command-map-file ~/.clawteam/debateclaw/command-map.json \
  --json
```

## Launch workflow

### UI config boundary

This installable bundle does **not** define or store reusable frontend `config_id`
objects inside the bundled `control/` metadata.

If a user provides a `config_id`, treat it as an **external operator-owned launch
input** backed by a local runtime store on the machine.

Default shared runtime path:

```text
~/.clawteam/debateclaw/control-ui/
```

Override it when needed with:

```bash
DEBATECLAW_CONTROL_UI_HOME=/custom/path
```

Expected files there:

- `run-configs/<config_id>.json`
- optional `model-catalog.json`
- optional `run-metadata/<run_id>.json`

Rules:

- Do **not** invent HTTP calls or assume an external API/sidecar exists.
- Do **not** start, stop, or manage any API service unless the user explicitly
  asks you to work on that API surface.
- Stay on the normal script-driven DebateClaw path by default.
- If `config_id` is present, prefer the bundled helper:

  ```bash
  python3 <skill-root>/scripts/launch_from_config.py \
    --root <skill-root> \
    --config-id <config-id> \
    --goal "<normalized goal>" \
    --entry-session-key <entry-session-key>
  ```

- The helper reads the external shared runtime store, applies inline fixed-slot
  model mapping, compiles/materializes the run, and records run metadata.
- If the external shared runtime store or the target `config_id` does not
  exist, say plainly that the local runtime is missing the operator-provided UI
  config store, then ask for the equivalent standard launch inputs instead:
  preset/mode, proposer count, per-slot model mapping, round limits, and the
  concrete goal.

A `config_id` is therefore a valid operator hint, but it depends on the local
runtime store rather than the bundled DebateClaw control metadata.

### Hard gates

Before launch, make sure all of these are true:

1. The motion is concrete unless the user explicitly asked for a smoke test.
2. Local `clawteam launch --help` has been checked.
3. For OpenClaw, env-name discovery has been done without printing secrets.
4. Assigned providers or slots passed real smoke tests.
5. Slot reuse plus session isolation are defined.

Do not launch with placeholder goal text like “the user's requested task”.

### Preset selection

- `parallel@1` — multiple independent proposals, outer agent judges afterward
- `review-loop@1` — proposal + cross-review + rebuttal stress test before outer judgment

### Main V1 entrypoint

Prefer the unified entrypoint:

```bash
python3 <skill-root>/scripts/launch_from_preset.py \
  --root <skill-root> \
  --preset parallel@1 \
  --goal "<normalized goal>" \
  --launch-mode print
```

Use `--launch-mode print` first unless the user explicitly wants the actual
launch now and preflight is already solid.

### Fresh-run default

Treat "start a debate" as "create a new debate run" by default.

- Default to a **fresh run id** and a **new debate round** for every new launch.
- Reuse fixed slots, but **do not** reuse a previous run id or implicitly
  continue an old run just because the topic is similar.
- Only inspect, re-materialize, resume, or recover an existing run when the
  user explicitly asks for that exact old run or names the run id.
- If the user asks to debate the same motion again, treat that as a **new
  round** with a **new run id**, not a continuation of the old one.

Useful overrides:

- `--run-id <id>`
- `--model-profile <profile>`
- `--proposer-count <N>`
- `--review-rounds <R>`
- `--rebuttal-rounds <B>`
- `--additional-file-workspace <opaque-locator>`
- `--launch-mode run`

### Additional file boundary

`--additional-file-workspace` is an **opaque run-scoped locator**.
DebateClaw passes it through into the run plan, runtime context, prompt bundle,
and rendered template, but does not interpret or materialize it.

### Useful operator scripts

Compile only:

```bash
python3 <skill-root>/scripts/compile_runplan.py --root <skill-root> --preset parallel@1 --goal "..."
```

Launch from an external reusable `config_id` store:

```bash
python3 <skill-root>/scripts/launch_from_config.py \
  --root <skill-root> \
  --config-id <config-id> \
  --goal "<normalized goal>"
```

Re-materialize a persisted run (only when the user explicitly wants that exact
existing run recovered or re-rendered):

```bash
python3 <skill-root>/scripts/rerender_run.py --root <skill-root> <run-id>
```

List runs:

```bash
python3 <skill-root>/scripts/list_runs.py --root <skill-root>
```

Show one run:

```bash
python3 <skill-root>/scripts/show_run.py --root <skill-root> <run-id>
```

Clean generated artifacts and stored run state:

```bash
python3 <skill-root>/scripts/cleanup_run.py --root <skill-root> <run-id>
```

## User update contract

Immediately after creating a debate, report:

- run ID
- preset / template name
- role -> slot -> model mapping
- how to watch progress

Use precise language:

- **team created** — ClawTeam accepted the launch
- **debate healthy** — workers are responding and state is advancing
- **results ready** — proposals/results are present in the debate state and the outer agent can judge

Do not claim a debate is healthy merely because the team exists.

## Review-loop operator rules

For `review-loop@1`, treat these as hard rules:

- Cross-review means review only the targets listed by `debate_state.py next-action`; never self-review.
- A failed or conceded proposal does **not** end that agent's run. Failed proposers still review, wait,
  and follow `next-action` until it returns `stop`.
- If an agent repeats the same tool validation/schema failure twice, treat it as blocked. Do not assume
  it will self-recover; inspect `next-action`, logs, and be ready to intervene.

## Monitoring and handoff

Useful commands:

```bash
clawteam board show <team-name>
clawteam task wait <team-name>
~/.clawteam/debateclaw/bin/debate_state.py summary --team <team-name> --json --include-bodies
```

When the team completes, the **outer entry agent** is the final judge.
Read the debate state and synthesize or select the final answer for the user.

## Retry discipline

If a run fails:

- stop stale waiters or wrappers before retrying
- explain the real failure mode plainly
- change something material before retrying
- avoid layered retries that leave multiple partial runs consuming tokens

Abort and report instead of improvising more retries if:

- the motion is still ambiguous
- the same provider fails the same smoke test twice
- session isolation is still unclear
- the next retry would add no new information
