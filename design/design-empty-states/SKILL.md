---
name: design-empty-states
description: Use when designing screens that appear before content exists — first use, no-results, user-cleared state, or error — to orient users and guide the next action instead of showing a blank screen.
source: NNG "Empty States in Mobile UX" (Laubheimer, 2016); Google Material Design "Empty states" guidelines; IBM Carbon Design System "Empty states" documentation
tags: [empty-states, onboarding, ux, first-use, no-results, error-states, ui-patterns]
---

# Design Empty States

Write copy, add a single CTA, and use illustration or iconography to transform blank screens into helpful prompts that keep users oriented and moving forward.

## Why This Is Best Practice

**Adopted by:** Google Material Design, Apple Human Interface Guidelines, IBM Carbon, Shopify Polaris, and Atlassian Design System all provide explicit empty state guidelines and components; Intercom, Slack, and Notion have each published case studies on how improved empty states increased feature activation rates
**Impact:** NNG (2016) identifies empty states as among the top causes of user abandonment on first use — a blank screen with no context leaves users unsure whether the product is broken, the feature is loading, or action is required; Intercom reported a 17% increase in feature adoption after redesigning first-use empty states with action-oriented copy and a single CTA; Slack attributes part of its onboarding success to empty-state design that guides users to their first message
**Why best:** A blank screen is an implicit error state — it gives users no information about what to do next; a loading spinner without completion feedback is equivalent; empty state design fills the information vacuum with the exact content users need at the moment of uncertainty

Sources: NNG "Empty States in Mobile UX" (Laubheimer, 2016); Google Material Design "Empty states" (material.io); Kleppmann "Designing for Empty States" (Intercom Design, 2017)

## Steps

### 1. Classify the empty state type

Different types require different content:

| Type | When it appears | User's mental state |
|------|----------------|-------------------|
| **First-use** | Feature used for the first time; no data yet | Curious but uncertain what to do |
| **User-cleared** | User deleted all items or completed all tasks | Accomplished; needs next step |
| **No-results** | Search or filter returned nothing | Frustrated; needs to adjust or try again |
| **Error** | Load failed due to network or server issue | Frustrated or confused |

Mismatching type to treatment is the most common empty state error — a first-use state that looks like an error increases anxiety; a no-results state that looks like first-use is confusing.

### 2. Write the headline (orientation copy)

One short sentence that tells the user exactly where they are and why it's empty.

```
First-use:    "No projects yet"
User-cleared: "All caught up!"
No-results:   "No results for 'invoic'"
Error:        "Couldn't load your projects"
```

**Rules:**
- State the entity name ("projects", "messages", "invoices") — not generic ("No content here")
- First-use and user-cleared: positive or neutral tone
- No-results: include the search term so users know the empty state is specific to their query
- Error: acknowledge the failure without blaming the user

### 3. Write the body copy (reason or instruction)

One sentence that explains why it's empty or what to do next.

```
First-use:    "Create a project to start tracking your team's work."
User-cleared: "Check back when new tasks are assigned."
No-results:   "Try a different spelling or check for typos."
Error:        "Check your connection and try again, or contact support."
```

For first-use states, body copy is the highest-value element — it answers the question users actually have ("what does this do and where do I start?").

### 4. Add one primary CTA (first-use and user-cleared only)

First-use and user-cleared empty states need a single, specific action button. Not two buttons; not a link buried in body text — one prominent CTA.

```
First-use:    [Create project]
User-cleared: [Browse new tasks] or just leave without a CTA if genuinely "done"
```

**No-results and error states** do not need a CTA to create — they need a CTA to recover:
```
No-results:   [Clear filters] or [Browse all]
Error:        [Try again] or [Go to dashboard]
```

Never use a generic "Get started" CTA — name the action ("Create your first project").

### 5. Add illustration or icon (optional but high-value for first-use)

Visual support makes the empty state scannable and less clinical.

- **Icon**: appropriate for compact or data-dense UIs (tables, sidebars)
- **Illustration**: appropriate for full-page first-use states; increases memorability
- **No image**: acceptable for inline no-results states within a search result list

Guidelines:
- Illustration should represent the content type, not a generic empty box
- Do not use sad faces, broken items, or error imagery for first-use states — they signal failure, not opportunity
- Keep illustrations small enough not to dominate the layout; empty state is a waypoint, not a landing page

### 6. Apply by state type — complete templates

**First-use:**
```
[Illustration of the content type]
[Entity name] — e.g., "Projects"
[Orientation] — e.g., "Organize your work into projects to track progress with your team."
[Primary CTA] — e.g., [Create project]
```

**User-cleared:**
```
[Optional celebratory icon]
[Positive headline] — e.g., "All done!"
[Next-step copy] — e.g., "New tasks will appear here when they're assigned."
[Optional CTA if genuinely relevant]
```

**No-results:**
```
[Search icon or neutral illustration]
[Specific headline] — e.g., "No results for 'invoic'"
[Recovery copy] — e.g., "Check for typos or try a different term."
[Recovery CTA] — e.g., [Clear search]
```

**Error:**
```
[Error icon — not a broken image]
[Honest headline] — e.g., "Couldn't load your projects"
[Cause + action] — e.g., "Check your connection and try again."
[Retry CTA] — e.g., [Try again]
[Secondary] — e.g., [Contact support]
```

### 7. Test with zero-state users

Before shipping, conduct a 5-user test with participants who have never seen the feature:
- Can they identify what the feature is for?
- Do they know what to do next?
- Does the state feel like an error or an invitation?

First-use empty states that users mistake for loading errors indicate orientation copy needs to be clearer.

## Rules

- Every empty state must have at minimum: a specific headline (not "Nothing here") and body copy
- No-results empty states must include the search term or filter that caused them
- Error empty states must offer a recovery action — "Try again" or "Go back" — never just an explanation with no path forward
- Never use blank white space alone as an empty state — even a text explanation is better than silence
- Illustrations for first-use empty states should represent the content, not the emptiness (show what a project looks like, not an empty box)

## Common Mistakes

- **Generic copy**: "No data to display" — fails to orient the user, name the entity, or suggest next action
- **Error imagery on first-use**: a sad face or broken icon on a first-time-user screen communicates that something is wrong, creating unnecessary anxiety
- **Multiple CTAs**: two or three buttons in an empty state dilute focus; pick one action that best unblocks the user
- **No-results state that looks like first-use**: if "No results for 'X'" looks identical to "No projects yet", users can't tell if the search worked or the feature is empty
- **Empty state for authenticated-only features behind a paywall**: don't show an empty first-use state for a feature the user cannot access; show a gate/upgrade prompt instead

## When NOT to Use

- When the empty state is transient and resolves in < 1s — a brief loading flash that resolves immediately doesn't need empty state treatment; use a skeleton screen or spinner instead
- When the feature genuinely has no actionable next step from the empty state (e.g., an audit log with no events yet) — body copy explaining the condition is sufficient; don't fabricate a CTA
