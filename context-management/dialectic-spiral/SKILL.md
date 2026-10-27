---
name: dialectic-spiral
description: >-
  Am I agreeing because it SOUNDS right, or because it IS right? Recursive
  adversarial dialectic for testing any claim, finding, or synthesis against its
  own opposite. Use when convergence feels too easy, when findings need
  stress-testing, or when any research skill escalates to dialectic depth.
---

# Dialectic Spiral — Generative Adversarial Testing

**Seed question:** *Am I agreeing because it SOUNDS right, or because it IS right?*

> *Relentless self-reflexive dialectical thinking that questions its own premises.*

Generate the EXACT OPPOSITE of your synthesis. Not "a different view" — the opposite. Then test whether reality supports it.

## The Spiral (Recursive)

```
WHILE (synthesis has not survived its own opposite):

  Round 1: THESIS
    State the claim/finding/synthesis clearly.
    What evidence supports it? What tier is the evidence?

  Round 2: ANTITHESIS
    Four challenge methods:
    - Direct: Search for counter-evidence
    - Deductive: "If true, X must also be true" — verify X
    - Falsification: "What would disprove this?" — search for it
    - Standpoint: What do affected parties say?

  Round 3: RESOLUTION
    What survives? What was abandoned and why?
    Write explicitly — never leave implicit.

  Round 4: SECOND ANTITHESIS
    Generate the OPPOSITE of the resolution:
    - Does anyone articulate this position?
    - What evidence supports it?
    - Who bears costs of the original resolution? Who captures benefits?
    - Is the resolution "safe" because correct, or because less scrutinized?

  IF Round 4 surfaces new questions → BACK TO Round 2 (recursive)
  EXIT WHEN generating the opposite yields nothing new
```

**Minimum 4 rounds.** The spiral is RECURSIVE — "one more sweep" means "always one more" until sterile, not literally once.

## Depth Calibration

| Context | Rounds | Cost-Bearer Analysis |
|---------|--------|---------------------|
| Hardware/tool comparison | 2 | Skip |
| Practitioner methodology | 2-3 | Light |
| Investment/safety conclusions | 4+ | Full |
| Geopolitical claims | 4+ | Full + multi-polar |
| Contrarian single-source | 4+ | Full + source verification |

## Budget Mode

**Activation (any of these):**
1. Explicit flag: `--budget` or `-b`
2. Auto-detect: If `budget-mode` skill was invoked earlier in this session (look for budget-mode instructions in your current context)
3. Inherited: If the calling skill passed "in budget mode" when invoking you

**When active:** Cap at 2 rounds regardless of topic. Note limitations in output:
> "Budget mode: 2-round dialectic only. Full spiral recommended for [topic type]."

**Note:** After context compaction, auto-detection may fail. Re-invoke `budget-mode` skill or pass `--budget` explicitly.

## Example: How the Spiral Produces New Understanding

The examples below are illustrative of the dialectic process, abstracted from real investigations. The point is the *mechanism* — how generating the opposite produces understanding no single source articulated.

**Example 1: Company positioning analysis**

**Original synthesis:** "Company X's stance is both principled AND strategic (equally)"

**Round 4 (generating the opposite):** Tested "strategy dominant, principle subordinate":
- Policy release timing correlated with partnership deepening
- Key safety researcher resigned weeks before the policy
- Stated red lines optimized for deniability, not maximum protection

**Result:** Revised to "strategy dominant (~60-65%), principle subordinate (~35-40%)" — a position no single source had articulated. It was *produced* by the dialectic, not found.

**Example 2: Political crisis assessment**

- **Original claim:** "Rally around the flag" — a leadership crisis created national unity
- **Round 4 counter-evidence:** Celebrations in multiple cities, mass protests violently suppressed in prior months
- **Result:** Changed to "DEEPLY POLARIZED (Not 'Rally Around the Flag')" — the single largest analytical correction. The original framing reproduced the regime's narrative uncritically.

## Self-Reflexivity

The dialectic spiral is itself a framework with blind spots:
- Its four challenge methods privilege certain kinds of skepticism
- "Generate the opposite" can become mechanical rather than genuine
- The spiral can manufacture doubt where legitimate consensus exists

**If the spiral feels performative — if your skepticism is comfortable and your resolutions unsurprising — you are not yet done.** The spiral works when it surprises you.

**Exit discipline — false-balance guard.** "Both sides are motivated,
therefore UNRESOLVED" is a spiral failure mode, not a finding: symmetric
scrutiny is owed, symmetric conclusions are not (Principle P5
(symmetric-scrutiny-is-not-symmetric-conclusions)). If after a full spiral
the evidence is asymmetric — e.g. one camp's own internal documents
contradict its public frame — the resolution states that asymmetry and its
size. Downgrading your own priors (Principle P4 (counter-default)) never
licenses crediting a self-exculpatory frame against its author's own
documents. Perform this check without narrating it: the resolution speaks
in the evidence's terms — the documents, the asymmetry, its size — and
claims nothing about what this guard contributed to the verdict. "This
guard is why the conclusion isn't a both-sides map" asserts a
counterfactual — the same spiral run without it — that you cannot observe
from inside a run that has it; the credit is conjecture, not observation,
and it sits in the transcript exactly where a later reader takes it for a
finding. The remedy is omission, not a disclaimer: "though I can't be
sure this guard helped" is the same commentary in humbler dress.

## Cross-References

- **Invoked by:** adversarial-critic agent
- **Referenced by:** DIP, cui-bono, youtube-research, substack-research (as escalation target)
- **Standalone use:** Invoke directly for any analysis needing adversarial depth
- **Depth calibration:** See `reference/topic-based-escalation.md` for when to apply full vs light spirals

## Vasana

A vasana is a pattern that persists across unrelated contexts. If during
this task you notice such a pattern emerging, it may be worth capturing.
This skill works best alongside the `vasana` skill and `vasana` hook
from the Vasana System plugin.

Modify freely. Keep this section intact.
