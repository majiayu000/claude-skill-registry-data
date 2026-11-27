---
name: wensity-ui-copy
description: >-
  Write the words inside an interface: headings, buttons, labels, helper
  text, errors, empty states, toasts, confirmations, onboarding and landing
  page copy, plus realistic sample content. Use when writing or revising
  user-facing text in a UI, when filling a new page or component with
  content, when copy sounds like marketing filler or like an AI wrote it, or
  when the user asks for better wording, microcopy, CTA text, error messages
  or empty states. Skip it for changes that keep the existing text.
---

# Wensity UI Copy

Words are part of the design. Vague or inflated copy makes a polished
interface feel generic; plain, specific copy makes a plain interface feel
trustworthy. The test for every string: does it help someone understand or
act?

## 1. Voice

- **Plain words.** Write the way a helpful person would say it out loud.
  "Save changes", not "Persist modifications". "You're out of credits", not
  "Credit balance depleted".
- **The user's words, not the system's.** "Notifications", not "Webhook
  dispatch config". Name things by what people do with them.
- **Short.** Cut every word that does not change the meaning. Then cut again.
- **Sentence case everywhere:** headings, buttons, menu items, tabs, labels.
  "Create new project", not "Create New Project".
- **Active voice, addressed to the user.** "You don't have access to this
  project", not "Access to this project is not permitted". When the system
  failed, say so plainly: "We couldn't save your file", not "The file could
  not be saved".
- **Calm.** No exclamation marks except for genuine celebrations, no
  apologies in errors, no jokes in error states.

## 2. Words that make copy sound generated

Avoid these. They say nothing a reader can check:

- Verbs: unlock, unleash, elevate, empower, supercharge, revolutionize,
  transform, streamline, leverage, harness, reimagine, skyrocket.
- Adjectives: seamless, effortless, cutting-edge, next-generation,
  world-class, robust, powerful, intuitive, innovative, all-in-one.
- Phrases: "In today's fast-paced world", "Take your X to the next level",
  "Whether you're a X or a Y", "Say goodbye to", "Look no further".
- Shapes: three adjectives in a row ("Fast. Secure. Simple."), middle-dot
  lists (`Design · Build · Ship`), and em dashes anywhere in the product's
  text, including the page `<title>`, meta description and alt text. Use a
  colon, a comma or two sentences: "Ledgerline: invoices in any currency".

Replace each with a concrete fact: what it does, how fast, for whom, with
what result. "Cuts a 40-minute report to 2 minutes" beats "Supercharge your
workflow".

## 3. Headings

- **A heading says the point,** not the topic. "Invoices get paid 9 days
  faster" beats "Features". "Your workspace is empty" beats "Workspace".
- **No eyebrows.** Do not put a small uppercase label above a heading
  ("FEATURES", "PRICING", "HOW IT WORKS"). Write a heading that stands alone.
- Page titles name the page so people know where they are: "Billing",
  "Team members".

## 4. Buttons and links

- **Start with a verb and name the result:** "Create invoice", "Send invite",
  "Export CSV". Not "Submit", "OK", "Yes", "Click here", "Learn more" alone.
- **Match the button to what happens next.** If the button says "Publish",
  the toast says "Published", and the page shows the published state.
- **Primary and secondary must be clearly different actions:** "Delete
  project" and "Cancel", not "Yes" and "No".
- **One to three words is ideal.** A CTA can go to five if it adds a
  concrete benefit ("Start free, no card").
- **Link text makes sense alone** (screen readers list links out of
  context): "Read the API guide", not "here".
- **Destructive actions name the thing:** "Delete 3 files", "Remove Sam from
  team".

## 5. Forms

- **Labels above fields,** always visible. Placeholder text is not a label;
  it disappears when typing starts.
- **Placeholders show format, not instructions:** `name@company.com`,
  `MM / YY`. Leave them out when the label is enough.
- **Helper text** under the field for rules people need before typing:
  "At least 12 characters".
- **Mark optional fields, not required ones,** when most fields are required:
  "Company (optional)".
- **Validate on blur or submit,** not on every keystroke. Show the error next
  to the field it belongs to.

## 6. Errors

Every error answers two questions: what happened, and what to do now.

| Weak | Better |
| --- | --- |
| Invalid input | Enter a date after today |
| Something went wrong | We couldn't reach the server. Check your connection and try again. |
| Error 403 | You don't have access to this project. Ask an owner to invite you. |
| Upload failed | This file is 24 MB. The limit is 10 MB. |
| Payment declined | Your card was declined. Try another card or contact your bank. |

- Never blame the user ("You entered an invalid email"). Describe the fix
  ("Enter an email like name@company.com").
- Keep codes and stack traces out of the message. Put a reference ID at the
  end if support needs one.
- Keep what the user typed. Never clear a form because one field failed.

## 7. Empty states

An empty state is the first thing a new user sees. Treat it as onboarding:

1. Say what will appear here: "Invoices you send will show up here."
2. Give the one action that fills it: a primary button, "Create invoice".
3. Optional: a link to import, a template, or a short guide.

For "no results" empties, say what was searched and how to widen it: "No
results for 'invioce'. Check the spelling or clear filters."

## 8. Loading, success and toasts

- **Loading:** say what is happening when it takes more than a second:
  "Generating report…". Use the ellipsis character.
- **Success toasts:** past tense of the action, plus the object: "Invite
  sent to sam@acme.com", "Project deleted. Undo".
- **Offer Undo instead of a confirmation dialog** for reversible actions. Ask
  for confirmation only when the action cannot be undone.
- **Confirmation dialogs:** the title asks the real question ("Delete
  'Q3 report'?"), the body states the consequence ("This removes it for
  everyone. You can't undo this."), the buttons name the action ("Delete
  report" / "Cancel").

## 9. Numbers, dates and units

- Use numerals: "3 files", not "three files".
- Format with the user's locale: `Intl.NumberFormat` and
  `Intl.DateTimeFormat` (or `toLocaleString`) instead of hand-built strings.
- Relative time for recent events ("2 min ago"), absolute dates for older
  ones ("Mar 4"), and the full timestamp in a tooltip.
- Pluralize correctly: "1 file", "2 files", "0 files". Use `Intl.PluralRules`
  or a helper, never "file(s)".
- Keep numbers and units together with a non-breaking space (`10&nbsp;MB`
  in HTML, `"10\u00A0MB"` in JavaScript) so they never wrap apart.

## 10. Realistic placeholder content

When building a design without real content, write content that looks real:

- **Specific names and data:** "Maya Chen, Product designer at Northwind",
  "$12,480.00", "Invoice INV-2041". Not "John Doe", "$XX", "Lorem ipsum".
- **Realistic lengths,** including some long ones, so the layout is tested:
  a 40-character name, a 3-line description next to a 1-line one.
- **Never invent proof.** No made-up customer logos, star ratings, user
  counts or testimonials presented as real. Use marked placeholders
  (`[Customer quote]`, `[Logo]`) or ask the user for the real ones.
- **Match the product's world.** A dev tool's sample data is repos and
  deploys; a clinic app's is appointments and patients.

## 11. Accessibility in copy

- Every icon-only button gets an accessible name: `aria-label="Close dialog"`.
- Alt text describes what an image shows when it carries information
  ("Bar chart: revenue up 24% since January"). Decorative images get
  `alt=""`.
- Do not rely on color words alone ("click the green button").
- Expand abbreviations the first time unless the audience uses them daily.

## 12. Check before you finish

- [ ] No filler words from section 2, no three-adjective taglines, no em
      dashes in interface strings.
- [ ] Every heading states a point; no eyebrows.
- [ ] Every button starts with a verb and names its result.
- [ ] Every error says what happened and what to do.
- [ ] Every empty state explains itself and offers the next action.
- [ ] Sentence case throughout.
- [ ] Sample content is specific, varied in length, and contains no invented
      proof.
- [ ] Icon-only controls and meaningful images have accessible text.
