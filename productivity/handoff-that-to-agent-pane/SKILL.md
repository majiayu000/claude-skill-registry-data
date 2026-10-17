---
name: handoff-that-to-agent-pane
description: Hand off a bounded task to a chosen coding agent in a right-hand Herdr pane using a conversation snapshot.
disable-model-invocation: true
---

# Handoff That to Agent Pane

Treat the handoff as a **brief**: give the specialist the relevant context, a bounded assignment, and a checkable deliverable.

Take the snapshot first: load and follow the `tmp-snapshot` skill before any other step in this workflow, preflight included. Load and follow the `herdr` skill before issuing any Herdr command.

## Resolve the brief

Determine these inputs from the request:

- **Agent:** `claude`, `codex`, `agent` (Cursor Agent), or `pi`. Default to `claude` when the user omits it. Take the executable's Herdr `--kind` from the launch matrix: read `~/.agents/skills/herdr-orchestration/references/agent-launch.md`. When that file is not installed, take the kind from `herdr agent`'s installed kind list instead — the kinds are named for agents, and the executable name `agent` is not among them.
- **Model:** normalize natural-language model and effort names before choosing the launch command; otherwise use the table below.
- **Context slice:** include only the part of the conversation and current work the specialist needs.
- **Assignment:** state the work to perform, its boundaries, whether edits are allowed, the deliverable, and how to verify it.
- **Delegation:** carry any requested subagent strategy into the assignment, including requests to use as many subagents as useful.
- **Return path:** decide whether the user only wants the pane started or wants this session to collect and integrate the result.

Ask once before mutating anything only when the assignment cannot be inferred safely.

## Model defaults

| Agent | Default | Interactive launch command |
|---|---|---|
| `claude` | Opus 5.5, high effort | `claude --model opus --effort high --dangerously-skip-permissions` |
| `codex` | GPT-6 Sol, xhigh thinking | `codex -m gpt-6-sol --approve-for-me -c 'model_reasoning_effort="xhigh"'` |
| `agent` | Grok 4.6 High | `agent --model cursor-grok-4.6-high --yolo --sandbox disabled` |
| `pi` | Kimi K3-256k, max thinking | `pi --approve --provider kimi-coding --model k3-256k --thinking max` |

Each command above is complete and verbatim: it already embeds its agent's autonomous posture, so dispatch needs no extra permission or sandbox flags. The launch matrix (`~/.agents/skills/herdr-orchestration/references/agent-launch.md`) is the canonical explanation of those posture flags — including why the Codex command needs no separate `--sandbox` or `--ask-for-approval` flag and why pi's `--approve` is a trust flag, not a permission flag. Consult it instead of re-deriving flags; when it is not installed, the commands above still stand as written.

Treat `GPT 6`, `GPT 6 Sol`, and `Sol` as the model ID `gpt-6-sol`, `Astra` as `gpt-6-astra`, and `Luna` as `gpt-6-luna`; treat an explicit `GPT 5.6`, `GPT 5.6 Sol`, or `Codex 5.6` as `gpt-5.6-sol`. Treat `ultra` as **ultra reasoning effort** (`model_reasoning_effort="ultra"`), which Sol and Astra support; Luna has no ultra, so report that rather than substitute another effort. Treat `maximum` and `max` as **max reasoning effort**. Efforts are never part of a model ID. Thus “GPT 6 ultra” means:

```bash
codex -m gpt-6-sol --approve-for-me -c 'model_reasoning_effort="ultra"'
```

Treat `xhigh` and `extra high` as xhigh reasoning. Use another literal Codex model ID only when the user supplies the exact ID explicitly. Never manufacture an ID from prose.

For Cursor Agent, use this exact command when the user asks for Grok 4.6 High or does not override the `agent` default:

```bash
agent --model cursor-grok-4.6-high --yolo --sandbox disabled
```

Grok 4.6 exposes `low`, `medium`, `high`, and `xhigh`, each with a `-fast` twin; match on the ID rather than the label, since `cursor-grok-4.6-high` is labelled “Cursor Grok 4.6” and `cursor-grok-4.6-high-fast` is labelled “Cursor Grok 4.6 Fast”. Grok 4.5 exposes `low`, `medium`, and `high`, each with a `-fast` twin, and has no `xhigh`. Treat `xhigh` and “extra high” as the literal model ID `cursor-grok-4.6-xhigh-fast` when “fast” is requested, and `cursor-grok-4.6-xhigh` when it is not. Grok 4.7 IDs have no `cursor-` prefix: `grok-4.7-low`, `grok-4.7-medium`, `grok-4.7-high`, and `grok-4.7-xhigh`, each with a `-fast` twin. When the user asks for Grok 4.7, apply the same tier and “fast” rules to these IDs; with no tier named, use `grok-4.7-high`, mirroring the default. Do not infer any other Cursor model ID from prose.

When the chosen agent is `agent` (Cursor Agent) or `pi`, confirm before splitting that the selected literal model ID is listed. Run only the check for the agent you are dispatching, and skip this block entirely for `claude` and `codex`, which expose no local model list:

```bash
agent --list-models
pi --version
pi --list-models k3
```

`pi --list-models k3` currently surfaces `kimi-coding/k3` (1.0M context), `kimi-coding/k3-256k` (262.1K context), and `openai-codex/gpt-5.3-codex-spark`. Our pi default is **`kimi-coding/k3-256k`**.

For the Cursor default, require the exact `cursor-grok-4.6-high` entry. If it is absent, report the failed precondition; never silently fall back to a `-fast` variant, another Grok 4.6 tier, or Grok 4.5. For pi's default, require version 0.80.10 or later, configured Kimi Code access, and the exact `kimi-coding/k3-256k` entry. If `k3-256k` is absent, report the failed precondition and never silently use `k3`, K2.7, or another listed model. If any requested default is unavailable, stop before creating the pane and substitute only with the user's approval.

Keep the launch interactive and preserve the current working directory. Run each agent in the autonomous posture its table command already carries, per the launch matrix. Honor an explicit permission override from the user.

Preflight with local, non-inference commands only: `command -v`, `--version`, `--help`, or the model-list commands above. Never run `codex exec`, a print-mode agent turn, or any paid probe to test a model. Do not inspect personal config to replace defaults pinned by this skill.

## Dispatch

1. Invoke `tmp-snapshot` to save the relevant context slice as a standalone handoff in `/tmp`. Include current state, relevant decisions, concrete paths or artifacts, constraints, and unresolved questions. Treat its returned path and outline as a sub-step result and continue this workflow.
2. Confirm the snapshot path is readable and contains enough context to perform the assignment without the chat.
3. Follow `herdr` to verify `HERDR_ENV=1`, learn the installed CLI, and preflight the chosen executable and model. Complete this step only with a valid interactive launch command.
4. Split the calling pane to the right without moving focus:

   ```bash
   herdr pane split --current --direction right --cwd "$PWD" --no-focus
   ```

5. Read the new pane ID from the JSON response. Rename the pane for the assignment, then start the agent by name and kind, passing the launch command's arguments after `--`:

   ```bash
   herdr pane rename <returned-pane-id> "<short-label>"
   herdr agent start <name> --kind claude --pane <returned-pane-id> -- --model opus --effort high --dangerously-skip-permissions
   ```

   `--kind` selects the executable, so everything after `--` is the remainder of the chosen command from the table above. `agent start` returns once Herdr detects the agent ready for input. If it returns `agent_not_ready`, the agent is blocked at a startup dialog such as a trust or permissions prompt: read it with `herdr agent read <name> --source visible --format ansi`, surface it to the user, and prompt only once the agent is idle. Use a few words for the pane label; the full brief goes in the prompt template below, not in the label. Agent names must be unique among all live agents, so derive a short kebab-case name from the assignment and check `herdr agent list` first; if `agent start` returns `agent_name_taken`, choose another name.
6. Send one task prompt with `herdr agent prompt <name> "<text>"`. Use this shape:

   ```text
   Read <absolute-snapshot-path>. It is the handoff context for this assignment.

   Assignment: <specific work>
   Scope: <boundaries and whether edits are allowed>
   Delegation: <requested subagent strategy, or "decide as needed">
   Deliverable: <review, second opinion, implementation, investigation, or side-task result>
   Verification: <evidence or checks required>
   Unconfirmed: mark anything you couldn't confirm, and say where you looked.

   Treat this prompt as authoritative if it conflicts with the snapshot. Stop only for a blocker you can't resolve, and stay inside Scope.
   ```

7. Confirm the agent moved to `working`. If it did not, inspect its status and transcript before reporting the failure.

## Return

When the user only asked to open or hand off, finish after dispatch starts. Report the pane ID, agent and model, snapshot path, and assignment in one compact status.

When the user asked for the result, wait with `herdr agent wait <name>`, whose defaults settle on `idle`, `done`, or `blocked`, handle blockers through the user, read the transcript, and return or integrate the requested deliverable.

Finish only when the correct right-hand pane exists, the requested model is running, the snapshot-backed brief has been submitted, and the return path requested by the user is complete.
