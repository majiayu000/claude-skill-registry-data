---
name: design-flow
description: "Designs an end-to-end user flow before any pixels are drawn — entry point, screens, decisions, branches, error/recovery paths, edge cases, microcopy hooks. Outputs a structured spec engineering and design can build from."
argument-hint: "<flow name, e.g., 'signup', 'checkout', 'invite teammate', 'reset password'>"
---

# /design-flow

Design a complete user flow at the right altitude. Most flow design fails because it stops at the happy path — this skill walks the full surface (decisions, branches, edge cases, recovery) and outputs something engineers can actually build.

## When to use

- Designing a new feature flow before any UI work.
- Spec'ing an existing flow that's never been documented.
- Translating a vague product goal ("we need onboarding") into a concrete user-facing journey.
- Comparing your flow against how Stripe / Linear / Notion / Shopify handle the same problem.

## Operating method — ASK FIRST

Before designing anything, get answers in one round:

1. **Who is the user?** Persona + context. Not "a user" — "a small-business owner whose first action is connecting a bank account on a phone."
2. **What's their goal?** The thing they want completed.
3. **What's the success criterion?** Measurable. "First-time user can complete in under 90 seconds, ≤ 3 attempts."
4. **What's the entry point?** Where do they arrive from? Email link, marketing CTA, in-app banner, deep link from another product?
5. **What's the hardest case?** The edge that's breaking it today (or the case you're worried about).
6. **What constraints?** Compliance (KYC, GDPR consent), accessibility, mobile-first, third-party integrations.

Do not start designing without these. Designing the wrong flow takes the same time as designing the right one — and one of them ships.

## Method

### 1. Story altitude

Walk the journey end to end in plain language. 5–12 numbered steps. Each step:
- Where the user is (URL / screen / state).
- What they see.
- What they decide.
- What they do.
- What the system responds.

This pass tests whether the journey is coherent before any wireframing.

### 2. Decisions and branches

Every flow has decisions. Build a table:

| Decision point | Default path | Alternatives | If user bails | If error |
|---|---|---|---|---|
| Pick auth method | Magic link to email | Google OAuth, SAML SSO | Save email, send link 1h later | Show error + retry |
| Confirm phone | Enter SMS code | Resend, change number | Hold account 7d | Show error + alt verification |

Every alternative path that's reachable must have its own design. Branches you don't design *will* break in production.

### 3. Edge cases

Walk these explicitly:

- **Empty state** — first-time, no data yet.
- **Partial state** — some required info missing.
- **Long content** — names with 200 characters, lists with 10K items.
- **Special characters** — emoji, RTL text, accents, zero-width.
- **Slow network** — what's shown for 5+ seconds?
- **Offline** — the network drops mid-flow.
- **Returning user mid-flow** — they bailed yesterday, came back today; resume or restart?
- **Permission denied** — the user lacks the role for this action.
- **Concurrent edit** — two people editing the same resource.
- **Account state** — suspended, past-due, trial-expired, archived.
- **Locale / timezone** — date display, currency, number formats.
- **Accessibility** — keyboard-only flow, screen-reader sense, reduced motion.

Each relevant edge case needs a planned response.

### 4. Microcopy hooks

For every screen, name the strings that matter:

- Page title / heading.
- Primary CTA label.
- Secondary action.
- Field labels.
- Error messages (per failure mode).
- Empty-state explanation + CTA.
- Success confirmation.

Don't ship "Submit" or "Error: invalid input." Specify the actual copy. Voice and tone come from the project's existing convention (read existing UI for the pattern); fall back to direct, friendly, verb-led if no convention exists.

### 5. Compare to prior art (optional)

For flows that have a thousand prior implementations (signup, checkout, password reset, invitations, onboarding), look at how 2–3 mature products handle it before designing. The `/competitive-analysis` skill is the deep version of this. For a quick check, just name the references in the output: "Stripe handles this with X; we'll differ because Y."

### 6. Save the design

Write the result to `.claude/memory/project/flow-<name>.md` so future sessions inherit it. Add to `MEMORY.md` index.

## Output format

```
## Flow: <name>

### Goal
<one sentence>

### User
<persona — specific>

### Success criterion
<measurable>

### Entry points
- <where they come from>
- <where they come from>

### Story
1. User arrives at <X> from <source>. They see <screen 1 summary>. They <action>.
2. System <response>. User sees <screen 2 summary>. They decide <decision 1>.
3. …

### Screens (state-by-state)
| Screen | Purpose | States needed | Key components |
|---|---|---|---|
| /signup | First-touch | default, error (email taken), loading | Email input, primary CTA, OAuth alts |
| /signup/verify | Confirm code | default, code-sent, error (bad code), expired | Code input, resend link, change-email link |
| …

### Decisions and branches
[table]

### Edge cases
- <case 1> — handled how
- <case 2> — handled how

### Microcopy
| Screen | Element | Copy |
|---|---|---|
| /signup | Page title | "Create your account" |
| /signup | Primary CTA | "Send magic link" |
| /signup | Error: email taken | "That email's already in use. Sign in instead?" |
| …

### Open questions for you
1. <question>
2. <question>

### Engineering handoff
- Routes needed: …
- Backend endpoints: …
- New components needed: …
- Reused components: …
- Analytics events to instrument: …
```

## Boundaries

- Don't design without the 6 questions answered. Domain ambiguity makes for irrelevant design.
- Don't draw pixels at story altitude.
- Don't skip edge cases — they're the point.
- Don't design dark patterns. Refuse, name them, offer honest alternatives.
- Don't recommend a flow longer than the goal requires. The shortest flow that covers all states wins.
- Always cite prior art when borrowing patterns from competitors.
