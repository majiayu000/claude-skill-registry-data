---
name: playwright-agents
description: "Use when a coding agent works with Playwright through playwright-cli, Playwright MCP or the planner, generator and healer Test Agents: setting them up, reviewing healer diffs before merging, debugging a failing test from its trace in a terminal with no display, and leaving a video receipt."
---

# playwright-agents

## Overview

Playwright ships three things built for coding agents, and they solve
different problems:

| Tool | What it is | Use it for |
|---|---|---|
| `playwright-cli` | A command-line browser driver: `open`, `click e15`, `snapshot`, `screenshot` | An agent checking a page, reproducing a bug or poking a flow while it also works in a large codebase |
| Playwright MCP | An MCP server that exposes the browser as tools and returns accessibility snapshots | Long agent loops that keep browser state and reason over page structure |
| Playwright Test Agents | Three agent definitions (planner, generator, healer) generated into your repo by `npx playwright init-agents` | Turning an app into a Markdown test plan, then into `@playwright/test` files, then keeping them green |

The official guidance on the first two
([getting-started-cli][pw-cli]): "`playwright-cli` is best for **coding
agents** (Claude Code, GitHub Copilot, etc.) that favor token-efficient,
skill-based workflows", while "MCP is best for specialized agentic loops
that benefit from persistent state and iterative reasoning over page
structure".

This skill covers choosing between them, setting them up, and the
review a human still owes their output. Writing Playwright tests by hand
(locators, web-first assertions, config, sharding) is
`playwright-testing`; scaffolding a whole harness for a repo with no
suite is the `automation-harness-bootstrapper` agent; cleaning up a
recorded codegen spec is `playwright-codegen-reviewer`.

Facts below are checked against Playwright 1.65 docs and a local
`npx playwright init-agents --loop=claude` run on `@playwright/test`
1.65.0. Agent definitions change between releases, so re-check after an
upgrade.

[pw-cli]: https://playwright.dev/docs/getting-started-cli
[pw-mcp]: https://playwright.dev/docs/getting-started-mcp
[pw-agents]: https://playwright.dev/docs/test-agents
[pw-notes]: https://playwright.dev/docs/release-notes
[pw-intro]: https://playwright.dev/docs/intro

## When to use

- "Have Claude open the app and check X" or "reproduce this UI bug in a
  browser".
- "Set up Playwright MCP / playwright-cli for Claude Code."
- "Generate Playwright tests for this app with the planner / generator /
  healer agents", or "the healer changed my tests, is that OK?"
- A Playwright test fails only on CI and the agent has to debug it from a
  trace in the terminal.
- A reviewer wants proof the agent actually ran the flow (video receipt).

Not a fit: hand-writing or refactoring specs (`playwright-testing`),
cross-browser matrix planning (`browser-matrix-strategy-reference`).

## Step 1 - Pick the tool

| Situation | Pick | Why |
|---|---|---|
| Claude Code works in a repo and needs to check a page now and then | `playwright-cli` | Commands avoid "loading large tool schemas and verbose accessibility trees into the model context" ([pw-cli][pw-cli]); each snapshot is written to a file the agent reads only when needed |
| An MCP-only client (Claude Desktop, Cursor, VS Code chat) or a long exploration loop | Playwright MCP | Tools and snapshots stay in the conversation; persistent profile by default ([pw-mcp][pw-mcp]) |
| You want a test suite, not a one-off check | Test Agents | They write `specs/*.md` plans and `tests/*.spec.ts` files you keep and run in CI ([pw-agents][pw-agents]) |
| You need the agent to see your own signed-in browser tabs | Either, with the Playwright Extension: `playwright-cli attach --extension` or MCP `--extension` | Connects to existing tabs instead of a fresh browser |

Do not install all three "just in case": each MCP server adds its tool
schemas to every conversation.

## Step 2 - Set up playwright-cli

Per [pw-cli][pw-cli] (Node.js 20+ for the CLI itself):

```bash
npm install -g @playwright/cli@latest
playwright-cli --help
playwright-cli install --skills        # skill files for the agent, this project
# or: playwright-cli install --skills -g   (into ~/.claude/skills)
```

Since 1.62, a project that already has `@playwright/test` can run the
bundled copy as `npx playwright cli` ([pw-notes][pw-notes]).

First run, headless by default:

```bash
playwright-cli open http://localhost:3000/login
playwright-cli snapshot                 # element refs like e15
playwright-cli fill e15 "user@example.com"
playwright-cli click "role=button[name=Sign in]"
playwright-cli screenshot --filename=after-login.png
playwright-cli console                  # browser console messages
playwright-cli requests                 # network since page load
playwright-cli close
```

Sessions: `-s=<name>` runs several browsers side by side; `list`,
`close-all`, `kill-all` manage them; `playwright-cli show` opens a live
dashboard of every session. The profile lives in memory unless you pass
`--persistent`. A headless session closes itself after an hour without
commands; change that with `open --idle-timeout=<ms>`. Project defaults go
in `.playwright/cli.config.json`, loaded automatically.

## Step 3 - Set up Playwright MCP

Claude Code ([pw-mcp][pw-mcp]):

```bash
claude mcp add playwright npx @playwright/mcp@latest
```

Other clients take the standard config:

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest", "--headless", "--isolated"]
    }
  }
}
```

| Flag | Effect (from [pw-mcp][pw-mcp]) |
|---|---|
| (none) | Headed browser and a persistent profile per workspace: logins and cookies survive between sessions |
| `--headless` | No visible window; needed on CI and in containers |
| `--isolated` | Fresh profile every session; add `--storage-state <file>` to start signed in |
| `--browser=firefox` | `chrome`, `firefox`, `webkit` or `msedge` |
| `--idle-timeout=<ms>` | Close an idle headless browser sooner than the default hour; `0` disables |
| `--port 8931` | Standalone HTTP server, for a headed browser on a machine without a display |
| `--no-webmcp` | Stop offering tools that the page itself registers via WebMCP (1.65, [pw-notes][pw-notes]) |

Prefer `--isolated` for test work: the default persistent profile keeps
yesterday's login and cart, which makes "it works" depend on leftover
state.

## Step 4 - Set up the Test Agents

```bash
npm init playwright@latest            # only if the repo has no Playwright yet
npx playwright init-agents --loop=claude
```

(`npm init playwright@latest` is the standard installer, [pw-intro][pw-intro].)
Other loops: `--loop=vscode`, `--loop=codex`, `--loop=opencode`
([pw-agents][pw-agents]). With `--loop=claude` on 1.65.0 the command
writes:

| File | Purpose |
|---|---|
| `.claude/agents/playwright-test-planner.md` | Explores the app, saves a Markdown plan to `specs/` |
| `.claude/agents/playwright-test-generator.md` | Turns one plan item into a test file, checking selectors live |
| `.claude/agents/playwright-test-healer.md` | Runs failing tests, debugs them, edits the test until it passes |
| `.mcp.json` | Server `playwright-test`: `npx playwright run-test-mcp-server` |
| `seed.spec.ts` | Seed test the agents run first to get a ready page |
| `specs/README.md` | The plans folder |

Then:

1. Edit `seed.spec.ts` so it does the real setup: your custom fixtures,
   sign-in, base URL. The planner runs it and "will also use this seed
   test as an example of all the generated tests" ([pw-agents][pw-agents]).
   A blank seed gives plans for the login page only.
2. Restart Claude Code so it loads `.mcp.json` and approve the
   `playwright-test` server.
3. Commit the agent files. The docs say the definitions "should be
   regenerated whenever Playwright is updated to pick up new tools and
   instructions" ([pw-agents][pw-agents]): re-run `init-agents` in the same
   PR as every `@playwright/test` bump.

## Step 5 - Run the loop with review gates

The agents run unattended, so each hand-off gets a human check.

| Stage | Prompt | Output | Review before moving on |
|---|---|---|---|
| Plan | "Use the playwright-test-planner agent to plan guest checkout. Seed: `seed.spec.ts`. PRD: `docs/checkout.md`" | `specs/guest-checkout.md` | Scenarios match the requirement, error paths present, nothing out of scope |
| Generate | "Use the playwright-test-generator agent for section 1 of `specs/guest-checkout.md`" | `tests/.../*.spec.ts` | Role or test-id locators, `expect` web-first assertions, each expected result from the plan is asserted |
| Run | `npx playwright test` | Pass or fail | A pass on the first run proves little: break the app or the assertion once and see it fail |
| Heal | "Use the playwright-test-healer agent on `tests/checkout/apply-coupon.spec.ts`" | Edited test, or `test.fixme()` | The diff review below |

### Reviewing what the healer changed

The healer's own instructions (generated `playwright-test-healer.md`,
1.65) tell it to fix "assertions and expected values", to "Do not ask
user questions ... do the most reasonable thing possible to pass the
test", and, when it is confident the test is right, to "mark this test
as test.fixme()" with a comment. So a green healer run can hide a real
bug. Review its diff with this table:

| Diff shows | Accept? |
|---|---|
| Locator updated to a role, label or test id that matches the new UI | Yes |
| Missing wait replaced by a web-first assertion | Yes |
| Expected text, count or URL changed | Only if the spec or product changed on purpose. Otherwise it is the app's bug: revert, file it |
| Assertion deleted or loosened (`toHaveText` to `toBeVisible`, exact to broad regex) | No. Restore it |
| `test.fixme()` added | Treat the comment as a bug report: file it, link it, keep the test |
| `waitForTimeout` or `networkidle` added | No. The healer is told "Never wait for networkidle"; send it back |

Run `git diff tests/` after every healer session, and run the suite
again yourself before merging.

## Step 6 - Debug a failing test from the terminal

When a test fails on CI, the agent can read the trace without a GUI
(1.59+, [pw-notes][pw-notes]):

```bash
npx playwright trace open test-results/checkout-chromium/trace.zip
npx playwright trace actions --grep="expect"   # failing step and its number
npx playwright trace action 9                  # error, expected vs received
npx playwright trace snapshot 9 --name after    # DOM after that step
npx playwright trace close
```

To step through a test live:

```bash
npx playwright test tests/checkout.spec.ts --debug=cli
# prints: Run "playwright-cli attach tw-87b59e" to attach to this test
playwright-cli attach tw-87b59e
playwright-cli --session tw-87b59e step-over
```

For flaky tests, set `trace: 'retain-on-failure-and-retries'` in the
config: it "retains all traces when an attempt fails", so a passing and
a failing attempt can be compared (1.59). `PLAYWRIGHT_DASHBOARD=1` shows
`@playwright/test` browsers in the `playwright-cli show` dashboard.

## Step 7 - Leave evidence a human can check

An agent saying "I checked the page" is not evidence. Leave one of:

- A screenshot per checked state: `playwright-cli screenshot --filename=...`.
- A video receipt with `page.screencast` (1.59+, [pw-notes][pw-notes]),
  which "serves as a receipt: chapter titles provide context, action
  annotations highlight each interaction":

```ts
await page.screencast.start({ path: 'receipt.webm' });
await page.screencast.showActions({ position: 'top-right' });
await page.screencast.showChapter('Verifying coupon', { description: 'SAVE20 applies 20%' });
await page.getByLabel('Coupon').fill('SAVE20');
await page.getByRole('button', { name: 'Apply' }).click();
await expect(page.getByTestId('discount')).toContainText('20%');
await page.screencast.stop();
```

- For generated tests: the `npx playwright test` output, with counts.

## Security

- `browser_run_code_unsafe` "runs arbitrary JavaScript in the Playwright
  server process and is RCE-equivalent", so the docs say to enable it only
  for trusted MCP clients ([pw-mcp][pw-mcp]). The generated planner definition lists
  this tool, so the planner can run code on your machine.
- Page content is untrusted input to the agent. WebMCP tool "names,
  descriptions, schemas and results are provided by the page, so treat
  them as untrusted input" ([pw-cli][pw-cli]); use `--no-webmcp` when you
  test sites you don't control.
- The default MCP profile is persistent: real logins in it are reachable
  by whatever the agent does next. Use `--isolated` plus a test-account
  `--storage-state` file, and keep that file out of git.

## Anti-patterns

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| Adding Playwright MCP to every project "in case" | Tool schemas cost context in every session | `playwright-cli` for occasional checks (Step 1) |
| Leaving `seed.spec.ts` as generated | Planner explores a blank page; generated tests skip your fixtures | Real setup in the seed (Step 4) |
| Upgrading `@playwright/test` without re-running `init-agents` | Agent files call tools that changed or no longer exist | Regenerate in the same PR (Step 4) |
| Merging healer output unread | Healer is told to fix expected values and not ask; real bugs become passing tests | Diff review table (Step 5) |
| Counting `test.fixme()` as "healed" | The failing behavior is now silently skipped | File the bug, keep the test (Step 5) |
| Default persistent profile for tests | Results depend on leftover cookies and carts | `--isolated` + `--storage-state` (Step 3) |
| "Checked in the browser, looks fine" with no artifact | Nothing to review | Screenshot or screencast receipt (Step 7) |

## Limitations

- Agent definitions, tool names and CLI commands move fast (the CLI is
  0.x). Check the release notes on upgrade.
- Test Agents generate `@playwright/test` code only (JS/TS); Python, Java
  and .NET Playwright users get the CLI and MCP but not this loop.
- The agents explore through the accessibility tree. Canvas apps and
  pages with poor ARIA give thin snapshots and weak locators.
- Generated plans and tests reflect what the agent saw in one session;
  they are a draft for review, not a coverage guarantee.

## References

- [pw-cli][pw-cli] - Playwright, "Coding agents": install, `--skills`,
  commands, sessions, idle timeout, config file, CLI vs MCP, WebMCP.
- [pw-mcp][pw-mcp] - Playwright, "Playwright MCP": `claude mcp add`,
  flags, profile modes, idle timeout, `browser_run_code_unsafe`.
- [pw-agents][pw-agents] - Playwright, "Agents": planner, generator,
  healer, `init-agents --loop`, seed test, regenerate on update.
- [pw-notes][pw-notes] - Playwright release notes: 1.56 Test Agents;
  1.59 screencast, `--debug=cli`, `npx playwright trace`,
  `retain-on-failure-and-retries`, `PLAYWRIGHT_DASHBOARD`; 1.62 bundled
  `npx playwright cli` / `mcp`; 1.65 `--no-webmcp`.
- [pw-intro][pw-intro] - Playwright, "Installation": `npm init playwright@latest`.
- Local check: `npx playwright init-agents --loop=claude` on
  `@playwright/test` 1.65.0 (file list in Step 4, healer and planner
  definitions quoted in Steps 5 and Security).
