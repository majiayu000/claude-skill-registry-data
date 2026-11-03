---
name: frontend-design
description: "Build distinctive, accessible web and mobile UI from a committed design direction and token plan."
when_to_use: "Use when building or restyling pages, screens, components or Flutter widgets, or from a DESIGN.md or Stitch design; not for backend work."
---

# ac:frontend-design

UI work in two parts. The decisions (direction, tokens, critique) go to `ac:design-director`, a read-only Opus agent, when the work needs them. The implementation is yours. `DESIGN.md` is the contract between the two: tokens in YAML, intent in prose. Covers web in any framework, iOS-feel and Material-feel interfaces, and Flutter.

## Standing rules

These hold for the whole run and sit before the procedure so a compaction keeps them.

- Direction before code. No palette, typeface or layout is chosen while writing components. Without a visual `DESIGN.md` or a theme with a point of view, run phase 2. With one, build inside it.
- Tokens only. Every colour, size, radius and duration comes from `DESIGN.md` or the theme files; no literal outside them.
- Generic instructions fail. "Clean and modern" lands on the same palette every time; commit to named hex values and typefaces, and keep the patterns in `${CLAUDE_SKILL_DIR}/references/anti-slop.md` out of the result. The user's own words win over any default here.
- Ground the screen in its subject. The audience, the job and the subject's own vocabulary are where distinctive choices come from; the hero shows the most characteristic thing in that world, and a big number with supporting stats and a gradient accent is the default to avoid. Words are design content: a button names its action, an error says how to fix it, an empty state invites (`anti-slop.md`, Subject, hero and copy).
- One platform family per surface. iOS-feel follows the HIG, Android and Material-feel web follow Material 3, Flutter uses the adaptive widgets; numbers in `${CLAUDE_SKILL_DIR}/references/tokens-and-platforms.md`.
- UX first. Every screen designs loading, empty, error and success, not only the happy path. Touch targets 48 px or larger, visible keyboard focus, text contrast 4.5:1, `prefers-reduced-motion` honoured, one signature motion per screen and feedback under 200 ms (`${CLAUDE_SKILL_DIR}/references/motion.md`).
- Build what the brief lists. Sonnet adds tests, docs and extra components nobody asked for; name such an idea in the report instead of building it.
- Judge by the render. Your description of the result is not evidence; a screenshot is.
- `ac:design-director` cannot ask the user anything, so the choice it recommends goes to the user through `AskUserQuestion`, in the user's language.

## 1. Read the context

Read `DESIGN.md` (the visual-identity file; a DESIGN.md that describes architecture is the old home of ARCHITECTURE.md, so treat the project as having no visual one and tell the user), the theme and token files, and one to three existing screens, for the stack, the platform target and the conventions. When the UI patterns are unclear in a large repository, send one `ac:explore` brief rather than searching yourself.

## 2. Direction (greenfield or ambiguous)

Spawn `ac:design-director` in `directions` mode. The brief carries the audience, the job the screen does, the platform, the content, the constraints, any taste the user stated, and the files you read.

Put its three directions to the user with `AskUserQuestion`: each option carries the palette hex values, the typefaces and the rationale, with the director's recommendation first. The user's pick is the direction.

With a design system in place skip this phase. Use `commit` mode for a new screen or a major component, and skip the director for a tweak (spacing, copy, a colour that is already a token). At most one direction or commit call and one critique call per request; it is not a reviewer for your own code.

## 3. Token plan

Write or update `DESIGN.md` with the chosen tokens (format and lint through `ac:design-md-writer`). When the project has none, also propose one `.claude/rules/ui.md` scoped with `paths:` to the view files that points at DESIGN.md, through `ac:claude-md-rules-creator`, so later sessions load the tokens when they touch UI. For a new screen add an ASCII wireframe in your reply, then read the plan against the patterns to rule out and rewrite any part that matches a generic default.

## 4. Build

Work from the tokens, the platform rules and the motion table. When the build runs through `ac:flow`, put the `DESIGN.md` path and the token plan into each worker brief under Codebase conventions; a worker never opens anything the brief omits.

## 5. Verify

Run the loop in `anti-slop.md`: lint `DESIGN.md`, grep for literals outside the tokens, screenshot at 360, 768 and 1280 px wide, check overflow and accessibility. Three fix rounds at most. Say which checks the project could not run.

## 6. Critique (greenfield or a visible redesign)

One `ac:design-director` call in `critique` mode with the screenshots from phase 5 and the brief. Fix the HIGH and MEDIUM findings; LOW ones go in the report. Skip it for a small change.

## 7. Report

Result first: what changed, the direction chosen, the checks run and their results, what a still image could not show (motion, hover, focus), and the ideas you left out.

## Stitch

Only when the user asks for a design-first flow through Google Stitch: read `${CLAUDE_SKILL_DIR}/references/stitch.md` and follow its detection, prompt shape and guardrails. Tell `ac:design-director` in its brief that the build goes through Stitch, so its `commit` output ends with the Stitch prompt block; you send it, with the real copy filled in. Never start it unasked.

## References

| File | Read when |
|---|---|
| `${CLAUDE_SKILL_DIR}/references/tokens-and-platforms.md` | Choosing sizes, type, targets, contrast or the platform's conventions |
| `${CLAUDE_SKILL_DIR}/references/motion.md` | Adding animation, loading states or feedback |
| `${CLAUDE_SKILL_DIR}/references/anti-slop.md` | Writing a brief, reviewing a token plan, writing copy, or verifying a render |
| `${CLAUDE_SKILL_DIR}/references/stitch.md` | The user asks for Stitch: detection, the prompt shape, the loop and the hand-off to code |
