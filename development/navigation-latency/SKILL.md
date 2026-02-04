---
name: navigation-latency
description: Measure time from navigation tap to screen fully loaded and interactive. Use when tracking screen transitions, deep links, or tab switches.
triggers:
  - "deep link performance"
  - "measure TTI"
  - "screen load time"
  - "slow screen navigation"
  - "tab switch latency"
  - "track screen transitions"
priority: 2
---

# Navigation Latency

Time from tap to destination screen interactive (TTI).

## Phases

```
TAP → TRANSITION → VIEW_INIT → DATA_LOAD → INTERACTIVE
     |_____________________________________________|
                   Navigation Latency
```

## When to Use

- Tab bar taps
- List item → detail screen
- Deep link → target screen
- Any screen-to-screen transition

## Key Thresholds

| Rating | Duration |
|--------|----------|
| Good | <400ms |
| Acceptable | <1s |
| Poor | >1s |

## Measurement Points

1. `onNavigationStart` - user taps (source screen)
2. `onViewAppear` - destination view visible
3. `onContentReady` - data loaded, interactive

## Implementation

See `references/ui-performance.md` (Navigation Latency section) for:
- iOS: NavigationLatencyTracker with os_signpost
- Android: Fragment/Activity lifecycle hooks
- React Native: React Navigation listeners

## Common Mistakes

- Measuring only view appear (missing data load)
- Not correlating source → destination
- Ignoring warm vs cold screen loads

## Related Skills

- See `skills/interaction-latency` for button/tap response times (vs full screen loads)
- Combine with `skills/user-journey-tracking` to correlate navigation with user intent
