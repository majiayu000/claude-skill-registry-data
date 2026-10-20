---
name: explore-app-for-bugs
description: >-
  Load this skill when the running app itself must be tried for bugs: launch it, explore the
  changed areas, report each bug with repro steps. Report-only unless asked to fix. Trigger on "QA
  this", "click through the app and find bugs", "try to break it", "smoke-test the feature".
argument-hint: "[report | fix] [area]"
disable-model-invocation: false
user-invocable: true
compatibility: >-
  Needs whatever the target app needs to run locally (its runtime, package manager, database).
  Driving a web UI needs the Claude in Chrome tools in the main session, or Playwright through the
  project's own setup; without either, only a CLI or HTTP API can be explored.
license: Apache-2.0
---

# Explore app for bugs

Use the running app the way a hostile, careless, and hurried user would, and write down every bug
with steps that make it happen again. The task is done when every charter has run to its budget or
found its bug, and the report lists each bug as confirmed (reproduced twice) or unconfirmed.

Pick the mode from `$ARGUMENTS` or the request: **report** (default) changes no code, **fix** fixes
each confirmed bug after the report is written. Fix mode runs only when the user asks for it.

## Procedure

1. **Launch the app locally.** Use the project's own launch skill or documented start command, or
   Claude Code's `run` skill. Record the commit, the command, and the URL or entry point. Never
   point this at production or a shared environment: exploring creates, edits, and deletes data.
2. **Write the charters.** From the diff against the main branch (or the area the user names), list
   what changed and every flow that passes through it. Write one charter per risk, in this form:
   `Explore <area> with <technique> to find <risk>`, each with a budget of about 20 actions. Three
   to six charters is a session. Without a diff or a named area, chart the app's main flows.
3. **Run each charter.** Drive a web UI through the Claude in Chrome tools, a CLI through the
   shell, an HTTP API with `curl`. Work through the techniques that fit the charter:
   - Inputs: empty, one, many, the maximum, past the maximum, unicode and emoji, leading spaces,
     pasted rich text, a value of the wrong type.
   - Sequence: back button and refresh mid-flow, double submit, two tabs on the same record, leave
     and return, the steps in the wrong order.
   - State: a new user with no data, a user with a lot of data, logged out, a role without the
     permission, an expired session.
   - Environment: a slow or dropped network, a narrow window, a dependency that is down.
     After every action, read the console errors and the failed requests (4xx and 5xx), not only the
     screen: a page that looks fine while a request fails is a bug.
4. **Confirm each bug.** Reproduce it a second time from a clean start with the fewest steps that
   still trigger it. Capture the evidence: a screenshot, the console line, the response body, or
   the command output. A bug that would not happen twice is listed as unconfirmed, never dropped.
5. **Write the report** in the Output shape.
6. **Fix mode only:** take confirmed bugs in severity order. Find the cause first, then fix it with
   a failing test first (`ceh-coding-conduct:find-root-cause` and `ceh-testing:test-a-bug-fix`, when
   installed). Re-run the bug's reproduction steps after the fix and record the result in the
   report.

## Rules

- **Severity comes from what happened**, on this scale: **Critical** loses or corrupts data,
  crashes, or exposes something to the wrong user. **Major** breaks a flow with no workaround.
  **Minor** breaks it with a workaround. **Cosmetic** is visible but changes nothing a user can do.
- **Report-only means no edits**, not even an obvious one-line fix. The user asked what is broken,
  and a quiet fix hides it from the report.
- **A finding is a bug, not a preference.** Confusing wording, layout, or flow goes in a separate
  usability list and to `ceh-usability-audit`, so the bug list stays something a developer can
  act on.
- **Leave the app as you found it.** Delete the test data you created, or list it in the report
  when deleting it would itself need a code path you are testing.

## Output

Write `.agents_workspace/qa/<YYYYMMDD-HHMM>/QA_REPORT.md`, timestamp from one `date` call, with
screenshots and logs beside it.

```markdown
# QA report: <app> at <commit>

**Launched with:** `<command>` → <url or entry point>
**Mode:** report | fix

## Charters

| Charter                                        | Actions used | Bugs  |
| ---------------------------------------------- | ------------ | ----- |
| Explore <area> with <technique> to find <risk> | <n>/20       | <ids> |

## Bugs

### <ID>: <Critical|Major|Minor|Cosmetic>: <one-line title>

- **Status:** confirmed (reproduced twice) | unconfirmed
- **Steps:** 1. ... 2. ... 3. ...
- **Expected / actual:** <...> / <...>
- **Evidence:** <screenshot path, console line, response body>
- **Fix (fix mode):** <commit and the re-run result>

## Usability notes (not bugs)

## Not explored

<flows, roles, or environments no charter covered, and why>
```

## Stop conditions

- The app will not start from its documented command → report the exact error as the first bug
  and stop. Exploring a half-started app produces noise.
- A flow needs real credentials, a payment, or a third-party account → explore up to that
  boundary, list the rest under Not explored, and never invent credentials.
- A bug looks like a security hole (another user's data, an unauthenticated write) → report it as
  Critical at once, and do not probe further than it takes to confirm.
