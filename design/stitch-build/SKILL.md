---
name: stitch-build
description: Create a Stitch project and generate screens from a feature specification or user description. Calls Stitch MCP tools directly to build screens one at a time, following best practices for Stitch prompting.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, mcp__stitch__create_project, mcp__stitch__generate_screen_from_text, mcp__stitch__list_projects, mcp__stitch__list_screens, mcp__stitch__get_screen, mcp__stitch__get_project
---

Build screens in Stitch for: $ARGUMENTS

$ARGUMENTS should include:
- What to build (e.g., "the onboarding flow", "a course detail page", "dashboard screens")
- Optionally: a reference to an existing stitch-export file (e.g., "_docs/stitch-exports/onboarding.md")
- Optionally: an existing Stitch project ID to add screens to
- Optionally: device target ("mobile", "desktop", "tablet")
- Optionally: a sketch, wireframe, or screenshot to use as a visual reference
- Empty — ask the user what they want to build

## Purpose

This skill takes a feature description or a `/stitch-export` specification and builds it in Stitch by calling the MCP tools directly. It creates a project (if needed), then generates screens one at a time using prompts that follow Stitch best practices.

Google Stitch is an experimental AI UI generator powered by Gemini that transforms text prompts and visual references into functional UI designs. It supports text-to-UI generation, image-to-UI conversion, multi-screen app flows, and export to HTML/CSS, Figma, and code.

## Before Starting

1. **Check for an existing export** — If the user references a stitch-export file, read it. The Stitch Prompt sections are ready to use.
2. **Check for an existing project** — If the user provides a project ID, use it. Otherwise, create a new project.
3. **Determine device target** — Default to DESKTOP if not specified. Ask if the feature clearly needs a specific target.
4. **Determine build order** — If building multiple screens, build them in the order a user would encounter them (entry screen first).
5. **Check for visual references** — If the user provides a sketch, wireframe, or screenshot, incorporate it as context alongside the text prompt.

## Stitch Prompting Best Practices

When generating prompts for `generate_screen_from_text`, follow these rules:

### DO:
- **Lead with purpose** — Start every prompt with what the screen IS and what it ACCOMPLISHES
- **Name the user** — "for a student enrolling in a course" not just "an enrollment screen"
- **List content by priority** — Most important information first, supporting details after
- **Include realistic data** — Use domain-appropriate example values, names, prices, dates
- **State actions clearly** — "The user can [verb] [object] which [outcome]"
- **Mention all states** — Tell Stitch about empty, loading, error, and success states (see State Coverage below)
- **One screen per prompt** — Keep each generation focused on a single view
- **Be specific about data** — "Shows 6 course cards with title, instructor name, duration, and price" not "shows some courses"
- **Include functional requirements** — Describe interactive elements, form fields and validation, navigation patterns, and user flows
- **Specify platform context** — Indicate whether this is mobile, tablet, desktop, or responsive web so Stitch can make appropriate layout decisions
- **Mention accessibility needs** — Include requirements like minimum touch target sizes, color contrast needs, keyboard navigation support, and screen reader considerations as functional constraints (not visual prescriptions)

### DON'T:
- **Don't prescribe design** — No colors, fonts, layouts, components, spacing, CSS, Tailwind, or visual style. Even subtle hints like "clean and modern" constrain Stitch unnecessarily.
- **Don't name components** — No "card", "modal", "sidebar", "hero", "navbar". Describe what the user sees.
- **Don't specify arrangement** — No "left side", "top-right corner", "in a grid", "below the fold". Let Stitch decide layout.
- **Don't include code** — No HTML, JSX, TypeScript, or any code snippets
- **Don't over-constrain** — Give Stitch freedom to make design decisions. More constraints = worse output.
- **Don't use vague language** — "A nice dashboard" tells Stitch nothing. Be specific about content and function.

### Prompt Structure Template:
```
Build a [screen type] for [user persona in context].

This screen [purpose — the job it does for the user].

The screen shows:
- [Most important content with example value]
- [Second most important content with example value]
- [Supporting content]

The user can:
- [Primary action — what happens when they do it]
- [Secondary action — what happens]

[Key business rule that affects display]

When there's nothing to show yet, [empty state — what message and what action].
If something fails, [error state — what the user sees and can do about it].

Use realistic [domain] content — [specific guidance].
```

### State Coverage

Every screen prompt should consider these states. Include whichever are relevant:

- **Default** — The screen with typical data loaded
- **Empty** — Nothing to show yet. What message does the user see? What action can they take?
- **Loading** — Data is being fetched. What does the user see while waiting?
- **Error** — Something failed. What does the user see? How do they recover?
- **Success** — An action completed. How is the user confirmed and guided to the next step?
- **Partial** — Only some data is available (e.g., new user with one item instead of many)
- **Edge cases** — Overflow text, missing images, expired content, permission restrictions

### Image-to-UI Workflows

When the user provides a sketch, wireframe, or screenshot as a reference:

1. **Describe what the image shows** — Translate the visual into the content-and-function language Stitch works best with
2. **Specify what to keep vs. change** — "Follow the information hierarchy from this wireframe, but this is for [user persona] who needs to [goal]"
3. **Add missing context** — Sketches rarely include states, data specifics, or interaction details. Fill those gaps in the prompt.
4. **Don't ask Stitch to copy visual style** — Use the reference for structure and content priority, not colors or fonts

## Execution Steps

### Step 1 — Gather Input
If the user referenced a stitch-export file, read it. Extract the screen specs and Stitch prompts. If no export exists, gather requirements conversationally (ask up to 4 questions max).

### Step 2 — Create or Select Project
```
If no project ID provided:
  → Call mcp__stitch__create_project with a descriptive title
  → Record the project ID

If project ID provided:
  → Call mcp__stitch__get_project to verify it exists
  → Call mcp__stitch__list_screens to see what's already built
```

### Step 3 — Generate Screens
For each screen in the specification:

1. **Compose the prompt** using the template above. If a stitch-export exists, use its Stitch Prompt sections. If not, write the prompt from scratch following the best practices.

2. **Call `generate_screen_from_text`** with:
   - `projectId`: the project ID
   - `prompt`: the composed prompt
   - `deviceType`: the target device (DESKTOP, MOBILE, TABLET, or AGNOSTIC)
   - `modelId`: GEMINI_3_1_PRO (default to the most capable model)

3. **Check `output_components`** — If the response contains suggestions, present them to the user before proceeding.

4. **Wait for confirmation** before generating the next screen. Generation takes time — never retry a call that hasn't returned yet.

5. **Report what was built** after each screen generation.

### Step 4 — Review and Report

After all screens are generated:

```markdown
## Stitch Build Complete: [Feature Name]

### Project
- **Title:** [project title]
- **Project ID:** [project ID]

### Screens Generated
1. [Screen name] — [device type] — [status]
2. ...

### Next Steps
- Open Stitch to review the generated screens visually
- Use `/stitch-iterate` to refine individual screens
- Use `/stitch-variants` to explore design alternatives for key screens
- Use `edit_screens` for targeted adjustments (e.g., "make the call-to-action more prominent")
```

## Handling Multiple Screens

When building a multi-screen flow:

1. **Build in user-journey order** — Start with the entry screen, end with the completion screen
2. **One at a time** — Generate, review, then proceed. Don't batch.
3. **Reference previous screens** — When generating screen 2+, mention continuity: "This is the next step after [previous screen]. The user has already [what they did]. Now they need to [current purpose]."
4. **Maintain consistency** — Mention the same terminology, data shapes, and user persona across all prompts so Stitch maintains visual and content consistency.

### Responsive Multi-Screen Strategy

When a feature needs to work across device sizes:

1. **Pick a primary device** — Build all screens for one device first (usually whichever the user will use most)
2. **Complete the flow** — Get the full user journey working on the primary device before adapting
3. **Adapt screen by screen** — When generating for additional devices, reference what the primary version shows and describe how content priority or available actions might shift (e.g., "On mobile, the user still needs to see [critical data] and [primary action], but [secondary content] can be deferred")
4. **Don't prescribe responsive layout** — Describe what content matters at each size. Let Stitch decide how to arrange it.

## Iteration After Generation

Once screens exist in a project, use these strategies to refine:

### Annotate to Edit
Use Stitch's annotation feature for targeted changes without regenerating the whole screen. Describe modifications in content/function terms:
- "The primary action needs to be more prominent"
- "Add a way for the user to see their progress"
- "This section needs to show the instructor's credentials"

### Generate Variants
Request multiple variations to explore different approaches to the same content:
- "Generate 3 variants: one emphasizing the data, one emphasizing the primary action, one emphasizing social proof"
- Variants help when you're unsure which information hierarchy works best

### Progressive Refinement
Start broad, then add specificity in follow-up prompts:
1. Generate the screen with core content and actions
2. Refine by adding states ("Now add the empty state for when the user has no courses yet")
3. Refine by adding secondary content ("Add a way for the user to see related content")

## Model Selection

- **GEMINI_3_1_PRO** — Default. Best quality. Use for important screens, complex layouts, or when quality matters most.
- **GEMINI_3_FLASH** — Faster, good quality. Use for rapid iteration, simple screens, or when exploring ideas quickly.

Choose based on the screen complexity and user's preference for speed vs. quality.

## Anti-Patterns

- **Don't retry failed generations** — Stitch generation takes time. If a call times out, check with `get_screen` later rather than retrying immediately.
- **Don't batch all screens at once** — Generate one at a time so the user can review and course-correct.
- **Don't include design direction in prompts** — Even subtle hints like "clean and modern" constrain Stitch unnecessarily. Focus on content and function.
- **Don't generate without context** — A prompt like "build a dashboard" produces generic results. Always include who uses it, what data it shows, and what actions are available.
- **Don't skip the export step for complex features** — If the feature has more than 3 screens, run `/stitch-export` first to plan the screen flow before building.
- **Don't forget states** — A screen with only the happy path is incomplete. Always consider empty, error, and loading states.
- **Don't copy visual style from references** — When using sketches or screenshots as input, extract the content structure and user intent, not the colors, fonts, or layout decisions.

## Workflow

Part of the Stitch workflow: stitch-build → stitch-iterate → stitch-variants → stitch-export
