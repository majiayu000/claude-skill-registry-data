---
name: design-md-writer
description: "Write or audit a visual-identity DESIGN.md: design tokens plus rationale in the Google Labs format, for UI agents. Use when a UI needs a brand or style spec or a token file for the `frontend-design` skill; the architecture doc is the `architecture-md-writer` skill."
---
<!-- ported-from: plugins/ac/skills/design-md-writer/SKILL.md sha256:76de89b3ada29468c4e118d27251ad78b12e7586b0d7a1afe663a7f1d2d8b656 -->

# DESIGN.md Writer

DESIGN.md tells an agent how an interface looks: exact token values (colours, type, radii, spacing, component styles) in YAML, and the reason for each in prose. The `frontend-design` skill builds from it, `ac/design-director` commits to it and critiques against it, and Google Stitch imports it as a design system. This skill writes it, updates it, or audits an existing one.

Scope: one file plus one pointer. It records a visual direction; it does not choose one. A palette or typeface comes from an existing theme, from the user, or from `ac/design-director` through the `frontend-design` skill. It does not edit UI code, README or CHANGELOG, and it does not write the architecture doc (the `architecture-md-writer` skill), the project's why and scope (the `project-md-writer` skill) or its commands and conventions (write AGENTS.md by hand). Report adjacent problems instead of fixing them.

The format is Google Labs' `design.md`, spec version `alpha`; the CLI `@google/design.md` is at 0.4.0 (checked 2026-11-01). Expect changes, and read `references/visual-identity.md` for the schema, section order and tooling before writing.

## Where it sits

| Layer | File | Holds |
|---|---|---|
| Rules | AGENTS.md | commands, conventions, off-limits |
| How it is built | ARCHITECTURE.md | boundaries, invariants, flows |
| How it looks | DESIGN.md | tokens, component styles, visual rationale |

opencode loads AGENTS.md into every agent in full at session start, so DESIGN.md stays out of it and one pointer line with a UI trigger is the wiring.

## Pick the mode

- No DESIGN.md exists: write.
- One exists and lints clean: update in place, keep its headings.
- One exists and agents ignore it, or its quality is unknown: audit first and report ranked findings; edit only when the user asked for the fix.
- The existing DESIGN.md describes architecture (no YAML tokens, sections like Components and Data flow): stop. Ask with the `question` tool whether to `git mv DESIGN.md ARCHITECTURE.md` (then the `architecture-md-writer` skill owns it) and write the visual file fresh. The move is the user's call.

## Workflow

### 1. Find what exists

`glob` `DESIGN.md` and `docs/DESIGN.md`; find the theme: Tailwind config or `@theme` CSS, CSS custom properties, Flutter `ThemeData` and `ColorScheme`, an iOS asset catalog, a Stitch export under `.stitch/`. Read any `ac/design-director` output in the conversation.

Success: you know the mode, the target path and which source supplies the values.

### 2. Collect the decisions

Existing theme files are the source: derive the tokens from them and verify each value. A new identity takes its values from the chosen `ac/design-director` direction or `commit` plan (named hex values, typefaces, radius, spacing unit), verbatim. Ask the user, with the `question` tool in their language, only for brand intent the code cannot show: audience, tone, what to avoid.

With no theme and no direction, stop and say so: run phase 2 of the `frontend-design` skill, which asks `ac/design-director` for directions. A palette invented here is the generic default the whole chain exists to avoid.

Success: every token traces to a file, a director decision or a user answer.

### 3. Write from the template

Read `assets/DESIGN.template.md` and fill it. `references/example.md` shows a filled one that lints clean; match its register.

Success: no placeholder left, every colour has a role sentence, 150 lines or fewer.

### 4. Lint and export

```bash
npx @google/design.md@0.4.0 lint DESIGN.md
```

It exits 1 on errors (a `broken-ref` is one) and prints warnings for contrast, missing primary, orphaned tokens and section order. Fix errors, read every warning, and rerun. The linter checks contrast only on component `backgroundColor` and `textColor` pairs, so check the text roles you use outside components (muted text on the surface) against 4.5:1 yourself.

Export when the project consumes the tokens: `--format css-tailwind` (Tailwind v4 `@theme`), `json-tailwind` (v3), `dtcg` or `css-vars`. There is no Flutter exporter; map the tokens by hand as the `frontend-design` skill's `references/tokens-and-platforms.md` describes.

Success: lint exits 0 and the warnings left are ones you can defend.

### 5. Wire the pointer

Add one line to AGENTS.md if none points here: "Before changing UI, read DESIGN.md and build from its tokens." Use a plain path, not an `@import`.

Success: the line exists and names DESIGN.md.

## Rules

- Tokens carry exact values and prose carries the reason. A token without a role sentence gets used arbitrarily; a role sentence without a token gets approximated.
- One role per colour ("the sole driver for interaction"), not a mood. `primary` is required.
- Name every typeface with its source (system stack, a Google Fonts family, the project's own files). No list of acceptable typefaces is a mandate.
- Components reference tokens with `{path}` instead of repeating a value; a hover or pressed state is its own key (`button-primary-hover`). Define a colour only where a component uses it: the linter warns about an orphaned token, except for the standard family names (`primary`, `secondary`, `tertiary`, `error`, `surface`, `background`, `outline`) and for a family some component already references.
- Elevation has no token group in the spec: write the shadow values in prose under Elevation & Depth.
- Do's and Don'ts are concrete and checkable ("one primary button per view"). Carry the patterns the brief rules out, from the `frontend-design` skill's `references/anti-slop.md`.
- Write the tokens in the front matter. The 0.4.0 parser also merges every fenced `yaml` block in the file into the tokens, although its bundled spec does not document them, so keep no illustrative `yaml` fence in a DESIGN.md: a repeated top-level key rejects the file.
- Sections keep the spec's order and names, so agents and the linter can find them. Leave a section out with `omitted:` and a reason, not with an empty heading.
- State what is true now. When the theme file and DESIGN.md disagree, that is an audit finding and the user decides which wins.
- Write in the project's documentation language, English by default.

## Update rules

Update DESIGN.md in the same change as the code when a change alters a token value in the theme, adds a component style, or changes the direction. Run `npx @google/design.md@0.4.0 diff DESIGN.md.old DESIGN.md` against the previous copy (it exits 1 on regressions) and lint again.

## Audit checklist

- Lint exits 0, no `broken-ref`, and each warning is explained.
- Every colour has a role sentence; Do's and Don'ts are checkable rules.
- Token values match the theme files (grep both).
- Text roles on their surfaces meet 4.5:1 (3:1 for large text).
- Every typeface has a named source.
- It is a visual file: YAML tokens first, not an architecture doc.
- 300 lines or fewer, and a pointer in AGENTS.md exists.

## References

| File | Load when |
|---|---|
| `references/visual-identity.md` | Always, before writing: schema, section order, lint rules, exports |
| `assets/DESIGN.template.md` | Writing or restructuring the file |
| `references/example.md` | Matching register and level of detail |
