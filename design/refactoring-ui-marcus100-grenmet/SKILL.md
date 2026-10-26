---
name: refactoring-ui
description: Visual design heuristics from Refactoring UI (Wathan & Schoger), bridged onto this repo's token contract. Use when designing or building a UI surface, when a design "looks off" but the cause is unclear, when choosing between two visual treatments, or when another skill needs the hierarchy/spacing/color/depth vocabulary.
---

Design quality here is not taste — it is a small set of decisions applied consistently. This skill holds those decisions. It is reference, not a sequence: read the ladder, then load only the chapter you need.

## The systems already exist — do not invent new ones

The book's core advice is "define systems in advance so you stop making the same low-level decision twice." This repo already did that. Your job is to **pick from the system**, never to hand-tune a value.

| Book system | Where it lives here | Utility |
|---|---|---|
| Type scale (11 steps, hand-crafted, non-linear) | `--font-size-*` + paired `--line-height-*` in `packages/ui/src/styles/globals.css` | `text-body`, `text-heading-md`, `leading-body-base` |
| Spacing & sizing scale | Tailwind's own scale — deliberately **not** shadowed by a token, so `p-4` keeps its computed value | `p-4`, `gap-6`, `mt-10` |
| Color shades (greys, primary, accents) | Layer 1 `--brand-*` / `--status-*`, consumed through the Layer 2 semantic contract | `bg-primary`, `text-muted-foreground`, `bg-warning-soft` |
| Elevation | `--brand-shadow-card`, `--brand-shadow-focus` | `shadow-card` |
| Radius | `--radius` + `--radius-sm…4xl` | `rounded-lg` |
| Fixed dimensions | `--header-height` | `h-header` |

GMS's own palette is `--gm-*` in `packages/gms/src/styles/foundation.css` — a brand layer, not the shared contract.

**Read the lane spec first.** `docs/design/<gms|gaa-admin|mbia|signal>.md` states each app's colours by role (with contrast), type roles, the allowed radii, elevation approach, signature components and do/don'ts. The heuristics below tell you *how* to judge; the lane spec tells you *what is on-system* for that app.

Adding or changing a token is a cross-app contract change and needs user approval. If a book technique demands a value that has no token, say so and stop — that is a token request, not a licence to hardcode. Everything below is achievable with what already exists.

## The ladder

When a design feels wrong, work down this list. The causes are ordered by how often they are the real problem — most "this looks bad" is a hierarchy failure two rungs above where people start looking.

1. **Hierarchy** — is it obvious what matters most? Nothing else helps until this is right. → [hierarchy.md](hierarchy.md)
2. **Space** — is there enough, and is it grouped so relationships read correctly? → [layout-and-spacing.md](layout-and-spacing.md)
3. **Type** — are sizes on the scale, and do weight, colour and line-height carry their share? → [typography.md](typography.md)
4. **Colour** — is it supporting the hierarchy or fighting it? → [color.md](color.md)
5. **Depth** — do raised and recessed elements sit at meaningful z-heights? → [depth.md](depth.md)
6. **Images** — are photos, icons and screenshots at their intended size, with consistent text contrast? → [images.md](images.md)
7. **Finish** — empty states, accent borders, fewer borders, supercharged defaults. → [finishing-touches.md](finishing-touches.md)
8. **Craft** — every state designed, keyboard and focus, forms, non-text contrast, motion, wording. → [interface-craft.md](interface-craft.md)

When you are starting a surface from nothing rather than fixing one, read [process.md](process.md) first — it covers designing a feature before a layout, working in grayscale, and shipping the smallest useful version.

## Three rules that override instinct

These are the ones most likely to be violated by a plausible-looking first draft, so check them by default:

- **De-emphasise the competition instead of amplifying the target.** When something will not stand out, soften what surrounds it. Adding weight and colour to the thing itself usually makes the page noisier without making it clearer.
- **Semantics are secondary to hierarchy.** An `h1` is a semantic choice, not a size instruction; a destructive button is not automatically red and prominent. Pick the element for meaning, style it for its place in the hierarchy.
- **Colour must never be the only signal.** Pair every colour cue with text, an icon, or a contrast difference. This is also a repo rule — see the Warning Pattern Checklist in `docs/design-system.md` for public warnings and bulletins.

## Where this fits

A supplied design reference or available design workflow produces the canvas; `/ui-check` compares an implementation against it, `pnpm design-system:check` guards the token contract. This skill is the judgment layer under all three: it tells you *what* to change; those tools tell you *whether the change is on-system*.
