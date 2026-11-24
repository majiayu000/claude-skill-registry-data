---
name: conversion-cro
description: "Landing pages built around one goal and one action."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [web, design, conversion]
    category: web
    related_skills: [web-design, trust-design, ab-testing]
    web_designer_stages: [copy, direction]
---

# Conversion and CRO Skill

A landing page is designed around one goal: one page, one promise, one call to action repeated with identical wording. This skill covers defining the single conversion before designing, removing competing exits, placing proof beside the claim it supports, and proposing the test order. Load-on-demand only, loaded by the web-designer coordinator for its stages; never auto-loads; never contacts the user directly — the coordinator is the only router.

## When to Use

- For landing, signup, checkout and lead-capture pages where a single action is the point.
- At the direction stage, when the chosen direction must serve one goal rather than several.
- At the copy stage, when the page copy must answer what, why and what next in under five seconds.
- When a page has several calls to action competing with each other and one must be chosen as the point of the page.
- When a revision changes a conversion element and the test order for the change needs to be proposed.

It is not for pages with several equal goals, where no single action can be the point. It is not a way to claim a conversion lift from a small user test — lifts are measured by A/B testing on live traffic, not asserted from a design review.

## Prerequisites

- The run is active, the coordinator loaded this skill for its stage(s).
- The single conversion is defined before designing: what the visitor must do, and what success looks like.
- The brief is settled, so the promise the page makes matches the brief's primary action and audience.
- The ab-testing skill is available for the test order this skill proposes.
- Proof exists or can be supplied: real names, real results, real badges — nothing fabricated.

## How to Run

1. Define the single conversion before designing anything: one page, one promise, one goal.
2. Remove competing navigation and exit leaks on the landing page, so the one action is the obvious path.
3. Place the first call to action above the fold, and repeat it with identical wording after each proof section.
4. Keep message match: the headline continues the promise the visitor arrived with.
5. Put social proof near the conversion point, beside the claim it supports, and handle objections and risk reversal on the page.
6. Ask for the minimum form fields, design mobile-first, and keep LCP under 2.5s.
7. Propose the test order: headline, CTA wording, hero image, form length, proof placement — one variable at a time.
8. Check the first screen as a stranger would: what, why and what next must all be answerable in under 5 seconds, before scrolling.
9. Confirm the form asks only for what the conversion needs; each extra field is a reason to leave.
10. Check the page at the mobile width first, since the landing page is designed mobile-first and the first screen is smallest there.
11. Place risk reversal where the visitor hesitates — near the conversion point, not in a footer.
12. Record the test order with the page, so the next revision starts from the next variable in the order rather than from opinion.

## Quick Reference

- Structure: one page / one promise, one call to action repeated with identical wording.
- First call to action: above the fold, repeated after proof sections.
- Message match: headline continues the ad's promise.
- Proof: social proof near the conversion point, beside the claim it supports.
- Form: minimum fields.
- Performance: LCP under 2.5s; mobile-first.
- Test order: headline, CTA wording, hero image, form length, proof placement — one variable at a time.
- First screen: answers what, why and what next in under 5 seconds.
- Proof rule: specific and verifiable; never fabricated testimonials, ratings or badges.
- Form: each field must be needed for the conversion; extras are reasons to leave.
- Mobile-first: the first screen is checked at the mobile width first.
- Risk reversal: placed where the visitor hesitates, near the conversion point.

## Procedure

### 1. What it is

Designing a page around one goal: one page/one promise, one CTA repeated with identical wording, message match (headline continues the ad's promise), social proof near the conversion point, objection handling, risk reversal, minimum form fields, mobile-first, LCP under 2.5s, test one variable at a time.

### 2. How Hermes applies it

Hermes defines the single conversion before designing, removes competing nav/exit leaks on landing pages, places the first CTA above the fold and repeats it after proof sections, and proposes the test order: headline, CTA wording, hero image, form length, proof placement.

### 3. What it returns to the stage

The copy stage record in `gateway/web_designer/machine.py` (`STAGE_RECORDS`) requires `pages` and `meta`, and the direction stage record requires `directions` and `chosen`. This skill's work fills the copy record with the landing-page copy — the headline, the repeated call to action in identical wording, the proof placed beside its claim, and the objection and risk-reversal copy — and fills the direction record with the chosen direction serving the single conversion. A page recorded with two competing calls to action, or a first call to action below the fold, is not recorded as a conversion page. The proposed test order is recorded with the page, one variable at a time.

The proof recorded with the page is specific and verifiable: a named result, a rating, a badge — placed beside the claim it supports, not in a distant section. Where proof was claimed but not supplied, the record notes it as missing rather than inventing it, since fabricated testimonials, ratings or badges are never acceptable.

The test order exists so that revisions improve the page one variable at a time instead of redesigning it on opinion: headline, CTA wording, hero image, form length, proof placement. Each test answers which performs better, and the order is recorded with the page so the next revision continues it rather than restarting it. A page whose test order is not recorded is a page whose next revision has no starting point.

### 4. Good looks like

The first screen answers what, why and what-next in under 5 seconds; one CTA, repeated; proof sits beside the claim it supports.

A first screen that answers what, why and what next in under five seconds is a screen that did its job. The five seconds are the test, not the layout. Where the visitor must scroll to learn what the page offers, the page has already lost the conversion it was built for. That is why the first call to action sits above the fold, and why proof sits beside the claim it supports.

## Pitfalls

- Two or more competing calls to action, so no single action is the point.
- A first call to action below the fold, or repeated with different wording each time.
- Navigation and exit leaks left on a landing page, draining visitors away from the one goal.
- Proof placed far from the claim it supports, where it cannot help the decision.
- A headline that breaks message match with the promise the visitor arrived with.
- Asking for form fields the conversion does not need.
- Claiming a conversion lift from a small user test instead of measuring it with A/B testing.
- Fabricated testimonials, ratings or badges used as proof where real proof was not supplied.
- A first screen that needs scrolling before what, why and what next can be answered.
- An extra form field that the conversion does not need.
- Risk reversal buried in a footer, far from where the visitor hesitates.
- Starting the next revision's test from opinion instead of the recorded test order.

## Verification

- One goal, one promise, one call to action repeated with identical wording.
- The first screen answers what, why and what next in under 5 seconds; the first call to action is above the fold.
- Proof sits beside the claim it supports; objections and risk reversal are handled on the page.
- Form fields are the minimum needed; LCP is under 2.5s.
- Proof is specific and verifiable; no fabricated testimonial, rating or badge is present.
- The test order is recorded with the page, one variable at a time.
- Every form field is needed for the conversion.
- The first screen is checked at the mobile width first.
- Risk reversal sits near the conversion point.
- The content judger checks the related copy rules and the performance judger checks LCP. The skill does the work and the judgers check it; the skill never grades its own output.

## Coordinator wiring

Loaded by stages: copy, direction. Returns: copy stage-record keys `pages`, `meta` and direction stage-record keys `directions`, `chosen`, with the single conversion and the repeated call to action. Judger boundary: content judger checks the related copy rules; performance judger checks LCP.
