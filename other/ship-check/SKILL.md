---
name: ship-check
description: The finish line for an agent-built or vibe-coded app. Before you tell the developer a new or materially changed web app or API is done, review the change for common security mistakes, scan the running app with NightVision, fix what is real in code written this session, verify each fix with a retest, and report what is still open. Use when finishing app work, when a user asks "is this safe to ship", "security check before I deploy", or "make sure this is secure", or when an org rule or the NightVision enforcement hook requires a scan before work is complete.
allowed-tools: Bash, Read, Grep, Glob, mcp__nightvision__auth-status, mcp__nightvision__preflight-app, mcp__nightvision__run-app-security-scan, mcp__nightvision__wait-for-scan, mcp__nightvision__get-scan-status, mcp__nightvision__summarize-scan-findings, mcp__nightvision__export-sarif, mcp__nightvision__list-issues, mcp__nightvision__get-issue-details, mcp__nightvision__get-issue-occurrences, mcp__nightvision__list-check-categories, mcp__nightvision__start-scan, mcp__nightvision__list-scans, mcp__nightvision__get-scan-paths
---

# NightVision Ship Check

The completion gate for app work: the app is not done until NightVision has tested it running, and every finding is fixed and verified, or reported as open. This skill strings the other NightVision skills together in order; follow each one's own instructions at its step.

## When it applies

Run it when the session created or materially changed something an attacker can reach: a web app, API, route handler, auth or session logic, database access, file handling, an AI endpoint, or the security configuration (headers, CORS, cookies). Skip it, and say in one line that you skipped it and why, for changes that are only docs, tests, styling, or build tooling.

## Steps

1. **Review the change.** Read the diff of this session's work against the `secure-build` rules: secrets in code or frontend bundles, unscoped object lookups, string-built queries, unsafe rendering, permissive CORS, debug settings. Fix what you find in code you wrote this session before scanning; it is cheaper than finding it in the scan.
2. **Review access control** with `authz-review` when the change added or changed routes that take object IDs, list user data, or perform privileged actions.
3. **Scan the running app** with `app-security-scan`: start the app, or restart it if it was already running so it serves the code you just wrote, pass the source directory as `project_path` and its URL as `target_url`, and route the scan through `run-app-security-scan`. Report the Source Intelligence result before polling, wait for the scan to reach a terminal status, and apply that skill's coverage floor (a scan that exercised no endpoints is a setup failure, not a pass).
4. **Triage** the findings with `scan-triage`: for each Critical, High and Medium finding, decide whether it is real by replaying it with `curl` and reading the code at its source `file:line`.
5. **Fix what is real** in code written this session, matching the codebase's patterns (the remediation section of `app-security-scan` explains where each class of fix goes). Running ship-check, because the developer asked for it or their organization requires it, is the go-ahead to fix code you wrote in this session: it is your own unfinished work. For real findings in code that existed before this session, report them and ask before changing that code.
6. **Verify every fix** with `verify-fix`. A fix without a clean retest stays "fixed in code, not yet verified".
7. **Report** to the developer, using the template below.

## What you never do

- Mark findings False Positive, Resolved or Won't Fix in NightVision. Dispositions belong to the developer and their AppSec team; list your false-positive candidates with the evidence and let them decide in app.nightviz.ai.
- Call the app secure, safe or vulnerability-free. Say what NightVision tested and what it found.
- Disable checks, narrow scope, or lower scan settings to make findings go away.
- End the turn with a scan still running and nobody watching. If the developer is not there, wait for the scan, then report.

## Report template

```
Security check: <app name>
- Scanned: <target URL>, <endpoint count> endpoints from Source Intelligence, scan <scan_id> (<status>)
- Fixed and verified: <finding> on <method path> (retest <scan_id>), ...
- Fixed in code, not yet verified: ... (why: ...)
- Open, needs a decision: <severity> <finding> on <method path>: <one line on why it is open>
- Possible false positives for AppSec review: <finding> on <method path>: <evidence>
- Access-control review: <n> routes checked, <n> missing, <n> unclear (see table)
- Not covered: <for example, authenticated pages if the scan ran without auth>
Artifacts: .nightvision/manifest.json, .nightvision/retest.json, <sarif path>
```

If the scan could not run, the report leads with the blocker (app would not start, not logged in to NightVision, no project, target unreachable) and the work is not complete.

## How AppSec sees the app

The scan creates or updates a target in the NightVision project, under the developer's own NightVision account. Keep one stable target per app (the harness names it from the repository) so repeat checks update the same target instead of adding new ones; that target list is how the AppSec team sees which apps were built and what is open on each.
