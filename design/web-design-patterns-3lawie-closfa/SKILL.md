---
name: web-design-patterns
description: Modern web application patterns — route-level data loading, streaming, cache invalidation, optimistic UI, cursor pagination, error/loading/empty states, form flows. Consult when building or refactoring any route, data flow, or user-facing interaction.
---

# Web Design Patterns

The app-flow rulebook: how data and interaction move through a modern web application. `/patterns` covers server conventions; this skill covers the web layer on top. When both apply, read both.

Read `learnings.md` beside this file before starting; append an entry when a flow rule needed adaptation for this stack.

## Governing Principle

> **The URL is the source of truth. Every view is linkable, every state is recoverable, every action gives feedback.** Users should never wonder "did that work?" or lose their place.

## Data Loading

- **Route loaders own initial data.** Data a page needs on arrival loads in the route's loader, not in a component-level waterfall. Components fetch only data that appears after interaction.
- **Stream what's slow, block what's cheap.** Critical shell data blocks rendering; below-the-fold or expensive queries stream behind `Suspense` boundaries with skeleton placeholders. **Discover** the project's existing skeleton components before creating new ones.
- **One query-key convention.** `['entity', id]` for items, `['entity', 'list', params]` for collections. Mutations **invalidate** the narrowest key that covers the change — never invalidate without a key.
- **Cursor pagination over offset.** Feeds paginate by cursor (timestamp + id tiebreaker) with infinite-query patterns; offset pagination breaks under inserts and degrades on deep pages.

## Mutations & Optimistic UI

- **Classify before implementing:**
  - *Cheap + reversible* (like, follow, bookmark) → **optimistic**: update the cache immediately, roll back on failure.
  - *Costly or identity-bearing* (create, delete, payment) → **pessimistic**: spinner on the trigger element, update UI only after server confirms.
- Every mutation surfaces all three outcomes in the UI: **pending** (disabled trigger + indicator), **success** (confirmation), and **error** (server's human-readable message inline — never silent failure, never raw stack traces).
- **Constrain**: form state survives failure — never clear inputs before confirmed success.

## States Are Features

Every list/detail surface ships four states or it isn't done:

| State | Requirement |
|---|---|
| **Loading** | Skeleton mirroring the final layout — no layout shift. **Discover** existing skeleton components. |
| **Empty** | What it is + the action to fill it (never a blank screen). |
| **Error** | What failed + retry affordance. |
| **Content** | The happy path. |

**Instrument**: grep for missing states before calling any surface complete.

## Navigation & Flow

- Auth redirects carry a return path — post-login lands where the user intended.
- Destructive actions confirm; the confirmation names the consequence ("Delete this? This cannot be undone.").
- URL is state: filters, tabs, and pagination live in search params (typed route validation), so every view is linkable and survives refresh.

## Handoffs

- Designing a new feature's flow from scratch → start with `/system-design`; this skill then details each route it produced.
- Visual execution of these flows → `/creative-ui`.
- Server-side counterpart of any rule here → `/patterns` (validation, error contracts, middleware).
- Done building → `/full-review` (the ux-reviewer agent checks against exactly these rules).
