---
name: poteto-help
description: Guides users through pstack setup, poteto-mode, and picking the skill, playbook, or principle for a task. Invoke `pstack:poteto-help` with a question; it does not load on its own. Not for requests to do work, even ones that name pstack.
disable-model-invocation: true
---

# Poteto help

Answer the user's question about pstack, hand them a prompt they can send, and link the file the answer came from. For a help question, don't start the work. The user asked how, and a pstack run spends real tokens, so let them send the prompt.

A message that asks for work, such as "use pstack to fix this bug", is not a help question. Read [`poteto-mode`](../poteto-mode/SKILL.md), do the work under it, and mention once that session-start routing can keep it coming back for later tasks.

This file maps questions to the skills and docs that hold the answers. Those files own the details. Read the file you route to before you quote it, and trust it when it disagrees with this map. The links here point into the installed plugin, which the user may not be able to open, so give the user the file's public copy: `https://github.com/arjitj2/open-pstack/blob/main/plugins/pstack/` followed by its path. Install and update steps live in the README, which isn't packaged; its public copy is `https://github.com/arjitj2/open-pstack/blob/main/README.md`.

## Find out what they need

Infer the need from the message and the conversation. A named situation, such as "which skill reviews a PR?", goes straight to its section. If the need is still unclear, ask one multiple-choice question with these options, then answer only the section they pick:

- Get set up
- Start a task with `poteto-mode`
- Pick a skill for a situation
- Fix a run that went wrong
- Make pstack my own

Check the state that changes the answer, and mention it only when it does:

- Read the active parent's model sheet: `~/.claude/pstack-models.md` on Claude Code or `~/.codex/pstack-models.md` on Codex. A missing sheet uses documented role defaults. A missing role in a policy-enabled sheet is an error, not permission to use a default; unreadable or malformed sheets also fail. See [provider dispatch](../poteto-mode/references/provider-dispatch.md) for the legacy-sheet distinction.
- No `verify-*` skill or other app harness in the project means agents have no scripted way to drive the app. Mention `create-verification-skill` when the question is about proving a change works.

When no model sheet is saved and it matters, answer the question and include a Now/Later setup question in that same reply. It matters when the user is new, the question is about setup or cost, or the answer depends on which models run. Do not replace the question with only a setup link or example prompt. Ask at most once per chat, and if the need is also unclear ask both questions together. A request not to change settings or start workers does not prevent this explanation-only offer. Respect an explicit request not to ask questions, a previous choice of Later, or an earlier offer in this chat. The offer writes nothing; `setup-pstack` saves the sheet only after the user runs it and confirms. Offer two choices:

- Now: give them `setup-pstack` to invoke, and answer their question too.
- Later: answer their question, and add one line saying every role keeps its documented default until they run `setup-pstack`.

Skill names are namespaced under `pstack:`. In Claude Code, invoke `/pstack:poteto-mode`. In Codex, select `pstack:poteto-mode` in the skill picker or mention `$pstack:poteto-mode`. The rest of this file writes the bare names.

## Get set up

1. Install from the README's Install section (`https://github.com/arjitj2/open-pstack/blob/main/README.md#install`). In Claude Code, run `/plugin marketplace add arjitj2/open-pstack` then `/plugin install pstack@open-pstack` inside the app. In Codex, run `codex plugin marketplace add arjitj2/open-pstack` then `codex plugin add pstack@open-pstack` in the shell.
2. Run `setup-pstack`. It asks for a reasoning budget, checks the providers you pick, maps a model to each role, and writes the model sheet: `~/.claude/pstack-models.md` on Claude Code, `~/.codex/pstack-models.md` mirrored into `~/.codex/AGENTS.md` on Codex. The saved sheet loads at the start of a session or task.
3. Start a real task with `poteto-mode`, a goal, and a check that can pass or fail.

Claude Code loads pstack's session-start routing at session start, clear, and compaction, so non-trivial engineering work enters `poteto-mode` without naming it. Codex ships the same routing as an opt-in `SessionStart` hook covering startup, resume, clear, and compaction: it stays inactive until the user reviews and trusts the pstack entry in `/hooks`. The README's Get started section has the details. Offer to word their first prompt with them, per [`references/prompting.md`](references/prompting.md).

If cost is the worry, say where the tokens go and how to spend fewer. pstack spends extra tokens on subagents and review panels. Rerun `setup-pstack` and pick a smaller budget or cheaper models. A role set to `auto` or `inherit-parent` runs on the parent's current model. The sheet's access facts guide recommendations but do not prove entitlement; the saved API-spend setting controls whether metered access is authorized. The [provider dispatch contract](../poteto-mode/references/provider-dispatch.md) owns native versus external routes, access checks, and approved recovery chains. A shorter panel list runs fewer subagents, one for each entry. Save `poteto-mode` for work that needs rigor.

This distribution runs in Claude Code and Codex. Its skills use the Agent Skills format, so other tools can read them, but workflow skills spawn subagents through the parent's delegation surface and the shipped runner, so they may not work elsewhere. For Cursor itself, use the original Pstack. [Lauren's guide](https://github.com/cursor/plugins/tree/main/pstack/docs/guide) walks a real task in Cursor's interface; the ideas carry over.

## Start a task with `poteto-mode`

`poteto-mode` matches the task to a playbook, copies the playbook's steps into the todo list, and runs the other skills as the steps need them. A step it skips stays in the list as `skip: <reason>`. A good prompt states the goal and how to tell it's done. It doesn't list skills, because a hand-written sequence tends to drop or reorder steps the playbook would keep. Read [`references/prompting.md`](references/prompting.md) before you help word one. The Playbooks section of [`poteto-mode`](../poteto-mode/SKILL.md) has the list.

How `poteto-mode` stays in effect depends on the parent:

- Selecting the skill loads it for the task. It fades as the chat moves on.
- Claude Code reloads pstack's session-start routing at session start, clear, and compaction, so the next non-trivial engineering task enters `poteto-mode` again without naming it.
- On Codex the routing is opt-in. Once the user trusts the plugin's `SessionStart` entry in `/hooks`, new tasks route the same way. Untrusted or disabled, nothing routes: select the skill for each task.
- There is no mode to toggle on. Routing and explicit selection are the persistence. Mid-chat, "new task" makes the mode match a fresh playbook.

For ad-hoc native helpers, Claude Code can use `poteto-agent`; Codex has no such agent type and instead passes instructions to read `poteto-mode`. Configured roles must use [provider dispatch](../poteto-mode/references/provider-dispatch.md), preserving their selected models and effort. See the [Codex tool mapping](../poteto-mode/references/codex-tools.md#subagent-policy) for host details.

## Pick a skill

The default answer is `poteto-mode`, which runs most of the others when its steps need them. Name a skill directly when the user wants more or less of something than the playbook gives. Read the skill before you recommend it, and give one example prompt.

| The user wants to | Skill |
|---|---|
| Do any non-trivial task with rigor | [`poteto-mode`](../poteto-mode/SKILL.md) |
| Know how code works now, or where new code should live | [`how`](../how/SKILL.md) |
| Know why code is shaped this way, or where a number came from | [`why`](../why/SKILL.md) |
| Understand a change or subsystem, explained plainly | [`teach`](../teach/SKILL.md) |
| Catch up on their own recent work on a topic | [`recall`](../recall/SKILL.md) |
| Know what a small diff could break outside itself | [`blast-radius`](../blast-radius/SKILL.md) |
| Settle types and module shape before code that crosses a function boundary | [`architect`](../architect/SKILL.md) |
| Get several attempts at one brief, merged into the best one | [`arena`](../arena/SKILL.md) |
| Run parallel checks over slices, or race workers | [`swarm`](../swarm/SKILL.md) |
| Have different models review a diff and try to break it | [`interrogate`](../interrogate/SKILL.md) |
| Fix a bug test-first when a cheap local test exists | [`tdd`](../tdd/SKILL.md) |
| Apply TypeScript rules to `.ts` or `.tsx` work | [`typescript-best-practices`](../typescript-best-practices/SKILL.md) |
| Strip comments before review, using a reviewer that didn't write them | [`no-comments`](../no-comments/SKILL.md) |
| Clean AI tells out of prose | [`unslop`](../unslop/SKILL.md) |
| Clean AI slop and style noise out of code | [`deslop`](../deslop/SKILL.md) |
| Write docs, an RFC, a README, a PR description, or a commit message to a standard | [`technical-writing`](../technical-writing/SKILL.md) |
| Hear the last reply again in plain words | [`bro`](../bro/SKILL.md) |
| Give agents a scripted way to drive the app and prove behavior | [`create-verification-skill`](../create-verification-skill/SKILL.md) |
| Bring a verification skill and its feature map back in line with the app | [`maintain-verification-skill`](../maintain-verification-skill/SKILL.md) |
| Vet a performance number before reporting or acting on it | [`benchmark-checklist`](../benchmark-checklist/SKILL.md) |
| Run a large or cross-cutting change, or one to review after stepping away | [`figure-it-out`](../figure-it-out/SKILL.md) |
| Keep a decision log during a run, and review it afterward | [`show-me-your-work`](../show-me-your-work/SKILL.md) |
| Shepherd an open PR to merge-ready without re-prompting | [`babysit`](../babysit/SKILL.md) |
| Find and fix a PR's failing checks | [`fix-ci`](../fix-ci/SKILL.md) |
| Resolve a merge conflict non-interactively | [`fix-merge-conflicts`](../fix-merge-conflicts/SKILL.md) |
| Fetch and summarize review comments on the active PR | [`get-pr-comments`](../get-pr-comments/SKILL.md) |
| Tidy a PR's history, description, and reviewer guidance | [`make-pr-easy-to-review`](../make-pr-easy-to-review/SKILL.md) |
| Get an especially harsh maintainability review | [`thermo-nuclear-code-quality-review`](../thermo-nuclear-code-quality-review/SKILL.md) |
| Summarize their commits over a period | [`what-did-i-get-done`](../what-did-i-get-done/SKILL.md) |
| Pick a model for each role and a reasoning budget | [`setup-pstack`](../setup-pstack/SKILL.md) |
| Turn their own working habits into a personal mode skill | [`automate-me`](../automate-me/SKILL.md) |
| Turn what a finished task taught into skill edits | [`reflect`](../reflect/SKILL.md) |
| Stop agents from repeating the same mistakes in this repo | [`correct`](../correct/SKILL.md) |
| Find their way around pstack | `poteto-help` |

If a skill directory next to this one is missing from the table, read its frontmatter and route by its description. The `principle-*` directories are covered under principles below.

Close calls:

- `how` explains what the code does. `why` explains the reasons. `teach` runs one or both and explains the result plainly.
- `arena` gives every worker the same brief and merges the best parts. `swarm` splits work into slices or a race and returns one report.
- `architect` implements right after it settles the design. Add "with checkpoint" to review the design before it writes code.
- `interrogate` reviews the diff. `blast-radius` looks for breakage outside the diff and proves the one fact that makes the change safe.
- `recall` rebuilds context across recent sessions. Resuming one specific task or branch is the Session pickup playbook.
- A PR-status request under `poteto-mode` runs the Babysit playbook. The bundled `babysit` skill is the standalone form of the same job outside a run.
- `figure-it-out` designs one rigorous run. The Orchestrate playbook runs a program that spans days and many PRs. The Autonomous run playbook drives one task to a finish condition.

Not in pstack:

- `control-cli` and `control-ui` are Cursor Team Kit tools. The equivalents here are Claude Code's built-in `run` and `verify`; [`codex-tools.md`](../poteto-mode/references/codex-tools.md) maps them on Codex.
- `/create-skill` is a Cursor built-in. Authoring guidance here lives in `plugin-dev:skill-development`.
- `/loop`-style scheduling is a host built-in, not a pstack skill.
- pstack has no `/orchestrate` skill. Orchestrate is a `poteto-mode` playbook backed by the shipped `orch` bookkeeping CLI. If a slash menu shows `/orchestrate`, another plugin provides it.
- Cursor's Custom Mode is not part of this port. Persistence comes from session-start routing and explicit selection, described under Start a task.

`deslop` and `babysit` are bundled in this distribution. `deslop` comes from Cursor Team Kit; `babysit` is port-authored.

## Playbooks and principles

Playbooks are step lists inside `poteto-mode`, not skills, so they have no slash command. Inside `poteto-mode`, describing the task picks one, and these phrases name one directly:

- "babysit this pr" or "check on pr 123" runs Babysit. It drives the PR to merge-ready and stops there. It doesn't merge unless the user asks to merge, land, or ship.
- "land the stack" runs Shipping.
- "take over this branch" runs Session pickup.
- "pause safely" runs Pause safely.
- "full autopilot on this queue" runs Autopilot-full. "stack them, don't ship" runs Autopilot-stack.
- "run the eval playbook" runs Eval.

Without `poteto-mode`, a phrase such as "babysit this pr" can start the bundled `babysit` skill for the same job instead. The Playbooks section of [`poteto-mode`](../poteto-mode/SKILL.md) lists every playbook and when it applies.

pstack has no planning skill. The host's plan feature works alongside it. For work that spans phases or stacked PRs, asking `poteto-mode` for a plan runs the [Multi-phase plan playbook](../poteto-mode/playbooks/multi-phase-plan.md), which writes the plan and doesn't implement it. For a design question, the Prototype playbook or `architect` settles it in code first.

Principles are one-rule skills that `poteto-mode` reads and cites in its replies. They don't appear in the skill picker. The user steers with the names instead, as in "apply prove it works. show me the real output." The Principles section of [`poteto-mode`](../poteto-mode/SKILL.md) lists them.

## Fix a run that went wrong

| Symptom | Fix |
|---|---|
| The mode stopped applying after a few turns | The skill was selected for one task. Persistence is session-start routing (always on Claude Code; on Codex once the `SessionStart` hook is trusted in `/hooks`) or selecting `poteto-mode` per task. |
| Codex tasks never enter `poteto-mode` on their own | The `SessionStart` hook is untrusted or disabled. Trust it in `/hooks`, or select the skill by name. |
| A question got treated as the next step of the last task | Say "new task", or say the turn doesn't need the mode. |
| A new model choice had no effect | The saved sheet loads at the start of a session or task. Start a new one. |
| Runs cost more than expected | See the cost paragraph under Get set up. |
| A skill didn't load on its own | Skills load when named, when a description matches, or when `poteto-mode` runs them, and it doesn't run every skill. `poteto-help` is manual-only: it runs only when invoked. Session-start routing only steers non-trivial engineering work into `poteto-mode`. |
| Parallel agents overwrote each other | Give each writer its own worktree or unique output directory. |
| A worker stopped instead of switching models | By design. Only the sheet's saved `primary -> fallback` chain, under its [`# fallback` policy](../poteto-mode/references/provider-dispatch.md#saved-fallback-and-backend-recovery), may take over. Anything else is a dropout; repair the route or change assignments through `setup-pstack`. |
| An overnight run moved but finished nothing | A scheduled loop needs a check that can pass or fail, not a duration. |
| The reply claims success from a green build | Ask for the real command, flow, stored value, or profile. That's the prove-it-works principle. |

For a run that drifts, [`references/prompting.md`](references/prompting.md) has one-line steers.

## Make pstack my own

- [`automate-me`](../automate-me/SKILL.md) drafts a personal mode skill from the user's own history, to use alongside `poteto-mode`.
- [`reflect`](../reflect/SKILL.md) after a session turns its lessons into skill edits the user approves.
- `poteto-mode write a skill for <workflow>` runs the authoring playbook. The eval playbook tests a skill change blind.
- Fix a misbehaving skill in its own PR, not inside the feature work where it went wrong.

## Reply

Lead with the answer. Give at most one example prompt in a code block, adapted from [`references/recipes.md`](references/recipes.md) when one fits, then the link to that file. Keep it short unless the user asked for the whole map.
