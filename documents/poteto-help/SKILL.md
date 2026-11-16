---
name: poteto-help
description: Guides users through pstack setup, /poteto-mode, and picking the skill, playbook, or principle for a task. Type /poteto-help with a question.
disable-model-invocation: true
---

# Poteto help

Answer the user's question about pstack, hand them a prompt they can send, and link the file the answer came from. For a help question, don't start the work. The user asked how, and a pstack run spends real tokens, so let them send the prompt.

A message that asks for work, such as "use pstack to fix this bug", is not a help question. Read [`poteto-mode`](../poteto-mode/SKILL.md), do the work under it, and mention once that `/poteto-mode` stays in context until the chat is compacted.

This file maps questions to the skills and guide pages that hold the answers. Those files own the details. Read the file you route to before you quote it, and trust it when it disagrees with this map. The links here point into the installed skills, which the user may not be able to open, and `docs/` is not installed at all, so give the user the file's public copy: `https://github.com/ynginkim/pstack-anywhere/blob/main/` followed by its path from the repository root (`skills/<name>/SKILL.md`, `docs/guide/<page>.md`).

## Find out what they need

Infer the need from the message and the conversation. A named situation, such as "which skill reviews a PR?", goes straight to its section. If the need is still unclear, ask one multiple-choice question with these options, then answer only the section they pick:

- Get set up
- Start a task with `/poteto-mode`
- Pick a skill for a situation
- Fix a run that went wrong
- Make pstack my own

Check the state that changes the answer, and mention it only when it does:

- No `~/.agents/skills/select-model/SKILL.md` means `/setup-pstack` hasn't run for this user, so skills run on their default models and say so once.
- No `verify-*` skill or other app harness in the project means agents have no scripted way to drive the app. Mention `/create-verification-skill` when the question is about proving a change works.
- No formal verification skill in the project means no property is checked past what tests reach. Mention `/create-formal-verification-skill` when the question is about a race, an invariant, or another case tests rarely hit. When one exists and the code it covers changed after the commit it records as last in sync, mention `/maintain-formal-verification-skill` if the question touches that code.

When `select-model` is missing and it matters, ask whether the user wants to set it up now. Setup surveys this computer and asks five questions about budget and model preferences. It matters when the user is new, the question is about setup or cost, or the answer depends on which models run. Ask at most once per chat. If the need is also unclear, ask both questions together. Offer two choices:

- Now: give them `/setup-pstack` to type, and answer their question too.
- Later: answer their question, and add one line saying skills keep their default models until they run `/setup-pstack`.

## Get set up

1. Install the skills for the user's harnesses: `npx skills add ynginkim/pstack-anywhere -g -s '*' -y`, with one `-a <id>` for each harness. The For users section of each harness adapter in [`resolve-capability/adapters/`](../resolve-capability/adapters/) gives its id, where it reads skills, and how a skill runs there. Start a new session afterwards.
2. Run [`/setup-pstack`](../setup-pstack/SKILL.md). It surveys this computer, asks five questions about budget and model preferences, and writes the `select-model` skill. Every skill reads it at the start of a task. Then it offers once each to generate a verification skill and a formal verification skill for the project, unless the project already has one.
3. Start a real task with `/poteto-mode`, a goal, and a check that can pass or fail.

Installing changes nothing until the user invokes a skill. Which skills a harness loads from the user's words alone is in its adapter's For users section. The [README](../../README.md) and [guide page 1](../../docs/guide/01-setup.md) have the details. Offer to word their first prompt with them, per [`references/prompting.md`](references/prompting.md).

If cost is the worry, say where the tokens go and how to spend fewer. pstack spends extra tokens on subagents and review panels. Rerun `/setup-pstack` and pick a smaller budget or cheaper models. A preference to follow the session's model keeps subagents on the chat's model, which saves tokens when the chat runs on Auto or a cheaper model. Say you want fewer models used at once, and the review panels run smaller. Save `/poteto-mode` for work that needs rigor.

pstack runs in each harness that has an adapter in [`resolve-capability/adapters/`](../resolve-capability/adapters/), in a terminal, in an environment that adds to harnesses, or in a harness's desktop app. A skill names what it needs from the environment (`spawn-worker`, `ask-user`, and so on), and the [`resolve-capability`](../resolve-capability/SKILL.md) skill says how each is done where the user is. An environment adapter adds supervised workers, durable runs, schedules, and remote environments. Without one, a skill that wants another vendor's model starts that product's CLI headless when it is installed and logged in, and otherwise runs the seat on its own model and says so.

## Start a task with `/poteto-mode`

`/poteto-mode` matches the task to a playbook, copies the playbook's steps into a visible plan (the harness's plan or todo tool, or a list in the reply), and runs the other skills as the steps need them. A step it skips stays in the list as `skip: <reason>`. A good prompt states the goal and how to tell it's done. It doesn't list skills, because a hand-written sequence tends to drop or reorder steps the playbook would keep. Read [`references/prompting.md`](references/prompting.md) before you help word one. [Guide page 2](../../docs/guide/02-poteto-mode.md) has examples.

`/poteto-mode` stays in context until the chat is compacted. When the mode stops applying, or after a compaction, start the next task with `/poteto-mode` again. Mid-chat, "new task" makes the mode match a fresh playbook.

Link the skills documentation of the user's harness when this comes up. Its adapter's For users section has the link. `/poteto-mode` already starts the subagents its playbook steps spawn with the `poteto-agent` rules. To get the same style from a subagent of your own, start its prompt with "Read `<path of poteto-mode/SKILL.md>` in full, including its Principles section, before any work."

## Pick a skill

The default answer is `/poteto-mode`, which runs most of the others when its steps need them. Name a skill directly when the user wants more or less of something than the playbook gives. Read the skill before you recommend it, and give one example prompt.

| The user wants to | Skill |
|---|---|
| Do any non-trivial task with rigor | [`/poteto-mode`](../poteto-mode/SKILL.md) |
| Check that the agent understood their goal and the problem before it starts | [`/in-your-own-words`](../in-your-own-words/SKILL.md) |
| Get a prompt rewritten deeper, not bigger, before sending it: what a top professional would add, their raw material and methods, and an outside check. It returns the prompt and doesn't do the task | [`/sharpen`](../sharpen/SKILL.md) |
| Know how code works now, or where new code should live | [`/how`](../how/SKILL.md) |
| Know why code is shaped this way, or where a number came from | [`/why`](../why/SKILL.md) |
| Understand a change or subsystem, explained plainly | [`/teach`](../teach/SKILL.md) |
| Catch up on their own recent work on a topic | [`/recall`](../recall/SKILL.md) |
| Catch up on what changed in this chat since their last message, in plain words and small visuals, with every item waiting on them listed and decidable from the reply alone | [`/ketchup`](../ketchup/SKILL.md) |
| Catch up like `/ketchup`, in a short subtitled video of slides, with the waiting calls as text under it | [`/ketchup-video`](../ketchup-video/SKILL.md) |
| Know what a small diff could break outside itself | [`/blast-radius`](../blast-radius/SKILL.md) |
| Settle types and module shape before code that crosses a function boundary | [`/architect`](../architect/SKILL.md) |
| Get several attempts at one brief, merged into the best one | [`/arena`](../arena/SKILL.md) |
| Run parallel checks over slices, or race workers, each in its own checkout | [`/swarm`](../swarm/SKILL.md) |
| Have different models review a diff and try to break it | [`/interrogate`](../interrogate/SKILL.md) |
| Fix a bug test-first when a cheap local test exists | [`/tdd`](../tdd/SKILL.md) |
| Apply TypeScript rules to `.ts` or `.tsx` work | [`/typescript-best-practices`](../typescript-best-practices/SKILL.md) |
| Remove code slop a branch added before commit: needless defensive checks, type escapes, deep nesting | [`/deslop`](../deslop/SKILL.md) |
| Strip comments before review, using a reviewer that didn't write them | [`/no-comments`](../no-comments/SKILL.md) |
| Clean AI tells out of prose | [`/unslop`](../unslop/SKILL.md) |
| Write docs, an RFC, a README, a PR description, or a commit message to a standard | [`/technical-writing`](../technical-writing/SKILL.md) |
| Hear the last reply again in plain words | [`/bro`](../bro/SKILL.md) |
| Drive a web, IDE, or Electron UI and capture evidence | [`/control-ui`](../control-ui/SKILL.md) |
| Drive a CLI or TUI with a repeatable harness and capture evidence | [`/control-cli`](../control-cli/SKILL.md) |
| Give agents a scripted way to drive the app and prove behavior | [`/create-verification-skill`](../create-verification-skill/SKILL.md) |
| Bring a verification skill and its feature map back in line with the app | [`/maintain-verification-skill`](../maintain-verification-skill/SKILL.md) |
| Formally verify a race, invariant, or other property that tests rarely reach | [`/create-formal-verification-skill`](../create-formal-verification-skill/SKILL.md) |
| Bring a formal verification back in line after the code it covers changed, and learn whether a failure is drift or a bug | [`/maintain-formal-verification-skill`](../maintain-formal-verification-skill/SKILL.md) |
| Show a PM or designer what the user sees as a chart checked by a TLA+ model, with the shortest path to each state that breaks a rule | [`/statechart`](../statechart/SKILL.md) |
| Vet a performance number before reporting or acting on it | [`/benchmark-checklist`](../benchmark-checklist/SKILL.md) |
| Run a large or cross-cutting change, or one to review after stepping away | [`/figure-it-out`](../figure-it-out/SKILL.md) |
| Keep a decision log during a run, and review it afterward | [`/show-me-your-work`](../show-me-your-work/SKILL.md) |
| Set up model selection: survey this computer, pick preferences and a reasoning budget | [`/setup-pstack`](../setup-pstack/SKILL.md) |
| Turn their own working habits into a personal mode skill | [`/automate-me`](../automate-me/SKILL.md) |
| Turn what a finished task taught into skill edits | [`/reflect`](../reflect/SKILL.md) |
| Stop agents from repeating the same mistakes in this repo | [`/correct`](../correct/SKILL.md) |
| Find their way around pstack | `/poteto-help` |

If a skill directory next to this one is missing from the table, read its frontmatter and route by its description. The `principle-*` directories are covered under principles below.

Close calls:

- `/how` explains what the code does. `/why` explains the reasons. `/teach` runs one or both and explains the result plainly.
- `/deslop` edits the code a branch added. `/no-comments` handles its comments, and `/unslop` handles prose.
- `/control-ui` and `/control-cli` drive the app once, for this change. `/create-verification-skill` writes a lasting skill for one repository.
- `/arena` gives every worker the same brief and merges the best parts. `/swarm` splits work into slices or a race and returns one report.
- `/architect` implements right after it settles the design. Add "with checkpoint" to review the design before it writes code.
- `/interrogate` reviews the diff. `/blast-radius` looks for breakage outside the diff and proves the one fact that makes the change safe.
- `/recall` rebuilds context across recent chats. `/ketchup` covers only this chat since the user's last message. Resuming one specific chat or branch is the Session pickup playbook.
- `/figure-it-out` designs one rigorous run. The Orchestrate playbook runs a program that spans days and many PRs. The Autonomous run playbook drives one task to a finish condition.

Not in pstack:

- pstack has no skill that drives a native desktop window. `drive-app` in the adapter says how this environment does it.
- Loops and skill authoring come from the harness. Its adapter's For users section names them, and `author-skill` resolves skill authoring. The Authoring a skill playbook covers the rest.
- pstack has no `/orchestrate` skill. Orchestrate is a `/poteto-mode` playbook. If the slash menu shows `/orchestrate`, another plugin provides it.

## Playbooks and principles

Playbooks are step lists inside `/poteto-mode`, not skills, so they have no slash command. Inside `/poteto-mode`, describing the task picks one, and these phrases name one directly:

- "babysit this pr" or "check on pr 123" runs Babysit. It drives the PR to merge-ready and stops there. It doesn't merge unless the user asks to merge, land, or ship.
- "land the stack" runs Shipping.
- "take over this branch" runs Session pickup.
- "pause safely" runs Pause safely.
- "full autopilot on this queue" runs Autopilot-full. "autopilot, don't merge" runs Autopilot-stack.
- "run the eval playbook" runs Eval.

Without `/poteto-mode`, a phrase such as "babysit this pr" may start a skill from another plugin or from the harness for the same job instead. The Playbooks section of [`poteto-mode`](../poteto-mode/SKILL.md) lists every playbook and when it applies. [Guide page 6](../../docs/guide/06-verify-and-ship.md) covers opening, babysitting, and landing a PR.

pstack has no planning skill. The harness's plan mode works alongside it, and its adapter's For users section names it. For work that spans phases or stacked PRs, asking `/poteto-mode` for a plan runs the [Multi-phase plan playbook](../poteto-mode/playbooks/multi-phase-plan.md), which writes the plan and doesn't implement it. For a design question, the Prototype playbook or `/architect` settles it in code first.

Principles are one-rule skills that `/poteto-mode` reads and cites in its replies. The user rarely invokes one. They steer with the names instead, as in "apply prove it works. show me the real output." Typing `/principle-<name>` still loads one on demand. [Guide page 8](../../docs/guide/08-principles.md) lists them.

## Fix a run that went wrong

| Symptom | Fix |
|---|---|
| The mode stopped applying after a few turns | It left the context when the chat was compacted. Start each task with `/poteto-mode`. |
| A question got treated as the next step of the last task | Say "new task", or say the turn doesn't need the mode. |
| A new model choice had no effect | Skills read `select-model` at the start of a task. Edit the sentence under `## Preferences` in it, or run `/setup-pstack` again, then start the task again. |
| Runs cost more than expected | See the cost paragraph under Get set up. |
| A skill didn't load on its own | Some harnesses load only `/setup-pstack` from the user's words, as each adapter's For users section says. The others load when the user types them or when `/poteto-mode` runs them, and it doesn't run every skill. |
| Parallel agents overwrote each other | Give each agent its own checkout, as `isolate-checkout` says, or a remote environment through `run-remote` where an environment adapter has one. |
| An overnight run moved but finished nothing | A recurring run needs a check that can pass or fail, not a duration. See [guide page 7](../../docs/guide/07-overnight.md). |
| The reply claims success from a green build | Ask for the real command, flow, stored value, or profile. That's the prove-it-works principle. |

For a run that drifts, [`references/prompting.md`](references/prompting.md) has one-line steers. [Guide page 10](../../docs/guide/10-recipes-and-pitfalls.md) has more pitfalls and the recipes worth copying.

## Make pstack my own

- [`/automate-me`](../automate-me/SKILL.md) drafts a personal mode skill from the user's own history, to use alongside `/poteto-mode`.
- [`/reflect`](../reflect/SKILL.md) after a session turns its lessons into skill edits the user approves.
- `/poteto-mode write a skill for <workflow>` runs the authoring playbook. The eval playbook tests a skill change blind.
- Fix a misbehaving skill in its own PR, not inside the feature work where it went wrong.

[Guide page 9](../../docs/guide/09-make-it-yours.md) covers each of these.

## Reply

Lead with the answer. Give at most one example prompt in a code block, adapted from [`references/recipes.md`](references/recipes.md) when one fits, then the link to that file. Keep it short unless the user asked for the whole map.
