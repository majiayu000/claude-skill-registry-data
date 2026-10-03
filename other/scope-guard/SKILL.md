---
skill_id: scope-guard
name: Scope Guard — catch scope creep + draft the boundary reply
description: "Decide whether a request is scope creep — \"is this in scope\", \"is this scope creep\", \"should I push back on this client request\", \"draft a boundary reply\". Returns in-scope, creep or grey-zone with a suggested reply."
version: 1.0.0
category: operational
office: coo
lead_agent: planner
everyday_skill: true
triggers:
  - "is this in scope"
  - "is this scope creep"
  - "should I push back on this client request"
  - "draft a boundary reply"
collaborates_with:
  - planner
  - negotiation-specialist   # the boundary-reply phrasing
references:
  adr_moat_framing: documents/ADRs/ADR-007-behavioral-moat-framing-doctrine.md
  adr_confidence: documents/ADRs/ADR-010-confidence-tag-technical-educator-rubric.md
confidence_default: 🟢 HIGH
---

# Scope Guard

> **Does:** spots scope creep in a client request and drafts a polite, firm boundary reply.
> **Solves:** saying yes to free extra work without noticing.
> **Triggers on:** *"is this in scope"* + the client message · *"draft a boundary reply"*

## How Maxim does this (not a generic "say no" template)

Compares the incoming request against the agreed scope (paste the SOW/proposal, or describe it). Returns a verdict — **in-scope / creep / grey-zone** — with the *specific* clause or expectation the request exceeds, then drafts a reply via `negotiation-specialist` that holds the line **without damaging the relationship** (offers a change-order path, not a flat refusal).

## Behavioral overlay

- **Frameworks (cited per ADR-007):** **Loss Aversion** (frame the change-order as protecting *their* timeline/quality, not your time) · **Anchoring** (re-anchor to the original agreement) · **Commitment & Consistency** (Cialdini — "as we scoped…") · **Boundary-setting** (assertive, non-defensive language).
- **Tone-safe:** the reply is firm + warm by default; it never threatens or guilt-trips.
- **Confidence tag (ADR-010)** on the verdict — 🟡 if the original scope wasn't supplied (it'll ask).

## Output

Verdict (in-scope / creep / grey-zone) · the exact expectation exceeded · a ready-to-send boundary reply with a change-order option.
