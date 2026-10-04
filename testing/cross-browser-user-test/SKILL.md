---
name: cross-browser-user-test
description: 'Execute an optional test plan and audit a running web app with three dedicated Playwright MCP servers for Chrome, Firefox, Safari-oriented WebKit, and mobile/tablet/desktop/wide viewports. Use when asked to run browser tests, test a website, verify responsive rendering, check browser compatibility, exercise user flows, inspect console/runtime errors, capture screenshots, or produce a cross-browser user-test report.'
argument-hint: 'Optional URL, test-plan path, routes, themes, or user flows'
---

# Cross-Browser User Test

Perform a read-only user-facing audit with Playwright MCP. Test behavior and rendering; do not edit application source unless the user separately asks for fixes.

All generated screenshots, logs, and reports must be written beneath the repository-root `.playwright-mcp/` directory. The final report must be `.playwright-mcp/user-test-report.md`.

## Required invocation disclaimer

At the beginning of every invocation, before calling browser tools or beginning any test work, display this notice prominently:

> [!IMPORTANT]
>
> **Three Playwright MCP servers must be running.**
>
> This audit requires responsive `playwright-chrome`, `playwright-firefox`, and `playwright-webkit` servers. I will verify all three before testing and install missing Playwright browser binaries when needed. If any server remains missing, unreachable, or runs the wrong engine, the audit will stop until it is started or restarted.

Do not omit, shorten, or bury this notice, even when the user already supplied a URL or says the servers are running.

## Defaults

- Browsers: Chrome, Firefox, and Playwright WebKit as Safari-oriented coverage. Never claim this is a test of the installed Safari application.
- Browser servers: require three dedicated, simultaneously available MCP servers named `playwright-chrome`, `playwright-firefox`, and `playwright-webkit`.
- Viewports: mobile `375×812`, tablet `768×1024`, desktop `1280×800`, and wide desktop `1920×1080`.
- Scope: all discoverable same-origin application routes, both themes when the app exposes themes, and safe representative interactions.
- Test plan: optional Markdown supplied as an attachment, inline content, or a workspace path. When omitted, run the exploratory audit defined by this skill.
- Evidence: capture screenshots for every failure and for representative passing layouts. Do not capture every passing route unless requested.

Honor browser, viewport, route, theme, and flow overrides supplied by the user.

## 1. Verify prerequisites and stop when missing

Do not start partial testing before all three browser servers are ready.

1. Determine the repository root and resolve all artifact paths from it.
2. Check that `playwright-chrome`, `playwright-firefox`, and `playwright-webkit` tools are all available.
3. Call a lightweight operation such as listing browser tabs on each server. This verifies that the server responds; configuration files or processes alone are insufficient evidence.
4. If a server reports a missing browser executable, or browser availability cannot be established, run this command once from the repository root:

   ```bash
   playwright-mcp install-browser chromium firefox webkit
   ```

   Using the same `playwright-mcp` executable that starts the servers installs browser revisions matching that MCP package. The command is idempotent and skips matching binaries already installed. Do not add `--force` or `--with-deps` unless the user explicitly requests it.

5. After installation succeeds, retry the three lightweight server checks once. If MCP does not restart automatically, stop and ask the user to restart or reload all three servers, then resume verification. Do not rerun the installer repeatedly.
6. If installation fails, report the relevant error and stop. Do not continue with partial browser coverage.
7. Verify each engine from the browser user agent or equivalent runtime evidence. Do not infer the engine from the server name.
8. If any server is still absent, unreachable, or launches the wrong engine, **stop**. Tell the user exactly which server failed and ask them to start or restart it using [the MCP setup guide](./references/mcp-setup.md). Do not test with the remaining servers and do not silently reduce coverage.
9. Obtain the application URL from the invocation or conversation. If none was provided, ask the user to start the web server and provide its URL, then stop.
10. Navigate one browser to the URL. If navigation fails, the response is not an application page, or the server is unavailable, stop and ask the user to run the web server and provide a reachable URL.

Do not start the application server yourself unless the user explicitly asks. Do not guess a localhost port from `package.json` and proceed without confirming that it responds.

## 2. Prepare artifacts

Create `.playwright-mcp/` and use these paths:

- `.playwright-mcp/user-test-report.md` — final report
- `.playwright-mcp/screenshots/<browser>/<viewport>/<route>-<theme>-<state>.png`
- `.playwright-mcp/logs/<browser>-console.txt` — only when console export is supported or useful

Use lowercase filesystem-safe slugs. Use `home` for `/`. Keep every explicit Playwright filename under `.playwright-mcp/`; never use a bare filename.

Preserve existing artifacts unless overwriting the same audit-owned path is necessary. The report should describe only the current run.

## 3. Load the optional test plan

Use [the test-plan template](./references/test-plan-template.md) as the supported format.

1. Accept a test plan supplied as an attachment, inline Markdown, or a workspace-relative/absolute path.
2. If the user requests a plan but has not written one, copy the template to `.playwright-mcp/test-plan.md`, ask them to complete or approve it, and stop before testing.
3. Validate that every test case has a unique ID, steps, and an observable expected result. Resolve `all` and `default` environment values against this skill's browser, viewport, and theme defaults.
4. Ask a focused clarification and stop if a missing precondition, credential, test datum, expected result, or safety decision prevents reliable execution. Never invent credentials or consent for destructive actions.
5. Treat supplied cases as mandatory. Add the exploratory route, rendering, overflow, console, and safe-interaction checks from this skill unless the user explicitly requests plan-only execution.
6. Build a traceability list mapping each test-case ID to every browser × viewport × theme combination that must run. Do not mark a case PASS from a different environment than the one specified.

The plan describes tests; it does not replace execution. Do not produce a report based only on reviewing the plan.

## 4. Build the test inventory

1. Start with planned test cases plus routes and flows named by the user.
2. Discover same-origin routes from navigation, sitemap data, framework route metadata, and relevant source files. Exclude logout, destructive, admin-only, external, download, mail, telephone, and fragment-only links.
3. Deduplicate normalized paths while preserving meaningful query-string variants.
4. Identify app-wide modes such as themes, locale, authentication state, or feature flags. Test all user-visible themes by default.
5. Identify safe critical interactions: navigation, menus, dialogs, tabs, accordions, forms with non-destructive local calculations, theme controls, copy buttons, and validation states.
6. Record the final browser × viewport × theme × route matrix before execution. If the matrix is unusually large, test every route at mobile and desktop, then representative layout families at tablet and wide desktop; disclose this sampling in the report.

Never submit purchases, contact forms, account changes, deletions, or other irreversible/external actions without explicit permission.

## 5. Execute the tests and matrix

Run every applicable planned test case through Playwright MCP. Do not generate Playwright Test source files and do not substitute static source review for browser execution.

For each planned test case and environment combination:

1. Establish its preconditions and test data without leaking secrets into screenshots, logs, or the report.
2. Perform each step in order through the correct browser server.
3. Observe the stated expected result; do not infer success merely because no exception was thrown.
4. Record PASS, FAIL, BLOCKED, or NOT RUN for that exact test-case ID and environment.
5. Capture evidence according to the plan. Always capture a useful screenshot for FAIL; explain why evidence is absent when capture itself is blocked.
6. Reset relevant browser state before the next case when tests can influence one another.

For each required browser, viewport, theme, and route:

1. Set the viewport before navigation.
2. Navigate directly to the route and wait for the page to settle.
3. Apply the theme or mode and verify that it actually changed.
4. Check:
   - the expected page shell and primary content render;
   - no loading indicator remains indefinitely;
   - navigation and visible controls are usable;
   - dialogs, menus, and overlays fit the viewport and can be dismissed;
   - text, media, code, tables, forms, and controls are not clipped or overlapping;
   - keyboard focus is visible for representative interactive controls;
   - no unexpected horizontal document overflow exists;
   - no uncaught runtime errors or relevant console errors occur.
5. Measure overflow using `document.documentElement.scrollWidth - document.documentElement.clientWidth`. Treat a positive result greater than one CSS pixel as a failure, then locate the responsible element instead of hiding document overflow.
6. Exercise representative safe interactions once per relevant layout/browser combination. Reset state between flows when prior actions could affect results.
7. Capture a screenshot immediately when a failure is visible. Include enough context to identify the problem; use a full-page screenshot only when it improves evidence.
8. Record PASS, FAIL, BLOCKED, or NOT RUN with concise evidence. A console warning is not automatically a failure; classify it by user impact and relevance.

Continue after individual failures when safe. Stop only if the app or browser server becomes unusable, and mark remaining combinations BLOCKED.

The application “works” only when all mandatory planned cases and required exploratory checks pass. Any FAIL means the overall result is FAIL. Any BLOCKED or NOT RUN mandatory case prevents an overall PASS.

## 6. Validate findings

Before reporting a defect:

1. Reproduce it once in the same combination.
2. Compare another browser or viewport to determine whether it is engine-specific or responsive.
3. Exclude expected browser-extension, dev-server, hot-reload, and third-party noise unless it affects the user flow.
4. Capture the smallest useful screenshot and exact route, browser, viewport, theme, and steps.
5. Distinguish WebKit findings from confirmed installed-Safari findings.

## 7. Write the report

Use [the report template](./references/report-template.md) and write `.playwright-mcp/user-test-report.md` even when all tests pass or execution is partially blocked.

The report must include:

- date, URL, scope, limitations, and exact browser engines;
- viewport and theme matrices;
- the test-plan source or `None — exploratory audit`;
- one result row for every planned test-case/environment combination;
- tested routes and interactions;
- summary counts for PASS, FAIL, BLOCKED, and NOT RUN;
- prioritized findings with reproduction steps and expected versus actual behavior;
- Markdown links or embeds for every related screenshot using paths relative to the report, for example `![Mobile overflow](screenshots/firefox/mobile/tools-overflow.png)`;
- console/runtime evidence where relevant;
- explicit untested areas and the reason.

Do not claim “all browsers,” “Safari tested,” or “everything works” unless the recorded matrix supports that statement. End the chat response with the report path, a short result summary, and blockers if any.

## Completion checklist

- [ ] All three dedicated MCP servers responded and their engines were verified.
- [ ] Missing browser binaries were installed once, or installation was confirmed unnecessary.
- [ ] The supplied URL was reachable before testing began.
- [ ] Every supplied test case was executed in each required environment.
- [ ] Every test-case ID is traceable from its plan entry to report evidence.
- [ ] Every planned matrix entry has a result status.
- [ ] Safe critical interactions were exercised.
- [ ] Failures were reproduced and have useful evidence.
- [ ] Every generated artifact is under `.playwright-mcp/`.
- [ ] `.playwright-mcp/user-test-report.md` exists and links to its screenshots.
