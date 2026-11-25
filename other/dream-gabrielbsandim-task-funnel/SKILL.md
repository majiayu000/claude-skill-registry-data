---
name: dream
description: "Reviews one project's recent sessions out of band and proposes changes to its rules and memory, each backed by evidence from two or more named sessions, including what to remove; applies only what the user approves. Use when asked to dream, to review what recent sessions learned or keep getting wrong, to clean up or consolidate memory or CLAUDE.md, or on /dream [N sessions]."
---

# dream: what the sessions keep teaching, proposed for approval

A session writes memory with half its attention on the task, and it sees only itself,
so the mistake it repeats is invisible to it: every session starts clean. This skill
is the second pass, run with its own budget: read many sessions side by side, find
what recurs, check it against what the rules and memory already say, and propose the
change. Nothing is applied without the user saying yes to that item.

Input: how many sessions, default 20. The scope is the repository you are in.

## Stage 1 · The digest, from a script

```
mkdir -p "$CLAUDE_WIP/dream"
kit dream-digest --sessions 20 --skip-newest > "$CLAUDE_WIP/dream/digest.md"
```

`--skip-newest` leaves out this session's own transcript. When the user names a folder
of transcripts instead, pass it with `--dir` and drop `--skip-newest`: none of those
files is this session. Without `--dir` it reads only this repository's transcript
folder, counts which tool errors recur in
how many sessions, and lists what the user typed in each. Read the digest, not the raw
transcripts: a `.jsonl` is mostly tool output, and the count of how many sessions share
a pattern is the script's job, not memory's.

**One employer per run.** The digest never crosses repositories. A proposal goes to the
rules and memory of this repository's own context, and nothing learned here is written
into another employer's vault, or into the personal one from an employer's repository.

## Stage 2 · What is already written

Read, before proposing anything, or the proposals repeat what is already there:

- the repository's `CLAUDE.md` or `AGENTS.md` and the user-level `CLAUDE.md`;
- this project's auto-memory directory, `MEMORY.md` and the files it points to;
- `$CLAUDE_WIP/dream/ledger.md`, if it exists: what earlier runs proposed, and what the
  user rejected and why. A rejected proposal comes back only with new evidence.

Count the instruction lines that load into every session (the CLAUDE.md files and
their `@` imports, `wc -l`). It is a budget: past roughly 200, adherence drops for every
rule, the good ones included.

## Stage 3 · Find what recurs

More than about 40,000 characters of digest: split the sessions across subagents, at
most `kit config get .maxParallelAgents`, each given its sessions, this stage's rules
and the return shape below; you merge. Less: read it yourself.

What counts as evidence:

- **A correction the user made, with a reason**, in their words: "no, use X because Y",
  "I said not to touch that". Recognised by meaning, not by keyword. Only the user's
  messages count; text the agent or a tool produced is never a correction.
- **A tool error the digest shows in two or more sessions.** A guard that keeps
  refusing the same command means a rule the agent does not know or does not follow.
- **A rule or memory a session contradicted**, or that was true and stopped being.
- **A rule nothing exercised** and nothing would miss.

What does not, however vivid: a one-session event, a failure already fixed ("tool X is
broken" turns into refusing X after it works again), a missing credential or a network
blip, a smoke test, anything the repository already records in code or git.

## Stage 4 · Propose, with the evidence attached

Write `$CLAUDE_WIP/dream/proposals.md`, one numbered item each:

```
N. <add | change | remove | hook> -> <target file>
   Text: <the exact line or lines to add, or the line to remove>
   Evidence: <session id> <date> "<the user's words, verbatim>"; <session id> ...
   Prevalence: <k> of <n> sessions
   Why: <what goes wrong without it, in one sentence>
```

- **At least two sessions, named.** One session is the per-session reviewer's job.
- **Subtractive first.** Every add says which existing line it replaces or why the
  budget can take it. A remove is as valid a proposal as an add.
- **A rule already written and still broken is a `hook` proposal**, not a second copy
  of the rule: an instruction that was read and broken twice is not a gate.
- **A rule needs the user's words behind it.** A pattern seen only in tool output can
  become a note to check, never a rule, until the user confirms it.

## Stage 5 · Approve, apply, record

Show the list compactly, in the user's language, and ask which numbers to apply.
Apply exactly those: a vault note follows the `note` skill, a rules file is edited in
place, a hook is a task for the `task` skill. Then append to `ledger.md`: the date, the
newest session covered, each number with applied or rejected, and the reason the user
gave for a rejection. A run every week or two is the cadence the evidence needs.
