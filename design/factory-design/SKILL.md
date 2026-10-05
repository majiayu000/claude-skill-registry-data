---
name: factory-design
description: Design-system discipline distilled across builds. Semantic token vocabulary (name intent, not palette position), CSS variables bridged into Tailwind, dark/light as a variable swap, single- vs two-layer token systems, component primitives as token consumers, when to promote a repeated utility cluster into a primitive, and the vocabulary-sprawl failure mode. Read whenever you touch styling — marketing surface, internal app, or design-system repo. Paired with factory-frontend, which delegates here for visual coherence.
---

# Factory design

Each section leads with **Principle** (one sentence, stack-agnostic), then **Why** (constraint → option → tradeoff), then **Recipe** (the Tailwind + CSS-vars shape we use), and **Failure mode** when there's one to name.

The kit's default styling layer is Tailwind. The discipline here is what turns Tailwind from "every page styled in isolation" into a coherent design system: a small shared vocabulary that every surface draws from.

## Token vocabulary — name intent, not palette position

**Principle.** Tokens are named by the role they play in the layout, never by their position in a colour ladder.

**Why.** Palette-position names (`primary`, `secondary`, `base-100`, `base-200`, `neutral-300`) are the dominant failure mode of theme systems like daisyUI, Bootstrap, and stock Material. The names describe *where on the ramp* a colour lives, not *what it's for*. Asking "is this card a `base-100` or `base-200`?" has no semantic answer — so each developer (and you-on-a-different-day) guesses, and drift accumulates invisibly until two surfaces side by side look subtly off and nobody can articulate why.

Intent-named tokens collapse the ambiguity. `bg` is the page background. `surface` is the raised thing on top of the background. `fg` is primary text. `fg-muted` is the dimmer label next to it. `accent` is the brand pull. `border-subtle` is a divider you barely see. When the vocabulary is small and meaning is unambiguous, the same decision gets made the same way every time. That's the cleanness users feel — it's not "better colours," it's lower entropy.

**Recipe.** Eight to twelve tokens covers most projects. Default set:

| Token | Role |
|---|---|
| `bg` | Page background |
| `surface` | Raised surface on top of `bg` (cards, panels) |
| `surface-hover` | What `surface` becomes on hover |
| `fg` | Primary text |
| `fg-muted` | Secondary text, captions, dimmer labels |
| `border` | Standard divider / outline |
| `border-subtle` | Faint divider (~50% the contrast of `border`) |
| `accent` | Brand pull — CTAs, active state, focus rings |
| `accent-hover` | What `accent` becomes on hover |
| `accent-fg` | Text colour that sits on top of `accent` |
| `code-bg` | Inline code / code-block background (only if the project ships docs) |

Optional semantic-state tokens — add only when the project actually uses them:

`success`, `warning`, `danger`, `info`, each paired with a `-fg` if they appear as filled backgrounds.

**Failure mode.** Importing daisyUI / Bootstrap / Material with their `primary`/`secondary`/`base-N` vocabulary and then "customising" the values. The names leak into every component; renaming later is a codebase-wide search-and-replace. Pay the naming cost up front.

## Token source — CSS variables, bridged into Tailwind

**Principle.** Tokens live as CSS custom properties on `:root`; Tailwind references them via `theme.extend.colors`. No hex literals in any component file, ever.

**Why.** Two consumers need the same source of truth: Tailwind utilities (`bg-surface`, `text-fg-muted`) and the occasional raw CSS rule (`background-color: var(--surface)`). If tokens live only in `tailwind.config`, raw CSS can't reach them. If they live only in CSS, Tailwind can't reach them. CSS custom properties on `:root` are visible to both, and the Tailwind config becomes a thin bridge — it maps utility names to var lookups, nothing more.

The deeper reason: CSS custom properties are runtime-resolved. That makes dark mode a single variable swap (next section) rather than a parallel palette. Build-time constants — Tailwind theme values without var indirection — would force two complete configs.

**Recipe.**

```css
/* src/styles/global.css */
@layer base {
  :root, .dark {
    --bg:             #0b1220;
    --surface:        #131c2e;
    --surface-hover:  #1a2438;
    --fg:             #e2e8f0;
    --fg-muted:       #94a3b8;
    --border:         rgba(148, 163, 184, 0.15);
    --border-subtle:  rgba(148, 163, 184, 0.08);
    --accent:         #5b63fe;
    --accent-hover:   #6b73ff;
    --accent-fg:      #ffffff;
  }
  html:not(.dark) {
    --bg:             #fafafa;
    --surface:        #ffffff;
    --surface-hover:  #f5f5f5;
    --fg:             #0f172a;
    --fg-muted:       #64748b;
    --border:         rgba(15, 23, 42, 0.12);
    --border-subtle:  rgba(15, 23, 42, 0.06);
    --accent:         #4f56e0;
    --accent-hover:   #4049c8;
    --accent-fg:      #ffffff;
  }
}
```

```js
// tailwind.config.mjs
export default {
  theme: {
    extend: {
      colors: {
        bg: "var(--bg)",
        surface: "var(--surface)",
        "surface-hover": "var(--surface-hover)",
        fg: "var(--fg)",
        "fg-muted": "var(--fg-muted)",
        border: "var(--border)",
        "border-subtle": "var(--border-subtle)",
        accent: "var(--accent)",
        "accent-hover": "var(--accent-hover)",
        "accent-fg": "var(--accent-fg)",
      },
    },
  },
};
```

**Failure mode.** A hex literal appears in a component. `bg-[#0f172a]` slips in once because it's "just this card" — six months later, three pages have different greys and the dark-mode swap is broken for that surface. Lint rule or PR-review rule: no hex in components.

## Mode is a variable swap, not a parallel palette

**Principle.** Light/dark (and brand variants) re-define the same token names. Components don't branch on theme.

**Why.** The naive Tailwind pattern is `bg-white dark:bg-slate-900` repeated on every element. That works for tiny apps and collapses at scale: every surface now carries two colour decisions, every refactor doubles the change surface, and a designer can't tweak dark mode without touching every component. The single-variable-swap model moves the decision from the component to the token: `bg-surface` is correct in light and dark; `--surface` knows what to be.

Cost: you commit to symmetric token coverage — every semantic role has a value in every mode. Benefit: components stop knowing what theme they're in.

**Recipe.** Theme class on `<html>` (`.dark` for dark, absent for light), then a sibling rule overrides the vars. No `dark:` Tailwind variants on components — they're a sign the token system isn't carrying its weight.

```html
<html class="dark"> <!-- or no class for light -->
```

**Failure mode.** A page that works in light mode and is unreadable in dark. Almost always one of: a hex literal, a `bg-white` without a `dark:` partner, or a token role that wasn't defined in one mode.

## One layer or two — when to split primitives from semantic

**Principle.** Start single-layer (semantic tokens hold raw values). Split into two layers (primitive → semantic) when the palette needs to be swappable independent of the role names.

**Why.** Two-layer systems separate the *reference palette* (`--blue-500: #4f56e0`) from the *semantic system* (`--accent: var(--blue-500)`). The cost is one more file and one more lookup; the benefit is the ability to swap the palette without renaming roles — useful when you have multi-brand theming, white-label deployments, or a separate design team owning the palette.

For a single product with one brand, single-layer is correct: the semantic name *is* the value. Adding a primitive layer pre-emptively buys flexibility you don't need and dilutes the small vocabulary that makes the system legible.

**Recipe.**

```css
/* Two-layer — when warranted */
:root {
  /* Layer 1: primitives (reference palette) */
  --blue-500: #4f56e0;
  --blue-600: #4049c8;
  --slate-50: #fafafa;
  --slate-900: #0f172a;

  /* Layer 2: semantic (what components consume) */
  --accent:        var(--blue-500);
  --accent-hover:  var(--blue-600);
  --bg:            var(--slate-50);
  --fg:            var(--slate-900);
}
```

Component CSS only references Layer 2. Layer 1 names never appear in `tailwind.config` or component files.

**Failure mode.** Components referencing Layer 1 (`bg-blue-500`) instead of Layer 2 (`bg-accent`). Defeats the whole point — the palette is no longer swappable. Treat Layer 1 names as private.

## What gets a token, what stays a utility

**Principle.** Colour, radius, type scale, and motion get tokens. Spacing, grid, and flex stay raw Tailwind utilities.

**Why.** Tokens carry brand identity — change the accent colour or the type ramp and the product's personality changes. Spacing carries layout, not identity — `p-4` vs `p-6` is a per-surface judgement, not a theme decision. Tokenising spacing produces sprawl (`--space-section-y-md`, `--space-card-x-lg`) without proportional payoff; Tailwind's spacing scale is already the system.

There's a watch-line on type: define a small number of named text styles when a project has clear repeated needs (`text-display`, `text-h1-token`, `text-body-lg`, `text-micro`), but resist tokenising every size.

**Recipe.** Tokenise:

- Colours (the whole semantic set above)
- Radii — `--radius-sm/md/lg/xl` (4/8/12/16px is a common ramp)
- Named type scale — display, h1/h2/h3 equivalents, body-lg, micro
- Motion durations — `--duration-fast/normal/slow` if you find yourself repeating timing values

Leave as raw Tailwind:

- Spacing (`p-`, `m-`, `gap-`)
- Layout (`flex`, `grid`, `col-span-`)
- Sizing (`w-`, `h-`, `max-w-`)

**Failure mode.** Tokenising spacing because "tokens are good." Six months later you have `--space-1` through `--space-24` and nobody can remember which is which, while Tailwind's `p-1` through `p-24` already worked.

## Component primitives consume tokens; pages compose primitives

**Principle.** Build a small set of thin component primitives (Button, Card, Pill, NavLink, SectionLabel) that bake the variant matrix in once. Pages compose primitives, not raw utilities.

**Why.** Tokens alone don't prevent drift — they prevent *colour* drift. The other drift vectors are spacing, padding, focus rings, hover states, radius choices, and motion. A primitive freezes those decisions: every Button has the same focus ring, every Card has the same radius and hover behaviour. Pages stop making those decisions and start composing.

This is also what makes the design system *systematic* rather than *aesthetic*. The token vocabulary defines the words; the primitives define the sentences. Together they make every screen feel like the same product.

**Recipe.** Astro / React component, ~30–50 lines, props for variant/size/state, no hex anywhere. Example shape:

```astro
---
interface Props {
  variant?: "primary" | "ghost" | "outline";
  size?: "sm" | "md";
  href?: string;
}
const { variant = "primary", size = "md", href } = Astro.props;

const base = "inline-flex items-center justify-center rounded-lg font-medium transition-all focus-visible:ring-2 focus-visible:ring-accent/60 focus-visible:ring-offset-2 focus-visible:ring-offset-bg";
const sizing = size === "sm" ? "h-9 px-3 text-sm" : "h-11 px-5 text-sm";
const variantClass =
  variant === "primary" ? "bg-accent text-accent-fg hover:bg-accent-hover"
  : variant === "outline" ? "border border-border bg-transparent text-fg hover:bg-surface-hover hover:border-accent/60"
  : "bg-transparent text-fg-muted hover:text-fg hover:bg-surface-hover";
---
<a href={href} class={`${base} ${sizing} ${variantClass}`}><slot /></a>
```

The minimum primitive set for most sites: Button, Card, Pill / Badge, NavLink, SectionLabel, PageHero. Add one when repeated use justifies it; don't pre-build.

**Failure mode.** Pages full of long Tailwind class strings that *almost* match — `rounded-lg` here, `rounded-xl` there, `h-11` here, `h-12` there. Each near-match is design drift; each primitive collapses dozens of near-matches into one canonical decision.

## Promote drift into a primitive

**Principle.** When the same cluster of utilities appears three times across pages, it's a primitive waiting to be born. Extract it.

**Why.** Three is the rule because two might be coincidence; three is a pattern. Waiting longer means the divergence has already started — by the time you go to lift it, one site has `tracking-[0.18em]` and another has `tracking-[0.16em]` and you have to decide which is canonical (and tell whoever wrote the loser). Lifting at three keeps the cost low: it's a move, not a refactor.

**Recipe.** When you spot a recurring cluster like `text-fg-muted text-sm uppercase tracking-[0.18em]`, create a primitive (`SectionLabel`) and convert callers. Don't add the primitive speculatively; extract from real repetition.

**Failure mode.** "I'll lift this later" written above an inline component that diverged from its siblings before "later" arrived. The lie every local component tells — same one called out in factory-frontend's "Build local components last" section.

## Hold the line on vocabulary size

**Principle.** Stop at ~10–12 tokens. Add a new token only with repeated, hard evidence — never in anticipation.

**Why.** Token sprawl is the failure mode of mature design systems. `surface-2`, `surface-2-hover`, `surface-card`, `surface-card-elevated`, `surface-card-elevated-hover` — each addition feels precise in the moment; in aggregate they collapse the vocabulary back into palette-noise. The fewer words in the dictionary, the less room for the contract to be violated; the more tokens, the more decisions per component and the higher the drift surface.

The honest truth: most "I need another token" moments are actually "I want this specific surface to look slightly different and a token would justify it." That's the moment to push back. Either the new look is wrong, or the existing token's value should change for everyone.

**Recipe.** Before adding a token, write the rule in English: *what role does this play that the existing set doesn't already name?* If the answer is "it's a slightly different shade of an existing role," reject and use the existing token. If the answer names a genuinely new role ("a sunken inset surface, distinct from raised cards"), add it.

**Failure mode.** A `tokens.css` with 60+ entries, three of which differ from each other by 5% opacity and nobody remembers why. At that point the system is design-by-Excel; the recovery is a vocabulary audit and a brutal cull.

## When the existing surface is daisyUI / Bootstrap / Material

**Principle.** Replace the named-palette vocabulary in one pass; don't try to coexist.

**Why.** Half-replaced systems leak. A `btn btn-primary` next to a `bg-accent text-accent-fg` means the design system has two answers to "what's a primary button," and the older answer wins by inertia. Coexistence doubles the surface to maintain and guarantees drift. One pass — replace the colour names, replace the component library's variants with thin primitives, delete the dependency — is finite work. Coexistence is infinite work.

**Recipe.** Approximate sequence:

1. Define the semantic token set (CSS vars on `:root`, light + dark).
2. Bridge into Tailwind via `theme.extend.colors`.
3. Scaffold the minimum primitive set (Button, Card, Pill, NavLink).
4. Convert pages section by section — header, hero, content sections, footer.
5. Remove the old library from `package.json` and config.
6. Lint or grep for hex literals and old class names; treat findings as bugs.

**Source pattern.** fullstack-founder did this exact migration off daisyUI in commits `c324be8` → current; see `tailwind.config.mjs`, `src/styles/global.css`, `src/components/ui/*.astro` for the reference shape.
