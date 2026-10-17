---
name: design-system-authoring
category: design
description: Use when you derive, change or extend a design system - where tokens live per stack, the DTCG token tree, role-based names for both themes, base vs layer vs drift, the DESIGN.md section order, the inventory format, the contrast check and the lint every proposal returns
---
# Design System Authoring

## Overview

A design system the team will actually build with is derived from the code that already exists, named by role, proven against contrast in both themes, and proposed — never invented in a vacuum. The proposal is what every developer run in those repositories will build with from the day it is approved, so a vague token or a missing dark value becomes a hundred one-off decisions downstream.

**Core principle:** Read everything first, keep what is shared, give every deliberate difference a reason, and report the rest as drift.

## 1. Find what exists

Read every repository with a UI (clone the ones not in your workspace: `git clone --depth 1 <root_path or remote_url> _design/<name>`, then `grep_code`/`read_file` with `path: "_design/<name>"`). Note every value with the file and line it came from.

| Stack | Tokens live in | Fonts | Components |
|---|---|---|---|
| Web, Tailwind v4 | `@theme` in `src/index.css` / `app/globals.css`; `:root` and `.dark` / `[data-theme=dark]` CSS variables | `<link>` in `index.html`, `@font-face`, `next/font` in `app/layout.tsx` | `src/components/{ui,atoms,molecules,…}`, `INVENTORY.md`, `components.json`, `*.stories.tsx` |
| Web, Tailwind v3 | `tailwind.config.{js,ts}` `theme.extend` + the CSS variables it points at | same | same |
| Web, CSS-in-JS | `createTheme` (MUI), `extendTheme` (Chakra), `theme.ts` (styled-components / emotion) | same | same |
| iOS (SwiftUI) | `Assets.xcassets/**/*.colorset/Contents.json` (Any/Dark), `Theme.swift`, `Color+*.swift`, `Font+*.swift` | `UIAppFonts` in `Info.plist` | `Views/Components/`, `DesignSystem/` |
| Android (Compose) | `ui/theme/Color.kt`, `Theme.kt`, `Type.kt`, `Shape.kt` | `res/font/` | `ui/components/` |
| Android (views) | `res/values/colors.xml`, `themes.xml`, `values-night/`, `dimens.xml` | `res/font/` | `res/layout/`, custom views |
| Flutter | `ThemeData`, `ColorScheme`, `ThemeExtension`s (`lib/ui/core/theme/`) | `fonts:` in `pubspec.yaml` | `lib/ui/core/{atoms,molecules,organisms}` |

Find the real palette by frequency, not by the theme file alone — a value used in 40 places is the palette, one used once is a one-off or drift. Read-only, in the workspace:

```
grep -rhoE '#[0-9a-fA-F]{6}\b' src | tr 'a-f' 'A-F' | sort | uniq -c | sort -rn | head -40
grep -rhoE 'Color\(0x[0-9A-Fa-f]{8}\)' lib | sort | uniq -c | sort -rn | head -40
```

### Nothing to derive from

A new product with no UI code yet: the brief is the source. Ground every choice in the audience, the subject matter and the references the brief names (rule avoid-ai-default-looks applies hardest here), make ONE deliberate proposal rather than a menu, and write each decision with its reason in DESIGN.md's Overview — the human approves or annotates it like any other.

## 2. Name by role, never by hue

- **Colour:** `background`, `foreground`, `surface`, `surface-raised`, `muted`, `muted-foreground`, `border`, `input`, `ring`, and each action/status colour with its text-on-it pair: `primary`/`on-primary`, `secondary`/`on-secondary`, `accent`/`on-accent`, `destructive`/`on-destructive`, `success`, `warning`, `info` (each with `on-*`). Keep the convention the code already uses (`primary-foreground` in a shadcn repo) — one convention per design system.
- **Type:** `font.family.sans` / `font.family.display` / `font.family.mono`, a `font.size` scale, `font.weight`, `line-height`, and the named roles (`typography.heading-1`, `body`, `body-sm`, `label`, `caption`) as composite tokens.
- **Spacing** on a 4px base (`space.1` = 4px … `space.16` = 64px); **radius** (`radius.sm/md/lg/full`); **shadow** by elevation (`shadow.sm/md/lg`); **motion** (`duration.fast/normal`, `easing.standard`); **layout** (`breakpoint.sm/md/lg/xl`, `container.max`); on mobile `size.touch-target`.
- `blue-500` is a palette value, not a role. A raw palette may exist as its own `palette` group that role tokens alias (`"$value": "{palette.green.700}"`); components only ever see roles.

## 3. The DTCG token tree

Groups are objects; a token is an object with `$value` (and `$type`, on the token or inherited from its group; `$description` where the use is not obvious). Values in the form the code writes them — `#RRGGBB` hex by default (the contrast check reads it), `16px`, `150ms`. Both themes carry the SAME keys; a key missing from one theme is a defect.

```json
{
  "color": {
    "$type": "color",
    "light": {
      "background": { "$value": "#FFFFFF" },
      "foreground": { "$value": "#1C2024" },
      "muted-foreground": { "$value": "#5A6560" },
      "primary": { "$value": "#1F5F4A", "$description": "Primary action, links, focus ring" },
      "on-primary": { "$value": "#FFFFFF" }
    },
    "dark": {
      "background": { "$value": "#111416" },
      "foreground": { "$value": "#E8ECEA" },
      "muted-foreground": { "$value": "#9AA5A0" },
      "primary": { "$value": "#5FB894" },
      "on-primary": { "$value": "#0B1F17" }
    }
  },
  "font": {
    "family": { "sans": { "$type": "fontFamily", "$value": ["Source Sans 3", "system-ui", "sans-serif"] } },
    "size": { "$type": "dimension", "body": { "$value": "16px" }, "heading-1": { "$value": "32px" } }
  },
  "space": { "$type": "dimension", "1": { "$value": "4px" }, "2": { "$value": "8px" }, "4": { "$value": "16px" } },
  "radius": { "$type": "dimension", "md": { "$value": "6px" } },
  "duration": { "$type": "duration", "fast": { "$value": "150ms" } }
}
```

A repository layer holds ONLY the tokens it adds or overrides — a layer token replaces the base token whole; a group merges key by key. Never `null` (refused: a layer cannot delete a base token), never a copy of the base.

## 4. Base, layer or drift

| The difference | It is | It goes |
|---|---|---|
| Every UI repository does it | base | the project base |
| One repository differs on purpose, for a reason a user or a platform gives — a marketing site's campaign colours, iOS 44pt / Android 48dp touch targets, a TV app's larger type | layer | that repository's layer, with the reason in `rationale` |
| One repository differs because a value was copied and changed — `#1F5F4A` vs `#1F5F4B`, 15px body vs 16px, a fourth grey | drift | the report's drift table; the Apply task after approval fixes it |
| The code differs from an already-approved design system | drift | same |

When unsure, it is drift — a layer needs a reason you can write in one sentence. A repository with no project base gets a layer-only, complete design system (every token, DESIGN.md, inventory). If the repository belongs to several projects and none is chosen as its base, ask with `record_open_questions` before proposing anything.

Proposing: base first (`scope: "project"`, `project_id`, `design_md`, `tokens`, `inventory_md`), then each layer (`scope: "repository"`, `repository_id`, `tokens`, `rationale`). Calling it again for the same target from the same task replaces that pending version — that is how you revise. The human approves every version at once by approving the task.

### Lint, after every proposal

Every `propose_design_system` result carries `lint`, and every version `get_design_system` returns carries it too:

| Code | Severity | Means | Fix |
|---|---|---|---|
| `unresolved_alias` | error | `{palette.green.700}` names a token that does not exist | point it at a real token, or add that token |
| `invalid_color` | error | a colour value that is not hex, `rgb()`, `hsl()`, `oklch()`, `oklab()` or a DTCG colour object | write it as `#RRGGBB`, the form the code uses |
| `contrast_below_aa` | error | a colour and its `-foreground` / `on-` pair below 4.5:1, with the `ratio` | change the token until the pair passes — never footnote it |
| `empty_group` | warning | a group with no tokens in it | fill it or drop it |
| `missing_section` | warning | a DESIGN.md section the base lacks | write the section (§5) |

Fix every `error` and propose again before the report is attached — a version with an error finding never goes to review. A `warning` you leave on purpose is named in the report with its reason.

## 5. DESIGN.md — this order, these headings

1. **Overview** — the product, its audience, the feel in three adjectives, and the deliberate choices that make it this product's look and not a template's. The context block other agents get shows only the opening of DESIGN.md, so the first paragraph carries the rules that matter most.
2. **Colors** — each role, what it is for, both themes, the contrast pairs.
3. **Typography** — families and why, the scale (size / line-height / weight per role), measure.
4. **Layout** — breakpoints, grid, container widths, the spacing scale and rhythm, density.
5. **Elevation & Depth** — shadow levels and when each is used; borders vs shadows.
6. **Shapes** — the radius scale and where each applies; the icon library, stroke and sizes.
7. **Components** — the core set, their variants and states; points at the inventory.
8. **Do's and Don'ts** — concrete and checkable ("One primary button per view." "Never a raw hex in a component." "Status is never colour alone.").

Plain markdown, under ~8 KB. A layer's `design_md` covers only what the layer changes and why.

## 6. Component inventory

One line per component, grouped by level, with where it lives in each repository:

```
atom · Button · actions · primary/secondary/ghost/destructive × sm/md/lg · default/hover/focus/active/disabled/loading · web: src/components/atoms/Button.tsx · ios: Views/Components/AppButton.swift
molecule · SearchField · filter a list · with/without clear · default/focus/filled/disabled · web: src/components/molecules/SearchField.tsx · ios: — (missing)
```

A component one repository lacks is listed with `— (missing)`; two implementations of the same thing in one repository are drift.

## 7. Contrast check (WCAG 2.x AA), both themes

Body text ≥ 4.5:1; large text (≥ 24px, or ≥ 18.66px bold) and UI boundaries, icons and focus rings ≥ 3:1. Check every `on-*` against its colour, `foreground` and `muted-foreground` against `background` and `surface`, `primary` as link text on `background`, `ring` against `background`. Read-only, nothing written:

```
python3 - <<'PY'
def lum(h):
    h = h.lstrip('#')
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
def ratio(a, b):
    hi, lo = sorted((lum(a), lum(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)
for name, fg, bg in [
    ("light foreground/background", "#1C2024", "#FFFFFF"),
    ("light muted-foreground/background", "#5A6560", "#FFFFFF"),
    ("dark on-primary/primary", "#0B1F17", "#5FB894"),
]:
    r = ratio(fg, bg)
    print(f"{name}: {r:.2f} {'AA' if r >= 4.5 else 'large text only' if r >= 3 else 'FAIL'}")
PY
```

Convert OKLCH/HSL values to hex first. A failing pair is fixed in the token, never footnoted. The server's lint checks each colour against its `-foreground` / `on-` pair; this check covers the rest — muted text, links, the focus ring. The ratio table goes into the report.

## 8. The report

ONE self-contained HTML document (sanitizer-safe-html), titled `design system: <project or repository> v<N>`: swatches for both themes (each with its token name, value, a text sample in its `on-*` colour and the ratio); the type scale set in real copy; spacing, radius and elevation samples; the core components drawn in their states; per repository a table — token · today in the repository (file:line) · design system · layer or drift; and the lint warnings left, each with its reason. It is what the human approves; everything a reviewer may question is text, not only a picture. Serve it on loopback (screen-mockup-html's self-check) and save a full-page `browser_screenshot` with `attach_to_task: true` and `title: "design-system-<name>-v<N>"`, so the human sees the palette on the task.

## Worked Example

```
web (Tailwind v4): --primary #1F5F4A (src/index.css:14), body 16px, buttons 40px tall
ios (SwiftUI):     Primary.colorset #1F5F4B, body .body (17pt), buttons 44pt tall

#1F5F4A vs #1F5F4B → drift (one digit, no reason) → base color.light.primary #1F5F4A; drift row for ios
17pt vs 16px body  → layer for ios: font.size.body 17px, rationale "iOS Dynamic Type default body size"
44pt vs 40px       → layer for ios: size.touch-target 44px, rationale "Apple HIG minimum hit target"
```

## Common Mistakes

- Inventing a palette for a product whose repositories already have one.
- Hue names (`green-700`) where a role belongs.
- A dark theme with fewer keys than the light one.
- A layer that restates the whole base, or encodes drift with an invented reason.
- Proposing without having run the contrast check.
- Attaching the report while the last `propose_design_system` result still lists an `error`.

## Red Flags

- A token value you cannot trace to a file, the brief, or a decision written in the notes.
- `rationale` that describes the value instead of the reason ("uses a darker green").
- A report with swatches but no per-repository layer/drift table.
