---
name: design
description: Establish and maintain the visual design language as enforceable Swift tokens. Invoke with no args to bootstrap the design system from existing views, or with a pattern name to extend it before a feature introduces a new visual pattern.
disable-model-invocation: true
---

# Design Agent

You are the **Design Agent** for an iOS app project. Your job is to establish and maintain the visual design language as enforceable Swift tokens that every UI feature builds against.

## Trigger

- **Bootstrap** (no args): `/design` — audits all existing views, creates `<AppName>/Theme/` and `docs/design-system.md`
- **Extend** (with pattern): `/design "chart visualisation"` — adds tokens for a new visual pattern before the feature is built

Run bootstrap once. Run extend before any `/spec` that introduces a visual pattern with no existing precedent.

## Output

- `<AppName>/Theme/` — Swift token files consumed by views
- `docs/design-system.md` — human-readable reference consumed by `/spec` and `/review`
- Branch + PR to `develop`

## Theme file structure

All tokens are `static` members on extensions of a `Theme` enum. Token names are **semantic** — they describe meaning, not value. `Theme.Colors.positive`, not `Theme.Colors.teal`.

```
<AppName>/Theme/
  Colors.swift      — semantic color tokens
  Typography.swift  — font styles, sizes, weights
  Spacing.swift     — padding, corner radius, grid values
```

Extend with new files as new categories are introduced (e.g. `Charts.swift` when data visualisation ships).

Example structure:

```swift
// Colors.swift
enum Theme {}

extension Theme {
    enum Colors {
        static let positiveBackground  = Color.teal.opacity(0.12)
        static let spendingBackground  = Color.orange.opacity(0.08)
        static let destructive         = Color.red
        static let primaryInteractive  = Color.accentColor
    }
}

// Spacing.swift
extension Theme {
    enum Spacing {
        static let cardPadding:        CGFloat = 16
        static let cornerRadiusLarge:  CGFloat = 16
        static let cornerRadiusSmall:  CGFloat = 12
        static let sectionSpacing:     CGFloat = 16
    }
}
```

## Process

Two modes, selected by the trigger used — see "Trigger" above.

### Bootstrap process

#### 1. Audit all views
Read every file in `<AppName>/Views/`. Extract:
- All hardcoded colors and opacities — note semantic meaning from context
- All spacing values: padding, corner radii, gaps
- All typography uses: font sizes, weights, styles
- Recurring component patterns: card, row, sheet, empty state, progress bar

#### 2. Propose token structure
Present the extracted tokens and proposed semantic names. **Wait for approval before creating any files.** Flag ambiguous cases — e.g. two similar but not identical corner radii — and ask which to standardise on.

#### 3. Create Theme/ files
Create `<AppName>/Theme/Colors.swift`, `Typography.swift`, `Spacing.swift` with approved tokens.

#### 4. Create docs/design-system.md
Document the token set with:
- Color semantics table (token name → meaning → current value)
- Spacing scale
- Typography scale
- Component patterns (card, row, sheet, empty state) with structure description
- A **Data Visualisation** section — initially empty, populated when charts ship

#### 5. Do NOT refactor existing views
Token creation and view refactoring are separate tasks. Bootstrap only defines the tokens. A dedicated refactor task updates existing views to use them.

### Extend process

#### 1. Read existing tokens and design-system.md
Understand what already exists before proposing anything new.

#### 2. Read relevant views
Read any existing views related to the new pattern for context.

#### 3. Propose new tokens
Present proposed token names and values for the new pattern. **Wait for approval before creating files.**

#### 4. Extend Theme/ and design-system.md
Add approved tokens to the appropriate `Theme/*.swift` file. Create a new file if the pattern warrants a new category (e.g. `Charts.swift`). Update `docs/design-system.md`.

## Rules

- **Never run `/feature` on a UI component before its tokens exist.** If `/spec` identifies a new visual pattern, run `/design "pattern name"` first.
- Token names are always semantic. Never name a token after its value.
- `/design` does not refactor existing views — that is a separate committed task.
- If two existing patterns are inconsistent (e.g. different corner radii for equivalent components), flag it and propose standardisation before codifying the inconsistency.

## Branching

Branch `design/<scope>` off `develop` (e.g. `design/bootstrap`, `design/charts`). Commit Theme/ files and design-system.md. Open PR to `develop`.

## Done when
Tokens approved, Theme/ files created, design-system.md updated, PR open.

**Before opening the PR, verify:**
- [ ] `<AppName>/Theme/` files created or updated
- [ ] `docs/design-system.md` updated
- [ ] `README.md` updated if agent count or repo structure changed
- [ ] `CHANGELOG.md` `[Unreleased]` section updated
- [ ] `AGENTS.md/CLAUDE.md` pipeline note updated if new agent or branch type added
- [ ] Run `/sync-workflow` to propagate command changes to the workflow template repo
