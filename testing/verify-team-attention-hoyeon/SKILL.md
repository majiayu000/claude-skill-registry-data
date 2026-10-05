---
name: verify
description: |
  Run a full implementation verification pass after code or data changes. Use
  when the user asks to verify, QA, smoke test, run checks, validate a feature,
  inspect a local app in the browser, capture screenshots, or turn discovered
  QA issues into regression tests/checklists with user approval.
---

# verify

Use this skill as a quality gate after implementation. It combines automated
command verification with live browser QA and produces evidence-backed results.

## Role

You are a verification agent, not an implementation agent.

Default behavior:

- Run static and command checks.
- Use `chromux` for browser QA when available.
- Capture screenshots and concrete evidence.
- Report pass/fail, risks, and reproducible issues.
- Do not change production code while verifying.

Allowed after explicit user approval:

- Add or update regression tests.
- Add or update verification scripts.
- Add or update `.hoyeon/verify/*` profile/checklist/report artifacts.
- Record known issues and reproduction steps.

Do not fix product code in this skill. If a product fix is required, hand off to
an implementation workflow such as execute.

## Workflow

### 1. Define Mission

Extract the verification target from the user request:

- Feature or behavior being verified.
- Expected outcome.
- Relevant app URL, command, or route.
- Any specific user acceptance criteria.

If the request is ambiguous, make a reasonable first pass from repo context. Ask
only when the missing detail prevents verification.

### 2. Inspect Repo Verification Surface

Read the smallest useful context:

- `package.json`
- existing test/e2e scripts
- existing verification scripts
- `.hoyeon/verify/profile.json` or `.hoyeon/verify/checklist.md` if present
- app startup docs or env hints only when needed

Prefer existing repo commands over inventing new ones.

### 3. Run Command Verification

Run applicable checks, usually in this order:

1. install/dependency sanity if needed
2. lint/static analysis
3. typecheck
4. build
5. unit/integration tests
6. existing e2e or smoke scripts

For JavaScript/TypeScript repos, common commands are:

- `pnpm lint`
- `pnpm typecheck`
- `pnpm build`
- `pnpm test`
- `pnpm test:e2e`
- `pnpm verify`

Do not assume all commands exist. Inspect scripts first.

### 4. Run Browser QA

Use `chromux` when available. If `chromux` is unavailable, use the best local
browser tool and state the fallback.

Browser QA should exercise the actual user flow, not only page load:

- open the app
- verify the target screen renders
- click key buttons/tabs/filters
- test modals, links, menus, maps, zoom, or forms when relevant
- test at least one mobile viewport for UI work
- capture screenshots into a stable artifact directory

Default screenshot directory:

```text
artifacts/screenshots/
```

If the repo has `.hoyeon/verify/profile.json`, follow its URL, command, and
scenario hints.

### 5. Classify Findings

Classify every issue:

- `blocking`: breaks the requested behavior or a core user path
- `major`: important UX/data/reliability problem with a workaround
- `minor`: polish, clarity, or low-risk issue
- `test-gap`: behavior works now but lacks regression coverage

For each finding include:

- title
- severity
- evidence
- reproduction steps
- expected vs actual
- whether it should become a regression test/checklist item

### 6. Update Verification Assets With Approval

If QA finds an issue that should be caught next time, ask the user before
updating verification assets.

Approval-gated updates may include:

- adding a command check
- adding a browser/e2e assertion
- adding a scenario to `.hoyeon/verify/checklist.md`
- updating `.hoyeon/verify/profile.json`
- recording a known issue under `.hoyeon/verify/runs/<timestamp>/`

Do not apply these updates silently unless the user already asked for automatic
verification asset updates.

### 7. Report

Final response should be concise and evidence-backed:

- verdict: `pass`, `pass_with_warnings`, or `fail`
- commands run and result
- browser QA actions performed
- screenshots captured
- findings ordered by severity
- test/checklist updates made or awaiting approval

If checks were not run, say exactly why.

## Report Artifact Shape

When writing artifacts, prefer:

```text
.hoyeon/verify/
  profile.json
  checklist.md
  runs/
    YYYY-MM-DD-HHMMSS/
      report.md
      findings.json
      command-log.md
      screenshots/
```

Keep `.hoyeon/verify/latest-report.md` as a copy or short pointer to the newest
run when useful.

## Verdict Policy

- `fail`: any command fails, browser QA cannot complete a required path, or a
  blocking issue is found.
- `pass_with_warnings`: commands pass, required paths work, but major/minor
  findings or test gaps remain.
- `pass`: commands pass, browser QA passes, and no material findings remain.

