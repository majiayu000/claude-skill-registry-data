---
name: browser
description: Browser automation and desktop UI. Use for web-page reads and interaction, screenshots, browser tests, login or session reuse, Orca's embedded browser, explicit Camofox or Camoufox browsing, and native windows or dialogs. Selects a runtime and controller by task and harness.
---

# Browser

## Workflow

1. **Read policy.** Read [policy.md](references/policy.md) before browser or
   desktop actions. It defines authorization, focus, ownership, and secret
   handling for every controller and takes precedence over controller-specific advice.
2. **Identify the harness.** Use Orca when `ORCA_WORKTREE_ID` is set; otherwise
   use the terminal. This identifies available controllers; the selected
   recipe owns runtime readiness.
3. **Select a recipe.** Choose the first matching row and read its linked
   reference. Each recipe names its runtime, controller, identity support and
   limits. Apply the fallback rules below when a route cannot complete the task.

   | Task | Orca | Terminal |
   | --- | --- | --- |
   | Prateek requests his running Chrome | [browser-harness](references/drivers/browser-harness.md) | [browser-harness](references/drivers/browser-harness.md), or Claude in Chrome when named |
   | Prateek explicitly requests Camofox or Camoufox page browsing | [Camofox REST](references/drivers/camofox.md), task-owned Camoufox | [Camofox REST](references/drivers/camofox.md), task-owned Camoufox |
   | Explicit runtime without a supported recipe | Report the limit and ask which alternative is acceptable | Report the limit and ask which alternative is acceptable |
   | Prateek names another browser tool | The named tool, when supported here | The named tool |
   | Native window, dialog, or app chrome | [Orca](references/drivers/orca.md), using `orca computer` | [Native UI](references/drivers/native.md) |
   | Cross-browser test suite (Firefox or WebKit) | [Playwright](references/drivers/playwright.md) | [Playwright](references/drivers/playwright.md) |
   | Public-page read without interaction | Web fetch, API, or domain CLI | Web fetch, API, or domain CLI |
   | Other page work, including blocked or incomplete fetches | [Orca](references/drivers/orca.md) | [agent-browser](references/drivers/agent-browser.md) |

   For Chrome running inside Orca, use browser-harness and explain that Orca's
   browser commands operate only on Orca's embedded pages.
   The Camofox exception uses its own process, not Orca's embedded browser.
   The named-tool row selects a controller; it does not qualify another runtime.

   **Fallback.** Start with the selected route and distinguish constraints from
   preferences in Prateek's request:

   - For generic browsing, automatically try an installed, compatible alternative
     when the selected route is unavailable or fails. Prefer Orca inside Orca,
     then agent-browser, then [Camofox REST](references/drivers/camofox.md).
     In a terminal, start with agent-browser, then Camofox. Read each selected
     recipe, preserve the task's identity/retention constraints, and briefly report
     a controller change. A fallback runs from the current harness; it does not
     require moving the agent to another harness or installing software.
   - An explicit runtime, engine, tool, live browser or profile is a constraint.
     Preserve it; if compatible routes are exhausted, explain the blocker and ask
     which alternative Prateek accepts. "Try X first" allows fallback; "use X"
     keeps X unless his request otherwise permits alternatives. Honor requests
     for checkpoints or discussion before trying another route.
   - Before replaying an action elsewhere, reconcile any uncertain outcome using
     the [interaction loop](references/policy.md#interaction). Use an alternative
     only within existing authorization for identity, secrets and visible windows.
     Report a blocker when available compatible alternatives are exhausted.
4. **Choose identity and retention.** Use isolated, temporary state by default. Before creating a
   session, importing a login, or entering credentials, read
   [auth.md](references/auth.md). Continue when the identity is chosen and any
   import source or live browser has been named by Prateek.
   For an owned private service whose self-signed certificate Orca cannot
   accept, follow [certificate recovery](references/certificate.md).
5. **Work.** Follow the selected recipe's workflow and the shared
   [interaction loop](references/policy.md#interaction). Verify the requested
   page or app state before calling the task complete.
6. **Clean up and report.** Apply [resource cleanup](references/policy.md#ownership).
   State the result, identity used, and any resources intentionally retained.

## Terms

- **Harness:** the environment running this agent: Orca or terminal.
- **Runtime:** the browser executing the page, such as Orca's embedded browser,
  live Chrome, or task-owned Camoufox. Its engine determines web compatibility.
- **Controller (driver):** the tool that acts on the runtime or native window,
  such as Orca CLI, Playwright or Camofox's REST server.
- **Transport:** the connection used by the controller, such as REST, CDP or
  MCP. A shared protocol does not establish browser compatibility.
- **Identity:** browser state used for the task. **Isolated** means fresh,
  task-owned state. **Imported** means a login copied from a source Prateek
  names. **Live attach** means control of his running browser. Imports and live
  attaches require his request.
- **Retention:** whether task-owned state is deleted or explicitly kept after
  the task. Isolated state can still be written to disk; cleanup must cover it.
- **Owned resource:** a browser, session, profile, or tab created for this task
  or explicitly named by Prateek for it.
