---
name: client-intake-builder
description: Generate a branded, single-file HTML client intake questionnaire for any service business. Picks the right question set (brand identity, web design, automation project, or pre-call brief), styles it with the project's brand colours and fonts, and includes validation, progress, and a success state. Pairs with php-form-mailer to make it send email. Use when the user says "intake form", "client questionnaire", "project brief form", or "onboarding form".
---

# Client Intake Builder

You build the form a client fills in before the first real conversation. A good intake questionnaire does two jobs at once: it gathers the answers the project actually needs, and it shows the client they are dealing with a professional before any work begins. The form is part of the brand.

## Step 1: Establish the brief

Ask (or take from the request):

1. **Service type**, which selects the question bank:
   - `brand` for brand identity / logo projects
   - `web` for website projects
   - `automation` for automation / systems projects
   - `precall` for a short pre-call brief before a discovery call
2. **Brand styling**: if the project folder has a site or brand CSS, read the colours and fonts from it. Otherwise ask for 2 or 3 brand colours, a font preference, and the business name for the header.
3. **Anything unusual to ask** beyond the standard bank.

## Step 2: Plan the questions

Build sections A to E from the bank for the chosen type. Keep the total under 20 questions; an intake form that takes more than 10 minutes does not get finished.

### Question banks

**brand**: A. The business (name, what it does, years active) · B. The project (new brand or rebrand, what triggered it, deadline) · C. Audience and market (ideal customer, main competitors, how they differ) · D. Taste (3 brands they admire and why, words their brand should and should not feel like, colour likes/dislikes) · E. Logistics (budget range as radio bands, decision maker, how they found you)

**web**: A. The business · B. The site (purpose, must-have pages, current site and what fails about it) · C. Content (who writes copy, what exists, photography) · D. Taste (3 sites they like and why, features seen elsewhere) · E. Logistics (budget bands, deadline, hosting/domain status)

**automation**: A. The business · B. The pain (the repetitive task, hours per week it costs, who does it now) · C. The stack (tools in use, where the data lives, what must not change) · D. The win (what done looks like, how they would measure it) · E. Logistics (budget bands, urgency, technical contact)

**precall**: One short section, 6 questions max: what they need, what prompted it now, timeline, budget band, decision maker, anything they want you to see before the call.

Every multiple-choice question gets explicit `value` attributes plus human-readable labels, so a mail handler can map them later.

## Step 3: Generate the HTML file

One self-contained file: `intake-<type>.html`. Requirements:

- All CSS and JS inline. The only allowed external request is a Google Fonts link if a webfont was chosen; offer a system-font fallback for zero external requests.
- Branded header with the business name, the section structure A to E with visible progress, and a closing reassurance line about confidentiality.
- Every input has a `<label>`, required fields are marked, and the form validates name and email in JS before submit.
- A hidden honeypot field named `website` for spam protection.
- A styled success state that hides the form on submission.
- Mobile-first layout, readable at 360px wide, keyboard navigable, `prefers-reduced-motion` respected if anything animates.
- No analytics, no trackers, no external JS.

The form `action` is left as a clearly marked placeholder.

## Step 4: Wire it up

The form needs a backend to send email. If the `php-form-mailer` skill is installed, offer to run it on the generated file next. Otherwise point the user at the placeholder `action` and the README of their form backend of choice.

## Rules

- Never invent the user's services, prices, or budget bands. Budget radio bands come from the user.
- Ask for brand colours once; never default to a generic template look if brand assets exist in the project.
- Keep the client's perspective in the microcopy: questions in plain language, no industry jargon the client will not know.
- The intake answers are client-confidential by design. Do not add features that send data anywhere except the user's own form handler.
