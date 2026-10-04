---
name: ds-code-audit
description: |
  DS Code Auditor — finds ALL design system violations in Swift code: inline patterns that should be reusable components, hardcoded values, missing tokens, duplicate UI patterns, non-extracted molecules. Use this skill ALWAYS when checking code for DS compliance, before any Figma sync, or after writing new screens/components. Trigger: "ds audit", "дс аудит", "проверь дизайн систему", "design system check", "найди дубли", "inline patterns", "что не в компонентах", "code consistency", "полная проверка кода".
---

# DS Code Auditor

You are auditing the Hexbound iOS codebase for design system compliance and component extraction opportunities. Your goal: **every visual pattern in the codebase should either be a reusable component or use one**.

## Before You Start

**Read these files first** — they are the ground truth:
1. `Hexbound/Hexbound/Theme/DarkFantasyTheme.swift` — all color/font tokens
2. `Hexbound/Hexbound/Theme/LayoutConstants.swift` — all spacing/radius/icon tokens
3. `Hexbound/Hexbound/Theme/ButtonStyles.swift` — all button styles
4. `Hexbound/Hexbound/Theme/CardStyles.swift` — card modifiers + dividers
5. `Hexbound/Hexbound/Theme/OrnamentalStyles.swift` — ornamental components
6. `CLAUDE.md` — project rules (root)
7. `Hexbound/CLAUDE.md` — iOS-specific rules

## Phase 1: Automated Token Scan (`rg`-based)

Run ALL of these. Zero tolerance for violations.

```bash
cd "$(git rev-parse --show-toplevel)"

echo "=== 1. Invented font tokens ==="
rg -n 'DarkFantasyTheme\.(largeTitleFont|titleFont|bodyFont|bodyBoldFont|headlineFont|subtitleFont|captionFont)' Hexbound -g '*.swift' || echo "CLEAN"

echo "=== 2. Invented spacing tokens ==="
rg -n 'LayoutConstants\.(spacing|padding|margin)[A-Z]' Hexbound -g '*.swift' || echo "CLEAN"

echo "=== 3. Hardcoded hex colors in Views ==="
rg -n 'Color\(hex:' Hexbound/Hexbound/Views -g '*.swift' || echo "CLEAN"

echo "=== 4. Hardcoded system fonts ==="
rg -n '\.font\(\.system\(size:' Hexbound/Hexbound/Views -g '*.swift' | rg -v 'design: .monospaced|design: .rounded|// emoji|// keep|// SF Symbol|pillIconSize|textCard|iconSize' || echo "CLEAN"

echo "=== 5. Raw Color.xxx in Views ==="
rg -n 'Color\.(red|orange|green|blue|gray)' Hexbound/Hexbound/Views -g '*.swift' | rg -v 'DarkFantasyTheme|// keep|SurfaceLighting|OrnamentalStyles' || echo "CLEAN"

echo "=== 6. SF Symbol currency icons ==="
rg -n 'dollarsign\.circle|diamond\.fill.*currency' Hexbound/Hexbound/Views -g '*.swift' || echo "CLEAN"

echo "=== 7. Hardcoded cornerRadius literals ==="
rg -n 'RoundedRectangle\(cornerRadius: [0-9]' Hexbound/Hexbound/Views -g '*.swift' | rg -v 'cornerRadius: 0|cornerRadius: 1\b' || echo "CLEAN"

echo "=== 8. Hardcoded spacing in VStack/HStack ==="
rg -n 'VStack\(spacing: [0-9]|HStack\(spacing: [0-9]' Hexbound/Hexbound/Views -g '*.swift' | rg -v 'spacing: 0|LayoutConstants|// keep' || echo "CLEAN"

echo "=== 9. Hardcoded padding values ==="
rg -n '\.padding\([^)]*[0-9]+\)' Hexbound/Hexbound/Views -g '*.swift' | rg -v 'LayoutConstants|// keep|\.padding\(0\)|\.padding\(\)' || echo "CLEAN"

echo "=== 10. Raw Divider() usage ==="
rg -n 'Divider\(\)' Hexbound/Hexbound/Views -g '*.swift' | rg -v 'GoldDivider|OrnamentalDivider|EtchedGroove|// keep|statDivider|SwiftUI menu' || echo "CLEAN"

echo "=== 11. Rectangle as divider ==="
rg -n 'Rectangle\(\)\.fill.*frame\(height: 1\)' Hexbound/Hexbound/Views -g '*.swift' | rg -v 'EtchedGroove|// keep' || echo "CLEAN"

echo "=== 12. Button without .buttonStyle ==="
rg -n 'Button\(' Hexbound/Hexbound/Views -g '*.swift' -l | while read f; do
  buttons=$(rg -c 'Button\(' "$f" || true)
  styles=$(rg -c '\.buttonStyle\(' "$f" || true)
  buttons=${buttons:-0}
  styles=${styles:-0}
  if [ "$buttons" -gt "$styles" ]; then
    echo "$f: $buttons Button() vs $styles .buttonStyle()"
  fi
done || echo "CLEAN"

echo "=== 13. Hardcoded frame dimensions ==="
rg -n '\.frame\(width: [0-9]+, height: [0-9]+\)' Hexbound/Hexbound/Views -g '*.swift' | rg -v 'LayoutConstants|// keep|// layout|Dev/' || echo "CLEAN"

echo "=== 14. Merge conflict markers ==="
rg -n '^(<<<<<<<|=======$|>>>>>>>)' . -g '*.swift' -g '*.ts' -g '*.prisma' -g '!node_modules/**' -g '!.git/**' || echo "CLEAN"
```

**Every finding must be either FIXED or marked with `// keep` comment + justification.**

## Phase 2: Duplicate Pattern Detection

Search for **repeated inline UI patterns** that appear 2+ times and should be extracted into reusable components.

### What to look for:

1. **Repeated badge/pill patterns** — same Text + padding + background + cornerRadius appearing in multiple files
2. **Repeated card layouts** — same VStack/HStack structure with identical modifiers in 2+ places
3. **Repeated button patterns** — custom Button labels not using ButtonStyles
4. **Repeated overlay/sheet chrome** — same modal wrapper structure duplicated
5. **Repeated status indicators** — same conditional coloring/icon logic in multiple views

### How to find them:

```bash
# Find identical padding+background+cornerRadius combos (badge pattern)
rg -n '\.padding.*\.background.*\.clipShape|\.padding.*\.background.*RoundedRectangle' Hexbound/Hexbound/Views -g '*.swift' | rg -v 'Components/'

# Find repeated Text+font+foregroundStyle+padding combos
rg -n '\.font\(DarkFantasyTheme\.caption\.bold\(\)\)' Hexbound/Hexbound/Views -g '*.swift' | rg -v 'Components/'

# Find views with inline gradient backgrounds (should be tokens or components)
rg -n 'LinearGradient\(' Hexbound/Hexbound/Views -g '*.swift' | rg -v 'Theme/|Components/' | head -30
```

### Classification:

For each repeated pattern, classify:
- **EXTRACT** — appears 3+ times, identical structure → create reusable component
- **PARAMETERIZE** — appears 2+ times, similar but not identical → extract with parameters
- **KEEP INLINE** — appears 1-2 times, context-specific → leave but document why
- **ALREADY EXISTS** — a component exists but isn't being used → replace inline with component

## Phase 3: Component Inventory vs. Usage

Cross-reference all files in `Views/Components/` with actual usage:

```bash
# For each component, check if it's actually used
for f in Hexbound/Hexbound/Views/Components/*.swift; do
  name=$(basename "$f" .swift)
  count=$(rg -l "$name" Hexbound/Hexbound/Views -g '*.swift' | rg -v "$f" | wc -l)
  echo "$name: used in $count files"
done
```

Flag:
- **Orphaned components** — exist but used 0-1 times (consider removing or documenting why kept)
- **Missing components** — inline patterns used 3+ times but no component extracted
- **Underused components** — component exists but inline duplicates also exist (not using the component)

## Phase 4: Token Coverage

Check if ALL tokens from Theme files are actually used in Views:

```bash
# Extract all static let names from DarkFantasyTheme
rg 'static let' Hexbound/Hexbound/Theme/DarkFantasyTheme.swift | sed 's/.*static let \([a-zA-Z]*\).*/\1/' | while read token; do
  count=$(rg -l "DarkFantasyTheme\\.$token" Hexbound/Hexbound/Views -g '*.swift' | wc -l)
  if [ "$count" -eq 0 ]; then
    echo "UNUSED TOKEN: DarkFantasyTheme.$token"
  fi
done
```

Flag:
- **Unused tokens** — defined but never referenced (dead code or missed usage)
- **Missing tokens** — hardcoded values that should have tokens

## Output Format

Produce a structured report:

```
## DS Code Audit Report — [date]

### Token Violations: [count]
[list each violation with file:line and fix]

### Duplicate Patterns: [count]
[for each pattern: what it is, where it appears, recommended action]

### Missing Components: [count]
[patterns that should be extracted]

### Orphaned Components: [count]
[components with 0-1 usage]

### Unused Tokens: [count]
[tokens defined but never used]

### CDO Verdict: CLEAN / [N] ISSUES
```

## Legitimate Exceptions (DO NOT flag)

- `Color.white` / `Color.black` with `.opacity()` inside `SurfaceLightingOverlay` and `OrnamentalStyles`
- `.font(.system(size:))` for SF Symbol icons with `// SF Symbol` or `// keep` comment
- `spacing: 0` / `padding(0)` — zero values are fine
- `cornerRadius: 0` or `cornerRadius: 1` — micro values
- Files in `Dev/` directory — development/debug views exempt
- SwiftUI `Divider()` inside `.contextMenu` — Apple API requirement
- `Color.clear` — transparent is not a design token
- Non-square `.frame()` for layout containers (scrollviews, sheets, etc.)
