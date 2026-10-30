---
name: ui-states
description: >
  Design all 7 UI states for any data-dependent view: empty, loading, skeleton,
  partial, complete, error, offline. Use when asked about "loading state",
  "skeleton screen", "error message", "empty state", "optimistic UI", "what
  happens while data loads", or before marking any data-dependent view as done.
  Every view that fetches data must pass all 7 states before ship.
origin: adapted:ux-ui-mastery
license: MIT © phazurlabs
version: 1.0.0
compatibility: "Any frontend stack. Framework-agnostic patterns."
---

<!-- Adapted from phazurlabs/ux-ui-mastery (MIT) — Performance States Patterns skill.
     7-state lifecycle, perceived performance pillars, audit checklist.
     YAMTAM structure, Anti-Fake-Pass gate, and condensed format are original. -->

## When to Use

- Use when: building any component that loads data from an API or async source
- Use when: a view shows a blank screen, spinner, or broken layout during load
- Use when: error messages are technical or give no recovery path
- Use when: pre-ship checklist for any data-dependent screen

---

## The 7-State Lifecycle

Every data-dependent view must handle all 7. Missing states are bugs, not edge cases.

| State | What it is | Design goal |
|---|---|---|
| **Empty** | No content yet — brand new account, cleared list | Guide and motivate — "what do I do first?" |
| **Loading** | Request in flight, duration unknown | Reassure — something is happening |
| **Skeleton** | Placeholder shapes matching content layout | Reduce perceived wait — structure before data |
| **Partial** | Some data arrived, rest still loading | Progressive enhancement — must look intentional |
| **Complete** | All data loaded, all interactions available | Happy path — the designed state |
| **Error** | Something failed: network, auth, validation, rate limit | Recovery — tell what, why, and what to do next |
| **Offline** | Network lost | Graceful degradation — cached content + queue writes |

---

## Per-State Rules

### Empty
Two types — design both separately:
- **First-use empty**: answers "What is this?" + "What do I do first?" → illustration + explanation + primary CTA
- **No-results empty**: search/filter matched nothing → suggest how to broaden, never just "No results"

### Loading
- Brief wait (< 1s): simple spinner is acceptable
- Content-heavy view: skeleton screen preferred — never blank white
- ARIA: `aria-live="polite"` region to announce loading to screen readers

### Skeleton
```css
/* Pulse animation — matches content dimensions exactly */
.skeleton {
  background: linear-gradient(90deg, #e0e0e0 25%, #f0f0f0 50%, #e0e0e0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s ease-in-out infinite;
}
@keyframes shimmer {
  0%   { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
/* Stagger skeleton groups 50ms apart */
```
Rules: match exact dimensions of real content. Never show more skeleton items than will actually appear.

### Optimistic UI
Show the expected result immediately — don't wait for server confirmation.
On failure: smoothly revert + show error toast. Never silently swallow errors.
Use for: like/unlike, follow/unfollow, send message, mark complete.

### Error
Three-part requirement — all three are mandatory:
1. **What happened** (plain language — no error codes, no stack traces)
2. **What it means for the user**
3. **What to do next** (retry button, contact support link, or alternative path)

Additional rules:
- Preserve user input — never clear a form on error
- Show cached/stale data with a staleness indicator when available
- Retry button for transient failures (network, timeout, rate limit)

### Offline
Offline is a state, not an error. Required:
- Clear disconnection indicator
- Show cached content where available (mark as "last updated X ago")
- Queue write actions silently, sync on reconnect
- Indicate queued actions: "Will send when connected"

---

## Perceived Performance — Three Pillars

Speed users *feel* matters more than speed they can measure:

1. **Immediate feedback** — acknowledge every action within 100ms (even if just a spinner appearing)
2. **Visual continuity** — maintain spatial relationships during transitions so the brain can track changes
3. **Progressive disclosure** — show something useful as early as possible, then enhance

> A 3s load that *feels* fast (skeleton + progressive render) beats a 2s load that *feels* slow (blank then content dump).

---

## Audit Checklist

For every data-dependent view before ship:

```
□ First-use empty state — illustration + explanation + CTA
□ No-results state — helpful suggestion, not just "no results"
□ Loading state — spinner or skeleton chosen appropriately
□ Skeleton matches real content dimensions
□ Partial state looks intentional, not broken
□ Complete (happy path) — fully designed
□ Error state — 3-part message (what / means / do next) + retry
□ Offline state — cached content shown, writes queued
□ ARIA live region on loading indicator
□ Optimistic UI: failure reverts visibly with error feedback
```

---

## Anti-Fake-Pass Rules

Before claiming a view is done, you MUST show:
- [ ] All 7 states identified — none marked "not applicable" without reason
- [ ] Empty state: first-use AND no-results designed separately
- [ ] Error state: shows what happened + what to do (not just a red banner)
- [ ] Offline state: cached content strategy stated
- [ ] ARIA live region present on loading indicator

Reference: `gates/anti-fake-pass-gate.md` | `gates/ui-quality-gate.md`
