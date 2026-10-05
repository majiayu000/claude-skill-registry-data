---
name: hig-review
description: Audit designs, prototypes, or code against Apple's Human Interface Guidelines. Use for Apple-marked review asks — "is this HIG compliant", "review my iOS app", "review my Mac app", "does this feel native", "would Apple reject this", "check this against the HIG" — or when reviewing SwiftUI UI code, an HTML prototype that imitates native Apple UI, or Figma frames built on Apple's kits. Covers screens, flows, copy, accessibility, Liquid Glass usage, system surfaces (widgets, Live Activities, notifications), and App-Review-enforced rules. Model priors on Apple's design system are stale (Liquid Glass era) — never judge native correctness from memory. Does NOT fire on unmarked "review my prototype/UI" for web apps (use ui-craft or interface-craft); web mechanics of HTML prototypes stay with ui-craft — this skill owns native idiom and metric values.
---

# HIG Review

Audit process for Apple-platform work. Shared references live at `../hig/references/` (sibling install).

**Judge against the references, not your priors.** Your training data predates Liquid Glass; what looks wrong to you may be current (floating tab bars, layered icons) and what looks fine may be dead (opaque bars, hamburger menus on iOS).

---

## 1. Severity tiers — every finding carries one

1. **Rejection risk** — rules App Review objectively enforces (privacy permission screens, Sign in with Apple / Apple Pay brand specs, account deletion, ratings-prompt caps, marketing-notification rules, minimum-functionality signals). Only `checklists/review-compliance.md` items may use this tier.
2. **Feels broken** — real usability failures: illegible glass, missing Dynamic Type, hit targets under minimum, gesture conflicts, missing loading/empty/error states.
3. **Feels non-native** — platform-idiom drift: web controls on iOS, incomplete macOS menu bar, wrong icon for action, stale terminology.

**Never claim Apple will reject for tiers 2–3.** Most HIG violations never block App Review; saying otherwise destroys trust. Tag tier-2/3 judgment findings with the relevant design principle from `../hig/references/doctrine.md` (e.g. *Familiarity*, *Maintain your craft*) — Apple's vocabulary, not taste.

## 2. Process

1. **Identify medium and platform(s).** Load the matching adapter (`../hig/references/adapters/html.md` / `figma.md` / `swiftui.md`) — note its **cannot-verify list** now; you'll report against it.
2. **Triage surfaces present:** screens · flows · copy · accessibility · Liquid Glass surfaces · system surfaces (widgets/Live Activities/notifications) · compliance-sensitive features (auth, payments, tracking, ratings, subscriptions).
3. **Code media only:** run `../hig/scripts/hig-scan.sh <path> <medium>` first. Its output is **candidates, not findings** — judge every line against the checklists; suppress false positives (look for compliance markers).
4. **Checklist pass.** Load only the checklists for surfaces present: `review-screen-ios.md` / `review-screen-macos.md` (self-sufficient composites), then as triaged: `review-flow.md`, `review-copy.md`, `review-a11y.md`, `review-liquid-glass.md`, `review-system-surfaces.md`, `review-compliance.md`. For targeted asks ("just check accessibility"), load only that checklist.
5. **Judgment pass.** Beyond the checklists: does the screen respect the two-layer model, platform character, and component semantics? The checklists are self-sufficient — open the corpus only for **contested** findings, and read sections, never whole files: `grep -n "^## <slug>" ../hig/references/corpus/<file>.md` → Read with offset/limit at the match. Budget the whole audit at roughly two checklists + adapter + a handful of corpus sections; if you're reading a fifth corpus file, you're re-deriving what the checklist already encodes.
6. **Flow honesty.** Static screens can't show state machines (first-run order, drag lifecycle, undo visibility, interruptions). If you only saw statics, say which flow checks were not performed.

## 3. Finding format

```text
[tier] [principle (tiers 2–3)] <what's wrong, with the exact value>
  spec: <expected> — <slug>, changed <date>
  fix: <in the user's medium: CSS for HTML, inspector steps for Figma, modifier for SwiftUI>
```

End every audit with: **Not verifiable in this medium:** <items from the adapter's cannot-verify list relevant to this artefact> — and, for Figma renders, tag estimated values "estimated from render — confirm in Figma inspector".

## 4. Verification limits by medium

| Medium | Trust | Never claim |
|---|---|---|
| HTML prototype | DOM/CSS values, structure, copy | swipe-back, rubber-banding, detent feel, real glass refraction |
| Figma via MCP | layout judgment from thumbnails | any exact pt value — view_node returns images, not geometry |
| SwiftUI code | API usage, modifiers, structure | runtime rendering (simulator ≠ hardware for glass) |
| Screenshots | visible idiom, hierarchy, copy | anything interactive or off-screen |

## 5. Integrity rules

Exact values with citations (slug + change date); never approximate; never flatten platforms. Check `../hig/references/versions.md` expiry — if expired, verify hot-page claims live (`../hig/scripts/hig-fetch.sh <slug>`) or attach a staleness caveat. If a fetch fails, report with the stale value PLUS the caveat — never bare. Findings on 27-beta behaviour are version-gated.
