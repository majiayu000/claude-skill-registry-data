---
name: ui-microcopy
description: Write or refine UX copy — button labels, error messages, empty-state text, tooltips, helper text, loading messages, confirmation dialogs — to be specific, action-oriented, and consistent in voice. Use this skill whenever the user wants to review or improve the wording in a UI, when generated copy sounds robotic or generic (e.g. plain "Submit" buttons, "Invalid input" errors, "No data" empty states), when a brief has been written but the implementation language hasn't been decided, or as a step before ui-generate-code so the copy in the generated UI is intentional rather than default. Always use it on any UI where the user describes the audience as non-technical, because default AI copy is heavily skewed toward developer voice.
status: stable
---

# UI Microcopy

**Note: This skill is a recommended addition to the original 7-skill kit.** Microcopy is one of the highest-leverage parts of a UI and is often the place where "robotic AI voice" leaks back in even when layout and components are correct. It's separated from the rest because the skills needed (voice, brevity, error empathy) don't fit cleanly into the structural specs.

Specifies the wording of every UI string so the implementation isn't filled with placeholder copy like "Submit", "Error", "Loading...".

## When to use this skill

Use this skill when:
- A spec has been written but the language hasn't been nailed down.
- Generated UI sounds robotic, generic, or developer-voiced.
- The user wants to review copy independently of layout.
- A brief specifies a target audience whose voice doesn't match default AI English (consumer apps, kids, accessibility users, non-English contexts).

Do **not** use this skill when:
- The user is fine with default copy (rare, but valid for internal tools).
- The UI is purely technical / for developers and developer voice is appropriate.

## Core principles

1. **Buttons say what they do, not what they are.** "Save profile" not "Submit". "Delete account" not "Confirm".
2. **Errors say what's wrong AND how to fix it.** "Email already in use — sign in instead?" not "Invalid input".
3. **Empty states tell the user what to do next.** "No projects yet — create your first one" not "No items".
4. **Loading copy reflects the actual operation.** "Looking up your team..." not "Loading...".
5. **Voice is consistent.** Decide on a voice (formal, friendly, terse, warm) and apply it everywhere.

## Pre-flight check

1. **Brief or context exists.** Need to know the audience and the brand voice.
2. **The strings to write are listed.** Do you have a screen, a component, or a whole flow? Output should enumerate every string.
3. **Voice is decided.** If no voice exists, propose 2–3 candidates with samples and ask the user to pick.

## Voice options (pick one)

| Voice | Sample greeting | Sample error |
|---|---|---|
| **Plain & direct** | "Welcome back." | "That email isn't registered." |
| **Warm & casual** | "Hey, welcome back!" | "Hmm, we don't recognize that email. Try another?" |
| **Formal** | "Welcome." | "The email address provided is not associated with an account." |
| **Playful** | "Hey there 👋" | "We couldn't find that email. Maybe a typo?" |
| **Terse / utility** | "Sign in" | "Email not found." |

Different voices make sense for different products. A consumer wellness app and a B2B compliance tool should not sound the same.

## The categories every UI needs

| Category | Examples |
|---|---|
| **Actions** | Button labels, link labels, menu items |
| **Inputs** | Field labels, placeholders, helper text, character counters |
| **Validation** | Error messages, success messages, warning messages |
| **States** | Empty, loading, error, success, no-results |
| **Feedback** | Confirmations, toasts, snackbars |
| **Headers** | Page titles, section titles, modal titles |
| **Microinformation** | Tooltips, badges, status pills |
| **Destructive confirmation** | "Are you sure?" dialogs |

## Workflow

1. **List every string.** From the spec or implementation, extract every piece of UI copy.
2. **Categorize each.** Use the table above.
3. **Apply voice.** Rewrite each in the chosen voice.
4. **Apply the principles.** Buttons say what they do; errors say how to fix; empty states tell what to do next.
5. **Check length.** Mobile screens have small text areas. Prefer short over verbose. Set a soft cap per category (button labels: 2–3 words; tooltips: 8 words; errors: 12 words).
6. **Check consistency.** "Sign in" or "Log in"? "Cancel" or "Discard"? Pick one and use it everywhere.

## Output template

```markdown
---
spec_type: microcopy
spec_id: <slug>
based_on: <brief / blueprint / component spec slugs>
voice: <plain | warm | formal | playful | terse>
created: <YYYY-MM-DD>
status: draft
---

# Microcopy: <feature or screen name>

## 0. Voice
**Chosen voice:** <name>
**Defining traits:** <e.g. "warm but not cute, contractions OK, never use exclamation points except in success">

## 1. Actions

| Where | Default copy (bad) | Approved copy | Notes |
|---|---|---|---|
| Primary CTA on signup | "Submit" | "Create account" | Action-verb specific |
| Save in settings | "Save" | "Save changes" | "Save what" reduces ambiguity |
| Cancel in modal | "Cancel" | "Cancel" | Already specific enough |
| Delete account | "Delete" | "Delete account permanently" | Adds weight to a destructive action |

## 2. Inputs

| Where | Field | Placeholder | Helper text | Error message |
|---|---|---|---|---|
| Signup | Email | "you@example.com" | (none) | "We need an email to send you a verification link." |
| Signup | Password | (no placeholder) | "At least 8 characters, including a number." | "That password is too short — we need at least 8 characters." |
| Settings | Display name | "Your name" | "This is shown to your teammates." | "Display name can't be empty." |

## 3. Validation

| Trigger | Default copy (bad) | Approved copy |
|---|---|---|
| Required field empty | "This field is required" | "Please add your email." |
| Email already exists | "Email already exists" | "That email is already in use. Sign in instead?" |
| Server error | "An error occurred" | "Something went wrong on our end. Try again in a moment." |
| Network timeout | "Request failed" | "We couldn't reach our servers. Check your connection and retry." |

## 4. States

| State | Where | Default copy (bad) | Approved copy |
|---|---|---|---|
| Empty | Project list | "No items" | "No projects yet — create your first one to get started." |
| Empty | Search results | "No results found" | "Nothing matches \"{query}\". Try a different search?" |
| Loading | Account page | "Loading..." | "Loading your account..." |
| Loading | Search | "Loading..." | "Searching..." |
| Success toast | After save | "Success" | "Saved." |
| Error toast | After failed save | "Error" | "We couldn't save that. Your changes are still here — retry?" |

## 5. Headers and titles

| Where | Default copy (bad) | Approved copy |
|---|---|---|
| Page title — settings | "Settings" | "Account settings" |
| Modal title — delete | "Confirm" | "Delete this project?" |
| Modal title — invite | "Invite" | "Invite teammates" |

## 6. Tooltips

| Where | Approved copy | Length |
|---|---|---|
| ⓘ on "two-factor authentication" | "Adds a second step to your sign in for extra security." | 9 words ✓ |
| ⓘ on "billing email" | "Receipts and invoices go here, separate from your account email." | 10 words ✓ |

## 7. Destructive confirmations

| Action | Default copy (bad) | Approved copy |
|---|---|---|
| Delete project | "Are you sure?" | "Delete this project? This can't be undone, and any teammates will lose access." |
| Delete account | "Confirm" | "Delete your account and all data? This is permanent." |

## 8. Banned words / phrases

| Avoid | Use instead | Why |
|---|---|---|
| "Submit" | "Save", "Send", "Create", "Continue" — depending | Generic and developer-voiced |
| "Invalid" | Specific reason it's invalid | Tells the user nothing |
| "Error" | What went wrong, in plain terms | Same |
| "Click here" | The actual action | Bad for screen readers |
| "Loading…" with no context | "Loading <thing>…" | Cargo-cult phrasing |

## 9. Open questions
- <e.g. "Do we use 'log in' or 'sign in'? Pick one for the whole product.">

## 10. Assumptions
- ⚠️ <flagged>
```

## Rules that prevent hallucinated copy

1. **Don't write copy the brief doesn't support.** Tone of voice traces back to the audience and brand. If the brief doesn't say, ask.
2. **Never invent product features in microcopy.** "We'll send you a curated weekly digest" — does the product actually do that? Don't oversell in copy.
3. **Don't use exclamation points by default.** They're easy to overuse. Reserve for genuine moments of delight or success.
4. **Don't use second-person plural ("we") inconsistently.** Decide once: is the product a "we" (a company speaking to a user) or a tool (no narrator)? Apply uniformly.
5. **Don't use idioms that don't translate.** "Hit the ground running", "knock it out of the park" — confusing for non-native speakers and screen readers.

## Acceptance criteria for this skill's output

- [ ] Voice is named and characterized.
- [ ] Every category that applies to the scope has at least one row (no empty categories — omit if not applicable).
- [ ] Every string has a "default (bad)" → "approved" pair so the contrast is visible.
- [ ] No banned word ("Submit", "Invalid", "Error", "Click here") survives in approved copy without justification.
- [ ] Length checks: button labels ≤ 3 words; tooltips ≤ 12 words; errors ≤ 15 words (these are guides, not laws — flag exceptions).
- [ ] Consistency check: "log in" vs "sign in", "delete" vs "remove", "save" vs "update" — pick one of each and apply uniformly.
