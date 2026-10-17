---
name: migrate-memories
description: Move leftover Claude Code and Codex memory files into fixes, instructions, or skills, then archive them so built-in memory stays off.
disable-model-invocation: true
---

# Migrate memories

Built-in agent memory is off by policy (`agents-config` enforces it). Memory
files left on disk are corrections that skipped the ladder in the
"Corrections" section of the instructions. This skill puts each one on the
right rung and archives the rest.

## 1. Inventory

Run `agents-config plan --only memory`. It lists any client with memory still
on and every leftover file:

- Claude Code: `~/.claude/projects/*/memory/*.md` (skip `MEMORY.md`, it is an
  index of the others).
- Codex: `~/.codex/memories/`. `MEMORY.md` and `memory_summary.md` hold the
  consolidated set; `raw_memories.md` and `rollout_summaries/` are their
  inputs, read them only to resolve something unclear.

Nothing listed means nothing to migrate; go to step 4.

## 2. Triage

Read every memory. Put each one on exactly one line of a table: memory, rung,
destination, action. Rungs, best first:

1. **Architecture**: a code change makes the mistake impossible (a tool that
   refuses the dangerous call, a type that cannot hold the bad state).
2. **CI**: a lint rule or test catches it.
3. **Rule**: an instruction fragment in `~/Agents/Config/Instructions/fragments/`
   or a skill in `~/Agents/Config/Skills/Skills/`. Prefer the skill that owns
   the workflow over the global instructions.
4. **Drop**: project working notes, dated decisions, one-off incident state,
   or anything already covered by existing instructions, skills, or repo
   docs. Grep before deciding something is new.

Show the table and wait for approval before changing anything.

## 3. Apply

- Rungs 1 and 2: implement in the owning repo only when it is a personal repo
  and the change is small and verifiable. Otherwise submit it with
  `hindsight.submit_feedback` (category `codebase` or `tooling`, with the
  rung) and record it as filed.
- Rung 3: edit the fragment or skill with the smallest delta in the
  surrounding style. Generalize repo-specific wording only when the rule holds
  more widely. No dates, session ids, or incident narrative.
- Never copy credentials, tokens, or personal data out of a memory.

## 4. Archive and enforce

1. Move every leftover memory file, keeping its path, under
   `~/.local/state/agents-config/backups/<YYYYmmdd-HHMMSS>-memories/`. Move;
   do not delete.
2. Run `agents-config apply --only memory`, then
   `agents-config apply --only instructions` and
   `agents-config apply --only skills` if a fragment or skill changed.
3. `agents-config plan --only memory` must report 0 clients with memory on and
   0 leftover files.

## 5. Report

The triage table with outcomes, the archive path, and
`git -C ~/Agents/Config status --short`. Commit fragment and skill edits in
`~/Agents/Config` with a short imperative message. Ask before pushing.
