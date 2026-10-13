---
name: compiling-brand-design-systems
description: >
  Use whenever the user says "compile the design system", "build a design
  system", "build the brand system", "make me a token system", "turn this
  brand into tokens", "design tokens for", "component library for my brand",
  or names a brand plus "design system" — even if they don't say "tokens" or
  "components". Also triggers on: brand system compile, full DS build, token
  architecture, dark/light theming build, sub-brand namespace, CVA component
  set, DTCG tokens, ship the design system, rebuild the design system,
  extend the design system for [sub-brand].
metadata:
  version: "1.0.1"
---

# Compiling Brand Design Systems

Deterministic pipeline: brand inputs → DTCG tokens → CSS custom properties →
Tailwind bridge → typed CVA components → mandatory strict-compile gate →
packaged output. Built from the Abstrekkt parent-system compile (June 2026),
which caught 11 strict-mode type errors that an unvalidated build would have
shipped.

## TL;DR

Three-tier tokens (primitive → semantic → component) in DTCG v1 format,
Tailwind v4 CSS-first as the default bridge, CVA for variants, and a
**mandatory** `tsc --noEmit` gate against current React types before any
file is presented. The compile gate is not optional — it is the skill.

---

## Decision Tree

```
Brand inputs known? (base colors, accent, typefaces, tone, light/dark req)
  ├─ No  → Elicit: category, audience, tone-in-5-words, accent color,
  │        dark/light/both, sub-brands now-or-later. Max 6 questions.
  ├─ Partial → Fill gaps with defaults, label "Assuming X, Y, Z"
  └─ Yes → proceed

Existing brand config file? (e.g., references/brand-config-<name>.md)
  ├─ Yes → Load it. Locked tokens are IMMUTABLE — never regenerate them.
  └─ No  → Generate primitives in OKLCH with hex fallbacks

Token format?
  ├─ DEFAULT: DTCG v1 (2025.10) — $value/$type, file ext .tokens.json
  │   (portable: Style Dictionary v4, Figma, Tokens Studio, Penpot)
  └─ Fallback: custom three-tier JSON only if a consuming tool requires it
      → still document a DTCG export step

Tailwind era?
  ├─ DEFAULT: v4 CSS-first — @theme directive in CSS, NO tailwind.config
  └─ Fallback: v3 tailwind.config.ts bridge — only if the target repo is
      pinned to v3 (check package.json before deciding)

Component variant layer?
  ├─ 3+ variants on a component → CVA (lightweight, best TS inference)
  ├─ 1–2 variants → plain conditional classes, no abstraction
  └─ Never expose Tailwind class names as the public API — components are
      the API (props in, styled element out)

Sub-brands?
  ├─ Yes → Core + extension model: [data-brand="x"] overrides SEMANTIC
  │        layer only. Primitives and component tokens never overridden.
  └─ No  → still ship the three-tier hierarchy (future-proofs extension)

Validation (MANDATORY — no skip path)
  └─ npm install real deps → strict tsc --noEmit → fix → re-run to exit 0
      → sync patched files → package

Scope per session: ONE brand system per session. Sub-brand extensions are
separate sessions that load the parent's locked output.
```

---

## Usage Examples

**Example 1 — Full parent-brand compile.**
User: "Compile the full design system for Abstrekkt."
→ Load `references/brand-config-abstrekkt.md` (locked tokens). Run pipeline:
tokens.tokens.json (DTCG) → tokens.css → @theme bridge → types → utils →
components (Button, Input, Card/Badge/Tooltip, Modal, Toast, Tabs/Select,
Nav/Sidebar/Breadcrumb, Dropdown, Table) → voice.md, accessibility.md,
patterns.md, example page → compile gate → zip.

**Example 2 — Sub-brand extension.**
User: "Extend the design system for Load-Bearing."
→ Load parent core (immutable). Generate ONLY `[data-brand="load-bearing"]`
semantic overrides + type-hierarchy flip. No new primitives. Validate that
zero primitive tokens were touched. Compile gate still mandatory.

**Example 3 — Cold start, unknown brand.**
User: "Build me a design system for my coffee subscription startup."
→ No config file exists. Elicit the 6 brand inputs. Generate primitives in
OKLCH. Full pipeline with defaults labeled. Offer to save a
brand-config-<name>.md so the next run is warm-start.

---

## Pipeline (8 steps)

| # | Step | Output | Reference |
|---|---|---|---|
| 1 | Brand spec | `design/design.md` — identity, type thresholds, surface hierarchy, texture, UX state machines | `references/pipeline-templates.md` |
| 2 | Tokens | `tokens/tokens.tokens.json` (DTCG v1) — primitive/semantic/component tiers | `references/pipeline-templates.md` |
| 3 | CSS | `tokens/tokens.css` — :root dark, [data-theme="light"], component @layer, focus-visible, reduced-motion, grain | `references/pipeline-templates.md` |
| 4 | Tailwind bridge | v4: `@theme` block in CSS. v3 fallback: `tailwind.config.ts` full-override | `references/pipeline-templates.md` |
| 5 | Types + utils | `types/index.ts`, `lib/utils.ts` (cn, trapFocus, announce, prefersReducedMotion) | `references/react19-gotchas.md` |
| 6 | Components | CVA-variant components, forwardRef, full a11y | `references/react19-gotchas.md` |
| 7 | Docs | voice.md, accessibility.md, patterns.md, example page | — |
| 8 | **Gate + package** | strict compile → exit 0 → diff-sync → zip | below |

Typography ratio: Perfect Fourth (1.333) for editorial brands, Major Third
(1.25) for dense UI brands. Spacing: 4px base, layout in 8px multiples.
Shadows: hue-matched to the base undertone — never `rgba(0,0,0,x)`.

---

## Mandatory Compile Gate

Run in a scratch dir, never against the deliverables directly:

```bash
mkdir -p /home/claude/ds-validate && cd /home/claude/ds-validate
cp -r <outputs>/<system>/* .
npm init -y --silent && npm install --silent --no-audit --no-fund \
  typescript @types/react @types/react-dom react react-dom \
  class-variance-authority clsx tailwind-merge tailwindcss
cat > tsconfig.json << 'EOF'
{ "compilerOptions": { "target": "ES2022",
  "lib": ["ES2022","DOM","DOM.Iterable"], "module": "ESNext",
  "moduleResolution": "bundler", "jsx": "react-jsx", "strict": true,
  "noEmit": true, "skipLibCheck": true, "esModuleInterop": true,
  "paths": { "@/*": ["./*"] } },
  "include": ["components/**/*","lib/**/*","types/**/*","app/**/*"] }
EOF
npx tsc --noEmit   # FAIL gate: must reach exit 0 before presenting files
```

After exit 0: copy ONLY the patched files back, verify parity with
`diff -rq` (exclude node_modules, package*.json, tsconfig.json), then zip.
Installing latest deps is deliberate — it surfaces type-definition drift
(React 19 broke five patterns in the Abstrekkt run). If the target repo
pins versions, pin the same versions in the scratch dir instead.

---

## Gotchas

1. **React 19 types break five common patterns.** Zero-arg `useRef<T>()`,
   untyped `cloneElement` children, polymorphic `forwardRef` over element
   unions, `T extends Record<string, unknown>` rejecting interfaces, and
   default event generics (`React.MouseEvent` = `Element`, not
   `HTMLElement`). Exact fixes: `references/react19-gotchas.md`. These pass
   review by eye and fail compile — which is why the gate is mandatory.
2. **Tailwind v4 has no config file.** Emitting `tailwind.config.ts` into a
   v4 repo creates a dead file that silently does nothing. Check
   `package.json` for the Tailwind major before choosing the bridge.
3. **DTCG modes are still settling.** Light/dark theming has a draft
   `$mode` proposal but tools ship their own conventions (Tokens Studio
   sets, Style Dictionary themes). Encode modes as parallel semantic
   token groups + CSS `[data-theme]` overrides — that survives all three.
4. **Sub-brands may only override the semantic layer.** Overriding
   primitives forks the system; overriding component tokens breaks the
   `--ds-*` contract. Enforce by grep: a sub-brand block containing
   `--primitive-` or `--ds-` is a FAIL.
5. **Token bleed prevention is structural, not disciplinary.** Components
   reference `--ds-*` only. Semantic references primitives. Nothing
   references primitives directly from markup. Violations compound
   silently until a rebrand.
6. **Grain/texture overlays need `pointer-events: none` and a fixed
   z-index above content but below modals/toasts** — or every click on the
   page dies. Place portal layers (modal, toast) above the grain z-index.
7. **Don't regenerate locked tokens.** If a brand config marks tokens as
   locked (e.g., FlashFusion v3 violet/magenta/cyan), regeneration —
   even to "equivalent" OKLCH — is a contract violation. Copy verbatim.
8. **One brand per session.** The Abstrekkt run produced 19 files at 232KB
   of source. Stacking sub-brands into the same session degrades the
   later files. Compile parent first; extensions load its locked output.

---

## Self-Verification Checklist

0. Brand inputs confirmed or explicitly defaulted ("Assuming X, Y, Z")
1. Locked tokens (if any) copied verbatim — zero regeneration
2. Tokens in DTCG v1 format (`$value`/`$type`, `.tokens.json`) unless
   consumer-tool exception documented
3. Tailwind era matched to target repo (v4 `@theme` default; v3 config
   only if repo pins v3)
4. Three-tier hierarchy intact; sub-brand overrides touch semantic only
5. Compile gate run; `tsc --noEmit` exit 0 on strict mode with current
   (or repo-pinned) React types
6. Patched files synced back; `diff -rq` parity confirmed before zip
7. No TODO/stub/placeholder strings (`grep -rn "TODO\|FIXME\|PLACEHOLDER"`)
8. Every component: forwardRef, a11y roles/aria, keyboard path, disabled
   and error states
9. Output zipped with single top-level folder; user told where it landed

---

## CLAIMS

- [SOURCED] DTCG spec reached first stable version 2025.10; recommended
  format for new token systems in 2026; Style Dictionary v4, Figma,
  Tokens Studio, Penpot support it — designtokens.org, W3C announcement
  Oct 28 2025
- [SOURCED] Tailwind v4 is CSS-first via `@theme`; the JS config file is
  eliminated — Tailwind v4 docs, corroborated by multiple 2026 practice
  guides
- [SOURCED] CVA preferred at 3+ variants for lightweight runtime and TS
  ergonomics; below that, plain conditionals — Tailwind v4 architecture
  guides, 2026
- [SOURCED] The compile gate caught 11 strict-mode errors across 5 defect
  classes in the Abstrekkt run, June 2026 — session transcript
- [GENERATED] Hue-matched shadows read as higher-craft than neutral black
  shadows on tinted dark bases — design judgment, not measured

## COUNTEREXAMPLE

- A system can pass the compile gate and still be visually broken — type
  safety says nothing about contrast ratios, spacing rhythm, or whether
  the grain overlay renders. The gate is necessary, not sufficient.
- DTCG-default is wrong when the only consumer is a legacy Style
  Dictionary v3 pipeline that predates DTCG support.

## CONTRADICTIONS

! "Latest deps in the gate" vs. "match the target repo" — latest catches
  type drift early but can fail on patterns the pinned repo accepts.
  Resolution: latest by default; pin when a target repo exists.
! Tailwind v4-primary vs. the validated Abstrekkt artifact, which shipped
  a v3-style config (validated against tailwindcss latest but unexecuted
  as a build). The skill's default is ahead of its own reference
  implementation — migrate the Abstrekkt bridge to `@theme` at next touch.
! packaging-skills v3.0.0 requires top-level `version:` frontmatter;
  capturing-workflows v1.2.0 requires `metadata.version`. This skill uses
  `metadata.version` (newer guidance) — expect a WARN from older
  packagers, not a FAIL.
