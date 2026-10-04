---
name: polish
description: Polish a branch by reviewing, QAing, fixing, and simplifying it in rounds until nothing worth fixing remains. Use when the user asks to polish a branch, or when another skill needs a branch polished.
---

A **round** is one sweep of review passes, then the fixes they earn. The **ledger** is every finding from every round with its **disposition**, kept in a file so it survives a restart. Every pass and every fix runs in a sub-agent.

## 1. Establish the scope

The fixed point is the one the user named, else the current branch's merge-base with its base branch. Commit any uncommitted changes per `/commit` first, so every pass reads the same tree.

Find the spec once: the one already in this session, issue references in the commit messages, the open PR, or a spec file matching the branch under `docs/`, `specs/`, or `.scratch/`. If none turns up, ask the user once. The spec, or its confirmed absence, goes into every brief.

Browser QA is **live** when the app is browser-driven and the change under review touches something a user sees. When it is, dispatch a sub-agent to set up the **fixtures** every round's QA reuses: the test data the affected flows need, built with the project's seeds or the **run** skill. It returns each fixture with how to reach it (ID, URL, or sign-in), and where each flow's effects land outside the app, such as a CRM record or an analytics event.

Done when you hold the fixed point, the spec, whether QA is live, and, when it is, the fixtures.

## 2. Run the passes

Dispatch each pass in the round's plan as its own sub-agent, all in parallel. Each brief carries the exact commit range to review (`<from>..HEAD`) and the ledger file, so the pass skips findings the ledger holds as **won't fix**, **defer**, **ask**, or **settled**. It names the skill to invoke and asks for the findings back as a list: file, line, one-line claim, why it matters. A `/browser-qa` pass's brief also carries the fixtures and where effects land.

Round 1's plan is every pass against the fixed point:

- `/code-review` at `high` effort.
- `/mattpocock-skills:code-review`.
- `/browser-qa`, when live.

Done when every pass in the plan has returned its list. A reply without the list means the pass is still working: message it to finish and send the list.

## 3. Triage

Merge the lists into the ledger, collapsing findings that make the same claim into one entry naming its sources. Then give each new finding its disposition, on its face:

- **fix**: valid, and fixed this round.
- **won't fix**: invalid, or the change costs more than it earns. Keep the one-line reason.
- **defer**: valid, but separate work.
- **ask**: the fix is hard to reverse and you lack a strong case for which way to go. Hard to reverse looks like a public API's surface, a schema or migration, deleting data, or a rename that ripples past the diff. Keep the candidate fixes, your recommendation first.
- **settled**: its fix would undo a fix from an earlier round. This is **oscillation**: the earlier fix stands. Name that fix.

A **fix** finding that is a bug an earlier round fixed, back by a new route, is a **recurrence**: that fix was too shallow, so its fix brief names the earlier fix and targets the shared cause.

From round 2 on, a naming finding, test names included, is a **fix** only when the name **misleads**: it claims something the code doesn't do, or contradicts the project's glossary. A name that could merely be better is **won't fix**, so later rounds stop relitigating names earlier rounds chose.

Done when every finding in the ledger carries a disposition.

## 4. Fix

Cluster the **fix** findings by file: one sub-agent per cluster, in parallel, each briefed with its findings. Each brief asks the sub-agent to:

- Confirm each finding holds before changing code.
- Fix the class: find the same bug elsewhere and fix those instances too.
- Trace every path into the code it changes and run the tests that cover it, so the fix lands no **regression**.
- Return what it changed, which behaviour moved, and what it checked and left alone, with why.

Each item left alone enters the ledger as **won't fix** with that reason. Commit per `/commit`.

Done when every **fix** finding is committed or moved to **won't fix**.

## 5. Plan the next round

When this round fixed nothing, go to step 6.

Otherwise, plan the next round's passes. A **settled** finding this round predicts more oscillation, so lean toward skipping passes, narrower ranges, and lower effort.

- **Range**: the commits since this round began for contained fixes; the fixed point when a fix reshaped the change.
- **Effort**: `low` for small, local fixes; `medium` when a fix changed control flow, error handling, or state shared across callers, or fixed a **recurrence**.
- `/mattpocock-skills:code-review` runs only when a fix changed behaviour.
- `/browser-qa` runs only when live for the fixes' diff.
- After a **dense** round 1, one that fixed many findings, round 2's `/code-review` covers the fixed point: a dense round leaves misses in unchanged code.

Each brief names the fixes behind its range, so the pass hunts **regressions** in them.

Done when you have stated the plan to the user: every pass run or skipped with its reason, and each that runs with its range and, for `/code-review`, its effort. Return to step 2 with the plan.

## 6. Simplify and tidy

Dispatch `/simplify` in a sub-agent over the branch diff, once, and commit per `/commit`. Then do the same with `/tidy`. When either changed anything, dispatch `/code-review low --fix` in a sub-agent over their commits, and commit per `/commit`.

Done when simplify's and tidy's changes and the review's fixes are committed.

## 7. Report

Report in this shape:

- One or two opening lines: whether the branch is ready or has items that need the user, and the rounds run, flagging more than three.
- `## Fixed`: each **fix** finding, one line apiece.
- `## Won't fix`: each with its reason; each **settled** finding names the fix that stands.
- `## Needs you`: each **ask** with its candidate fixes, your recommendation first; then each **defer** as a plain item to act on.
