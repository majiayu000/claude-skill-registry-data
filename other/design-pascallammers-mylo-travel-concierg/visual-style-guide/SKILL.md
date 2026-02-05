---
name: visual-style-guide
description: This skill should be used when the user asks about "colors", "hex codes", "path colors", "tile background", "rendering order", "sorting order", "token design", "SVG styling", "stroke width", "line cap", "grid lines", "glow effect", "visual style", or discusses Zero-Day Attack visual design and styling.
version: 0.2.0
---

# Visual Style Guide

Expert knowledge of Zero-Day Attack visual design, color palette, rendering specifications, and SVG styling conventions.

## Color Palette

### Background Elements

| Element          | Hex       | RGB          | Description                    |
| ---------------- | --------- | ------------ | ------------------------------ |
| Tile Background  | `#151820` | (21, 24, 32) | Very dark blue-gray            |
| Grid Lines       | `#222630` | (34, 38, 48) | Slightly lighter (50% opacity) |
| Board Background | `#0D0F14` | (13, 15, 20) | Darkest blue-gray              |

### Path Colors

| Color  | Hex       | RGB             | Purpose           |
| ------ | --------- | --------------- | ----------------- |
| Red    | `#FF2244` | (255, 34, 68)   | Red player paths  |
| Blue   | `#44BBFF` | (68, 187, 255)  | Blue player paths |
| Purple | `#BB88FF` | (187, 136, 255) | Shared paths      |

### Color Accessibility

Colors tested for color vision deficiencies:

- High contrast between paths and background
- Red appears brownish but distinct in colorblind view
- Blue remains clearly visible
- Purple maintains unique identity

## Path Specifications

### SVG Path Attributes

```svg
<path d="M [start] C [control1], [control2], [end]"
      fill="none"
      stroke="#FF2244"
      stroke-width="8"
      stroke-linecap="butt"/>
```

| Attribute      | Value       | Purpose                       |
| -------------- | ----------- | ----------------------------- |
| fill           | none        | Paths are stroked, not filled |
| stroke         | (color hex) | Path color                    |
| stroke-width   | **8**       | Path thickness in SVG units   |
| stroke-linecap | **butt**    | Square end caps               |

### Path Connections

- Paths connect at edge midpoints (100 units from corners on 200×200 tile)
- Curved paths use bezier curves with consistent radius
- Paths do NOT connect where they visually cross (gap indicates underpass)

## Grid Line Styling

### Cyberpunk Glow Effect

Two-layer rendering:

```csharp
// Glow layer (sorting order 1)
Color glowColor = new Color(0.73f, 0.53f, 1f, 0.3f);  // #BB88FF @ 30%
float glowWidth = 0.2f;

// Core layer (sorting order 2)
Color coreColor = new Color(0.73f, 0.53f, 1f, 0.9f);  // #BB88FF @ 90%
float coreWidth = 0.08f;
```

### Grid Structure

- 5×5 grid with 40-unit spacing in SVG terms
- Lines rendered at 50% opacity
- Reserve zone boundaries: Blue on left, Red on right

## Token Design

### Attack Token

```text
Design: Filled target
- Three concentric circles (solid fill)
- Cross pattern overlay
- Player color fill
```

### Exploit Token

```text
Design: Hollow rings
- Two concentric circles (outline only)
- Faint crosshair overlay
- Player color stroke
```

### Ghost Token

```text
Design: Gradient opacity
- Four concentric circles
- Graduated opacity: 30%, 50%, 70%, 100%
- Player color with transparency
```

### Token Dimensions

| Attribute    | Value                   |
| ------------ | ----------------------- |
| SVG viewBox  | 80×80 units             |
| World Size   | 0.4 units (20% of tile) |
| Texture Size | 40 pixels (at 100 PPU)  |

## Tile Dimensions

| Attribute    | Value            |
| ------------ | ---------------- |
| SVG viewBox  | 200×200 units    |
| World Size   | 2.0×2.0 units    |
| Texture Size | 200 (at 100 PPU) |

### SVG Import Settings (CRITICAL)

**Always use PPU = 100. Adjust Texture Size for world size.**

```text
World Size = Texture Size ÷ 100
```

| Asset  | Texture Size | PPU | World Size |
| ------ | ------------ | --- | ---------- |
| Tiles  | 200          | 100 | 2.0        |
| Tokens | 40           | 100 | 0.4        |

## Rendering Order (Sorting Layers)

Higher sorting order = renders in front.

| Layer         | Order  | Content               | Component           |
| ------------- | ------ | --------------------- | ------------------- |
| Background    | -10    | Board color           | BackgroundRenderer  |
| Tiles         | 0      | Tile sprites          | TileView            |
| Grid Glow     | 1      | Wide purple lines     | GridOverlayRenderer |
| Grid Core     | 2      | Thin purple lines     | GridOverlayRenderer |
| Reserve Lines | 1      | Zone boundaries       | GridOverlayRenderer |
| Edge Nodes    | 3      | Connection indicators | (future)            |
| UI            | Canvas | Text, scores          | Unity UI            |

### Critical: Grid Above Tiles

Grid sorting order MUST be higher than tiles:

- Tiles: 0
- Grid Glow: 1
- Grid Core: 2

If grid order is lower, tiles cover the grid lines.

## Board Layout

### Display Specifications

Target: 1920×1080 pixels = 19.2×10.8 world units (100 PPU)

### Horizontal Layout Visual

```text
┌────────┬──────────┬────────────────────────────┬──────────┬────────┐
│Blue UI │ Blue Res │       5×5 PLAYABLE GRID    │ Red Res  │ Red UI │
│  2.1   │   2.0    │           10.0             │   2.0    │  2.1   │
│#44BBFF │ #44BBFF  │    #BB88FF (firewall)      │ #FF2244  │#FF2244 │
└────────┴──────────┴────────────────────────────┴──────────┴────────┘
← Blue player sits here                      Red player sits here →
```

### Player Orientation

- **Blue player**: Views from LEFT side (x < 0)
- **Red player**: Views from RIGHT side (x > 0)
- UI text rotated appropriately for each player's viewing angle

## SVG Technical Specifications

### Tile Template

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">
  <!-- Background -->
  <rect width="200" height="200" fill="#151820"/>

  <!-- Grid (40-unit spacing, 50% opacity) -->
  <path d="M 0 40 L 200 40 M 0 80 L 200 80 M 0 120 L 200 120 M 0 160 L 200 160"
        stroke="#222630" stroke-width="1" opacity="0.5"/>
  <path d="M 40 0 L 40 200 M 80 0 L 80 200 M 120 0 L 120 200 M 160 0 L 160 200"
        stroke="#222630" stroke-width="1" opacity="0.5"/>

  <!-- Paths -->
  <path d="M 100 0 C 100 50, 150 100, 200 100"
        fill="none" stroke="#FF2244" stroke-width="8" stroke-linecap="butt"/>
</svg>
```

### Edge Node Positions (200×200 viewBox)

| Node   | Position   |
| ------ | ---------- |
| Top    | (100, 0)   |
| Right  | (200, 100) |
| Bottom | (100, 200) |
| Left   | (0, 100)   |

### Path Types

**Quarter-curve (adjacent nodes)**:

```svg
<!-- Left to Top -->
<path d="M 0 100 C 50 100, 100 50, 100 0" .../>
```

**Straight line (opposite nodes)**:

```svg
<!-- Left to Right -->
<path d="M 0 100 L 200 100" .../>
```

## Unity Color Usage

### In C# Code

```csharp
// Background
Color boardBackground = new Color(0.05f, 0.06f, 0.08f);  // #0D0F14
Color tileBackground = new Color(0.08f, 0.09f, 0.13f);   // #151820

// Paths
Color redPath = new Color(1f, 0.13f, 0.27f);             // #FF2244
Color bluePath = new Color(0.27f, 0.73f, 1f);            // #44BBFF
Color purplePath = new Color(0.73f, 0.53f, 1f);          // #BB88FF

// Grid
Color gridLine = new Color(0.13f, 0.15f, 0.19f, 0.5f);   // #222630 @ 50%
```

### In Inspector

Enter hex values directly: `#FF2244`, `#44BBFF`, etc.

## Consistency Rules

1. **Path width**: Always 8 SVG units
2. **Line cap**: Always "butt"
3. **Grid opacity**: Always 50%
4. **Grid spacing**: Always 40 SVG units
5. **Token size**: Always 20% of tile size

## Additional Resources

### Reference Files

For complete visual specifications:

- **Documentation/game-visual-style-guide.md** - Full style guide
- **Documentation/tile-style-guide.svg** - Visual reference with examples
- **Assets/Tiles/** - Reference existing tile SVGs
- **Assets/Tokens/** - Reference existing token SVGs
