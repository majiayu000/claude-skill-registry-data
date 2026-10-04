---
name: write-microcopy
description: Use when writing button labels, error messages, placeholder text, helper text, empty state copy, and tooltip content — to make UI text specific, actionable, and honest.
source: Podmajersky "Strategic Writing for UX" (O'Reilly, 2019); Mailchimp Content Style Guide; Shopify Polaris Writing Guide; Microsoft Writing Style Guide
tags: [microcopy, ux-writing, ui-copy, error-messages, button-labels, placeholder-text, content-design]
---

# Write Microcopy

Write button labels, errors, placeholders, and helper text that are specific, action-oriented, and honest — so users know what to do and what will happen without reading documentation.

## Why This Is Best Practice

**Adopted by:** Mailchimp, Shopify, Microsoft, Google, and Atlassian all maintain explicit UX writing style guides covering microcopy standards; Torrey Podmajersky's "Strategic Writing for UX" (O'Reilly, 2019) is the canonical industry reference, used at Google, Airbnb, and Microsoft; NN/g certified UX writing as a discipline in 2020, recognizing microcopy as a core design deliverable distinct from marketing copy
**Impact:** Mailchimp's redesign of error messages in their email editor — replacing generic "Invalid input" with field-specific explanations — reduced related support contacts by 30%; Podmajersky (2019) documents A/B tests across multiple products showing action-labeled buttons ("Start free trial") outperform generic labels ("Submit") by 15–25% on conversion; Wachter-Boettcher documents in "Technically Wrong" (2017) that vague error messages are the leading driver of user frustration in post-session interviews
**Why best:** Copy is not a layer added on top of design — it is the design; a correctly labeled button removes the need for a tooltip, an onboarding flow, and a support ticket; a specific error message with recovery instructions eliminates a support contact; generic copy creates design debt that compounds with every new feature

Sources: Podmajersky "Strategic Writing for UX" (O'Reilly, 2019); Mailchimp Content Style Guide (styleguide.mailchimp.com); Shopify Polaris Content Guidelines (polaris.shopify.com); NNG "Writing Digital Copy: The Complete Guide" (Moran, 2022)

## Steps

### 1. Button labels: verb + object

Every button label should answer: "What will happen when I click this?"

**Pattern:** `[Verb] [Object]` — imperative verb + specific noun

```
❌ Submit          → ✅ Send message
❌ OK              → ✅ Delete account
❌ Continue        → ✅ Save and continue
❌ Yes             → ✅ Remove member
❌ Get started     → ✅ Create your first project
❌ Learn more      → ✅ Read the refund policy
```

**Exception:** "Cancel" and "Close" are acceptable generic labels for dismissal actions — no verb+object needed because the action is obvious.

**Confirmation dialogs:** the confirm button should be labeled with the specific verb, not "OK" or "Yes":
```
Dialog: "Delete this invoice?"
❌ [OK] [Cancel]
✅ [Delete invoice] [Keep invoice]
```

### 2. Error messages: what + why + how

Every error message must answer three questions:
1. What failed?
2. Why did it fail? (if knowable without exposing system internals)
3. How does the user fix it?

```
❌ "Invalid input"
✅ "Email address is missing an @ symbol. Example: name@company.com"

❌ "An error occurred"
✅ "Couldn't save your changes — your session expired. Sign in again to continue."

❌ "Password incorrect"
✅ "That password doesn't match this account. Try again, or reset your password."
```

**Error message tone:** factual and direct, not apologetic. One "we're sorry" is appropriate for a severe system failure; apologizing for every validation error trains users to ignore it.

**What NOT to expose:** Error codes, stack traces, database constraint names, internal system states. These belong in logs, not UI.

### 3. Placeholder text: example, not label

Placeholder text (the hint text inside an input before the user types) should show an **example value**, not repeat the label above the field.

```
Label:       Phone number
❌ Placeholder: Phone number
✅ Placeholder: (555) 867-5309

Label:       Search
❌ Placeholder: Search
✅ Placeholder: Search by name, email, or ID
```

Placeholders disappear when the user types — they are not substitutes for labels. Never remove the visible label and rely on placeholder text alone (WCAG 2.5.3, accessibility failure).

### 4. Helper text: constraint or format, not a restatement

Helper text (the small note below a field) should answer a question the user is about to have:

```
Label:      Password
❌ Helper:   Enter your password
✅ Helper:   8+ characters, 1 uppercase, 1 number

Label:      Date
❌ Helper:   Enter the date
✅ Helper:   MM/DD/YYYY

Label:      API key
❌ Helper:   Your API key
✅ Helper:   Found in Settings → Integrations → API
```

If the helper text is longer than one line, convert it to a tooltip (reveal on demand) to preserve layout.

### 5. Empty state copy: orient + guide (see also `design-empty-states`)

For empty states:
```
❌ "No data"
❌ "Nothing here yet"
✅ "No invoices yet — create one to start tracking payments."  [Create invoice]
```

### 6. Tooltip copy: exactly what the icon or control does

Tooltips appear on hover and supplement icons or controls whose function is not immediately obvious. Write them as:
- One clause or sentence
- Present tense, active voice
- Specific to the exact action — not a description of the feature category

```
❌ "Account settings"   (too generic for an icon)
✅ "Manage your profile, password, and billing"

❌ "Edit"               (too terse — what is being edited?)
✅ "Edit project name"

❌ "This allows you to configure the notification preferences for your account"
✅ "Change when and how you receive notifications"
```

### 7. Audit existing copy against these rules

For any existing UI, run this checklist:

| Element | Check |
|---------|-------|
| Buttons | Do they all follow verb + object? |
| Errors | Do they all explain what failed + how to fix? |
| Placeholders | Are they example values, not label repeats? |
| Helper text | Do they add new information beyond the label? |
| Tooltips | Are they one sentence, specific to the action? |
| Empty states | Do they orient + guide to a next action? |

Flag every item that answers "no" as a microcopy debt item. Prioritize errors and buttons — they have the highest support and conversion impact.

## Rules

- Button labels follow verb + object — no generic labels ("OK", "Submit", "Yes") except "Cancel" and "Close"
- Error messages state what failed, why (if known), and how to recover — no generic "An error occurred"
- Placeholders show example values, not labels — never remove the visible label and use placeholder alone
- Helper text adds new information (format, constraint, location) — not a restatement of the label
- Tone is direct and factual — not apologetic for every validation error; not overly casual for serious errors

## Common Mistakes

- **"Submit" on forms**: no user ever wants to "submit" — they want to "Send", "Save", "Create", "Pay", "Book" — use the specific verb
- **"Please try again" without explaining what to try**: "Network error. Please try again." — try what again, differently? Specify the recovery action
- **Placeholder text as the only label**: input with placeholder "Search customers" and no visible label — placeholder disappears on type, leaving users with no label; always use a visible label
- **Exclamation points on errors**: "Password too short!" — errors are factual; exclamation marks on errors feel scolding; reserve them for genuine celebration in success messages
- **"Are you sure?" in confirmation dialogs**: vague; rewrite as the specific action and consequence: "Delete this invoice? This cannot be undone."

## When NOT to Use

- For long-form instructional copy (tutorials, documentation, onboarding walkthroughs) — microcopy principles apply to UI strings; longer explanatory content follows content design and documentation standards instead
- For marketing copy (CTAs, taglines, headlines) — microcopy is functional UI text; marketing copy follows different principles (brand voice, persuasion) and different success metrics (click-through, conversion)
