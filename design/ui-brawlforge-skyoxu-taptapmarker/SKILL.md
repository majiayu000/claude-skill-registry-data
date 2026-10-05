---
name: ui-brawlforge
description: "UrhoX UI Design — BrawlForge 竞技/卡通/美式/潮酷对战风格。Use when users need to (1) 创建竞技 / 卡通 / 美式 / 潮酷对战主题游戏 UI, (2) 使用 chunky shapes / vibrant colors / American cartoon 界面主题, (3) 用户提到 BrawlForge 风格或对战卡通主题, (4) competitive / battle-themed 游戏 UI 带粗厚边框与鲜艳配色。"
---

# UrhoX UI Design — BrawlForge Sci-Fi HUD Style

> **Target reader: AI Agent.** When the user asks to "generate UI", "create an interface", "make a button/popup/card" in BrawlForge style, follow this design spec and code templates to produce UrhoX Lua UI code.

## Trigger

Activate this skill when the user request mentions:
- BrawlForge style, blue sci-fi HUD, combat HUD, dark-blue game UI
- Creating any UI component in the cyberpunk / military / esports / neon-blue style

## Design DNA — 8 Rules

**BrawlForge** is a dark, sharp-edged sci-fi HUD style that feels like a futuristic combat interface. Every component should feel **angular, bold, and battle-ready**.

1. **Sharp HUD Silhouette** — Outer frames and buttons use `borderRadius = 0`. No rounding on interactive controls. The HUD should feel like stamped metal panels with crisp edges.
2. **Border System** — Black outer borders (`#0A1020`) define structure. Bottom accent borders in darker variant colors create depth. Colored borders (`$primary`/`$borderFocus`) communicate state and emphasis.
3. **Soft HUD Shadow** — Main shadow token is `$shadow` (`#00000040`). Common offsets are `(6,6)` on panels and buttons, `(8,8)` on toasts. Blur is always `0` for sharp pixel-perfect shadows.
4. **Blue Surface Stack** — `$background` (#2259B7), `$surface` (#21458A), `$surfaceHover` (#2D66C8), with deep black borders for separation. Everything sits on layers of blue.
5. **Accent Ramps** — Primary uses `$primary` / `$primaryHover` / `$primaryPressed` (bright cyan-blue). Secondary uses `$secondary` / `$secondaryHover` / `$secondaryPressed` (vivid purple). Each variant has a darker inset stroke for depth.
6. **Bold Typography** — All UI text uses **Noto Sans SC** with **bold weight** (`fontWeight = "bold"`). Font sizes: 24 / 20 / 18 / 16 / 14 / 12 / 10px (design) mapped to pt. No light or regular weight text anywhere.
7. **Status + HUD Colors** — Success, warning, error, info and rarity colors are all exposed as tokens. HUD bars (HP/MP/Stamina/XP) use dedicated vivid colors.
8. **State System** — Components consistently use default, hover, pressed, focused and disabled states, with `$borderFocus` (#6FE7FF cyan glow) and `$overlay` for emphasis.

## Fonts Setup

Copy fonts and their xml configs from this skill's `fonts/` directory to your project's assets:
```
mkdir -p /workspace/assets/Fonts/
cp ./fonts/* /workspace/assets/Fonts/
```

Required fonts:
- `NotoSansSC-Black.ttf` — all UI text (sans bold, this theme uses bold weight exclusively)

## Workflow

1. **Fonts** — Ensure fonts are copied to project assets (see above)
2. **Widget API** — Read `urhox-libs/UI/Widgets/*.lua` source for props reference
3. **Token table** — Colors/spacing/radius/fonts see `references/theme-tokens.md`
4. **Layout rules** — See `ai-dev-kit/engine-docs/recipes/ui.md`

## Quick Reference

### Theme Initialization

```lua
local UI = require("urhox-libs/UI")

-- BrawlForge HUD shadow: sharp drop, zero blur
local HUD_SHADOW = {
  { x = 6, y = 6, blur = 0, color = {0, 0, 0, 64} },
}

-- Button shadow: .pen offset (10,10) from inner frame, minus border overhang (right=4,bottom=4)
local BTN_SHADOW = {
  { x = 6, y = 6, blur = 0, color = {0, 0, 0, 51} },
}

-- Toast shadow
local TOAST_SHADOW = {
  { x = 8, y = 8, blur = 0, color = {0, 0, 0, 64} },
}

-- Create BrawlForge theme
local BrawlForgeTheme = UI.Theme.ExtendTheme(UI.Theme.defaultTheme, {
  fonts = {
    { family = "sans", weights = {
      normal = "Fonts/NotoSansSC-Black.ttf",
      bold = "Fonts/NotoSansSC-Black.ttf",
    }},
  },
  colors = {
    -- Primary: bright cyan-blue
    primary = {31, 162, 255, 255},           -- #1FA2FF
    primaryHover = {70, 183, 255, 255},      -- #46B7FF
    primaryPressed = {13, 126, 230, 255},    -- #0D7EE6

    -- Secondary: vivid purple
    secondary = {214, 53, 255, 255},         -- #D635FF
    secondaryHover = {224, 97, 255, 255},    -- #E061FF
    secondaryPressed = {181, 35, 232, 255},  -- #B523E8

    -- Background: deep blue layers
    background = {34, 89, 183, 255},         -- #2259B7
    surface = {33, 69, 138, 255},            -- #21458A
    surfaceHover = {45, 102, 200, 255},      -- #2D66C8

    -- Text
    text = {255, 255, 255, 255},             -- #FFFFFF
    textSecondary = {213, 226, 255, 255},    -- #D5E2FF
    textDisabled = {157, 166, 198, 255},     -- #9DA6C6

    -- Border
    border = {10, 16, 32, 255},              -- #0A1020
    borderFocus = {111, 231, 255, 255},      -- #6FE7FF

    -- Disabled
    disabled = {57, 71, 107, 255},           -- #39476B
    disabledText = {139, 150, 184, 255},     -- #8B96B8

    -- Semantic
    success = {67, 213, 44, 255},            -- #43D52C
    successHover = {98, 232, 78, 255},       -- #62E84E
    warning = {255, 198, 26, 255},           -- #FFC61A
    warningHover = {255, 215, 85, 255},      -- #FFD755
    error = {245, 50, 45, 255},              -- #F5322D
    errorHover = {255, 90, 71, 255},         -- #FF5A47
    info = {70, 199, 255, 255},              -- #46C7FF

    -- Overlay
    overlay = {7, 16, 28, 187},              -- #07101CBB

    -- Hover
    hover = {255, 255, 255, 25},             -- #FFFFFF19
  },
  radius = {
    none = 0,
    sm = 4,
    md = 6,
    lg = 10,
    xl = 14,
    full = 9999,
  },
  componentDefaults = {
    borderRadius = 0,   -- Design DNA rule 1: sharp HUD silhouette
    fontWeight = "bold", -- Design DNA rule 6: all UI text is bold
    -- borderWidth and boxShadow are per-component
  },
  components = {
    -- =========================================================
    -- Inputs (Zone 2)
    -- =========================================================
    Button = {
      -- Outer black border: 3D emboss (thicker on right+bottom)
      borderWidth = {2, 4, 4, 2},  -- {top, right, bottom, left}
      borderRadius = 0, fontWeight = "bold",
      height = 50, fontSize = 15, -- 44px content + 2px border top + 4px border bottom
      padding = {4, 6, 10, 4},  -- center text within decoration inner area
      boxShadow = BTN_SHADOW,
      -- Inner colored accent: decoration stroke, inset matches outer border {top=2,right=4,bottom=4,left=2}
      -- deriveBorderColor(props): derives decoration border colors from parent props.
      -- Returns nil to keep static values (standard variant), or {borderColor, ...} to override.
      decorations = (function()
        -- Deepen a color: reduce RGB channels by factor, return integer RGBA
        local function deepen(c, factor)
          return {math.floor(c[1]*factor), math.floor(c[2]*factor), math.floor(c[3]*factor), c[4] or 255}
        end
        -- Shared derive function for all BrawlForge variants: deepen parent bg for inner accent
        local function brawlforgeDeriveDecor(parentProps)
          local bg = parentProps.backgroundColor
          if not bg then return nil end  -- standard variant: keep hand-tuned static values
          return {
            borderColor = deepen(bg, 0.70),
            hoverBorderColor = deepen(parentProps.hoverBackgroundColor or bg, 0.85),
            pressedBorderColor = deepen(parentProps.pressedBackgroundColor or bg, 0.45),
          }
        end
        return {
          primary = {
            { position = "absolute", top = 2, left = 2, right = 4, bottom = 4,
              borderWidth = {2, 2, 6, 2}, borderColor = {27, 115, 227, 255},
              hoverBorderColor = {43, 143, 240, 255},
              pressedBorderColor = {8, 79, 146, 255},
              deriveBorderColor = brawlforgeDeriveDecor },
          },
          secondary = {
            { position = "absolute", top = 2, left = 2, right = 4, bottom = 4,
              borderWidth = {2, 2, 6, 2}, borderColor = {142, 45, 226, 255},
              hoverBorderColor = {163, 71, 244, 255},
              pressedBorderColor = {101, 16, 171, 255},
              deriveBorderColor = brawlforgeDeriveDecor },
          },
          danger = {
            { position = "absolute", top = 2, left = 2, right = 4, bottom = 4,
              borderWidth = {2, 2, 6, 2}, borderColor = {169, 27, 23, 255},
              hoverBorderColor = {196, 42, 38, 255},
              pressedBorderColor = {132, 17, 14, 255},
              deriveBorderColor = brawlforgeDeriveDecor },
          },
          success = {
            { position = "absolute", top = 2, left = 2, right = 4, bottom = 4,
              borderWidth = {2, 2, 6, 2}, borderColor = {35, 116, 24, 255},
              hoverBorderColor = {53, 181, 33, 255},
              pressedBorderColor = {22, 111, 9, 255},
              deriveBorderColor = brawlforgeDeriveDecor },
          },
        }
      end)(),
    },
    TextField = { borderWidth = 3, borderRadius = 0, fontWeight = "bold" },
    Checkbox = {
      borderWidth = 3, borderRadius = 0,
      checkedBgColor = {31, 162, 255, 255},          -- $primary
      checkedBorderColor = {10, 100, 183, 255},      -- #0A64B7
      hoverBorderColor = {31, 162, 255, 255},        -- $primary
      checkmarkColor = {255, 255, 255, 255},         -- white
    },
    Toggle = {
      borderWidth = 3, borderRadius = 0,
      thumbColor = {213, 226, 255, 255},             -- $textSecondary
      thumbCheckedColor = {255, 255, 255, 255},      -- white
      thumbHoverColor = {255, 255, 255, 255},        -- $text
      trackBg = {33, 69, 138, 255},                  -- $surface
      trackBorderColor = {10, 16, 32, 255},          -- $border (black)
      trackHoverBgColor = {45, 102, 200, 255},       -- $surfaceHover
      trackHoverBorderColor = {31, 162, 255, 255},   -- $primary
      trackCheckedBgColor = {31, 162, 255, 255},     -- $primary
      trackCheckedBorderColor = {10, 100, 183, 255}, -- #0A64B7 (darker primary)
      trackCheckedHoverBgColor = {70, 183, 255, 255}, -- $primaryHover
    },
    Slider = {
      borderRadius = 0, trackHeight = 4,
      trackBgColor = {33, 69, 138, 255},             -- $surface
      trackFillColor = {31, 162, 255, 255},           -- $primary
      thumbColor = {31, 162, 255, 255},              -- $primary
      thumbSize = 18,
      thumbBorderWidth = 3,
      thumbBorderColor = {10, 100, 183, 255},        -- #0A64B7
      thumbBorderRadius = 0,
    },
    FileUpload = {
      showHeader = false,
      dropzoneHeight = 104,
      dropzoneBgColor = {18, 63, 127, 255},          -- #123F7F
      dropzoneBorderStyle = "solid",
      iconSize = 28,
      iconColor = {63, 169, 255, 255},               -- #3FA9FF
      labelFontWeight = "bold",
    },

    -- =========================================================
    -- Display (Zone 3)
    -- =========================================================
    Card = {
      borderWidth = 2, borderRadius = 0,
      boxShadow = { { x = 4, y = 4, blur = 0, color = {0, 0, 0, 64} } },
    },
    Badge = { borderWidth = 2, borderRadius = 0 },
    Alert = { borderWidth = 3, borderRadius = 0 },
    Chip  = { borderWidth = 3, borderRadius = 0 },
    Avatar = { showBorder = true },
    ProgressBar = { borderRadius = 0, height = 8 },

    -- =========================================================
    -- Navigation (Zone 4)
    -- =========================================================
    Tabs = {
      borderWidth = 3, borderRadius = 0,
      lineBorderWidth = 3,                           -- line variant base line 3px (pen bottom stroke)
      lineBorderColor = {0, 0, 0, 255},             -- #000000 black base line (pixel-art outline)
      activeBorderColor = {30, 163, 255, 255},       -- #1EA3FF (primary)
      activeBgColor = {30, 163, 255, 255},           -- #1EA3FF for pills/enclosed active
      inactiveTextColor = {213, 226, 255, 255},      -- $textSecondary
      variantTabHeight = {
        line = 40,
        pills = 36,
        enclosed = 44,
      },
      pillMargin = 0,                                -- pill fills full height (no vertical inset)
      variantTabGap = {
        pills = 8,                                   -- 8px gap between pills (line/enclosed stay flush)
      },
      variantBorderRadius = {
        pills = 0,
        enclosed = 0,
      },
      variantActiveBorderColor = {
        pills = {10, 100, 183, 255},                 -- #0A64B7 darker primary
      },
      variantActiveBgColor = {
        enclosed = {30, 163, 255, 255},              -- #1EA3FF
      },
      variantBoxShadow = {
        enclosed = { { x = 0, y = 0, blur = 0, color = {12, 100, 184, 255} } }, -- #0C64B8
      },
      enclosedPadding = 0,
      tabGap = 0,
    },
    Menu = {
      variant = "outlined",
      borderWidth = 3, borderRadius = 0,
      boxShadow = HUD_SHADOW,
      itemHoverBgColor = {31, 84, 190, 255},         -- #1F54BE
      itemHoverTextColor = {31, 162, 255, 255},      -- $primary
      itemHoverInset = 0,
      itemHoverRadius = 0,
      itemVerticalInset = 0,
    },
    Stepper = {
      borderWidth = 3, borderRadius = 0,
      stepBorderWidth = 3,                           -- border on step circles
      hoverBorderColor = {31, 162, 255, 255},        -- $primary
      activeBgColor = {31, 162, 255, 255},           -- $primary
    },
    Breadcrumb = {
      linkColor = {31, 162, 255, 255},               -- $primary
      hoverColor = {70, 183, 255, 255},              -- $primaryHover
      currentColor = {255, 255, 255, 255},           -- $text
      separatorColor = {213, 226, 255, 255},         -- $textSecondary
    },
    Pagination = {
      variant = "outlined",                          -- outlined draws borders on all items
      buttonBorderWidth = 2,
      borderRadius = 0,
      activeBgColor = {31, 162, 255, 255},           -- $primary (fills active item)
      activeBorderColor = {10, 100, 183, 255},       -- #0A64B7
      activeTextColor = {255, 255, 255, 255},        -- white
      hoverBgColor = {45, 102, 200, 255},            -- $surfaceHover
    },
    Carousel = {
      borderWidth = 3, borderRadius = 0,
      arrowBgColor = {33, 69, 139, 255},             -- #21458B (≈ $surface)
      arrowHoverBgColor = {31, 84, 190, 255},        -- #1F54BE
      arrowBorderWidth = 0,                          -- no border on arrows
      dotColor = {114, 119, 132, 255},               -- #727784
    },

    -- =========================================================
    -- Overlay (Zone 5)
    -- =========================================================
    Toast = {
      borderWidth = 2, borderRadius = 0,
      boxShadow = TOAST_SHADOW,
      accentBarWidth = 4,
      accentBarHeight = 32,
      accentBarInset = 12,
      showIcon = false,
    },
    Tooltip = {
      borderWidth = 2, borderRadius = 0,
      boxShadow = HUD_SHADOW,
      tooltipBgColor = {254, 160, 2, 255},           -- #FEA002 (gold/orange)
      borderColor = {249, 95, 3, 255},               -- #F95F03
    },
    Popover = {
      borderWidth = 2, borderRadius = 0,
      boxShadow = HUD_SHADOW,
    },
    Modal = {
      borderWidth = 3, borderRadius = 0,
      boxShadow = HUD_SHADOW,
      headerBgColor = {14, 137, 255, 255},           -- #0E89FF
      contentBgColor = {33, 69, 139, 255},           -- #21458B
      headerBorderWidth = 5,
      footerBorderWidth = 0,                         -- no footer separator
      headerFullWidthBorder = true,
    },
    Drawer = {
      borderWidth = 3, borderRadius = 0,
      boxShadow = HUD_SHADOW,
      contentPadding = 12,
      headerPadding = {0, 16},
    },

    -- =========================================================
    -- Data (Zone 6)
    -- =========================================================
    Dropdown = {
      borderWidth = 2, borderRadius = 0,
      boxShadow = { { x = 8, y = 8, blur = 0, color = {0, 0, 0, 64} } },
      triggerBgColor = {33, 69, 138, 255},           -- $surface
      arrowColor = {31, 162, 255, 255},              -- $primary
      openBorderColor = {30, 163, 255, 255},         -- $primary
      itemHoverBgColor = {12, 44, 109, 255},         -- #0C2C6D
      itemHoverInset = 0,
      itemHoverRadius = 0,
      itemVerticalInset = 0,
    },
    Table = {
      variant = "striped", borderWidth = 3, borderRadius = 0,
      headerBgColor = {14, 137, 255, 255},           -- #0E89FF
      headerFontWeight = "bold",
      headerBorderWidth = 5,
      rowOddBgColor = {11, 44, 109, 255},            -- #0B2C6D
      rowEvenBgColor = {32, 69, 141, 255},           -- #20458D
      rowHoverBgColor = {20, 64, 153, 255},          -- #144099
    },
    List = {
      borderWidth = 3, borderRadius = 0,
      itemBgColor = {248, 210, 39, 255},             -- #F8D227 (gold, normal)
      itemTextColor = {0, 0, 0, 255},                -- black text on gold (normal)
      itemSelectedBgColor = {255, 146, 3, 255},      -- #FF9203 (orange)
      itemSelectedTextColor = {255, 255, 255, 255},  -- white on orange
      itemHoverBgColor = {255, 212, 46, 255},        -- #FFD42E (bright gold)
      itemHoverTextColor = {0, 0, 0, 255},           -- black text on gold
    },
    Accordion = {
      variant = "default", borderWidth = 3, borderRadius = 0,
      headerExpandedBgColor = {157, 0, 198, 255},    -- #9D00C6 (bright purple)
      collapsedTextColor = {213, 226, 255, 255},     -- $textSecondary
      contentBgColor = {30, 40, 57, 255},            -- #1E2839
      bgColor = {74, 38, 82, 255},                   -- #4A2652 (dark purple, collapsed headers)
      headerFontWeight = "bold",
    },
    Rating = { borderRadius = 0 },
    DatePicker = {
      borderWidth = 2, borderRadius = 0,
      fieldBorderRadius = 0,                         -- rect field
      fieldBorderColor = {10, 16, 32, 255},          -- $border (closed state)
      fieldBgColor = {33, 69, 138, 255},             -- $surface
      primaryColor = {31, 162, 255, 255},            -- $primary
      popupBgColor = {47, 52, 80, 242},              -- #2F3450F2
      popupBorderRadius = 0,
      navBtnBgColor = {31, 162, 255, 255},           -- $primary
      navBtnRadius = 0,
      todayBtnRadius = 0, todayBtnHeight = 30,        -- rect shape, pen height=30
      todayBtnBgColor = {45, 102, 200, 255},         -- $surfaceHover
      todayBtnBorderColor = {31, 162, 255, 255},     -- $primary
      todayBtnBorderWidth = 2,
      todayBtnTextColor = {213, 226, 255, 255},      -- $textSecondary (pale blue-white)
      monthFontWeight = "bold",
      weekdayFontWeight = "bold",
    },
    TimePicker = {
      borderWidth = 2, borderRadius = 0,
      fieldBorderRadius = 0,                         -- rect field
      fieldBorderColor = {10, 16, 32, 255},
      fieldBgColor = {33, 69, 138, 255},
      primaryColor = {31, 162, 255, 255},
      popupBgColor = {47, 52, 80, 242},
      selectedBgColor = {31, 162, 255, 255},
    },
    Calendar = {
      borderWidth = 3, borderRadius = 0,
      primaryColor = {31, 162, 255, 255},
      selectedBgColor = {31, 162, 255, 255},
      navBtnBgColor = {31, 162, 255, 255},
      navBtnRadius = 0,
      monthFontWeight = "bold",
      weekdayFontWeight = "bold",
    },
    ColorPicker = {
      borderWidth = 2, borderRadius = 0,
      fieldBorderRadius = 0,                         -- rect field
      fieldBorderColor = {10, 16, 32, 255},
      fieldBgColor = {33, 69, 138, 255},
      primaryColor = {31, 162, 255, 255},
      sliderRadius = 4,                              -- track cornerRadius
      sliderBorderWidth = 2,                         -- track black border
      presetRadius = 0,
      -- Slider thumb (hue/alpha bars)
      cursorWidth = 18,
      cursorHeight = 24,                             -- taller than wide
      cursorRadius = 0,                              -- rect shape
      cursorBorderWidth = 3,
      cursorBorderColor = {10, 100, 183, 255},       -- #0A64B7 darker primary
    },
    Timeline = {
      borderRadius = 0,
      hoverTitleColor = {252, 211, 28, 255},         -- #FCD31C (gold)
      titleFontWeight = "bold",
    },
    Tree = {
      borderRadius = 0,
      backgroundColor = {21, 59, 135, 255},          -- #153B87
      padding = 16,
      nodeGap = 10,
      hoverBgColor = {38, 81, 166, 255},             -- #2651A6
      hoverRadius = 0,
      iconColor = {191, 197, 208, 255},              -- #BFC5D0
    },
  },
})

UI.Init({
  theme = BrawlForgeTheme,
  scale = UI.Scale.DEFAULT,
})
```

### Key Rules Quick Reference

| Rule | Details |
|------|---------|
| **DO NOT hand-write style props** | `borderRadius`, `borderWidth`, `boxShadow` are set by the theme. **NEVER** write these on components. Use `UI.Card` instead of `UI.Panel` + manual styles. Only override when a specific instance needs a different value. |
| **Dark theme** | Background is deep blue `{34,89,183}`, text is white `{255,255,255}` — dark theme! |
| **Sharp corners** | `borderRadius = 0` everywhere. No rounding on interactive controls. The HUD must feel angular and stamped. |
| **Blue primary** | Primary action = bright cyan-blue `{31,162,255}`, secondary = vivid purple `{214,53,255}` |
| **All text is bold** | Every text element uses `fontWeight = "bold"`. Never use regular/light weight. |
| **Font size unit** | UrhoX uses pt. Design uses px. `pt = px * 0.75` (e.g., 20px = 15pt) |
| **Button text** | White text on colored backgrounds. Button text is ALL CAPS in the design. |
| **Bottom accent borders** | Buttons and headers have a darker bottom accent bar (via decorations or headerBorderWidth). This is a key visual signature. |
| **Black outer borders** | `border` color is `{10,16,32}` (near-black). All components are outlined with this deep dark border. |
| **Zero-blur shadows** | Shadows use `blur = 0` for pixel-sharp edges. Offsets: (6,6) panels and buttons, (8,8) toasts. |
| **Tooltip is gold** | Tooltip background is gold/orange `{254,160,2}` with orange border — NOT blue surface! |
| **Modal header blue glow** | Modal header is bright blue `{14,137,255}` with a 5px bottom accent. Content area is standard surface blue. |
| **Accordion purple header** | Expanded accordion header is vivid purple `{157,0,198}` — matches the secondary color family. |
| **Color format** | `{R, G, B, A}`, values 0-255 |
