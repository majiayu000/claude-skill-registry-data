---
name: aiwf-debug-agent-swarm
description: Parallel debugging and codebase-crawling workflow for spawning many focused Codex subagents across a project. Use when the user explicitly asks to spawn agents, use subagents, swarm a repo, crawl a project, run many debugging agents, perform broad bug triage, parallelize code investigation, audit an unfamiliar codebase for failures, or split debugging/fix work across independent modules.
---

# Debug Agent Swarm

Coordinate a high-fanout debugging crawl. Maximize useful parallelism: one clear lane per agent, no duplicated crawling, no overlapping write ownership, and parent-agent integration of every result. Subagents discover and log issues; the parent agent implements fixes.

## Quick Start

1. Confirm the user has authorized subagents. This skill's trigger normally satisfies that when the request says "spawn agents", "swarm", "subagents", or "as many agents as possible".
2. If subagent tools are not visible, call `tool_search` for `multi-agent subagent spawn worker explorer`. Use `multi_agent_v1.spawn_agent`, `wait_agent`, `send_input`, and `close_agent` when available.
3. Parent reads local project instructions first: `AGENTS.md`, README files, package manifests, test configs, CI files, and `git status`.
4. Create a debug pass folder for subagent Markdown reports. For UI/API work, prefer:

```powershell
python <this-skill>\scripts\scaffold_debug_pass.py --root <project-root> --slug <short-slug>
```

5. Run the inventory helper when the project is large or unfamiliar:

```bash
python <this-skill>/scripts/project_inventory.py --root <project-root> --out <project-root>/.codex/aiwf-debug-agent-swarm/inventory.md
```

6. Read [references/swarm-playbook.md](references/swarm-playbook.md) and `C:\Users\Shawn\.codex\skills\aiwf-ui-electrician\references\debug-pass-protocol.md` before spawning the first wave. Use their lane matrix and report templates.

## Subagent Context Rules

Subagents should get narrow context and write artifacts instead of long summaries.

- Give each subagent the debug pass folder and one lane.
- Subagents read parent-provided context, `_context.md`, `SUB_AGENTS.md` if present, or only the `Known Issues` section of `AGENTS.md`.
- Subagents do not read full `AGENTS.md` unless the parent explicitly says the whole file is needed.
- Subagents read relevant project notes for their lane, but avoid broad repo archaeology.
- Subagents use online or primary-source research when framework, runtime, model-card, or API semantics are uncertain.
- If no source research is used for a claim, confidence must be 90/100 or higher.

## Fanout Rules

- Spawn as many agents as there are independent, useful lanes. If the runtime refuses more agents or a concurrency limit is reached, stop spawning and continue in waves.
- Prefer `explorer` agents for read-only crawling, root-cause hypotheses, repro discovery, and risk finding.
- Do not use subagents for repair work by default. The parent agent reads reports and applies fixes.
- The only repair exception is a simple syntax fix of three changed lines or fewer. The subagent must record exact file and line changes in its report.
- Do not assign two agents the same lane unless the second pass is explicitly a verification pass.
- Do useful local work while agents run: reproduce the bug, inspect logs, run narrow tests, or prepare integration notes.
- Close each agent after its result is consumed so completed workers do not count against the concurrency limit.

## Report Contract

Each agent writes one Markdown file in the debug pass folder. The report must include:

- Scope and files/logs inspected.
- Issues found, ordered by severity.
- Evidence and user-visible impact.
- Repro or trigger when known.
- Affected files, routes, callbacks, model families, or UI areas.
- Confidence and whether research was used.
- Syntax-fix exception details, or `None`.

Do not ask subagents to write patch recipes. They should report the problem, not spend tokens explaining the fix.

## Parent-Agent Duties

The parent agent owns coordination and truth. Do not simply paste agent summaries.

1. Build a lane table with owner, scope, agent id, status, and expected output.
2. Read every Markdown report in the debug pass folder before implementing.
3. Deduplicate findings across agents.
4. Verify high-severity claims locally when cheap, especially before editing.
5. Research claims below 90/100 confidence before turning them into fixes.
6. Rank findings by impact: crash/data loss/security/build break first, then functional regressions, then maintainability.
7. Integrate patches only after checking changed paths and conflicts.
8. Report what was covered, what was not covered, exact commands run, and remaining risk.

## Safety

- Do not use destructive git commands, delete user files, push, publish, or change production services unless the user explicitly asks.
- Avoid long downloads, large model pulls, GPU-heavy runs, migrations, or external side effects unless they are clearly part of the requested debugging task or the user approves.
- Keep secrets out of prompts and summaries. Pass file paths, logs with secrets redacted, and narrow context instead of whole environment dumps.
- If subagent tools are unavailable, run the same lane plan serially and say no separate subagent runtime was available.
