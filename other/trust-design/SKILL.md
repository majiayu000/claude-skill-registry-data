---
name: trust-design
description: "Proof placed where conviction peaks, never fabricated."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [web, design, trust]
    category: web
    related_skills: [web-design, conversion-cro]
    web_designer_stages: [copy, wireframe]
---

# Trust and Social Proof Design Skill

This skill places proof where conviction peaks: named client results, ratings, logos, testimonials, and security or compliance badges directly beneath the primary CTA. It covers where proof goes, what counts as proof, and how proof is tied to the claim it supports. It does not invent proof, write the underlying copy, or decide the conversion goal — the copy and wireframe stages own those. Load-on-demand only, loaded by the web-designer coordinator for its stages; never auto-loads; never contacts the user directly — the coordinator is the only router.

## When to Use

- Near any CTA, price, form or claim that asks the visitor to trust the site.
- When a landing, signup, checkout or lead-capture page asks for money, data, or a commitment.
- When a claim on the page (a result, a guarantee, a security statement) has no evidence beside it.

It is NOT for:

- Inventing testimonials, ratings, badges, or client logos the user has not supplied.
- Writing long-form copy or the page's value proposition — that is the copy stage's work.
- Deciding the site's single conversion goal — that is set in the brief and scope freeze.

## Prerequisites

- The run is active and the coordinator loaded this skill for its stage(s).
- The brief records the primary action and the audience, so proof can be matched to the decision the visitor is making.
- Any proof used must come from the user or from a source the user supplied; Hermes never fabricates it.

## How to Run

1. Find the decision points: each primary CTA, price, form, and strong claim on the page.
2. For each decision point, pick the proof that answers the doubt at that exact moment — a named client result, a rating, a logo, a testimonial, or a security/compliance badge.
3. Place the proof adjacent to the claim it supports, directly beneath the primary CTA where the decision happens, not in a distant section.
4. Check every proof item is specific and verifiable: a real name, a real result, a real badge. Vague claims are removed or replaced.
5. Record the proof placement in the stage record so the wireframe and copy stages can see it.
6. Hand the work to the judger; do not grade it here.

## Quick Reference

- Proof placement: directly beneath the primary CTA, adjacent to the claim it supports.
- Acceptable proof: named client results, ratings, logos, testimonials, security/compliance badges (SOC 2, ISO 27001, GDPR).
- Never fabricated: no invented testimonials, ratings, or badges.
- Decision driver: risk aversion is often stronger than desire for gain in B2B — proof answers risk, not just desire.

## Procedure

### 1. What it is

Placing proof where conviction peaks: named client results, ratings, logos, testimonials, security/compliance badges (SOC 2, ISO 27001, GDPR) directly beneath the primary CTA — risk aversion is often stronger than desire for gain in B2B.

### 2. How Hermes applies it

Hermes puts proof adjacent to the claim it supports (not in a distant section), uses specific, verifiable proof over vague claims, and never fabricates testimonials, ratings or badges.

### 3. What it returns to the stage

- `copy` stage — `pages`: each page's copy notes which proof sits beside which claim and beneath which CTA.
- `copy` stage — `meta`: nothing new; proof does not change page metadata.
- `wireframe` stage — `pages`: each wireframe page records the proof blocks placed beneath the primary CTA and beside the claims they support, with their source noted.

### 4. Good looks like

A sceptical visitor sees a real name, a real result or a real badge at the moment they decide — not three screens later.

## Pitfalls

- Fabricated testimonials, ratings, or badges — proof the user never supplied is never written.
- Proof parked in a distant section while the CTA stands alone; proof only works beside the claim it supports.
- Vague claims ("trusted by thousands", "best in class") with no specific, verifiable evidence behind them.
- A badge shown for a certification the site does not hold.
- Proof that answers a doubt nobody at that decision point has, while the real doubt goes unanswered.

## Verification

- Every primary CTA has proof directly beneath it or beside the claim it supports.
- Every proof item is specific and verifiable: a real name, a real result, or a real badge.
- No proof item is invented: each one traces to the user or a supplied source.
- The content judger checks the proof placement and the honesty of the claims; the skill does the work and the judger checks it. The skill never grades its own output.

## Coordinator wiring

Loaded by stages: copy, wireframe. Returns: `copy` — `pages`, `meta`; `wireframe` — `pages`. Judger boundary: content judger checks proof placement and claim honesty.
