---
name: convex-worker-cli
description: Use this skill when orchestrating RLM-style or swarm-style work on this repo through the worker control plane, especially when a root Codex or Claude agent should launch cheap bash workers via `pnpm worker:codex` or `pnpm worker -- ...`, keep its own context small, and consume `/handoff/*` artifacts instead of raw child output.
---

# Convex Worker CLI

Use the worker control plane as the default subagent surface for this repo.

Prefer it when:

- the user wants subagents, a swarm, recursive decomposition, or RLM-style work
- the task benefits from cheap worker forks over the same synced repo state
- child work can be expressed as bounded shell tasks
- the root agent should receive reduced artifacts, not verbose tool logs

Do not use this skill for ordinary single-agent coding in one local sandbox.

If the user asks for "subagents" in this repo, prefer this skill before native `spawn_agent`. The intended cheap fan-out path here is Convex workers plus bash.

## Mental model

Automatic host-side orchestration:

```text
user goal
   |
   v
pnpm worker:codex -- run --goal "..."
   |
   +--> local Codex planner
   +--> root worker create/reuse
   +--> repo sync into /workspace
   +--> batch delegate child bash workers
   +--> collect /handoff/*
   +--> local Codex synthesizer
```

Manual provider-neutral orchestration:

```text
root agent
   |
   v
pnpm worker -- create / sync / delegate / collect
   |
   v
Convex worker records -> sandbox/session -> just-bash runtime
   |
   v
/handoff/summary.md / plan.md / findings.md
```

The root loop should stay small:

```text
1. decide decomposition
2. sync code once
3. delegate bounded child tasks
4. collect small artifacts
5. synthesize
```

## Choose a mode

Use `pnpm worker:codex` when:

- the root agent is Codex
- you want automatic planning plus synthesis
- local `codex exec` auth is working

Use raw `pnpm worker -- ...` when:

- you want provider-neutral orchestration
- you want precise control over child commands
- you are operating from Claude Code or plain shell
- you need a fallback if local Codex auth is unavailable

## Preconditions

The worker CLI needs a Convex deployment URL. Resolve it in this order:

1. `--url`
2. `CONVEX_URL`, `CONVEX_DEPLOYMENT_URL`, or `NEXT_PUBLIC_CONVEX_URL`
3. `./.env.local`, then `./.env`
4. `./.convex-worker.json`
5. `~/.config/convex-sandbox/worker.json`

Optional admin auth:

- `--admin-key`
- `CONVEX_ADMIN_KEY`
- `adminKey` in the JSON config

Config shape:

```json
{
  "url": "https://<deployment>.convex.cloud",
  "adminKey": "<optional>"
}
```

For host-side Codex orchestration, verify auth first:

```bash
codex login status
```

This repo includes a project-scoped ChatGPT profile in `.codex/config.toml`:

```toml
[profiles.worker-chatgpt]
forced_login_method = "chatgpt"
cli_auth_credentials_store = "keyring"
```

If needed:

```bash
codex login -c 'forced_login_method="chatgpt"' -c 'cli_auth_credentials_store="keyring"'
```

## Automatic mode: `pnpm worker:codex`

Start here when the user wants real subagent fan-out and the root agent is Codex.

Example:

```bash
pnpm worker:codex -- run \
  --goal "Map the worker orchestration surface and summarize the next engineering moves" \
  --codex-profile worker-chatgpt \
  --planner-model gpt-5.4-mini \
  --synth-model gpt-5.4
```

If local Codex warmup is slow on a machine, raise the preflight guardrail:

```bash
pnpm worker:codex -- run --goal "..." --auth-preflight-timeout-ms 180000
```

What the wrapper does:

```text
goal
  -> auth preflight
  -> planner prompt
  -> root worker create/reuse
  -> sync local repo to /workspace
  -> batch delegate child tasks
  -> collect artifacts
  -> synth prompt
  -> final report
```

Artifacts are written under:

- `.codex/worker-runs/<timestamp>-<slug>/goal.txt`
- `.codex/worker-runs/<timestamp>-<slug>/auth-preflight.txt`
- `.codex/worker-runs/<timestamp>-<slug>/plan.json`
- `.codex/worker-runs/<timestamp>-<slug>/batch-result.json`
- `.codex/worker-runs/<timestamp>-<slug>/final.md`
- `.codex/worker-runs/<timestamp>-<slug>/run.json`

Use this mode when you want the skill to behave like "launch subagents, then hand me the reduced answer."

## Manual mode: `pnpm worker -- ...`

Use this when you want explicit control over child instructions.

Create a root worker:

```bash
pnpm worker -- create --name root --goal "Map the repo and propose a plan"
```

Sync the local repo into the root sandbox:

```bash
pnpm worker -- sync --worker-id <rootWorkerId> --source . --dest-root /workspace --cwd /workspace --delete-missing
```

Delegate one child:

```bash
cat <<'EOF' | pnpm worker -- delegate --worker-id <rootWorkerId> --name grep-auth --goal "Find auth entry points" --artifact summary.md
cd /workspace
set -eu
rg -n "auth|token|session|jwt" .
mkdir -p /handoff
cat <<'OUT' > /handoff/summary.md
## Evidence
- Listed auth-related entry points with `rg`.

## Findings
- Add concise findings here.

## Next steps
- Add the smallest useful next action.
OUT
EOF
```

Batch fan-out:

```bash
cat <<'EOF' | pnpm worker -- batch delegate --worker-id <rootWorkerId>
{
  "tasks": [
    {
      "name": "grep-auth",
      "goal": "Find auth entry points",
      "command": "cd /workspace\nset -eu\nrg -n \"auth|token|session|jwt\" .\nmkdir -p /handoff\ncat <<'OUT' > /handoff/summary.md\n## Evidence\n- Auth scan complete.\n\n## Findings\n- Fill in concise findings.\n\n## Next steps\n- Fill in next steps.\nOUT",
      "artifacts": ["summary.md"]
    },
    {
      "name": "grep-worker",
      "goal": "Find worker orchestration touchpoints",
      "command": "cd /workspace\nset -eu\nrg -n \"worker|handoff|sandbox\" convex scripts README.md\nmkdir -p /handoff\ncat <<'OUT' > /handoff/summary.md\n## Evidence\n- Worker scan complete.\n\n## Findings\n- Fill in concise findings.\n\n## Next steps\n- Fill in next steps.\nOUT",
      "artifacts": ["summary.md"]
    }
  ]
}
EOF
```

Collect all child artifacts:

```bash
pnpm worker -- collect --worker-id <rootWorkerId> --read-artifacts
```

## Child worker contract

When you generate child commands, make them boring and strict.

Always:

- `cd /workspace`
- `set -eu`
- use fast read-only shell tools first: `rg`, `ls`, `find`, `sed`, `head`, `tail`, `wc`, `sort`, `uniq`, `cat`
- write reduced output to `/handoff/*`
- keep stdout short unless the task explicitly needs raw output

Default artifact names:

- `/handoff/summary.md`
- `/handoff/findings.md`
- `/handoff/plan.md`
- `/handoff/patch-plan.json`

Recommended child report shape:

```markdown
## Evidence
- Concrete commands run or files inspected.

## Findings
- Short factual bullets only.

## Open questions
- Only include true blockers or ambiguities.

## Next steps
- Smallest useful follow-up.
```

Avoid asking children to stream long logs back to the root. The whole point is reduction at the edge.

## Prompting guidance for automatic planning

Good root goals are concrete and bounded:

- "Map the worker orchestration surface and propose the next implementation steps."
- "Inspect auth token handling across the worker wrapper and summarize risks."
- "Split the repo into 4 review slices and produce one finding summary per slice."

Bad root goals are vague:

- "Look around."
- "Think hard about the repo."

If you already know the child decomposition, skip planner creativity and use `pnpm worker -- batch delegate` directly.

## Recommended root workflow

- Create or reuse one root worker per task.
- Sync the relevant repo slice once before fan-out.
- Prefer `sync --delete-missing` when the sandbox should converge to local state.
- Delegate bounded children with disjoint goals.
- Ask each child for one or two artifacts, not a transcript.
- Collect artifacts, then synthesize locally.

If a child is only doing one trivial command, run it in the root worker instead of forking.
