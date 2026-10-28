---
name: reflect-gate
description: >-
  Use when the user asks to close a session by auditing it AND writing the fixes
  into the project's instruction files — audits, applies and commits the edits,
  then asks whether to push. Not for a reflection that only reports findings.
---

<!-- GENERATED FROM framework/atoms/reflect-gate.md via scripts/generate-skill-composites.ts — DO NOT EDIT BY HAND -->

# Reflect Gate

## Overview

Runs after the work has landed. Audits the session, criticises its own
findings, applies the corrective edits to the project's instruction files,
reports each edit concretely, commits them, and asks whether to push that
commit — a refusal takes the commit and the edits back.

## Context

<context>
Split out of the commit workflow on 2026-08-17. Held inside `commit` the branch
had no hand-off form, so a composite that placed `commit` before another phase
lost that phase. The audit is performed HERE, inline — this atom does not
invoke the `reflect` skill or any other skill to do it. A sub-run ends with a
report, a report reads like the end of the work, and the turn stops there:
measured 2026-08-19, one run in three ended on the sub-run's report with the
Push Phase never reached. Inline steps have no such ending.
</context>

## Rules & Constraints

<rules>
1. **No delegation**: perform the audit yourself with the steps below. Do NOT
   invoke `reflect`, `reflect-by-history`, or any other skill for it.
2. **Apply and commit without asking; ask only about the push**: the edits and
   their commit are local and reversible, so you make both yourself. The one
   question in this atom is whether to push that commit, and it is the only
   place here where stopping is correct. A refusal is a verdict on the edits
   themselves, not just on the push: you take both the commit and the edits
   back.
3. **Scope of edits**: the project's own instruction files, tracked in this
   repository — `AGENTS.md`, `**/CLAUDE.md`, and the rule/skill files they
   point at. Never application code, never a task file, never SRS/SDS, and
   never your own memory store in place of them.
4. **Git Pager**: use `GIT_PAGER=cat` for all git commands.
5. **Error Handling**: on any error (commit failure, unexpected git state):
   investigate the cause, propose a fix to the user, and **STOP** without
   making corrections.
</rules>

## Instructions

<step_by_step>
1. **Decide whether this session earned a reflection**
   - Scan the conversation and the invocation message for complexity signals:
     - Errors or failed attempts (test failures, lint errors, build errors).
     - The same action retried more than once.
     - The user correcting your approach or output.
     - Workarounds or non-obvious solutions.
     - Explicit descriptors in the invocation message — "rough session", "had to retry", "wrong approach", "failed", "had to correct you". These count on their own.
   - **Say the verdict aloud either way** — one line: `Session complexity: none detected — skipping reflection`, or `Detected retries and a user correction — reflecting`. A silent skip is indistinguishable from a forgotten step.
   - No signals → skip to the final step. Signals → continue.
   - Do NOT ask whether to reflect. That is not the user's call here; the one question in this atom comes at step 6, and it is about pushing.

2. **Audit the session**
   - **Execution flow**: where did the work go wrong, and what did it cost — failed commands, wrong assumptions, rework.
   - **Logic patterns**: looping (retrying without changing strategy), blindness (ignoring a "file not found" or a linter error), stubbornness (forcing a solution that does not fit).
   - **Technical decisions**: proportionality, conformance to existing project patterns, abstraction fit, explicit error handling, robustness, obvious inefficiency, input validation, dependency justification, and fallbacks nobody asked for.
   - **Context gaps**: project docs never opened, related source never read, relevant skills or rules never consulted, verification skipped, ambiguities resolved by guessing instead of asking.
   - **Context waste**: files read but never used, whole files read for one fragment, the same unchanged file read twice, verbose tool output that added noise.
   - **Undocumented discoveries**: knowledge gained here that changes how the project is built, run, tested or deployed. Keep what generalises; discard the one-off.
   - **Stale instructions**: anything the project instructions told you that the repository contradicted — a command or task that does not exist, a path that moved, a convention the code does not follow. Compare the commands the instructions name with the ones the project's manifest defines.
   - **Automation opportunities**: a repeated multi-step sequence (→ a skill), an undocumented convention (→ a rule), an invariant you checked by hand (→ a hook).

3. **Criticise your own findings — before you touch a file**
   - **Validity**: is each finding backed by something you can quote from this session, or is it inference? Drop or downgrade the inferred.
   - **False positives**: reading a neighbouring file to learn the pattern is not wasted context; updating a test after a deliberate behaviour change is not test-fitting.
   - **Proportionality**: a one-off annoyance does not earn a new rule. Simplify anything disproportionate. This limits NEW rules only. A line in an existing instruction file that this session proved wrong is corrected on its first sighting, however rarely it bites: fixing a fact is not adding a rule. A "read-only" marker on `AGENTS.md` keeps task notes out of it; it does not protect a wrong fact in it.
   - **Blind spots**: which whole categories did you not look at — security, performance, documentation?
   - **Severity**: a pattern seen twice with different root causes is not recurring.
   - Say what this pass changed and why. What survives it is what you are about to write into the user's files.

4. **Apply the corrective edits**
   - Edit the instruction files directly. Each edit states the rule and the reason it exists, in the voice of the file it lands in.
   - **They land in the project's own tracked files, inside the repository working tree** — `AGENTS.md`, `**/CLAUDE.md`, and the rule or skill files those point at. Confirm it: the path you edited must appear under `git status`.
   - **Your own memory store is not a corrective edit.** Writing the lesson into the agent's persistent memory (a `memory/` directory under your home, a personal notes file, anything outside the repository) feels like it captures the finding and does not: it is not versioned, it does not reach anyone else working here, and a fresh checkout has none of it. It is also how this step gets silently skipped — measured 2026-08-19, one run in three wrote to `memory/` and reported there was nothing to commit. Use it in addition if you like, never instead.
   - One edit per surviving finding. A finding that produces no concrete edit is a report line, not a corrective action — say so and move on.
   - Keep them small and local: tighten an existing rule where one exists, add a new one only where none does.

5. **Show the edits and commit them — no question here**
   - List what you changed, file by file: the path, the section, what the rule now says, and which finding it came from. The user must be able to judge the edit from this list without opening a diff.
   - Then commit, in this same turn, without asking. The edits are already written; a commit of what is already on disk adds no risk the edit did not, and both are undone by one git command. Do not offer to commit, do not wait for encouragement.
   - Run `git status`. Stage ONLY the files you edited in step 4, by explicit path — never `git add -A`, never `.`; a working tree you did not touch is not yours to commit.
   - Commit with type `agent` and a scope naming what you tightened: `agent: apply reflect-suggested improvements`, or narrower, e.g. `agent(commit): tighten the doc-audit gate`. The type is `agent` because the change is to the agent's own instructions — never `docs:`, `chore:` or `feat:`, whatever the file extension says. Never amend an existing commit.
   - **Do not skip this step by not editing.** If the audit produced findings and you applied none of them, say why in one line — silence here reads as a clean session, and it was not.

6. **Ask whether to push it — and end your turn on the question**
   - This commit sits on top of whatever the calling workflow already pushed, so it is local until somebody sends it. That is why the question exists: it is the one thing here that reaches beyond this machine.
   - Ask, in one line, naming the branch: `Committed as <sha> on <branch>. Push it? Reply "yes" to push, or "no" to drop the commit and the edits with it.`
   - **Write nothing after the question until the reply arrives.** A question followed in the same breath by "pushing now" is not a question, it is an announcement — the user never got to answer. **You may not answer it on the user's behalf**: no pre-authorization carries over to a push, whatever the calling workflow already did.
   - On `yes`: run `git push` with no flags, then verify `git rev-parse @{u}` matches `HEAD` and say so. **Never `--force`, never `--force-with-lease`, never `--set-upstream`.** If the branch has no upstream, or the remote has commits you do not, do NOT improvise: report it and tell the user to run the project's push workflow, which owns those decisions.
   - On `no`: the edits are not wanted. Undo the commit and the edits together — a declined improvement left sitting in the branch is the same unwanted change, one `git log` further away.
     - **Check two things first, then it is one command.** (a) `git rev-parse HEAD` still equals the sha you reported — nothing landed on top of your commit. (b) `git status --porcelain` prints nothing — the tree carries no other work. Both hold by construction here: the earlier phases committed and pushed everything, and you committed your own edits in step 5.
     - Both true → `git reset --hard HEAD~1`. That is the whole undo: the commit and the file contents go together, and there is nothing to restore by hand.
     - Either check fails → **STOP and change nothing.** A `--hard` reset discards uncommitted work outright, and whatever made those checks fail is work you did not put there. Report what you found, leave your commit in place, and let the user decide.
     - Then confirm with `git log -1` that your commit is gone, and say in one line what you removed.

7. **TOTAL STOP**
   - Report in one line whether the reflection ran, what it changed, under which commit, and whether that commit was pushed. Then stop.
</step_by_step>

## Verification

<verification>
- [ ] Complexity verdict spoken aloud either way.
- [ ] Audit and self-criticism performed inline, without invoking another skill.
- [ ] Corrective edits applied and listed file by file.
- [ ] One `agent:` commit staging only the edited files, made without asking.
- [ ] Push question asked, and answered by the user before anything was pushed.
- [ ] On refusal: both guards checked, then one `git reset --hard HEAD~1`; on a failed guard, nothing changed at all.
</verification>
