---
name: spark-playwright-page-check
description: Use when a running Spark or DSH web service needs real-browser verification — page load, client-plugin boot errors, console errors, failed requests, or onboarding/dialog rendering — with the repository's own Playwright chromium.
---

# Spark Playwright page check

Verify the requested browser-visible behavior with the repository's Playwright
installation. HTTP success and empty error logs are supporting evidence, not
proof that client plugins or the requested interaction work.

## Procedure

1. Resolve the target URL and acceptance criteria from the task and running
   service. Check the owning package scripts and browser installation; use the
   existing setup command only when the environment needs it.
2. Run a temporary probe from a package that resolves Playwright, or extend an
   existing browser test when the behavior warrants a regression test. Capture
   console errors, page exceptions, failed requests, and HTTP error responses.
   A completed 4xx/5xx response is not a `requestfailed` event.
3. Navigate and wait for an explicit application-ready element or state. Exercise
   the requested interaction and assert its visible result; avoid treating
   `networkidle` or a fixed delay as readiness for a long-lived event connection.
4. Capture the relevant body evidence and screenshot. View the screenshot before
   making a visual claim. Bound observation time and report a timeout as missing
   evidence rather than success.
5. Close the browser even if the probe fails and remove only temporary files
   created by this check. Keep them out of commits.

## Evidence and authority

Report relevant errors, status, assertions, and rendered evidence, redacting
credentials and private data rather than dumping logs verbatim. Distinguish
page load, plugin readiness, and interaction acceptance. An empty error array
only means no error was observed in the checked interval.

Browser verification does not change service trust: direct LAN access accepts
only loopback or the host's discovered local interface IP literals, and remote
peers still require daemon-user authentication.

Return `pageStatus`, `consoleErrors`, `pageErrors`, `failedRequests`,
`bodyEvidence`, `verdict`, and `blockingReasons`.
