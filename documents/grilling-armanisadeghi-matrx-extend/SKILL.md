---
name: grilling
type: Skill
title: "grilling — interview by design tree, defaults ship"
description: "The interview primitive for putting open decisions to an owner. Use on 'grill me', 'stress-test this', or 'what do you need from me before you build this', and whenever a plan, scope, spec, vision, or question ledger needs owner rulings. NOT for steps only a human can perform (use a guided session)."
tags: [interview, decisions, doctrine]
timestamp: 2026-09-12T00:00:00Z
---

<!-- SYNCED COPY — do not edit here.
     Canonical: common-docs/skills/grilling/SKILL.md
     This file is distributed to every consuming repo by
     common-docs/meta/scripts/sync_skills.py. Edit the canonical, run the
     sync, and commit each repo. Edits made here are overwritten and lost. -->

# grilling — interview by design tree

Mechanic adapted from Matt Pocock's `grilling`. Every sentence to the owner follows
[talk to Arman like a person](/policies/talk-to-arman-like-a-person.md); filing and delivery follow
the [ask-arman](/skills/ask-arman/SKILL.md) skill.

## 1. Build the tree, then prune it (before any question)

Draft privately: every open decision, and the decisions that hang off it. Then DELETE every node that is:
- **Settled** — a node's DECISIONS.md or "settled — never re-ask" table, or
  [table stakes](/policies/talk-to-arman-like-a-person.md) (stream, persist, resume, never lose
  input = always yes).
- **A fact** — dispatch a subagent (lane named). Never ask him anything you can look up.
- **Decidable** from code, doctrine, or established best practice — decide it, with its companion
  machinery ([decisions are complete](/policies/talk-to-arman-like-a-person.md)). List it under
  "Decided" so he can override.
- **A number that is really a mechanism** — bring the mechanism.

What survives is only: vision, product semantics, money, brand, legal, deleting real data, an account
only he holds, his eyes on a real screen. The one exception: Arman invoking "grill me" on HIS OWN
plan — then challenge his assumptions too, still never ask facts.

## 2. Rounds

- **Frontier** = surviving nodes whose prerequisites are settled. A question whose answer depends on
  another question open this round waits for a later round.
- **Round size:** per [talk to Arman like a person](/policies/talk-to-arman-like-a-person.md); the
  rest wait on the Question Desk ([ask-arman](/skills/ask-arman/SKILL.md)), ordered by how much of
  the tree each answer unblocks.
- **Never block on exploration.** Send the fact-independent frontier now; only questions downstream of
  a running subagent wait. If he can step away while you explore, say so.
- **Number continuously across rounds** (round 2 starts at Q5), so "5 yes" is never ambiguous.

## 3. Question shape — exactly this

**Q<n> — <title>.** 2–3 plain sentences of background: no doc references, codenames, item IDs, or
emojis. Then the question, in one sentence.
- **Closed:** options only where they differ in approach, never just in magnitude; the best practice in
  one sentence; **Rec:** one recommendation + the companion work that makes it true + why.
- **Open (vision):** ask open, no rec; capture his words verbatim.
- **About a flow, surface, or behavior:** attach the clickable URL + where to look, OR a mermaid
  diagram of what actually happens, OR a throwaway prototype (Artifact or demo route) labeled
  PROTOTYPE. A question he cannot answer from what you gave him is a defect in the question — and often
  a sign the PATH is broken, which is the real finding.
- **Delivery:** plain numbered chat text — **never a structured question picker**.

Every round ends with:
`Decided (override by number): D1 … · D2 …` / `Anything you skip ships with my recommendation.` /
`What else should I know that I didn't ask?`
A question he skipped in an earlier round joins the Decided list as its own numbered item, carrying
the recommendation that shipped and the words **"default, not ruled"** — never written as though he
ruled it.

## 4. After every answer

1. **Record it where it belongs, then commit:** vision → verbatim in VISION/STATE; ruling → the settled
   table, dated; creates work → the pending list or owning handoff; kills work → remove it.
2. **Recompute the frontier:** prune branches the answer killed (say which queued questions died);
   unblock children; a partial answer gets a follow-up next round — never smoothed over.
3. **Skipped** = the recommendation ships, recorded as "default, not ruled". **"Defer"** = a dated
   explicit deferral. **"I need to see it first"** = deferral + the URL he needs. **"I don't know" /
   "we have options"** = the question failed him: research, then bring it back next round with
   better facts, best practice, and a rec — never picked silently, never re-asked as-is
   ([decisions are complete](/policies/talk-to-arman-like-a-person.md)).

## 5. Done

The frontier is empty: every node is answered, decided-with-override-offered, or deferred with a date.
Then act — no separate "confirm shared understanding" gate. State the final decisions in ≤10 lines in
the same message in which you start the work.

## Banned

One question per message · approval after each design section · "see the doc" · menus of numbers ·
asking whether it should stream/persist/resume · asking a fact · a fork with no recommendation · making
him wait for a full audit before round 1 · inventing a question that was not on the pruned tree.

**Never invent a question to have one to ask.** A candidate that was not on the tree goes through the
§1 prune first, like every other node — a decidable best practice spends a slot that belongs to
vision. If the frontier comes up empty, say so and ship (§5); an empty frontier is the success
condition, not a gap to fill.
