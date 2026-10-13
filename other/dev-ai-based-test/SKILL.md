---
name: dev-ai-based-test
description: >-
  AI-based testing via subagent + a per-task test-flow skill. Use when the user wants to verify
  something that mechanical assertions can't fully capture — image recognition, visual size/position
  comparison, animation smoothness, multi-step manual flows that need AI judgment. Triggers:
  'AI-based test', 'AI test', 'visual verify', 'image recognition test', 'manual operation test',
  'human-eye check', 'verify visually', 'compare screenshots', 'looks the same', 'looks correct'.
  The skill's job is to (1) author a focused test-flow skill that captures the exact procedure +
  verdict criteria, then (2) dispatch a verification subagent via the Agent tool that loads BOTH the
  test-flow skill AND a browser-driving skill (/verify-ui primary, /headless-browser fallback) so
  the subagent has clear context and consistent verdicts. NEVER uses `claude -p` — subagent dispatch
  goes through the Agent tool exclusively.
---

# Dev: AI-based test

AI-based testing for things that can't be cleanly mechanically asserted: image recognition, visual size / position parity, animation correctness, multi-step manual flows where a human eye would catch the bug but `assertEqual` won't.

The deliverable is **not just "run a test"** — it's a reusable, focused **test-flow skill** that captures the test procedure with clear context, plus a dispatched verification subagent that loads that skill alongside a browser-driving skill.

## When to use

- User explicitly asks for AI-based / visual / human-eye verification — "test this with AI", "verify visually", "make sure it looks the same", "image recognition test".
- A symptom is reported that mechanical assertions can't see: image rendered visibly smaller, animation stutters in a way frame-rate doesn't capture, a screenshot looks "off" in a way the user can describe but DOM measurements agree.
- A multi-step manual flow needs verification (drag-and-drop a real file, then compare two phases visually) and the existing fixed-suite specs don't cover it.
- The user wants the verdict produced **by an AI subagent** so it has fresh, isolated context — instead of inlining the test into the main agent's prompt where context drift erodes consistency.

## When NOT to use

- The test is a clean computed-style or DOM-rect assertion → use `/verify-ui` directly, no subagent needed.
- The test is a fixed Playwright spec that always runs the same way → write it as `.spec.ts` in `e2e/`, run via `pnpm exec playwright test`. No AI judgment required.
- The user wants a regression gate for CI — AI verdicts are non-deterministic. Reserve this for local b4push / one-shot evidence; pair with a deterministic spec for CI.

## Hard rule: NEVER use `claude -p`

The subagent dispatch in this skill uses the **Agent tool** (the same tool the main agent uses to spawn `subagent_type: general-purpose`, `Plan`, `Explore`, etc.). Never `claude -p`, never a subprocess shell invocation. The reasons matter:

- The Agent tool returns a structured result message into the parent's context. `claude -p` produces stdout text the parent has to re-parse and interpret.
- The Agent tool respects the parent's session permissions, memory, and skill availability. `claude -p` starts a fresh process that may not see project skills the parent does.
- The Agent tool's lifecycle is observable in the conversation. `claude -p` is opaque — if it stalls or fails, the parent doesn't get clean error signaling.

If you find yourself reaching for `claude -p` for a subagent dispatch, stop and use the Agent tool instead.

## Workflow

The skill has two halves: **author the test-flow skill**, then **dispatch the verification subagent**.

### Half 1 — author the test-flow skill

A test-flow skill is a small, focused skill at `$HOME/.claude/skills/test-flow-<topic>/SKILL.md` (or project-local `.claude/skills/test-flow-<topic>/SKILL.md`) that captures:

- **What scenario** to drive (the exact user-reproduce flow — open template, drop fixture, click button, etc.)
- **What to capture** (which screenshots, which DOM measurements, which evidence)
- **The verdict criteria** (specifically: what counts as PASS vs FAIL, tolerance numbers, threshold ratios)
- **The output format** (what the subagent should return — a JSON-like structured result with named fields)

The skill is **per-task**, not per-app. A single project will accumulate multiple test-flow skills as different tests are needed.

#### Authoring checklist

- [ ] Name follows convention: `test-flow-<short-topic-slug>` (e.g. `test-flow-composer-image-same-size`, `test-flow-animation-frame-pacing`).
- [ ] Description includes BOTH the trigger keywords AND a one-line "use when" — the test-flow skill is triggered by the verification subagent's prompt, so it has to load when the subagent reads its instructions.
- [ ] Body is **self-contained** — the subagent will start fresh with NO conversation history; the test-flow skill body must include everything needed to drive and verdict the test.
- [ ] Procedure is numbered and concrete — exact selectors, exact URLs, exact viewport sizes, exact fixture paths.
- [ ] Verdict criteria are mechanical where possible (tolerance numbers, pixel deltas) and AI-judgment-only where necessary (visual sameness, image recognition).
- [ ] Output schema is explicit — what fields the subagent must return (e.g. `pgenImageWidth`, `composerImageWidth`, `ratio`, `verdict`, `summary`).

Use the `skill-creator` skill's `init_skill.py` to scaffold the new test-flow skill, then write its body. Format with `pnpm dlx @takazudo/mdx-formatter --write <path-to-SKILL.md>`.

### Half 2 — dispatch the verification subagent

After the test-flow skill is written, dispatch a subagent via the Agent tool:

```
Agent({
  subagent_type: "general-purpose",  // browser-driving + structured output, no specialty needed
  description: "<short description>",
  prompt: `<self-contained brief — see template below>`,
})
```

The subagent's prompt must include:

- **Goal:** one sentence describing what verdict to produce.
- **Skills to load:** invoke `/test-flow-<topic>` (the just-authored skill) AND a browser-driving skill — `/verify-ui` for computed-styles / screenshot comparison, OR `/headless-browser` for multi-step interactive flows.
- **Inputs:** any per-run inputs the test-flow skill needs (e.g. the W2 PR preview URL, the fixture image path, the viewport size).
- **Output contract:** match the output schema declared in the test-flow skill.

#### Subagent prompt template

```
You are a verification subagent. Produce a structured verdict using the test-flow skill below.

## Goal
{one-sentence verdict goal, e.g. "Determine whether the composer-side image visually matches the pgen-side image at default landing viewport."}

## Skills to load
- /test-flow-<topic>  — the test procedure and verdict criteria. Read this first.
- /verify-ui          — primary browser-driving skill (computed-styles + screenshots).
- /headless-browser   — fallback if /verify-ui doesn't fit the task shape.

## Inputs
- Preview URL: <resolved URL — pass from the parent>
- Fixture: <path or asset reference>
- Viewport: <e.g. 1440x900>
- Any other per-run knobs the test-flow skill expects

## Output contract
Return a structured result message containing exactly these fields:
{ <list each field from the test-flow skill's output schema> }

Plus a `summary` field with a one-line human-readable verdict.

## Don'ts
- Don't improvise the test procedure — follow /test-flow-<topic> exactly.
- Don't change the verdict tolerance — it's locked in /test-flow-<topic>.
- Don't post anywhere — return the result to me; I (the parent agent) handle posting.
```

### After the subagent returns

The parent agent receives the structured result and decides what to do with it: post to a PR comment, write to an evidence file, gate a workflow step, etc. The test-flow skill stays on disk for reuse — next time the same test class is needed, the existing skill is invoked without re-authoring.

## Choosing the browser-driving skill — primary vs fallback

| Skill | Best for | When to fall back |
|---|---|---|
| `/verify-ui` | Deterministic computed-style checks; pure pgen-vs-composer parity; CSS / layout assertions | Cannot drive multi-step UI flows beyond single-page reads |
| `/headless-browser` | Multi-step interactive flows (drag-drop a file, click → screenshot → click → screenshot); element bounding-rect reads via Playwright CLI | Slightly heavier; only use when /verify-ui can't reach the test surface |

The test-flow skill should name BOTH so the subagent picks based on the task shape. If `/verify-ui` returns "cannot perform this flow" the subagent transparently switches to `/headless-browser` without re-prompting the parent.

## Reusability — the test-flow skill outlives the test

A test-flow skill is **not** a one-shot scaffold for a single PR. It's a permanent artifact that captures "how to verify this class of behavior in this codebase." When a similar test is needed later (regression check, repeated verification across PRs), invoke the same test-flow skill — the AI subagent gets the same context, produces consistent verdicts.

Sign that you're using this pattern correctly:

- The test-flow skill is checked into the project's `.claude/skills/` (project-scope, shared with the team), not just `$HOME/.claude/skills/` (personal-only).
- Subsequent invocations DO NOT re-author the skill — they just dispatch a fresh subagent that loads it.
- Updates to the procedure happen by editing the test-flow skill, not by inlining new instructions in the subagent prompt.

## Example skeleton — what a real test-flow skill looks like

```markdown
---
name: test-flow-composer-image-same-size
description: Verify the composer-side image visually matches the pgen-side image at default landing viewport. Use when /dev-ai-based-test dispatches a subagent for issue #1678 / composer-image-same-size verification.
---

# Test flow: composer image same size as pgen

## Scenario
1. Open <preview URL from inputs> at viewport 1440x900.
2. Click the first template card.
3. Click "Start cropping the pattern".
4. Drop `packages/pattern-gen-viewer/e2e/fixtures/red-100-fits-composition.png` on the pgen canvas-layer.
5. Capture screenshot A (pgen with image visible).
6. Click "Commit selection and open Composer".
7. Wait for composer mount (composer-art-canvas visible).
8. Capture screenshot B (composer with image visible).

## Measurements
- pgen image width (CSS px): read via `__pgenLayerState.getSelectedLayerTransform()` + pgen canvas CSS scale.
- composer image width (CSS px): read via `__composerTest.getState()` + cameraZoom + composer canvas CSS rect.
- ratio = composer / pgen.

## Verdict
PASS if ratio ∈ [0.95, 1.05] (±5%). FAIL otherwise.

## Output schema
{
  pgenImageWidth: number,
  composerImageWidth: number,
  ratio: number,
  delta: number,
  verdict: "PASS" | "FAIL",
  summary: string,
  pgenScreenshot: string (path),
  composerScreenshot: string (path),
  toolUsed: "verify-ui" | "headless-browser"
}
```

The example shows the shape; the verification subagent reads this and follows the procedure verbatim.
