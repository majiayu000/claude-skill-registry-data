---
name: microcopy
description: "Small words at the exact moment of action."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [web, design, copy]
    category: web
    related_skills: [web-design, ux-copywriting, form-validation]
    web_designer_stages: [copy, components]
---

# Microcopy Skill

Microcopy is the smallest copy: button labels, form labels and helpers, tooltips, error messages, confirmations and calls to action. This skill covers writing those words at the exact moment of action, so each one guides the decision in front of the user. Load-on-demand only, loaded by the web-designer coordinator for its stages; never auto-loads; never contacts the user directly — the coordinator is the only router.

## When to Use

- On every button, field, hint, error and confirmation — the highest-leverage words on most sites.
- At the copy stage, when labels and hints are written alongside longer copy.
- At the components stage, when a component's labels, helpers and errors are defined with the component itself.
- When a form field makes users hesitate and a helper line could answer the doubt at that exact moment.
- When an error message says something failed without saying what to do about it.

It is not for headlines, sections or long pages — that is UX copywriting. It is not for generic labels that describe the control instead of the result the user gets.

## Prerequisites

- The run is active, the coordinator loaded this skill for its stage(s).
- The action each button or field performs is known, so its label can state the result.
- The ux-copywriting skill is available for the longer copy the microcopy sits inside.
- Error and confirmation states exist for the components concerned, so microcopy can be written for each of them.
- The form-validation skill is available, since error wording and validation timing belong together.

## How to Run

1. Write every button label as the result the user gets, not as the chore: 'Get my free quote', not 'Submit'.
2. Add helper text that reduces anxiety at the exact moment of doubt — for example, 'Takes 2 minutes'.
3. Write every error as the fix: name what went wrong and what to do about it.
4. Write confirmations that say what happened and what happens next.
5. Keep each piece under three sentences; most are a few words.
6. Check every label, hint, error and confirmation in place, on the component it belongs to, before the component is used on a second page.
7. For each field, name the doubt a user has at that exact moment and confirm the helper answers that doubt, not a different one.
8. For each error state, confirm the message names the fix and the field it belongs to, so the user never has to guess where the problem is.
9. Write tooltips that answer the question the control raises, not a description of the control itself.
10. Check confirmations after the action they confirm, in the state the user sees next — not in isolation.
11. When a component is reused, confirm its microcopy still fits the new context; a label that fit one page may mislead on another.
12. Read all the microcopy on a page in order, as the user meets it, and cut any piece that adds no guidance.

## Quick Reference

- Length: under three sentences (NN/g definition).
- Button labels: the result the user gets — 'Get my free quote', never generic 'Submit' / 'OK'.
- Helper text: answers the doubt at that exact moment — for example, 'Takes 2 minutes'.
- Errors: name the fix, never generic 'Invalid input'.
- Confirmations: what happened and what happens next.
- Coverage: every button, field, hint, error and confirmation.
- Check: every piece is checked in place, on the component it belongs to.
- Tooltips: answer the question the control raises, not a description of the control.
- Confirmations: checked in the state the user sees after the action.
- Reuse check: microcopy still fits when the component moves to a new context.

## Procedure

### 1. What it is

The smallest copy — under three sentences (NN/g definition): button labels, form labels/helpers, tooltips, error messages, confirmations and CTAs. It guides decisions at the exact moment of action; changing 'Submit' to a result ('Get my free quote') is a classic conversion lift.

### 2. How Hermes applies it

Hermes writes button labels as the result the user gets, adds helper text that reduces anxiety ('Takes 2 minutes'), writes errors that name the fix, and never ships a generic 'Submit'/'OK'/'Invalid input'.

### 3. What it returns to the stage

The copy stage record in `gateway/web_designer/machine.py` (`STAGE_RECORDS`) requires `pages` and `meta`, and the components stage record requires `inventory`. This skill's work fills the copy record with the microcopy for each page — button labels, helpers, tooltips, errors and confirmations — and fills the components inventory with the same words attached to the component they belong to, including its error and empty states. A component recorded with a generic 'Submit', 'OK' or 'Invalid input' is not recorded as finished. Helper text is recorded against the field it reassures, so a hint that answers no doubt at that moment is visible as a gap.

The words travel with their component: when a component is reused on a second page, its microcopy travels with it unchanged, so the same action carries the same words everywhere. A label changed for one page is changed in the inventory, not just on that page, so the two do not drift apart.

Microcopy is the highest-leverage copy on most sites because it sits at the exact moment of action, where a few words decide whether the user proceeds or stalls. That is why each piece is checked in place, on its component, rather than in a list: a label that reads well alone and misleads in context has failed. The record attaches each piece to its page and component so the check is made where the words are met, not afterwards.

### 4. Good looks like

Every button says what happens next; every hint answers the doubt a user has at that exact moment; no label is a chore ('Submit') when it could be a promise.

Words that guide the exact moment of action are words that did their job. The moment is the test, not the sentence. Where a button says 'Submit' and the user hesitates, the label has failed, and no amount of surrounding copy repairs it. That is why each piece is checked in place, on its component, at the moment it is met.

## Pitfalls

- A generic 'Submit', 'OK' or 'Invalid input' shipped anywhere.
- A button label that names the control instead of the result the user gets.
- An error that says something failed without naming the fix.
- Helper text that states the obvious instead of answering the doubt the user has at that exact moment.
- Microcopy written away from its component, so it no longer matches the action in front of the user.
- Writing more than three sentences where a few words would do the job.
- Changing a label on one page without changing it in the inventory, so the same action carries different words on different pages.
- An error message that does not name the field it belongs to, so the user must guess where the problem is.
- A tooltip that describes the control instead of answering the user's question.
- A confirmation checked in isolation, not in the state the user sees next.
- Microcopy that fit one page and misleads on the page the component was reused on.

## Verification

- Every button says what happens next, as the result the user gets.
- Every hint answers the doubt a user has at that exact moment.
- No generic 'Submit', 'OK' or 'Invalid input' remains anywhere.
- Every error names the fix; every confirmation says what happened and what happens next.
- Every error names the field it belongs to.
- Microcopy travels with its component: the same action carries the same words on every page.
- Tooltips answer the question the control raises.
- Confirmations are checked in the state the user sees after the action.
- Microcopy is read in order, as the user meets it, and pieces that add no guidance are cut.
- The content judger checks the related copy rules: label clarity and error wording are judged there. The skill does the work and the judger checks it; the skill never grades its own output.

## Coordinator wiring

Loaded by stages: copy, components. Returns: copy stage-record keys `pages`, `meta` and components stage-record key `inventory`, with microcopy attached to its page and component. Judger boundary: content judger checks the related copy rules.
