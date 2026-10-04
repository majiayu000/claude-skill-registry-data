---
name: ui-ux-pro-theory
description: "Pure Design Intelligence for Game Development. Focuses on Color Theory, Typography, UX Patterns, and Visual Styles. Technology-agnostic design principles adapted for Unity (UI Toolkit & Canvas)."
---

# UI/UX Pro - Design Theory & Intelligence

Comprehensive design guide focus solely on **Visual Theory and UX Principles**. This skill provides color palettes, typography pairings, and interaction rules without tying you to web-specific implementations (React/HTML). Use this to design **High-Fidelity Game Interfaces**.

## When to Apply

- **Color Harmony:** Choosing palettes for factions, biomes, or UI themes.
- **Typography:** Selecting font pairings for readability and style.
- **UX Patterns:** Designing intuitive menus, HUDs, and inventory systems.
- **Visual Style:** Defining "Scavenger", "Gritty Tech", or "Golden Sands" aesthetics.
- **Accessibility:** Ensuring game UI is readable and usable by all players.

## 🏜️ Ohm-Yura: Scavenger Aesthetic (PRIMARY)

This project REJECTS generic "clean sci-fi" or "neon cyberpunk" looks. All UI developed using this skill MUST adhere to the following:

### 1. Color Palette: "Golden Sands & Muted Teals"
- **Primary (Sands):** `#D4AF37` (Dull gold), `#C2B280` (Sand), `#8B4513` (Saddle Brown).
- **Secondary (Teals):** `#2F4F4F` (Dark Slate Gray), `#008080` (Teal), `#20B2AA` (Light Sea Green).
- **Accents (Rust/Heat):** `#B22222` (Firebrick), `#FF4500` (Orange Red - used sparingly for heat/energy).
- **Backgrounds:** Off-blacks, dark leathery browns, or oxidized metal shades.

### 2. Shape Language: "Bolted & Notched"
- **NO Perfect Rectangles:** Avoid 4-point boxes. Use `clip-path` or notched corners (45-degree cuts).
- **Layering:** UI should look like "Plates" bolted together. Use thick borders (2px+) with gaps to simulate assembly.
- **Asymmetry:** Slight offsets or "tacked-on" elements (like a small status light on one corner) increase the scavenger feel.

### 3. Texture & Material
- **Grit:** Favor gradients with noise or subtle rust textures over flat colors.
- **Bevels:** Use subtle inner shadows to give UI elements thickness (like metal plates).
- **Glass:** Use "Scratched Glass" effects if using transparency—never perfectly clean blur.

## Rule Categories by Priority

| Priority | Category | Impact | Game Context |
|----------|----------|--------|--------------|
| 1 | Readability & Contrast | CRITICAL | `Text`, `Icons` |
| 2 | Feedback & State | CRITICAL | `Buttons`, `Slots` |
| 3 | Consistency | HIGH | `Theme`, `Layout` |
| 4 | Layout & Hierarchy | HIGH | `Screens`, `HUD` |
| 5 | Shape & Texture | HIGH | `Notches`, `Grit` |
| 6 | Animation & Feel | MEDIUM | `Juice`, `Tweening` |

## Quick Reference: Unity Translation

| Web Concent | Unity Equivalent | Notes |
|-------------|------------------|-------|
| `rem` / `em` | `px` / `%` | Unity prefers explicit pixels or percentages. |
| `Flexbox` | `Flexbox` | UI Toolkit uses standard Flexbox. |
| `z-index` | `Sort Order` | Use `BringingToFront()` or hierarchy order. |
| `hover` | `PointerEnter` | Requires `EventSystem` or `Manipulator`. |
| `focus` | `Selection` | Critical for Gamepad/Keyboard navigation. |

## How to Use This Skill

### Step 1: Generate Design System (Theory)

Use the CLI to generate a coherent design language for your game or interface.
**Ignore web-specific output code; focus on the Hex Codes, Font Names, and Spacing Rules.**

```bash
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "<theme> <genre> <mood>" --design-system
```

**Example:**
```bash
# Sci-Fi Survival HUD
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "sci-fi survival dark holographic" --design-system -p "Ohm-Yura HUD"
```

**Output Interpretation:**
- **Colors:** Use these Hex codes in your `ScriptableObjects` or USS variables.
- **Typography:** Map "Header" to your primary game font, "Body" to secondary.
- **Spacing:** Use the relative scale (e.g., 4px, 8px, 16px) for padding/margins.

### Step 2: Search Specific Domains

Refine specific aspects of your design.

```bash
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "<query>" --domain <domain>
```

| Domain | Use For | Example Keywords |
|--------|---------|------------------|
| `color` | Faction/Biome palettes | "toxic wasteland", "imperial gold", "cyber neon" |
| `typography` | Font discovery | "retro pixel", "clean sans", "gothic serif" |
| `ux` | Interaction rules | "inventory grid", "health bar", "tooltip" |
| `style` | Visual aesthetic | "glassmorphism", "neu-brutalism", "skeuomorphic" |

### Step 3: Implement in Unity

1.  **Define Variables:** Create a `Theme.uss` file with the generated colors and metrics.
2.  **Create Assets:** Import fonts and create TextMeshPro/UI Toolkit font assets.
3.  **Apply Logic:** Use the `ux` domain rules to guide your C# interaction logic (e.g., "Tooltips should appear after 0.5s hover").

## Common Game UI Patterns

### 1. HUD (Heads-Up Display)
- **Vitality:** Health/Ammo must be peripheral but legible.
- **Feedback:** Damage numbers and hit markers require high contrast.
- **Safe Area:** Keep critical UI within the 90% center box (TV safe area).

### 2. Menus & Inventory
- **Navigation:** Support generic input (Mouse, Keyboard, Controller) -> *Focus State is Key*.
- **Grids:** Use consistent spacing (e.g., 8px gaps) generated from the design system.
- **Tooltips:** unexpected obstructions; ensure z-ordering is correct.

### 3. World Space UI
- **Scale:** Distance-based scaling is crucial.
- **Occlusion:** Decide if UI renders on top or is occluded by geometry.

## Visual Quality Checklist

- [ ] **Scavenger Check:** No perfect rectangles or generic neon glows?
- [ ] **Palette Sync:** Using Golden Sands/Muted Teals?
- [ ] **Contrast:** Text vs Background meets 4.5:1 ratio.
- [ ] **Feedback:** Every interaction (Click, Hover) provides visual/audio response.
- [ ] **Consistency:** All buttons share the same base style/prefab.
- [ ] **Typography:** Hierarchy is clear (Header > Subheader > Body).
- [ ] **No "Programmer Art":** Use the defined project palette.
