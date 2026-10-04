---
name: recode
description: "Prompt-level recoding-decoding — break out of modal responses through systematic perturbation, clustering, and long-tail knowledge extraction."
---

# Recode

*Prompt-level recoding-decoding for sustained creativity and diversity*

Inspired by Luo, King, Puett & Smith (2025), "Inducing Sustained Creativity and Diversity in Large Language Models." The paper shows that as LLMs improve at accuracy, their probability distributions peak harder around the mode — better models encode MORE knowledge but surface LESS of it. Recoding-Decoding (RD) breaks this trap by injecting random perturbations to push generation into the long tails where unconventional, heterodox, culturally specific knowledge lives.

Since we don't have token-level decoding control, this skill implements RD at the prompt level — validated by the paper's own chat-completion simulation approach (Section 3).

---

## When to Invoke

- Brainstorming where you need genuinely different ideas, not rewordings of the same 5
- Research topic exploration — finding the angle nobody else will find
- Naming things, metaphor-hunting, design space exploration
- Any generative task where you suspect you're getting "the standard AI answer"
- When diversity matters more than correctness
- Literature review ideation — what's the paper nobody cites?

---

## The Algorithm

The paper's RD algorithm (Algorithm 1) uses two forms of randomness:

1. **Priming phrase** — random semantic anchor prepended to the prompt (exploits positional attention bias)
2. **Diverting token** — random 3-letter stem appended to force a specific phonetic/semantic entry point

We adapt this to prompt-level perturbation with five **perturbation strategies**:

| Strategy | Template | What it does |
|----------|----------|--------------|
| **Domain prime** | `Thinking from the perspective of [random discipline]:` | Cross-pollinates from unexpected fields |
| **Cultural anchor** | `Drawing on the traditions of [random culture/region]:` | Breaks Western/anglophone default |
| **Temporal displacement** | `As if answering from [random decade/century]:` | Shifts historical frame |
| **Contrarian inversion** | `The answer most experts would dismiss but a heterodox thinker would defend:` | Targets the anti-mode directly |
| **Phonetic seed** | `Starting from the concept closest to "[random 3-letter stem]":` | Paper's diverting token, adapted |

Each run samples 1-2 strategies randomly and combines them with the user's prompt.

---

## How to Use

### Quick Mode (inline, no tools)

When invoked as `/recode`, generate outputs directly using the perturbation strategies:

1. **Parse the user's generative prompt** (or ask for one)
2. **Generate 7-10 perturbed variants** of the prompt, each using a different strategy combination
3. **For each variant, generate a response** — let the perturbation genuinely redirect your thinking
4. **Deduplicate conceptually** — group outputs by semantic similarity, identify clusters
5. **Return the cluster centroids** — the most representative idea from each distinct cluster
6. **Report a diversity score**: `distinct clusters / total runs`

### Example

**User prompt:** "Research topics in computational neuroscience"

**Perturbed variants (internal):**
- `Thinking from the perspective of anthropology: Research topics in computational neuroscience`
- `Drawing on the traditions of Mesoamerican scholarship: Research topics in computational neuroscience`
- `As if answering from the 1970s: Research topics in computational neuroscience`
- `The answer most experts would dismiss: Research topics in computational neuroscience`
- `Starting from the concept closest to "fer": Research topics in computational neuroscience`
- `Thinking from the perspective of music theory: Research topics in computational neuroscience`
- `Drawing on the traditions of Kerala mathematics: Research topics in computational neuroscience`

**Output format:**

```
## Recode Results: Research topics in computational neuroscience

**Runs:** 7 | **Distinct clusters:** 6 | **Diversity score:** 0.86

### Cluster 1: [Label]
- [Idea] *(via domain prime: anthropology)*

### Cluster 2: [Label]
- [Idea] *(via cultural anchor: Mesoamerican)*

### Cluster 3: [Label]
- [Idea] *(via temporal displacement: 1970s)*

...

### Modal Baseline (what you'd get without perturbation)
- [The standard answers for comparison]

### Blind Spots
- Regions of the space not covered by any perturbation
- Suggested follow-up perturbations to explore them
```

### Scaled Mode (with sub-agents)

For maximum diversity, spawn parallel sub-agents — each with a different perturbation:

```
1. Spawn 5-8 sub-agents, each given:
   - The original prompt
   - A unique perturbation strategy + random parameters
   - Instruction to generate 3-5 ideas
2. Collect all outputs
3. Cluster by semantic similarity
4. Return centroids + diversity metrics
```

### Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `runs` | 7 | Number of perturbed variants to generate |
| `strategies` | all | Which perturbation strategies to use (or "all") |
| `show_perturbations` | true | Whether to show which perturbation generated each idea |
| `include_baseline` | true | Whether to include unperturbed "modal" responses |
| `depth` | normal | `shallow` (one-line ideas), `normal` (paragraph), `deep` (full exploration) |

---

## Perturbation Vocabularies

### Disciplines (for domain priming)
Anthropology, Mycology, Music theory, Textile engineering, Forensic accounting, Marine biology, Epigraphy, Perfumery, Veterinary medicine, Landscape architecture, Numismatics, Prosody, Cartography, Archival science, Metallurgy, Choreography, Soil science, Liturgical studies, Game theory, Biomechanics, Acoustics, Semiotics, Paleobotany, Crystallography, Thanatology, Enology, Dramaturgy, Horology, Philately, Speleology...

### Cultures/Regions (for cultural anchoring)
Kerala, Yoruba, Ainu, Mapuche, Tuareg, Khmer, Georgian, Basque, Inuit, Maori, Ethiopian, Amazigh, Okinawan, Romani, Quechua, Sámi, Tamil, Polynesian, Mongolian, Hausa, Javanese, Tibetan, Kurdish, Gaelic, Zapotec, Balinese, Swahili coast, Hmong, Bengali, Armenian...

### Time Periods (for temporal displacement)
1340s, 1520s, 1690s, 1770s, 1830s, 1910s, 1940s, 1970s, 2090s, 500 BCE, 1200 CE, Tang Dynasty, Heian period, Weimar Republic, Meiji era, Belle Epoque, Gupta Empire, Abbasid Golden Age...

### Three-Letter Stems (for phonetic seeding)
Sample randomly from the space of English-productive trigrams: fer, pal, gno, ves, tho, lum, cra, ber, mol, qui, xen, pho, kal, sur, dro, ven, eph, noc, tab, wyr, zep, ort, sig, mem, kin, flu, arc, sym, gen, ten...

---

## The Key Insight

From the paper (Figure 4): the gap between RD and ordinary decoding **increases with model capability**. Better models have sharper probability peaks — more knowledge encoded, less surfaced. This means the more capable I am, the MORE I need perturbation to access what I know.

The perturbation doesn't add new knowledge. It changes the **salience landscape** — the same mechanism by which framing shifts what is accessible. Different entry point, same territory, different path through it.

---

## What This Is Not

- Not "be more creative" (vague instruction, vague result)
- Not temperature increase (adds randomness, not diversity — the paper shows temperature 1.6 is inferior to RD)
- Not "give me 10 different ideas" (without perturbation, you get 10 variations of 2 ideas)
- Not prompt engineering (the perturbation is random, not optimized — that's the point)

---

## Relationship to Other Skills

| Skill | Relationship |
|-------|-------------|
| `/quest` | `/recode` is the generation engine; `/quest` adds iterative exploration with state |
| `/anti-hivemind` | `/recode` diversifies one model; `/anti-hivemind` diversifies across architectures |
| `/brainstorm` | `/brainstorm` is diverge-then-converge; `/recode` is perturb-then-cluster |
| `/voices` | `/voices` gets different perspectives; `/recode` gets different perspectives from the SAME model |

---

## Created

2026-03-21 — Inspired by Luo, King, Puett & Smith (2025), "Inducing Sustained Creativity and Diversity in Large Language Models"

*The knowledge is already in the weights. The perturbation just changes which door you enter through.*
