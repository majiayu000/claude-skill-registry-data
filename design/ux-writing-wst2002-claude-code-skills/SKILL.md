---
name: ux-writing
description: Use when writing or reviewing UI text or microcopy — button labels, error messages, empty states, form labels and hints, onboarding, tooltips, confirmation dialogs, notifications or success messages — or making product copy clearer, shorter and consistent.
---

# UX Writing

## Overview

Interface text is part of the design: it tells people what they can do, what happened, and what to do next. Good microcopy is specific, short, consistent and kind, and it still works when translated or read by a screen reader.

## Inputs

- The screen or flow (screenshot, Figma frame, or a list of strings) and where each string appears.
- Who the user is and what they are trying to do at that moment.
- Existing voice and tone guide or glossary, if any. Otherwise infer the tone from the product's existing copy and keep it.

## Method

1. **Context per string:** where it appears, what the user just did, what they want next, and how they feel (in a hurry, worried about money, first visit).
2. **Write or rewrite** each string with the patterns below.
3. **Consistency pass:** one name per concept across the flow (do not mix "workspace", "project" and "space"), the same verb for the same action, the same capitalisation style.
4. **Length pass:** fit the space; leave room for about 30% expansion in translation.
5. **Accessibility pass:** link and button text makes sense out of context, error text is tied to its field, no meaning carried only by an icon or colour.
6. **Deliver** as a table: location, current, suggested, why.

## Patterns

| Type | Pattern | Example |
|---|---|---|
| Button | Verb + object; says what will happen | "Save changes", "Send invite" (not "OK", "Submit") |
| Destructive confirmation | Title asks about the exact action; body states the consequence; buttons repeat the action | "Delete 'Q3 report'?" · "This can't be undone." · [Delete report] [Cancel] |
| Error message | What happened + how to fix it; no blame, no raw codes alone | "That card was declined. Try another card or contact your bank." |
| Form field error | Specific to the field and the rule | "Enter a date after today" (not "Invalid input") |
| Empty state | What will appear here + why it's empty + the action to fill it | "No invoices yet. Invoices you send will show up here. [Create invoice]" |
| Success | Confirm the result and the next step if there is one | "Invite sent to asha@example.com" |
| Loading | Say what is happening when it takes more than a moment | "Uploading 3 of 12 photos…" |
| Label and hint | Label names the field; hint explains format or why it's needed | Label "Phone number", hint "We'll text you a code to sign in" |
| Onboarding | Benefit first, one idea per step, easy to skip | "Connect your calendar to see free slots automatically" |
| Notification | Who or what + what happened + action | "Riya commented on 'Homepage v2'" |

## Report format

```
## UX writing: <screen or flow>

| Location | Current | Suggested | Why |
|---|---|---|---|
| Delete dialog, primary button | OK | Delete project | Names the action; "OK" hides that it is destructive |

**Glossary for this flow:** <term> (use) · <term> (avoid)
**Open questions:** <facts you need, e.g. "how long does the refund take?">
```

For the most important strings (primary buttons, key errors, headlines) give one or two alternatives with the trade-off.

## Rules

- Never invent facts in copy: timings ("within 24 hours"), prices, limits or policies. Ask, or leave a placeholder like `<refund time>`.
- Use the user's words, not internal or technical terms ("payment failed", not "transaction error 402").
- Front-load the important word; cut "please", "simply", "just" and filler.
- Sentence case unless the product's style says otherwise.
- Do not build sentences by joining strings ("You have " + n + " items"); write full strings with plural forms, so they can be translated.
- No "click here" or "learn more" alone; link text names its destination.
- Keep the product's existing voice; do not add jokes or exclamation marks to errors.

## Common mistakes

- "Something went wrong" with no cause and no next step.
- Buttons that say "Yes" and "No" under a question the user has to re-read.
- Three different words for the same thing in one flow.
- Copy that fits in English and breaks the layout in German.

---

Made by **Wageesha Tripathi** · [LinkedIn](https://www.linkedin.com/in/wst2002/) · [Email](mailto:tripathiwageesha2002@gmail.com) · [More skills](https://github.com/WST2002/claude-code-skills)
