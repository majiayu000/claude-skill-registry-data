---
name: ui-astroon
description: "UrhoX UI Design — Astroon Cosmic Cartoon Style. Use when users need to (1) 创建宇宙/太空/星际风格的游戏 UI, (2) 使用 Astroon 暗色渐变霓虹主题, (3) cosmic cartoon / space / neon / gradient UI, (4) 用户提到 Astroon 风格或宇宙卡通主题。"
---

# UrhoX UI Design — Astroon Cosmic Cartoon Style

> **Target reader: AI Agent.** When the user asks to "generate UI", "create an interface", "make a button/popup/card" in Astroon style, follow this design spec and code templates to produce UrhoX Lua UI code.

## Trigger

Activate this skill when the user request mentions:
- Astroon style, cosmic cartoon theme, space UI, cosmic gradient UI
- Creating any UI component in the cosmic/space/neon/gradient game style

## Design DNA — 8 Rules

**Astroon** is a dark, cosmic-themed game UI style with playful gradients and glowing accents. Every component should feel **cosmic, glowing, and game-ready**.

1. **Cosmic Gradient Background** — Always use the cosmic gradient (`#1A1140 -> #2D1B69`) for page backgrounds. Never use solid flat fill.
2. **Pill Buttons + Glow** — All buttons use **gradient fill + pill radius (9999) + color-matched outer glow shadow**. No borders on buttons.
3. **Token-based Corner System** — Use `sm 6`, `md 10`, `lg 16`, `xl 20`, and `pill 9999` by component role. Not one size everywhere.
4. **Gold = Primary CTA** — One gold button per screen max. Green for confirm, blue for secondary, red for danger.
5. **3-Level Text Hierarchy** — `{255,255,255,255}` for headings, `{255,255,255,170}` for body, `{255,255,255,85}` for muted/placeholder.
6. **Inter Everywhere** — Single typeface `"sans"` (Inter) for all UI text.
7. **Layered Surfaces** — Base panels use `surface` (`{42,31,94}`), elevated panels use `surfaceHover` (`{61,42,138}`), with subtle white-alpha border and dark shadow separation.
8. **Rarity Color System** — Blue (rare) + Purple (epic) + Gold (legendary), each with gradient background + glow.

## Fonts Setup

Copy fonts and their xml configs from this skill's `fonts/` directory to your project's assets:
```
mkdir -p /workspace/assets/Fonts/
cp ./fonts/* /workspace/assets/Fonts/
```

Required fonts:
- `Inter-Regular.ttf` — body text (sans normal)
- `Inter-Bold.ttf` — bold text (sans bold)

## Workflow

1. **Fonts** — Ensure fonts are copied to project assets (see above)
2. **Widget API** — Read `urhox-libs/UI/Widgets/*.lua` source for props reference
3. **Token table** — Colors/spacing/radius/fonts see `references/theme-tokens.md`
4. **Layout rules** — See `ai-dev-kit/engine-docs/recipes/ui.md`

## Quick Reference

### Theme Initialization

```lua
local UI = require("urhox-libs/UI")

-- Cosmic soft glow shadow (shared by panels/overlays)
local COSMIC_SHADOW = {
  { x = 0, y = 0, blur = 15, color = {0, 0, 0, 51} },
}

-- Create Astroon theme
local AstroonTheme = UI.Theme.ExtendTheme(UI.Theme.defaultTheme, {
  fonts = {
    { family = "sans", weights = {
      normal = "Fonts/Inter-Regular.ttf",
      bold = "Fonts/Inter-Bold.ttf",
    }},
  },
  colors = {
    primary = {255, 213, 79, 255},            -- #FFD54F Gold
    primaryHover = {255, 224, 102, 255},       -- #FFE066
    primaryPressed = {240, 160, 48, 255},      -- #F0A030
    secondary = {74, 139, 245, 255},           -- #4A8BF5 Blue
    secondaryHover = {91, 156, 246, 255},      -- #5B9CF6
    secondaryPressed = {51, 102, 204, 255},    -- #3366CC
    background = {26, 17, 64, 255},            -- #1A1140 Deep cosmic
    surface = {42, 31, 94, 255},               -- #2A1F5E
    surfaceHover = {61, 42, 138, 255},         -- #3D2A8A
    text = {255, 255, 255, 255},               -- #FFFFFF
    textSecondary = {255, 255, 255, 170},      -- #FFFFFFAA
    textDisabled = {255, 255, 255, 64},        -- #FFFFFF40
    border = {255, 255, 255, 24},              -- #FFFFFF18 subtle white-alpha
    borderFocus = {74, 139, 245, 255},         -- #4A8BF5
    disabled = {61, 42, 138, 255},             -- #3D2A8A
    disabledText = {255, 255, 255, 85},        -- #FFFFFF55
    success = {46, 204, 113, 255},             -- #2ECC71
    successHover = {61, 216, 138, 255},        -- #3DD88A
    warning = {255, 217, 61, 255},             -- #FFD93D
    warningHover = {255, 224, 102, 255},       -- #FFE066
    error = {255, 71, 87, 255},                -- #FF4757
    errorHover = {255, 107, 122, 255},         -- #FF6B7A
    info = {61, 214, 232, 255},                -- #3DD6E8 Cyan
    overlay = {0, 0, 0, 180},                  -- #000000B4
  },
  radius = {
    sm = 6,
    md = 10,
    lg = 16,
    xl = 20,
    full = 9999,  -- Pill shape: auto-clamped by NanoVG
  },
  componentDefaults = {
    borderRadius = 10,    -- Cosmic rounded corners on all controls
    -- borderWidth and boxShadow are per-component (layout containers should not have them)
  },
  components = {
    Button = {
      borderRadius = 9999,                     -- Pill shape (engine clamps to height/2)
      height = 48,
      fontSize = 13.5,                         -- 18px design = 13.5pt
      fontWeight = "bold",                     -- Button text always bold
      glowShadow = {                           -- Per-variant colored glow (base from variant color)
        alpha = { default = 96, hover = 128 },
        blur = { default = 12, hover = 16 },
        offset = { default = {0, 4}, hover = {0, 4} },
        pressed = { color = {0, 0, 0, 64}, blur = 6, offset = {0, 2} },
      },
    },
    TextField = { borderWidth = 1.5, borderRadius = 6, bgColor = {26, 17, 64, 255} },  -- $background
    Checkbox = {
      borderRadius = 4, borderWidth = 1.5,
      checkedBgColor = {74, 139, 245, 255},             -- $secondary blue (NOT primary gold)
      checkedBorderColor = {74, 139, 245, 255},         -- $secondary blue
      checkmarkColor = {255, 255, 255, 255},             -- white
      hoverBorderColor = {74, 139, 245, 255},            -- $secondary blue
    },
    Toggle = {
      borderRadius = 9999, thumbSize = 22,
      thumbColor = {255, 255, 255, 85},                 -- #FFFFFF55 muted
      thumbCheckedColor = {255, 255, 255, 255},          -- white
      thumbHoverColor = {255, 255, 255, 170},            -- #FFFFFFAA
      trackBg = {61, 42, 138, 255},                      -- $surfaceHover (off-state track)
      trackHoverBorderColor = {74, 139, 245, 255},      -- $secondary
      trackCheckedBgColor = {46, 204, 113, 255},         -- $success green
      trackCheckedHoverBgColor = {61, 216, 138, 255},    -- $successHover
    },
    Slider = {
      height = 20, borderRadius = 9999, borderWidth = 0,
      thumbBorderWidth = 0, thumbBorderRadius = 9999,
      trackBgColor = {26, 17, 64, 255},                  -- $background deep cosmic
      trackFillGradient = { direction = "to-right", from = {61, 214, 232, 255}, to = {74, 139, 245, 255} },
      thumbColor = {255, 255, 255, 255},                   -- white
    },
    -- Panels & overlays: subtle border + cosmic shadow
    Card = { borderRadius = 16, boxShadow = COSMIC_SHADOW },
    Modal = {
      borderWidth = 1, boxShadow = COSMIC_SHADOW, borderRadius = 20,
      headerBorderWidth = 0,
      footerBorderWidth = 0,
      contentPadding = {16, 24, 16, 24},                   -- top=16 (below header), right/left=24, bottom=16
      contentGap = 16,
      footerPadding = {12, 24, 16, 24},                    -- top=12, right/left=24 (match content), bottom=16
    },
    Drawer = {
      borderWidth = 1.5, boxShadow = COSMIC_SHADOW, borderRadius = 20,
      contentPadding = {8, 6},                             -- top/bottom=8, left/right=6
      headerPadding = {14, 16},                            -- top=14, left/right=16
    },
    Menu = {
      variant = "outlined", borderWidth = 1, boxShadow = COSMIC_SHADOW, borderRadius = 10,
      itemHoverBgColor = {61, 42, 138, 255},             -- $surfaceHover
      itemHoverTextColor = {255, 255, 255, 255},          -- white (NOT primary gold)
      itemHoverInset = 0, itemHoverRadius = 0,
      itemHoverFontWeight = "bold",                        -- hover item 600→bold
      itemVerticalInset = 0,                               -- items flush to panel edges
    },
    Dropdown = {
      height = 35, borderWidth = 1, borderRadius = 6,
      triggerBgColor = {26, 17, 64, 255},                  -- $background
      arrowColor = {255, 255, 255, 85},                    -- $textMuted
      boxShadow = { { x = 0, y = 0, blur = 8, color = {0, 0, 0, 64} } },
      hoverBorderColor = {61, 214, 232, 255},              -- $accent cyan
      openBorderColor = {61, 214, 232, 255},               -- $accent cyan
      popupBorderColor = {48, 39, 83, 255},               -- #302753 dark purple
      itemHoverBgColor = {61, 42, 138, 255},
      itemHoverTextColor = {61, 214, 232, 255},           -- $accent cyan
      itemHoverInset = 0, itemHoverRadius = 0,
      itemSelectedTextColor = {61, 214, 232, 255},         -- $accent cyan (NOT gold)
      selectedFontWeight = "bold",                         -- selected item 600→bold
      itemVerticalInset = 0,                               -- items flush to popup edges
    },
    List = {
      borderWidth = 1.5, borderRadius = 10,
      itemHoverBgColor = {61, 42, 138, 255},
      itemSelectedBgColor = {61, 42, 138, 255},
      itemHoverTextColor = {61, 214, 232, 255},
      itemSelectedTextColor = {61, 214, 232, 255},
    },
    Table = {
      variant = "striped", borderWidth = 1.5, borderRadius = 10,
      headerFontWeight = "bold",                           -- header 700
      headerBgColor = {61, 42, 138, 255},                 -- $surfaceHover
      rowOddBgColor = {28, 19, 70, 255},                  -- #1C1346
      rowEvenBgColor = {38, 28, 81, 255},                  -- #261C51
      rowHoverBgColor = {74, 139, 245, 31},                -- subtle blue glow
    },
    Toast = {
      borderWidth = 1, boxShadow = COSMIC_SHADOW, borderRadius = 10,
      accentBarHeight = 0,
      accentBarWidth = 0,                                  -- no accent bar decoration
      showIcon = true,
    },
    Tooltip = {
      borderWidth = 1, boxShadow = COSMIC_SHADOW, borderRadius = 8,
      tooltipBgColor = {42, 31, 94, 255},                 -- $surface
      borderColor = {255, 255, 255, 24},                   -- #FFFFFF18 subtle white
    },
    Popover = { borderWidth = 1, boxShadow = COSMIC_SHADOW, borderRadius = 10 },
    Alert = { borderWidth = 1, borderRadius = 10, borderOpacity = 0.19 },
    ProgressBar = {
      height = 10, borderWidth = 0, borderRadius = 9999,
      fillGradient = { direction = "to-right", from = {61, 214, 232, 255}, to = {74, 139, 245, 255} },
    },
    Badge = { borderRadius = 9999, fontWeight = "bold", borderWidth = 0 },
    Chip = { borderRadius = 9999, fontWeight = "bold" },      -- 600 in .pen → maps to bold
    Tabs = {
      activeFontWeight = "bold",                           -- active tab 700/600→bold
      activeBorderColor = {61, 214, 232, 255},             -- $accent cyan (line indicator + pills border)
      activeTextColor = {255, 255, 255, 255},              -- white (all variants)
      activeBgColor = {61, 42, 138, 255},                  -- $surfaceHover (pills/enclosed active bg)
      inactiveTextColor = {255, 255, 255, 85},             -- $textMuted
      enclosedPadding = 3,
      tabGap = 3,
      variantBorderRadius = {
        pills = 9999,                                      -- pill shape
        enclosed = 6,                                      -- slightly rounded
      },
    },
    Accordion = {
      variant = "outlined", borderWidth = 1.5, borderRadius = 10,
      headerFontWeight = "bold",                           -- header 600→bold
      headerExpandedBgColor = {61, 42, 138, 255},          -- $surfaceHover
      contentBgColor = {26, 17, 64, 255},                  -- $background
      indicatorExpandedColor = {61, 214, 232, 255},        -- $accent cyan
    },
    Timeline = {
      dotColor = {61, 214, 232, 255},                      -- $accent cyan (all dots)
      lineColor = {61, 214, 232, 255},                     -- $accent cyan (connectors)
      hoverTitleColor = {61, 214, 232, 255},               -- $accent cyan (NOT primary gold)
      titleFontWeight = "bold",                            -- title 700
      titleSize = 12,                                      -- 16px = 12pt
    },
    Breadcrumb = {
      linkColor = {61, 214, 232, 255},                     -- $accent cyan
      hoverColor = {255, 255, 255, 255},                   -- $text white
      currentColor = {255, 255, 255, 170},                 -- $textSecondary
      separatorColor = {255, 255, 255, 85},                -- $textMuted
    },
    Stepper = {
      borderWidth = 1.5, borderRadius = 9999,             -- circle (engine clamps to size/2)
      fontWeight = "bold",                                 -- step numbers always bold
      activeBgColor = {100, 76, 194, 255},                 -- #644CC2 cosmic purple
    },
    Calendar = {
      borderRadius = 9999,                                 -- day cell = circle (engine clamps)
      navBtnBgColor = {82, 64, 150, 255},                  -- #524096 nav button permanent bg
      navBtnRadius = 6,                                    -- nav button rounded rect (NOT circle)
      primaryColor = {61, 214, 232, 255},                  -- $accent cyan (today button etc.)
      monthFontWeight = "bold",                            -- month title 700
      weekdayFontWeight = "bold",                          -- weekday labels 600→bold
      selectedFontWeight = "bold",                         -- selected day 700
      selectedBgColor = false,                              -- no fill (outlined mode)
      selectedBorderColor = {61, 214, 232, 255},           -- cyan border
      selectedBorderWidth = 2,
      selectedTextColor = {61, 214, 232, 255},             -- cyan text
      todayBorderColor = {61, 214, 232, 255},
      todayTextColor = {61, 214, 232, 255},
    },
    DatePicker = {
      borderRadius = 9999,                                 -- day cell = circle (engine clamps)
      popupBorderRadius = 16,                              -- popup container corners (NOT circle!)
      navBtnBgColor = {82, 64, 150, 255},                  -- #524096 nav button permanent bg
      navBtnRadius = 6,                                    -- nav button rounded rect (NOT circle)
      popupBgColor = {61, 42, 138, 255},                   -- $surfaceHover (elevated popup)
      fieldBgColor = {33, 21, 77, 255},                    -- #21154D field background
      fieldBorderColor = {63, 53, 109, 255},               -- #3F356D field idle border
      fieldFontSize = 13.5,                                 -- 18px = 13.5pt
      monthFontWeight = "bold",                            -- month title 700
      weekdayFontWeight = "bold",                          -- weekday labels 600→bold
      selectedFontWeight = "bold",                         -- selected day 600→bold
      todayBtnRadius = 12,                                 -- Today button radius (≠ navBtnRadius 6)
      primaryColor = {61, 214, 232, 255},
      selectedBgColor = false,
      selectedBorderColor = {61, 214, 232, 255},
      selectedBorderWidth = 2,
      selectedTextColor = {61, 214, 232, 255},
      todayBorderColor = {61, 214, 232, 255},
      todayTextColor = {61, 214, 232, 255},
    },
    ColorPicker = {
      primaryColor = {61, 214, 232, 255},                  -- $accent cyan (open border)
      fieldBgColor = {33, 21, 77, 255},                    -- #21154D field background
      fieldBorderColor = {63, 53, 109, 255},               -- #3F356D field idle border
      fieldFontSize = 13.5,                                -- 18px = 13.5pt
      cursorWidth = 12,                                    -- slider knob width (.pen = 12)
      cursorRadius = 3,                                    -- slightly rounded rect (NOT circle)
      cursorBorderColor = {209, 213, 219, 255},            -- #D1D5DB light gray
      sliderRadius = 4,                                    -- hue/alpha track radius
      presetRadius = 6,                                    -- preset swatch radius
    },
    FileUpload = {
      borderRadius = 10, borderWidth = 1.5,
      showHeader = true,
      dropzoneHeight = 116,
      dropzoneBgColor = {42, 31, 94, 255},                 -- $surface
      dropzoneBorderStyle = "solid",
      iconSize = 46,
      iconBgColor = {26, 17, 64, 255},                     -- $background
      iconColor = {74, 139, 245, 255},                      -- $secondary
      iconRadius = 12,
      labelFontWeight = "bold",                             -- 600→bold
    },
    Carousel = {
      borderRadius = 9999,                                 -- arrow btn = circle (engine clamps)
      arrowBgColor = {71, 63, 112, 255},                   -- #473F70 dark purple
      arrowHoverBgColor = {67, 54, 133, 255},              -- #433685 bluer purple
      dotColor = {255, 255, 255, 85},                      -- $textMuted
    },
    TimePicker = {
      primaryColor = {61, 214, 232, 255},
      popupBgColor = {61, 42, 138, 255},                   -- $surfaceHover (elevated popup)
      popupBorderRadius = 16,                              -- popup container corners
      fieldBgColor = {33, 21, 77, 255},                    -- #21154D field background
      fieldBorderColor = {63, 53, 109, 255},               -- #3F356D field idle border
      fieldFontSize = 13.5,                                -- 18px = 13.5pt
      selectedFontWeight = "bold",                         -- selected time 700
      selectedFontSize = 15,                               -- 20px = 15pt (larger than normal 18px)
      selectedBgColor = {255, 255, 255, 26},               -- #FFFFFF1A subtle white
      selectedTextColor = {61, 214, 232, 255},             -- cyan text
    },
    Pagination = {
      buttonBorderWidth = 1,
      activeFontWeight = "bold",                           -- active page 700→bold
      activeBgColor = {100, 76, 194, 255},                 -- #644CC2 cosmic purple
      activeBorderColor = {100, 76, 194, 255},
      activeTextColor = {255, 255, 255, 255},              -- white
      hoverBorderColor = {61, 214, 232, 255},               -- $accent cyan #3ED6E8
      hoverBgColor = false,                                -- no hover bg highlight, border only
    },
    Tree = {
      borderRadius = 16, borderWidth = 1.5,
      backgroundColor = {42, 31, 94, 255},                 -- $surface
      padding = 18,
      fontSize = 12,                                       -- 16px = 12pt
      iconSize = 24,
      indent = 24,
      fontWeight = "bold",                                 -- root 700, children 600 → all bold
      folderIcon = "📁",
      folderOpenIcon = "📂",
      leafIcon = "📄",
      nodeGap = 10,                                          -- item vertical spacing
      hoverBgColor = {61, 48, 125, 255},                   -- #3D307D
      hoverRadius = 8,
      selectedBgColor = {61, 42, 138, 255},                -- $surfaceHover
      iconColor = {255, 255, 255, 85},                     -- $textMuted
      selectedTextColor = {61, 214, 232, 255},              -- $accent cyan
    },
  },
})

UI.Init({
  theme = AstroonTheme,
  scale = UI.Scale.DEFAULT,
})
```

### Button Gradient Formula

Astroon buttons use **gradient fills** for the full cosmic look. The glow shadow is auto-generated by the theme's `glowShadow` config (color derived from variant, no manual shadow needed). Apply `backgroundGradient` per variant:

```lua
-- Primary (Gold) — dark text on bright gold
UI.Button {
  text = "Start Game", variant = "primary",
  textColor = {26, 17, 64, 255},
  backgroundGradient = { direction = 180, from = {255, 213, 79, 255}, to = {240, 160, 48, 255} },
}

-- Success (Green)
UI.Button {
  text = "Confirm", variant = "success",
  backgroundGradient = { direction = 180, from = {46, 204, 113, 255}, to = {29, 168, 85, 255} },
}

-- Secondary (Blue)
UI.Button {
  text = "Details", variant = "secondary",
  backgroundGradient = { direction = 180, from = {74, 139, 245, 255}, to = {51, 102, 204, 255} },
}

-- Danger (Red)
UI.Button {
  text = "Delete", variant = "danger",
  backgroundGradient = { direction = 180, from = {255, 71, 87, 255}, to = {220, 53, 69, 255} },
}
```

| Variant | Gradient From | Gradient To | Text Color | Glow (auto) |
|---------|--------------|-------------|------------|-------------|
| primary | `{255,213,79}` | `{240,160,48}` | `{26,17,64}` **dark!** | gold glow |
| success | `{46,204,113}` | `{29,168,85}` | `{255,255,255}` white | green glow |
| secondary | `{74,139,245}` | `{51,102,204}` | `{255,255,255}` white | blue glow |
| danger | `{255,71,87}` | `{220,53,69}` | `{255,255,255}` white | red glow |

**Hover/Pressed gradient**: Automatically derived from `backgroundGradient` — engine applies `Lighten(from/to, 0.15)` for hover, `Darken(from/to, 0.2)` for pressed. Do NOT hand-write `hoverBackgroundGradient` or `pressedBackgroundGradient` unless you need exact values.

**Glow shadow**: Handled automatically by `glowShadow` in theme — engine derives glow color from `Theme.Color(variantName)` + alpha/blur parameters. Do NOT hand-write `boxShadow` on buttons.

**Without gradient**: buttons still render correctly with solid variant colors from the theme. Gradient is an enhancement for the full Astroon look.

### Cosmic Page Background

For the cosmic gradient page background:

```lua
UI.Panel {
  width = "100%", height = "100%",
  backgroundGradient = { direction = 180, from = {26, 17, 64, 255}, to = {45, 27, 105, 255} },
  children = { ... }
}
```

### Modal / Drawer Action Buttons

Modal action buttons follow a **role-based** rule, not a text-based rule:

- **Main action** (Save, Submit, Delete, Confirm, Apply, Next…) = always `variant="primary"` gold gradient — **never use danger variant**, even for destructive actions. Destructive intent is communicated via title/icon, not button color.
- **Dismiss action** (Cancel, Close, Back, Skip…) = depends on modal type:
  - With header: `variant="secondary"` (blue gradient)
  - Headerless centered dialog: ghost style (`backgroundColor = surfaceHover` + `borderColor = border`)
- **Layout**: both buttons `flexGrow=1, flexShrink=1, flexBasis=0` (equal width), `gap = 12`, in a horizontal row via `SetFooter()`
- **Headerless dialog**: override `contentPadding = {24, 24, 16, 24}` (top=24 without header)

```lua
-- Standard modal footer (with header)
local footer = UI.Panel {
  flexDirection = "row", gap = 12, width = "100%",
  children = {
    UI.Button { text = "Cancel", variant = "secondary", flexGrow = 1, flexShrink = 1, flexBasis = 0,
      backgroundGradient = { direction = 180, from = {74, 139, 245, 255}, to = {51, 102, 204, 255} },
    },
    UI.Button { text = "Delete", variant = "primary", flexGrow = 1, flexShrink = 1, flexBasis = 0,  -- primary, NOT danger!
      textColor = {26, 17, 64, 255},
      backgroundGradient = { direction = 180, from = {255, 213, 79, 255}, to = {240, 160, 48, 255} },
    },
  }
}
modal:SetFooter(footer)
```

### Key Rules Quick Reference

| Rule | Details |
|------|---------|
| **DO NOT hand-write style props** | `borderRadius`, `borderWidth`, `boxShadow`, `glowShadow` are set by the theme. **NEVER** write these on components. |
| **Dark theme** | Background is cosmic purple `{26,17,64}`, text is white `{255,255,255}` — NOT light theme! |
| **Gold primary** | Primary action = warm gold `{255,213,79}`, NOT blue |
| **Primary button text** | Dark `{26,17,64}` (NOT white!) — gold bg needs dark text for contrast |
| **Other button text** | White `{255,255,255}` — success/secondary/danger bg needs white text |
| **Button gradient** | Apply `backgroundGradient` per variant using the formula table above |
| **Pill radius** | Buttons use `borderRadius = 9999`. NanoVG auto-clamps to pill shape |
| **Accent color** | Cyan `{61,214,232}` — used for active tabs, accordion indicators, slider fills |
| **Font size unit** | UrhoX uses pt. Design uses px. `pt = px * 0.75` (e.g., 18px = 13.5pt) |
| **flexShrink** | Default 0 (no shrink). Set `flexShrink = 1` when children should compress |
| **flexDirection** | Default `"column"`. Use `"row"` explicitly for horizontal layout |
| **Border** | Always center-drawn, no inside/outside option |
| **Color format** | `{R, G, B, A}`, values 0-255 |
| **Timeline items: no `color`** | Do NOT set `color` on Timeline items (e.g. `color = "success"`). Per-item color overrides the theme's `dotColor` (cyan). Let the theme control all node colors uniformly. |
| **Rarity colors** | Common `{96,96,128}`, Uncommon `{46,204,113}`, Rare `{74,139,245}`, Epic `{168,85,247}`, Legendary `{255,213,79}` |
