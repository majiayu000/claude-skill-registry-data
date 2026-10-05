---
name: padosoft-ci-failure-triage
description: >-
  Use this skill when a test or a job is red in CI and somebody wants to know why — "the pipeline is red",
  "test X fails only in CI", "it passes locally", "the browser test is flaky", "fix the failing check on the
  PR". It is the procedure for collecting the complete evidence before forming a hypothesis: the full run
  log rather than the failed-step extract, every artifact, the application logs from the same window, and
  the correlation between them, ending in a classification — test defect, application defect, environment
  defect, or genuinely flaky — and a fix that names a file and a line. Do not use it to design the workflow
  (padosoft-ci-workflow-gates), to write the tests (padosoft-test-integrity), or to debug something failing
  in front of you locally.
license: MIT
compatibility: >-
  GitHub Actions and the `gh` CLI for the commands; the procedure applies to any CI that stores logs and
  artifacts. Browser-test examples assume a modern end-to-end runner.
metadata:
  version: 0.1.0
  author: Padosoft
  summary: The failed step says where the run stopped, not why — collect everything before diagnosing.
  profiles: devops
  scope: project
  repository: https://github.com/padosoft/skills
  keywords: ci, failing test, artifacts, triage, flaky, playwright, logs, diagnosis, github actions
---

# CI failure triage

The failed-step extract tells you **where the run stopped**, not why. The cause is frequently in a step that
passed — the database setup, the cache warm-up, the migration — or in a warning nobody reads.

**The rule: never propose a fix for a CI failure from the summary. Collect everything, correlate, classify,
then fix — naming the file and the line.**

---

## 1. Collect, before any hypothesis

```bash
# the red run
gh run list --workflow=<workflow>.yml --status=failure --limit 1
gh pr checks <PR>

# everything it produced, into a gitignored directory
mkdir -p ./_ci-debug/<RUN_ID>
gh run download <RUN_ID> --dir ./_ci-debug/<RUN_ID>/
gh run view <RUN_ID> --log        > ./_ci-debug/<RUN_ID>/full.log     # mandatory
gh run view <RUN_ID> --log-failed > ./_ci-debug/<RUN_ID>/failed.log   # triage shortcut only
```

`--log-failed` is an extract. **The complete log is the requirement**, because the failing assertion is
often a consequence of something three steps earlier that exited zero.

When the artifacts are too large to pull whole, fetch by name or pattern rather than skipping them — and
use a pattern, so a sharded matrix does not leave you with one shard out of six:

```bash
gh run download <RUN_ID> --pattern "app-logs*"
```

## 2. Read in this order

1. **The full run log** — including the steps that passed.
2. The failed-step extract, for fast orientation.
3. **The structured report**, if the runner emits one: the failure classification, silent errors, budget
   violations.
4. The HTML report — the steps with their screenshots inline.
5. **The trace**, opened in its viewer: the DOM, network and console timeline of the failing test.
6. **The application log from the same time window.** This is the one people skip, and it is where the real
   exception usually is.
7. The worker or queue log, if the test dispatches background work.

## 3. Correlate explicitly

The correlation is the work. Write it down — each line an observation with its source:

```text
✓ full.log:1240 — assertion failed: expected the submit button to be visible
✓ report.json  — classification says test defect, BUT silentErrors has one page error:
                 "Cannot read property 'cart' of undefined"
✓ app log, same minute — exception in the cart controller, thrown from the cart service
✓ reclassified: application defect, not a test defect
✓ root cause: the service throws when the session identifier is absent; the test runs with no cookies
✓ fix: handle the absent session in the service — early return with an empty cart
```

A failure that looks like a broken selector and is actually a backend exception is the **normal** case in a
browser suite, not the exotic one: the page did render, it just rendered the error state.

## 4. Classify before fixing

| Class | Signal | Fix goes in |
|---|---|---|
| **Test defect** | the application behaved correctly; the assertion or the setup was wrong | the test |
| **Application defect** | an exception, a wrong response, a silent console error | the application — and the test stays as it is, because it caught something |
| **Environment defect** | missing service, wrong configuration, absent fixture, a migration that did not run | the workflow or the configuration |
| **Flaky** | a race, a timing assumption, shared state between tests | the test's determinism — never a longer timeout |

**Check the flakiness history before touching a test.** A test already known to be intermittent is a
different problem from one that just started failing, and "fixing" it by loosening the assertion removes the
only thing that noticed.

## 5. What the fix has to state

- The file and the **line**, in a form that is clickable.
- The corrected code.
- Which class of failure it addresses, and why the other three were ruled out.
- If it is flaky: what the race actually was. A raised timeout is not a diagnosis.

## 6. Locally, the same discipline

Running it again and watching the terminal loses the artifacts. Capture the complete output to a file, keep
the run directory, and read the application log for the same window — the local failure and the CI failure
are the same investigation with different storage.

---

## Gotchas

- **"Re-run it and see" is not triage.** It spends minutes, and a pass proves nothing about a race — see
  **`padosoft-evidence-boundaries`**.
- **A green step can be the cause.** Exit code zero and "did what it was supposed to" are different claims.
- **A warning in the setup step becomes an error four steps later**, where it no longer names the cause.
- **Timestamps are in the runner's timezone**, and the application log may be in another. Line them up
  before concluding two events are unrelated.
- **A sharded matrix produces one artifact per shard.** Downloading by exact name gets one of them, and the
  failure is in another.
- **The console error is often the whole answer** and appears in no assertion output at all.
- **Do not commit the debug directory.** It contains logs, screenshots and traces — traces in particular are
  archives of real requests and can carry tokens and personal data.

## Checklist

- [ ] The **complete** run log downloaded and read, passing steps included
- [ ] Every artifact downloaded (by pattern, if selective), into a gitignored directory
- [ ] The application and worker logs for the failure window read
- [ ] Trace and screenshots inspected where the suite produces them
- [ ] Correlation written out, each observation with its source
- [ ] Flakiness history checked before touching the test
- [ ] Failure classified, with the other classes ruled out explicitly
- [ ] Fix names a file and a line, and is not a raised timeout
- [ ] Debug directory not committed

## Final report

```
Run: <id> · workflow <name> · job <name>
Evidence: full log ✓ · artifacts <n> · app logs ✓ · trace <…>
Observations: <source:line → what it says> (one per line)
Classification: test | application | environment | flaky — others ruled out because <…>
Root cause: <one sentence>
Fix: <file>:<line> — <what changes>
Re-run needed to confirm: yes | no (what confirms it instead)
```
