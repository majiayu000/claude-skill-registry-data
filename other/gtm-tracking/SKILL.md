---
name: gtm-tracking
description: Use when adding GTM analytics, tracking events, impressions, or click tracking to components - ensures consistent event shape, naming conventions, and correct implementation pattern
---

# GTM Event Tracking

## Overview

All GTM events use `sendGTMEvent` from `@next/third-parties/google`. Events follow a standard shape with four core fields plus optional domain-specific fields.

## Standard Event Shape

```ts
import { sendGTMEvent } from '@next/third-parties/google';

sendGTMEvent({
  event: 'click',                    // what happened
  eventGroup: 'search_expansion',    // feature/domain grouping
  section: 'search',                 // where in the page
  element: 'confirm_button',         // what was interacted with
  // + optional domain-specific fields
});
```

## Quick Reference

### Event Types

| `event` value | When to use |
|---|---|
| `click` | User clicks/taps an interactive element |
| `impression` | Element enters viewport |
| `contact` | User initiates contact (phone, email) |
| `form_submit` | Form submission |
| `swipe` | Carousel/swipe gesture |
| `virtual_pv` | SPA page navigation (handled by `GTMVirtualPageView`) |

### Existing `eventGroup` Values

Before creating a new group, check if one of these fits:

`search_expansion`, `stories`, `calculators`, `semantic_search`, `amenities`, `travel_time`, `credits`, `place_relation`, `odrednice`, `website_interactions`, `user_data`, `extended_search`

Some older events use `eventGroup: ''` — avoid this in new code.

### Naming Conventions

- `eventGroup`: `snake_case`, describes the feature domain
- `section`: `snake_case`, describes page area (e.g. `search`, `detalji_oglasa`, `kod_filtera`, `cenovnik`)
- `element`: `snake_case`, describes the specific UI element or action (e.g. `confirm_button`, `open_selection`)
- Domain-specific fields: `camelCase` (e.g. `amenityCategory`, `adId`, `searchCount`)

## Implementation Patterns

### Inline (default — use for 1-2 events)

Direct `sendGTMEvent()` call in an event handler:

```ts
const handleClick = () => {
  sendGTMEvent({
    event: 'click',
    eventGroup: 'your_feature',
    section: 'your_section',
    element: 'your_element',
  });
};
```

### Typed Tracker Module (use for 3+ distinct events)

Create a dedicated `track-{feature}.ts` file with discriminated union types. Reference implementation: `src/app/(base)/pretraga/[transactionType]/[[...otherSegments]]/_components/search-expansion/track-search-expansion.ts`

Pattern:
1. Define a `Payload` discriminated union (component-friendly names)
2. Define a `GTMEvent` discriminated union (exact GTM shape)
3. Write a mapper function between them
4. Export a single `trackFeatureName(payload)` function with try/catch

### Viewport Impressions

Use `ImpressionSenderWrapper` from `src/components/gtm/impression-sender-wrapper.tsx`:

```tsx
<ImpressionSenderWrapper
  event="impression"
  eventGroup="your_feature"
  section="your_section"
  element="your_element"
  unique  // only fire once
>
  {children}
</ImpressionSenderWrapper>
```

Note: this adds a wrapping `<div>` — be mindful of layout impact.

## Checklist Before Shipping

- [ ] Component is client-side (`'use client'` or guarded with window check)
- [ ] `eventGroup` reuses existing value or new value is justified
- [ ] All new field names use `snake_case` (section, element) or `camelCase` (domain fields)
- [ ] Impression events use `unique` flag if they should only fire once
- [ ] Events with 3+ variants use typed tracker module pattern
- [ ] GTM event shape is documented in the feature spec or PR description
