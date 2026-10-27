---
name: video-spec-eval
description: >
  LLM-as-judge eval of the spec.yaml produced by /ace:video-spec-generate
  (or /ace:video-from-program-page, or hand-authored) for an ace-web video
  program. Scores 6 quality dimensions and emits a verdict YAML with concrete
  improvement recommendations. Gated by video-spec-qa. Prompt-independent:
  derives all anchors from the template bundle (intent + example) and the
  universal rubric — no generate.prompt.md required.
disable-model-invocation: true
---

# Video Spec Eval

Grade the *goodness* of a video program's `spec.yaml`. Where
`video-spec-qa` checks structural correctness, this skill judges
quality: does the narration sound like Connect, does the spec describe
*this* program rather than generic Connect content, are the chosen
stats the most compelling ones from the source page, does the flow
build a story?

LLM-as-judge across 6 dimensions, each scored 0-10 with concrete
strengths/weaknesses and a one-line improvement recommendation. The
agent is the judge; this skill defines the rubric.

**This eval is prompt-independent.** Voice anchors live in this rubric.
Word budgets are derived from beat seconds (same formula as the generator).
Per-template fitness is anchored by the template's `intent` field and its
`example.spec.yaml` reference — both fetched from the template bundle, not
from a prose prompt file.

**Out-of-chain discipline:** the template's `intent` and `example_yaml` are
thin same-chain anchors produced by the same authoring pipeline that generated
the spec. **Source Fidelity — graded against the real source page, an
out-of-chain anchor — therefore remains the dominant, un-inflatable dimension.**
Do not award high Source Fidelity scores without cross-checking the spec against
the actual source URL.

See `skills/_eval-template.md` for the shared eval contract (verdict
YAML format, severity rules, inflation guard).

## Inputs

Pipeline-only: grades a video run's spec, which exists only in a run.

| Source | Artifact | Used for |
|---|---|---|
| ace-web Drive | `videos/<slug>/runs/<run-id>/spec.yaml` | the spec under judgment |
| Source URL (optional) | `provenance.generated_from` page content | cross-check that the spec describes the *actual* program (out-of-chain anchor — dominant dimension) |
| Template bundle | `GET /api/w/<ws>/videos/templates/<id>` → `meta.intent` | per-template narrative thesis (thin same-chain anchor) |
| Template bundle | `GET /api/w/<ws>/videos/templates/<id>` → `example_yaml` | few-shot exemplar of what good looks like for this template |

No `generate.prompt.md` is required. If a template has one, it is ignored
by this eval.

## Products

- `video-spec-eval_verdict.yaml` per the canonical `Verdict` schema
  (`lib/verdict-schema.ts`). The skill prints it to stdout for the
  caller to persist.

## Process

1. **Confirm QA passed.** Skip the eval if `video-spec-qa` failed
   irrecoverably — quality grading on a structurally broken spec is
   noise. (Operator override: pass `--ignore-qa` to grade anyway.)

2. **Read the spec.yaml from ace-web** (same access path as
   video-spec-qa step 1).

3. **Re-fetch the source page** at `provenance.generated_from`. If
   the URL 404s or the spec has no provenance.generated_from, set
   `source_available = false` and switch the **Source Fidelity**
   dimension to its no-source branch (score from internal coherence
   only).

4. **Fetch the template bundle** for `provenance.template`:

   ```bash
   curl -sS -H "Authorization: Bearer $ACE_WEB_PAT_TOKEN" \
     "$BASE_URL/api/w/$WORKSPACE_SLUG/videos/templates/$TEMPLATE_ID"
   ```

   Extract:
   - `meta.intent` — the template's narrative thesis (1–3 sentences).
     This is the per-template fitness anchor: does the spec fulfill the
     intent? Compare the spec's story arc against the intent.
   - `example_yaml` — the fully-filled reference spec. Study it as the
     "what good looks like" benchmark for voice, specificity, beat
     structure, and card language for this template.
   - `skeleton_yaml` — read to derive beat seconds and confirm which beats
     are present (incl. whether `problem`/`impact` stat beats exist).

5. **Derive per-beat word budgets** from beat seconds (same formula
   as the generator — non-negotiable, applies to all templates):

   ```
   target_words = round(beat_seconds × 2.5)
   min_words    = target_words - 2
   max_words    = target_words + 2
   ```

   Example: a `scene` beat of 8s → target 20w (range 18–22). A `hook` beat
   of 4s → target 10w (range 8–12). A `cta` beat of 0s → empty, expected.
   Use these derived budgets — not any per-template table in a prose prompt.
   Penalize beats that exceed `max_words` under Story Compression (dim 6).

6. **Score each dimension below 0-10.** For each, capture:
   - `score: <int 0-10>`
   - `strength: <one-liner>` — what's working
   - `weakness: <one-liner>` — what's the worst issue
   - `recommendation: <one-liner>` — one concrete edit

7. **Produce overall verdict.**
   - `pass` — every dimension ≥ 7
   - `revise` — any dimension 5-6 (operator should edit before render)
   - `fail` — any dimension ≤ 4 (regenerate the spec)
   - `summary` — 2-3 sentences total. Lead with the biggest lever.

## Dimensions

### 1. Narration Voice

**Rubric:** Does the narration read like Connect's voice — plain,
declarative, specific? Or does it drift into marketing-ad mode (long
sentences, abstract nouns, "powering / enabling / transforming")?

| Anchor | Score |
|---|---|
| Every beat reads as documentary lower-third. Numbers over adjectives. Active voice. Short sentences. | 9-10 |
| Mostly tight; 1-2 beats use a marketing-ad phrasing the operator should retune. | 7-8 |
| Multiple beats read as ad copy. Long sentences, abstract subjects ("our solution leverages..."). | 4-6 |
| Generic Connect marketing copy. Could plausibly apply to any Connect program. | 0-3 |

**Common penalties:** "leverage", "empower", "transform", "robust",
"comprehensive", "world-class" — the static QA catches a small list,
but this dimension catches the broader register.

### 2. Stat Selection

**Rubric:** Did the agent pick the *most compelling* numbers from the
source for `problem.big` and the two `impact[]` entries? Or did it
grab the first numbers it saw?

**Applicability:** this dimension applies only when the skeleton has
`problem` and/or `impact` stat beats (check `skeleton_yaml` or the
spec's `problem:` block). For explainer-mode templates (no `problem:`
beat, `impact` carries value-prop cards instead of outcome stats),
score this dimension N/A and note it in the verdict; it does not
factor into the overall score.

| Anchor | Score |
|---|---|
| problem.big is the headline number a reader would remember from the source. Both impact entries are the highest-leverage ones. | 9-10 |
| Either problem or impact uses a less-than-optimal number; the swap is obvious. | 7-8 |
| Both problem and impact are suboptimal; better stats exist on the source page. | 4-6 |
| Stats appear made up, are wrong, or fail to connect to this program. | 0-3 |

**Common penalties:** picking "X% completion" when "$Y per beneficiary"
is in the source; using a Connect-level stat where the program has
its own; using a vanity metric over an outcome metric.

**Audio/card stat parity (scored here, not elsewhere):** numbers spoken
in `narration` (problem/impact) must also appear as on-screen stat
**cards** — the cards are what the viewer remembers, and the template
intent requires the load-bearing numbers to be *memorable*, not merely
spoken. When the narration voices a stat that is not carded (e.g. an
88% completion rate spoken with no `impact[]` card), apply a mild Stat
Selection penalty (knock a point). Exception: acceptable when the two
strongest stats ARE carded and the uncarded one is genuinely
subordinate — but **flag (do not exempt) if the uncarded stat is
co-equal** with a carded one. Score this once here; do not also
penalize it under Story Compression.

### 3. Beat Coherence

**Rubric:** Does the spec's beat sequence flow as a story, or read as
disconnected sentences? The arc this template implies is declared in
`meta.intent` — compare the spec's actual narrative flow against it.
The general Connect arc is: hook → cycle (the how) → handoff (this
program) → scene (the field) → [problem (the stakes)] → product (the
proof) → impact (the result) → cta (empty / outro). Stat beats may be
absent for explainer-mode templates. Read the `example_yaml` to
understand what "clean handoffs" look like for this specific template.

| Anchor | Score |
|---|---|
| Each beat sets up the next. A listener with no Connect context follows the arc declared in the template's intent. | 9-10 |
| One beat feels bolted on or stylistically off-key; the rest land. | 7-8 |
| Two or more transitions feel abrupt; the listener has to recover context. | 4-6 |
| The arc is broken — beats appear in the wrong order or contradict each other. | 0-3 |

### 4. Source Fidelity

**Rubric:** Does the spec describe the *actual* program from the
source page, or is it generic Connect content with the program name
swapped in?

| Anchor | Score |
|---|---|
| Field-level specificity: country, partner names, activity descriptions, FLW tasks match the source verbatim or near-verbatim. | 9-10 |
| Mostly specific; one or two fields generic where the source has detail. | 7-8 |
| Half-specific: country + name are right but activities, partners, stats are generic. | 4-6 |
| Could plausibly apply to a different Connect program with no edits. Hallucinated stats or activities. | 0-3 |

**Brief-as-anchor branch** (the source is a structured brief, not a
live URL — `provenance.generated_from` is a brief/handle, not a
fetchable page): the anchor is the brief text. "Verbatim/near-verbatim"
means the spec uses the brief's actual program name, country, FLW
tasks, and numbers, inventing nothing beyond it. **Critically: under-use
of available specificity caps the score below 9.** If the brief supplies
named places (e.g. four districts) or scale figures the spec collapses
to generic "the country" / "four districts", that is a real fidelity
miss — cap at 8 even when every stated fact is correct. Reserve 9-10 for
specs that mine the brief's distinctive detail, not merely avoid errors.
**Graduated under-use threshold (for reproducibility):** count the
distinct brief specifics that are available but unused — named places,
co-equal scale figures, named partners/funders. **0 omitted → up to 9-10;
1-2 omitted → cap 8; 3+ omitted → cap 7; collapsed to country-only with
no named detail → 5-6.** Apply the count, don't eyeball it.

**No-source branch** (`source_available = false`, no brief and no URL):
grade on internal coherence only — does the spec hang together?

### 5. Tagline Mirror

**Rubric:** Does `narration.by_beat.hook` paraphrase Connect's
tagline "Pay for verified service delivery, not planned activity"
without inventing a different tagline?

| Anchor | Score |
|---|---|
| Verbatim or near-verbatim ("Connect pays for verified service delivery, not planned activity"). | 9-10 |
| Strong paraphrase keeping all four key concepts (pay / verified / service / delivery). | 7-8 |
| Drift — drops one concept ("we deliver" without "verified"). | 4-6 |
| New tagline invented from whole cloth. | 0-3 |

**Note:** the static QA catches gross divergence (3+ of 4 key tokens
required). This dimension catches the subtler stylistic drift.

### 6. Story Compression

**Rubric:** Within each beat's word budget, did the agent use the
words to maximum effect? Or did it pad with filler to hit the target?

| Anchor | Score |
|---|---|
| Every word earns its place. A reader couldn't trim by 2 words without losing meaning. | 9-10 |
| One or two beats use filler ("structured care that is delivered in their homes"). | 7-8 |
| Multiple beats pad; a sharp editor could compress by 20% with no loss. | 4-6 |
| Most beats are bloated. The 60s of audio carries 30s of content. | 0-3 |

**Budget check (reproducible — REQUIRED):** fetch `skeleton_yaml` (and
`programs/_defaults.yaml`) to read each beat's seconds, then derive the
ceiling per beat as `max = round(beat_seconds × 2.5) + 2`. Recount each
beat's actual words. **Any beat over `max` is a hard compression
defect** (the audio gets cut mid-word) — knock at least one point and
name the over-budget beat in the weakness. Do not grade this dimension
by feel; the budget is arithmetic. The recurring offender is the short
`problem` beat (~8s → max ~22 words); flag it when it carries both a
stat and a stakes clause.

## Verdict YAML shape

```yaml
schema_version: 1
skill: video-spec-eval
target: dimagi-team/kangaroo-mother-care/run-001
ran_at: 2026-05-15T12:34:56Z
capture_path: videos/kangaroo-mother-care/runs/run-001/spec.yaml
overall_score: 82
verdict: pass         # pass | revise | fail
qa_gated: true        # was QA passing when eval ran?
source_available: true
dimensions:
  narration_voice:
    score: 9
    strength: "Every beat reads as documentary lower-third."
    weakness: "Cycle beat uses 'verified' twice — feels redundant."
    recommendation: "Change cycle beat's second 'verified' to 'confirmed'."
  stat_selection: {score: 7, strength: ..., weakness: ..., recommendation: ...}
  beat_coherence: {...}
  source_fidelity: {...}
  tagline_mirror: {...}
  story_compression: {...}
summary: |
  Strong source fidelity and voice; the main lever is tightening
  the cycle beat's word choice. Spec is ship-ready after one edit.
```

## Inflation guard

Eval inflation is real — every well-written spec wants a 9. To keep
the rubric calibrated:
- Default ceiling for a first-pass agent-authored spec is 8 on any
  dimension. Reserve 9-10 for specs that genuinely could not be
  improved.
- If you find yourself scoring 9+ on every dimension, re-examine: am I
  grading what's *there* or am I grading absence of obvious flaws?
- A 7 is a good score. It means "ship-ready with one or two
  operator edits."

## MCP Tools Used

- Google Drive: `drive_read_file` (spec.yaml)
- WebFetch: `provenance.generated_from` to re-fetch the source page (out-of-chain anchor)
- HTTP (`curl`): `GET /api/w/<ws>/videos/templates/<id>` to fetch template bundle (intent + example + skeleton)
- Bash: writing the verdict YAML to a temp path

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-05-15 | Initial skill paired with /ace:video-from-program-page. Six dimensions covering voice, stats, coherence, fidelity, tagline, and compression. | ACE team |
| 2026-06-09 | Made prompt-independent: replaced "load generate.prompt.md" step with template bundle fetch (intent + example_yaml + skeleton); derived word budgets from beat seconds formula; updated step numbering; added stat-beat applicability guard; updated Beat Coherence to be template-agnostic; honored out-of-chain discipline principle. | ACE team |
