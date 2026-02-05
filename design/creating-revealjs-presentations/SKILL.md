---
name: creating-revealjs-presentations
description: >
  Creates, customizes, and troubleshoots Quarto Reveal.js presentations with proper SCSS theming,
  layout patterns, and extensions. Use when authoring .qmd slides or styling with SCSS.
---

## Purpose

Guide the agent to write **production-ready Quarto Reveal.js slides** in a single pass:
- Correct YAML configuration
- SCSS theme customization (variables + rules)
- Layout patterns (columns, absolute positioning, backgrounds)
- Extension usage (Font Awesome, embedio, editable)
- Accessibility and maintainability

## When to Use This Skill

Use when:
- Creating new `.qmd` presentation files
- Writing or modifying SCSS themes for Reveal.js
- Adding extensions (icons, embeds, interactive elements)
- Troubleshooting slide rendering issues
- Converting content into slide format

Do NOT use when:
- Working with Quarto documents that are NOT presentations
- The task involves only HTML/PDF/DOCX output formats

## Inputs and Outputs

**Inputs:**
- User's content requirements (topic, structure, style preferences)
- Existing .qmd files or SCSS to modify
- Design constraints (colors, fonts, branding)

**Outputs:**
- `.qmd` files with proper YAML frontmatter
- SCSS files with `/*-- scss:defaults --*/` and `/*-- scss:rules --*/` sections
- Extension installation commands when needed

## Behavior and Guidelines

### YAML Configuration

1. **Theme layering**: Use `theme: [default, styles/custom.scss]` — later entries override earlier ones.
2. **Scroll View**: Enable with `scroll-view: true` for Reveal.js v5 (Quarto 1.6+).
3. **Title slide backgrounds**: Use `title-slide-attributes:` with `data-` prefixed keys.

### SCSS Structure

1. **Two required sections**:
   - `/*-- scss:defaults --*/` for variables (colors, fonts, sizes)
   - `/*-- scss:rules --*/` for CSS rules
2. **Override specificity**: Prefix rules with `.reveal .slide` to beat built-in styles.
3. **Background image paths**: Use `url("../../../../../assets/...")` from compiled CSS location (5 levels up).

### Layout Patterns

1. **Columns**: Use `:::: {.columns}` with `::: {.column width="X%"}` children.
2. **Fit text**: Wrap with `::: r-fit-text` for auto-sizing headlines.
3. **Stack**: Use `.r-stack` to overlay elements revealed sequentially.
4. **Absolute positioning**: Add `{.absolute top="X" left="Y"}` to images/divs.
5. **Vertical center**: Use `.center` class for vertical centering.

### Advanced Features

1. **Fragments**: 20+ animation effects (`fade-*`, `highlight-*`, `grow`, etc.) with `fragment-index` ordering.
2. **Auto-animate**: Automatic transitions between slides using `data-id` matching.
3. **Vertical slides**: Create slide stacks with navigation modes (linear/vertical/grid).
4. **Parallax backgrounds**: Scrolling background images for depth effect.
5. **Presentation sizing**: Control dimensions, margins, and scaling.

### Extensions

1. **Font Awesome**: `quarto add quarto-ext/fontawesome` → `{{< fa icon >}}`
2. **embedio**: `quarto add coatless-quarto/embedio` → `{{< revealjs file="..." >}}`
3. **editable**: `quarto add EmilHvitfeldt/quarto-revealjs-editable` → drag/resize in preview

### Accessibility

1. Background images cannot have alt text — add visible text descriptions.
2. Use `title="..."` in Font Awesome shortcodes.
3. Ensure color contrast (avoid pure black/white).

## Step-by-Step Procedure

1. **Clarify requirements**: Ask about topic, slide count, style preferences, required extensions.

2. **Set up YAML frontmatter**:
   - Define `format: revealjs` with theme, transitions, slide-number
   - Add `execute: echo: false` for code-heavy slides
   - Reference `reference.md` § Minimal YAML Template

3. **Create SCSS theme** (if customizing):
   - Define color palette in `scss:defaults` ($body-bg, $body-color, $link-color)
   - Add font family and size variables
   - Write rules in `scss:rules` with `.reveal .slide` prefix

4. **Author slide content**:
   - Use `##` for slide breaks (or `---` for untitled slides)
   - Apply layout patterns from reference
   - Add speaker notes with `::: {.notes}`

5. **Install extensions** (if needed):
   - Provide `quarto add` commands
   - Show YAML activation (`revealjs-plugins`, `filters`)

6. **Validate**:
   - Check `quarto preview` runs without errors
   - Verify Scroll View (`R` key) and Print View (`?view=print`)

7. **Summarize** what was created and any assumptions made.

## Use of Reference Files

Load specific modules from `resources/` based on task:

| Module | When to Load |
|--------|--------------|
| `resources/yaml-config.md` | YAML frontmatter, sizing, navigation |
| `resources/scss-theming.md` | Theme customization, variables |
| `resources/layout.md` | Column, stack, positioning patterns |
| `resources/animation.md` | Fragments, auto-animate effects |
| `resources/extensions.md` | FontAwesome, embedio, editable |
| `resources/advanced.md` | Parallax, vertical slides, templates |
| `resources/troubleshooting.md` | Debugging rendering issues |

## Examples

**Example 1 – New presentation with custom theme**

- **User goal:** "Create slides for a tech talk with dark theme and code highlighting"
- **Expected behavior:**
  1. Generate YAML with `theme: [default, styles/dark.scss]`
  2. Create SCSS with dark $body-bg, light $body-color
  3. Enable `code-line-numbers: true`, `code-overflow: wrap`
  4. Provide slide structure with `##` headers

**Example 2 – Add icons and embeds**

- **User goal:** "Add GitHub icon and embed another slide deck"
- **Expected behavior:**
  1. Provide `quarto add quarto-ext/fontawesome` command
  2. Show `{{< fa brands github >}}` syntax
  3. Provide `quarto add coatless-quarto/embedio` command
  4. Show `{{< revealjs file="other.html" >}}` syntax

**Example 3 – Fix background image not showing**

- **User goal:** "My SCSS background-image doesn't work"
- **Expected behavior:**
  1. Diagnose path issue (CSS compiles to deep directory)
  2. Suggest `url("../../../../../assets/images/bg.jpg")` path
  3. Explain the 5-level depth from `_output/index_files/libs/revealjs/dist/theme/`
