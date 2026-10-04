---
name: design-md
version: 1.0.0
description: |
  Generate a DESIGN.md file that conforms to the Stitch (Google Labs) design.md alpha spec.
  Auto-discovers the project's design tokens, components, and brand context, then emits
  YAML frontmatter (machine-readable) + 8 standard markdown sections (human-readable).
  Single source of design truth that Claude Code, Cursor, Stitch, and any AI coding agent
  understand the same way.
  Triggers: "create DESIGN.md", "design system docs", "design.md spec", "Stitch-format design doc",
  "DESIGN.md 만들어줘", "디자인 시스템 문서화", "design.md 스펙", "Stitch 포맷 디자인 문서"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
  - WebFetch
triggers:
  - create DESIGN.md
  - design md file
  - design.md
  - Stitch design spec
  - design system docs
  - design token documentation
  - DESIGN.md 생성
  - 디자인 md 파일
  - Stitch 디자인 스펙
  - 디자인 시스템 문서
  - 디자인 토큰 문서화
---

# design-md · Stitch-spec DESIGN.md generator

## 0. Core Principles

This skill follows the **Google Labs [`@google/design.md`](https://github.com/google-labs-code/design.md) alpha spec** verbatim.

The generated `DESIGN.md` has two layers:

| Layer | Format | Purpose |
|---|---|---|
| **YAML Frontmatter** | YAML wrapped in `---` | Machine-readable (Stitch, linters, automated exports) |
| **Markdown Body** | Eight `##` h2 sections | Human-readable (design intent, usage guidance) |

**Must-haves:**
- Section order is fixed: Overview → Colors → Typography → Layout → Elevation & Depth → Shapes → Components → Do's and Don'ts
- Token reference syntax is `{colors.primary}`, `{typography.h1}`, `{spacing.4}` (curly braces + dot notation)
- Colors are `#` + hex (sRGB); dimensions carry `px|rem|em` units
- Primary color **must** be defined
- Optional sections can be omitted, but when present the order is mandatory

---

## 1. Workflow

When invoked, execute the five phases **in order**.

### Phase 1 · Project Discovery

Scan these patterns in parallel:

```bash
# Design-token source candidates
src/design-system/**/*.{ts,js,json}
src/theme/**/*.{ts,js}
src/**/tokens*.{ts,js,json}
tailwind.config.{js,ts,cjs,mjs}
src/**/design-tokens.*
tokens.json
tokens-studio.json
src/**/variables.css
src/**/theme.{ts,js}

# Component location candidates
src/design-system/ui/**/*.{tsx,ts}
src/components/ui/**/*.{tsx,ts}
src/components/**/*.{tsx,ts}
packages/ui/**/*.{tsx,ts}

# Existing design docs
DESIGN.md
docs/design.md
docs/DESIGN-SYSTEM.md
STYLEGUIDE.md
```

**Classify what you find:**

1. **Single-source token file** → parse directly (e.g. `source.js`, `tokens.ts`, `theme.ts`)
2. **Tailwind config** → parse `theme.extend`
3. **CSS variables** → grep `:root { --color-* }`
4. **MUI theme** → parse `createTheme({ palette, typography })`
5. **Nothing found** → enter interview mode (Phase 2b)

### Phase 2a · Automatic Token Extraction

From the discovered source, extract:

| Category | Minimum required | Collect if present |
|---|---|---|
| **colors** | primary | secondary, accent, success, warning, error, info, text/bg/border |
| **typography** | h1, body | h2–h6, caption, display, numeric |
| **spacing** | base scale (4/8/16px etc.) | full scale |
| **rounded** | sm/md/lg | full, xl+ |
| **components** | button, input, card | project-specific components |

### Phase 2b · Interview (when tokens are insufficient)

Use `AskUserQuestion` with up to 4 **grouped** questions:

1. **Brand Personality**: what tone? (professional / playful / minimal / editorial / brutalist / …)
2. **Primary Color**: what's the primary brand color hex?
3. **Target Users**: who uses this, and in what context?
4. **Typography Preference**: any specific typography requirements? (particular fonts, separate Latin/CJK/numeric stacks, weight constraints)

### Phase 3 · Generate YAML Frontmatter

Follow this **exact order and field set**:

```yaml
---
version: alpha
name: <product-name>
description: >
  <2–4 lines. Product identity, target user, core design language.>

colors:
  # Brand
  primary: "#xxxxxx"
  primary-dark: "#xxxxxx"
  primary-light: "#xxxxxx"
  secondary: "#xxxxxx"
  accent: "#xxxxxx"

  # Status (4 required)
  success: "#xxxxxx"
  warning: "#xxxxxx"
  error: "#xxxxxx"
  info: "#xxxxxx"

  # Text (primary/secondary/muted/disabled/inverse — at least 5)
  text-primary: "#xxxxxx"
  text-secondary: "#xxxxxx"
  text-muted: "#xxxxxx"
  text-disabled: "#xxxxxx"
  text-inverse: "#xxxxxx"

  # Background (primary/secondary/hover/selected — at least 4)
  bg-primary: "#xxxxxx"
  bg-secondary: "#xxxxxx"
  bg-hover: "#xxxxxx"

  # Border
  border: "#xxxxxx"
  border-focus: "#xxxxxx"

typography:
  # At minimum base + h1–h3; prefer 9–15 levels
  caption:
    fontFamily: <Font>
    fontSize: 1.2rem
    fontWeight: 400
    lineHeight: 1.4
  body:
    fontFamily: <Font>
    fontSize: 1.4rem
    fontWeight: 400
    lineHeight: 1.5
  h1:
    fontFamily: <DisplayFont>
    fontSize: 3.2rem
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: -0.02em
  # … h2, h3, numeric variants

rounded:
  none: 0
  sm: 2px
  DEFAULT: 4px
  md: 6px
  lg: 8px
  full: 9999px

spacing:
  "0": 0
  "1": 4px
  "2": 8px
  "3": 12px
  "4": 16px
  "6": 24px
  "8": 32px

components:
  # One entry per discovered component
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.text-inverse}"
    typography: "{typography.body}"
    rounded: "{rounded.md}"
    height: 40px
    padding: 0 16px
  button-secondary:
    backgroundColor: "{colors.bg-primary}"
    textColor: "{colors.primary}"
    borderColor: "{colors.primary}"
    rounded: "{rounded.md}"
  input:
    backgroundColor: "{colors.bg-primary}"
    borderColor: "{colors.border}"
    rounded: "{rounded.DEFAULT}"
    height: 40px
  card:
    backgroundColor: "{colors.bg-primary}"
    rounded: "{rounded.lg}"
    padding: 20px
---
```

**Token-reference rules:**
- When pointing one token at another, always use `"{category.name}"` form
- Quote as strings (YAML-parser compatibility)
- Max one hop for chained references (never token → token → token)

### Phase 4 · Write the 8-Section Markdown Body

**Required contents per section:**

#### ① Overview

- Brand Personality table (Tone / Density / Color / Voice / Target — 4–5 axes)
- Emotional Response (3–5 items the user should feel)
- Core Design Principles (5 or fewer)
- **Anti-Patterns** (What this is NOT) — what we deliberately avoid

#### ② Colors

- Palette Hierarchy diagram (how many tokens per category)
- Emphasize primary's single-source-of-truth role
- Status-color usage rules (when to use which)
- **WCAG accessibility contrast table** (at least 3–5 combinations)
- Text / Background / Border token tables

#### ③ Typography

- Font-stack rationale (why this font, when to use it)
- Fallback chain
- Full scale table (Token / Size / Line-Height / Weight / Use case)
- Numeric Variant section (when tabular-nums are required)
- Usage Heuristic — 5–8 ✅/❌ rules

#### ④ Layout

- Breakpoints table
- Container strategy (max-width, gutter)
- Full Spacing Scale
- Spacing Application Heuristic table (recommended gap per situation)
- Grid System (Flexbox vs CSS Grid decision criteria)
- Component Dimensions table (height size matrix)
- Z-Index semantic layers

#### ⑤ Elevation & Depth

- Philosophy statement (flat vs material, subtle vs dramatic)
- Full Shadow Tokens table
- **Status Glow Shadow** (if any)
- Elevation Hierarchy diagram (Z-elev 0–5)
- Motion Tokens (duration, easing)
- Opacity Scale

#### ⑥ Shapes

- Full Corner Radius Scale table
- Shape Language statement (4px default? 8px? 0?)
- Border width rules
- **Shape-to-Component Mapping table** (which component uses which radius)

#### ⑦ Components

For each major component:

- File path
- Primary API (props table)
- Usage example (real code — never fabricated)
- Token references (`{components.xxx}`)
- Variants / Presets table
- Design-intent explanation

Order: Button → Input/Field → Select/Combobox → Checkbox → Radio → Modal → Card → Tag → Table → Navigation → Custom

#### ⑧ Do's and Don'ts

- ✅ Do: 7–12 items (each = *principle + code example*)
- ❌ Don't: 7–12 items (each = *anti-pattern + correct alternative*)

Category coverage:
- Token references
- Units (px vs rem)
- Primary-use constraints
- Accessibility (focus ring, contrast)
- Z-Index semantics
- Deprecated usage bans

### Phase 5 · Appendix & Validation

**Include in the Appendix:**
1. Token cheatsheet (CSS variables / Tailwind class / framework theme)
2. Import cheatsheet (import paths for major components)
3. Contribution guide (workflow for adding new tokens / components)
4. Linting commands:
   ```bash
   npx @google/design.md lint DESIGN.md
   npx @google/design.md export --format tailwind DESIGN.md
   npx @google/design.md diff DESIGN.md DESIGN-v2.md
   ```

**Self-validation checklist (must pass before emitting):**

- [ ] YAML frontmatter opens and closes with `---`
- [ ] `name`, `colors.primary`, and `typography` are defined
- [ ] Eight sections in correct order
- [ ] No duplicate sections
- [ ] Every `{...}` token reference points at an existing token
- [ ] Hex values use `#` + 6 digits
- [ ] Dimensions include a unit (px/rem/em) or are exactly 0
- [ ] Optional h1 title; `##` is the main section level
- [ ] Primary-on-body contrast ≥ WCAG AA

---

## 2. Output Path

Default: `<project-root>/DESIGN.md` or `<project-root>/src/design-system/DESIGN.md`

**Decision rules:**
1. If `src/design-system/` already exists → write inside it
2. Otherwise → write to project root
3. If the user passes an explicit path → use that path

---

## 3. Language Policy

- Detect the project's primary language from `CLAUDE.md` or `README`
- Korean project (e.g. CLAUDE.md contains "always use korean") → **write in Korean**
- English project → **write in English**
- YAML frontmatter keys are **always English snake-case**

---

## 4. Invocation Examples

### 4.1 Default
```
/design-md
```
Scan the current directory → generate `DESIGN.md`.

### 4.2 Explicit output path
```
/design-md --output src/design-system/DESIGN.md
```

### 4.3 Update existing file
```
/design-md --update
```
Preserve existing `DESIGN.md` sections, re-extract tokens and components, and merge.

### 4.4 Skeleton only
```
/design-md --skeleton
```
Skip the interview and generate a placeholder-filled empty template.

---

## 5. Anti-Patterns (what this skill must NOT do)

- ❌ Invent components that don't exist and add them to the Components section
- ❌ Fabricate a "recommended palette" instead of extracting real project tokens
- ❌ Reorder sections arbitrarily
- ❌ Use `{colors.xxx}` token references that point at undefined tokens
- ❌ Write English prose for a Korean-language project
- ❌ Overwrite an existing `DESIGN.md` without backup (confirm before overwriting unless in update mode)

---

## 6. References

- Spec repo: https://github.com/google-labs-code/design.md
- Spec doc: https://github.com/google-labs-code/design.md/blob/main/docs/spec.md
- Stitch official: https://stitch.withgoogle.com/docs/design-md/
- Blog: https://blog.google/innovation-and-ai/models-and-research/google-labs/stitch-design-md/

---

## 7. Completion Report Format

On completion, report back in this format:

```markdown
## ✅ DESIGN.md generated

**Path:** <path>
**Size:** <NNkb, NN lines>
**Spec:** Stitch design.md alpha

### 📊 Extraction results
- Colors: <n> tokens (primary/status/text/bg/border/chart)
- Typography: <n> levels
- Spacing: <n> steps
- Components: <n> components

### ✔️ Self-validation passed
- [x] Frontmatter `---` valid
- [x] Required tokens present (primary)
- [x] 8-section order respected
- [x] Token-reference integrity
- [x] WCAG AA contrast

### 🔍 Next steps
\`\`\`bash
npx @google/design.md lint <path>
\`\`\`
```
