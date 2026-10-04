---
name: swiftui-animation-match
description: Match UI/UX interaction needs to proven SwiftUI animation patterns from curated open-source catalogs. Use when planning or building iOS/macOS screens where an interaction should feel alive - loaders, likes, toggles, card decks, reveals, shaders - or when asked which animation fits a moment. Recommends system-first restraint before custom motion.
---

# SwiftUI Animation Match

Use this skill to turn a vaguely felt interaction wish ("saving should feel
more satisfying", "this list is boring while it loads") into a concrete,
proven SwiftUI animation pattern — or into the deliberate decision to use
what the system already provides.

The skill is a matcher, not a snippet dump. Its value is the judgment step:
name the interaction moment first, check what the OS gives you for free,
and only then reach into the cataloged sources for custom motion that earns
its place. Animations add juice that makes a product feel human; forcing
one where the platform already shines makes it feel worse.

## First move

1. Name the moment. Translate the request into: what is the user doing,
   what should they feel, and how often does this happen? Read
   [references/matching-playbook.md](references/matching-playbook.md) —
   it has the moment taxonomy and the system-first checklist.
2. Decide system vs custom. If a system affordance covers the moment
   (Liquid Glass chrome, `.symbolEffect`, springs, `.contentTransition`,
   zoom navigation transitions, `.sensoryFeedback`), prefer it and stop.
3. If custom motion earns its place, search the catalogs (below) by
   interaction pattern and keywords, not by animation name.
4. Adapt, never paste. Every catalog entry has lift notes and each catalog
   ends with a lift checklist (dependencies to replace, old patterns to
   modernize, Reduce Motion).
5. Verify in motion. Build and watch it in Previews or Simulator; motion
   cannot be judged from code. If the app repo has build/test skills
   (for example `bootstrap-ios`), use them.

## Catalogs

Load only the catalog you need; entries are grouped by interaction moment
and carry keywords, exact source paths, technique summaries, and lift notes.

| Catalog | Contents |
|---|---|
| [catalog-shubham0812-swiftui-animations.md](references/catalog-shubham0812-swiftui-animations.md) | 30 SwiftUI animations + 7 Metal shaders: loaders, progress, action feedback, toggles, card decks, text heroes, input chrome, reveals, shader effects |

The source index with pinned commits and licenses is in
[references/sources.md](references/sources.md).

## Mode picker

| The product needs... | Look at |
|---|---|
| An indeterminate wait that feels crafted | Catalog: Wait states |
| Progress with a real percentage | Catalog: Progress with a real percentage |
| A tap that confirms, celebrates, or completes async work | Catalog: Action feedback and confirmation |
| A switch or mode change with personality | Catalog: Toggles and switches with identity |
| Browsing cards, decks, or carousels by gesture | Catalog: Cards and gesture-driven browsing |
| A hero headline or onboarding moment | Catalog: Text and hero moments |
| Composer / input chrome with delight | Catalog: Input chrome |
| An unlock, reveal, or brand easter egg | Catalog: Reveals and brand delight |
| Destroy, error, or premium image treatment | Catalog: Metal shader effects |
| "Which animation fits X?" during planning | [matching-playbook.md](references/matching-playbook.md) first, then the catalog |
| Add a new animation repo to this skill | [adding-a-source.md](references/adding-a-source.md) |

## Restraint rules

- One signature motion moment per screen. Everything else stays quiet.
- Frequency caps intensity: high-frequency interactions get subtle, short
  motion (or system defaults); rare moments may be theatrical.
- Do not re-skin system chrome that already animates well (tab bars,
  toolbars, sheets, Liquid Glass surfaces). Custom motion belongs in
  content, not in the platform's chrome.
- Honor Reduce Motion with a crossfade or reduced variant.
- Keep one motion vocabulary per app: consistent spring feel, consistent
  duration scale. A catalog entry adopted verbatim into a calm app will
  feel foreign until its curves are tuned to match.

## Adaptation posture

The catalogs describe working code from real repos, including its age. Keep
the load-bearing geometry (shapes, trim windows, offset math, shader
kernels) and modernize the plumbing:

- Timer state machines -> `.phaseAnimator`, `.keyframeAnimator`,
  `withAnimation` completion handlers, or `Task.sleep`.
- UIKit haptic wrappers -> `.sensoryFeedback`.
- Hardcoded screen bounds -> `GeometryReader` / container sizing.
- Demo colors, fonts, and assets -> the app's design tokens.
- Fake timer-driven progress -> real async work.

## Extending the skill

This skill is built to grow: each new animation repo becomes one catalog
reference file following the same entry format, registered in
`sources.md` and the catalog table above. The repeatable recipe — including
how to fan out parallel readers over a big repo and the exact entry
template — is in [references/adding-a-source.md](references/adding-a-source.md).
