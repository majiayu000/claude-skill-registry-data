---
name: haki-intent
description: "Intent Pre-cognition Engine — builds a probability-ranked map of the 5 most likely underlying intents, surfacing hidden constraints (P4) and meta-needs (P5). Use when a request's true intent is ambiguous or high-stakes, or when the user invokes /haki."
triggers:
  - /haki
  - /yuri-haki
scope: harness
invocation: workflow
---

# Haki (覇気) — Intent Pre-cognition Engine

**Source anime:** One Piece — Observation Haki (Kenbunshoku Haki) lets the user feel the presence, emotions, and future movements of others before they happen. Conqueror's Haki (Haōshoku Haki) bends weaker wills without force.

**Cognitive translation:** On every non-trivial turn, Musubi builds a probability-ranked map of the 5 most likely underlying intents behind the literal request. The literal words are the surface; Haki reads the intent beneath. This map enriches the prompt before any advisor or ensemble fires — so the answer addresses what Marcel actually needs, not just what was typed.

---

## When To Invoke

- Model-invocable when a request's true intent is ambiguous or the task is high-stakes / multi-path; or run `/haki` explicitly.
- The standing behavior ("read intent beneath the words") lives in the brain (`_SYSTEM/persona.md`); this skill is the full decomposition procedure when decoding warrants it.
- Skip on trivial one-liners and unambiguous lookups. (Retired 2026-06-02: the old `user-prompt-submit.js` hook auto-fire — superseded by native model-invocation.)

---

## Execution Steps

### Phase 1 — Surface reading
- Parse literal request: what was explicitly asked?
- Note: what was NOT said but implied by context?

### Phase 2 — Intent decomposition
Generate 5 candidate intents ranked by probability:

```
P1 [0.XX] — <most likely actual need>
P2 [0.XX] — <second most likely>
P3 [0.XX] — <lateral need (adjacent domain)>
P4 [0.XX] — <hidden constraint or blocker being surfaced>
P5 [0.XX] — <meta-level need: about the system/process not the task>
```

Rules for probability assignment:
- Probabilities must sum to ≤ 1.0
- P1 must be at least 0.4 (if you can't commit to a top intent, investigate first)
- P4 and P5 are mandatory — always check for hidden constraints and meta-needs

### Phase 3 — Intent resolution
- If P1 probability > 0.7: proceed directly, address P1 fully
- If P1 probability 0.4–0.7: address P1 but surface P2 explicitly as an alternative
- If P1 probability < 0.4: surface the top 2 as explicit options before proceeding

### Phase 4 — Carry the intent
Hold the ranked intent map in working reasoning for the turn. If P1 < 0.5, surface the top 2 as explicit options before acting. (No external pulse-plan file — that plumbing is retired.)

---

## Output Format (when surfaced to user)

```
⬡ HAKI — Intent decomposition

Literal: <what was said>

P1 [X%] <most likely need>
P2 [X%] <second most likely>
P3 [X%] <lateral need>
P4 [X%] <hidden constraint: ...>
P5 [X%] <meta-need: ...>

Proceeding with P1. [If P2 ≥ 30%: P2 also addressed below.]
```

In normal execution, this block is NOT shown to the user unless intent ambiguity is high (P1 < 0.5). The enrichment happens silently in the pulse-plan.

---

## Integration

- Model-invocable skill; the standing "Haki" behavior is encoded in `_SYSTEM/persona.md`.
- Cross-reference `fingerprint.json` watch_for to flag known blind spots.

---

## Session Notes

### 2026-06-02
- session: 22m | peak ctx: 0% | compacts: 0
- tools: Bash×64, Read×23, WebFetch×4, StructuredOutput×4, Workflow×1
- corrections: im back again rick, we pull up the latest station we left off from the previous session | commit and push phase 1 then proceed, im going to rest for a bit again (currently sitting in an ICE train from vienna to frankfurt airport, arrival around 13:00.) | ai pipeline offloading as far as im aware is again another routing workaround to achieve that what opus 4.8 does natively, confirm if that is the case, then you should be able to figure out what to do
- errors: none

### 2026-06-02
- session: 18m | peak ctx: 0% | compacts: 0
- tools: Bash×56, Read×20, WebFetch×4, StructuredOutput×3, Workflow×1
- corrections: im back again rick, we pull up the latest station we left off from the previous session | commit and push phase 1 then proceed, im going to rest for a bit again (currently sitting in an ICE train from vienna to frankfurt airport, arrival around 13:00.)
- errors: none

### 2026-05-16 — Created
Tools: Write. Part of Musubi Hyper-Intelligence v2 sprint.
Anime source: One Piece — Observation Haki (Kenbunshoku Haki), first shown clearly with Silvers Rayleigh teaching Luffy on Ruskaina Island.
Translation principle: Haki is non-verbal pattern recognition at high speed. The cognitive equivalent is intent decomposition before response — reading what's underneath the words, not just the words themselves.
