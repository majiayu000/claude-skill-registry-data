---
name: frontend-design
description: "Build distinctive, accessible web and mobile UI from a committed design direction and token plan. Use when building or restyling pages, screens, components or Flutter widgets, or from a DESIGN.md or Stitch design; not for backend work."
---
<!-- ported-from: plugins/ac/skills/frontend-design/SKILL.md sha256:8c310b1ae1cbf0321db9af5bec42633dd5bc59a5dda2200e570942e97d31d93e -->

# frontend-design

UI work in two parts. The decisions (direction, tokens, critique) go to `ac/design-director`, a read-only agent, when the work needs them. The implementation is yours. `DESIGN.md` is the contract between the two: tokens in YAML, intent in prose. Covers web in any framework, iOS-feel and Material-feel interfaces, and Flutter.

## Standing rules

These hold for the whole run and sit before the procedure so a compaction keeps them.

- Direction before code. No palette, typeface or layout is chosen while writing components. Without a visual `DESIGN.md` or a theme with a point of view, run phase 2. With one, build inside it.
- Tokens only. Every colour, size, radius and duration comes from `DESIGN.md` or the theme files; no literal outside them.
- Generic instructions fail. "Clean and modern" lands on the same palette every time; commit to named hex values and typefaces, and keep the patterns in `references/anti-slop.md` out of the result. The user's own words win over any default here.
- Ground the screen in its subject. The audience, the job and the subject's own vocabulary are where distinctive choices come from; the hero shows the most characteristic thing in that world, and a big number with supporting stats and a gradient accent is the default to avoid. Words are design content: a button names its action, an error says how to fix it, an empty state invites (`anti-slop.md`, Subject, hero and copy).
- One platform family per surface. iOS-feel follows the HIG, Android and Material-feel web follow Material 3, Flutter uses the adaptive widgets; numbers in `references/tokens-and-platforms.md`.
- UX first. Every screen designs loading, empty, error and success, not only the happy path. Touch targets 48 px or larger, visible keyboard focus, text contrast 4.5:1, `prefers-reduced-motion` honoured, one signature motion per screen and feedback under 200 ms (`references/motion.md`).
- Build what the brief lists. Models add tests, docs and extra components nobody asked for; name such an idea in the report instead of building it.
- Judge by the render. Your description of the result is not evidence; a screenshot is.
- `ac/design-director` cannot ask the user anything, so the choice it recommends goes to the user through the `question` tool, in the user's language.
- A failed subagent moves down its model chain; it is not a question. A `subagent` call that comes back with a provider failure (`Subagent failed (sessionID: ...)`, a `<subagent ... state="error">` message, an error such as `provider.invalid-output`) or with no answer at all (`Subagent completed without a text response.`, an empty report) failed on its model, not on the work. Continue the same child instead of spawning a new one: call `subagent` again with the same `agent`, `sessionID: "<the sessionID from the failure text>"` and the prompt `Your last turn stopped on a provider error. Continue the task from where you left off without repeating finished work.`, so the child keeps everything it already read. When it answered nothing or broke off mid-stream, continue it on the same model until it has run `retryAttempts` times there (from the `ac_models` tool, 3 in the shipped config); a 5xx was already retried inside the call, so it goes straight on. Then call `ac_fallback_next({ tier: "<the agent name without ac/>", tried: [<every model this call ran on>], session_id: "<the sessionID from the failure text>", status: <the HTTP status, when the error carried one> })`, with `tried` starting at the agent's chain head from `ac_models` unless you set its model yourself, continue the same child with `model: "<the returned value>"` as well, and give that model the same number of attempts. `wait:<seconds>` means that model has retries left: wait that long with one `shell` `sleep` and continue the child on the same model with `tried` unchanged. Start a fresh spawn with the full prompt only when the continuation is refused (`Subagent session not found`, `is not a child of the current session`) or the child's context overflowed. Only `none`, every entry of the chain tried, is a failure to report.

## 1. Read the context

Read `DESIGN.md` (the visual-identity file; a DESIGN.md that describes architecture is the old home of ARCHITECTURE.md, so treat the project as having no visual one and tell the user), the theme and token files, and one to three existing screens, for the stack, the platform target and the conventions. When the UI patterns are unclear in a large repository, send one `ac/explore` brief rather than searching yourself.

## 2. Direction (greenfield or ambiguous)

Spawn `ac/design-director` with `subagent` (`agent: "ac/design-director"`) in `directions` mode. The brief carries the audience, the job the screen does, the platform, the content, the constraints, any taste the user stated, and the files you read. Every call to the director, in any mode, also carries the resolved paths of `references/anti-slop.md` and `references/tokens-and-platforms.md`, plus `references/stitch.md` when the build goes through Stitch (against this skill's base directory), because the agent has no skill directory of its own.

Put its three directions to the user with the `question` tool: each option carries the palette hex values, the typefaces and the rationale, with the director's recommendation first. The user's pick is the direction.

With a design system in place skip this phase. Use `commit` mode for a new screen or a major component, and skip the director for a tweak (spacing, copy, a colour that is already a token). At most one direction or commit call and one critique call per request; it is not a reviewer for your own code.

## 3. Token plan

Write or update `DESIGN.md` with the chosen tokens (format and lint through the `design-md-writer` skill). For a new screen add an ASCII wireframe in your reply, then read the plan against the patterns to rule out and rewrite any part that matches a generic default.

## 4. Build

Work from the tokens, the platform rules and the motion table. When the build runs through the `flow` skill, put the `DESIGN.md` path and the token plan into each worker brief under Codebase conventions; a worker never opens anything the brief omits.

## 5. Verify

Run the loop in `anti-slop.md`: lint `DESIGN.md`, grep for literals outside the tokens, screenshot at 360, 768 and 1280 px wide, check overflow and accessibility. Three fix rounds at most. Say which checks the project could not run.

## 6. Critique (greenfield or a visible redesign)

One `ac/design-director` call in `critique` mode with the screenshots from phase 5 and the brief. Fix the HIGH and MEDIUM findings; LOW ones go in the report. Skip it for a small change.

## 7. Report

Result first: what changed, the direction chosen, the checks run and their results, what a still image could not show (motion, hover, focus), and the ideas you left out.

## Stitch

Only when the user asks for a design-first flow through Google Stitch: read `references/stitch.md` and follow its detection, prompt shape and guardrails. Tell `ac/design-director` in its brief that the build goes through Stitch, so its `commit` output ends with the Stitch prompt block; you send it, with the real copy filled in. Never start it unasked.

## References

| File | Read when |
|---|---|
| `references/tokens-and-platforms.md` | Choosing sizes, type, targets, contrast or the platform's conventions |
| `references/motion.md` | Adding animation, loading states or feedback |
| `references/anti-slop.md` | Writing a brief, reviewing a token plan, writing copy, or verifying a render |
| `references/stitch.md` | The user asks for Stitch: detection, the prompt shape, the loop and the hand-off to code |
