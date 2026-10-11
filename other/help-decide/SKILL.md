---
name: help-decide
description: Lay a decision out for Sergio so one word answers it, recommendation and pros and cons first, then how the thing works and what each choice changes. Use when he says help-decide, asks for pros vs cons, or answers a question with "don't understand, explain".
---

## Running in Codex

This is the Codex copy of this skill. Read the rest of it with these translations:

- Agents launched in parallel: spawn each one with `spawn_agent` before waiting on any, then collect the
  results with `wait_agent`. Tell every agent you spawn not to spawn agents of its own. If subagents are
  unavailable, run each lane yourself, one after another.
- "Your default model" and "your strongest model": spawn the agent with an `agent_type` whose role file in
  `~/.codex/agents/` sets `model` and `model_reasoning_effort`. An agent without a role runs on the
  session's model.
- A slash command such as `/name`: mention the skill as `$name`.
- This repository's hooks and `.claude/` paths are for Claude Code only, and nothing here installs a Codex
  hook. A loop runs one pass per invocation, saves its state and reports how to resume.
- `CLAUDE.md`: also read `AGENTS.md`, which is the file Codex loads.

# help-decide

Sergio answered a question with a question. He wants to decide, not to be told, and he decides fast once the choice is laid out plainly. The answer gives him the recommendation and the comparison first, the explanation after, and ends with the question phrased so that one word settles it.

## Before writing

1. **Restate the decision in plain words.** One sentence: what is being chosen, between which options, and what happens if he says nothing. When his question shows that the original wording misled him, say first what that sentence meant. Done when a reader who missed the thread knows what the choice is.
2. **Check every fact against the system.** Read the code path, run the command, read the defaults, measure the size. Each claim in the pros and cons carries where it was checked: a `file:line`, a command with its output, a doc path. A claim that could not be checked is marked as inferred. Done when nothing in the answer rests on memory alone.
3. **Pick a side.** One option, one reason. Ties go to the house rules: the smallest change that makes the behaviour unsurprising, nothing built for a case that has not happened, the reversible choice over the one-way one.

## The shape of the answer

In this order, each under its own short heading.

**Recommendation.** The option, the one reason, and what it costs if the choice turns out wrong. Two or three sentences.

**Options, pros and cons.** One block per option, named by what it does (`off deletes the two keys`, never `option B`). Under each, pros and cons as short bullets with the evidence beside each one. Say which cons are permanent and which a later change removes. Done when every fact appears under each option it touches, so he compares like with like.

**Worth knowing.** Whatever would change the answer: a trap already written down, a cost paid once against a cost paid every day, who else the choice reaches (teammates, other machines, other apps), and whether it is reversible and by which command.

**How it works.** The mechanism behind the choice with real names: the file, the key, the command, the process that reads it and the moment it reads it. Long enough that he could do it by hand, and no longer.

**What changes.** Per option, the concrete difference he sees and when: a prompt that appears or stays away, a process that starts or stays down, a file that exists or is gone. Observed and expected are marked as such.

**With it, without it.** One short scenario per option, walked from the triggering action to the last visible effect, so he can picture a day under each.

**The question.** The choice restated as a yes/no or a pick-one, the recommended answer listed first, so that "yes" or "1" is a complete reply.

## Rules for every sentence

- Plain words, short sentences, one idea each. A term is defined in the sentence where it first appears.
- Real names only: the exact path, key, flag, command, version. Explain around the name instead of replacing it with a description.
- Explain with the actual request, file or message. A comparison to another product appears only when it is a fact of the design.
- A number sits in a table or on its own line, next to the command that produced it.
- The decision is his. The recommendation is stated once and every option stays whole on the page.
- The length is what the choice needs: a two-way choice fits in about forty lines. Several decisions in one message each get the full shape, the shortest first.

The same shape serves a doc, where the citations become plain statements of what we decided.
