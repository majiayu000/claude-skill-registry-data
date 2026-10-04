---
name: apply-fitts-law
description: Use when designing interactive UI elements — buttons, links, menus, form controls — where target size, placement, and spacing affect the speed and accuracy of user interaction.
source: Fitts "The Information Capacity of the Human Motor System" (1954); MacKenzie "Fitts' Law as a Research and Design Tool in Human-Computer Interaction" (1992); Nielsen Norman Group interaction design principles
tags: [ui-ux, fitts-law, interaction-design, accessibility, performance]
verified: true
---

# Apply Fitts Law

Use Fitts's Law — the mathematical model of human pointing movement — to size and place interactive targets so users reach them faster and with fewer errors.

## Why This Is Best Practice

**Adopted by:** Apple Human Interface Guidelines, Google Material Design, Microsoft Fluent Design, and every major operating system and design system that specifies minimum touch target sizes.
**Impact:** MacKenzie (1992) validated Fitts's original model for HCI contexts, establishing that movement time is a predictable function of distance and target size; Apple's iOS HCI guidelines (based directly on Fitts's research) specify 44×44pt minimum touch targets, reducing touch error rates by approximately 30% compared to smaller targets; Google Material Design's 48dp minimum touch target specification similarly cites pointing time and error rate research.
**Why best:** Fitts's Law provides a mathematical basis for UI decisions that would otherwise be made by preference or convention. It converts "make the button bigger" from a designer opinion into an engineering constraint grounded in human physiology and over 70 years of empirical validation.

Sources: Fitts, Paul M. — "The Information Capacity of the Human Motor System in Controlling the Amplitude of Movement," Journal of Experimental Psychology (1954); MacKenzie, I. Scott — "Fitts' Law as a Research and Design Tool in Human-Computer Interaction," Human-Computer Interaction (1992); Nielsen Norman Group — "Fitts's Law and Its Applications in UX" (2022); Apple — "Human Interface Guidelines: Layout" (2024); Google — "Material Design: Accessibility" (2024).

## Steps

1. **Understand the model** — Fitts's Law states: Movement Time (MT) = a + b × log₂(2D/W), where D is the distance to the target and W is the width of the target in the direction of movement. The key implication: doubling target size reduces movement time more than halving the distance to the target. Size matters more than proximity for large distances; proximity matters more for small targets already nearby.

2. **Identify all interactive targets in the design** — List every clickable or tappable element: buttons, links, checkboxes, radio buttons, toggle switches, sliders, icons, navigation items, form inputs. Audit their current sizes and distances from the cursor's expected starting position (typically: screen center for desktop, thumb reach zones for mobile).

3. **Apply minimum size standards** — Minimum targets for touch interfaces: 44×44 CSS pixels (iOS HCI Guidelines) or 48×48dp (Material Design). Minimum for desktop pointer interfaces: 24×24px with 8px spacing between adjacent targets. These minimums are derived from pointing time and error rate research — treat them as non-negotiable floors, not targets to hit exactly.

4. **Prioritize large targets for high-frequency and high-consequence actions** — Fitts's Law dictates where to invest target-size increases. Primary CTAs (submit, purchase, confirm) should be the largest interactive elements on the screen. Destructive actions (delete, cancel subscription) should not be smallest — they should be separated spatially (far from frequent actions) while still meeting minimum size requirements.

5. **Exploit screen edges and corners** — Screen edges and corners are Fitts's Law exceptions: they have effectively infinite depth (the cursor cannot overshoot). Menus pinned to screen edges (macOS menu bar, Windows taskbar) are faster to reach than equivalent elements floating in the center. Use edge placement for high-frequency persistent controls.

6. **Reduce distance for high-frequency operations** — Context menus, hover states, and inline controls reduce the distance component of Fitts's Law for repeated operations. A "delete row" button that appears inline when hovering over a table row is faster to reach than a toolbar button at the top of the screen. Proximity design reduces pointing time for frequent micro-interactions.

7. **Audit spacing between adjacent targets** — Small spacing between adjacent interactive elements causes Fitts's Law errors — the user points accurately but hits the wrong target. Minimum 8px gap between desktop controls; minimum 8–16px gap between mobile touch targets. Form fields, tab bars, and icon grids are common violation sites.

8. **Design thumb-friendly zones for mobile** — On a 6-inch smartphone held in one hand, the bottom 60% of the screen is easily reachable by the right thumb; the top 25% requires a grip shift. Place primary actions (compose, send, pay) in the natural thumb zone. Place destructive or rarely-used controls (settings, delete) in the hard-to-reach zone — spatial distance provides a natural friction barrier.

9. **Validate with interaction analytics** — Use click/tap heatmaps (Hotjar, FullStory) to identify where users click adjacent to targets but miss. Missed clicks adjacent to a small target are empirical Fitts's Law violations — the user aimed correctly but the target was too small or too close to another element. Fix identified by heatmap data, not assumption.

10. **Apply to non-pointer contexts** — Fitts's Law extends beyond mouse and touch. Keyboard navigation (tab order and focus ring size), voice interface (command word length is the "target size"), and game controller interfaces (dead zone sizing) all exhibit Fitts-analogous relationships between target size/distance and interaction accuracy. Apply the principle, not just the formula.

## Rules

- Never reduce a target below minimum size to save layout space — reflow the layout instead; small targets cost users time and generate errors that manifest as support tickets and abandonment.
- Interactive targets must have a visual affordance that matches their actual hit area — a 12px icon with a 44px hit area must communicate its tappability through visual design (background, border, or generous spacing).
- Test on actual devices at actual DPI — design tools show targets at screen resolution, but touch targets must be validated on physical devices with real fingers.

## Common Mistakes

- **Icon-only controls without sufficient padding** — A 24px icon with 4px padding has an effective touch target of 32px — below the 44px minimum. Add invisible hit-area padding using CSS `padding` or a wrapping element sized to minimum target dimensions.
- **Placing destructive actions adjacent to frequent actions** — "Save" and "Delete" side by side at the same size creates error conditions where Fitts's Law's pointing variability causes accidental deletions. Separate destructive actions spatially or require a confirmation step.
- **Ignoring the distance component** — Making a button larger without reducing its distance from the user's cursor starting position provides less benefit than doing both. Design for both dimensions of the law.
- **Applying desktop target sizes to mobile** — 16px desktop links are acceptable for mouse interaction but catastrophically small for finger touch. Context-specific minimum sizes must be applied to each interaction modality.

## Examples

**Effective edge use:** The macOS Dock at the screen bottom is faster to access than any floating taskbar — the screen edge provides infinite effective depth, reducing pointing time to near zero for the approach vector.

**Thumb zone design:** Gmail's mobile compose button is a large FAB (56dp diameter) positioned in the bottom-right corner — at the intersection of maximum thumb reachability and the Fitts's Law screen-edge advantage.

**Adjacent target spacing:** Apple Calendar on iOS separates day-view navigation arrows (prev/next day) with at least 24dp of space and targets each at 44pt diameter — preventing adjacent-target errors despite their proximity.

## When NOT to Use

- Purely decorative elements with no interactive function — applying Fitts's Law sizing to non-interactive visuals wastes layout space.
- Contexts where pointer precision is intentionally required, such as graphics editing tools (precise pixel-level selection), where small targets preserve accuracy that broad targets would destroy.