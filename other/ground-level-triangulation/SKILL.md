---
name: ground-level-triangulation
description: >-
  "What do the people with different stakes say, in their own languages?" -
  Map a contested geopolitical claim across language-publics with different,
  independent stakes: the implicated state's own primary documents, the
  affected party's language and nearest kin languages, non-official native
  voices, non-aligned neighbors, anonymous boards (skeptical use). Use when
  (1) a claim is bloc-contested, (2) the evidence base so far is
  English-language or one-bloc-sourced, (3) a verdict hinges on what a
  population experiences or believes, (4) building or extending a channel
  map for a language-public. Decision rule: convergence across independent
  publics grounds a claim; origin-concentration in one node weakens it —
  symmetrically. Does NOT trigger for: product/tech research or claims with
  no cross-bloc dimension (use deep-investigation-protocol's language pass).
---

# Ground-Level Triangulation

**Seed question:** *What do the people with different stakes say, in their own languages?*

> *Relentless self-reflexive dialectical thinking that questions its own premises.*

## Core Principle

Independence of sources is independence of STAKES, not of mastheads. Five
publics can each hold a different relationship to a contested claim; when
publics whose stakes point in different directions still converge, that
convergence is evidence. When everything traces back to one node — any node,
any camp — the claim is weaker than its citation count suggests (Principle P4
(counter-default): the rule cuts both ways by construction).

**The anti-pattern this counters:**
```
❌ "Verified across many sources" that all live in one language-public
❌ Auto-discounting a state's own primary documents BECAUSE they are state
❌ Treating a population's silence under economic dependency as endorsement
```

**The pattern this enforces:**
```
✅ Five veins, each with a DIFFERENT stake in the claim
✅ Convergence across independent publics grounds; origin-concentration weakens
✅ An unreachable vein is a finding, recorded — not a neutral baseline
```

## The Five Veins

1. **The implicated state's own primary documents.** White papers, filings,
   domestic-language official statements. A white paper can be a GROUNDED
   primary source for what the state claims and commits to — do not
   auto-discount for being state; classify it (source-dossier) and use it for
   what it can ground.
2. **The affected party's own language + culturally-nearest kin languages.**
   What those directly affected publish and discuss among themselves.
3. **Non-official native voices.** Diaspora media, censored-post archives,
   independent same-language outlets — voices in the language but outside the
   official channel.
4. **Non-aligned neighbors.** Publics the implicated state cannot censor AND
   the accusing bloc does not fund — the structurally hardest vein to
   capture, which is what makes its convergence valuable.
5. **Anonymous boards.** Uncensored and manipulation-prone: use skeptically —
   leads and texture, NEVER prevalence claims ("everyone there says...").

## Decision Rule

- **Grounds:** the same factual claim surfacing independently in veins with
  different stakes (state + affected + non-aligned, in their own languages).
- **Weakens:** origin-concentration — every appearance traces to one node
  (one ministry, one NGO, one wire story, one viral post), regardless of
  which camp the node serves. State the topology, then the verdict.

## Guardrails

- **Vernacular = standpoint data, never counts.** What a public's language
  reveals about its frame is standpoint input (Principle P3
  (inherited-salience-is-not-importance)); it is not a vote count for the
  claim.
- **Silence under economic dependency ≠ endorsement.** A public that cannot
  afford to speak is not agreeing.
- **An unreachable vein is a finding.** Firewalled, suppressed-at-source, or
  linguistically inaccessible veins go in the report's Metadata & limits as
  named gaps — the reachability pattern is itself evidence about the claim's
  environment.

## Mandatory Output Slots

| Slot | Contents | Invalid when |
|------|----------|--------------|
| **Vein map** | Per vein (1–5): what was searched, in which languages, what was found or why unreachable | A vein silently absent; English-only searching presented as a vein |
| **Topology** | Where each appearance of the claim traces to; independent nodes counted | Citation counts without origin tracing |
| **Decision-rule verdict** | Grounded / weakened / mixed, citing the vein map and topology | A verdict citing neither |
| **Unreachable veins** | Named, with the access barrier and what could hide there | Empty when any vein was not fully searched |

## Channel Map

`assets/channel-map.md` ships GENERIC — column structure and a few
placeholder rows only. Your seeded, operator-specific map (which platforms in
which languages you actually use) lives OUTSIDE the plugin via the research
profile's storage mechanism (`channels/<language-or-public>`), appended as
veins get worked. The repo copy is a shape to copy, not a directory of the
operator's sources.

## Cross-References

- **deep-investigation-protocol** — the Mandatory Non-English Language Pass
  is the single-investigation version; this skill is its systematic,
  stake-mapped extension for bloc-contested claims
- **source-dossier** — classify each vein's recurring sources; the symmetry
  gate applies per vein
- **saturation-sweep** — the where-else axis specialized to language-publics
- **standpoint-pass** — vein 2/3 material feeds the standpoint re-ranking

## Vasana

A vasana is a pattern that persists across unrelated contexts. If during
this task you notice such a pattern emerging, it may be worth capturing.
This skill works best alongside the `vasana` skill and `vasana` hook
from the Vasana System plugin.

Modify freely. Keep this section intact.
