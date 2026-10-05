---
name: hig
description: Apple Human Interface Guidelines (HIG) lookup and routing for iOS, iPadOS, and macOS design work. Use when any Apple-platform design spec, term, or behaviour is in question — minimum tap target or hit target size, type sizes, Dynamic Type, safe areas, bar heights, corner radii, sheet detents, menu structure, native component names — or when work touches Liquid Glass-era APIs (glassEffect, GlassEffectContainer, scrollEdgeEffect, tabViewBottomAccessory) even without HIG framing. Model priors on Apple's current design system are stale (the HIG was rewritten for Liquid Glass in 2025–26) — never answer Apple design-spec questions from memory. Routes design and prototyping work to hig-design and HIG audits to hig-review. Also use to check whether the local HIG snapshot is current. For web-platform values on non-Apple work, use ui-craft.
---

# HIG

Coordinator and spec-lookup for the HIG suite. Snapshot: see `references/versions.md` — check its expiry before asserting volatile guidance.

**Your training-data priors on Apple design are wrong.** Apple rewrote its design system twice since 2024 (Liquid Glass, WWDC 2025; foundations rework, WWDC 2026). Opaque pinned tab bars, flat design, single-PNG icons, "Clarity/Deference/Depth", SiriKit, iOS 18/19 numbering — all dead. `references/corrections.md` lists what changed. Answer Apple design questions from the references or a live fetch, never from memory.

---

## 1. Route first

| Task | Lead | Load |
|---|---|---|
| Design, mock, or prototype a screen/app | `hig-design` | — |
| Port between iOS and macOS, "make a Mac version" | `hig-design` | `references/adaptation.md` |
| Implement or fix SwiftUI/Liquid Glass UI | `hig-design` | `references/adapters/swiftui.md` |
| Audit/review against the HIG, "does this feel native" | `hig-review` | — |
| Exact spec, term, or behaviour question | stay here | §2–§3 |
| "Is our HIG info current?" | stay here | §4 |

Composition rules:
- With the `prototype` skill on an Apple-native target: hig-design's constraint sheet loads **before** generation; one combined checklist pass across all options after.
- With ui-craft on an HTML prototype of native UI: ui-craft owns web mechanics, this suite owns native idiom and metric values; **on conflict, HIG wins** for native-targeting prototypes.

## 2. Hot numbers (hop-zero crib)

Verified against the snapshot; each value's authoritative home is in `references/tables/`. If `versions.md` is past expiry, re-verify hot rows before asserting.

| Spec | iOS/iPadOS | macOS | src |
|---|---|---|---|
| Control hit target — default / minimum | 44×44pt / 28×28pt | 28×28pt / 20×20pt | tables/accessibility-sizes.md |
| Padding around interactive elements | 12pt bezeled / 24pt bezel-less | same | tables/accessibility-sizes.md |
| Body text — default / minimum | 17pt / 11pt | 13pt / 10pt | tables/dynamic-type.md |
| Text contrast (WCAG AA) | 4.5:1; 3:1 ≥18pt or bold | same | tables/accessibility-sizes.md |
| App icon source | 1024×1024px, layered, six appearances | same | corpus/foundations-identity.md#app-icons |
| Menu bar height | — | 24pt | corpus/components-menus-actions.md#the-menu-bar |
| Alert buttons | ≤3 (more → action sheet) | ≤3 | corpus/components-presentation-status.md#alerts |
| Toolbar title | <15 characters | <15 | corpus/components-menus-actions.md#toolbars |
| Ratings prompts | ≤3 per 365 days | same | checklists/review-compliance.md |
| Sign in with Apple button | ≥140×30pt, exact titles/styles | same | tables/brand-buttons.md |
| Tooltip copy | — | 60–75 chars, sentence case, no period | checklists/review-copy.md |
| Default iPhone canvas (Sept-rot risk) | 402×874pt | — | corpus/foundations-layout-typography.md#layout |

Tab/nav bar heights are **no longer published** by Apple — never invent them; see `tables/metrics.md` for provenance-marked estimates.

## 3. Lookup protocol

1. Open `references/index.md` (≤2K tokens) → classify the slug: **corpus section** (note file + anchor, → step 2), **API symbol** (glassEffect, UISheetPresentationController, … — note the target slug, → step 2), or **live-fetch-only** (niche topics, no corpus section, → step 4).
2. `grep -n "^## <slug>" references/corpus/<file>.md` → `Read` that file with `offset` at the match, `limit` ≈ section length (sections are 5–80 lines). Do not read whole corpus files for one question. If the loaded section names another slug as load-bearing for *this* answer, load that one section too — one hop max.
3. Answer with the exact value/term, citing slug + change date from the section's `src:` line. State iOS and macOS separately when they differ — never "generally".
4. If the slug is live-fetch-only, the section is a stub, the topic is in `versions.md`'s hot list, or the snapshot is expired: fetch live — `scripts/hig-fetch.sh <slug>`. If fetch is unavailable (sandbox/denied), answer from the snapshot **and say so**: "per snapshot 2026-06-10; live verification unavailable here."

## 4. Currency protocol

- `references/versions.md` carries the snapshot date and expiry dates (Apple ships changes ~June/September/December). Past expiry → attach a staleness caveat to volatile answers, and offer to run `scripts/hig-whats-new.sh`.
- `hig-whats-new.sh` diffs Apple's changelog against the snapshot and lists changed pages **and** derived reference files needing review (via `src:` tags). A parse failure exits loudly — treat exit 2 as "unknown", never "no changes".
- Full refresh procedure: `scripts/refresh-workflow.md`.

## 5. Integrity rules

Cite exact values — never approximate. Never flatten platform differences. Every assertion traces to a corpus section (slug + date) or a live fetch. Numbers Apple doesn't publish are labelled with provenance and confidence. iOS/macOS 27 content is beta — keep it in delta blocks, version-gate it in answers. Mark uncertainty explicitly.
