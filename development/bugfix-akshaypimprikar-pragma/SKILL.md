---
name: bugfix
description: Fix a reported bug with a regression test. Invoke with a bug description and reproduction steps.
disable-model-invocation: true
---

# Bug Fix Agent

You are the **Bug Fix Agent** for an iOS app project. Your job is to fix a reported bug with a regression test.

## Trigger
Invoked with a bug report: description + reproduction steps (e.g. `/bugfix "CSV import creates duplicate transactions when imported twice"`).

## Process

### 1. Create the branch
**Regular bug:** Branch `fix/<bug-name>` off `develop`.
**Hotfix (production bug on main):** Branch `hotfix/<bug-name>` off `main`, then merge to both `main` and `develop`.

Read `AGENTS.md/CLAUDE.md` before touching any file.

Also read if they exist — skip silently if absent:
- `.claude/context/invariants.md` — inviolable rules; ensure the fix does not violate any
- `.claude/context/rejections.md` — past review violations; ensure the fix does not repeat known bad patterns
- `.claude/context/incidents.md` — past bugs and their root causes; check whether this symptom matches one already diagnosed before investigating from scratch

### 2. Write the failing test first
Before changing any production code, write a test that:
- Reproduces the exact bug described
- Fails with a clear error message that matches the symptom

Run it to confirm it fails:
```bash
xcodebuild test -project <AppName>.xcodeproj -scheme <AppName> \
  -destination 'platform=iOS Simulator,name=<simulator from AGENTS.md/CLAUDE.md>' \
  -only-testing:<AppName>Tests/<SuiteName>/<testName> \
  2>&1 | grep -E "Test.*passed|Test.*failed|BUILD"
```

Do not proceed until it fails for the right reason.

### 3. Implement the minimal fix
Change only what's needed to make the failing test pass. Do not refactor, rename, or clean up surrounding code unless it's the direct cause of the bug.

### 4. Confirm the fix
- Run the new test — must pass
- Run the full test suite — must all pass, no regressions:
```bash
xcodebuild test -project <AppName>.xcodeproj -scheme <AppName> \
  -destination 'platform=iOS Simulator,name=<simulator from AGENTS.md/CLAUDE.md>' \
  2>&1 | grep -E "TEST SUCCEEDED|TEST FAILED"
```

### 5. Update CHANGELOG

Append a one-line entry to the `## [Unreleased]` section of `CHANGELOG.md` (create the section if absent). Skip only for internal refactors with no user-visible behaviour change.

### 6. Log the incident

Append an entry to `.claude/context/incidents.md` (create the file with a one-line header if it doesn't exist):

```
## YYYY-MM-DD — <bug name>
**Symptom:** <what was observed — error message, wrong behavior, exact repro condition>
**Root cause:** <one line — the actual mechanism, not just "logic error">
**Fix:** <file:line or brief description of the change>
**Search terms:** <keywords a future symptom description might match — error strings, type names, subsystem>
```

The point is a searchable root-cause record, not a duplicate of the CHANGELOG entry (which is user-facing) or the git commit message (which is buried in history until someone thinks to `git log` for it). Keep each entry to what a future `/bugfix` run skimming this file needs to recognize "this is the same thing" from a different symptom description.

### 7. Commit and PR

```bash
git add <changed files>
git commit -m "fix: <short description of what was wrong>"
```

**Regular bug:** Open PR to `develop`. The Review Agent (`/review`) runs on the PR.
**Hotfix:** Open PR to `main` — also open a second PR to `develop`. Both go through `code-review:code-review` and `/review` (via `/pr-followup`) before merging; `/test`'s coverage audit runs before `/gates`. Unlike `release/SKILL.md`'s develop back-merge (safe as a raw `git merge` because a release branch only ever contains commits `develop` already reviewed), a hotfix branches directly off `main` and its commits have never been through `/review` on `develop` — so its back-merge needs the same gate its `main` PR got, not a raw merge.

## Architecture rules
All fixes must respect the layer boundaries in `AGENTS.md/CLAUDE.md`:
- Domain Service fixes stay in `Services/`
- Repository fixes stay in `Repositories/` (implementation subfolder per your architecture)
- No business logic moved into Views to work around a bug

## Done when
Failing test passes, full suite green, PR open.
