---
name: triage
description: 'Read-only grounding phase for a card — every card''s pickup. `/super-bootstrap:triage {ID}` dispatches the `triage` subagent (inherit — the session owner''s model) to ground the card cold — premise verify, aim validate, blast collect — and append a Verdict block — `## Verdict — auto-fix · {date}` (Fix-shape / Probe-deps / Execution tags) or `## Verdict — surface · {date}` (a fork the gateway climbs before any user hand-off) — to `docs/work/{ID}.md`. No code changes — the fix is a separate phase. Use at raw-card pickup (a card with no Verdict block) or when the user asks to triage/investigate a BUG/DEBT/GAP item.'
tags: [triage, verdict, card, pipeline]
---

# Triage — Read-Only Grounding Phase

Grounding pickup lane for a card. The thinking runs in the `triage` subagent (`agents/triage.md`, `model: inherit` — the session owner's model is the top tier); this skill is the dispatch shell + absorption protocol. The agent grounds the card cold — premise verify, aim validate, blast collect — sizes the fix, appends a Verdict block to the card; the fix is a later phase that inherits the verdict as its context scope.

## Arguments

| Invocation | Behavior |
| --- | --- |
| `/super-bootstrap:triage BUG-012` (any `BUG/DEBT/GAP-###` ID) | Dispatch the `triage` subagent on that card. |
| `/super-bootstrap:triage` (bare) | List open cards with no Verdict block yet; the user picks one, then dispatch. |

## Execution

1. Resolve the card: Glob `docs/work/` first (loads no file content, so the check fires no `docs/**` path-scoped rule) — nothing back → the repo carries no card substrate, whatever else tracks its work; print "No runway installed. Run `/super-bootstrap:setup` to set up the pipeline." and stop. Substrate present → the card file `docs/work/{ID}.md` exists; missing → report "no card {ID}", stop. A Verdict block already present in the card → surface its kind and date instead of re-dispatching (re-triage only on explicit user ask).
2. Dispatch: `Agent` tool, `subagent_type: "triage"`, prompt = the card ID + today's date + the gateway-aligned problem-aim when framing sharpened or corrected the card claim (premise / problem / scenario only). Exclude cause theories and fix preferences (bias-input exclusion) — the aligned aim is the user-validated target, not a prior; the card row carries the frozen claim.
3. Absorb the agent's report (`agents/triage.md` § Reporting):
   - **DONE / DONE_WITH_CONCERNS** — relay verdict + card path. auto-fix Verdict block → post the route line off its `Execution:` tag (inline / phased → implement within the envelope, skipping what the tag skips; full → cluster route per CLAUDE.md). surface Verdict block → climb before any hand-off: `docs/decisions.md` closed forks, then the specs / project docs, then the aligned aim (one option contradicts it → the other wins), then the proxy the verdict's `settles by:` names, run in its sized container — an `inline read` runs here; a `dispatched probe` or `phased build` is a route change, so the framing + route line re-fires (CLAUDE.md § Framing + Route) and the measurement dispatches or lands as a plan block (gateway doesn't build — CLAUDE.md § Dispatch) — a fork that resolves there lands as a `## Design — {date}` block naming the settling source, and the route line follows; only a fork inside business / risk / preference / private authority reaches the user as the verdict's `## Decision needed`, then wait for the ruling. User picks an option (the verdict's recommendation as-is counts) → the gateway appends a `## Design — {date}` block (shape, and how a wait ruling names its party: `docs/work/README.md` § Thread contract, Design line); user drops the card → delete the card file (resolve).
   - **NEEDS_CONTEXT** — relay the named gaps; the answer returns as an `## Amendment` append on the card — via `/super-bootstrap:log` (its amend path) or directly by the answering session.
   - **NEEDS_GRANTS** — grant the named tooling and re-dispatch; user round-trip only when the grant itself is user-owned (cost, consent).
   - **BLOCKED** — premise wrong; relay the counter-diagnosis to the user.
4. The verdict artifact rides the session's normal envelope commit — no in-phase commit.

## Rules

- **Dispatch, don't investigate.** The verdict judgment runs in the subagent's clean context; gateway priors corrupt it.
- **Check the verdict aim.** The gateway holds the aligned problem-aim; a verdict that re-aims the problem gets surfaced to the user, not absorbed (CLAUDE.md § Framing + Route).
- **Weigh the verdict's grounding.** A verdict resting on design-prose deduction over direct evidence is unproven — surface it for re-grounding, not adoption and not a competing gateway theory.
- **One card per dispatch.** A batch fans out — each dispatch's write set is its own `docs/work/{ID}.md` (`agents/triage.md` § Phase identity), so concurrent grounding keeps verdicts per-card atomic. The gateway's absorb of each verdict (step 3) stays serial.
- **Verdict block is the state.** No status fields anywhere — a Verdict block's presence says the card is grounded, its kind (auto-fix / surface) says whether a fork is still open — `/super-bootstrap:needs-me` reads an unruled `surface` as needing the user; `/super-bootstrap:autorun` grounds an ungrounded card itself.
- **Cleaner:** the session resolving the card deletes the card file (doc-sync temporal cleanup).
