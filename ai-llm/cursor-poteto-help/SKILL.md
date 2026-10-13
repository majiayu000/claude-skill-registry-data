---
name: cursor-poteto-help
description: Guides explicit questions about pstack setup, $cursor-poteto-mode, and choosing a skill, playbook or principle; answer with source links and a native Codex prompt without starting help-only work.
---

# Poteto help

Answer the user's question about pstack, hand them a prompt they can send, and link the file the answer came from. For a help question, don't start the work. The user asked how, and a pstack run spends real tokens, so let them send the prompt.

A message that asks for work, such as "use pstack to fix this bug", is not a help question. Read [`poteto-mode`](../cursor-poteto-mode/SKILL.md), do the work under it, and keep the distinction between answering a help question and executing an action request.

This file maps questions to the skills and guide pages that hold the answers. Read the native skill or bundled [Codex guide](references/guide/README.md) before answering. The pinned upstream guide remains provenance; its Cursor setup and runtime commands do not override native guidance. Use reviewed public mirror links when sharing these adapted files.

## Find out what they need

Infer the need from the message and the conversation. A named situation, such as "which skill reviews a PR?", goes straight to its section. If the need is still unclear, ask one multiple-choice question with these options, then answer only the section they pick:

- Get set up
- Start a task with `$cursor-poteto-mode`
- Pick a skill for a situation
- Fix a run that went wrong
- Make pstack my own

Check the state that changes the answer, and mention it only when it does:

- Read the standing `model-capability-router` and native task metadata when model selection changes the answer; absence of a Cursor rule says nothing about Codex setup.
- No `verify-*` skill or other app harness in the project means agents have no scripted way to drive the app. Mention `$cursor-create-verification-skill` when the question is about proving a change works.

When the model rule is missing and it matters, ask whether the user wants to pick a model for each role and a reasoning budget now. It matters when the user is new, the question is about setup or cost, or the answer depends on which models run. Ask at most once per chat. If the need is also unclear, ask both questions together. Offer two choices:

- Now: give them `$cursor-setup-pstack` to type, and answer their question too.
- Later: answer their question, and add one line saying the current native model selection remains unchanged until they run `$cursor-setup-pstack`.

## Get set up

Use the existing Codex adaptation and verified installed skill names; source publication is separate from installation. Installing or altering live skills requires operator authorization. Run `$cursor-setup-pstack` when model-role setup is requested; it follows `model-capability-router` and actual native capabilities. State the goal and a pass/fail completion check when invoking `$cursor-poteto-mode`.

Native roles and configured defaults are not proof of a running model. Keep review independence and panel responsibilities; choose available models and effort from native routing rather than Cursor slugs. Smaller panels and suitable effort can reduce work, but no measured token saving is claimed. Cursor cloud agents, Custom Modes and `/loop` are not available merely because these skills are mirrored.

## Start a task with `$cursor-poteto-mode`

`$cursor-poteto-mode` matches the task to a playbook, copies the playbook's steps into the todo list, and runs the other skills as the steps need them. A step it skips stays in the list as `skip: <reason>`. A good prompt states the goal and how to tell it's done. It doesn't list skills, because a hand-written sequence tends to drop or reorder steps the playbook would keep. Read [`references/prompting.md`](references/prompting.md) before you help word one. [Guide page 2](references/guide/02-poteto-mode.md) has examples.

In Codex, invoke `$cursor-poteto-mode` for the selected task and preserve it through that task's follow-ups. Cursor Custom Modes, Option+Enter/Alt+Enter and sticky per-turn loading are not Codex guarantees. Do not claim a native sticky mode exists without host proof. For a new task, explicitly select the skill again when needed. The named native `poteto-agent` reads the complete mode and principles before work; do not substitute a generic worker for that role.

## Pick a skill

The default answer is `$cursor-poteto-mode`, which runs most of the others when its steps need them. Name a skill directly when the user wants more or less of something than the playbook gives. Read the skill before you recommend it, and give one example prompt.

| The user wants to | Skill |
|---|---|
| Do any non-trivial task with rigor | [`$cursor-poteto-mode`](../cursor-poteto-mode/SKILL.md) |
| Know how code works now, or where new code should live | [`$cursor-how`](../cursor-how/SKILL.md) |
| Know why code is shaped this way, or where a number came from | [`$cursor-why`](../cursor-why/SKILL.md) |
| Understand a change or subsystem, explained plainly | [`$cursor-teach`](../cursor-teach/SKILL.md) |
| Catch up on their own recent work on a topic | [`$cursor-recall`](../cursor-recall/SKILL.md) |
| Know what a small diff could break outside itself | [`$cursor-blast-radius`](../cursor-blast-radius/SKILL.md) |
| Settle types and module shape before code that crosses a function boundary | [`$cursor-architect`](../cursor-architect/SKILL.md) |
| Get several attempts at one brief, merged into the best one | [`$cursor-arena`](../cursor-arena/SKILL.md) |
| Run parallel checks over slices, or race workers, as cloud agents | [`$cursor-swarm`](../cursor-swarm/SKILL.md) |
| Have different models review a diff and try to break it | [`$cursor-interrogate`](../cursor-interrogate/SKILL.md) |
| Fix a bug test-first when a cheap local test exists | [`$cursor-tdd`](../cursor-tdd/SKILL.md) |
| Apply TypeScript rules to `.ts` or `.tsx` work | [`$cursor-typescript-best-practices`](../cursor-typescript-best-practices/SKILL.md) |
| Strip comments before review, using a reviewer that didn't write them | [`$cursor-no-comments`](../cursor-no-comments/SKILL.md) |
| Clean AI tells out of prose | [`$cursor-unslop`](../cursor-unslop/SKILL.md) |
| Write docs, an RFC, a README, a PR description, or a commit message to a standard | [`$cursor-technical-writing`](../cursor-technical-writing/SKILL.md) |
| Hear the last reply again in plain words | [`$cursor-bro`](../cursor-bro/SKILL.md) |
| Give agents a scripted way to drive the app and prove behavior | [`$cursor-create-verification-skill`](../cursor-create-verification-skill/SKILL.md) |
| Bring a verification skill and its feature map back in line with the app | [`$cursor-maintain-verification-skill`](../cursor-maintain-verification-skill/SKILL.md) |
| Vet a performance number before reporting or acting on it | [`$cursor-benchmark-checklist`](../cursor-benchmark-checklist/SKILL.md) |
| Run a large or cross-cutting change, or one to review after stepping away | [`$cursor-figure-it-out`](../cursor-figure-it-out/SKILL.md) |
| Keep a decision log during a run, and review it afterward | [`$cursor-show-me-your-work`](../cursor-show-me-your-work/SKILL.md) |
| Pick a model for each role and a reasoning budget | [`$cursor-setup-pstack`](../cursor-setup-pstack/SKILL.md) |
| Turn their own working habits into a personal mode skill | [`$cursor-automate-me`](../cursor-automate-me/SKILL.md) |
| Turn what a finished task taught into skill edits | [`$cursor-reflect`](../cursor-reflect/SKILL.md) |
| Stop agents from repeating the same mistakes in this repo | [`$cursor-correct`](../cursor-correct/SKILL.md) |
| Build a page whose buttons wake a Grok Bot over a webhook | [`/make-bot-ui`](https://github.com/cursor/plugins/blob/c1c0a32802223f4be824112dd83d33ad29a8b26c/pstack/skills/make-bot-ui/SKILL.md) |
| Find their way around pstack | `$cursor-poteto-help` |

If a skill directory next to this one is missing from the table, read its frontmatter and route by its description. The `principle-*` directories are covered under principles below.

Close calls:

- `$cursor-how` explains what the code does. `$cursor-why` explains the reasons. `$cursor-teach` runs one or both and explains the result plainly.
- `$cursor-arena` gives every worker the same brief and merges the best parts. `$cursor-swarm` splits work into slices or a race and returns one report.
- `$cursor-architect` implements right after it settles the design. Add "with checkpoint" to review the design before it writes code.
- `$cursor-interrogate` reviews the diff. `$cursor-blast-radius` looks for breakage outside the diff and proves the one fact that makes the change safe.
- `$cursor-recall` rebuilds context across recent chats. Resuming one specific chat or branch is the Session pickup playbook.
- `$cursor-figure-it-out` designs one rigorous run. The Orchestrate playbook runs a program that spans days and many PRs. The Autonomous run playbook drives one task to a finish condition.

Not in pstack:

- `$cursor-deslop`, `control-cli`, and `control-ui` ship in the `cursor-team-kit` plugin.
- Cursor `/loop` maps only to explicitly requested native automation; authoring uses native `skill-creator`. Neither is installed or scheduled by this help skill.
- pstack has no `$cursor-orchestrate` skill. Orchestrate is a `$cursor-poteto-mode` playbook. If the slash menu shows `$cursor-orchestrate`, another plugin provides it.

## Playbooks and principles

Playbooks are step lists inside `$cursor-poteto-mode`, not skills, so they have no slash command. Inside `$cursor-poteto-mode`, describing the task picks one, and these phrases name one directly:

- "babysit this pr" or "check on pr 123" runs Babysit. It drives the PR to merge-ready and stops there. It doesn't merge unless the user asks to merge, land, or ship.
- "land the stack" runs Shipping.
- "take over this branch" runs Session pickup.
- "pause safely" runs Pause safely.
- "full autopilot on this queue" runs Autopilot-full. "stack them, don't ship" runs Autopilot-stack.
- "run the eval playbook" runs Eval.

Without `$cursor-poteto-mode`, a phrase such as "babysit this pr" can start the host's own workflow for the same job instead. The Playbooks section of [`poteto-mode`](../cursor-poteto-mode/SKILL.md) lists every playbook and when it applies. [Guide page 6](references/guide/06-verify-and-ship.md) covers opening, babysitting, and landing a PR.

pstack has no planning skill. Native Codex planning works alongside it. For work that spans phases or stacked PRs, asking `$cursor-poteto-mode` for a plan runs the [Multi-phase plan playbook](../cursor-poteto-mode/playbooks/multi-phase-plan.md), which writes the plan and doesn't implement it. For a design question, the Prototype playbook or `$cursor-architect` settles it in code first.

Principles are one-rule skills that `$cursor-poteto-mode` reads and cites in its replies. The user rarely invokes one. They steer with the names instead, as in "apply prove it works. show me the real output." Explicitly invoke the corresponding `$cursor-principle-<name>` skill when available. [Guide page 8](references/guide/08-principles.md) lists them.

## Fix a run that went wrong

| Symptom | Fix |
|---|---|
| The mode stopped applying after a few turns | Explicitly invoke `$cursor-poteto-mode` for the selected task; Cursor Custom Mode persistence is not a Codex guarantee. |
| A question got treated as the next step of the last task | Say "new task", or say the turn doesn't need the mode. |
| A new model choice had no effect | Check the actual native session selection; a changed default is not proof an existing task switched. |
| Runs cost more than expected | See the cost paragraph under Get set up. |
| A skill didn't load on its own | Respect each skill's native invocation policy; this help skill is explicit-only. Automatic selection is not established by source publication. |
| Parallel agents overwrote each other | Give each agent its own worktree, use separately authorized native cloud tasks only when actually supported. |
| An overnight run moved but finished nothing | A requested native continuation needs a check that can pass or fail, not a duration. See [guide page 7](references/guide/07-overnight.md). |
| The reply claims success from a green build | Ask for the real command, flow, stored value, or profile. That's the prove-it-works principle. |

For a run that drifts, [`references/prompting.md`](references/prompting.md) has one-line steers. [Guide page 10](references/guide/10-recipes-and-pitfalls.md) has more pitfalls and the recipes worth copying.

## Make pstack my own

- [`$cursor-automate-me`](../cursor-automate-me/SKILL.md) drafts a personal mode skill from the user's own history, to use alongside `$cursor-poteto-mode`.
- [`$cursor-reflect`](../cursor-reflect/SKILL.md) after a session turns its lessons into skill edits the user approves.
- `$cursor-poteto-mode write a skill for <workflow>` runs the authoring playbook. The eval playbook tests a skill change blind.
- Fix a misbehaving skill in its own PR, not inside the feature work where it went wrong.

[Guide page 9](references/guide/09-make-it-yours.md) covers each of these.

## Reply

Lead with the answer. Give at most one example prompt in a code block, adapted from [`references/recipes.md`](references/recipes.md) when one fits, then the link to that file. Keep it short unless the user asked for the whole map.
