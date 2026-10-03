---
name: perf-audit
description: Scan the codebase for React Native performance antipatterns and report ranked findings. Use for a performance review, a slow app, or a perf audit before release.
argument-hint: "[path to focus on]"
---

Audit the codebase (or the path in `$ARGUMENTS`) for the React Native performance antipatterns that actually matter. Read-only: report, do not edit.

Hunt for these, in priority order:

1. **Lists**: ScrollView wrapping `.map()` over data of meaningful size; FlatList/FlashList with inline arrow `renderItem`; missing or index-based `keyExtractor`; list images without fixed dimensions.
2. **Subscriptions**: components subscribing to whole stores (`useStore()` with no selector, or selectors returning fresh objects); context providers bundling fast-changing values with static ones.
3. **Render work**: heavy computation directly in render without memoization; date/number formatting per row per render; JSON.parse of large payloads on the interaction path.
4. **Animations**: setState driving per-frame animation; runOnJS inside gesture or frame callbacks; PanResponder where gesture-handler belongs; animating layout properties instead of transform/opacity.
5. **Startup**: heavy SDK/analytics initialization at module top level; barrel imports that pull the world into the entry file; synchronous storage reads before first render.
6. **Leftovers**: console.log in hot paths that ship to release; dev-only tooling imported unconditionally.

Method: grep for the patterns, then READ each hit before reporting it. A ScrollView over four static children is fine; the same over a fetched array is a finding. Judgment beats pattern-matching, and false accusations burn the reader's trust in the whole report.

Report format:
- Ranked findings, worst first. Each: `file:line`, the pattern, why it costs here specifically, and the one-line direction of the fix.
- Skip theory. No finding, no entry; an honest "lists are clean" beats padding.
- Close with the top three fixes worth doing this week. Verification means re-measuring in a release build, not eyeballing the simulator; say so at the end of the report.
