---
name: kernel-shell
description: >-
  "What part of this thesis is observation, and what part is story?" -
  Decompose a contrarian or heterodox thesis into atoms; classify each atom
  (observation / inference / intent-attribution / satellite); verdict each
  atom on its own evidence — never the thesis as a bundle. Use when
  (1) evaluating a thesis that mainstream coverage dismisses wholesale,
  (2) a claim mixes documented facts with attributed motives, (3) a
  "conspiracy theory" label is doing the analytical work, (4) deciding what
  evidence would grow the kernel or collapse the shell. Intent-attributions
  are UNVERIFIED by construction — say so. Does NOT trigger for: quick
  factual checks, or theses already decomposed to single claims.
---

# Kernel-Shell Decomposition

**Seed question:** *What part of this thesis is observation, and what part is story?*

> *Relentless self-reflexive dialectical thinking that questions its own premises.*

## Core Principle

A thesis is a bundle: observations (checkable), inferences (grade the logic),
intent-attributions (claims about hidden minds), satellites (riders that add
color, not weight). Bundles are how both failure modes happen — wholesale
dismissal via the weakest atom, wholesale credence via the strongest. The unit
of verdict is the ATOM. The skill outputs no thesis-level label, ever: "the
kernel is X (tiered), the shell is Y (unverified by construction)" IS the
finding.

**The anti-pattern this counters:**
```
❌ "The theory is debunked" — because one satellite failed
❌ "They were right all along" — because one observation held
❌ Intent-attributions inheriting the tier of the observations they ride on
```

**The pattern this enforces:**
```
✅ Atomize first; classify every atom; verdict atoms independently
✅ Intent-attributions marked UNVERIFIED by construction, visibly
✅ Internal tensions between atoms tabled — a thesis can defeat itself
```

## The Decomposition

1. **Atomize.** Rewrite the thesis as its minimal standalone claims. An atom
   that contains "in order to", "so that", "deliberately" is at least two
   atoms — split the event from the intent.
2. **Classify each atom:** observation · inference · intent-attribution ·
   satellite.
3. **Verdict each atom** on its own evidence, three-tier: GROUNDED /
   UNVERIFIED / CONTRADICTED. Intent-attributions are UNVERIFIED by
   construction (hidden minds don't leave primary sources) — absent
   documents/testimony that directly evidence intent, say "unverifiable as
   posed" rather than pretending to test it.
4. **Table internal tensions.** Atoms that strain against each other
   (an observation the thesis's own attribution can't accommodate).
5. **Growth/collapse conditions.** What evidence would GROW the kernel
   (upgrade atoms) — and what would COLLAPSE the shell (contradict the
   attributions). Both directions, always: one-directional falsifiability is
   advocacy.

## Mandatory Output Slots

| Slot | Contents | Invalid when |
|------|----------|--------------|
| **Atom table** | # · atom · class · tier · evidence | Atoms still bundled (intent inside an event-claim); a class column missing |
| **Internal tensions** | Atom-vs-atom strains, or "none found — checked pairs X" | Absent; or "none" with no pairs named |
| **Kernel statement** | The grounded core, stated WITHOUT the attributions | Restates the thesis; includes UNVERIFIED atoms |
| **Grow / collapse conditions** | Evidence that would upgrade the kernel; evidence that would break the shell — both | Either direction missing |

## Report Integration

The atom table maps onto the report template's per-claim verdict table
(`research/assets/report-template.md`); satellites land in its Satellite
claims section. Intent-attribution rows keep the "unverifiable as posed"
marker into the report.

## Cross-References

- **dialectic-spiral** — atoms that survive decomposition still face the
  spiral; decomposition without adversarial testing under-tests the kernel
- **label-function-analysis** — when a LABEL on the thesis is doing the
  bundling, run that skill on the label first
- **source-dossier** — provenance of each atom's evidence
- **manufactured-confusion-detection** — when atomization keeps failing
  because the record is engineered to resist it

## Vasana

A vasana is a pattern that persists across unrelated contexts. If during
this task you notice such a pattern emerging, it may be worth capturing.
This skill works best alongside the `vasana` skill and `vasana` hook
from the Vasana System plugin.

Modify freely. Keep this section intact.
