---
name: microcopy
description: "Writes or reviews UX copy — button labels, error messages, empty states, success messages, tooltips, form labels, onboarding text, confirmation dialogs. Voice-consistent, action-led, recovery-oriented. Localizable. No dark patterns."
argument-hint: "<context — e.g., 'error states for the checkout', 'empty state for inbox', 'tooltips for billing page'>"
---

# /microcopy

Write the small strings that decide whether users figure your product out — or churn. Bad copy makes good visuals fail; good copy carries average visuals.

## When to use

- Designing or reviewing any user-facing text — buttons, errors, empty states, tooltips, confirmations, form labels, onboarding.
- After a UX review flagged unclear messaging.
- When a feature ships with placeholder strings ("Submit," "Error," "Loading…") and needs real ones.
- When localizing — the source strings need to be localizable in the first place.

## Operating method

### 1. Establish voice

Read 5–10 existing strings from the product before writing new ones. Identify:

- **Tone** — professional / friendly / playful / clinical. Most B2B is professional-with-warmth; consumer varies wildly.
- **Person** — second person ("Save your changes") almost always. First-person plural ("We saved your changes") for system updates only.
- **Verb usage** — direct ("Save"), polite ("Please save"), or playful ("Stash it"). Pick one and stick with it.
- **Punctuation** — sentence case vs title case for buttons. Periods at end of error messages or not.
- **Emoji** — used or not. (Default: not. Add only if the product already uses them.)

If no existing strings exist, default to: direct, second person, sentence case for buttons, periods on full sentences, no emoji.

### 2. Apply the four rules

**Verbs over nouns on buttons.** Buttons do something. Use the verb.

| Bad | Good |
|---|---|
| Submit | Send invite |
| OK | Save changes |
| Confirmation | Confirm payment |
| Settings | Open settings |

**Specific errors with recovery.** Tell the user what went wrong AND what to do.

| Bad | Good |
|---|---|
| Invalid input | Email must include an @ symbol |
| Error | Couldn't reach the server. Check your connection or retry. |
| Try again | Card declined — try a different card |
| Failed | Two-factor code expired — request a new one |

**Empty states have CTAs.** Don't leave the user stranded with "No results."

| Bad | Good |
|---|---|
| No projects | Create your first project to get started |
| 0 messages | Your inbox is empty. Connect an account to start receiving mail. |
| Nothing here | No matching results. Try a broader search or [clear filters]. |

**Honesty in confirmations.** Don't trick users into clicking yes.

| Bad | Good |
|---|---|
| "OK" + "Cancel" on a destructive modal | "Delete project" + "Keep project" |
| "Are you sure?" | "Delete this project? This cannot be undone." |

### 3. Forbidden phrases

These signal lazy or hostile copy. Refuse to write them; replace if you find them.

| Phrase | Why it's bad | Replace with |
|---|---|---|
| "Simply…" / "Just…" / "Easy…" | Patronizes the user — if it were that simple, they wouldn't be reading the help text | Remove the word; explain the steps |
| "Oops!" / "Whoops!" | Trivializes the user's problem | Be specific about what happened |
| "Something went wrong" | The least useful possible error | Name what failed, name the recovery |
| "Please try again later" | Useless — when? Why? | Give a time, a reason, or a workaround |
| "Are you sure?" alone | Doesn't tell the user the consequence | "Delete X? This cannot be undone." |
| "Click here" / "Read more" | Bad for accessibility (screen readers without context) | Use descriptive link text: "Read the API docs" |
| Pre-checked consent ("☑ Yes, send me marketing emails") | Illegal in EU (GDPR) | Default unchecked; let users opt in |
| Confirmshaming ("No thanks, I don't want to save 50%") | Dark pattern | Plain language: "No thanks" |

### 4. Localization-friendly writing

Write strings that translate cleanly:

- **No idioms.** "Bite the bullet" doesn't translate. "Confirm the change" does.
- **No concatenation.** Don't write `"You have " + count + " messages"` — different languages put numbers in different positions, and some require plural forms beyond singular/plural.
- **Use ICU MessageFormat** or your framework's i18n library for plurals, gender, and number formatting.
- **Don't bake numbers into strings**. "5 items" → `{count, plural, one {# item} other {# items}}`.
- **Render dates and currencies in user locale**, not source locale.
- **Leave 30% room for expansion.** German strings are often 30–40% longer than English.

### 5. Cover all the moments

For every screen or component, walk the moments:

- **Default** — the standard view. What does it say?
- **Loading** — what's communicated while waiting?
- **Empty** — first-time-use copy + CTA.
- **Success** — confirmation message.
- **Error** — per failure mode (network, validation, permission, server).
- **Disabled** — why is this thing disabled? Tooltip explains.
- **Confirm** — destructive actions get a clear "do X / cancel" choice.
- **Onboarding** — first 3 actions for a new user.

### 6. Save patterns to memory

If the product establishes a copy convention (e.g., "always say 'Save changes' not 'Save'"), save it to `.claude/memory/feedback/copy-conventions.md` so future sessions follow the same voice.

## Output format

For a copy spec:

```
# Microcopy: <screen / feature>

## Voice
- Tone: <professional with warmth>
- Person: second
- Case: sentence (buttons), title (page headers)
- Punctuation: full sentences end with periods; buttons no periods

## Strings

### Page header
<copy>

### Primary CTA (button)
<copy>

### Secondary action
<copy>

### Form fields
| Field | Label | Placeholder | Help text | Error: blank | Error: invalid |
|---|---|---|---|---|---|
| Email | "Work email" | "you@company.com" | "We'll send sign-in links here." | "Email is required." | "Email must include an @ symbol." |

### States
| State | Copy |
|---|---|
| Loading | "Sending invite…" |
| Success | "Invite sent ✓" |
| Error: network | "Couldn't send the invite — check your connection or retry." |
| Error: already invited | "Already invited — resend or remove." |
| Empty | "No invites sent yet. Send your first below." |

### Confirmation dialog (destructive)
- Title: "Remove team member?"
- Body: "They'll lose access to all projects. This can't be undone."
- Confirm button: "Remove member"
- Cancel button: "Keep member"

### Tooltips
| Element | Tooltip |
|---|---|
| Disabled "Send" button | "Add at least one recipient to send" |
| ⚠ icon next to plan | "Card on file expires in 7 days" |
```

For a copy review:

```
## Verdict: GREAT | NEEDS WORK | REWRITE

## Issues by category

### Specificity (N issues)
- error.tsx:18 — "Something went wrong" → "Couldn't save changes — check your connection and retry."

### Voice consistency (N issues)
- onboarding.tsx:42 — Uses first-person ("We've saved your work") but the rest of the product uses second person.

### Forbidden phrases (N issues)
- billing.tsx:91 — "Simply enter your card" → "Enter your card."

### Empty states (N issues)
- inbox.tsx:5 — "No messages" with no CTA → "Your inbox is empty. Connect an account to start."

### Localization-readiness (N issues)
- list.tsx:30 — `"You have " + count + " items"` → use ICU plural format.

## What's working
- <thing>
- <thing>

## Recommended next moves
1. <highest-leverage>
```

## Boundaries

- Don't write for a voice the product doesn't have — read existing copy first.
- Don't write copy that's marketing-speak when the product is utilitarian, or vice versa.
- Don't recommend dark patterns. Refuse, name them, offer honest alternatives.
- Don't translate yourself — flag strings for translator review when localizing.
- Don't write copy without knowing the state. "Submit" with no context is meaningless.
- Always cover all relevant moments (loading / empty / error / success).
