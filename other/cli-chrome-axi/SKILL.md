---
name: cli-chrome-axi
description: 'Uses the chrome-devtools-axi CLI for browser automation, accessibility-tree snapshots, console and network inspection, screenshots, Lighthouse audits, and performance traces. Use when interacting with Chrome from the shell, especially when the user mentions chrome-devtools-axi, AX snapshots, browser debugging, or DevTools automation from the command line.'
---

# chrome-devtools-axi

Use `chrome-devtools-axi` when you want Chrome DevTools automation from the shell with agent-friendly output and stable accessibility refs.

## Why This CLI

`chrome-devtools-axi` is a thin CLI over `chrome-devtools-mcp` that keeps a persistent bridge alive between commands. Its default workflow is efficient for agents:

- `open` and `snapshot` return an accessibility tree with `uid=` refs you can reuse as `@<uid>` in later commands.
- Responses include compact structured metadata plus a readable page snapshot.
- Console, network, Lighthouse, performance tracing, and heap capture are available from the same session.

## Safe Invocation

Always disable the CLI's hook auto-install behavior when invoking it from this repo:

```bash
env CHROME_DEVTOOLS_AXI_DISABLE_HOOKS=1 npx -y chrome-devtools-axi --help
```

Use the same prefix for every command unless you intentionally want its global hook side effects.

If the task needs a visible browser, also set headed mode:

```bash
env CHROME_DEVTOOLS_AXI_DISABLE_HOOKS=1 CHROME_DEVTOOLS_AXI_HEADED=1 \
  npx -y chrome-devtools-axi open https://example.com
```

Useful environment variables:

- `CHROME_DEVTOOLS_AXI_HEADED=1` runs Chrome visibly instead of headless.
- `CHROME_DEVTOOLS_AXI_BROWSER_URL=http://127.0.0.1:9222` connects to an existing Chrome instance.
- `CHROME_DEVTOOLS_AXI_PORT=9225` changes the local bridge port.
- `CHROME_DEVTOOLS_AXI_USER_DATA_DIR=/path/to/profile` uses a persistent Chrome profile.

## Core Workflow

Start with the smallest command that gives you the next useful handle.

1. Open or select a page.
2. Capture a snapshot.
3. Reuse `uid=` refs from the snapshot as `@<uid>` for interaction.
4. Re-snapshot after navigation or DOM-changing actions.
5. Inspect console or network only when the page behavior is unclear.

Example loop:

```bash
env CHROME_DEVTOOLS_AXI_DISABLE_HOOKS=1 npx -y chrome-devtools-axi open http://localhost:5173
env CHROME_DEVTOOLS_AXI_DISABLE_HOOKS=1 npx -y chrome-devtools-axi snapshot
env CHROME_DEVTOOLS_AXI_DISABLE_HOOKS=1 npx -y chrome-devtools-axi click @3
env CHROME_DEVTOOLS_AXI_DISABLE_HOOKS=1 npx -y chrome-devtools-axi wait 1000
env CHROME_DEVTOOLS_AXI_DISABLE_HOOKS=1 npx -y chrome-devtools-axi snapshot
```

## Ref-Based Interaction

Prefer AX refs over CSS selectors whenever the snapshot already exposes the target.

```bash
env CHROME_DEVTOOLS_AXI_DISABLE_HOOKS=1 npx -y chrome-devtools-axi click @7
env CHROME_DEVTOOLS_AXI_DISABLE_HOOKS=1 npx -y chrome-devtools-axi fill @12 "user@example.com"
env CHROME_DEVTOOLS_AXI_DISABLE_HOOKS=1 npx -y chrome-devtools-axi hover @18
env CHROME_DEVTOOLS_AXI_DISABLE_HOOKS=1 npx -y chrome-devtools-axi drag @4 @9
env CHROME_DEVTOOLS_AXI_DISABLE_HOOKS=1 npx -y chrome-devtools-axi upload @22 ./fixtures/avatar.png
```

For keyboard-driven flows:

```bash
env CHROME_DEVTOOLS_AXI_DISABLE_HOOKS=1 npx -y chrome-devtools-axi type "search text"
env CHROME_DEVTOOLS_AXI_DISABLE_HOOKS=1 npx -y chrome-devtools-axi press Enter
```

For multi-field forms:

```bash
env CHROME_DEVTOOLS_AXI_DISABLE_HOOKS=1 npx -y chrome-devtools-axi fillform \
  @12='user@example.com' @13='secret'
```

## Navigation And Page State

```bash
env CHROME_DEVTOOLS_AXI_DISABLE_HOOKS=1 npx -y chrome-devtools-axi open https://example.com
env CHROME_DEVTOOLS_AXI_DISABLE_HOOKS=1 npx -y chrome-devtools-axi back
env CHROME_DEVTOOLS_AXI_DISABLE_HOOKS=1 npx -y chrome-devtools-axi wait "Dashboard"
env CHROME_DEVTOOLS_AXI_DISABLE_HOOKS=1 npx -y chrome-devtools-axi scroll down
env CHROME_DEVTOOLS_AXI_DISABLE_HOOKS=1 npx -y chrome-devtools-axi screenshot ./tmp/page.png --full-page
```

Use `wait <text>` when waiting on visible content, and `wait <ms>` for small fixed delays.

## Tabs And Page Selection

```bash
env CHROME_DEVTOOLS_AXI_DISABLE_HOOKS=1 npx -y chrome-devtools-axi pages
env CHROME_DEVTOOLS_AXI_DISABLE_HOOKS=1 npx -y chrome-devtools-axi newpage https://example.com
env CHROME_DEVTOOLS_AXI_DISABLE_HOOKS=1 npx -y chrome-devtools-axi selectpage 1
env CHROME_DEVTOOLS_AXI_DISABLE_HOOKS=1 npx -y chrome-devtools-axi closepage 1
```

When debugging popup or multi-tab flows, list pages after the action and switch explicitly.

## Eval

Use `eval` for quick DOM or app-state inspection.

Plain expressions are wrapped automatically:

```bash
env CHROME_DEVTOOLS_AXI_DISABLE_HOOKS=1 npx -y chrome-devtools-axi eval "document.title"
```

For multi-statement logic, pass an IIFE or function yourself:

```bash
env CHROME_DEVTOOLS_AXI_DISABLE_HOOKS=1 npx -y chrome-devtools-axi eval \
  "(() => Array.from(document.querySelectorAll('button')).map((button) => button.textContent?.trim()))()"
```

## Console And Network

Use these when interaction alone does not explain failures.

```bash
env CHROME_DEVTOOLS_AXI_DISABLE_HOOKS=1 npx -y chrome-devtools-axi console --type error --limit 20
env CHROME_DEVTOOLS_AXI_DISABLE_HOOKS=1 npx -y chrome-devtools-axi console-get 3

env CHROME_DEVTOOLS_AXI_DISABLE_HOOKS=1 npx -y chrome-devtools-axi network --type fetch --limit 20
env CHROME_DEVTOOLS_AXI_DISABLE_HOOKS=1 npx -y chrome-devtools-axi network-get 12
env CHROME_DEVTOOLS_AXI_DISABLE_HOOKS=1 npx -y chrome-devtools-axi network-get 12 \
  --request-file ./tmp/request.txt --response-file ./tmp/response.txt
```

Use `--page` to paginate when there are many results. Reach for `console-get` or `network-get` before rerunning broad list commands with much larger limits.

## Emulation, Accessibility, And Visual Checks

```bash
env CHROME_DEVTOOLS_AXI_DISABLE_HOOKS=1 npx -y chrome-devtools-axi emulate \
  --viewport 390x844x3,mobile --color-scheme light --network 'Fast 3G'

env CHROME_DEVTOOLS_AXI_DISABLE_HOOKS=1 npx -y chrome-devtools-axi resize 1440 900
env CHROME_DEVTOOLS_AXI_DISABLE_HOOKS=1 npx -y chrome-devtools-axi screenshot ./tmp/mobile.png --full-page
```

The accessibility snapshot is the default inspection surface. Use it first for structure, names, roles, and actionable targets before resorting to `eval`.

## Lighthouse And Performance

```bash
env CHROME_DEVTOOLS_AXI_DISABLE_HOOKS=1 npx -y chrome-devtools-axi lighthouse --mode navigation --device desktop

env CHROME_DEVTOOLS_AXI_DISABLE_HOOKS=1 npx -y chrome-devtools-axi perf-start --file ./tmp/trace.json --no-auto-stop
env CHROME_DEVTOOLS_AXI_DISABLE_HOOKS=1 npx -y chrome-devtools-axi perf-stop --file ./tmp/trace.json
env CHROME_DEVTOOLS_AXI_DISABLE_HOOKS=1 npx -y chrome-devtools-axi perf-insight <set> LCPBreakdown

env CHROME_DEVTOOLS_AXI_DISABLE_HOOKS=1 npx -y chrome-devtools-axi heap ./tmp/app.heapsnapshot
```

Use Lighthouse for a broad audit. Use perf tracing when you need to inspect a specific interaction or page load more closely.

## Running Multi-Step Scripts

Use `run` when a longer interaction is easier to express as a script than as separate shell calls.

Feed commands on stdin and keep the script focused on one scenario.

## Session Management

The CLI auto-starts its bridge on first use, but explicit control is available:

```bash
env CHROME_DEVTOOLS_AXI_DISABLE_HOOKS=1 npx -y chrome-devtools-axi start
env CHROME_DEVTOOLS_AXI_DISABLE_HOOKS=1 npx -y chrome-devtools-axi stop
```

State lives under `~/.chrome-devtools-axi/`, including the bridge PID file.

## Practical Guidance

- Prefer `snapshot` before guessing targets.
- Prefer `@<uid>` refs over brittle selectors.
- Re-snapshot after clicks, form submits, navigation, or dialog handling.
- Keep output small by using default limits first; add `--full` only when truncation hides needed detail.
- Use headed mode for visual debugging, hover states, or anything timing-sensitive.
- Use `CHROME_DEVTOOLS_AXI_BROWSER_URL` when a task needs to attach to an already-running Chrome session.
