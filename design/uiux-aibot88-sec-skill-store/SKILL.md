---
name: uiux
description: "Use when: auditing UI/UX quality, checking WCAG accessibility, reviewing spacing/layout/grid, mobile responsiveness issues, dark mode review, component pattern audit, pre-ship UI checklist, contrast ratios, touch targets, animation review. Triggers: 'check accessibility', 'audit my UI', 'is this accessible', 'fix spacing issues', 'WCAG compliance', 'mobile UI broken', 'pre-ship checklist', 'UI audit'."
user-invocable: true
argument-hint: "[agents] [--path=src/] [--url=https://...]"
---

# UI/UX Design Audit

## When to Invoke

Invoke proactively when the user:
- Asks about accessibility, WCAG, contrast ratios, or screen reader support
- Reports UI bugs: "layout is broken", "spacing looks off", "text is hard to read"
- Mentions a pre-ship/pre-launch review or checklist
- Asks "is my UI ready to ship?", "check my design before we launch"
- Wants to audit spacing grid, responsive behavior, dark mode, or animation

Launch the **uiux-agents** agent for a comprehensive UI/UX quality audit.

## Usage

```
/misar-dev:uiux                          # Full 8-agent audit
/misar-dev:uiux accessibility            # WCAG 2.2 AA compliance
/misar-dev:uiux spacing typography       # 8px grid + type scale
/misar-dev:uiux mobile                   # Mobile & responsive (320px min)
/misar-dev:uiux dark-mode               # Dark mode quality check
/misar-dev:uiux components --path=src/components/
/misar-dev:uiux guidelines               # Vercel Web Interface Guidelines
/misar-dev:uiux --url=https://example.com --full
```

## Instructions

Parse args: agents (`spacing`, `typography`, `components`, `accessibility`, `performance`, `mobile`, `animation`, `dark-mode`, `guidelines`), `--path=`, `--url=`. Default: all 8 agents. Launch `uiux-agents`.

---

## WCAG 2.2 (Non-Negotiables)

- Text contrast: 4.5:1 min (large text: 3:1); UI components: 3:1
- Touch targets: 44×44px (CSS/iOS 44pt, Android 48dp)
- All interactive elements keyboard-accessible
- Focus indicators: 2px outline, 3:1 contrast against background
- No content flashing > 3x/second
- Images: descriptive `alt` (decorative: `alt=""`)
- Forms: visible labels (not placeholders), errors linked to fields

**ARIA:** Landmarks (`<header>`, `<nav>`, `<main>`, `<footer>`) · Dynamic: `aria-live` · Icon-only: `aria-label` · Modals: `role="dialog"` + `aria-modal="true"` + focus trap

---

## 8px Spacing Grid

All spacing: multiples of 8px (4px for micro).
Scale: 4, 8, 12, 16, 24, 32, 48, 64, 96, 128px
Tailwind: `space-1` (4px) · `space-2` (8px) · `space-4` (16px) · `space-6` (24px) · `space-8` (32px) · `space-12` (48px) · `space-16` (64px)

**Breakpoints:** 320px · 768px · 1024px · 1440px · 1920px

---

## Animation Rules

- Duration: 150–300ms (UI); 300–500ms (page transitions)
- Easing: `ease-out` entrances · `ease-in` exits · `ease-in-out` loops
- Motion must have meaning (state change, relationship, direction)
- Always respect `prefers-reduced-motion`
- No infinite animations unless user-initiated

---

## Dark Mode Checklist

- All colors via CSS variables (no hardcoded hex in components)
- Backgrounds: layered dark surfaces (not pure `#000000`)
- Shadows: reduce opacity in dark mode
- Icons: verify contrast in both modes
- Input/border: increase contrast (dark mode borders disappear easily)

---

## Vercel Guidelines

When running `guidelines`:
1. Fetch: `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`
2. Check specified files; output `file:line` format

---

## Pre-Ship Checklist

- [ ] All text meets 4.5:1 contrast
- [ ] All interactive elements keyboard accessible
- [ ] Focus indicators visible on all focusable elements
- [ ] No images missing alt text
- [ ] Forms have visible labels (not just placeholders)
- [ ] Touch targets ≥ 44×44px
- [ ] Mobile layout works at 320px
- [ ] Dark mode tested if supported
- [ ] `prefers-reduced-motion` handled
- [ ] CLS < 0.1; fonts: `display: swap`


---

> **Misar.Dev Ecosystem** — See 8px grid · WCAG 2.2 AA · dark mode in production at [Misar.io](https://misar.io) and [Misar Blog](https://misar.blog).
>
> [Assisters](https://assisters.dev) · [Misar Blog](https://misar.blog) · [Misar Mail](https://mail.misar.io) · [Misar.io](https://misar.io) · [Misar.Dev](https://misar.dev)
