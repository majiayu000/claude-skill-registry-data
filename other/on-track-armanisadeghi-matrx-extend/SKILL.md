---
name: on-track
type: Skill
title: "on-track — is this work still what he asked for? Find the conversation, extract his words, judge against reality, plan the remedy, bring him the choice"
description: "Run the full on-track check on a conversation, project, or keyword the owner names: find the sessions, extract exactly what he typed, dispatch independent judges who go to the live product as him and report what was missed, plan the remedy, and return one page — what he will see, what is missing, the plan. Use when told to check whether work is on track, to audit a project that has drifted, on 'run the on-track check on X', or when a long campaign is about to freeze, hand off, or claim done."
tags: [agents, verification, drift, audit, ground-truth, orchestration]
timestamp: 2026-09-16T00:00:00Z
---

<!-- SYNCED COPY — do not edit here.
     Canonical: common-docs/skills/on-track/SKILL.md
     This file is distributed to every consuming repo by
     common-docs/meta/scripts/sync_skills.py. Edit the canonical, run the
     sync, and commit each repo. Edits made here are overwritten and lost. -->

# on-track

The owner names a thing — a conversation, a project, a phrase — and wants to know whether the
work is still what he asked for, what was missed, and what it would take to fix. You own the
whole run and return one page. Mechanics of each step live in `user-ground-truth`; the concept
behind all of it is [reality is the referee](/policies/reality-is-the-referee.md): his words are
reality, every plan and register is a model, and the judges exist to let reality contradict the
model — so nothing you already believe goes into their briefs.

## 1. Find it without reading it

Sessions live under `~/.claude/projects/<cwd-with-slashes-as-dashes>/*.jsonl`. The desktop app's
session ids do not name these files; his words are the key:

```bash
python3 /Users/armanisadeghi/code/common-docs/meta/scripts/transcript_user_messages.py \
  ~/.claude/projects/-Users-armanisadeghi-code*/*.jsonl --list --grep "<a phrase only he would have typed>" [--since YYYY-MM-DD]
```

One line per matching session — file, dates, message count, opening words. Pick from that;
if he named a conversation title, the desktop session list gives its date and folder, and the
opening words confirm the file. Never open a transcript to find one.

## 2. His words, then a fresh summary

```bash
python3 .../transcript_user_messages.py <matching files...> -o <ground-truth>.md [--since ...]
```

Then a `quick` lane (Sonnet) with only that file and his summarization instruction verbatim
(`user-ground-truth` §2). Commit the file. Read it yourself once — it is short, and everything
you say to him later is measured against it.

## 3. Judges — what was missed

One or more fresh lanes (`standard`; more than one only when the work spans clearly different
surfaces, each judge owning one). Each gets: the ground-truth file, the summary, and the work's
own claims by path (register, handoff, status, plan). The brief carries the situation and the
result wanted — where he said it should appear, what it should do, what he said mattered most —
and asks for what he asked for and cannot see, what was built somewhere else or beside something
that already existed, and what was reported done that is not there. It does not carry your
suspicions; withhold them and use them as the test of each report. A judge must go to the live
product as him and to the live data; a judge that only compares documents to documents has not
judged.

## 4. Planner — what it would take

One fresh `standard` lane with his words, the summary, and the judges' reports: the remedy as a
plan in his terms — what changes where, what gets folded into what already exists, what gets
deleted (one path, never a twin), what he will see when it is done, and the order. It goes to
the product and the code too; it does not take the judges' word any more than they took the
builder's.

## 5. Back to him — one page and a choice

Lead with what he will see today doing what he described, then what is missing, then the plan,
then three offers, numbered, in plain sentences:

1. Fix all of it here, now, in this session.
2. Send the plan to the agent working on it — one message, once, naming that agent, only because
   he asked (Law 7's exception is his explicit request naming the recipient; nothing else).
3. Something else he has in mind.

Nothing is fixed, sent or scheduled until he picks. Counts, lane names and run ids stay out of
the page; the judges' and planner's reports are linked for anyone who wants them.

## What makes this worthless

Briefing the judges with what you think is wrong · a judge that never opens the product ·
summarizing the summary instead of his words · running it on a clock instead of at his ask or a
decision point · sending him the reports instead of the page.
