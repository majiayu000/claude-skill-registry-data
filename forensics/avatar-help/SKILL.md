---
name: avatar-help
description: Aang showing a new friend around the team. Explains Team Avatar to a user, the roster and who owns what, how to invoke a skill on Claude Code and Codex, which skill fits a situation, and how to word a good prompt. Use for /avatar-help, "how do I use team avatar", "which skill should I use", "what can the team do", or a question about setup, routing, or a run that went wrong.
---

# Avatar help

When someone new arrives at the Air Temple, Aang does not hand them a scroll. He shows them around, introduces the team, and lets them try. Answer the user's question about Team Avatar, hand them a prompt they can send, and link the file the answer came from.

For a help question, do not start the work. The user asked how, and a Team Avatar run spends real tokens, so let them send the prompt. A message that asks for work, such as "use team avatar to fix this bug", is not a help question. Read [`avatar-mode`](../avatar-mode/SKILL.md) and do the work under it.

This file maps questions to the skills that own the answers. Read the matching skill before answering. Its instructions take precedence over this map. The local links point into the installed plugin, so give the user the public copy: `https://github.com/tmcfarlane/team-avatar/blob/main/plugins/team-avatar/` followed by the file's path relative to the plugin root.

On Codex, read [avatar-mode/references/codex.md](../avatar-mode/references/codex.md) for tool equivalents.

## Find out what they need

Infer the need from the message and the conversation. A named situation, such as "which skill reviews a PR?", goes straight to its section. If the need is still unclear, ask one multiple-choice question with these options, then answer only the section they pick.

- Meet the team
- Get set up
- Start a task with `avatar-mode`
- Pick a skill for a situation
- Fix a run that went wrong
- Make Team Avatar my own

Check the state that changes the answer, and mention it only when it does.

- For a model or routing question, identify the runtime (Claude Code or Codex) and the install type (plugin or skills-only). Then print the sheet with `sh <plugin>/skills/avatar-setup/scripts/show-sheet.sh claude` (or `codex`) before you say whether defaults or the user's choices apply.
- A project with no `verify` or `verify-*` skill and no app harness gives agents no scripted way to drive the app. Mention `vital-signs` when the question is about proving a change works.

When the sheet is missing and it matters, ask whether the user wants to pick a model per character and a default effort now. It matters when the user is new, the question is about setup or cost, or the answer depends on which models run. Ask at most once per chat. If the need is also unclear, ask both questions together. Offer two choices.

- Now. Give them the `avatar-setup` invocation for their runtime, and answer their question too.
- Later. Answer their question, and add one line saying every character keeps its default model until they run `avatar-setup`.

## Meet the team

Each character owns one discipline, and each skill belongs to one character. Aang routes the work through `avatar-mode`. The roster, with every skill, is the team table in [`avatar-mode`](../avatar-mode/SKILL.md#the-team).

| Character | Ask them for |
|-----------|--------------|
| Aang | Routing a task, history and rationale, catching up, setup, and this help |
| Sokka | Plans, architecture decisions, decision trails, and tools that automate the user's habits |
| Toph | How code works, and blunt review of a diff or a design. Read-only. She never edits. |
| Katara | Bugs, tests, CI, and cleaning code before review |
| Zuko | Performance, forensics, incidents, and bakeoffs between designs |
| Iroh | Writing, teaching, and writing or testing skills |
| Appa | Carrying a plan to a merged PR: refactors, opening PRs, babysitting, landing, pausing and resuming |
| Momo | Throwaway prototypes that settle a design question by observation, and quick small tasks |
| Suki | Parallel squads, long autonomous runs, and queues of PRs |

Each character is also a subagent. On Claude Code it is `team-avatar:<character>`. On Codex, `avatar-mode` dispatches a `spawn_agent` that reads the character's file, as [codex.md](../avatar-mode/references/codex.md#dispatching-a-character) describes.

## Get set up

1. Identify the runtime and install type, then give the matching install command from the plugin [README](https://github.com/tmcfarlane/team-avatar/blob/main/plugins/team-avatar/README.md#install).
2. Read [`avatar-setup`](../avatar-setup/SKILL.md) before you explain model choices, effort, where the sheet lives, or automatic routing. The plugin's SessionStart hook routes nontrivial work into `avatar-mode`. To turn it off, set `session hook: off` in the runtime's sheet. Codex runs the hook only after the user trusts it through `/hooks`. A skills-only install has no hook.
3. Offer a first task prompt with a goal and a check that can pass or fail, per [references/prompting.md](references/prompting.md), in the runtime's invocation syntax below.

**How to invoke a skill.**

| Runtime | Start avatar mode | Call one skill | Dispatch a character |
|---------|-------------------|----------------|----------------------|
| Claude Code | `/team-avatar:avatar-mode <task>`, or ask for "avatar mode" in words | `/team-avatar:<skill>`, for example `/team-avatar:healing-water` | The `Agent` tool with `subagent_type: "team-avatar:<character>"` |
| Codex | `$avatar-mode <task>` | `$<skill>`, for example `$earth-rumble` | `spawn_agent`, which needs `multi_agent = true` under `[features]` in `~/.codex/config.toml` |

If cost is the worry, say where the tokens go and how to spend less. Team Avatar spends extra tokens on dispatched characters and review panels. Rerun `avatar-setup` and pick a lower `default effort` or cheaper models. A line set to `inherit` runs on the chat's model, which costs less when the chat runs a cheaper one. A shorter `panel` list runs fewer runners, one per entry. Save `avatar-mode` for work that needs rigor.

## Start a task with `avatar-mode`

`avatar-mode` matches the task to a skill, copies that skill's steps into the todolist, and runs the other skills as the steps need them. A step it skips stays in the list as `skip: <reason>`. A good prompt states the goal and how to tell it is done. It does not list skills, because a hand-written sequence tends to drop or reorder steps the skill would keep. Read [references/prompting.md](references/prompting.md) before you help word one.

Check that the hook is on for this install before promising automatic routing. Without it, invoke `avatar-mode` for each new task. Mid-chat, "new task" makes it match a fresh skill. For dispatch defaults, read [Dispatching a character](../avatar-mode/SKILL.md#dispatching-a-character) and, on Codex, the codex.md mapping.

## Pick a skill

The default answer is `avatar-mode`, which runs most of the others when its steps need them. Name a skill directly when the user wants more or less of something than the route gives. Read the skill before you recommend it, and give one example prompt. The full route table is [Route the task](../avatar-mode/SKILL.md#route-the-task).

| The user wants to | Skill |
|-------------------|-------|
| Do any nontrivial task with rigor | [`avatar-mode`](../avatar-mode/SKILL.md) |
| Check the agent understood the goal before it starts | [`what-you-seek`](../what-you-seek/SKILL.md) |
| Aim a task higher before starting | [`sharpen-the-sword`](../sharpen-the-sword/SKILL.md) |
| Know how code works now, or where new code should live | [`seismic-sense`](../seismic-sense/SKILL.md) |
| Know why code is shaped this way, or where a number came from | [`past-lives`](../past-lives/SKILL.md) |
| Understand a change or subsystem, explained plainly | [`white-lotus`](../white-lotus/SKILL.md) |
| Catch up on their own recent work on a topic | [`spirit-world`](../spirit-world/SKILL.md) |
| Catch up on what changed in this chat since their last message | [`iceberg-wake`](../iceberg-wake/SKILL.md) |
| Know what a small diff could break outside itself | [`my-cabbages`](../my-cabbages/SKILL.md) |
| Settle types and module shape before code that crosses a function boundary | [`war-room`](../war-room/SKILL.md) |
| Get several attempts at one brief, merged into the best one | [`agni-kai`](../agni-kai/SKILL.md) |
| Run parallel checks over slices, or race workers | [`kyoshi-formation`](../kyoshi-formation/SKILL.md) |
| Have different models review a diff and try to break it | [`lie-detector`](../lie-detector/SKILL.md) |
| Review a diff for bugs, breaking changes, and security | [`earth-rumble`](../earth-rumble/SKILL.md) |
| Audit code quality and structure | [`metalbending`](../metalbending/SKILL.md) |
| Fix a bug | [`healing-water`](../healing-water/SKILL.md) |
| Fix a bug test-first when a cheap local test exists | [`push-and-pull`](../push-and-pull/SKILL.md) |
| Get red CI green | [`heal-ci`](../heal-ci/SKILL.md) |
| Apply TypeScript rules to `.ts` or `.tsx` work | [`typescript-forms`](../typescript-forms/SKILL.md) |
| Strip comments before review, with a reviewer who did not write them | [`clear-water`](../clear-water/SKILL.md) |
| Clean AI slop out of code | [`purify`](../purify/SKILL.md) |
| Write docs, an RFC, a README, a PR description, or a commit message, or clean AI tells out of prose | [`tea-time`](../tea-time/SKILL.md) |
| Hear the last reply again in plain words | [`plain-talk`](../plain-talk/SKILL.md) |
| Give agents a scripted way to drive the app and prove behavior | [`vital-signs`](../vital-signs/SKILL.md) |
| Bring a verification skill back in line with the app | [`checkup`](../checkup/SKILL.md) |
| Fix slowness, memory, or cost | [`breath-of-fire`](../breath-of-fire/SKILL.md) |
| Vet a performance number before reporting or acting on it | [`steady-flame`](../steady-flame/SKILL.md) |
| Push one metric up over many measured iterations | [`dragon-dance`](../dragon-dance/SKILL.md) |
| Diagnose a live symptom or a captured profile | [`ember-trace`](../ember-trace/SKILL.md) |
| Match two UIs pixel for pixel | [`twin-flames`](../twin-flames/SKILL.md) |
| Handle an outage or write a postmortem | [`redemption-arc`](../redemption-arc/SKILL.md) |
| Stop agents from repeating the same mistakes in this repo | [`honor-code`](../honor-code/SKILL.md) |
| Prototype options to settle a design question | [`scouting-flight`](../scouting-flight/SKILL.md) |
| Refactor with no behavior change | [`steady-flight`](../steady-flight/SKILL.md) |
| Plan work that spans phases or stacked PRs | [`master-plan`](../master-plan/SKILL.md) |
| Run a large or cross-cutting change, or one to review after stepping away | [`day-of-black-sun`](../day-of-black-sun/SKILL.md) |
| Keep a decision log during a run, and review it afterward | [`battle-map`](../battle-map/SKILL.md) |
| List what they got done | [`war-journal`](../war-journal/SKILL.md) |
| Open a PR | [`yip-yip`](../yip-yip/SKILL.md) |
| Make a PR easier to review | [`light-load`](../light-load/SKILL.md) |
| Babysit a PR to merge-ready | [`long-flight`](../long-flight/SKILL.md) |
| Pull a PR's review comments | [`messenger-hawk`](../messenger-hawk/SKILL.md) |
| Resolve merge conflicts | [`clear-skies`](../clear-skies/SKILL.md) |
| Land a green stack | [`safe-landing`](../safe-landing/SKILL.md) |
| Pause work safely, or pick it back up | [`make-camp`](../make-camp/SKILL.md), [`break-camp`](../break-camp/SKILL.md) |
| Clean up old worktrees and simulators | [`shedding-season`](../shedding-season/SKILL.md) |
| Run a task until done without stopping | [`night-watch`](../night-watch/SKILL.md) |
| Run a multi-day program of many PRs | [`kyoshi-command`](../kyoshi-command/SKILL.md) |
| Drive a queue of independent PRs on full autopilot | [`full-patrol`](../full-patrol/SKILL.md) |
| Build a queue of changes as one stack to land themselves | [`shield-wall`](../shield-wall/SKILL.md) |
| Write or change a skill | [`new-scroll`](../new-scroll/SKILL.md) |
| Test a skill or prompt change before promoting it | [`pai-sho`](../pai-sho/SKILL.md) |
| Pick a model per character and a default effort | [`avatar-setup`](../avatar-setup/SKILL.md) |
| Turn their own working habits into a personal mode skill | [`invention-workshop`](../invention-workshop/SKILL.md) |
| Turn what a finished task taught into skill edits | [`meditation`](../meditation/SKILL.md) |
| Steer by a principle | [`four-elements`](../four-elements/SKILL.md) |
| Find their way around Team Avatar | `avatar-help` |

If a skill directory next to this one is missing from the table, read its frontmatter and route by its description.

Close calls:

- `seismic-sense` explains what the code does. `past-lives` explains the reasons. `white-lotus` runs one or both and explains the result plainly.
- `agni-kai` gives every runner the same brief and merges the best parts. `kyoshi-formation` splits work into slices or a race and returns one report.
- `war-room` implements right after it settles the design. Add "with checkpoint" to review the design before it writes code.
- `lie-detector` reviews the diff with several models. `earth-rumble` is Toph's own deep review. `my-cabbages` looks for breakage outside the diff and proves the one fact that makes the change safe.
- `spirit-world` rebuilds context across recent chats. `iceberg-wake` covers only this chat since the user's last message. Resuming one specific chat or branch is `break-camp`.
- `day-of-black-sun` designs one rigorous run. `kyoshi-command` runs a program that spans days and many PRs. `night-watch` drives one task to a finish condition.
- `long-flight` drives a PR to merge-ready and stops there. It does not merge unless the user asks to merge, land, or ship, which is `safe-landing`.

Not in Team Avatar:

- `run` and `loop` ship with Claude Code. Team Avatar's skills use them where they exist. On Codex, codex.md names the equivalents.
- Claude Code's plan mode works alongside Team Avatar. For work that spans phases, `master-plan` writes the plan and does not implement it.

## Principles

Principles are one-rule entries that `avatar-mode` reads and cites in its replies. They live in [`four-elements`](../four-elements/SKILL.md), grouped by element. The user rarely invokes one. They steer with the names instead, as in "apply prove it works. show me the real output." The index in [`avatar-mode`](../avatar-mode/SKILL.md#principles) names each one and when it applies.

## Fix a run that went wrong

| Symptom | Fix |
|---------|-----|
| The mode stopped applying after a few turns | Check the hook through the sources under Get set up. Without it, invoke `avatar-mode` for each task. |
| A question got treated as the next step of the last task | Say "new task", or say the turn does not need the mode. |
| A new model choice had no effect | Print the sheet with `show-sheet.sh`, and run `check-sheet.sh` on it. Check that it sits at the runtime's path in [`avatar-setup`](../avatar-setup/SKILL.md#where-the-sheet-lives). |
| Runs cost more than expected | See the cost paragraph under Get set up. |
| A skill did not load on its own | Read its description and invoke it explicitly. `avatar-mode` does not run every skill. |
| Parallel agents overwrote each other | Give each writer its own worktree. |
| An overnight run moved but finished nothing | Read [`night-watch`](../night-watch/SKILL.md) and give the run a check that can pass or fail. For a queue, read `full-patrol` or `shield-wall`. |
| The reply claims success from a green build | Ask for the real command, flow, stored value, or profile. That is Prove It Works, Earth in `four-elements`. |
| A project playbook stopped applying after an upgrade | Run `node <plugin>/skills/avatar-mode/scripts/check-playbooks.mjs` from the repository root and fix each line it prints. |

For a run that drifts, [references/prompting.md](references/prompting.md) has one-line steers, and [references/recipes.md](references/recipes.md) has prompts to adapt.

## Make Team Avatar your own

- `invention-workshop` drafts a personal mode skill from the user's own history, to use alongside `avatar-mode`.
- `meditation` after a session turns its lessons into skill edits the user approves.
- `new-scroll` writes a skill for a workflow. `pai-sho` tests a skill change blind.
- A repository can extend any skill with a project playbook under `.agents/playbooks/`. See [Project playbooks](../avatar-mode/SKILL.md#project-playbooks).
- Fix a misbehaving skill in its own PR, not inside the feature work where it went wrong.

## Reply

Lead with the answer. Give at most one example prompt in a code block, adapted from [references/recipes.md](references/recipes.md) when one fits, in the user's runtime syntax, then the link to the file the answer came from. Keep it short unless the user asked for the whole map.
