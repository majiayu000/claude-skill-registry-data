---
name: address-review
description: Triage review findings with the user, then action them.
disable-model-invocation: true
---

**Triage** is a sorting pass: every finding lands on a **disposition** before any finding is actioned.

## 1. Get the review

A review is a set of findings — from a human or another agent — arriving as a file, a PR (or a PR comment), or session context. Take it from the first source that has one: what the user pointed you at; a review already in this session; the open PR for the current branch; otherwise ask the user.

Collect every finding into a list. Done when every finding from the source is on it.

## 2. Triage every finding

Judge each finding on its face — from what it claims and what you already know.

Present each finding as a one-line summary and offer its applicable **dispositions** as options (AskUserQuestion — one finding per question, batched up to four per call). Choose which dispositions fit and put your recommended one first.

- **fix** — valid, and should be fixed. Name the fix if the review suggests one or it's obvious to you; if several fixes are plausible, ask a follow-up to choose.
- **won't fix** — invalid, or you won't action it.
- **explain** *(interim)* — the user wants to understand it; you'll read the code and explain.
- **investigate** *(interim)* — you'll read the code to confirm whether it holds.
- **defer** — valid, but actioned as separate work (another task or issue).

Reading the code to settle a finding is itself a disposition — an interim one — chosen now and carried out in step 3.

Done when every finding has a disposition.

## 3. Action every finding

Run two tracks at once:

- **Foreground** — interim dispositions produce understanding, not outcomes; resolve them: explore the code (a subagent per finding), report back, and re-triage each with the user (as in step 2) into a final disposition — **fix**, **won't fix**, or **defer**.
- **Background** — action each final finding that's independent of every pending interim: implement the fix (a subagent per finding where fixes touch separate code) or file the deferral's issue. As re-triage lands newly final findings, action them too.

Done when every fix is made and every deferral filed.

## 4. Close the loop

Commit the changes. Write a summary with a line per finding — its disposition and what was done. If the review came from a PR, push the branch, post the summary as a comment, and mark the review resolved; otherwise report the summary to the user.

Finish by recommending whether a follow-up review is warranted. Done when the summary is delivered and, for a PR, every thread is resolved.
