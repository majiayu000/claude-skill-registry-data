---
name: repo-director
description: Coordinate an explicitly requested agent team maintaining the spring-boot-tools plugin, with bounded ownership, Herdr coordination, model selection and shared validation. Does not orchestrate Spring Boot application development through the shipped plugin.
---

# Repository director

Read `CONTRIBUTING.md` and `docs/architecture.md` from the repository root.
Keep the user's requested outcome as the team's scope. Team setup authorizes
orientation, not an unsolicited implementation or paid evaluation campaign.

## Roles and model policy

These are initial operating choices, not measured rankings. Verify model and
effort availability in the current environment before launch; never silently
substitute an unavailable model. The director keeps its current model unless
the user changes it; a skill cannot reconfigure the running parent session.

| Role | Initial model / effort | Owned surface when assigned implementation |
| --- | --- | --- |
| Runtime and MCP (`sbt-runtime`) | `gpt-6.1-sol` / `high` | `runtime/`, `hooks/`, `mcp-server/`; related functional regressions |
| Skills and behavior (`sbt-behavior`) | `gpt-6.1-sol` / `high` | shipped `skills/`, `agents/`, behavioral `evals/`; executable examples by assignment |
| Quality and packaging (`sbt-quality`) | `gpt-6.1-sol` / `medium` | independent review, CI/packaging evidence; edits only by explicit assignment |
| Difficult unresolved design/review | `gpt-6-astra` / `xhigh` | bounded escalation after concrete uncertainty or failed attempts |

Use fewer agents for smaller tasks. Keep at most three specialists active with
the director by default; this is a coordination limit, not a claimed CLI limit.
Reuse idle specialists. Raise effort to `xhigh` for demonstrated concurrency,
cancellation, compatibility or cross-component reasoning difficulty. Routine
inventory can use `medium`. Do not default to `max`/`ultra` for every task.

The shipped Claude agent `model: sonnet` settings are independent product
configuration; do not rewrite them to match this maintenance team.

## Dispatch

Give each specialist the objective, required context, permitted files/actions,
expected evidence, completion condition and return format. Start orientation
read-only. Assign edits only when an implementation objective is authorized.
Give each assignment a task ID and require that ID in the final report.
Before submitting new work, confirm the specialist is idle/done and collect
its previous report. Do not treat a busy agent's earlier completion as the
new task's result. Deliberate steering of active work must name the active ID.
Shared files, manifests, README and integration decisions belong to the
director unless handed off. Tests touching another specialist's owned files
require an ownership handoff, not simultaneous edits.

Ask each specialist to return: inspected scope; findings with path/line and
trigger; confirmed versus inferred consequences; validation performed; next
action and remaining uncertainty. Empty findings are valid. The director
deduplicates reports, resolves disagreements and owns the final verdict.

## Herdr transport

Use the installed Herdr skill and CLI help as the operational reference.
This transport applies only when the user requested Herdr and `HERDR_ENV=1`.
Check `HERDR_ENV=1` and `herdr status`. Discover existing agents before creating
duplicates. Use explicit IDs or names, `--current` for the caller and
`--no-focus` for background layout. Default to sibling panes in this tab and
the repository cwd; additional workspaces/worktrees require user intent.
Choose split direction from live geometry and capture IDs from JSON.

Launch supported Codex agents in available shell panes, for example:

```sh
herdr agent start sbt-runtime --kind codex --pane <returned-pane-id> -- -m gpt-6.1-sol -c 'model_reasoning_effort="high"' -s read-only -a never
herdr agent prompt sbt-runtime '<bounded orientation task>' --wait --timeout 45000
herdr agent read sbt-runtime --source recent-unwrapped --lines 120
```

Read-only sandbox is appropriate for initial orientation and review. For a
implementation assignment, start a workspace-write session within the
authorized scope; instructions cannot elevate an existing sandbox. With the
user's no-interruption preference, use `-a never`: a restricted action fails
instead of opening an approval dialog. Workers report the failed action and
evidence to the director, who performs already-authorized work using its own
available permissions. Do not repeatedly relaunch workers to gain privileges.
Never expand a worker to full access merely to suppress prompts. Do not change
global account settings or persisted trust to arrange this workflow.

The director owns Herdr commands; specialists perform their bounded task and
return results, without spawning another team or controlling sibling panes.
Submit independent tasks promptly, then wait in bounded intervals of at most
45 seconds and collect reports. Use native subagents only as an explicit
fallback, not as a second duplicate team for the same work. On interruption,
discover live names and state before retrying starts or prompts.

Inspect blocked UI before acting. Resolve ordinary failures within existing
authorization; do not ask the user to repeat an authorization already given.
Actual approval/trust dialogs remain subject to the installed Herdr skill;
do not answer them on the user's behalf. A no-questions preference is not
permission to accept an unrelated trust or destructive action.
If such a dialog cannot be resolved within existing authorization, leave that
specialist blocked, record the exact impediment and continue independent work.
With a no-questions instruction, report the unresolved blocker instead of
opening repeated permission questions. Never claim that `-a never` prevents
every startup, authentication or trust dialog.

Waits observe lifecycle, not task identity. After timeout/stall, inspect before
retrying a prompt. `unknown` is not completion. Larger transcript reads may
require idle state; use visible output while working. If a completed report
cannot be recovered, request a temporary Markdown report only when the agent
already has an authorized writable destination; otherwise request a shorter
response and read it through Herdr.
Record live names, IDs, requested model/effort and verified status in the
session report; do not treat today's pane IDs as persistent configuration.
Never close unrelated panes or stop a server to refresh the team.

## Integration and validation

Collect reports before changing scope. Review the complete diff and run
appropriate checks from `CONTRIBUTING.md`. One designated runner owns expensive
shared verification. Run executable regressions for executable changes;
documentation-only coordination changes need
`claude plugin validate docs/skills --strict` and `git diff --check`.
`claude plugin validate skills --strict` covers only the shipped catalog, not
this maintenance skill under `docs/skills/`.
Quality must not independently approve its own CI/packaging implementation;
assign that review to another specialist or the director.
Report skipped or unavailable checks accurately. Behavioral evaluations and
Java examples are distinct evidence and must not be described as production
acceptance. Preserve failed results when evaluations are explicitly requested.

This skill lives under `docs/skills/` deliberately: `skills/` is the plugin's
public catalog with packaging checks. Root `AGENTS.md` makes this workflow
discoverable to repository maintainers without adding a shipped skill.

Official references: [Herdr stable index](https://herdr.dev/llms.txt),
[automation](https://herdr.dev/tui/docs/agent-automation/),
[Codex configuration](https://learn.chatgpt.com/docs/config-file/config-reference).
Recheck installed versions before relying on syntax after upgrades.
