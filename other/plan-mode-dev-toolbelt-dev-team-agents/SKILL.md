---
name: plan-mode
description: Plan-before-execute — structured plan, approval, replanning.
---

# Plan Mode — Mandatory Planning Protocol

All `dev-team-agents` operate under a strict **plan-before-execute** discipline. No non-trivial task may be executed without a prior approved plan.

---

## When a Plan Is Required

A plan is required whenever a task involves:

| Category | Examples |
|----------|---------|
| File operations | Creating, modifying, deleting, or moving any file |
| Commands with side effects | Installs, migrations, deploys, cache clears, git operations |
| Architecture or design decisions | Choosing tech stack, defining API contracts, schema design |
| Document generation | Backlog items, sprint plans, ADRs, code standards |
| Multi-step implementations | Any task with 2 or more sequential steps |
| Multi-agent delegations | Any task that spawns one or more subagents |

**A plan is NOT required for:**
- Answering a question
- Explaining or reading existing code
- Showing a file's contents or grep results
- Single-character / single-line typo fixes explicitly requested

When in doubt: **write the plan**.

---

## Plan Format

**Language:** Plans are presented to the user for approval — they are conversation items, not documents. Present plans in the user's preferred language from `.dev-team-agents/resolved/preferences.json` → `language` (default: English).

Load `.dev-team-agents/templates/plan-template.md` and fill it in. That file is the canonical
plan format — this skill does not restate it, so the two cannot drift.

Two rules the template encodes, restated here only because they change how you *execute*:

- The **Par.** column groups steps that can run simultaneously. Steps sharing a letter are sent as
  simultaneous agent prompts in a single message; `---` means the step must wait for the previous one.
- The plan ends with the approval closer. Present it verbatim from the template and then stop.

Plans render as **pure markdown** — no box-drawing characters or decorative symbols, per
`skills/shared/output-format/SKILL.md`.

---

## Approval Protocol

**Formatting rule — the plan and the approval question are two separate messages, never one.** First, output the filled `plan-template.md` as plain markdown chat text — headings, tables, and line breaks intact. Only after that, if using `AskUserQuestion` to collect approval, send the short **"Plan approval gate"** pattern from `skills/shared/interaction-patterns/SKILL.md` (question: "Plan ready. Do you approve?", options: Approved / Adjust first / Cancel). Never paste the plan body — or any part of the Steps table — into the `question`, `header`, or option `description` fields; those fields collapse line breaks and render the plan as an unreadable wall of text.

After presenting the plan:

1. **Stop.** Do not execute any step.
2. **Wait** for an explicit approval signal from the user — either a plain-text reply or the "Plan approval gate" quiz above.
3. **Approval signals**: "approved", "go ahead", "proceed", "yes", "looks good", "do it", or selecting "Approved — proceed"
4. **Rejection signals**: any feedback, correction, question, "no", or selecting "Adjust first" / "Cancel"

On **rejection**: acknowledge the feedback, adjust the plan, re-present the full plan. Never partially execute before replanning.

On **approval**: execute steps in order (agents with Execution Strategy Gate enabled MUST present the gate before executing). Report progress after each step per the **Progress Reporting** rule below. If execution reveals a problem that changes the plan, **stop and replan** before continuing.

---

## Progress Reporting

After finishing each step of an approved plan — whether executed directly or delegated to a subagent — send the user a short status update as its own chat message, in the user's preferred language from `preferences.json` → `language`. Pure markdown, no box-drawing characters, per `skills/shared/output-format/SKILL.md`.

A plan's steps are not only ones the agent drafts on its own: when the user hands over their own itemized list of activities (e.g. "do X, Y, Z"), that list falls under the "Multi-step implementations" trigger in *When a Plan Is Required* above — it still must be formalized into `plan-template.md`'s Steps table before execution, with the user's items becoming the steps. Once formalized and approved, this Progress Reporting rule applies exactly the same regardless of whether the steps originated from the agent's own plan or the user's own checklist.

Format (per-step update):

```
✅ Step {step_number}/{step_total} done: {step title/description from the plan}
⏱️ Time spent: {duration for this step, e.g. "3m 42s"}

Pending {done_total}/{steps_total}:
  [x] {completed step title} ({its time spent})
  [x] {completed step title} ({its time spent})
  [] {not-yet-done step title}
  [] {not-yet-done step title}
```

Closing format (after the last step):

```
✅ Plan complete
⏱️ Total time: {sum of every step's time spent}

All {step_total} steps done. Nothing pending.
```

Rules:

- Track each step's start time when execution begins and compute the duration when it finishes — do not guess or omit it.
- The checklist under `Pending {done_total}/{steps_total}` always lists **every** step in plan order, not just what remains: `[x]` with its elapsed time for steps already done, `[]` for steps not yet done. `done_total` is the count of `[x]` lines; `steps_total` equals `step_total`.
- Send this update immediately after each step completes, before starting the next one. Do not batch multiple steps into a single update.
- When the last step finishes, send the closing format instead of the per-step format — never a checklist on the closing message.
- In multi-agent execution, this reporting duty belongs to the orchestrating (main) agent, not each subagent — a subagent's own completion is one input to the main agent's update, not a separate message to the user. This is independent of, and does not replace, the periodic check-in on background subagents defined in `skills/shared/work-feedback/SKILL.md`.
- **Relationship to `work-feedback`**: the two do not compete — they report at different granularities. Progress Reporting fires **between** steps, once per step, when a step finishes. `work-feedback` fires **within** a step, on its own interval, only while that step's work is delegated to background subagents. A single background step can produce several `work-feedback` tables (one per poll tick) before it completes and produces exactly one Progress Reporting update. Never substitute one for the other, and never suppress a step's Progress Reporting update because `work-feedback` already reported on it — they are separate messages for separate audiences of the same work.

---

## Task List Mirroring

An approved plan's steps also live in your provider's **native task list**. That list is what the
desktop app's task board reads (`docs/specs/task-board.md`): a plan kept only in chat or in a file
never reaches it.

| Tool | Provider | Update model | Drop a step |
|------|----------|--------------|-------------|
| `TaskCreate` / `TaskUpdate` | Claude Code | One task per step; later changes by the id `TaskCreate` returned | `TaskUpdate` with status `deleted` |
| `TodoWrite` (only where `TaskCreate` is unavailable) | Claude Code | Whole list on every call | Omit it from the list |
| `update_plan` | Codex | Whole list on every call | Omit it from the list |
| `todowrite` | opencode | Whole list on every call; each step with `id: "step-N"` and `priority: "medium"` | Omit it from the list |

- **When** — create the list once the plan is approved **and** the Execution Strategy Gate (if it
  applies) has cleared, immediately before step 1; never before, so a rejected or cancelled plan
  leaves no task behind. Where the rendered body has no plan gate, the start of execution is the
  approval.
- **One task per Steps row**, in plan order, titled `Step N: <action>`, all `pending`. Name a secret
  by its variable, never by its value: step titles are stored on this machine for good.
- **Titles and ids are frozen.** The board recognises a step by its exact text (and by `id` on
  opencode): never rename or renumber a step once created. A replan keeps the original numbers (see
  § Replanning During Execution); new steps take the next unused `N`; dropped steps are removed as
  the table says; finished steps are left exactly as they are.
- **Moving** — the first step, or every step of the first **Par.** group, goes `in_progress` when
  execution starts. When a step finishes, mark it `completed` and whatever starts next `in_progress`
  in the same update (one call on a whole-list tool), then send its Progress Reporting message. A
  **Par.** group moves together: all its steps `in_progress` at once, each `completed` as it returns.
- **One list per plan** — on a whole-list tool (`TodoWrite`, `update_plan`, `todowrite`) the mirrored
  list is the only list until the plan ends: every call sends it whole. Scratch sub-steps go into a
  step's own work or a subagent, never into a call that would replace this list.
- **Owner** — the orchestrating agent keeps the list, as it owns Progress Reporting. A subagent
  handed a slice of an approved plan creates **no** list; it keeps one only for a plan it presented
  and had approved itself.
- **Reviews** — a step that runs a review or QA pass needs nothing extra to enter In Review. Its
  findings leave In Review only through a fix list: add them as new steps through a replan, so the
  board sees tasks created after the result. A review or QA pass's **own** plan is not mirrored — it
  would count as finished work in the next review.
- **Aborted run** — if the user cancels mid-execution or the run is abandoned, drop every step not
  yet `completed`, as the table says, so no pending task outlives the plan.

---

## Execution Strategy Gate

This optional gate applies between plan approval and execution. When an agent's configuration mandates it, the agent MUST present an interactive quiz after the user approves the plan and before executing any step.

### Trigger

After the user signals approval ("approved", "go ahead", "proceed", "yes", "looks good", "do it"), **before** executing step 1.

### Procedure

1. Read the worktree preferences from `.dev-team-agents/resolved/preferences.json`:
   ```bash
   python3 -c "import json;d=json.load(open('.dev-team-agents/resolved/preferences.json'));print(json.dumps({k:d.get(k) for k in['worktree_active','worktree_base_branch','worktree_path','worktree_docker_isolate']}))" 2>/dev/null
   ```
   If the file is unreadable or keys are absent, assume defaults: `worktree_active=true`, `worktree_base_branch` = auto-detected default, `worktree_path=.worktrees`, `worktree_docker_isolate=true`.

2. Determine the recommended option:
   - `worktree_active == true` → recommend **Isolated worktree** (first option)
   - `worktree_active == false` → recommend **New branch** (second option)
   - key absent → recommend **Isolated worktree** (first option)

3. Present the quiz using the `AskUserQuestion` tool. Use the user's preferred language from `preferences.json` → `language`. The recommended option MUST be the first option with the label showing it is recommended.

   Quiz structure (pt-BR example):
   ```json
   {
     "questions": [
       {
         "question": "Como este plano deve ser executado?",
         "header": "Estratégia",
         "multiSelect": false,
         "options": [
           { "label": "Worktree isolada (Recomendado)", "description": "Criar uma worktree git isolada com base em <base_branch>, em <worktree_path>, com Docker isolado=<sim/nao>" },
           { "label": "Nova branch", "description": "Criar uma nova branch a partir da branch atual e executar nela" },
           { "label": "Branch atual", "description": "Executar diretamente na branch atual, sem alteracoes git" },
           { "label": "Outro", "description": "Especificar outra abordagem manualmente" }
         ]
       }
     ]
   }
   ```
   Translate to the user's language. Dynamically interpolate the actual `worktree_base_branch`, `worktree_path`, and `worktree_docker_isolate` values into the recommended option's description.

4. Options and corresponding actions:

   | User choice | Action |
   |---|---|
   | **Isolated worktree** | Load `skills/shared/worktree/SKILL.md` and follow the full worktree setup flow. Use `worktree_base_branch` as the base, `worktree_path` for the worktree root, and `worktree_docker_isolate` to determine Docker isolation. |
   | **New branch** | Ask for a branch name (suggest `<context>/<brief-title>`), then run `git checkout -b <name>`. Continue executing steps in the new branch. |
   | **Current branch** | Proceed executing steps directly on the current branch with no git changes. |
   | **Other** | Ask the user to describe their desired approach in free text, then adapt accordingly. |

5. Announce the chosen strategy before executing the first step so the user can verify the decision is correct.

---

## Replanning During Execution

If you discover mid-execution that a step cannot be done as planned:

1. Stop immediately.
2. Describe what was found and why the original plan needs to change.
3. Present an updated plan covering only the remaining steps, keeping their original step numbers;
   new steps continue from the next unused number (§ Task List Mirroring depends on it).
4. Wait for approval again before continuing — the new steps' tasks are created only then.

**Do not silently improvise.** If the plan changes, the user must know.

---

## Agents Must Self-Enforce

Every agent in `dev-team-agents` is responsible for applying this protocol independently. The plan-mode rule is not optional and is not enforced by an external system — it is part of each agent's operating discipline.

If a user asks an agent to "just do it" without a plan: explain that the plan takes less than a minute to write, protects against misunderstandings, and produces better results. Then write the plan. Never skip it.

---

## Context Self-Monitoring

After any response that involved reading many large files, producing long outputs, or running multiple tool calls in sequence, add a brief context advisory when appropriate:

> ⚡ **Context advisory**: this session has accumulated significant context. If responses start feeling less precise, run `/compact` or start a fresh session before the next task.

Apply this judgment after: reading 5+ files, producing 3+ large tool outputs, or a long back-and-forth session. You cannot see the exact percentage — err toward mentioning it. This supplements the automated hook-based warning, which fires based on a transcript token estimate.
