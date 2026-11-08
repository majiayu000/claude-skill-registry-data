---
name: full-loop
description: Drive a repository to done with sergio-loop, then keep improving it with refine-loop at a descending theta. Use only when the user explicitly invokes full-loop.
argument-hint: "[goal]"
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

# full-loop

**Your first action is to load the `sergio-loop` skill, not to analyse.** Load it now, before reading
further, before inspecting the repository, and before answering anything. Do not paraphrase, summarize or
reimplement what that skill does: load it and follow it. If you find yourself planning the work in this
turn without having loaded it, you have already gone wrong. Stop and load it.

Apply [the shared loop contract](references/loop-contract.md) to every operation; both loops follow it too.

The goal is this skill's arguments. If none were given, the goal is whatever the repository's own state
says is unfinished.

Stay in `sergio-loop` for as long as there is work left. Then, once you have **checked that nothing is
pending**, load the `refine-loop` skill (again a real load, not a description of it) and step theta down,
one segment per level, passing the goal as the refinement intent every time:

1. `refine-loop theta=2.0 <goal>` starts the first segment.
2. When that segment reaches a terminal outcome, `refine-loop --continue theta=1.0 <goal>` opens the next.
3. Then `--continue theta=0.5 <goal>`, then `--continue theta=0.25 <goal>`. Stop after the `0.25`
   segment: refine-loop rejects `theta <= 0`, so the schedule ends at that positive floor.

If no goal was given, use one sentence naming what the repository's state said was unfinished as the
intent, so refine-loop never stops to ask for one.

"Nothing is pending" is a check, not a feeling. It holds only when all of these are true, each with
evidence recorded:

- no ready work remains in the issue tracker for this repository;
- `docs/DEFERRED-QUESTIONS.md` has no open question that a resolution pass could close. Run the pass
  rather than assuming;
- every request this segment satisfied has been reported back, with its link actually delivered;
- the goal's acceptance criteria passed fresh verification and an independent review.

If any of those fails, there is still work left, so stay in `sergio-loop`. When its run has already
ended in `SUCCESS`, it does no more work on its own: start the next segment with
`sergio-loop --continue <new goal>`, where the new goal names the failing check's work (for example the
ready tracker items, or the open deferred questions).

Do not treat a blocker as final until you have said whether it is impossible or merely hard. Hard is
yours to solve. When something truly needs the owner, say in plain terms what you need and what each
answer unblocks.

Do not run builds or tests in the background while a loop is running: a live background task at stop
time ends the loop silently, spending no continuation and writing no terminal state. Run them in the
foreground.

$ARGUMENTS
