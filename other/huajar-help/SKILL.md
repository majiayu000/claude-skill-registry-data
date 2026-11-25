---
name: huajar-help
description: Guides users through huajar-stack setup, /huajar-stack:huajar-mode, and picking the skill, playbook, or principle for a task. Type /huajar-stack:huajar-help with a question.
disable-model-invocation: true
---

# Huajar help

In Claude Code, read [the Claude Code adapter](../../docs/harness/claude-code.md) once per session before you follow this skill. It maps the Cursor names in pstack skills to Claude Code.

Answer the user's question about huajar-stack, hand them a prompt they can send, and link the file the answer came from. For a help question, don't start the work. The user asked how, and a huajar-stack run spends real tokens, so let them send the prompt.

A message that asks for work, such as "use huajar-stack to fix this bug", is not a help question. Read [`huajar-mode`](../huajar-mode/SKILL.md), do the work under it, and mention once that the mode stays in context until a compaction drops part of it, so the user invokes `/huajar-stack:huajar-mode` again for a new task or after a long session.

This file maps questions to the skills and guide pages that hold the answers. Those files own the details. Read the file you route to before you quote it, and trust it when it disagrees with this map. The links here point into the installed plugin, which the user may not be able to open, so give the user the file's public copy: `https://github.com/huajar/huajar-stack/blob/main/` followed by its path.

## Find out what they need

Infer the need from the message and the conversation. A named situation, such as "which skill reviews a PR?", goes straight to its section. If the need is still unclear, ask one multiple-choice question with these options, then answer only the section they pick:

- Get set up
- Start a task with `/huajar-stack:huajar-mode`
- Pick a skill for a situation
- Fix a run that went wrong
- Make huajar-stack my own

Check the state that changes the answer, and mention it only when it does:

- No `~/.claude/rules/huajar-stack-models.md` means `/huajar-stack:setup-huajar-stack` hasn't run for this user, so every role uses its default model.
- No `verify-*` skill or other app harness in the project means agents have no scripted way to drive the app. Mention `/huajar-stack:create-verification-skill` when the question is about proving a change works.
- No formal verification skill in the project means no property is checked past what tests reach. Mention `/huajar-stack:create-formal-verification-skill` when the question is about a race, an invariant, or another case tests rarely hit. When one exists and the code it covers changed after the commit it records as last in sync, mention `/huajar-stack:maintain-formal-verification-skill` if the question touches that code.

When the model rule is missing and it matters, ask whether the user wants to pick a model for each role and a reasoning budget now. It matters when the user is new, the question is about setup or cost, or the answer depends on which models run. Ask at most once per chat. If the need is also unclear, ask both questions together. Offer two choices:

- Now: give them `/huajar-stack:setup-huajar-stack` to type, and answer their question too.
- Later: answer their question, and add one line saying every role keeps its default model until they run `/huajar-stack:setup-huajar-stack`.

## Get set up

1. Install from the shell with `claude plugin marketplace add huajar/huajar-stack`, then `claude plugin install huajar-stack@huajar-stack`. Inside a session, the same commands are `/plugin marketplace add huajar/huajar-stack` and `/plugin install huajar-stack@huajar-stack`, which opens the plugin in the `/plugin` panel to install it. `claude plugin list` then shows `huajar-stack@huajar-stack` as enabled. [Install plugins](https://code.claude.com/docs/en/plugins/install) has the details.
2. Run [`/huajar-stack:setup-huajar-stack`](../setup-huajar-stack/SKILL.md). It asks for a reasoning budget, maps a model to each role, and writes a rule. The rule applies to new chats. Then it offers once each to generate a verification skill and a formal verification skill for the project, unless the project already has one.
3. Start a real task with `/huajar-stack:huajar-mode`, a goal, and a check that can pass or fail.

Installing changes nothing until the user invokes a skill. Only `/huajar-stack:setup-huajar-stack` and the four team kit skills (`deslop`, `control-cli`, `control-ui`, `verify-this`) load from the user's words. The [README](../../README.md) and [guide page 1](../../docs/guide/01-setup.md) have the details. Offer to word their first prompt with them, per [`references/prompting.md`](references/prompting.md).

If cost is the worry, say where the tokens go and how to spend fewer. huajar-stack spends extra tokens on subagents and review panels. Rerun `/huajar-stack:setup-huajar-stack` and pick a smaller budget or cheaper models. A role set to `auto` or `inherit-parent` runs on the chat's model, which saves tokens when the chat runs on a cheaper model. A shorter panel list runs fewer subagents, one for each entry. Save `/huajar-stack:huajar-mode` for work that needs rigor.

huajar-stack is built for Claude Code. Its skills use the Agent Skills format, so other tools can read them. But most workflow skills, including `/huajar-stack:huajar-mode`, `/huajar-stack:how`, and `/huajar-stack:teach`, spawn Claude Code subagents with per-role models, so those parts may not work there.

## Start a task with `/huajar-stack:huajar-mode`

`/huajar-stack:huajar-mode` matches the task to a playbook, copies the playbook's steps into the todo list, and runs the other skills as the steps need them. A good prompt states the goal and how to tell it's done. It doesn't list skills, because a hand-written sequence tends to drop or reorder steps the playbook would keep. Read [`references/prompting.md`](references/prompting.md) before you help word one. [Guide page 2](../../docs/guide/02-huajar-mode.md) has examples.

Once the user invokes `/huajar-stack:huajar-mode`, its `SKILL.md` enters the conversation as one message and stays there across later turns. After a compaction, only part of it may be re-attached, and older skills can drop. So the user invokes `/huajar-stack:huajar-mode` again for a new task or after a long session.

Link [Claude Code's skills docs](https://code.claude.com/docs/en/skills) when this comes up. Mid-chat, "new task" makes the mode match a fresh playbook. `/huajar-stack:huajar-mode` already uses `huajar-agent` for the subagents its playbook steps spawn. To get the same style from a subagent of your own, spawn it with `subagent_type: "huajar-stack:huajar-agent"`.

## Pick a skill

The default answer is `/huajar-stack:huajar-mode`, which runs most of the others when its steps need them. Name a skill directly when the user wants more or less of something than the playbook gives. Read the skill before you recommend it, and give one example prompt.

| The user wants to | Skill |
|---|---|
| Do any non-trivial task with rigor | [`/huajar-stack:huajar-mode`](../huajar-mode/SKILL.md) |
| Check that the agent understood their goal and the problem before it starts | [`/huajar-stack:in-your-own-words`](../in-your-own-words/SKILL.md) |
| Get a prompt rewritten deeper, not bigger, before sending it: what a top professional would add, their raw material and methods, and an outside check. It returns the prompt and doesn't do the task | [`/huajar-stack:sharpen`](../sharpen/SKILL.md) |
| Know how code works now, or where new code should live | [`/huajar-stack:how`](../how/SKILL.md) |
| Know why code is shaped this way, or where a number came from | [`/huajar-stack:why`](../why/SKILL.md) |
| Understand a change or subsystem, explained plainly | [`/huajar-stack:teach`](../teach/SKILL.md) |
| Catch up on their own recent work on a topic | [`/huajar-stack:recall`](../recall/SKILL.md) |
| Catch up on what changed in this chat since their last message, in plain words and small visuals, with every item waiting on them listed and decidable from the reply alone | [`/huajar-stack:ketchup`](../ketchup/SKILL.md) |
| Catch up like `/huajar-stack:ketchup`, in a short subtitled video of slides, with the waiting calls as text under it | [`/huajar-stack:ketchup-video`](../ketchup-video/SKILL.md) |
| Know what a small diff could break outside itself | [`/huajar-stack:blast-radius`](../blast-radius/SKILL.md) |
| Settle types and module shape before code that crosses a function boundary | [`/huajar-stack:architect`](../architect/SKILL.md) |
| Get several attempts at one brief, merged into the best one | [`/huajar-stack:arena`](../arena/SKILL.md) |
| Run parallel checks over slices, or race workers, each in its own worktree | [`/huajar-stack:swarm`](../swarm/SKILL.md) |
| Have different models review a diff and try to break it | [`/huajar-stack:interrogate`](../interrogate/SKILL.md) |
| Fix a bug test-first when a cheap local test exists | [`/huajar-stack:tdd`](../tdd/SKILL.md) |
| Apply TypeScript rules to `.ts` or `.tsx` work | [`/huajar-stack:typescript-best-practices`](../typescript-best-practices/SKILL.md) |
| Strip comments before review, using a reviewer that didn't write them | [`/huajar-stack:no-comments`](../no-comments/SKILL.md) |
| Clean AI tells out of prose | [`/huajar-stack:unslop`](../unslop/SKILL.md) |
| Write docs, an RFC, a README, a PR description, or a commit message to a standard | [`/huajar-stack:technical-writing`](../technical-writing/SKILL.md) |
| Hear the last reply again in plain words | [`/huajar-stack:bro`](../bro/SKILL.md) |
| Give agents a scripted way to drive the app and prove behavior | [`/huajar-stack:create-verification-skill`](../create-verification-skill/SKILL.md) |
| Bring a verification skill and its feature map back in line with the app | [`/huajar-stack:maintain-verification-skill`](../maintain-verification-skill/SKILL.md) |
| Formally verify a race, invariant, or other property that tests rarely reach | [`/huajar-stack:create-formal-verification-skill`](../create-formal-verification-skill/SKILL.md) |
| Bring a formal verification back in line after the code it covers changed, and learn whether a failure is drift or a bug | [`/huajar-stack:maintain-formal-verification-skill`](../maintain-formal-verification-skill/SKILL.md) |
| Vet a performance number before reporting or acting on it | [`/huajar-stack:benchmark-checklist`](../benchmark-checklist/SKILL.md) |
| Run a large or cross-cutting change, or one to review after stepping away | [`/huajar-stack:figure-it-out`](../figure-it-out/SKILL.md) |
| Keep a decision log during a run, and review it afterward | [`/huajar-stack:show-me-your-work`](../show-me-your-work/SKILL.md) |
| Pick a model for each role and a reasoning budget | [`/huajar-stack:setup-huajar-stack`](../setup-huajar-stack/SKILL.md) |
| Turn their own working habits into a personal mode skill | [`/huajar-stack:automate-me`](../automate-me/SKILL.md) |
| Turn what a finished task taught into skill edits | [`/huajar-stack:reflect`](../reflect/SKILL.md) |
| Stop agents from repeating the same mistakes in this repo | [`/huajar-stack:correct`](../correct/SKILL.md) |
| Find their way around huajar-stack | `/huajar-stack:huajar-help` |

If a skill directory next to this one is missing from the table, read its frontmatter and route by its description. The `principle-*` directories are covered under principles below.

Close calls:

- `/huajar-stack:how` explains what the code does. `/huajar-stack:why` explains the reasons. `/huajar-stack:teach` runs one or both and explains the result plainly.
- `/huajar-stack:arena` gives every worker the same brief and merges the best parts. `/huajar-stack:swarm` splits work into slices or a race and returns one report.
- `/huajar-stack:interrogate` reviews the diff. `/huajar-stack:blast-radius` looks for breakage outside the diff and proves the one fact that makes the change safe.
- `/huajar-stack:recall` rebuilds context across recent chats. `/huajar-stack:ketchup` covers only this chat since the user's last message. Resuming one specific chat or branch is the Session pickup playbook.
- `/huajar-stack:figure-it-out` designs one rigorous run. The Autonomous run playbook drives one task to a finish condition.

Not in huajar-stack, or not from pstack:

- `/huajar-stack:deslop`, `control-cli`, `control-ui`, and `verify-this` ship with huajar-stack.
- `/loop` is a Claude Code bundled skill. Claude Code has no built-in `create-skill`.
- huajar-stack has no `/orchestrate` skill. If the slash menu shows `/orchestrate`, another plugin provides it.

## Playbooks and principles

Playbooks are step lists inside `/huajar-stack:huajar-mode`, not skills, so they have no slash command. Inside `/huajar-stack:huajar-mode`, describing the task picks one, and these phrases name one directly:

- "babysit this pr" or "check on pr 123" runs Babysit. It drives the PR to merge-ready and stops there. It doesn't merge unless the user asks to merge, land, or ship.
- "land the stack" runs Shipping.
- "take over this branch" runs Session pickup.
- "pause safely" runs Pause safely.
- "full autopilot on this queue" runs Autopilot-full. "stack them, don't ship" runs Autopilot-stack.
- "run the eval playbook" runs Eval.

The Playbooks section of [`huajar-mode`](../huajar-mode/SKILL.md) lists every playbook and when it applies. [Guide page 6](../../docs/guide/06-verify-and-ship.md) covers opening, babysitting, and landing a PR.

huajar-stack has no planning skill. Claude Code's Plan Mode works alongside it. For work that spans phases or stacked PRs, asking `/huajar-stack:huajar-mode` for a plan runs the [Multi-phase plan playbook](../huajar-mode/playbooks/multi-phase-plan.md), which writes the plan and doesn't implement it. For a design question, the Prototype playbook or `/huajar-stack:architect` settles it in code first.

Principles are one-rule skills that `/huajar-stack:huajar-mode` reads and cites in its replies. The user rarely invokes one. They steer with the names instead, as in "apply prove it works. show me the real output." Typing `/huajar-stack:principle-<name>` still loads one on demand. [Guide page 8](../../docs/guide/08-principles.md) lists them.

## Fix a run that went wrong

| Symptom | Fix |
|---|---|
| The mode stopped applying after a few turns | Its content stays in context, but a long run drifts from it, and a compaction can trim or drop it. Invoke `/huajar-stack:huajar-mode` again, and start each new task with it. |
| A question got treated as the next step of the last task | Say "new task", or say the turn doesn't need the mode. |
| A new model choice had no effect | The rule from `/huajar-stack:setup-huajar-stack` applies to new chats. Start one. |
| Runs cost more than expected | See the cost paragraph under Get set up. |
| A skill didn't load on its own | Only `/huajar-stack:setup-huajar-stack` and the four team kit skills (`deslop`, `control-cli`, `control-ui`, `verify-this`) load from the user's words. The others load when the user types them or when `/huajar-stack:huajar-mode` runs them, and it doesn't run every skill. |
| Parallel agents overwrote each other | Give each agent its own worktree. |
| An overnight run moved but finished nothing | `/loop` needs a check that can pass or fail, not a duration. See [guide page 7](../../docs/guide/07-overnight.md). |
| The reply claims success from a green build | Ask for the real command, flow, stored value, or profile. That's the prove-it-works principle. |

For a run that drifts, [`references/prompting.md`](references/prompting.md) has one-line steers. [Guide page 10](../../docs/guide/10-recipes-and-pitfalls.md) has more pitfalls and the recipes worth copying.

## Make huajar-stack my own

- [`/huajar-stack:automate-me`](../automate-me/SKILL.md) drafts a personal mode skill from the user's own history, to use alongside `/huajar-stack:huajar-mode`.
- [`/huajar-stack:reflect`](../reflect/SKILL.md) after a session turns its lessons into skill edits the user approves.
- `/huajar-stack:huajar-mode write a skill for <workflow>` runs the authoring playbook. The eval playbook tests a skill change blind.
- Fix a misbehaving skill in its own PR, not inside the feature work where it went wrong.

[Guide page 9](../../docs/guide/09-make-it-yours.md) covers each of these.

## Reply

Lead with the answer. Give at most one example prompt in a code block, adapted from [`references/recipes.md`](references/recipes.md) when one fits, then the link to that file. Keep it short unless the user asked for the whole map.

Before you hand over a prompt, check it against the Leave out list in [`references/prompting.md`](references/prompting.md) and cut what it names, steps included. A cause or fix you read off the code is a guess, not a finding. Put it in only as a hypothesis for the run to measure, and never make it the done check.
