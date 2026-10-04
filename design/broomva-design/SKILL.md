---
name: broomva-design
description: Materialize and apply Broomva's platform-neutral calm blue-axis design system across digital products. Includes a portable DESIGN.md contract, semantic styling foundations, general React/web primitives, product-pattern and platform-adaptation guidance, and an optional agentic-work extension. Use for Broomva-branded web, native mobile, desktop, commerce, content, analytics, SaaS, internal tools, communication products, design reviews, or when a request mentions Broomva design, the blackhole mark, blue-axis styling, Undertow, receipts, DESIGN.md, or the Broomva component library.
---

# Broomva Design

Apply one Broomva identity to the product's actual domain. The foundation is calm, matte, blue-axis, and product-neutral. Web components and agentic work patterns are adapters layered above it, never requirements of the brand.

## Start here

1. Read this skill's `DESIGN.md` before changing UI.
2. Inspect the target's platform, existing styles, primitives, accessibility baseline, and incumbent `DESIGN.md`.
3. Read `references/product-patterns.md` and `references/platform-adaptation.md` for the relevant product and platform.
4. Ask the materializer to recommend the smallest profile, then confirm it against the target's real domain. Do not overwrite an incumbent system without an explicit migration request.
5. Implement through semantic roles and reusable components, then validate behavior, accessibility, themes, and representative viewports or device classes.

Set `SKILL_DIR` to the directory containing this file, then materialize the neutral foundation:

```bash
python3 "$SKILL_DIR/scripts/materialize.py" materialize . --profile foundation
python3 "$SKILL_DIR/scripts/materialize.py" verify . --profile foundation
```

For an unfamiliar target, get a recommendation before materializing:

```bash
python3 "$SKILL_DIR/scripts/materialize.py" recommend .
```

Use `--agentic-work` only for products that actually model autonomous work, or `--maintainer` when evolving the design system itself. Explicit intent wins over an installed profile and framework detection. `--framework` accepts only supported web adapters; use `--platform native`, `desktop`, or `embedded` for other products.

Preview without writing:

```bash
python3 "$SKILL_DIR/scripts/materialize.py" materialize . --profile web --dry-run
```

Dry-run output shows grouped counts first. Add `--verbose` only when every affected path is needed.

The command writes `DESIGN.md` at the target root, selected assets under `design-system/broomva/`, and relevant guidance under `design-system/broomva/references/`. Existing differing files cause a failure. Use `--force` only when the user explicitly authorized replacement. When intentionally moving from a broader profile to a smaller one, add `--prune`; the materializer removes only paths owned by another Broomva profile and still protects modified files unless `--force` is also explicit.

## Primary profiles

| Profile | Materializes | Use when |
|---|---|---|
| `foundation` | Portable `DESIGN.md`, machine-readable semantic tokens, standalone CSS, logo, font/license, product patterns, and platform adaptation | Starting any Broomva digital product; this is the default |
| `web` | Foundation plus a web stylesheet entrypoint, 22 general React exports, prompt contracts, public entry points, manifest, and adherence rules | Building a Broomva web or React product without domain-specific work orchestration |
| `agentic-work` | Web profile plus Composer, live-signal motion, seven work exports, canonical work states, and agentic composition guidance | Building agent runs, orchestration, human-in-the-loop decisions, or receipt-driven work UI |

## Advanced and compatibility profiles

These profiles remain available for maintainers and existing automation, but they are not peer choices for a new product.

| Profile | Materializes | Use when |
|---|---|---|
| `full` | Complete curated archive evidence: all 31 exports, specimens, guidelines, templates, desktop kit, browser bundle, and Maestro reference app | Developing or auditing the design system itself; not a default product starter |
| `essentials` | Legacy `DESIGN.md`, `broomva-essentials.css`, and blackhole logo layout | Existing automation that depends on the original minimal profile |
| `tokens` | Legacy essentials plus archived modular tokens, motion, root CSS, fonts/license, full manifest, and adherence rules | Existing automation that depends on the original token-profile file layout |

Prefer `foundation` or `web` for new products. The legacy profiles preserve their pre-portability paths and therefore retain source-era vocabulary; they are not the product-neutral boundary. Do not copy the bundled Maestro app or agentic vocabulary into an unrelated product. Extensions never leak upward into the foundation.

## Auditing this skill (unslop / design gates)

The unit under audit is **`assets/portable/`** — the product-neutral boundary every new product
inherits. It gates CLEAR on its own (BRO-2197: 12 PASS · 2 WARN · 0 FAIL; zero copy tells, zero hex
outside token files, every radius and font a `--bv-*` token). `assets/system/` is the **curated
archive** (full/essentials/tokens profiles): its specimens keep source-era vocabulary as evidence and
must not be edited to green a check — that would be falsifying the archive. A whole-skill survey
therefore reads loud; `.unslop/waivers.json` encodes the boundary with reasons — but waivers are
check-global, so the boundary is **enforced by `.unslop/audit.sh`**: gate 1 re-runs `assets/portable/`
with ZERO waivers (new portable drift fails there no matter what the waiver file says), gate 2 runs
the whole skill with the archive waivers. `.unslop/render-harness.html` renders the shipped
foundation for screenshot evidence. `DESIGN.md`
here is the materialized product contract — never add audit or skill-internal notes to it.

## Preserve the visual thesis

- Keep application chrome on the system sans stack. Cal Sans is opt-in for marketing and hero display surfaces only.
- Use Blue-black ink and whisper-chroma cool neutrals. Reserve Resonant AI Blue for focus, links, information, selection, and rare brand emphasis.
- Keep cards, panels, sidebars, and chrome matte. Glass is earned by real elevation: dialogs, command palettes, popovers, tooltips, dropdowns, and rare focal controls.
- Use the 4px spacing ladder and restrained radii. Cards are `0.75rem`; dialogs are `1rem`; pills belong to action buttons, avatars, and compact status controls, never generic cards.
- Use motion to explain state or spatial change. Preserve meaning under `prefers-reduced-motion`.
- Let the product domain determine composition and language. Do not turn every Broomva product into an orchestration console.

## Adapt to the product

Start from the product's primary objects and user jobs, then select the matching pattern family:

- commerce and transactions;
- editorial, knowledge, and media;
- analytics, monitoring, and operations;
- onboarding, accounts, and settings;
- communication and collaboration;
- agentic work and human intervention.

Read `references/product-patterns.md` for composition guidance. Read `references/platform-adaptation.md` before translating the system to native mobile, desktop, embedded, or constrained surfaces. Preserve semantic roles and interaction quality; do not blindly copy web dimensions to another platform.

## Reuse before inventing

The `web` profile contains 22 general exports across core, forms, navigation, and overlays. The `agentic-work` and `full` profiles expose 31 exports after adding the work extension.

Before creating a new web primitive:

1. Check the selected profile's `manifest.json` for a public export.
2. Read the matching `components/<category>/<Name>.prompt.md` contract.
3. Inspect its `.jsx` and `.d.ts` only when implementation detail is necessary.
4. Import through the profile's public `index.js`, not component internals.

Prompt contracts are compact agent-facing documentation. Load only those relevant to the product task.

## Use the agentic-work extension conditionally

Only load `references/agentic-work.md` when the product actually models autonomous or long-running work. Then use the canonical vocabulary exactly: `Queued`, `Running`, `Stuck`, `Needs you`, `Done`, `Standing`.

- Prefer receipts, decisions, asks, and lifecycle stages over synthetic completion percentages.
- Use `Needs you` only for a concrete human decision or intervention.
- Use Undertow and tidepool as shared live signals, with a static reduced-motion treatment.
- Pair every state color with text, iconography, or structure.

## Agentic design-development loop

For each meaningful interface change:

1. **Retrieve** — read `DESIGN.md`, the target surface, its styles, and relevant pattern/component contracts.
2. **Frame** — state the user job, product objects, information hierarchy, platforms or viewports, and reused primitives.
3. **Implement** — work from semantic roles toward composed components; keep changes surgical.
4. **Inspect** — render at representative device sizes; for responsive web include `375px`, `768px`, and `1440px`, in light and dark themes where supported.
5. **Interact** — exercise keyboard or native input, focus, hover where applicable, loading, empty, error, and reduced-motion states.
6. **Audit** — verify WCAG 2.2 AA contrast, visible focus, appropriate touch targets, semantic structure, and no horizontal overflow.
7. **Reconcile** — if implementation intentionally changes the system, update `DESIGN.md` and related assets in the same change.

Use browser automation, device previews, or screenshots when available. A code-only review is not visual validation.

## Adherence checks

Run the deterministic source check at any time:

```bash
python3 "$SKILL_DIR/scripts/materialize.py" verify-source
```

The `web`, `agentic-work`, and `full` profiles include an Oxlint adherence profile. Integrate it only when the target already uses Oxlint; the materializer does not mutate project lint configuration.

Also audit for:

- raw color values where a semantic token exists;
- new spacing or radius values outside the ladder;
- ambient glass on non-floating surfaces;
- generic gradient heroes or decorative blobs unrelated to the brand mark;
- title case, emoji, em dashes, vague labels, or ornamental eyebrow copy;
- `transition: all`, hover transforms that move layout, or motion without reduced-motion handling;
- icon-only controls without accessible names;
- agentic work language appearing in a product that does not model agentic work.

## Voice

Write plain, precise, action-oriented product copy. Use sentence case. Prefer a short verb phrase over a branded abstraction. Do not use emoji, em dashes, title case, or decorative eyebrow labels. Let domain terms come from the product, not from the design system.

## Boundaries

- Use `broomva-design` for any current Broomva-branded digital product.
- Use the `agentic-work` profile only for orchestration, agent runs, or human-in-the-loop work.
- Use `arcan-glass` only when the request explicitly targets the older glass-forward Arcan language or its Next.js integration patterns.
- Use `design-engineering` for general premium design workflows that are not Broomva-branded.
- Use `design-distill` when extracting a new system from external references rather than applying this one.
- Never claim visual fidelity without rendered evidence.

## Resources

- `DESIGN.md` — canonical platform-neutral design contract copied to target roots.
- `scripts/materialize.py` — safe, deterministic materializer and verifier.
- `references/product-patterns.md` — composition guidance across common digital-product families.
- `references/platform-adaptation.md` — rules for web, native mobile, desktop, and constrained surfaces.
- `references/agentic-work.md` — optional work-state semantics and orchestration composition guidance.
- `references/provenance.md` — archive audit, portability layer, curation decisions, and licensing provenance.
- `references/dogfood-receipt.md` — rendered evidence from independently materialized product designs.
- `assets/portable/` — authored product-neutral foundation and general web adapter metadata.
- `assets/system/` — hash-pinned curated source bundle and visual specimens.
