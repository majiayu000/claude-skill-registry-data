---
name: ask-arman
type: Skill
title: "ask-arman — the homework gate, the Question Desk, and the interview"
description: "The gate and path for any question an agent wants Arman to decide. Use when about to ask him anything, ending a turn on a question for him, writing 'needs Arman's decision', marking work blocked on him, or on /ask-arman. NOT for a step only he can perform (use a guided session)."
tags: [questions, decisions, arman, discipline, operations]
timestamp: 2026-10-02T00:00:00Z
---

<!-- SYNCED COPY — do not edit here.
     Canonical: common-docs/skills/ask-arman/SKILL.md
     This file is distributed to every consuming repo by
     common-docs/meta/scripts/sync_skills.py. Edit the canonical, run the
     sync, and commit each repo. Edits made here are overwritten and lost. -->

# ask-arman — the homework gate, the desk, the interview

How every sentence to him is shaped: [talk to Arman like a person](/policies/talk-to-arman-like-a-person.md).
Default to stating numbered
decisions, then one "confirm and I start". This skill is the path a real question travels.

## 1. The homework gate — run in order, record each result

The first test that says "not a question" ends it.

0. **Boss or user?** Would the question exist if he had never used the product himself? A
   question about ONE organization's content, taste or settings is a customer's: make it an
   onboarding step, a starter kit, or a knob with a default ([ask the boss](/policies/talk-to-arman-like-a-person.md)).
0b. **Does any answer change what he will see?** If not, decide and record it.
1. **A fact?** Code, the DB, a doc or the web settles it: look it up (a `quick` lane if tedious).
2. **Already ruled or delegated?** Grep the SUBJECT nouns across the owning node's
   `DECISIONS.md` and `VISION.md`, the vocabulary lexicon, [conflicts](/operations/conflicts.md),
   and `question_desk(action='list_answers')`. A dated ruling → apply and cite it. "Research the
   best and decide" → decide, record the reason in `DECISIONS.md`, tell him.
3. **Table stakes, a knob, a limit or a number?** Decide it
   ([table stakes](/policies/talk-to-arman-like-a-person.md),
   [limits are knobs](/policies/limits-are-knobs-agents-set-them.md)).
4. **Do the champions agree?** ([champions](/policies/champions.md)) Do what they do, name
   who, list it as "decided — override by number".
5. **A human step?** His account, his screen, money, a credential → one guided session in chat
   ([rule 11](/policies/talk-to-arman-like-a-person.md)), not a question.

## 2. Never stop — the default in force

Write which way you go if he never answers, how it reverses, and keep building on it. Only a
**one-way door** (real data deleted, money spent, something sent outside, a contract bound)
waits; everything around it proceeds.

## 3. File it on the Question Desk

The desk is the in-app surface `/administration/question-desk/<interview id>`, driven by the
AI Dream MCP tool `question_desk`. There is no markdown ledger.

1. `question_desk(action='list_interviews')`, then `get_interview` on the open ones; a question
   on the same subject exists → add yourself through `update_question` (`also_asked_by`), adopt
   its default, stop.
2. Otherwise `create_interview` (respondent Arman; needs full MCP access) or reuse an open one,
   then `add_question` with `slug`, `title`, `question` and `fields`: the five parts
   (`ruled_before`, `the_best_do`, `today`, `implications`, `recommendation`), `background`,
   `default_in_force`, `door`, `node` (a real `systems/…` or `projects/…` path), `checked`
   (your gate results), `filed_chat_title`, `filed_session_id`.
3. `update_question(status='researched')` once all five parts are filled (the tool refuses
   otherwise).

## 4. Say it in chat

Number it, one or two sentences a stranger needs, ONE direct question, the best practice and
your recommendation (or "this one is open-ended"), then the admin URL the tool returned and:
*"I'm proceeding on my recommendation, which is reversible."* No path, id, code or codename in
the sentence. Keep working.

## 5. Interview mode (/ask-arman when he has time)

1. **Gather:** every open question across `list_interviews` and the owner questions in
   [conflicts](/operations/conflicts.md). Merge duplicate subjects.
2. **Re-run §1 for every asker.** Close what fails with its reason and evidence; a rescue of a
   closed row must show the ruling is absent.
3. **Research survivors:** one `standard` brief per question fills the five parts with sources;
   tag kind (quick/complex), door, weight.
4. **Rounds:** open with "I have N questions to ask you and M things to tell you"; the things
   first. Then rounds per the [grilling](/skills/grilling/SKILL.md) mechanics in plain numbered
   chat text, `mark_asked` as each goes out, closing with how many remain and "anything you skip
   ships with my recommendation". "I don't know" means the question failed: back to research.
5. **Record:** answers he typed in the admin surface are already on the row; an answer given in
   chat → `record_answer`, verbatim. Then the owning `DECISIONS.md` (his words → `VISION.md`).
6. **Deliver:** the asking chat gets one paragraph (question, verbatim answer, where recorded)
   via `SendMessage`, or `claude --resume <session> -p` when it is closed; then
   `mark_delivered`. Drain the agent half of `work_loop` campaign `question-desk`
   (`qd:overturn:*`, `qd:decide:*`, claimed by exact key) until `status` shows nothing claimable.
7. **Close:** answered, closed-without-him (one line each), remaining, chats he must poke.

Never create a schedule for this ([no unapproved schedules](/policies/no-unapproved-schedules.md)).

## 6. Picking up your answer

On resume: `question_desk(action='list_answers')` (or the bounded `wait_for_answers` when idle),
read it verbatim, apply it, reverse the default where it differs.

## Rationalizations

| Excuse | Reality |
|---|---|
| "This needs Arman's decision" | Tests 1–4 were not run. |
| "It's blocked on him" | Only a one-way door blocks. |
| "I don't guess on a permissions question" | Champions decide it; the default is reversible. |
| "I end my turn there on that one question" | File it, say it, keep building. |
| "Which one do you want?" | A fork without a recommendation is homework handed to him. |

## Red flags

- "Let me check with Arman before I…" before grepping `DECISIONS.md`.
- "Blocked" in your status with no one-way door.
- A question containing a path, a code, or "see".
