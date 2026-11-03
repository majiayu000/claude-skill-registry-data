---
name: verify-before-claim
description: Pre-commit verification floor for two specific claim shapes that recur at decision points — vendor-specific quantitative claims (price, rate limit, free-tier coverage, supported tickers/exchanges) and codebase-state claims ("we already inject X", "the system already validates Y"). When typing either shape, stop and verify against the canonical source — the vendor's own URL for vendor claims, the file itself this session for codebase-state claims. Use this whenever drafting an ADR, doctrine entry, handoff, sparring reply, or review verdict that hangs on a quantitative vendor fact or a "the existing code does X" claim. The behavioral why and source cases live in `feedback_decision_claims_need_source_and_confidence.md`; this skill is the procedural floor that fires at the moment of typing.
metadata:
  version: "1.0.2"
---

# Verify before claim

Run this skill at the moment you are about to type a decision-shaping claim that fits one of two shapes. The verification cost is low (one fetch or one Read tool call); the risk of skipping cascades into doctrine, ADRs, budget, or design choices that have to be unwound when reality differs.

## When this fires

Two specific claim shapes:

**Shape 1 — vendor-specific quantitative claims:**

- "X costs $Y/mo" (vendor pricing tier).
- "X has a free tier" (coverage claim about a vendor).
- "Y rate-limits at Z calls/min" (vendor rate limit).
- "Provider P supports exchange E" (vendor coverage).
- "Tier T includes feature F" (vendor coverage).

**Shape 2 — codebase-state claims:**

- "the system already X".
- "X is already wired up".
- "we already enforce Y at layer Z".
- "we already inject / abstract / validate / serialize / log / journal X".
- "the existing code does X".
- "this is handled by X".

## Pre-flight

1. Identify which shape the claim fits (vendor-quantitative or codebase-state). Both shapes can apply to the same claim — handle both checks if so.
2. Decide whether the claim is decision-shaping. Critical decision points: architecture choices, provider/tool/library selection, doctrine ratifications, scope decisions, anything recorded in an ADR or doctrine doc, anything where undoing would cost meaningful work. If exploratory or informational with no decision riding on it, the floor relaxes — the rule remains stance-level (cite confidence, not proof).
3. Open this session's terminal — recall-only verification does not count.

## Procedure for vendor-quantitative claims

The verification floor is **the vendor's own canonical page**. Not:

- A third-party article citing the vendor.
- A search snippet.
- A blog or comparison site.
- Training-data prior.

**Pre-commit check before quoting any vendor-specific number:**

> *"Did I read this from {vendor}'s own page (URL), or from someone else citing them? If the latter, can I read the canonical page in one more fetch — and if yes, why haven't I?"*

If you cannot cite the vendor's own URL, either (a) fetch it now via WebFetch, or (b) flag the number as "per third-party source X, unverified against vendor canonical." The unverified flag must accompany the number wherever it propagates (ADR, doctrine doc, budget, brief).

Surface conflicting sources explicitly. If one source says "5 calls/min, 500/day" and another says "25 calls/day," mention both and note the discrepancy. Do not silently pick one and present it as fact.

## Procedure for codebase-state claims

The verification floor is **the file itself, this session**. Cite path + line range when making the claim. Format: `[file.py:L<start>-L<end>]`.

**Pre-commit check before any "the codebase already does X" claim:**

> *"Did I open this file in this current session, or am I claiming from prior-context recall? If recall, open it now or flag the claim as unverified."*

Open via Read tool with the line range that supports the claim. Do not paraphrase the file; cite the slice. If the claim is broader than what the slice supports, narrow the claim or open more of the file.

## Output shape

A claim that passes this skill carries one of:

- **Verified vendor claim:** `<claim>. Source: <vendor canonical URL>.`
- **Verified codebase-state claim:** `<claim>. Source: [file.py:L<start>-L<end>].`
- **Flagged unverified:** `<claim>, per <third-party source>, unverified against {vendor canonical | the file this session}. Will verify before propagation.`

The unverified flag must propagate with the number/claim through subsequent artifacts. Do not strip the flag silently.

## Common failure modes

- Citing tier pricing from a search snippet. Pricing pages reorganize; tiers rename; the snippet is stale.
- Treating "we already X" as too obvious to need a citation. Confident claims about codebase state are exactly where blast radius cascades.
- Stopping at search results when one more fetch would land on the canonical page.
- Generalizing a vendor claim from one feature description ("free tier = US-only") to another endpoint or region without specific verification.
- Citing path without line range — `auth.py` is not enough; the claim depends on the specific symbol or function.

## When this skill does NOT fire

- Exploratory conversation with no decision riding on the claim.
- Brainstorming where ranges are explicitly placeholders.
- Recall-from-prior-context where the prior context is THIS session and the claim is about a file already opened in this turn (re-citing the same Read output is fine).
- General factual answers where the claim is not vendor-quantitative or codebase-state shaped (e.g., "Python uses indentation" — not vendor, not codebase-state).

## Related memories and skills

*(The rules set was parked whole at `98c0946`; the files below are the **source cases** that produced
these checks, not rules that still bind.)*

- `~/.claude/rules_parked/feedback_decision_claims_need_source_and_confidence.md` — core rule (decision-time stance), source cases (Finnhub vs Alpha Vantage 2026-04-24; Finnhub Premium pricing 2026-04-25; codebase-state extension 2026-05-01), behavioral why, meta-honest note.
- `~/.claude/rules_parked/feedback_user_state_correction_is_alert.md` — when user corrects state, re-verify fully. This skill is the verification step.
