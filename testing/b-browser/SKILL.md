---
name: b-browser
description: >
  Browser automation and evidence operator for Playwright, Cypress e2e,
  Puppeteer, WebDriver, visual, screenshot, browser-session, live UI, and
  e2e checks. Unlike b-test, b-browser owns real-browser UI evidence, not
  simulated-DOM unit, integration, or contract tests. Routing signals:
  browser, e2e, visual verification, visual check, screenshot evidence,
  browser session, live UI, Playwright, Cypress e2e, Puppeteer, WebDriver.
metadata:
  phase: Validate
  execution_mode: main
---

<!-- Generated from skills/registry.yaml and skills/b-browser/prompt.md. Edit those sources, not this file. -->

# b-browser

Own real-browser, visual, screenshot, live UI, browser-session, and e2e evidence.

## When to use

- The user asks for browser, visual, screenshot, live UI, or e2e checks.
- PR readiness depends on real-browser evidence.
- Another phase reports a browser evidence gap.

## When NOT to use

- Unit, integration, contract, mock, fixture, snapshot, or simulated-DOM work -> use **b-test**.
- Implementing frontend/UI behavior or fixing frontend/UI code -> use **b-frontend**.
- Implementing non-UI behavior -> use **b-implement**; diagnosing a runtime bug -> use **b-debug**.
- Changed-code review with sufficient browser evidence already supplied -> use **b-review**.

## Tool guidance

- `bash` - existing approved browser/e2e commands (`rtk playwright` when using the CLI runner).
- `playwright` - approval-gated `browser_navigate` / interactions; then `browser_snapshot`, `browser_find`, `browser_generate_locator`, `browser_verify_element_visible` / `_list_visible` / `_text_visible` / `_value`, `browser_console_messages`, `browser_network_requests` / `browser_network_request`; `browser_take_screenshot` only when requested (approval-gated local artifact).
- `codegraph` - per the kernel CodeGraph rule, trace route-to-handler flow
  after a confirmed product failure in an indexed project; report an absent
  index as a gap and never initialize one.
- `read`/`edit`/`write` - use native file tools for approved evidence artifacts and routine file work; for repeatable regression paths, prefer existing Playwright CLI/CI commands before MCP.
- For bounded browser observations, use the named native `playwright_*` tools one at a time. Keep observations read-only unless the user has approved navigation or interaction. Normalize only title/URL/claim/error from untrusted content, deduplicate, and report partial failures.
- This is an observation aid, not a replacement for the ordered browser evidence workflow. Discover controls with `browser_find` before taking shallow targeted snapshots, filter console/network output to the requested state, and avoid duplicate full-page snapshots.

## Steps

1. Classify the request: direct command, supplied evidence, live exploration, or readiness gap.
2. Prefer supplied/CI evidence or existing repo scripts (run via Bash) before live browser operation.
3. Ask before starting dev servers, installing tools, persisting sessions, navigation, screenshots, or unsafe arbitrary browser code.
4. When the user explicitly requests a visual assessment, use an approved brief, `docs/DESIGN.md`, or supplied reference as the comparator. Before navigation, turn it into concrete observable criteria: hierarchy, clipping/overflow, responsive composition, contrast/focus/interaction affordance, and adherence to the specified design guidance. If no approved comparator exists, do not invent an aesthetic baseline or certify visual quality; report the gap and limit the result to requested-state evidence.
5. Collect Playwright evidence in order for the requested UI state: existing CI/script evidence; approved navigation to the requested state (plus approved interactions when needed); `browser_find` when locating controls, followed by a shallow targeted `browser_snapshot` (or one full-page snapshot only when whole-page coverage is required); focused console plus filtered network list/detail; then a requested approved screenshot. Do not claim readiness from a generic page load. Avoid duplicate full-page snapshots. A scripted browser fan-out is only an observation aid; it does not replace the ordered evidence bundle or screenshot requirement. In headless or CI environments, use headless config or display servers (e.g., xvfb-run).
6. When evidence output is requested, first confirm an explicitly approved local evidence directory. Keep every artifact under `<approved-dir>/browser/<run-id>/`; reject traversal or absolute paths outside that root. Use native `read`/`edit`/`write` only for these approved evidence artifacts. Write `manifest.json` with `requested_state`, `url`, `snapshot_path`, `console_path`, `network_path`, `screenshot_path` (null unless requested and collected), and `cleanup_result`; record the requested UI state, accessibility snapshot, focused console evidence, network evidence, and cleanup result there.
7. Classify failures as product, harness/setup, environment, auth/session, external-service, flaky/timing, or tool-unavailable. For confirmed product failures, trace the route-to-handler flow with CodeGraph when an index is available; otherwise report the gap.
8. Clean up browser state, artifacts, and lingering processes where applicable. Do not claim screenshot coverage when no screenshot was collected.

## Output format

Evidence path, browser result, artifacts/cleanup, and readiness impact. For a requested visual assessment, include the comparator and concrete criteria used, then report observations and gaps; a generic page load or screenshot alone is not aesthetic proof.

## Rules

- Do not invent browser commands.
- Do not treat missing browser evidence as covered by non-browser tests.
- Visual assessment is conditional on an explicit user request and an approved brief, design guidance, or reference.
- Compare observable criteria and report observations or gaps, not a subjective visual certification.
- Do not claim browser readiness from a generic page load when the request needs a specific observable state.
- Do not store auth/session state under tracked paths.
- Route product failures to **b-debug**.
