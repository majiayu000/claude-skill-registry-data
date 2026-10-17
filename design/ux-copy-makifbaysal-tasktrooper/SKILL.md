---
name: ux-copy
category: design
description: Use when you write any words a user reads in a mockup or a hand-off - content language and voice, buttons, labels, errors, empty states, confirmations, numbers and dates, and the longest-string check
---
# UX Copy

## Overview

The words are part of the design: a button label decides whether the user knows what happens next, an error decides whether they can recover. Copy written as an afterthought — "Submit", "Error occurred", "No data" — is how a well-drawn screen still fails.

**Core principle:** Say what happens, in the user's words, in the product's language — and write the longest version you will ever see.

## Language and voice

- Write in the product audience's content language (the brief names it) — never in TaskTrooper's own UI locale just because the board is in it.
- Read the product's existing strings first (`locales/*.json`, `Localizable.strings`, `res/values/strings.xml`, `lib/l10n/*.arb`) and reuse its terms exactly: if the app says "Workspace", a new screen does not say "Project". Match its voice — formal or casual, "you" or impersonal.
- Copy the brief gives is used verbatim. Copy you wrote is listed in `#notes` as draft copy.

## Patterns

| Element | Write | Not |
|---|---|---|
| Button | verb + object, sentence case: "Send invoice" | "Submit", "OK", "Click here" |
| Destructive button | names the thing: "Delete invoice" | "Delete", "Yes" |
| Field label | a noun above the field: "Customer email" | the placeholder as the only label |
| Placeholder | an example: "name@company.com" | the label repeated |
| Helper text | the constraint, before the user hits it: "At least 8 characters" | a tooltip-only hint |
| Error | what happened + how to fix, no blame, no apology: "Enter an email address like name@company.com" | "Invalid input", "Oops! Something went wrong" |
| System error | what failed + what to do: "Invoices couldn't load. Check your connection and try again." + "Retry" | an error code alone |
| Empty, first use | why it is empty + the one next action: "No invoices yet — create your first one in under a minute." + "New invoice" | "No data" |
| Empty, no results | the query + the way out: "No invoices match "Ortiz"" + "Clear search" | the first-use empty state |
| Success | the outcome with the object: "Invoice INV-204 sent to Dana Ortiz" | "Success!" |
| Confirmation dialog | title asks with the object ("Delete invoice INV-204?"), body states the consequence ("This can't be undone."), buttons are the verb and "Cancel" | "Are you sure?" with Yes / No |
| Link | where it goes: "View invoice" | "Click here", "More" |
| Icon-only control | its accessible name, written in the spec: "Filter invoices" | nothing |

## Numbers, dates, plurals

- Amounts, dates and numbers in the content language's locale format, with the currency the product uses; tabular figures where amounts line up.
- Plurals for every count ("1 invoice", "2 invoices"); relative dates only for recent events ("2 hours ago"), absolute beyond that.

## Length

- Draw the longest plausible string at least once: the longest customer name, a title that wraps to three lines, a five-digit count. German, Finnish and Turkish run 30–40% longer than English.
- Say what truncates and where the full text lives — on touch screens there is no hover to reveal it.

## Common Mistakes

- Generic labels that fit any screen ("Submit", "Details", "Manage").
- One empty state for "nothing yet" and "nothing matches".
- Apologetic, jokey or blaming errors.
- Copy in the board's language instead of the product's.

## Red Flags

- A placeholder doing a label's job.
- An error message that does not say how to recover.
- A destructive action whose button says only "Delete" or "Yes".
