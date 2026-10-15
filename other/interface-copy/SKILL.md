---
name: interface-copy
description: Write the words in an interface - headlines, buttons, labels, empty states, errors, confirmations, notifications - and the realistic content that fills demos and designs (names, numbers, dates, messages), so the product reads as specific, honest and consistent. Use when writing or reviewing UI text, replacing placeholder content, writing demo data, or when copy sounds generic.
---

# /interface-copy

Interface copy is part of the design. A button that says **Create workspace** is a better button than one that says **Submit**, in the same way a clear icon is. The rules below make words specific, short and consistent.

## Principles

- **Specific over impressive.** "Deploys in 41 seconds" beats "lightning-fast deploys". If a sentence could appear on a competitor's site unchanged, rewrite it around something only this product can say.
- **The reader's words, not the team's.** Say "your photos", not "media assets", unless the users say "assets".
- **Front-load.** Put the important words first: people scan the first two words of every line.
- **One idea per sentence.** Most interface sentences should be under 15 words.
- **Consistent terms.** Pick one word per concept and keep it: never "delete" in one place and "remove" in another for the same action. Keep a glossary as you go.
- **No filler.** Cut these words:
  - "simply", "just", "easily", "please note"
  - "in order to"
  - "we're excited to"
  - exclamation marks

## Pattern by pattern

**Headlines.** Say what it is or what it does, with a number, a name or a concrete outcome. Choose a verb over an adjective.

| Instead of | Write |
|---|---|
| Supercharge your workflow | Every pull request gets its own live preview |

**Buttons and links.** Use a verb and an object, in sentence case, and name the result:

- Create workspace
- Save changes
- Send invoice
- Compare plans

The label should still make sense read on its own, out of context. Avoid Submit, OK, Yes, Click here and Learn more. For a destructive action, name the thing: **Delete "Q3 report"**.

**Form labels and hints.** Labels are nouns ("Work email"). Hints say what's accepted and why ("We send the invoice here"). Never use placeholder text as the label.

**Errors.** Say what happened and what to do next, in plain words. Don't blame, and don't show codes unless someone will search for them.

| Instead of | Write |
|---|---|
| Invalid input | Enter a date after today |
| Something went wrong | We couldn't save your changes because the connection dropped. They're kept on this device; try again when you're back online. |

**Empty states.** Say why it's empty and give the one next step.

| Instead of | Write |
|---|---|
| No data | No invoices yet. Invoices you send appear here. [Create invoice] |

A first-run empty state and a no-results state are different messages; write both.

**Confirmations.** Restate the consequence, and make the buttons say what they do:

> Delete "Q3 report"? It will be removed for everyone in Vitrine. [Delete report] [Keep it]

**Success and status.** Confirm briefly, in past tense, with the object:

- Invoice sent to Hamza
- Saved 2 minutes ago

Offer undo instead of asking "Are you sure?" when the action can be reversed.

**Loading and progress.** Say what's happening when it takes more than a second: "Reading 3 files…", "Building preview…". Never write "Please wait".

**Notifications.** Who did what to which thing: "Salim commented on ATL-209 · Deploy previews". Put the actor first and the object last.

## Realistic content

Placeholder content hides design problems: short fake names never wrap, round numbers never overflow. Write demo and design content as if it were real.

- **People.** Use full names, and name a consistent cast: the same people across screens, each with a role. Mix name lengths and origins that fit the product's market. Avoid celebrity names and "John Doe".
- **Numbers.** Make them plausible and uneven: 12,430 rather than 10,000, and 3.42% rather than 5%. Keep them consistent: if the dashboard says 48 deploys today, the activity log shows them. Include the awkward cases: zero, one, a very long value, a negative change.
- **Dates and times.** Use real, recent and consistent ones, in the format and time zone of the audience. Include "2 minutes ago", yesterday, and last year.
- **Places, products and companies.** Invent them, but make them believable and specific to the domain (a logistics platform ships containers to Sohar, not "Location A").
- **Long content.** Include at least one title that wraps, one name with a diacritic, and one right-to-left string if the product might see them.

## Review

When reviewing copy, go screen by screen and list:

1. **Every button and link label** that isn't verb + object, with its replacement.
2. **Every error, empty state and confirmation**, rewritten to the patterns above.
3. **Terminology conflicts**, with the one term to keep.
4. **Generic claims**, with specific rewrites. Ask the user for the real facts rather than inventing them.

`/template-tells`'s scanner finds buzzwords, placeholders and generic labels in the source automatically; run it first on large projects.

Deliver changes as `before → after` pairs grouped by screen, or edit the source directly if asked.
