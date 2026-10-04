---
name: user-ground-truth
type: Skill
title: "user-ground-truth — the person's own words, extracted by script, summarized by a fresh agent, judged against the work"
description: "Extract exactly what the person typed in a Claude Code session (script, no agent context spent), have a fresh agent write a faithful structured summary under it, and optionally have an adversarial agent judge whether the working agent is still on track. Use at a checkpoint, before a handoff, after a compaction, when a long session may have drifted from what the owner asked, or when told to 'summarize what I said' or 'check we're on track'."
tags: [agents, context, summary, ground-truth, drift, verification]
timestamp: 2026-09-16T00:00:00Z
---

<!-- SYNCED COPY — do not edit here.
     Canonical: common-docs/skills/user-ground-truth/SKILL.md
     This file is distributed to every consuming repo by
     common-docs/meta/scripts/sync_skills.py. Edit the canonical, run the
     sync, and commit each repo. Edits made here are overwritten and lost. -->

# user-ground-truth

A long session drifts from what the person asked for, and nobody notices because every later
agent reads an agent's paraphrase of him instead of him. This skill keeps his words as an
unaltered file, puts a faithful summary beside them (never in place of them), and lets a third
agent check the work against both. The principle is [reality is the referee](/policies/reality-is-the-referee.md):
his words are reality; every summary and every plan is a model of them.

## 1. Extract — a script, never an agent

```bash
python3 /Users/armanisadeghi/code/common-docs/meta/scripts/transcript_user_messages.py \
  ~/.claude/projects/<escaped-cwd>/<session-id>.jsonl -o <out>.md
```

The transcript is JSONL under `~/.claude/projects/` (the folder is the session's working
directory with `/` turned into `-`). The script keeps only top-level user turns that a person
typed: tool results, injected skill bodies, slash-command output, task notifications, the
compaction summary, cron wake-ups and the app's automatic "Continue from where you left off" are
all dropped (the harness marks its own turns `isMeta`). One entry per message: the time, then the
text verbatim. `--include-injected` keeps the dropped records, labelled, to audit the filter.

Never do this step by hand or by reading the transcript into an agent — it costs nothing as a
script and a fortune as context, and an agent "extracting" his words will tidy them.

Where the file goes: something the owner is meant to keep lives under
`common-docs/operations/for-arman/<date>/`; a working copy for a session lives in the scratchpad.

## 2. Summarize — a fresh agent, his instruction verbatim, appended below the raw text

Dispatch a fresh lane (`quick` is enough — this is reading, not judgment) with **only** the
extracted file and this instruction, which is the owner's own (2026-09-16) and is not to be
improved:

> Review this document: `<path>`. Do not read any other resources. These are the exact messages
> a user sent during a conversation with an agent. Your task is to create a clear, complete and
> coherent summary of what the user said in this conversation and what the user wants. The
> concept is to make it well structured, clean, complete and accurate. However, the chronology
> is not as important, unless the user changes their mind on something. In that case, you would
> state what was said first and what it became but always focus on the final version of that
> item. Do not include inconsequential things that are purely transitive messages or just
> meaningless things. Add your summary at the bottom of the doc in a clearly identified section
> you create. Your goal is to get everything, keep it clean and structured, but don't lose or
> change the meaning of what he said. You absolutely can clean up language and things like that
> as long as you're certain that you're not changing the meaning or intent.

Why "no other resources": a summarizer that has seen the codebase or the plan summarizes toward
them. Why appended, never replacing: the raw text is the check on the summary. A reader who
doubts a summary sentence finds the message it came from, or finds that it has none.

Commit the file after the summary is appended — an uncommitted summary is one regeneration from gone.

Known trap: his messages are often dictated. A transcription slip ("contact slots" for "context
slots") can be carried into the summary as a confident wrong term. The summarizer may not fix what
it cannot be sure of; the judge below, who knows the system, can.

## Poison and runaway — the two ways this turns on itself

**Poison.** The only source is the transcript. The words are regenerated from it on every run
and never edited; the script writes a marker under them, keeps whatever was appended below the
marker, refuses to overwrite a file that has no marker (it cannot tell appended text from the
words), and `--verify` recomputes the words and exits non-zero if the file's upper part differs —
a tampered ground truth is found in one command. A summary is derived from the words, never
from an earlier summary; a judge's note is derived from words + summary + the agent's claims, and
the claims are read as claims. Nothing derived is ever written above the marker. The first time
this skill was used, an uncommitted summary was lost to a regeneration — commit what you append.

**Runaway.** This is reached for at a decision — before a dispatch, a freeze, a "done", a
handoff, after a compaction — never on a clock and never every N messages ([no unapproved
schedules](/policies/no-unapproved-schedules.md)). One judge per checkpoint; never a judge of the
judge. The judge writes to the working agent, not to the owner; if it finds nothing, it says one
line and stops. A judge that runs constantly is noise wearing a badge.

## 3. Judge — optional, adversarial, and only useful if it looks at reality too

At a decision point — a dispatch, a freeze, a "done", a handoff, a resume after compaction — a fresh agent gets three things:
the raw file, the summary, and whatever the working agent currently claims (its plan, its last
status, its register). Its question is one: **is the work still what he asked for?** — where he
said it should appear, what he said it should do, what he said mattered most.

The trap that makes this step worthless: a judge that compares the summary to the plan finds
only inconsistencies of wording. The drift that costs weeks is the plan matching his words while
the *product* does not — because the working agent never stood where he stands. So the judge's
brief carries the concept, not a method: reality is the referee; go to the live product and the
live data as the person he describes, and report where his words, the plan and reality disagree.
Tell the working agent, in his terms, where it is off; never a score, never a checklist.

Cheap per run (a `quick` lane on the raw file is minutes); the judge that actually goes to the
product costs more and is the one worth paying for. It is not a substitute for the working agent
asking itself the three questions in the policy.

## 4. Auditing something already in flight

A project that has run for weeks across many sessions has the same disease in more places:
his words paraphrased into a register, work built beside what existed, "done" reported as
counts. The audit is the same three steps at project scale, and the concept is the same — the
audit finds what its briefer does not know, or it is not an audit:

1. One ground truth for the whole project: every session under the project's folder in
   `~/.claude/projects/`, merged and filtered — `--since` for the period, `--grep "<a phrase only
   he would have typed about it>"` to pick the sessions without reading any. Read the result
   yourself once; it is short and it is his.
2. A fresh summary beneath it (§2, his instruction verbatim).
3. A fresh judge (§3) with his words, the summary, and the project's own claims (register,
   handoff, status messages) — briefed with the situation and the result wanted, never a list of
   suspected defects. It goes to the live product as him and to the live data, and reports in
   his terms: what he asked for and where he would look for it; what is there; what was built
   somewhere else, beside something that already existed, or not at all; what was reported done
   that he cannot see. What the briefer already suspects is withheld and used as the test of the
   report.

The output for him is a page he can act on — what he will see, doing what he described — not
the judge's transcript.
