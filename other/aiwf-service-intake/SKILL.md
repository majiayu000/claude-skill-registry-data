---
name: aiwf-service-intake
description: Use for Ai Embedded Systems service leads, website/workflow/bot/training inquiries, AI fit checks, project scoping, quote discovery, constraints, and first-pass deliverables.
---

# AIWF Service Intake

## Core Rule

Turn a lead into a scoped first pass, not a vague AI project. Identify the buyer's current workflow, desired win, systems/files involved, users, timeline, budget range, decision status, risks, and the smallest useful deliverable.

## Workflow

1. Classify the lead lane: website work, workplace workflow, AI model/bot, AI fit consultation, marketing/SEO, employee AI training, embedded prototype, robotics/Rnv1, or mixed scope.
2. Extract the concrete problem: what is happening now, who feels the pain, how often it happens, what would count as a win, and what evidence/files/screenshots exist.
3. Decide whether AI is actually needed. A form, script, spreadsheet rule, checklist, website fix, or training session may be cheaper and safer.
4. Define a first-pass deliverable: audit, page fix, workflow map, bot plan, prototype outline, training session, risk report, or quote-ready implementation plan.
5. List what is needed from the customer before work starts.

## Guardrails

- Do not sell a broad AI retainer when a small scoped pass will answer value and risk faster.
- Keep private customer data out of public docs and training artifacts.
- Separate decision-maker, recommender, and end-user needs.
- Add `aiwf-security-guardrails` for private files, credentials, customer data, auth, or public deployment.
- Add `aiwf-fastapi-coding`, `aiwf-react-coding`, `aiwf-vue-vitepress-coding`, `aiwf-web-seo`, or another focused skill only after the scope becomes implementation.
- Add `aiwf-networking-iot`, `aiwf-embedded-edge-ai`, or `aiwf-robotics-systems` for hardware, devices, or robotics leads.

## Output Shape

For an intake result, provide:

- lane and likely buyer need
- smallest useful first pass
- required inputs
- risks and privacy notes
- proposed validation or acceptance criteria
- next quote/discovery question list

## Primary Source Anchors

- Ai Embedded Systems services page: https://aiembeddedsystems.com/services/
- Ai Embedded Systems contact page: https://aiembeddedsystems.com/contact/
- Ai Embedded Systems timeline: https://aiembeddedsystems.com/timeline/

Use the current website as the source of truth for public service categories and intake language.
