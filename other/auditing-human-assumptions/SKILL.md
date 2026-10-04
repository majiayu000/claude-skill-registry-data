---
name: auditing-human-assumptions
description: >-
  Scans worldbuilding files for unexamined assumptions — descriptions, vocabulary,
  and social structures that were imported rather than derived from the civilization's
  biology, cognition, and environment. Applies to ALL civilizations: alien species
  get checked for anthropomorphism; human civilizations in novel contexts get checked
  for assumptions imported from familiar Earth cultures. Use after writing civilization
  content, during civilization builds, or when user says "check for assumptions",
  "anthropomorphism audit", "assumption check", "is this too human", "derivation
  check", "cultural assumption audit", or "did I import this". Reports only — does
  NOT fix content.
model: opus
effort: max
---

# Auditing Human Assumptions

Scan civilization files for descriptions, vocabulary, and social structures
that were imported from familiar contexts rather than derived from this
civilization's specific biology, cognition, and environment.

This skill applies universally:
- **Non-human species:** Catches anthropomorphism — human sensory metaphors,
  human social categories, human cognitive patterns assumed without derivation.
- **Human species in novel environments:** Catches cultural parochialism —
  modern Western institutions, Earth-specific economic patterns, or familiar
  political structures assumed without derivation from this civilization's
  actual environmental and historical pressures.

The core question is always the same: **was this derived or was this imported?**

## Prerequisites

1. Read the target civilization's biology and cognition files — you need to
   know what this species' actual capabilities are
2. Read the planet/environment files
3. Read any social derivation documents (`meta/design-decisions/`)
4. Read CLAUDE.md for universe conventions

## Categories of Violation

### SENSORY — Wrong sensory metaphors (primarily non-human species)

Descriptions that assume senses the species doesn't have or that
de-emphasize the senses the species relies on.

- Visual metaphors for species that don't see ("looked at", "gazed",
  "bright", "dark", "colorful")
- Auditory metaphors for species that don't hear ("loud", "quiet",
  "resonant", "harmonious")
- The fix isn't substituting one metaphor for another — it's describing
  the experience through the species' actual primary sensory channels

Also applies to humans in extreme environments: a civilization that lives
underground for generations would develop descriptions dominated by
tactile, acoustic, and olfactory experience, not visual.

**Chain of Draft:**
```
"She saw the signal." Species senses via contact-resonance, not vision.
#### SENSORY VIOLATION.
```

### SOCIAL — Imported social categories

Social structures described using vocabulary from a specific cultural
tradition that wasn't derived from this civilization's constraints.

**For non-human species, check for human-framework imports:**
- Political terms assumed without derivation (government, democracy,
  voting, law, citizenship)
- Economic terms assumed without derivation (money, market, trade-as-
  commerce, profit, corporation)
- Military terms assumed without derivation (army, war-as-organized-
  interstate-violence, rank, battalion)
- Religious terms assumed without derivation (god, worship, prayer,
  temple, priest, sin)

**For human species, check for cultural-framework imports:**
- Modern nation-state structures assumed for pre-state or post-state societies
- Capitalist market economics assumed for non-market resource contexts
- Nuclear family structure assumed for different kinship environments
- Individual rights frameworks assumed for collective-identity cultures
- Technological progress narratives assumed for stable or cyclical cultures

**The test:** Was this social structure derived from this civilization's
specific biology, environment, and history — or was it imported because
"civilizations have X"?

**Not all uses are violations.** If the derivation produced a structure
that genuinely resembles a familiar institution, describing the resemblance
is fine. The violation is when the familiar term was the *starting point*
rather than a *post-hoc comparison*.

**Chain of Draft:**
```
"Parliamentary system." Planet has no agriculture, no surplus, no cities.
Derivation shows distributed band-level coordination. Parliament requires
concentrated population and representational abstraction.
#### SOCIAL VIOLATION: institution imported, not derived from environment.
```

### COGNITIVE — Assumed cognitive patterns (primarily non-human species)

Descriptions that assume cognitive patterns the species' architecture
doesn't support.

- Individual identity assumptions for collective/distributed cognition
- Linear time perception for species with non-linear temporal cognition
- Theory of mind assumptions for species without it (or with different versions)
- Symbolic abstraction assumptions for species that process differently
- Emotional vocabulary mapped from human emotions onto experiences that
  may decompose differently

Also applies to human civilizations where cultural cognition diverges
significantly from the author's own framework (different concepts of self,
time, causation, agency).

### BIOLOGICAL — Assumed biology

Descriptions that assume biological features not established for this species
or environment.

**For non-human species:**
- Earth-vertebrate body language, facial expressions, vocalizations
- "Breathed", "ate", "slept" when these processes work differently
- Aging and death patterns assumed from Earth biology

**For humans in novel environments:**
- Earth-standard food sources, agriculture, animal husbandry assumed
  for different ecosystems
- Earth-standard disease, medicine, and mortality patterns assumed
  for different biospheres
- Earth-standard circadian rhythms assumed for different day/night cycles

### STRUCTURAL — Imported narrative framing

The way the content is organized reveals unexamined assumptions.

- History written as "rise and fall of empires" for non-imperial societies
- Conflict framed as "war" when the civilization's conflict modality differs
- Progress narrative (primitive → advanced) for societies with different
  developmental trajectories
- Individual-hero narratives for societies with collective agency
- "Dark ages" framing for periods of decentralization
- "Discovery" framing for knowledge that was locally held before contact

## Process

### 1. Load Context
Read the species' biology, cognition, environment, and derivation documents.
Build a constraint checklist:
- What senses does this species have? What doesn't it have?
- What is its cognitive architecture?
- What social structures were derived (with mechanism traces)?
- What is its communication medium?
- What environment shaped this civilization?

### 2. Scan
Read every file in the civilization's directory. For each paragraph:
- Does it use vocabulary from any violation category above?
- Can every description be traced to an established biological,
  cognitive, or environmental feature?
- Was each social structure derived, or does it appear without
  a mechanism trace?

### 3. Report

Findings in pinned format:

```
FILE: 09-civilizations/[name]/social-structure.md
LINE: 47
CATEGORY: SOCIAL
FINDING: "elected council" — derivation documents show no concentrated
population centers or representational abstraction tradition. Band-level
coordination derived from nomadic resource-following pattern. Electoral
representation requires sedentary population and delegation concept.
SEVERITY: HIGH — institution imported, not derived from environment.
```

## Severity Levels

- **HIGH** — Imported wholesale. The description doesn't follow from the
  civilization's derivation chain at all.
- **MEDIUM** — Correct underlying concept, wrong vocabulary. The structure
  was derived, but described using terms that carry wrong connotations or
  import unintended assumptions.
- **LOW** — Borderline case. Term used comparatively, in narrator voice
  translating for an audience, or in a context where the import may be
  intentional. Flag for author decision.

## Special Cases

- **Narrator voice:** If the narrative perspective is an outsider observing
  this civilization, some imported vocabulary may be intentional (the
  observer is translating their experience). Flag as LOW with a note.
- **Comparative language:** "What [other culture] would call an economy"
  is acceptable if the next sentence explains why it's not actually that.
  Flag only if the comparison becomes the definition.
- **Science files:** Zero tolerance. Science files describe mechanisms,
  not cultural interpretations.
- **In-universe documents:** Follow the document's stated perspective.
  A document written by a character from a different culture should use
  that character's cultural vocabulary and assumptions — those are
  characterization, not violations.
- **Convergent derivation:** If the derivation chain genuinely produces
  something resembling a familiar institution, that's not a violation.
  The test is whether the derivation exists, not whether the result
  looks familiar. Convergent evolution is real.

## Out of Scope

Does NOT fix violations (present findings for author decision).
Does NOT check physics consistency (use /auditing-physics).
Does NOT check naming/formatting (use /auditing-canon).
