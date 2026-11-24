---
name: ux-copywriting
description: "Plain headlines that state what, for whom and why."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [web, design, copy]
    category: web
    related_skills: [web-design, microcopy, content-hierarchy]
    web_designer_stages: [copy]
---

# UX Copywriting Skill

Writing in the brand's voice for headlines, sections and pages — plain language, one idea per paragraph, conclusion first. This skill covers hero copy, section copy and longer pages, and is distinct from marketing puff. Load-on-demand only, loaded by the web-designer coordinator for its stages; never auto-loads; never contacts the user directly — the coordinator is the only router.

## When to Use

- For hero copy, section copy, About/product pages and any text longer than a label.
- At the copy stage, when the copy skeleton becomes finished page copy.
- When a headline hides its meaning behind cleverness and needs to state what the thing is instead.
- When a section reads well aloud but a scanner cannot get its point from the heading alone.
- When the voice differs from page to page and the brand needs to sound like one brand again.

It is not for button labels, field hints or error messages — that is microcopy. It is not for slogans, and it is not for text that sounds good while saying nothing.

## Prerequisites

- The run is active, the coordinator loaded this skill for its stage(s).
- The brief is settled, so copy can state what the thing is, who it is for and the outcome, against a known audience and primary action.
- The brand voice is recorded, so tone matches the brand on every page.
- The microcopy skill is available for the labels and hints that sit inside the longer copy.
- The content-hierarchy skill is available, since headings must form a readable outline on their own.

## How to Run

1. Write headlines that state what the thing is, who it is for and the outcome — not slogans.
2. Put the conclusion first (inverted pyramid), then the supporting detail.
3. Keep one idea per paragraph, in plain language, with descriptive headings that say what the section holds.
4. Keep the voice consistent across pages; the same brand must sound like the same brand everywhere.
5. Check every headline against the five-second test: a stranger must be able to answer what, why and what next in under 5 seconds.
6. Cut jargon and clever headings that hide meaning; if a heading needs explaining, rewrite the heading.
7. Read the headings alone, in order, and confirm they form a readable outline of the page.
8. Read the finished copy once as a stranger would, in one pass, and cut anything that does not survive that read.
9. Write the meta title and description from the same plain language as the page, not from the slogan.
10. Cut any paragraph that repeats what the heading already said; the heading carries the point, the paragraph carries the detail.
11. Check the copy at the mobile width, where long paragraphs fail first and headings carry more of the meaning.
12. When the voice drifts on one page, fix the page to the recorded voice rather than rewriting the voice to fit the page.

## Quick Reference

- Headline test: answers 'what, why, what next' in under 5 seconds.
- Structure: inverted pyramid — conclusion first.
- Paragraphs: one idea per paragraph.
- Headings: descriptive, not clever.
- References: GOV.UK and Mailchimp style guides are the standard free references.
- Voice: consistent across pages, matching the brand.
- Outline test: headings alone, in order, form a readable outline of the page.
- Stranger test: copy a stranger can understand in one read.
- Meta: titles and descriptions in the same plain language as the page.
- Repetition: a paragraph that repeats its heading is cut.
- Mobile: copy checked at the narrow width, where long paragraphs fail first.

## Procedure

### 1. What it is

Writing in the brand's voice for headlines, sections and pages — plain language, one idea per paragraph, inverted pyramid (conclusion first), descriptive headings — distinct from marketing puff; GOV.UK and Mailchimp style guides are the standard free references.

### 2. How Hermes applies it

Hermes writes headlines that state what the thing is, who it is for and the outcome (not slogans), keeps voice consistent across pages, and its judger checks a headline answers 'what, why, what next' in under 5 seconds.

### 3. What it returns to the stage

The copy stage record in `gateway/web_designer/machine.py` (`STAGE_RECORDS`) requires `pages` and `meta`. This skill's work fills the `pages` key with the finished copy for each page — headlines, sections and body text written in the brand voice — and the `meta` key with the titles and descriptions that carry the same plain language. Copy that states a slogan instead of what the thing is, who it is for and the outcome is not recorded as finished. The five-second headline check is recorded per page, so a headline that fails it is visible in the record rather than silently shipped.

The `meta` entries carry the same discipline as the page copy: titles and descriptions state what the page is and what it offers, in plain language, rather than repeating a slogan. A page whose headings alone do not form a readable outline is recorded with that gap, so the outline test is part of the stage record rather than a private judgement.

The five-second test is the standard the copy is held to, and it is applied per page, not once for the site: a headline that passes on the home page and fails on a product page is a failure on that page. The record therefore holds the check per page, so the judgement is visible where the copy lives. Voice consistency works the same way — the recorded voice is the standard, and a page that drifts is fixed to the voice, never the other way round.

### 4. Good looks like

Copy a stranger can understand in one read; no jargon, no clever heading that hides its meaning; tone matches the brand on every page.

Copy that a stranger understands in one read is copy that did its job. The single read is the test, not the word count. Where a heading needs explaining, the heading has failed, and rewriting the explanation does not fix it. That is why the five-second test is applied per page, and why a clever heading is cut rather than defended.

## Pitfalls

- A slogan in place of a headline that states what, for whom and why.
- A clever heading that hides its meaning, so the reader must guess what the section holds.
- Jargon a stranger cannot understand in one read.
- Burying the conclusion at the end of a long paragraph instead of leading with it.
- A voice that changes from page to page, so the brand sounds like several brands.
- Writing marketing puff and calling it UX copy.
- Headings that do not form a readable outline on their own, so a scanner gets nothing from them.
- A title or description that repeats the slogan instead of stating what the page is.
- A meta title or description that repeats the slogan instead of the page's plain language.
- A paragraph that repeats its heading instead of adding detail.
- Rewriting the recorded voice to fit a page that drifted, instead of fixing the page.

## Verification

- Every headline states what the thing is, who it is for and the outcome.
- A stranger can answer what, why and what next from the headline in under 5 seconds.
- No jargon and no clever heading that hides its meaning; one idea per paragraph.
- Tone matches the brand on every page.
- Headings alone, in order, form a readable outline of the page.
- Titles and descriptions state what the page is, in the same plain language as the page copy.
- Meta titles and descriptions use the same plain language as the page.
- No paragraph repeats what its heading already said.
- Copy is checked at the mobile width.
- The content judger checks the related copy rules: clarity, honesty and the headline test are judged there. The skill does the work and the judger checks it; the skill never grades its own output.

## Coordinator wiring

Loaded by stages: copy. Returns: copy stage-record keys `pages`, `meta`. Judger boundary: content judger checks the related copy rules.
