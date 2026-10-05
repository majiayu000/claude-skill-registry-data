---
name: app-bug-forensics
description: Use when diagnosing or fixing user-reported application bugs. Guides evidence-backed root-cause analysis from symptoms, screenshots, logs, provider failures, background tasks, storage, or desktop lifecycle behavior through a scoped patch and regression tests.
license: MIT
---

# App Bug Forensics

Use this skill when a user reports a bug, screenshot, intermittent failure, or
confusing app behavior. The goal is root cause first, patch second.

## Workflow

1. Preserve the symptom.
   - Identify the exact screen, action sequence, visible message, and affected
     data scope.
   - Inspect screenshots and logs when available.
   - Do not assume the visible error string names the real failing component.

2. Trace the path.
   - Follow the request from UI event to state store, API client, backend route,
     persistence, sidecar/process boundary, and external provider when relevant.
   - Search for all places that can set the visible error state.
   - Check whether the failing request still belongs to the current selection.
   - For AI failures, identify the exact provider, model, transport, profile,
     credential source, timeout, and whether the request reached the provider.

3. Classify likely root cause.
   - Stale async request or route watcher race.
   - Frontend/backend version mismatch or old sidecar process.
   - Missing optional capability being treated as fatal.
   - Provider protocol, model, key, base URL, or auth mismatch.
   - Default AI profile being added when the user selected another profile.
   - Long-running provider request blocked behind an unclosable dialog.
   - Provider request timed out locally after remote token usage already began.
   - Background job result, status, reconnect, or cancellation state was lost.
   - Saved credential/profile source disappeared or was overwritten by another
     profile.
   - Data migration/path/access issue.
   - UI overlay, selection, scrolling, or layout state bug.
   - Result view was hidden or discarded by navigation instead of explicit
     clearing.
   - Installer or process lifecycle half-update.

4. Reproduce minimally.
   - Prefer a focused test or local run over broad speculation.
   - If the issue is intermittent, add timing, request tokens, or controlled
     mocked delays to reproduce the race.
   - If external provider behavior is suspected, separate mock branch tests
     from one real minimal connectivity test.
   - For charged or slow provider paths, do not auto-retry the full generation
     while investigating. Probe status and run only minimal real requests.

5. Fix the cause.
   - Ignore stale results instead of showing stale errors.
   - Translate current real errors into user-facing copy.
   - Keep optional feature failures local to their own UI area.
   - If a request may already be running remotely, reconnect to local job state
     rather than resending the provider call.
   - Preserve completed AI results until the user explicitly clears or replaces
     them.
   - Preserve user data; do not "fix" by deleting local state unless the user
     explicitly asks.

6. Lock the regression.
   - Add the narrowest meaningful test for the bug shape.
   - Include a manual acceptance path when the bug depends on installer,
     provider, OS, or real browser behavior.
   - Report what was reproduced, what was fixed, and what remains only manually
     verified.

## Reference Use

Read `references/app-quality-principles.md` when the bug involves user-visible
errors, provider tests, storage, startup, or UI state.

Read `references/living-to-tell-casebook.md` when the bug resembles raw
`Not Found`, `Failed to fetch`, provider 403 HTML, sidecar leftovers, stale
article/reference selection, startup black windows, data location confusion, or
duplicate anchors/excerpts, AI result hiding, provider timeout after token use,
profile key isolation, or background job recovery.

## Red Lines

- Do not hide a current valid failure by catching and ignoring every exception.
- Do not claim the issue is fixed because a mock test passes.
- Do not use fake data, fake provider success, or broad fallback behavior to
  make a test pass while the real user workflow remains broken.
- Do not expose API keys, auth files, private text, or raw provider HTML in the
  final report.
