---
name: tac-uipro-bridge
description: >-
  MANDATORY when the agent is about to invoke or surface output from `ui-ux-pro-max` (uipro) inside tac-express. The uipro skill ships 67 styles, 96 palettes, 57 font pairings — most of which are FORBIDDEN by the Violet Grid design system. This bridge filters uipro recommendations through the Fourteen Laws so the breadth of inspiration never compromises identity. Use whenever a task mentions uipro, "Pro Max", "design intelligence", "67 styles", "96 palettes", or whenever ui-ux-pro-max would otherwise produce a recommendation.
---

# TAC Express — uipro Bridge (ui-ux-pro-max → Violet Grid filter)

> The `ui-ux-pro-max` skill is a **breadth tool**. The Violet Grid is a **constraint identity**. This bridge keeps both true at once: use uipro for accessibility checklists, font-pairing reference, animation timing tokens, anti-pattern lookup — but **never** as a style picker, never as a palette source, never as a font selector.

---

## 0. Hard Filter — what uipro can NEVER override

Before reading anything from uipro CSV results, apply this filter:

| uipro category | Allowed in tac-express? | Why |
|---|---|---|
| **Style: brutalism** | ✅ allowed (this IS the system) | Violet Grid IS brutalist offset shadows, sharp corners |
| **Style: minimalism** | ✅ allowed (compatible companion) | Reduction is the system's premium read |
| **Style: dark mode** | ✅ allowed (default) | Dark-first design |
| **Style: bento grid** | ⚠️ allowed only in marketing surfaces | Compatible with sharp corners; never on dashboard |
| Style: glassmorphism | ❌ FORBIDDEN | LAW 13 — solid surfaces only |
| Style: neumorphism | ❌ FORBIDDEN | Soft shadows banned (LAW 9) |
| Style: claymorphism | ❌ FORBIDDEN | Curves + soft shadows |
| Style: skeuomorphism | ❌ FORBIDDEN | Visual realism contradicts mission-control |
| Style: flat design | ⚠️ degrades to minimalism | Strip the "no shadow" advice — we use offsets |
| **Palette: any** | ❌ NEVER pick from uipro | LAW 1 — only globals.css colors |
| **Font pair: any** | ❌ NEVER pick from uipro | LAW 4 — Plus Jakarta Sans + IBM Plex Mono + Lora only |
| Charts: any uipro suggestion | ❌ FORBIDDEN | Use TAC Orbital primitives only (`docs/CHARTS-ORBITAL.md`) |
| **Accessibility rules** | ✅ ALWAYS use | uipro ≥ tac-accessibility on breadth |
| **Animation timing** | ⚠️ cross-check | uipro suggests 150-300ms; we have `--duration-fast/base/slow` — map, don't replace |
| **Touch targets** | ✅ ALWAYS use | 44×44px minimum is universal |
| **Layout patterns** | ⚠️ adopt the structure, not the visuals | Take grid templates, ignore styling |

**Rule:** if a uipro CSV row's `style` column is anything other than `brutalism`, `minimalism`, `dark mode`, or `bento grid`, **discard the entire row**. Do not mention it to the user.

---

## 1. The 4 Legitimate Uses of uipro in tac-express

### 1.1 Accessibility checklist lookup
```bash
python3 .claude/skills/ui-ux-pro-max/scripts/search.py --domain ux --priority 1
```
Output: WCAG-grounded rules. Cross-reference with `tac-accessibility` — if uipro lists a rule we don't enforce, add it to `tac-accessibility`.

### 1.2 Anti-pattern lookup (uipro's banned-patterns DB)
Use uipro's anti-pattern data to expand the "premium-killers" list in `tac-design-tokens`. Always re-state in Violet Grid terms.

### 1.3 Font-pairing **reference** (NOT selection)
We are locked to Plus Jakarta Sans / IBM Plex Mono / Lora. uipro's 57 pairings tell you **which weights and tracking ranges** other premium pairings use — borrow the *kerning math*, not the family choice.

### 1.4 Animation timing & easing reference
Cross-reference uipro's `duration-timing` rule with our `--duration-fast/base/slow` and `--ease-smooth/spring/linear` tokens. If uipro suggests a timing we don't have a token for, **add a token** rather than hardcoding.

---

## 2. The Translation Table

When uipro returns advice, translate it before applying:

| uipro phrase | Violet Grid translation |
|---|---|
| "Use a card with soft shadow" | `tac-fui-panel` (border + brutalist offset) |
| "Add a gradient background" | DO NOT — solid surfaces. Exception: `t-gradient-hero` on hero h1 only |
| "Round the corners 8px" | DO NOT — `--radius: 0rem` always (LAW 13) |
| "Use a primary blue" | `bg-primary` (resolves to Violet Grid violet) |
| "Use a CTA orange" | `bg-accent-warning` if status; `bg-primary` if action |
| "Inter / Geist / Space Grotesk" | `font-sans` (Plus Jakarta Sans) |
| "Add a hover glow" | `tac-signal-glow` (1px ring + 8px primary bloom) |
| "Use a 12px radius modal" | `--radius: 0rem` — sharp modal, brutalist offset shadow |
| "Skeleton with soft pulse" | `animate-skeleton-pulse` (defined in globals.css) |
| "Make it feel premium with depth" | Use `--surface-base/elevated/floating` tiers, NOT shadow-blur |

---

## 3. Pre-Flight Before Surfacing uipro Output to the User

```
[ ] Filtered out forbidden styles (glassmorphism / claymorphism / neumorphism / skeuomorphism)
[ ] Did NOT recommend a palette from uipro — referenced globals.css instead
[ ] Did NOT recommend a font from uipro — referenced LAW 4 fonts only
[ ] Translated all "rounded-*" / "shadow-*" / "blur-*" advice to Violet Grid equivalents
[ ] Cross-checked accessibility advice against tac-accessibility (loaded together)
[ ] Animation timing maps to --duration-fast / --duration-base / --duration-slow (not raw ms)
[ ] If chart suggested: load tac-design-tokens § "Charts — TAC Orbital" and use Orbital primitives only
```

If any check fails, drop that uipro recommendation and do not relay it.

---

## 4. When NOT to Use uipro at All

uipro is **off-limits** for:

- New feature design (use `tac-brainstorming` → `tac-design-tokens` → `tac-premium-patterns`)
- Picking a color (only `globals.css`)
- Picking a font (only LAW 4)
- Charts (only `docs/CHARTS-ORBITAL.md` + `@workspace/ui/components/charts`)
- Form layout (only `tac-forms`)
- Component structure (only `tac-ui-authoring`)
- Auth UI (only `tac-auth`)

uipro is **on-limits** for:

- "What does uipro say about [accessibility / touch / animation timing / anti-pattern X]?"
- "What's the WCAG rule for [...]?"
- "What's a premium kerning value for a 3rem display heading?" (cross-reference, then apply our `.t-display`)
- "List CSS chart anti-patterns" (then we ignore everything except the structural advice)

---

## 5. Quick Recipe — Using uipro Safely

```bash
# Step 1: Search a focused domain
python3 .claude/skills/ui-ux-pro-max/scripts/search.py --domain accessibility

# Step 2: Apply the Filter (§0)
# Step 3: Apply the Translation Table (§2)
# Step 4: Cross-check against the relevant tac-* skill (tac-accessibility, tac-design-tokens)
# Step 5: Restate the advice in Violet Grid terms before showing it to the user
```

> Never paste raw uipro output. Always translate first.
