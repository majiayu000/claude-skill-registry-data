---
name: investigate-bug
description: >-
  Finds the cause of a bug in an Umbraco package or backoffice extension: reproduces it,
  gathers evidence, and tests one hypothesis at a time until the cause is proven. Never
  writes the fix; routes it to `quick-fix` or the feature pipeline. Use for "why is this
  broken", "this stopped working", an unexplained failing test, or an issue triaged as
  needing investigation. `--unattended` runs without questions in its own worktree.
user-invocable: true
argument-hint: <what's going wrong, or an issue ID> [--unattended]
---

# investigate-bug

A fix aimed at a guessed cause often moves the bug instead of removing it. This skill finds
the cause first and proves it, so the fix lane (`quick-fix` or the pipeline) starts from a
known cause and a repro, not a theory.

## Scope

- IN: reproduce, gather evidence, narrow, prove the cause, find other places with the same
  cause, write the report, draft the issue's update, suggest the route for the fix.
- OUT: the fix itself, and any lasting change to the project's code. Scratch work (a
  throwaway test, a script, temporary logging) is allowed, but it's removed before the
  hand-off. Investigation leaves `git status` as it found it.

## Argument

`$ARGUMENTS` is the symptom in the user's words, or an issue ID. For an issue ID, read the
issue, and use this session's `issue-triage` report for it if there is one, or else the
issue's latest triage notes.

## Running unattended

`--unattended` means nobody is there to answer questions. Only pass it to a run in its own
worktree, where nothing it does can disturb the user's checkout. The steps below still
apply, with these changes:

- **No questions.** Work from the issue and its notes. If step 1 or step 2 needs something
  only the reporter can give, stop there and suggest `state/needs-info`.
- **No asking before `git bisect`.** The worktree is yours alone. Still end with `git bisect
  reset`.
- **The demo site** runs on this worktree's own port (`git wdp-port`), never a fixed one.
- **Leave the worktree clean**, as Scope says, so it's removed when you finish.
- **A security match** still stops everything: return only the flag and the issue ID.

## 1. Pin down the symptom

Before reading code, get these. Ask for what's missing, one question at a time:

- **Steps.** What the user did, in order, and where (backoffice screen, front-end page, API
  call, background job).
- **Expected and actual.** What should have happened, and what did instead, word for word
  for any error.
- **Where it runs.** CMS version, package version, database provider, browser if it's
  backoffice, single server or load-balanced.
- **When it started.** Always, or since an upgrade, a deploy, or a config change.

A vague symptom ("saving is broken") gets one round of questions, not a guess.

**Security check.** If the symptom matches what `issue-triage`'s Security reports section
counts as a vulnerability, stop and follow that section.

## 2. Reproduce it

Reproduce through the real entry point, in the first way the project supports, using the
same order as `feature-build`'s "Smoke the real entry point" step: an e2e test, the demo
site (drive the backoffice, or send the real Management API request), or an integration test
that boots Umbraco.

- Write the repro down as exact steps or a scratch test. It goes in the report.
- **Can't reproduce?** Check the "Where it runs" details against your setup and change one
  thing at a time toward theirs (database provider, version, config, data). If it still
  won't reproduce, stop and report what you tried and what you'd need from the reporter. An
  unreproduced bug doesn't get a fix.

## 3. Gather evidence

Look before theorising. Collect what the failure leaves behind:

- **Server log.** `umbraco/Logs/UmbracoTraceLog.<machine>.<date>.json` in the site folder,
  one JSON object per line (Serilog's compact format). Search it for errors and warnings
  around the repro, and for the package's own `SourceContext`. The backoffice shows the same
  log under Settings › Log Viewer.
- **The API response.** For a backoffice bug, the Management API request behind the screen:
  status code and body (a `ProblemDetails` body names the error). Read it from the browser's
  network panel or send it yourself.
- **The browser.** Console errors and failed network requests, read with Playwright or the
  browser tools. A backoffice extension that never loads usually shows here first.
- **The data.** If the symptom is wrong data, read the rows themselves on the database the
  user runs.

Quote what you find (log line, status and body, console message) in the report.

## 4. Narrow it down

Cut the search space before reading code in depth. Use whichever of these splits fits:

- **Backend or frontend.** Does the Management API return the right thing? If yes, the bug
  is in the client. If no, it's on the server.
- **Package or CMS.** Does it happen without the package, on a plain Umbraco site at the same
  version? If yes, read the CMS at that tag (`umbraco-cms-source`) and search its issues
  (`gh search issues --repo umbraco/Umbraco-CMS "<error text>"`). A CMS bug gets reported
  upstream and worked around in the package, not patched inside the package.
- **Which change.** If it used to work, find the change that broke it. Read `git log` for the
  area first. If that doesn't find it and the repro can run as a command, use `git bisect
  run` with it. Bisect checks out old commits, so it needs a clean working tree: **ask the
  user before starting**, and always end with `git bisect reset`.
- **Which data or config.** If it only happens for some content, users, or settings, compare
  one that fails with one that works and change one difference at a time.

`references/umbraco-suspects.md` lists where Umbraco bugs often hide. Check it once the
search space is small, not before.

## 5. Prove the cause

Work one hypothesis at a time:

1. State it as a cause that would explain every piece of evidence so far.
2. Name a check that would prove it wrong: a log line that should or shouldn't appear, a
   value read in the debugger, a scratch test, a one-line temporary change.
3. Run the check and record the result, whichever way it goes.

A cause is proven when changing it changes the symptom: the scratch test fails with the
cause in place and passes with it removed, or the repro stops failing. "This code looks
wrong" isn't proof. If the evidence contradicts every hypothesis, go back to step 3 for more
evidence rather than inventing a fourth.

Then name the cause, not just the line (a missing permission check, a scope that's never
completed, an alias two extensions share), and grep for other places with the same cause.

If the package's own docs and its code disagree, don't pick a side. Docs drift, but they're
also what users were told to expect, so which one is right is the maintainer's call. In the
report, ask "which is right?" and give both fixes: change the code to match the docs, or
change the docs to match the code, each with what it means for users. (This is about the
package's docs. For how the CMS itself behaves, `umbraco-docs`' "Source wins" still holds.)

Remove every scratch change, end any bisect, and check `git status` matches the start.

## 6. Report

Write the report in chat:

```markdown
**Symptom:** <one line>
**Repro:** <exact steps, or the scratch test's code>
**Cause:** <the cause, at file:line> (<CMS tag or commit, if relevant>)
**Evidence:** <the check that proved it, and its result>
**Same cause elsewhere:** <file:line per place, or "none found">
**Suggested fix:** <one or two lines, and the test that should guard it>
**Route:** <quick-fix | feature-explore | upstream CMS issue>, because <one line>
```

**If the argument was an issue ID**, also draft the issue's update, following
`issue-triage`'s State labels and Tracker comments sections:

- Cause proven → `state/ready`, its notes filled from the report.
- Can't reproduce, and only the reporter can close the gap → `state/needs-info`, asking for
  what step 2 found missing.
- Not a bug (works as designed, or a usage mistake) → a close, saying why.
- Cause is in the CMS and no package workaround is planned → `state/blocked`, linking the
  upstream issue once the user has posted it.

Then pick the route for the fix, for the report's **Route** line:

- **An issue ID with a proven cause:** `issue-resolve` with that ID and the report, so the
  fix gets tracked on the issue.
- **Small fix** (one concern, the size `quick-fix` describes): `quick-fix`, passing it the
  cause, the repro, and the places with the same cause.
- **Bigger fix**, or a shared fix across several places: `feature-explore`, with the report as
  its starting material.
- **CMS bug:** draft an issue for `umbraco/Umbraco-CMS` with the minimal repro on a plain
  site, never posting it yourself. Route any package workaround as above.

If the cause is a mistake a future `builder` would likely repeat, offer to save it to
`.claude/memory/` as a `gotcha` (see `.claude/memory/README.md` for the format). If Claude
wrote the faulty code and a devkit skill should have prevented it, also suggest
`skill-report`, so the devkit learns from it.

## Rules

- No fix before a proven cause. A guessed fix gets reported as a guess, not shipped.
- One bug per run.
- Evidence beats memory. Quote the log line, response, or source line behind every claim.
- Never commit from this skill. Never write to the tracker either: the update is a draft,
  applied only as the Hand off says.

## Hand off

The report, the drafted update if there is one, and the route.

- **If another skill started this one**, return those and stop. That skill decides what to
  apply and what runs next.
- **Otherwise**, show the drafted update and apply it only on the user's yes. Then offer the
  route as a one-line question.
