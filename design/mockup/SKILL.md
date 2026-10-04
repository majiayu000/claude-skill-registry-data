---
name: mockup
description: "Use for \"mock this up\", \"show me what this would look like\", \"prototype this flow\", or before building any UI where the shape isn't settled. One self-contained HTML file with a tab per state of the flow, so a person clicks through the whole thing with no backend. This is how design-it-twice and experience-first prototype."
---

# Mockup

One HTML file, no dependencies, a tab bar across the top, one tab per state of the flow. Someone opens it and clicks through the feature end to end before anyone writes real code. Cheap to make, cheap to throw away, and it settles arguments that descriptions can't.

## What you're given

Some of: a description of the feature and its flow, a screenshot of the app it lives in, a design system to match, the specific states they want to see.

## 1. Work out the states

From the description, list every distinct screen or state. The usual shapes:

- Create or edit: empty, form, saving, saved, error.
- Upload: pick a file, uploading, preview, confirm, done.
- Wizard: step one, step two, review, submit, confirmation.
- Dashboard: loading, populated, empty, filtered, detail.
- Action: idle, in progress, complete, failed.

Show the list before building. "I see five states, input, processing, preview, request changes, created. Adjust anything?" Wait for a yes.

## 2. Pick the look

In this order:

1. **A screenshot.** Match it exactly. Colors, type, spacing, form controls, buttons, section headers, layout. Reproduce the chrome, nav, sidebar, header, footer, so the feature shows up in context. Study it before writing a line.
2. **A design system.** Its tokens, components, patterns.
3. **An app name.** Approximate that app's look.
4. **Nothing.** Clean default. White or light gray background, dark text, the system font stack, subtle borders and shadows, one blue action color, 14px base. No framework.

## 3. Build the file

A sticky dark bar at the top, `#2c2c2c`, "Flow state:" on the left in a muted color, then one numbered tab per state, "1. Input", "2. Processing". The active tab is lighter. Clicking a tab shows that state and scrolls to the top.

Each state is a full page, not a fragment. The whole chrome repeated, then the feature area in that state, with realistic data and the right feedback: a success banner, an error message, a spinner.

Interaction stays small. Tab switching. Hover on buttons. Action buttons that jump to the logical next tab, submit goes to processing. Collapsible sections where they make sense. Form fields present but not validated.

Nothing external. No CDN, no framework, no fetch, no build step. Only CSS transitions and simple spinners.

## 4. Realistic data

Never lorem ipsum. Names that fit the domain. Plausible numbers and dates. The status labels the app would actually use. Three to six varied rows in any table. Real error text. Empty states that say what to do next.

## 5. Hand it over

Save it somewhere the human can find it, open it in the browser, tell them it's open and list the tabs. Offer to save it somewhere permanent if they want to keep it.

Changes go into the same file. Reopen, say what moved.

## Before you hand it over

Every state has a complete tab. The bar works. The look matches the reference. The data reads as real. Action buttons cross-link to the next state. No external dependencies. It holds up at common widths. Loading states spin. Success states confirm. Error states explain.

## Some flows for reference

- Checkout: cart, shipping, payment, processing, confirmation, error.
- Import: upload, validating, preview, confirm, success, partial failure.
- Settings: view, edit, saving, saved.
- Search: initial, loading, results, no results, detail.
- Approval: draft, submitted, under review, approved, rejected.
