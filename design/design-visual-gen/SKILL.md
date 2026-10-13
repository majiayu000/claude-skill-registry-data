---
name: design-visual-gen
description: Create simple vector-style illustrations and diagrams for help text, documentation, onboarding, and feature explanations, matching the project's visual language. Use for schematic UI miniatures and explanatory images, including -var / --variations galleries; use a raster image skill for photographic or painterly artwork.
---

# Simple Visual Gen

Make a small visual that explains one idea: simplified windows, cards, text strokes, selection, relationships, or a short sequence. Default to editable SVG rather than an image-generation service. These are help illustrations, not full UI redesigns or screenshots.

Use `/design-visual-gen` in Claude Code. From Codex, load this same source with `$ccref /design-visual-gen` and pass the request and flags after it. The workflow uses ordinary file editing, shell commands, and available browser/vector-rendering tools; no harness-specific API is required.

## Interpret the request

- No variation flag: produce one finished visual. When asked to update help/docs, integrate the visual and requested explanation into the existing documentation/component system.
- `-var` and `--variations` are aliases, accepted anywhere in the request. Accept a positive integer after either flag or with `=`; also honor a natural-language count such as “10 patterns.” Default to 3 if variations are requested without a count. A requested count without the flag also means variations. Clarify conflicting counts rather than silently reducing the work.
- Variations are candidate artifacts in the project's cclogs directory. Do not choose and install a candidate in production unless the request also authorizes selection/integration. Continue any separately requested prose work.
- Standalone image requests without a destination also go to cclogs. Use an explicit requested destination when supplied.

Examples:

```text
/design-visual-gen make the image of Pile View of our app
Update the Pile View help explanation; use /design-visual-gen for the diagram.
/design-visual-gen -var 10 Pile View
/design-visual-gen Pile View --variations=10
```

## Ground the drawing

Read the feature documentation or implementation before choosing the metaphor. Verify which actions and states actually exist; arrows and labels must not invent behavior. Use neutral sample content, not personal notes or real credentials.

Look for project tone/design guidance, tokens, existing help art, icon shapes, and the intended embedding context. Inspect user-supplied references. Derive palette, corner radius, stroke weight, spacing, density, and light/dark behavior from those sources. Record the important choices in artifact notes. Project guidance wins over the neutral default below. Do not bake one project's identity or paths into this global skill.

When no guidance exists, use neutral outlines, generous whitespace, short text strokes, small corners, and one restrained accent for the teaching point. Avoid decorative gradients, shadows, perspective, or large filled panels unless the project uses them. Keep a single visual hierarchy; do not shrink a whole screenshot until it becomes illegible.

## Choose the implementation

- Standalone: self-contained SVG with a `viewBox`, no external assets/fonts/scripts, and an accessible title/description. Supply alt text describing the concept. Prefer basic shapes and paths; keep labels sparse and readable at the intended display size.
- Existing help system: follow its native SVG/JSX or HTML/CSS illustration convention. Map colors to its actual theme tokens. Do not add a parallel illustration framework just to insert one image.
- Inline SVG can inherit theme variables/currentColor. An SVG loaded via `<img>` cannot inherit the page's CSS variables: provide internal defaults and suitable theme exports or internal theme rules instead. Namespace IDs and scope internal style selectors if multiple SVGs share a document; avoid leaking generic rules into the host.
- Static is the default. Add motion only when requested or required by the host; retain a meaningful static/reduced-motion state.

## Variations and delivery

Resolve cclogs using `node "$HOME/.claude/scripts/get-logdir.js"` from the project root, or follow the available `/cclogs` skill. If the resolver is unavailable, use `$DROPBOX_CCLOGS_DIR/<repo-basename>` and report that worktree/numbered-sibling folding was unavailable. If neither exists, ask for an output location rather than guessing a Dropbox path.

Create a fresh `<timestamp>-design-visual-gen-<subject>/` under the resolved location; preserve earlier runs. Keep project-specific generators and evidence here, not inside this global skill.

For N variations, produce exactly N genuinely different compositions or explanatory approaches to the same subject. Decide each candidate's teaching point first. Changing only hue, stroke weight, or theme does not count as a new variation. Keep a coherent visual family unless the user asks to explore styles.

Include:

- Numbered, descriptively named editable SVGs, or the requested native format.
- A local, self-contained `index.html` gallery using relative paths or embedded art, with names and a sentence explaining each candidate. Show intended-size previews; offer light/dark comparison when relevant. It should open without a build step or network.
- Brief artifact notes with the request/count, source context, palette decisions, alt text, any simplification, and a recommendation for the intended placement. A contact sheet is useful for larger sets.

For a single integrated diagram, put the asset/component in the established project location, wire it into the requested help text, and verify that embedding. Do not leave only a proposed edit.

## Verify the result

Parse SVG/XML and check local references. Render in a browser or available vector renderer and visually inspect at the intended size. For a gallery, inspect every candidate, confirm the count, and check narrow layout plus supported themes. Fix clipping, unreadable labels, weak hierarchy, inconsistent styling, and misleading behavior. Run relevant project checks if application/docs files changed; artifact-only work does not require the app's full test suite.

If rendering is unavailable, disclose that visual inspection remains unverified. Finish with links to the image or gallery and a short explanation, rather than dumping SVG source into chat.
