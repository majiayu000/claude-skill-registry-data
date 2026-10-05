---
name: ui-pixelforge
description: "UrhoX UI Design — PixelForge Retro Pixel-Art Style. Use when users need to (1) 创建像素/复古/8-bit/街机风格的游戏 UI, (2) 使用像素字体和硬边阴影主题, (3) pixel-art / retro / 8-bit / arcade / chunky / blocky UI, (4) 用户提到 PixelForge 风格或像素复古主题。"
---

# UrhoX UI Design — PixelForge Retro Pixel-Art Style

> **Target reader: AI Agent.** When the user asks to "generate UI", "create an interface", "make a button/popup/card" in PixelForge style, follow this design spec and code templates to produce UrhoX Lua UI code.

## Trigger

Activate this skill when the user request mentions:
- PixelForge style, pixel-art UI, retro/8-bit game UI, chunky/blocky UI
- Creating any UI component in the pixel, retro, or arcade style

## Design DNA — 6 Rules

**PixelForge** is a dark, high-contrast pixel-art game UI style. Every component should feel **chunky, crisp, and arcade-ready**.

1. **Border Radius = 0** — **All corners are sharp. No rounding. Zero. Ever.** This is the #1 pixel-art tell. `borderRadius` must not appear in any component code. (Exception: Calendar nav buttons and picker elements use radius 2 internally via theme tokens.)
2. **2px Inside Stroke** — Every interactive element has a `2px` inset border in a **darker shade** of its fill color.
3. **Hard Drop Shadow** — Zero-blur shadows at varying offsets create the chunky pixel-perfect depth effect. Buttons get 3px + bevel highlight; cards get 4px; modals get 4px dark. The theme handles all shadow assignments — do not hand-write `boxShadow`.
4. **Deep Dark Background** — `#0F0F23` base, `#1B1B3A` surface. The high contrast makes pixel edges pop and glow.
5. **High-Saturation Accents** — Teal `#21BDAE` primary, Purple `#6C5CE7` secondary, Red `#FF4757` danger. Bold, saturated, game-ready colors.
6. **Pixel Fonts** — Fusion Pixel 12px Proportional (body/bold) and Monospaced (code/numbers). A generated bold variant (`FusionPixel-12px-Prop-zh_hans-Bold.ttf`) is available — `fontWeight = "bold"` renders visibly thicker text.

## Fonts Setup

Copy fonts and their xml configs from this skill's `fonts/` directory to your project's assets:
```
mkdir -p /workspace/assets/Fonts/
cp ./fonts/* /workspace/assets/Fonts/
```

Required fonts:
- `FusionPixel-12px-Prop-zh_hans.ttf` — body text (regular weight)
- `FusionPixel-12px-Prop-zh_hans-Bold.ttf` — bold text
- `FusionPixel-12px-Mono-zh_hans.ttf` — monospace text

## Workflow

1. **Fonts** — Ensure fonts are copied to project assets (see above)
2. **Widget API** — Read `urhox-libs/UI/Widgets/*.lua` source for props reference
3. **Token table** — Colors/spacing/radius/fonts see `references/theme-tokens.md`
4. **Layout rules** — See `ai-dev-kit/engine-docs/recipes/ui.md`

## Quick Reference

### Theme Initialization

```lua
local UI = require("urhox-libs/UI")

-- Button shadow: 3px hard drop + top-left bevel (Buttons ONLY)
local PIXEL_SHADOW = {
  { x = 3, y = 3, blur = 0, color = {10, 10, 26, 204} },
  { x = -1, y = -1, blur = 0, color = {255, 255, 255, 48} },
}

-- Create PixelForge theme
local PixelForgeTheme = UI.Theme.ExtendTheme(UI.Theme.defaultTheme, {
  fonts = {
    { family = "sans", weights = {
      normal = "Fonts/FusionPixel-12px-Prop-zh_hans.ttf",
      bold = "Fonts/FusionPixel-12px-Prop-zh_hans-Bold.ttf",
    }},
    { family = "mono", weights = {
      normal = "Fonts/FusionPixel-12px-Mono-zh_hans.ttf",
    }},
  },
  colors = {
    primary = {33, 189, 174, 255},            -- Teal #21BDAE
    primaryHover = {61, 208, 193, 255},       -- #3DD0C1
    primaryPressed = {25, 168, 153, 255},     -- #19A899
    secondary = {108, 92, 231, 255},          -- Purple #6C5CE7
    secondaryHover = {133, 119, 237, 255},    -- #8577ED
    secondaryPressed = {90, 75, 214, 255},    -- #5A4BD6
    background = {15, 15, 35, 255},           -- Deep dark navy #0F0F23
    surface = {27, 27, 58, 255},              -- Dark panel #1B1B3A
    surfaceHover = {37, 37, 80, 255},         -- #252550
    text = {240, 240, 240, 255},              -- Near-white #F0F0F0
    textSecondary = {160, 160, 192, 255},     -- Muted lavender #A0A0C0
    textDisabled = {80, 80, 112, 255},        -- #505070
    border = {58, 58, 106, 255},              -- Indigo border #3A3A6A
    borderFocus = {33, 189, 174, 255},        -- Teal focus = primary
    disabled = {42, 42, 74, 255},             -- #2A2A4A
    disabledText = {80, 80, 112, 255},        -- #505070
    success = {80, 200, 120, 255},            -- Bright green #50C878
    successHover = {102, 216, 142, 255},      -- #66D88E
    warning = {255, 217, 61, 255},            -- Bright yellow #FFD93D
    warningHover = {255, 224, 102, 255},      -- #FFE066
    error = {255, 71, 87, 255},               -- Bright red #FF4757
    errorHover = {255, 107, 122, 255},        -- #FF6B7A
    info = {69, 170, 242, 255},               -- Bright blue #45AAF2
    overlay = {0, 0, 0, 180},                 -- #000000B4
  },
  radius = {
    sm = 2,    -- subtle pixel rounding for picker/calendar elements
    md = 2,
    lg = 4,
    xl = 4,
    full = 0,  -- pill shapes not used in pixel-art
  },
  componentDefaults = {
    borderRadius = 0,              -- sharp corners on ALL components by default
  },
  components = {
    ----------------------------------------------------------------
    -- Inputs
    ----------------------------------------------------------------
    Button = { borderWidth = 2, boxShadow = PIXEL_SHADOW },
    TextField = { borderWidth = 2 },
    Checkbox = {
      borderWidth = 2,
      checkedBgColor = {33, 189, 174, 255},        -- primary
      checkedBorderColor = {27, 176, 161, 255},     -- #1BB0A1
      checkmarkColor = {255, 255, 255, 255},        -- white
      hoverBorderColor = {33, 189, 174, 255},       -- primary
    },
    Toggle = {
      borderWidth = 2, thumbSize = 18,
      thumbColor = {160, 160, 192, 255},            -- $textSecondary (gray when off)
      thumbCheckedColor = {255, 255, 255, 255},     -- white when on
      thumbHoverColor = {240, 240, 240, 255},       -- $text (brighten on hover)
      trackHoverBgColor = {37, 37, 80, 255},        -- $surfaceHover
      trackHoverBorderColor = {33, 189, 174, 255},  -- $primary (border turns teal)
    },
    Slider = {
      borderWidth = 1,
      trackBgColor = {27, 27, 58, 255},             -- $surface
      trackFillColor = {33, 189, 174, 255},          -- $primary
      thumbColor = {33, 189, 174, 255},              -- $primary
      thumbBorderWidth = 2,
      thumbBorderColor = {27, 176, 161, 255},        -- #1BB0A1
    },

    ----------------------------------------------------------------
    -- Display
    ----------------------------------------------------------------
    Card = {
      borderWidth = 2,                               -- outlined variant border (engine only applies to outlined)
      boxShadow = {                                   -- elevated variant shadow
        { x = 4, y = 4, blur = 0, color = {10, 10, 26, 204} },
      },
    },
    Badge    = { borderWidth = 1 },
    Alert    = { borderWidth = 2 },
    Chip     = { borderWidth = 2 },
    Avatar   = { showBorder = true, shape = "square" },
    ProgressBar = { height = 16, borderWidth = 2 },
    FileUpload = {
      dropzoneBgColor = {27, 27, 59, 255},           -- #1B1B3B (surface-ish)
      iconColor = {69, 170, 242, 255},                -- $info
    },

    ----------------------------------------------------------------
    -- Navigation
    ----------------------------------------------------------------
    Tabs = {
      borderWidth = 2,
      activeBorderColor = {33, 189, 174, 255},      -- $primary (line indicator + pills active border)
      activeFontWeight = "700",                      -- bold active tab text (all variants)
      inactiveTextColor = {160, 160, 192, 255},     -- $textSecondary
      tabGap = 8,                                    -- gap between pills tabs
      enclosedPadding = 0,                           -- no internal padding in enclosed container
      variantActiveBgColor = {                        -- per-variant active tab bg
        enclosed = {37, 37, 80, 255},                 -- $surfaceHover
        -- pills: nil → engine default primary
      },
      variantActiveBorderColor = {                    -- per-variant active tab border
        pills = {27, 176, 161, 255},                  -- #1BB0A1 (darker primary)
        -- line: nil → activeBorderColor (primary)
      },
      variantBoxShadow = {                            -- per-variant active tab shadow
        pills = {{ x = 2, y = 2, blur = 0, color = {10, 10, 26, 204} }},
      },
    },
    Menu = {
      borderWidth = 2,
      boxShadow = {
        { x = 3, y = 3, blur = 0, color = {10, 10, 26, 204} },
      },
      itemHoverBgColor = {37, 213, 194, 24},         -- primary-ish 9% alpha
      itemHoverTextColor = {33, 189, 174, 255},      -- $primary
      itemHoverFontWeight = "600",                    -- semi-bold on hover
      itemHoverInset = 0,
      itemHoverRadius = 0,
      itemVerticalInset = 0,                          -- flush to top/bottom edges
    },
    Stepper  = { borderWidth = 2, hoverBorderColor = {33, 189, 174, 255} },
    Pagination = {
      buttonBorderWidth = 2,
      hoverBorderColor = {33, 189, 174, 255},
      activeBgColor = {33, 189, 174, 255},           -- $primary
      activeBorderColor = {25, 168, 153, 255},       -- $primaryPressed
    },
    Carousel = {
      arrowBgColor = {49, 49, 99, 255},              -- #313163
      arrowHoverBgColor = {50, 50, 126, 255},         -- #32327E
      dotColor = {108, 114, 135, 255},                -- #6C7287 (inactive dots)
    },

    ----------------------------------------------------------------
    -- Overlay
    ----------------------------------------------------------------
    Modal = {
      borderWidth = 2,
      boxShadow = {
        { x = 4, y = 4, blur = 0, color = {0, 0, 0, 204} },
      },
      headerBgColor = {20, 20, 46, 255},             -- #14142E
      headerBorderWidth = 2,
      headerFullWidthBorder = true,
      footerBorderWidth = 2,
      footerFullWidthBorder = true,
      contentPadding = 16,
      footerPadding = {10, 16},
    },
    Drawer = {
      borderWidth = 2,
      boxShadow = {
        { x = 4, y = 0, blur = 0, color = {10, 10, 26, 204} },
      },
      contentPadding = 12,
      headerPadding = {0, 16},
    },
    Toast = {
      borderWidth = 2,
      boxShadow = {
        { x = 3, y = 3, blur = 0, color = {10, 10, 26, 204} },
      },
      accentBarHeight = 32,
      accentBarWidth = 4,
      accentBarInset = 12,
      showIcon = false,
    },
    Tooltip = {
      borderWidth = 2,
      boxShadow = {
        { x = 2, y = 2, blur = 0, color = {10, 10, 26, 204} },
      },
      tooltipBgColor = {30, 30, 58, 240},            -- #1E1E3AF0
    },
    Popover = {
      borderWidth = 2,
      boxShadow = {
        { x = 3, y = 3, blur = 0, color = {10, 10, 26, 204} },
      },
    },

    ----------------------------------------------------------------
    -- Data
    ----------------------------------------------------------------
    Dropdown = {
      borderWidth = 2,
      boxShadow = {
        { x = 3, y = 3, blur = 0, color = {10, 10, 26, 204} },
      },
      arrowColor = {33, 189, 174, 255},              -- $primary (arrow ▼)
      itemHoverBgColor = {37, 213, 194, 24},         -- primary-ish 9% alpha
      itemHoverTextColor = {33, 189, 174, 255},      -- $primary
      itemSelectedTextColor = {33, 189, 174, 255},   -- $primary
      selectedFontWeight = "600",                     -- semi-bold selected
      itemHoverInset = 0,
      itemHoverRadius = 0,
      itemVerticalInset = 0,                          -- flush to top/bottom edges
    },
    Table = {
      variant = "striped", borderWidth = 2,
      headerBgColor = {37, 37, 80, 255},             -- $surfaceHover
      rowOddBgColor = {27, 27, 58, 255},             -- $surface
      rowEvenBgColor = {27, 27, 58, 128},            -- $surface 50% alpha
      rowHoverBgColor = {37, 213, 194, 16},          -- primary-ish 6% alpha
    },
    List = {
      borderWidth = 2,
      itemSelectedBgColor = {37, 213, 194, 16},      -- primary-ish 6% alpha
      itemSelectedTextColor = {33, 189, 174, 255},   -- $primary
    },
    Accordion = {
      borderWidth = 2,
      headerExpandedBgColor = {37, 37, 80, 255},     -- $surfaceHover
      collapsedTextColor = {160, 160, 192, 255},     -- $textSecondary
      contentBgColor = {15, 15, 35, 32},             -- $background 12% alpha
    },
    Calendar = {
      primaryColor = {33, 189, 174, 255},             -- $primary
      selectedBgColor = {33, 189, 174, 32},           -- primary 12% alpha
      selectedBorderColor = {33, 189, 174, 255},      -- $primary
      selectedBorderWidth = 2,
      selectedTextColor = {69, 170, 242, 255},        -- $info (#45AAF2)
      navBtnBgColor = {30, 50, 75, 255},              -- dark blue tint
      navBtnRadius = 2,
      borderRadius = 0,
    },
    DatePicker = {
      primaryColor = {33, 189, 174, 255},
      selectedBgColor = {33, 189, 174, 32},
      selectedBorderColor = {33, 189, 174, 255},
      selectedBorderWidth = 2,
      selectedTextColor = {69, 170, 242, 255},
      navBtnBgColor = {30, 50, 75, 255},
      navBtnRadius = 2,
      popupBgColor = {27, 27, 58, 255},               -- $surface
      fieldBorderColor = {58, 58, 107, 255},           -- ~$border
      fieldBgColor = {27, 27, 58, 255},                -- $surface
    },
    TimePicker = {
      primaryColor = {33, 189, 174, 255},
      selectedBgColor = {33, 189, 174, 32},
      selectedTextColor = {255, 255, 255, 255},        -- white
      popupBgColor = {27, 27, 58, 255},
      fieldBorderColor = {58, 58, 107, 255},
      fieldBgColor = {27, 27, 58, 255},
    },
    ColorPicker = {
      primaryColor = {33, 189, 174, 255},
      fieldBorderColor = {58, 58, 107, 255},
      fieldBgColor = {27, 27, 58, 255},
      sliderRadius = 0,                               -- sharp slider tracks
      presetRadius = 2,                                -- subtle rounding on preset swatches
    },
    Timeline = {
      dotColor = {32, 189, 174, 255},                  -- ~$primary
      lineColor = {38, 178, 167, 255},                 -- #26B2A7
      hoverTitleColor = {32, 189, 174, 255},           -- ~$primary
    },
    Tree = {
      backgroundColor = {27, 27, 58, 255},             -- $surface
      borderWidth = 2,
      padding = {18, 22},                               -- vertical 18, horizontal 22
      nodeGap = 16,
      hoverBgColor = {47, 47, 88, 255},                -- #2F2F58
      iconColor = {108, 92, 231, 255},                  -- $secondary (folder icons)
      iconSize = 22,
      folderIcon = "📁",
      folderOpenIcon = "📂",
      leafIcon = "📄",
      hoverRadius = 2,
      indent = 22,                                      -- child left padding offset
    },
    Breadcrumb = {
      linkColor = {33, 189, 174, 255},                  -- $primary
      separatorColor = {160, 160, 192, 255},            -- $textSecondary
      currentColor = {240, 240, 240, 255},              -- $text
    },
  },
})

UI.Init({
  theme = PixelForgeTheme,
  scale = UI.Scale.DEFAULT,
})
```

### Shadow Reference

Different components use different shadow profiles — **all handled by the theme**, never hand-write `boxShadow`:

| Shadow | Offset | Bevel | Components |
|--------|--------|-------|------------|
| PIXEL_SHADOW | 3px | Yes (-1,-1 white) | Button |
| Drop 3px | 3px | No | Menu, Dropdown, Toast, Popover |
| Drop 2px | 2px | No | Tooltip |
| Drop 4px | 4px | No | Card (elevated) |
| Dark 4px | 4px (black) | No | Modal |
| Horiz 4px | x=4, y=0 | No | Drawer |

### Key Rules Quick Reference

| Rule | Details |
|------|---------|
| **DO NOT hand-write style props** | `borderRadius`, `borderWidth`, `boxShadow` are set by the theme. **NEVER** write these on components. Use `UI.Card` instead of `UI.Panel` + manual styles. Only override when a specific instance needs a different value. |
| **Dark theme** | Background `{15,15,35}`, text `{240,240,240}` — deep dark with bright text |
| **Teal primary** | Primary action = bright teal `{33,189,174}`, NOT blue |
| **Font size unit** | UrhoX uses pt. Design uses px. `pt = px * 0.75` (e.g., 14px = 10.5pt) |
| **flexShrink** | Default 0 (no shrink). Set `flexShrink = 1` when children should compress |
| **flexDirection** | Default `"column"`. Use `"row"` explicitly for horizontal layout |
| **Border** | Always center-drawn, no inside/outside option |
| **Color format** | `{R, G, B, A}`, values 0-255 |
| **Button text color** | White `{240,240,240}` — dark theme contrast |
| **Pixel font** | Bold variant available (`FusionPixel-12px-Prop-zh_hans-Bold.ttf`). `fontWeight = "bold"` renders visibly thicker text. |
| **Pagination shape** | Pass `shape = "square"` to match pixel-art style |
| **Avatar shape** | Default `shape = "square"` via theme; circle avatars use explicit `shape = "circle"` |
| **Modal 按钮布局** | 有 footer 分隔线（默认）：固定宽度按钮 + `justifyContent = "end"` 靠右。无分隔线：`width = "fill_container"` 按钮 + `justifyContent = "space-between"` 平铺。确认按钮统一用 `primary`（不用 danger）。 |
