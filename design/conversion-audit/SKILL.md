---
name: conversion-audit
description: >
  Audit a landing page or marketing site through one lens: what is the ONE thing this page wants
  the visitor to do, and does every element on the page move them toward it? Reconstructs who
  lands on the page and why, spawns visitor-persona agents to react to it cold, maps the belief
  chain a visitor must climb before acting, inventories CTAs and everything competing with them,
  then delivers a prioritized cut/move/add/rewrite plan. Use whenever the user asks "what do we
  want people to do on this page", "is this page converting", "critique this landing page", "why
  would someone book/buy/sign up here", "audit the funnel on X page", or wants strategic critique
  of page content and structure (not visual polish). Works from frontend code in a repo, a live
  URL via browser tools, or pasted copy/screenshots. Judges persuasion and intent-alignment; for
  flow usability and friction use ux-audit, for visual and aesthetic quality use the impeccable
  critique/audit skills.
---

# Conversion Audit

Every page exists to move a specific visitor toward a specific action. Most pages fail not because they're ugly or broken, but because they never decided what that action is — or decided, then buried it under everything else the owner wanted to say. This skill audits a page the way a visitor experiences it: skeptical, distracted, five seconds from leaving.

The output is not a redesign. It is a verdict on **intent clarity** plus a prioritized list of moves — things to cut, move, add, or rewrite — each justified by visitor behavior, not taste.

## The Core Questions

Everything in this audit reduces to answering these, in order. Do not skip ahead; each depends on the previous.

1. **Who lands here?** Not "the target market" — the actual arriving human: what did they click to get here (ad, search result, referral, nav link), what do they already know, what mood are they in?
2. **What is the ONE action this page wants from them?** One. If the honest answer is "three things," that is Finding #1 and everything downstream inherits it.
3. **What must they believe before they'll take it?** Write the belief chain explicitly: e.g. "these people are real → they've done this for businesses like mine → it worked → it won't be a nightmare to work with them → booking a call is low-risk." Actions have prerequisites; pages that skip a link in the chain leak visitors at that link.
4. **What on the page builds each belief — and what builds nothing?** Every section either advances a belief, removes an objection, or competes with the goal. There is no neutral content: attention is finite, so a section that does no work does negative work.
5. **When the belief is built, is the action obvious, easy, and low-fear?** The CTA question — visibility, wording, competition, and what the visitor imagines happens after clicking.

## Phase 0 — Establish the Goal

Before reading a single section, determine the page's intended action:

- If the user stated it, use it.
- Otherwise infer from the page itself: the primary CTA, where CTAs point, the funnel position. State your inference explicitly ("This page appears to exist to get a strategy call booked") so the user can correct it.
- If you genuinely cannot tell — multiple CTAs with equal weight, no CTA, contradictory asks — **stop and report that as the headline finding.** A page with no discernible goal cannot be optimized, only decided.

Also establish the **arrival context**: enumerate the realistic entry paths (nav from home? Google search for what query? paid ad with what promise? backlink?) and what each arriving visitor already believes. A visitor from a "web design Houston" search and one clicking from the pricing nav item need different first sentences; note when the page can only serve one of them.

## Phase 1 — Gather the Evidence

Pick per what's available; combine when possible:

- **Code in repo**: read the page component(s) top-to-bottom in render order. Extract the actual copy — headlines, subheads, CTA labels, section order. Note what's above the likely fold. Follow every link/CTA target to know where it actually goes.
- **Live page**: use browser tools to load it, screenshot the initial viewport (the real five-second view), scroll and capture the full page, click the primary CTA to verify the next step works and matches the promise.
- **Pasted copy/screenshots**: work from what's given; flag what you can't verify (fold position, link targets).

Record the raw material as a **section inventory**: for each section in order — its message in one sentence, the belief it serves (or "none"), and its CTA if any.

## Phase 2 — Cold-Visitor Persona Swarm

Your own read is contaminated: you know what the page is trying to say. Spawn parallel agents (Agent tool, one message, concurrent) who don't. Give each agent ONLY the page content/screenshots and its persona — **do not tell them the page's goal or your hypotheses.**

Default panel (adjust to the site's audience):

| Persona | Brief |
|---|---|
| **5-second skimmer** | You will read only the headline, subhead, and whatever is visually loud, then decide: stay or leave. Report what you think this company does, for whom, and what you'd do next. |
| **Skeptical buyer** | You've been burned by vendors before. Hunt for reasons NOT to trust this page: vague claims, missing proof, stock-photo energy, anything that smells templated. Report every objection the page raises and whether it answers them. |
| **Ready-to-act visitor** | You already want this service; you arrived to take action. Time how long (in scrolls/clicks) until you can. Report every obstacle between arrival and done. |
| **Wrong-fit visitor** | You're adjacent to the target market but not it. Report whether the page tells you it's not for you (good) or wastes your time / lets you book a bad-fit call (bad). |
| **Comparison shopper** | You have three tabs open with competitors. Report what, if anything, you'd remember about this one in ten minutes, and which tab you'd go back to. |

Require structured returns from each: `first_impression` (what page is, one sentence), `would_do_next` (the honest action, including "close tab"), `bail_points` (where and why), `unanswered_questions`, `strongest_moment`, `weakest_moment`.

Where persona reports agree, that's signal. Where they contradict your Phase 3 analysis, the personas win — they're the visitor.

## Phase 3 — Conversion-Path Analysis

Now analyze deliberately, dimension by dimension:

**Five-second test.** From the initial viewport alone: can a stranger say what's offered, for whom, and why care? Headlines that are clever-but-opaque fail here; personality is allowed only after clarity is achieved.

**CTA inventory.** Count every clickable ask on the page. Classify: primary action, secondary action, exit ramp (nav links, social icons, outbound links). Compute the competition: how many things fight the primary CTA for the click? Check CTA copy — does it say what happens next ("Book a strategy call") or is it vapor ("Get started", "Learn more")? Check repetition: is the primary CTA re-offered after each belief-building section, or does the visitor have to scroll back up?

**Belief-chain coverage.** Take the chain from Core Question 3 and map sections onto it. Mark every link with no supporting content (leak), and every section supporting no link (ballast). Order matters too: proof before claims land weaker than claims then proof; pricing before value framing raises objections early.

**Objection ledger.** List the top 5 objections this specific visitor has (too expensive, too small a shop, will this take forever, what if it doesn't work, why you and not the other tab). For each: where does the page answer it, or does it not?

**Momentum and friction.** Where does the page's energy die — a wall of text, a section that changes topic, a detour to something the owner cares about but the visitor doesn't? Where does it ask for effort (long form, unclear next step, forced choice) before earning it?

**Post-click integrity.** Follow the primary CTA. Does the next page/step deliver what the button promised? A great page with a broken or bait-and-switch next step converts at zero.

## Phase 4 — Synthesize the Report

Structure, in order:

1. **The one thing** — "This page wants the visitor to ___." (Or: "This page has not decided; that is the finding.")
2. **Verdict** — 2–3 sentences: does the page get a cold visitor there, and where does it mainly leak?
3. **What's working** — genuinely, so it doesn't get broken in revision. Be specific.
4. **Prioritized moves** — each tagged `CUT` / `MOVE` / `ADD` / `REWRITE`, ordered by conversion impact, not ease. Each move states: the element, the change, and the visitor-behavior reason ("the skeptical-buyer persona bailed here because…"). Severity-group them: *leaks* (actively losing people) → *drag* (slowing belief) → *polish* (marginal).
5. **Belief-chain map** — the chain with each link marked covered/weak/missing.
6. **What I couldn't verify** — analytics, real traffic sources, actual conversion data. Never fabricate these; recommend measuring where it would settle a judgment call.

Ground every claim in evidence: quote the actual copy, cite the file/line or screenshot, name the persona whose reaction supports it. No "best practices say" without a mechanism — always the *why* in terms of what a visitor believes, feels, or does.

## Scaling

- **Quick pass** (user asks for a gut-check, single page): skip the swarm, run Phases 0–1 and 3–4 yourself, but still write the belief chain and CTA inventory — those are the skill.
- **Full audit** (default for "audit this page/site"): full persona swarm per page.
- **Multi-page/site-wide**: run Phase 0 across all pages first to build the intent map (each page's one action and how pages hand off to each other), then audit the highest-traffic/highest-stakes pages fully. Cross-page finding to always check: do all roads lead to the same conversion door, or does the site scatter its asks?
