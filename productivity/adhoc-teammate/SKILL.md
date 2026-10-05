---
name: adhoc-teammate
description: Manually spawn a one-off teammate after listing available models and proposing the best provider, model, and thinking level for the task. Use when manually invoked to create an ad hoc worker for focused implementation, research, review, or planning.
disable-model-invocation: true
---

## Workflow

1. Clarify `cwd`, teammate role, task, and expected deliverable.
2. Run `pi --list-models`.
3. Prefer providers in this order when suitable: `openai-codex`, `zai`, `github-copilot`, `anthropic`.
4. Propose a table in this exact shape: `team_mate | provider | model | thinking level`.
5. Default suggestions:
   - deep code / planning / review → `openai-codex | gpt-5.4 | high`
   - cheap parallel scout / light edits → `openai-codex | gpt-5.4-mini | medium`
   - prose-heavy synthesis / research → `anthropic | claude-sonnet-4.6 | high`
   - if unavailable, choose the nearest fit from the live list
6. Ask for approval or refinement. Do **not** call `team_create` or `spawn_teammate` until approved.
7. After approval, create or reuse a small runtime team, then `spawn_teammate` with a self-contained prompt.

## Rules

- Quality first, then price.
- Keep the teammate prompt narrow, concrete, and file/task scoped.
- Manual use only. Never invoke this skill from another model.

## Waiting / polling policy

- Prefer event-driven orchestration over tight polling.
- After dispatching a teammate, do **not** immediately re-check status in a rapid loop.
- Default behavior: send the work, state the expected reply, then explicitly conclude your turn and become idle.
- After dispatch, assume you will be resumed automatically when a new teammate message arrives; do not manufacture wake-ups yourself.
- Only poll when a human explicitly asks for progress, when a timeout/risk threshold matters, or when a teammate has been silent longer than reasonably expected for the task size.
- Never do repetitive `check_teammate` / inbox polling every few seconds.
- Polling via `wait_background_process` is prohibited without a strong explicit reason, such as an external long-running job, a human-requested progress check, or a real timeout/risk boundary.
- For normal teammate orchestration, wait for messages instead of scheduling artificial wake-ups.
- If you must poll, use a coarse cadence measured in minutes, not seconds, unless the task is known to complete almost instantly.

## Communication
Honor active caveman mode for user-facing replies per `../../references/communication-mode.md`. Keep durable artifacts normal unless the human asks otherwise. Drop caveman for safety/clarity when needed, then resume.
