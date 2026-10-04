---
name: design-with-apple-hig
description: Apply and verify current Apple Human Interface Guidelines for design, implementation, review, scoring, refactoring, and audit. Use for iOS, iPadOS, macOS, watchOS, tvOS, visionOS, SwiftUI, UIKit, AppKit, Liquid Glass, SF Symbols, Dynamic Type, VoiceOver, accessibility, screenshots, prototypes, or Apple-inspired Web and cross-platform interfaces. Retrieve current Apple primary guidance, preserve Apple wording strength and platform scope, route only necessary specialist skills, separate official requirements from SDK facts, standards, observations, audit-tool signals, and heuristics, and re-verify implemented changes.
---

# Apple HIG Design Skill

Direct Apple-platform design work from current primary evidence. Use third-party skills as bounded specialists, never as the authority. Preserve the difference between Apple-native alignment and Apple-inspired design on other platforms.

## Run the evidence-first workflow

1. Classify the task as `explain`, `design`, `build`, `review`, `score`, `refactor`, or `audit`.
2. Identify target platform and OS range, framework, artifact, input methods, requested depth, and testable states. Infer clear facts; ask only when the answer changes navigation, input, or implementation architecture.
3. Read [source-routing.md](references/source-routing.md). Build the smallest evidence bundle that can decide the task.
4. Read the relevant section of [official-source-map.md](references/official-source-map.md). Retrieve current Apple pages for every material, exact, version-specific, or normative claim. Use `scripts/fetch_apple_hig.py` when the HTML page is JavaScript-only.
5. Read only the applicable platform section in [platform-routing.md](references/platform-routing.md). Do not flatten platform differences.
6. Form a concise design contract: purpose, hierarchy, navigation, primary action, input, density, adaptation, appearance, accessibility, motion, privacy, localization, and recovery.
7. Design, implement, or review. Prefer system behavior and semantics over visual imitation.
8. For formal review or scoring, read [review-rubric.md](references/review-rubric.md). Lead with observable task and safety issues.
9. For code changes or runnable UI, execute [verification-loop.md](references/verification-loop.md). Re-test failed and high-severity paths after changes.

Read [bibliography.md](references/bibliography.md) only when updating this skill, evaluating a third-party source, explaining provenance, or auditing source quality.

## Preserve source meaning

Keep Apple guidance at its original strength:

- Treat `required`, `must`, API availability, safety constraints, and platform-enforced behavior as requirements only when the current primary source supports that strength.
- Preserve `prefer`, `consider`, `generally`, `if`, and `avoid` as conditional guidance. Do not rewrite them as `always` or `never`.
- Treat measurements with their component, platform, input, and OS scope. A general target is not automatically a release-blocking minimum everywhere.
- Treat the HIG as design guidance, SDK documentation as implementation fact, App Review Guidelines as distribution policy, and WCAG or another standard as a separate normative source.
- When Apple gives a principle without a number, do not invent a grid, breakpoint, page count, timing, score, or threshold.

If evidence conflicts, prefer the current platform-specific Apple page, then current SDK behavior, then accessibility-preserving system behavior. State unresolved conflicts and dates rather than silently choosing.

## Label material claims

Use these labels in formal reviews and evidence ledgers:

- `APPLE-HIG`: current Apple HIG or Apple Design guidance.
- `APPLE-SDK`: current Apple framework documentation or observed platform behavior.
- `APPLE-RESOURCE`: official design kit, template, symbol, or asset guidance.
- `ACCESSIBILITY`: an applicable accessibility standard, API, or assistive-technology test.
- `OBSERVATION`: visible or reproducible in the supplied artifact.
- `AUDIT`: a static or automated tool signal requiring confirmation.
- `HEURISTIC`: a reasoned recommendation that is not an Apple requirement.

For `APPLE-*` and `ACCESSIBILITY` findings, retain the page URL and retrieval date. For exact values, retain the surrounding scope or section.

## Route specialist skills narrowly

Use another installed skill only when it materially contributes. Read its `SKILL.md` first and follow host announcement rules.

- Use frontend-design or a site-building skill to implement substantial Web UI; keep this skill responsible for Apple-versus-Web boundaries and evidence.
- Use browser, Chrome, computer-use, or Playwright skills to inspect screenshots, responsive states, focus, keyboard operation, and live behavior.
- Use repository-native build, preview, test, snapshot, and accessibility tooling for Apple implementations.
- Use HIG Doctor for code-detectable candidates only. Classify every result and never equate a clean scan with HIG compliance.
- Use a distilled HIG corpus only for topic discovery. Re-fetch Apple primary sources before adopting its values or wording.
- Use motion-specialist guidance for direct manipulation, continuity, and implementation ideas; label transferred values and Web physics as heuristics unless Apple currently specifies them.

Do not load every specialist or a full HIG corpus. A normal bundle is one platform overview, one to four relevant HIG topics, one framework/API page, and one applicable accessibility page. Add current Design/WWDC updates for new OS, beta, Liquid Glass, or changed-component work.

## Preserve platform boundaries

- Describe verified Apple-platform work as `HIG-aligned`, with coverage limits; do not promise total compliance.
- Describe Web, Android, and generic cross-platform output as `Apple-inspired`, never HIG-compliant.
- Share domain logic, content models, and brand tokens. Adapt navigation, windows, commands, density, input, materials, and accessibility semantics to each host platform.
- Prefer standard controls and semantic values. Customize only when the product value exceeds losses in familiarity, accessibility, and OS adaptation.
- Express branding through content, composition, imagery, and restrained styling before replacing platform behavior.

## Respect artifact limits

- A screenshot can establish visible hierarchy, density, typography, color, targets, and one state. It cannot establish motion, focus or reading order, Dynamic Type, VoiceOver, or end-to-end behavior.
- Source code can establish implementation choices and reachable paths, but not final rendering or assistive-technology output without execution.
- A build, static scan, simulator screenshot, or single device never establishes ship readiness by itself.
- Score only verified dimensions and disclose the denominator. Any Critical finding makes the result `not ship-ready` regardless of arithmetic score.

## Protect rights and integrity

- Link to Apple primary material; do not bundle a copied or distilled HIG corpus.
- Keep repository code licenses separate from rights in Apple text and assets.
- Check the applicable license before distributing Apple Design Resources, fonts, SF Symbols exports, templates, imagery, or third-party text.
- Do not sacrifice clarity, accessibility, performance, or platform behavior for Liquid Glass, translucency, blur, or animation.

## Deliver the result

For design or implementation, provide the design contract, platform decisions, source ledger, changes, verification, and remaining limits.

For review or audit, order findings by severity. Include `Finding`, `Severity`, `Evidence`, `Source`, `Impact`, `Fix`, and `Verify`. Separate confirmed issues, contextual judgments, false positives, and unverified areas. Place citations beside the claims they support.
