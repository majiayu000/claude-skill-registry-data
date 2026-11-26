---
name: verify-fix
description: Prove a NightVision finding is fixed by replaying it and rerunning only the check that found it against the same target, instead of a full scan. Use after changing code to fix a NightVision finding, when a user asks "is it fixed", "retest this", or "verify the fix", or as the last step of ship-check. Drives the NightVision MCP `start-scan` tool with `run_only_zap_checks` or `run_only_nuclei_folders`.
allowed-tools: Bash, Read, Grep, mcp__nightvision__auth-status, mcp__nightvision__list-check-categories, mcp__nightvision__start-scan, mcp__nightvision__list-scans, mcp__nightvision__wait-for-scan, mcp__nightvision__get-scan-status, mcp__nightvision__get-scan-paths, mcp__nightvision__list-issues, mcp__nightvision__get-issue-details, mcp__nightvision__get-issue-occurrences, mcp__nightvision__run-app-security-scan
---

# NightVision Verify Fix

A fix is not done until NightVision fails to reproduce it. This skill closes the loop on one finding (or a few from the same check) by retesting just that check against the target that found it.

Never tell the developer a finding is fixed on the strength of the code change alone. Say "fixed in code, not yet verified" until the retest below comes back clean.

This is the one place a scan is started with `start-scan` instead of the `run-app-security-scan` harness: the harness has just created the target and refreshed its spec from source, and the retest reuses both. When that no longer holds (step 2), go back to the harness.

## What you need

- The original finding: its name (the vulnerability or check), method and path, parameter, and the proof-of-concept request or payload. Read these from the scan summary, the SARIF, or `get-issue-details`.
- The original scan's settings. `.nightvision/manifest.json` in the app's source directory has them: `nightvision.target_name`, `nightvision.project_name`, `nightvision.app_auth`, `nightvision.force_private_scan`, `app.target_url`, and the original `scan.scan_id`.
- The app running with the fix, at the same URL the original scan used. Restart it if your change needs a restart or rebuild; a retest against the old process proves nothing.

## Workflow

1. **Replay first.** Send the finding's proof-of-concept request with `curl` against the running app and confirm the evidence is gone (the payload no longer reflects, the error no longer leaks, the query no longer changes the response). This takes seconds and catches a fix that did not load. If the evidence is still there, the fix is not working: go back to the code.
2. **Decide how to retest.**
   - **Request-level findings** (SQL injection, XSS, command injection, path traversal, SSTI and similar ZAP active checks): retest with only that check, step 3.
   - **Nuclei findings** (a CVE or misconfiguration template): retest with only that template's folder, step 3.
   - **Response and configuration findings** (missing security headers, cookie flags, information disclosure): these come from passive checks that run on every scan. Confirm with `curl -sI` that the header or flag is now right, then let the next full scan confirm it; a narrowed scan adds nothing here.
   - **The spec may be stale**: your fix changed routes, parameters or the auth flow, routes were added since the original scan, or there is no manifest from a harness run. Run `run-app-security-scan` with `project_path` instead, so Source Intelligence refreshes the spec, and check the finding in that scan.
3. **Run the narrowed scan.** Call `list-check-categories` and find the check whose name matches the finding. Then call `start-scan` with:
   - `target_name` and `project` from the manifest;
   - the same app auth the original scan used (`auth` or `auth_id`), or `no_auth: true` if it ran unauthenticated, and `force_private_scan: true` if the manifest records it;
   - for a ZAP finding, `run_only_zap_checks: ["<check name>"]` and `no_nuclei: true`;
   - for a Nuclei finding, `run_only_nuclei_folders: ["<folder>"]` and `no_zap: true`.

   Each `run_only_*` parameter narrows only its own engine, so leaving out `no_nuclei` or `no_zap` runs the other engine in full. If no check name clearly matches the finding, do not guess: fall back to a full `run-app-security-scan`. Check `start-scan`'s input schema first: an older NightVision MCP server ignores parameters it does not know rather than rejecting them, so if `run_only_zap_checks` or `no_nuclei` is missing from the schema, tell the developer to update the server and say the retest ran wider than one check.
4. **Wait for it.** If `start-scan` returns `scan_id_pending: true` instead of a scan ID (common for local and private apps), poll `list-scans` for the target until the new scan appears. Then `wait-for-scan` until it reaches a terminal status. Keep the MCP server running for local and private apps so the relay stays up. A narrowed scan still crawls the target, so it is shorter than a full scan, not instant.
5. **Check the result.**
   - Confirm the retest reached the endpoint: `get-scan-paths` for the new scan, filtered to the path, must list it. If it does not (auth expired, the route moved, the crawl missed it), the fix is unverified, not verified.
   - Then call `list-issues` for the new scan, filtered to the path (`filter`), or `get-issue-occurrences` with the path, method and kind. The fix is verified when the endpoint was exercised and the finding no longer appears on that path and parameter. If it still appears, compare the new evidence with the old: a different payload getting through means the fix is partial (for example, one sink was parameterized and another was not).
6. **Record the retest** in `.nightvision/retest.json` in the app's source directory, next to the manifest, so the record and the NightVision enforcement hook know a scan ran after the fix:

   ```json
   {"scan_id": "<retest scan id>", "original_scan_id": "<scan.scan_id from the manifest>", "finding": "<finding name>", "endpoint": "<METHOD path>", "result": "verified", "recorded_at": "<ISO 8601 time>"}
   ```

   Use `"result": "still_open"` or `"unverified"` when that is the outcome. Overwrite the file on each retest; the NightVision scan history keeps every scan.
7. **Report** in one line per finding: `Verified fixed: <finding> on <method path> (retest scan <scan_id>)`, `Still open: <finding> on <method path> (retest scan <scan_id>)` with the evidence, or `Unverified: <finding> on <method path>` with the reason.

## Limits to state honestly

- A narrowed scan runs one check. It says nothing about other vulnerability classes: do not present it as a clean bill of health for the app.
- Marking the original finding Resolved in NightVision (app.nightviz.ai) is the developer's or the AppSec team's call; tell them the retest scan ID so they can.
- If the retest scan fails before testing (blocked, unreachable, auth failure), the fix is unverified, not verified. Report the blocker.

## Related skills

`app-security-scan` runs the full scan. `scan-triage` explains findings and how to validate them with `curl`. `ship-check` uses this skill for every fix made before an app is called done.
