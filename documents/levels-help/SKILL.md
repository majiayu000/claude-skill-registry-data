---
name: levels-help
description: "Explain the level skill set to a new user: what it is, which skill to start with, how a run goes, what the arguments mean and what it costs. Read-only and cheap. Use when the user runs /levels-help or asks how the level skills work, what they do or how to start."
summary: Read the guide
argument-hint: "[skill name | overview | models | arguments | examples]"
model: haiku
---

# Levels help

Arguments: `$ARGUMENTS`

Read-only. This skill changes no file, spawns no agent and starts no other skill. Answer from the text below. Do not audit the project.

- No argument: print **Overview**, then **Start here**, then **Skills**. End with the one-line list of topics.
- Argument is a topic (`overview`, `models`, `arguments`, `examples`): print that section only.
- Argument is a skill name: read that skill's `SKILL.md` and summarise it in at most twelve lines: what it audits, its five levels in one line each, its arguments, what it never does, and one example command. If the skill is not installed, say so.
- A question in plain words: answer it from this text in a few sentences, then name the section to read for more.

Use the skill names as the skill listing shows them (a name may carry a prefix). If a skill named below is missing from the listing, mark it as not installed.

## Overview

The level skills rate one part of a project on a scale from 1 to 5, show what is missing for the level you want, and then do the work if you ask. Every skill follows the same seven steps:

1. **Context.** It looks at the project, then asks you only what it could not find.
2. **Audit.** It states the level you are at now, with evidence, and lists the gaps.
3. **Options.** For the main gaps it gives two or three choices with costs, and marks one as recommended. Then it stops and waits for you.
4. **Plan.** It splits what you chose into small sub-plans.
5. **Delegation gate.** It shows which model will do each sub-plan and asks before anything runs.
6. **Execution.** The sub-plans run on the models you approved.
7. **Review.** It checks the result and reports what moved and what is still open.

Level 5 is not the goal. Pick the level that fits the product. A small tool is finished at level 2 or 3, and the skills will tell you when a target is too high.

Results are kept in `LEVELS.md` in the project root, so later skills do not ask the same questions again.

## Start here

- First time, or not sure: run `/levels`. It asks what you want to do with a tick-box prompt and runs the right skills in a safe order.
- Just want to see where the project stands: `/levels-status`.
- Want one recommendation: `/levels-next`.
- Know exactly which part you want: run that skill directly, for example `/test-level`.

Every skill starts in `audit` mode unless you say `build`. An audit changes nothing in your product code, so it is always safe to run first.

## Skills

<!-- skills-table:start -->
| Skill | Use it to |
|---|---|
| `levels` | Run several skills as one workflow |
| `levels-status` | See every level and open gap in one table |
| `levels-next` | Get the single best next step |
| `levels-help` | Read the guide |
| `idea-level` | Find or sharpen a project idea, up to a build-ready blueprint |
| `ux-level` | Check whether users can finish their tasks |
| `restyle-level` | See alternative looks and layouts as mockups |
| `design-level` | Raise the quality of the interface |
| `backend-level` | Harden the server, logic and edge cases |
| `data-level` | Fix stored data shape, integrity and migrations |
| `test-level` | Prove the product works |
| `security-level` | Find and close security weaknesses |
| `perf-level` | Measure and improve speed |
| `code-level` | Clean up structure without changing behaviour |
| `docs-level` | Make documentation accurate and usable |
| `ship-level` | Prepare a safe, repeatable release |
| `pitch-level` | Prepare a demo, talk or submission |
<!-- skills-table:end -->

## Arguments

Arguments go after the command, in any order.

- **A number 1 to 5**: the level to aim for. Each skill has its own default.
- **`audit` or `build`**: `audit` rates and proposes only. `build` goes on to plan and delegate the work.
- **A path or screen name**: limits the skill to that area.
- **Skill-specific switches**: for example `a11y` on `design-level` and `restyle-level` turns accessibility requirements on. They are off unless you ask. Run `/levels-help <skill>` to see the switches for one skill.

## Models

- Opus (or Fable, if your session runs it) does the thinking: context, audit, options, plan and review.
- Haiku or Sonnet does the building. Haiku is the default. Sonnet is used where the work cannot be fully written out in advance.
- Before any building starts you see a line such as `Delegation: 6 sub-plans on Haiku, 2 on Sonnet. Review on Opus.` and four choices: as planned, Haiku only, Sonnet for all, or no delegation.
- Nothing builds until you answer. Each skill started by another skill asks again, because it starts its own spend.
- To spend least: run audits only, choose few gaps, and keep the level modest.

## Safety

- No skill deploys, touches a live system or works on real data. Steps on a live system are written out for you to run.
- Skills stay in their own area. `test-level` writes tests only, `code-level` never changes behaviour, `restyle-level` never edits product code.
- One skill may offer to start another when it finds a problem outside its area. It always asks first.
- Accepted risks and steps waiting on you are recorded in `LEVELS.md`. `/levels-status` lists them.

## Examples

- `/levels`: answer the prompt, confirm the level plan, approve each skill as it comes up.
- `/levels release`: tests, security, documentation and release checks before a date.
- `/design-level 3 audit`: rate the interface against level 3 and list the gaps.
- `/backend-level 4 build server/`: audit the `server/` folder, then plan and build to level 4.
- `/restyle-level 2 4`: four alternative directions, each as one first screen.
- `/idea-level`: brainstorm project ideas from your constraints.

## Common questions

- **Will it change my code?** Not in `audit` mode. In `build` mode, only after you pick options and approve the delegation gate.
- **Can I stop halfway?** Yes. Progress is in `LEVELS.md`. Run `/levels` again to resume.
- **Do I need every skill?** No. Skip what does not apply. The skills say so when a requirement does not fit the product.
- **It asked for a level I do not understand.** Run `/levels-help <skill>` to see that skill's five levels.
- **A skill is missing.** The others still work. Handoffs to a missing skill stop and tell you.

Topics: `overview`, `models`, `arguments`, `examples`, or any skill name.
