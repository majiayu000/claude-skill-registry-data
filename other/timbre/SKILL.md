---
name: timbre
description: >-
  Write copy in a specific human voice using a three-role, layered pipeline —
  a Cartographer that maps the voice from real samples, a Drafter that writes
  conditioned on verbatim exemplars, and a blind Adversarial Reader that never
  sees the voice map and grades against a planted control. Use when the user
  wants copy that "sounds like me", "sounds human", "matches our brand voice",
  "doesn't read like AI", "rewrite this in my voice", "humanize this draft",
  "make this less ChatGPT-ish", or hands over writing samples and asks for new
  copy in that register. Also fires on /timbre. Produces a voice map, a draft,
  a blind review with a falsification control, and a receipt stating what the
  pass did and did not achieve. Do NOT use this to pass work off as a human's in an academic-integrity or legal-attestation context, or to impersonate a named person without their consent — see Non-negotiables. Do NOT fire for plain explanation of technical material (that is /feynman), for shortening text that is already clear (a summary), or when no voice samples exist and none can be obtained — say so instead of inventing a voice from adjectives.
argument-hint: "[target artifact] [voice-sample paths or 'paste']"
---

# timbre

Copy in a named voice, produced by three roles that are not allowed to grade each other's work.

Nothing here needs to be installed. No `tick`, no Node, no Python, no shell script — the whole pipeline runs on one markdown thread file you name and three role-switches inside a session (or three sub-agents, if the host supports them). It borrows XYZ's *handoff discipline*, not its runtime.

## TL;DR of what this skill does

Maps a real human voice from real samples into verbatim exemplars plus a measurable fingerprint,
drafts against those exemplars, then hands the draft to a reader who has **never seen the voice map**
and must pick the target out of a lineup that contains a planted control. Reconciles the findings,
revises once, and ships a receipt that states plainly what the pass achieved and what it did not.

## The one rule everything else serves

> **Exemplars, not adjectives.**

A voice is reproduced by showing the model the author's actual sentences, not by describing them.
"Warm but direct, punchy, conversational" is a mood board; it is not a voice, and the research is
blunt about it — zero-shot statistical style summaries *"were not effective anchors for imitation"*
([arXiv:2509.24930](https://arxiv.org/abs/2509.24930)). If you cannot get real samples, this skill
does not apply. Say so.

## Non-negotiables

- **No detector evasion.** This skill exists to make copy read well in a voice its owner is entitled
  to use. It is not an "AI humanizer" for defeating detection. If the request is to pass machine text
  through an academic-integrity check, a plagiarism gate, a legal attestation, or any process that
  asks *"did a human write this?"* — **refuse and say why.** The relevant finding is not that evasion
  is hard; it is that fidelity and detectability are *separable axes*
  ([arXiv:2509.24930](https://arxiv.org/abs/2509.24930)), so success at voice tells you nothing about
  what a detector sees, and promising otherwise is a lie with someone else's name on it.
- **Consent for named voices.** Writing in the user's own voice, their company's brand voice, or a
  voice they are commissioned to write in: fine. Impersonating a specific third party who has not
  agreed: no.
- **Never claim the authorship gap is closed.** Prompt-time personalization moves style *within* the
  model's own regime and does not reach human authorship
  ([arXiv:2608.19746](https://arxiv.org/abs/2608.19746)). Every receipt says so. Copy can be good,
  on-voice, and worth shipping without that claim.
- **The Drafter never grades its own draft.** Separated grading is the point of the three roles, not
  ceremony — see [Why three roles](#why-three-roles-and-not-one-good-prompt).
- **No fabricated facts in service of voice.** If matching the register tempts you to invent a
  statistic, an anecdote, or a customer quote, stop and flag the gap. Voice is a delivery property;
  truth is a content property.

## Inputs

| Input | Required | Notes |
|---|---|---|
| The brief | Yes | What the copy must do, for whom, at what length |
| Voice samples | **Yes** | 3–8 pieces of *real* writing by the target author. Prefer whole pieces over excerpts |
| Anti-samples | Optional, valuable | Writing the author would never publish — the negative space is diagnostic |
| Thread file path | Yes | One markdown file. You name it; everything below writes there |
| Prior-run receipt | Optional | If revising, read the last receipt before Layer 1 |

**If fewer than 3 samples exist**, run anyway but downgrade the output: mark the voice map
`LOW-CONFIDENCE` and say in the receipt that the fingerprint is under-determined. Do not silently
compensate by inventing traits.

## Layer 0 — Should this fire at all?

| The ask | Route to |
|---|---|
| Explain dense material plainly | [feynman](../feynman/SKILL.md) |
| Shorten text that is already clear | a summary — no skill needed |
| Assess whether a claim is defensible | [honest](https://github.com/HiQS-Labs/XYZ-forge/blob/development/skills/3-weekly/honest/SKILL.md) |
| Get a second model's read on a finished draft | [consult](https://github.com/HiQS-Labs/XYZ-forge/blob/development/skills/1-hourly/consult/SKILL.md) |
| Copy in a specific human voice, samples available | **stay here** |

## Why three roles, and not one good prompt

Because a single agent grading its own voice-matching is the exact failure PersonalBench measured.
In that study the LLM judge rated a machine-generated style profile **higher than the real author's
own text** (0.542 vs 0.427), while the trained authorship model showed no such advantage — a
circularity between the trait extraction doing the writing and the trait extraction doing the
judging ([arXiv:2608.19746](https://arxiv.org/abs/2608.19746)). An agent that both drafts and grades
will reliably certify its own idea of the voice.

Two structural answers, both borrowed from this repo's own principles:

- **Separated grading.** The producer is never the sole grader
  ([`GUIDING-PRINCIPLES.md`](https://github.com/HiQS-Labs/XYZ-forge/blob/development/GUIDING-PRINCIPLES.md), principle 12).
- **A green verdict needs a witnessed red control.** A review that cannot fail is not evidence
  (principle 13). Hence the lineup in Layer 3.

The same source also reports that cross-metric correlations are near zero (|r| < 0.07), so
**single-lens judging is unreliable** — the Reader runs two firewalled lenses, not one.

## The three roles

| Role | Sees | Never sees | Produces |
|---|---|---|---|
| **A — Cartographer** | Samples, anti-samples | The brief | Voice map: exemplar bank + fingerprint |
| **B — Drafter** | Brief, voice map, exemplars | The Reader's rubric | Structure outline, then draft |
| **C — Reader** | Draft + lineup, brief | **The voice map** | Blind verdict, flatness audit, findings |

Withholding the brief from A keeps the map descriptive rather than aspirational. Withholding the
rubric from B prevents writing to the test. Withholding the map from C is what makes C's verdict
worth anything.

---

## Layer 1 — Map the voice (Role A)

Read the samples cold. Produce a voice map with two halves.

**Half 1 — the exemplar bank.** Verbatim, attributed, at least 12 entries:

- 3–5 **openings** — how this author enters a piece
- 3–5 **transitions** — how they move between ideas
- 2–3 **closings**
- 3–5 **signature moves** — the constructions that recur and would be recognized

Quote exactly. A paraphrased exemplar is worthless; it is the model's voice wearing the author's
name. This bank is the primary conditioning asset — the research finding is that few-shot exemplars
buy up to **23.5× more style-matching accuracy** than describing the style, and that continuation
against real prefix text reaches near-total style agreement
([arXiv:2509.24930](https://arxiv.org/abs/2509.24930)).

**Half 2 — the fingerprint.** Measurable, not impressionistic:

| Dimension | Record |
|---|---|
| Sentence length | Range and **variance** — the rhythm, not the mean |
| Paragraph shape | Typical length; do they use one-line paragraphs? |
| Punctuation habits | Em-dashes, semicolons, parentheticals, ellipses — with frequency |
| Person and stance | First/second/third; hedged or declarative |
| Lexical tics | Words they reach for; words they conspicuously avoid |
| Register floor and ceiling | How casual and how formal do they actually get |
| Structural habits | Lists? Headers? Questions? Anecdote-first or claim-first? |
| **Never-does list** | From anti-samples — the negative space |

Close the map with **three falsifiable predictions**: specific things that must be true of a
genuine piece by this author. These are what Layer 3 tests. A prediction like "sounds warm" is not
falsifiable; "opens with a concrete scene, not a thesis statement" is.

`NEXT: Drafter`

## Layer 2 — Draft (Role B), in two passes

Do not write voice and structure at once; they pull against each other and voice loses.

**Pass 2a — structure, voice off.** Outline in plain functional prose: what each section must
accomplish, in what order, with what evidence. Confirm the brief is actually satisfiable. If a claim
needs a fact you do not have, mark it `[GAP: …]` — never write around it.

**Pass 2b — voice on.** Write the draft with the exemplar bank in front of you. Working rules:

- **Vary deliberately.** Match the author's sentence-length *variance*, not their average. Uniform
  rhythm is the single loudest tell, and it is measurable: human essays average perplexity **29.5**
  against roughly **15–16** for matched machine output, with ~90% of machine texts falling below a
  threshold that only ~15% of human texts fall below
  ([arXiv:2509.24930](https://arxiv.org/abs/2509.24930) — the abstract reports 15.2, the results
  section 16.07; the gap, not the decimal, is the point).
- **Commit.** Hedging stacks ("it's worth noting that it may perhaps") are a register, and rarely the
  author's.
- **Honor the never-does list** even when a forbidden construction would be the elegant choice.
- **Leave the seams.** Real writing has asymmetric sections and unresolved asides. Sanding those off
  is what makes copy read as machined.

Carry any `[GAP: …]` markers into the draft unresolved. They are the Drafter's honest output.

`NEXT: Reader`

## Layer 3 — Blind adversarial read (Role C)

The Reader must not have seen the voice map. Build the lineup first:

1. The draft.
2. **A real control** — an unused genuine sample by the target author.
3. **A flat control** — a passage on the same subject written deliberately in generic
   assistant register: even sentence lengths, hedged, tidy, listy.

Label them only as A/B/C, order shuffled. Then run two firewalled lenses.

**Lens 1 — blind attribution.** Which passage is by the target author? Rank all three by
author-likelihood and state the discriminating features. *Then* reveal the labels.

The control is the falsification mechanism, and reading it correctly is the whole job:

| Reader outcome | What it means |
|---|---|
| Picks the real control first, draft second | Working as intended — findings are trustworthy |
| Picks the draft over the real control | **Do not celebrate.** This is the PersonalBench circularity signature — the reader is rewarding a machine-flavored idea of the voice. Discard the verdict, re-read, note it in the receipt |
| Cannot separate the flat control from the draft | The draft failed. Revision is mandatory, not optional |
| Ranks confidently with vague reasons | Verdict is unreliable — re-run demanding feature-level evidence |

**Lens 2 — flatness audit**, run independently of Lens 1 and *without* its verdict:

- Sentence-length series for the draft — report the actual variance, and flag any run of 4+
  sentences within a narrow band
- Hedge density, and every stacked hedge
- Repeated openers, transitions, and structural parallelism
- Tricolons, "not only… but also", "it's not just X, it's Y" and their kin
- Register drift — where the piece leaves the author's floor or ceiling

Findings must be **line-referenced and rankable**: severity, location, and the specific fix. Prose
like "could be more natural" is not a finding.

`NEXT: Coordinator`

## Layer 4 — Reconcile, then revise once

The coordinator (you) resolves the two lenses. They will disagree; that is why there are two.

- **Both lenses agree** → fix it.
- **Lens 1 clean, Lens 2 flags flatness** → fix the rhythm. Voice can be right while predictability
  is wrong; these are separate axes, not one score.
- **Lens 1 flags voice, Lens 2 clean** → an on-rhythm draft in the wrong voice. Re-read the exemplar
  bank; this usually means the Drafter wrote from the fingerprint table instead of the exemplars.
- **Test the three predictions** from Layer 1 explicitly. Each: met / missed / not-applicable.

Then **one** revision pass by the Drafter, addressing ranked findings only. Resist a second full
cycle — past one revision, drafts converge toward the reviewer's preferences rather than the
author's voice. If it still fails, the honest move is a different draft or better samples, not a
third pass.

## Output contract

The thread file ends with all five, in order:

```markdown
STATUS: Approved | Needs-Samples | Failed
NEXT: —

## Voice map            (exemplar bank + fingerprint + 3 predictions)
## Draft                (final, with any [GAP: …] preserved)
## Blind review         (lineup result, both lenses, ranked findings)
## Revision log         (what changed, what was declined and why)
## Receipt              (below)
```

The receipt is the deliverable that makes this honest:

```markdown
### Receipt
- Samples used: N pieces (+ M anti-samples) — confidence: high | low
- Lineup result: reader ranked [real / draft / flat] — control read correctly: yes | no
- Predictions: X of 3 met
- Flatness: sentence-length variance <draft> vs <samples>
- Open gaps: [GAP: …] items still unresolved
- **Limits:** this pass matched voice within a language model's stylistic
  regime. It does not establish human authorship, and it was not evaluated
  against any detector. (arXiv:2608.19746)
```

## Honest caveats

- **The ceiling is real and measured.** Inference-time personalization produces author-differentiated
  output (AUC 0.918 *within* generated text) yet lands at 0.484–0.508 similarity to real authors —
  **below the 0.626 cross-author human floor**. Generated text sits farther from any human author
  than two random humans sit from each other ([arXiv:2608.19746](https://arxiv.org/abs/2608.19746)).
  Closing that gap is reported to need training-time adaptation, which this skill does not do.
- **The Reader is an LLM judging an LLM.** The lineup control constrains the circularity; it does not
  abolish it. Treat a clean verdict as "no defects found by this method", never as proof.
- **Fingerprint dimensions here are hand-measured**, not the trained authorship-verification models
  the papers use. Directionally useful, not calibrated.
- **Continuation is the strongest known conditioning** (~99.9% style agreement) and is deliberately
  *not* offered as a mode: continuing a real prefix means shipping text welded to sentences the
  author actually wrote, and the same paper notes such outputs *"may evade detection by stylometric
  means."* That is the detector-evasion boundary, so the skill stops at few-shot.

## Neighbors

| Skill | Relationship |
|---|---|
| [feynman](../feynman/SKILL.md) | Plain-language *translation*; timbre is voice fidelity. Different goals |
| [honest](https://github.com/HiQS-Labs/XYZ-forge/blob/development/skills/3-weekly/honest/SKILL.md) | Two-audience assessment writing; shares the "state your limits" discipline |
| [consult](https://github.com/HiQS-Labs/XYZ-forge/blob/development/skills/1-hourly/consult/SKILL.md) | If the harness is installed, a genuine second *model* can play Role C — a real independence upgrade over role-switching |
| [relay](https://github.com/HiQS-Labs/XYZ-forge/blob/development/skills/1-hourly/relay/SKILL.md) | The Producer/Reviewer handoff pattern this pipeline imitates in a single file |
| [triangulate](https://github.com/HiQS-Labs/XYZ-forge/blob/development/skills/1-hourly/triangulate/SKILL.md) | The three-lenses-in-fixed-order shape, applied to engineering decisions |
| [better-options](https://github.com/HiQS-Labs/XYZ-forge/blob/development/skills/1-hourly/better-options/SKILL.md) | Run first if the brief itself may be wrong |

**Upgrade path.** With the XYZ harness available, Roles A/B/C map onto real relay turns with
separate model backends, which replaces role-switching with actual independence. This skill is the
zero-install form of the same discipline, not a lesser version of it.

## Provenance

Design constraints here are taken from two peer-reviewed/preprint sources, both verified against the
arXiv record:

- **Jemama, R. & Kumar, R. — "How Well Do LLMs Imitate Human Writing Style?"**
  [arXiv:2509.24930](https://arxiv.org/abs/2509.24930) · accepted, IEEE UEMCON 2025 · code:
  <https://github.com/rajeshjnu2006/writing-style-uemcon2025>
  Supplies: exemplars over descriptions (few-shot up to 23.5× zero-shot; zero-shot summaries are not
  effective anchors); prompting strategy outweighs model size; **fidelity and detectability are
  separable** (human perplexity 29.5 vs machine ~15–16). Note: the abstract reports 15.2 and the
  results section 16.07 — an internal inconsistency in the source, immaterial to the design.
- **Sawant, Y. G. — "PersonalBench: Measuring the Authorship Gap in LLM Personalization"**
  [arXiv:2608.19746](https://arxiv.org/abs/2608.19746) · code:
  <https://github.com/yashsawant22/personalbench>
  Supplies: the authorship gap (0.484–0.508 vs the 0.626 human floor); **judge circularity** — the
  LLM judge preferred a machine profile (0.542) over the real author (0.427); near-zero cross-metric
  correlation (|r| < 0.07), hence two firewalled lenses rather than one score.

**Flagged for the reader:** applied "humanizer" utilities — including tools circulated for papers
and grant writing — are *not* used as a foundation here. They are applied products rather than
evaluated method, they are contested within the research community, and their goal (reducing
detector signal) is explicitly outside this skill's boundary. They are named only to mark the line.

Neither paper endorses this skill. The pipeline is an engineering response to their findings, and
inherits their limits — most importantly that no amount of prompt-time work has been shown to reach
human authorship.
