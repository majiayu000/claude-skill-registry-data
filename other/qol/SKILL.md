---
name: qol
description: Quality-of-life audit and polish for any app surface. Finds invisible friction, missing native behaviors, and UX gaps using a 10-category framework, 10 organization laws, and ChefFlow-specific compound patterns drawn from 10 games, 15 service platforms, and 10 best-organized websites/apps in the world. Use when user says "QoL", "quality of life", "polish", "make it feel better", "overhaul", "clean up the UX", or describes wanting a surface to feel more refined.
---

# QoL: Quality of Life

Not new features. Native behavior that should already work. Missing QoL = bug, not nice-to-have.

Core principle: quality measured by what DISAPPEARS from the user's cognitive load.

## Phase 1: Audit (10-Category Framework)

Read the target surface. Score each category PASS / WEAK / FAIL.

These categories come from studying how top game studios (Larian, FromSoft, ConcernedApe, GGG, Blizzard, Mojang) and product teams (Linear, Figma, Notion, Shopify, Stripe, Slack, Discord, Vercel) continuously polish their products, plus ChefFlow-adjacent service platforms (HoneyBook, Dubsado, Jobber, Housecall Pro, Toast, Calendly, FreshBooks, Intercom, CaterZen, Galley, Tripleseat).

| #   | Category                 | What It Means                                                                                  | Check                                                                                                                                                               |
| --- | ------------------------ | ---------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | **Indicator Clarity**    | Surface state changes visually/audibly. Never force users to hunt for what changed.            | New items marked? Status transitions visible? Completion progress shown? Badge counts accurate? Toast/feedback on mutations?                                        |
| 2   | **Accident Prevention**  | Stop users from destroying their own work.                                                     | Destructive actions confirm? Unsaved changes warned? Undo available? Bulk deletes require extra intent? Immutable records protected?                                |
| 3   | **Click Reduction**      | Fewer steps for routine actions. Every extra click on a daily task compounds into frustration. | Common actions reachable in 1-2 clicks? Keyboard shortcuts for power users? Bulk operations where 5+ items? Smart defaults pre-filled? Auto-focus on primary input? |
| 4   | **Progress Compounding** | Never repeat finished work. Prior effort should accelerate future effort.                      | Templates from past work? Defaults learned from history? Cross-entity sharing (menus, recipes, ingredients)? Settings persist?                                      |
| 5   | **Context Preservation** | Keep info accessible without leaving flow. Kill the alt-tab.                                   | Related data visible in-context? No dead-end pages? Back button goes where expected? Modals preserve scroll position? Breadcrumbs/navigation clear?                 |
| 6   | **Friction Removal**     | Cut mechanics that annoy without adding value. If it just irritates, remove it.                | Unnecessary confirmations? Redundant steps in flows? Loading screens that could be eliminated? Forced refreshes?                                                    |
| 7   | **Safe Defaults**        | Correct behavior without configuration. Works right out of the box.                            | New accounts land in useful state? Permissions sensible by default? Date/currency formats locale-aware? Timezone handled?                                           |
| 8   | **Accessibility**        | Works for all users, all input methods, all contexts.                                          | Keyboard navigable? Focus management correct? Color contrast sufficient? Touch targets 44px+? Screen reader labels? Error messages specific?                        |
| 9   | **Performance Feel**     | Invisible speed gains. User doesn't know what changed, just feels faster/smoother.             | Optimistic updates? Skeleton loaders (not blank space)? No layout shift? Smooth animations on state changes? Prefetching likely next actions?                       |
| 10  | **Recovery**             | Graceful handling of mistakes and failures.                                                    | Failed loads show error states (not $0.00 or empty)? Retry available? Draft auto-saved? Session survives refresh? Clear path back from errors?                      |

### Scoring

- **8-10 PASS:** Surface is polished. Minor tweaks only.
- **5-7 PASS:** Needs targeted work. Fix FAIL categories.
- **Under 5 PASS:** Full overhaul. Prioritize categories 1-3 first.

Report score table. Get user buy-in before building.

## Phase 1a: Organization Laws Check

After the 10-category audit, check these 10 organization laws. Extracted from the best-organized digital products in the world (Stripe, Apple, GOV.UK, Notion, Linear, Superhuman, Airbnb, Duolingo, Arc, Wikipedia).

| #   | Law                                   | Rule                                                                            | Check                                                                                         |
| --- | ------------------------------------- | ------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| 1   | **Name things what they are**         | No brand jargon in navigation. Plain words. (Stripe)                            | Every nav item and label uses plain language the chef already knows?                          |
| 2   | **5 items max in primary nav**        | More than 5 = decision paralysis. Group the rest. (Apple)                       | Primary nav has 5 or fewer items? Secondary items accessible but not competing?               |
| 3   | **Hide until needed**                 | Show minimum viable info. Reveal depth on demand. (Notion, Apple)               | Details hidden behind progressive disclosure? No info-dump on first view?                     |
| 4   | **One question per dashboard**        | First screen answers: "Is everything okay?" (Linear, Vercel)                    | Dashboard has a clear primary status? Not 12 competing widgets?                               |
| 5   | **Speed IS organization**             | Sub-100ms interactions eliminate need for wayfinding. (Superhuman)              | Page transitions instant? Cached data serves immediately? No loading spinners for local data? |
| 6   | **Color = meaning, consistently**     | Every color maps to ONE semantic meaning across entire app. (Duolingo)          | Green always = good, red always = problem, amber always = attention? No decorative color?     |
| 7   | **Consistent templates at scale**     | Every entity of same type follows same structural template. (Wikipedia, GOV.UK) | All dinner pages have same section order? All client pages same layout?                       |
| 8   | **Cross-link everything**             | Every entity is a portal to related entities. Never a dead end. (Wikipedia)     | Click ingredient -> recipes using it? Click client -> their dinners? No orphan pages?         |
| 9   | **Separate contexts, never mix**      | Different work modes get different spaces. (Arc)                                | Dinner prep context vs. client communication context vs. financial context stay clean?        |
| 10  | **Force decisions, don't accumulate** | Act on each item: do, defer, dismiss. No growing backlog. (Superhuman)          | Inquiry inbox forces response/defer/decline? No items silently aging without action?          |

Score as PASS / WEAK / FAIL. Any FAIL on a core surface = P0 structural issue (fix before cosmetic QoL).

## Phase 1b: ChefFlow Compound Pattern Check

After the 10-category audit, check these ChefFlow-specific patterns. Each appeared across 3+ similar service platforms and represents behavior chefs expect from an operational tool.

| Pattern                        | What To Check                                                                                                                          | Learned From                          |
| ------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------- |
| **Cascading State**            | Does completing/archiving an entity update all related entities? (Close dinner -> close invoices, pause workflows, archive comms)      | HoneyBook, Dubsado, Tripleseat        |
| **Communication Omnipresence** | Can the chef message a client from ANY context (dinner view, menu view, invoice view), not just the inbox?                             | Housecall Pro, Intercom, HoneyBook    |
| **Silent Resilience**          | Do failed uploads/syncs retry automatically without user action? Does the app work offline for critical actions?                       | Housecall Pro, Jobber, Wave           |
| **Historical Intelligence**    | Does past event data accelerate future event creation? Templates, learned defaults, "repeat last September's dinner"?                  | Tripleseat, CaterZen, Monday.com      |
| **Client Self-Service**        | Can clients do things without back-and-forth? (View menu, confirm dietary info, see timeline, pay)                                     | Calendly, Tripleseat, Square          |
| **Financial Paper Trail**      | Is every price change, payment, and adjustment logged with who/when/why?                                                               | FreshBooks, CaterZen, Dubsado         |
| **Smart Stop**                 | Do automated sequences (Remy emails, reminders) stop when the goal is met? (Client responded -> stop follow-ups)                       | Housecall Pro, HoneyBook, Mailchimp   |
| **Mobile Action Parity**       | Can the chef do critical actions from their phone? (Send invoice, reply to inquiry, check tonight's menu)                              | FreshBooks, Jobber, Square, Mailchimp |
| **Template-First Creation**    | Does creating a new entity start from a good default/template, not a blank form?                                                       | Mailchimp, Tripleseat, Galley         |
| **Receipt-to-Cost Pipeline**   | Can the chef capture a receipt and have it flow into food costing automatically? (Photo -> extract -> assign to dinner -> update cost) | Wave, FreshBooks, Galley              |

Score these as WIRED / PARTIAL / MISSING. Any MISSING pattern on a core surface = P1 work.

## Phase 2: Build

### Priority order

Fix in this order (highest user impact per effort):

1. **Recovery** (broken states hurt trust most)
2. **Indicator Clarity** (users lost = users frustrated)
3. **Accident Prevention** (data loss = unforgivable)
4. **Click Reduction** (daily compound pain)
5. **Cascading State + Financial Paper Trail** (data integrity)
6. **Everything else** by FAIL score

### Canonical patterns

#### Collapsible sections

```tsx
<button className="group flex w-full items-center gap-3 py-2 px-1 ...">
  <ChevronDown className={`transition-transform duration-200 ${collapsed ? '-rotate-90' : 'rotate-0'}`} />
  <span className="text-[11px] font-semibold uppercase tracking-widest">{label}</span>
  {collapsed && summary && <span className="ml-auto text-xs truncate">{summary}</span>}
</button>

<div className="grid transition-[grid-template-rows] duration-200 ease-in-out"
     style={{ gridTemplateRows: collapsed ? '0fr' : '1fr' }}>
  <div className="overflow-hidden">{children}</div>
</div>
```

#### State persistence

- Use `useCollapsedWidgets(storageKey)` hook (`lib/hooks/use-collapsed-widgets.ts`)
- Storage key convention: `cf:{surface}-{feature}` (e.g., `cf:dashboard-sections-collapsed`)

#### Layer dividers

```tsx
<div className="flex items-center gap-3 pt-4 pb-1">
  <div className="h-px flex-1 bg-stone-800/50" />
  <span className="text-[10px] font-medium uppercase tracking-widest text-{color}-500/60">
    {label}
  </span>
  <div className="h-px flex-1 bg-stone-800/50" />
</div>
```

#### Indicator patterns

- Toast on every mutation (success AND failure)
- Badge counts on nav items with pending actions
- `!` or dot indicators on new/changed items
- Completion percentage bars on multi-step entities

#### Click reduction patterns

- Auto-focus first input on page/modal load
- Keyboard shortcuts for top 5 daily actions
- "Collapse All / Expand All" for 5+ collapsible items
- Smart defaults from last-used values

#### Cascading state pattern

- One action (archive/complete/cancel) triggers all downstream updates
- Use server action that handles the full cascade, not client-side chaining
- Log every cascaded change to audit trail
- Show summary toast: "Dinner archived. 3 invoices closed, 2 workflows paused."

#### Communication omnipresence pattern

- Every entity view (dinner, menu, invoice, client) has a "Message" action
- Opens pre-contextualized compose: subject, recipient, relevant details pre-filled
- Sent message logged on the entity AND the client record

#### Silent resilience pattern

- Wrap uploads/syncs in retry with exponential backoff
- Queue failed mutations for retry when connectivity returns
- Never show "failed" for something that can be retried automatically
- Only surface errors after 3+ silent retries fail

## Phase 3: Verify

- [ ] Every state change has visible feedback (toast, indicator, animation)
- [ ] Destructive actions require confirmation
- [ ] Failed loads show error states, not empty/zero
- [ ] Auto-focus on primary input field
- [ ] Collapsed/preference state persists after reload
- [ ] Back button returns to expected location
- [ ] No blank loading states (skeletons or spinners)
- [ ] Animations on show/hide transitions (no snap)
- [ ] Mobile: no overflow, touch targets 44px+, responsive layout
- [ ] Keyboard navigation works for primary flows
- [ ] Cascading actions update all related entities
- [ ] Communication accessible from entity context (not just inbox)
- [ ] Failed operations retry silently before surfacing errors
- [ ] New entity creation offers template/history-based defaults
- [ ] Financial changes logged with audit trail
- [ ] Typecheck clean

## Real-World Reference (Why This Framework Exists)

### Game Studios (Universal QoL)

| Source          | Lesson                                                             |
| --------------- | ------------------------------------------------------------------ |
| Elden Ring      | `!` icons on new items; dot when upgrade available. Surface state. |
| Stardew Valley  | Move while using tools; NPCs protect chests. Prevent accidents.    |
| Path of Exile 2 | One-click price check; in-game build guides. Kill the alt-tab.     |
| Helldivers 2    | Removed weather slowdown. Cut friction that adds no depth.         |
| WoW: War Within | Warband sharing across characters. Never repeat finished work.     |
| BG3             | Concentration warnings before casting. Prevent expensive mistakes. |
| Linear          | Opinionated defaults. Fewer settings, smarter behavior.            |
| Figma           | Links open without interrupting flow. Preserve context.            |
| Discord         | E2E encryption as default, not opt-in. Safe defaults.              |
| Slack           | VoiceOver fixes. Accessibility is QoL, not niche.                  |

### Service Platforms (ChefFlow-Adjacent QoL)

| Source        | Lesson                                                                                 |
| ------------- | -------------------------------------------------------------------------------------- |
| HoneyBook     | Skip one automation step without breaking the chain. Graceful override.                |
| Dubsado       | Archive project cascades: pauses workflows, closes invoices. One action, full cleanup. |
| Jobber        | Offline mode for field workers. Works without internet.                                |
| Housecall Pro | Chat on every page, not just inbox. Auto photo retry in bad signal.                    |
| Toast POS     | Card swipe auto-fills guest name. Zero-effort data capture.                            |
| Calendly      | Canceled items hidden by default. Clean default view.                                  |
| FreshBooks    | Period lock on finalized financials. Immutability when it matters.                     |
| Intercom      | AI follows multi-step procedures, not just answers questions. Structured workflows.    |
| CaterZen      | Cart abandonment alerts. Recover stale inquiries.                                      |
| Galley        | Recipe change propagates to all menus instantly. Single source of truth.               |
| Tripleseat    | Last year's event data templates this year's. Historical intelligence.                 |
| Square        | Drag-and-drop rescheduling on calendar. Direct manipulation.                           |
| Mailchimp     | Campaign stops when client takes action. Smart stop.                                   |
| Wave          | Receipt photo -> auto-categorize -> assign to job. Capture at source.                  |
| Monday.com    | Natural language builds dashboards. Describe what you want, get it.                    |

### Best-Organized Products (Organization Laws)

| Source      | Lesson                                                                                                      |
| ----------- | ----------------------------------------------------------------------------------------------------------- |
| Stripe      | No brand jargon. Products named what they do. Docs follow identical structure.                              |
| Apple.com   | 5 nav items max. Progressive depth via "Learn More." One purpose per page.                                  |
| GOV.UK      | 2,000 sites unified by design system. Content types as structural skeleton. Plain language mandate.         |
| Notion      | Hide complexity until needed. Sidebar accordion for hierarchy. Breadcrumbs for wayfinding.                  |
| Linear      | Dashboard answers one question: "Is everything okay?" Fixed sidebar scales to 50 features.                  |
| Superhuman  | Sub-100ms everything. One item at a time. Command palette from anywhere. Force decisions.                   |
| Airbnb      | Card-based browsing: photo + 4 key facts. Filters invisible until needed. Personalized defaults.            |
| Duolingo    | Color = meaning consistently. Micro-units of progress. One-tap to start. Instant feedback on every action.  |
| Arc Browser | Spaces separate contexts. Command bar searches everything. Auto-archive completed items.                    |
| Wikipedia   | Same template across millions of pages. Auto-generated TOC. Infobox for quick facts. Cross-link everything. |
