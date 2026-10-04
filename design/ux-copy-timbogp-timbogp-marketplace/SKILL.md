---
name: ux-copy
description: This skill should be used when the user wants to write or review interface microcopy and says things like "write copy for", "what should this button say", "review this error message", "empty state copy", "onboarding text", "confirmation dialog wording", "rename this CTA", or "microcopy". It writes clear, user-centered UX copy and critiques existing copy with before/after rewrites.
version: 0.1.0
---

# UX Copy

Write and review UX microcopy — the small but high-leverage words inside an interface that guide users, prevent errors, and set tone. Produce copy that is clear, concise, and centered on the user's goal, then write it into the relevant components when editing code.

## When to use

Trigger on requests like: "write copy for [element]", "what should this button say", "review this error message", "empty state copy", "onboarding text", "confirmation dialog wording", "rename this CTA", "is this microcopy clear", "tone of this message". Use it both to author new copy and to critique and rewrite existing copy.

## Scope

UX copy covers all the in-product text users read while doing things:
- **Buttons & CTAs** — the action labels that drive the interface.
- **Form labels & helper text** — what to enter and how.
- **Error & validation messages** — what went wrong and how to fix it.
- **Empty states** — what's missing and what to do about it.
- **Success / confirmation messages** — acknowledging that an action worked.
- **Onboarding & tooltips** — orienting new users without overwhelming them.
- **Confirmation dialogs** — especially for destructive or irreversible actions.
- **Notifications** — timely, relevant, dismissible.

## Principles

1. **Clarity over cleverness.** A user mid-task wants to understand, not be entertained. Cut wit that costs comprehension.
2. **Lead with the user's goal.** Frame copy around what the user is trying to do, not what the system is doing. "Find your order" beats "Order lookup module."
3. **Be concise.** Remove words that don't add meaning. Front-load the important part so it survives a glance.
4. **Use plain language.** Avoid jargon, internal terms, and acronyms. Write for the least familiar user who still belongs in the audience.
5. **Use specific verbs in CTAs.** Name the action: "Save changes," "Send invite," "Delete project" — not "Submit," "OK," or "Yes." The button should make sense read on its own.
6. **Keep terminology consistent.** Pick one word per concept (e.g., "delete," not "delete/remove/trash") and use it everywhere.
7. **Sentence case by default.** "Save changes," not "Save Changes" and not "SAVE CHANGES." Reserve other casing only if the project's style demands it.
8. **Stay accessible.** Don't rely on copy alone to carry meaning that color, icon, or layout should also convey. Write labels and messages that make sense to a screen reader read in isolation; ensure interactive elements have meaningful accessible names.

## Error messages framework

A good error message does three things, in order:
1. **What happened** — name the problem in plain language.
2. **Why** — only if it helps the user act (skip if it doesn't).
3. **How to fix it** — the concrete next step or recovery path.

Rules: never blame the user ("You entered an invalid…" → "That email doesn't look right"). Keep technical codes out of the primary message (offer a code secondarily for support if needed). Keep the tone calm — match the stakes, don't amplify them. See `references/error-message-patterns.md` for before/after patterns across required fields, formats, credentials, network failures, permissions, not-found, rate limits, destructive confirmations, and form- vs field-level errors, plus placement and timing guidance.

## Voice & tone

Define a **voice** (the product's consistent personality) and adapt **tone** to context (voice stays the same; tone shifts with the situation). A celebratory empty state and a serious data-loss error share a voice but call for very different tones. See `references/voice-and-tone.md` for defining voice attributes, a tone-by-context table, capitalization and punctuation conventions, preferred/avoided word choices, and inclusive plain-language guidance.

## Review mode

When critiquing existing copy, work through this checklist and propose rewrites as **before → after** pairs:

- Is it clear at a glance, or does it need re-reading?
- Does it lead with the user's goal?
- Can words be cut without losing meaning?
- Any jargon, acronyms, or internal terms?
- Do CTAs use specific action verbs, or vague ones ("OK," "Submit")?
- Is terminology consistent with the rest of the product?
- Sentence case (unless the style guide says otherwise)?
- For errors: does it cover what/why/how without blaming the user or leaking codes?
- Is the tone appropriate to the context?
- Does it work for a screen reader and not depend on color/icon alone?

Present each issue with the original, the rewrite, and a one-line reason.

## Editing code

When the change lands in code, write the copy directly into the relevant components or string files. Match the project's existing approach:
- If an **i18n / localization** system exists (e.g., a `messages` / `locales` / translation file or hook), add or update keys there rather than hardcoding strings, and follow the existing key-naming convention.
- If strings are inline, place them where comparable copy already lives and match the surrounding style.
- Keep one source of truth — reuse an existing key for a repeated phrase instead of duplicating it.
