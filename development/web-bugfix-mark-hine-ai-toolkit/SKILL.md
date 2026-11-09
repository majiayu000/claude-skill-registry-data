---
name: web-bugfix
description: "Bug-fix playbook for React, Next.js and TypeScript web apps: reproduce (test or browser), root cause, minimal fix, regression test, review, commit."
---

Read the project AGENTS.md (or GEMINI.md) and applicable guidance first. Fall back to CLAUDE.md if AGENTS.md is absent. Follow global rules for optional tools, specialist subagents and Git actions.

# Bug fix: the user request

Repo facts (package manager, framework and router, scripts, test runners, dev URL) come from the project's `AGENTS.md` (or `GEMINI.md`).

1. **Restate** the symptom, expected behaviour, and affected route, browser or device if known. Branch `fix/<ticket>-<slug>`.
2. **Locate.** A research subagent returns the path from symptom to code (route → component → hook or data function → API) as `file:line` entries.
   Then read that whole path yourself, not the first suspicious line, because the subagent reads excerpts. `git log -S` for the change that introduced it.
3. **Reproduce.** Prefer a failing unit or component test in the module that owns the defect. For a bug that only shows
   in the browser, write a failing Playwright test when the repo has Playwright. Otherwise reproduce it with
   `/web-run-app`, and capture a screenshot plus the browser console or dev server log excerpt. Quote the failing
   output. If the bug does not reproduce, stop and report what you tried and the evidence still needed. Do not ship a speculative fix.
4. **Root cause.** One paragraph: what is wrong and why it produces the symptom. If a fix would only mask it (optional
   chaining that hides an undefined value, an Effect that patches state after render, `suppressHydrationWarning`, a
   `catch` that swallows the error), say so and propose the real fix. Ask `web-researcher` when a framework behaviour change is suspected.
5. **Fix** with the minimal diff. Note refactor candidates as follow-ups instead of doing them. If the test stays red, go back to step 4 rather
   than stacking changes. After three failed fixes, stop and report what each attempt showed.
6. **Verify.** Failing test now green plus the file's other tests, the type check and the lint script. For UI bugs, hand
   the captures, any Playwright run and the flow's journey (if one exists) to the `web-verifier` agent and quote its results. A unit-only rerun stays in this
   session, because `web-reviewer` runs the tests again.
7. **Review.** `web-reviewer` with the symptom and root cause as the task statement. Confirm each Blocker and Major against the code first, and decline a refuted one with the counter-evidence. Fix the rest, then re-run the type check and the affected tests. Send the same reviewer the finding IDs and their "Verified fixed when" criteria to re-review the fix delta. Stop after two re-review rounds and report anything still open.
8. **Commit, only if asked.** Follow the shared Git conventions. Do not push unless asked.
9. **Report**: cause, fix, evidence (test before/after, screenshots), regression risk, pre-existing issues noticed.
