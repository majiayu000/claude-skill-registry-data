---
name: ds-extract-component
description: |
  DS Extract Component — extracts an inline UI pattern from Swift code into a reusable component + creates matching Figma DS component. Full pipeline: identify pattern → extract Swift struct → add to pbxproj → create Figma component with tokens → update all call sites. Use this skill when ds-code-audit finds duplicate patterns, when you see the same UI repeated 2+ times, or when building a new molecule/atom. Trigger: "extract component", "вынеси в компонент", "сделай переиспользуемым", "make reusable", "ds extract", "создай компонент", "новый компонент DS", "refactor to component", "дубликат UI".
---

# DS Extract Component

You extract inline UI patterns from Hexbound Swift code into proper reusable components and create matching Figma DS component sets.

## Prerequisites

1. Read `CLAUDE.md` (root) — especially Xcode Project File section and Figma DS rules
2. Read `Hexbound/CLAUDE.md` — iOS-specific rules
3. Read the Theme files to know available tokens:
   - `DarkFantasyTheme.swift` — colors, fonts
   - `LayoutConstants.swift` — spacing, radius, icons
   - `ButtonStyles.swift` — button styles
   - `CardStyles.swift` — card modifiers
   - `OrnamentalStyles.swift` — ornamental overlays

## Step 1: Identify the Pattern

Before extracting, answer these questions:

1. **Where does this pattern appear?** List all files + line numbers
2. **What varies between instances?** (text, color, icon, size, action)
3. **What stays constant?** (layout, spacing, font, background shape)
4. **Is there an existing component it could extend?** Check `Views/Components/` first
5. **What should it be called?** Follow naming convention: `{Thing}{Role}View.swift` or `{Thing}{Role}.swift`

## Step 2: Design the Component API

Design the Swift struct interface:

```swift
// Template:
struct ComponentName: View {
    // Required parameters (what varies)
    let title: String
    let color: Color

    // Optional parameters (with defaults)
    var size: Size = .standard
    var onTap: (() -> Void)? = nil

    // Enum for variants (if applicable)
    enum Size { case compact, standard, large }

    var body: some View {
        // ALL values from design system tokens:
        // - Colors: DarkFantasyTheme.xxx
        // - Fonts: DarkFantasyTheme.xxx
        // - Spacing: LayoutConstants.xxx
        // - Radius: LayoutConstants.xxx
        // - Buttons: .buttonStyle(.xxx)
    }
}
```

### Rules for the component:

- **ZERO hardcoded values** — every color, font, spacing, radius from tokens
- **Minimum font 11px** (badge) or 12px (caption) — never smaller
- If it has a tap action → wrap in `Button` with `.buttonStyle(.plain)` or appropriate style
- If it shows rarity → accept `ItemRarity` parameter, use `DarkFantasyTheme.rarityColor(for:)`
- If it shows class → accept `CharacterClass` parameter, use class color tokens
- If ornamental → use `.panelCard()` / `.rarityCard()` / appropriate card modifier

## Step 3: Create the Swift File

1. **Write the component** to `Hexbound/Hexbound/Views/Components/ComponentName.swift`
2. **Add to pbxproj** — generate random 24-char hex IDs (NOT sequential):
   ```bash
   openssl rand -hex 12 | tr 'a-f' 'A-F'  # For fileRef ID
   openssl rand -hex 12 | tr 'a-f' 'A-F'  # For buildFile ID
   ```
   Add entries to ALL 4 sections: PBXBuildFile, PBXFileReference, PBXGroup (Components), PBXSourcesBuildPhase

3. **Verify pbxproj** — no duplicate IDs, entries sorted alphabetically

## Step 4: Replace All Call Sites

For every instance of the inline pattern:

1. `rg -n` to find ALL occurrences
2. Replace each with the new component
3. Verify the parameters match the original inline code
4. Run CDO scan to confirm no violations introduced

**CRITICAL:** After refactoring, search ALL callers with `rg` to make sure nothing broke. Common mistakes:
- Missing import
- Parameter name mismatch
- Optional vs required parameter
- Closure signature change

## Step 5: Create Figma DS Component

Use `figma-use` skill with the current verified DS file key. Historical default: `uDjXIz7CdJxcEOI5jCBcjY`; verify before writing.

### Determine the correct Figma page:

| Component type | Figma page |
|---|---|
| Button variant | Components / Buttons |
| Card/panel | Components / Cards |
| Badge/pill/tag | Components / Badges & Pills |
| Progress indicator | Components / Progress Bars |
| Loading state | Components / Loading |
| Navigation element | Components / Navigation |
| Input field | Components / Input |
| Skeleton/placeholder | Components / Skeleton |
| Hero/character display | Components / Hero & Character |
| PvP/arena element | Components / Arena & PvP |
| Dungeon/quest element | Components / Dungeon & Progression |
| Social/messaging | Components / Social & Messaging |
| Toast/banner/alert | Components / Toast & Banners |
| Modal/sheet/overlay | Components / Modals & Sheets |
| Currency display | Components / Currency Display |

### Build the Figma component:

1. **Create component variants** matching Swift's enum/parameter variations
2. **Bind ALL colors** to Color collection variables
3. **Bind ALL spacing** to Spacing collection variables
4. **Apply text styles** to ALL text nodes
5. **Apply effect styles** to root node (Shadow/Card or Shadow/Modal)
6. **Use existing sub-components** (Button instances, Divider instances, etc.)

### Figma quality checklist (MANDATORY):

- [ ] Every TEXT node has `textStyleId` set (linked to Heading/* or Body/*)
- [ ] Every colored fill/stroke has `boundVariables.fills` or `boundVariables.strokes`
- [ ] Every auto-layout gap has `boundVariables.itemSpacing`
- [ ] Every padding has `boundVariables.paddingTop/Right/Bottom/Left`
- [ ] Every cornerRadius has `boundVariables.topLeftRadius` (etc.)
- [ ] Root component has effect style applied
- [ ] No FRAME nodes pretending to be buttons — use Button instances
- [ ] No RECTANGLE nodes pretending to be dividers — use Divider instances
- [ ] Component set uses `combineAsVariants` with clear property names

## Step 6: Update Documentation

1. **Update `CLAUDE.md`** — if component count changed, update the Figma DS stats line
2. **Update Figma page table** in CLAUDE.md if new component added to existing page
3. **Update `docs/07_ui_ux/SCREEN_INVENTORY.md`** if new component affects screen inventory

## Step 7: Verify

Run full CDO scan:
```bash
# Token violations
rg -n 'DarkFantasyTheme\.(largeTitleFont|titleFont|bodyFont)' Hexbound -g '*.swift'
rg -n 'LayoutConstants\.(spacing|padding|margin)[A-Z]' Hexbound -g '*.swift'

# Component actually used
rg -n 'ComponentName' Hexbound/Hexbound/Views -g '*.swift' | wc -l

# pbxproj valid
rg 'ComponentName' Hexbound/Hexbound.xcodeproj/project.pbxproj | wc -l  # Should be 4
```

Take a Figma screenshot of the new component to visually verify.

## Example: Extracting "Class Tag" Pattern

**Before (inline, repeated 3 times):**
```swift
Text(opponent.characterClass.displayName.uppercased())
    .font(DarkFantasyTheme.caption.bold())
    .foregroundStyle(classColor)
    .padding(.horizontal, LayoutConstants.spaceSM)
    .padding(.vertical, LayoutConstants.space2XS)
    .background(
        RoundedRectangle(cornerRadius: LayoutConstants.radiusXS)
            .fill(classColor.opacity(0.12))
            .overlay(
                RoundedRectangle(cornerRadius: LayoutConstants.radiusXS)
                    .stroke(classColor.opacity(0.25), lineWidth: 0.5)
            )
    )
```

**After (extracted component):**
```swift
struct ClassTagView: View {
    let characterClass: CharacterClass

    var body: some View {
        let color = DarkFantasyTheme.classColor(for: characterClass)
        Text(characterClass.displayName.uppercased())
            .font(DarkFantasyTheme.caption.bold())
            .foregroundStyle(color)
            .padding(.horizontal, LayoutConstants.spaceSM)
            .padding(.vertical, LayoutConstants.space2XS)
            .background(
                RoundedRectangle(cornerRadius: LayoutConstants.radiusXS)
                    .fill(color.opacity(0.12))
                    .overlay(
                        RoundedRectangle(cornerRadius: LayoutConstants.radiusXS)
                            .stroke(color.opacity(0.25), lineWidth: 0.5)
                    )
            )
    }
}
```

**Call sites become:** `ClassTagView(characterClass: opponent.characterClass)`

**Figma:** Component Set "Class Tag" on Badges & Pills page, 4 variants (Warrior/Rogue/Mage/Tank), all fills bound to class/* color variables.
