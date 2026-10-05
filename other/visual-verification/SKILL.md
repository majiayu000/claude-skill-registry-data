---
name: visual-verification
description: "Verify UI-facing changes by running a screenshot-analyze-verify loop across configured viewports, with a browser-tool priority cascade (Playwright MCP → Chrome DevTools MCP → CLI fallback → external skill fallback) and bounded iteration. Use after build/runtime verification passes and the diff includes `.tsx`/`.jsx`/`.vue`/`.html`/`.css`/`.scss`/`.svelte` files OR the acceptance criteria mention UI/page/render/display/visual. This skill MUST be consulted because UI changes that pass build and unit tests can still ship blank pages, render-blocking console errors, or broken responsive layouts that no other verification phase catches."
allowed-tools: Bash, Read, Glob, Grep, TaskCreate, TaskList, TaskUpdate
agent: Explore
paths:
  - "**/*.tsx"
  - "**/*.jsx"
  - "**/*.vue"
  - "**/*.svelte"
  - "**/*.html"
  - "**/*.css"
  - "**/*.scss"
  - "**/*.sass"
  - "**/*.less"
---

# Visual Verification

## Contract

Iron law: **UI changes are visually verified or explicitly skipped with a structured result — a
passing build does not prove the page renders, and a screenshot does not prove an interaction
works.** Invoked with `runtime-verification` by `/flow:start` Phase 4 (retried at step 8) and
`/flow:pr` Phase 4 via `Agent(integration-verifier)` when the diff has UI files or criteria
mention UI. Returns the Visual Verification and Visual Evidence tables, one
`Viewport`/`Screenshot`/`Result`/`Observed:` block per viewport for `### Visual analysis`, a
`Step:`-carrying block per step on an interaction criterion, and P1/P2/P3 findings
(`category=visual`), labeled PASS/FAIL/SKIP/SKIP_WARN/SKIP_USER_APPROVED/MANUAL/BLOCKED.
Permitted skips: `SKIP` when no UI signal fires or the dev server is unavailable; `SKIP_WARN`,
`SKIP_USER_APPROVED`, `MANUAL` only via the cascade.

## UI Relevance

Activates when changed files match `\.(tsx|jsx|vue|html|css|scss|svelte)$`, or criteria contain
UI, page, display, render, visual, layout, responsive, component or style. Neither: `SKIP — no UI-relevant changes
detected.` `requireVisualVerification` (default `false`) controls escalation only; an unattempted
UI change still yields `SKIP_WARN`.

## Browser Tool Cascade

Only an **interactive** tool can run a flow: a picture-only tool cannot click, and treating it as
if it could reports a flow that performed none. Playwright MCP and Chrome DevTools MCP are
interactive; the `npx playwright screenshot` CLI and `compound-engineering` browser skills are
**not**.

Playwright MCP exposes `browser_navigate`, `browser_snapshot`, `browser_click`, `browser_type`,
`browser_take_screenshot`, `browser_console_messages`. Take names from the server's docs, not
memory: a call to a tool that does not exist finds nothing and says nothing, so the check never
runs and nothing reports it.

No tool: `SKIP_WARN`, or `BLOCKED` when `requireVisualVerification` is true (escalate per
`references/escalation-format.md`). Never install silently.

## Screenshot-Analyze-Verify Loop

Needs the dev server URL from `runtime-verification`; if it failed to start, return `SKIP` ("dev
server unavailable") — that failure is primary. Bounded by `maxIterations` (default 3). Per page
and viewport in `visualVerification.viewports`: screenshot, analyze, write the block, read
`browser_console_messages`. Findings per `references/finding-schema.md`, prefix `VIS-` or `INT-`,
located at URL path and viewport.

## Interaction Flows

Governed by `visualVerification.flows` (`"on"` | `"off"`, default `"on"`); off, or no interactive
tool, write `Flows: none — {reason}` into `### Visual analysis` instead of step blocks.

A UI criterion gets one to three scenarios when it describes an action a user performs — cue
verbs: click, submit, type, select, toggle, open, navigate, drag — or a risk-map row names a UI
state. Neither: write `Flows: none — no interaction`. Each scenario is at most
`visualVerification.maxFlowSteps` (default 8) steps:

`navigate <route>` · `click <element>` · `type <element> <text>` · `expect <element or text>`

**Targets come from `browser_snapshot`**, never a selector guessed from the criterion's text.
Drive with `browser_click` and `browser_type`; after every step screenshot and write a block
carrying the `Step: {n}/{m} {action}` line shown below.

`Observed:` describes the page AFTER that step. Desktop by default, every viewport when the
criterion mentions responsive or mobile. Step blocks are additional to viewport blocks, never
a replacement. A step whose `expect` is not met is a `category=visual` finding. When
`browser_start_video` is available, cite the path; its absence is **not** a skip, warning or
finding.

## Output Format

One block per page and viewport in `### Visual analysis`, plus one per step:

```
Viewport: {name} {width}x{height}
Screenshot: {path}
Step: {n}/{m} {action}          (interaction steps only)
Result: PASS|FAIL
Observed: {two to four plain sentences}
```

The judge has no file tools and reads only `Observed:`, so name the element the criterion asks
for. `Result: FAIL` when a block has a P1/P2 finding; only `FAIL` and `BLOCKED` fail the gate.

Result meanings, cascade roster, severity classification, the flow procedure, a worked example and
task tracking: [`visual-verification-output.md`](../../references/visual-verification-output.md).
