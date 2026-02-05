---
name: finetune-generate
description: Use when generating synthetic training data for multi-turn conversation fine-tuning. Triggers - have design artifacts ready, need to generate conversations, ready to assess quality. Requires finetune-design first.
---

# Fine-tune Generate

Iteratively generate and filter training data until quality stabilizes.

## Prerequisites

Complete [finetune-design](../finetune-design/SKILL.md) first. You need:

- [ ] Model choice and token constraints
- [ ] Input taxonomy
- [ ] Evaluation rubric with calibration examples
- [ ] Persona template
- [ ] User simulator, assistant, and system prompts

## Outputs

By the end of this phase, you will have:

- [ ] `training_data.jsonl` — Filtered, sliced training examples
- [ ] `generation_stats.md` — Pass rates, criterion breakdown, iterations
- [ ] `prompt_versions/` — History of prompt iterations

---

## The Core Loop

**This is the most important part of the entire pipeline.**

```
┌─────────────────────────────────────────────────────────────┐
│  TIGHT LOOP (5 transcripts per iteration)                   │
│                                                             │
│  1. Generate 5 transcripts                                  │
│  2. Assess with rubric (all backends)                       │
│  3. HUMAN REVIEWS both transcripts AND assessments          │
│  4. Iterate based on human judgment                         │
│  5. Repeat until ≥70% pass rate AND human satisfied         │
│                                                             │
│  Then: Scale to full volume                                 │
└─────────────────────────────────────────────────────────────┘
```

### Why 5 Transcripts?

- Small enough for human to actually READ each one carefully
- Fast feedback (minutes, not hours)
- See patterns without wasting compute
- Iterate while context is fresh

### Why Human-in-the-Loop? (Non-Negotiable)

**Human review is required, not optional.** The human reviews BOTH transcripts AND assessment results:

| Human reviews... | Looking for... |
|------------------|----------------|
| Transcripts | Quality issues the rubric might miss |
| Assessment results | False positives (passed but shouldn't have) |
| Assessment results | False negatives (failed but seems fine) |
| Both together | Gaps in what the rubric even checks |

**Without human review:**
- You're optimizing against a potentially broken metric
- False positives silently corrupt training data
- Rubric blind spots never get discovered

### Red Flags: Rationalizations to Resist

| Rationalization | Reality |
|-----------------|---------|
| "Human review slows us down" | Skipping review = optimizing against broken metric. 1 hour of review saves days of bad data. |
| "Pass rate is high, must be fine" | High pass rate with single backend misses 20-30% of issues. Multi-backend + human review required. |
| "We can add calibration examples later" | Without calibration examples, backends disagree silently. Add them during design. |
| "The rubric is complete" | Rubrics evolve (e.g., 12→18 criteria). New failure modes emerge. |
| "One assessor backend is enough" | Single backend gave transcript 1000 perfect 1.0; other backends caught 4 failures. |
| "Let's just scale and filter later" | Scaling before 70% pass rate wastes compute. Fix prompts first. |

**If you catch yourself using any of these rationalizations: STOP. Follow the gates.**

### Dual Iteration

You iterate on TWO things, not one:

| When you see... | Iterate on... |
|-----------------|---------------|
| Transcript quality issues | Generation prompts (user-sim, assistant) |
| Assessment seems wrong | Assessor prompt, criteria wording |
| Backend disagreement | Calibration examples for that criterion |
| Missing failure mode | Add new criterion to rubric |
| Pass rates high but something feels off | Run expert role-play critique |

**The rubric is never "done."** In one project, criteria evolved: 12 → 14 → 16 → 17 → 18.

**Expert role-play critique is required** — periodically have Claude role-play domain experts to critique your rubric and small transcript batch directly. This catches blind spots invisible from your own perspective. See [assessment-guide.md#expert-role-play-critique](assessment-guide.md#expert-role-play-critique).

---

## Workflow

### Step 1: Tight Iteration Loop

For each batch of 5 transcripts:

1. **Generate** 5 transcripts using two-agent simulation
2. **Assess** with rubric using multiple backends (Claude, Gemini, GPT-5)
3. **Human reviews** both transcripts and assessments:
   - Read each transcript: Is this actually good?
   - Read each assessment: Did the rubric catch what matters?
   - Note: false positives, false negatives, missing criteria
4. **Iterate** based on human judgment:
   - Fix generation prompts (if transcript quality issues)
   - Fix assessor prompt/criteria (if assessment issues)
   - Add calibration examples (if edge cases found)
5. **Repeat** until quality stabilizes

**Gate (before scaling):**

| Condition | Action |
|-----------|--------|
| ≥70% pass rate AND human satisfied | Proceed to scale |
| 50-70% OR human sees issues | Continue iterating |
| <50% | Major revision needed |

**Reference:** [generation-guide.md](generation-guide.md), [assessment-guide.md](assessment-guide.md)

---

### Step 2: Scale Generation

Once the tight loop stabilizes:

1. **Generate target volume** (100+ transcripts)
2. **Continue assessment** with same multi-backend approach
3. **Periodic human spot-checks** (every 20-50 transcripts)
4. **Track statistics** (pass rate, criterion breakdown)

**Warning signs during scale:**
- Pass rate drifting down → Revisit prompts
- New failure patterns emerging → Add criteria
- Perfect scores (1.0) → Suspiciously high, investigate

---

### Step 3: Audit Patterns

Run quantitative analysis on the full dataset to catch issues invisible in spot-checks:

| Check | Red Flag | Action |
|-------|----------|--------|
| Phrase repetition | Any phrase in >50% of responses | Add to anti-patterns, regenerate |
| Structural rigidity | 100% same format | Vary response structure |
| Response length ratio | Avg >2x user length | Tighten length constraints |
| Praise distribution | Late responses 2x more praise | Adjust tone consistency |

**Gate:** No audit red flags

**Reference:** [assessment-guide.md#audit-patterns](assessment-guide.md#audit-patterns)

---

### Step 4: Fixup or Reject

For failing transcripts, decide whether to fix or reject:

| Failure Type | Action |
|--------------|--------|
| Soft failures (language, tone) | Attempt fixup with entailment constraint |
| Safety gate failures | Truncate at failure point or reject entirely |
| Structural issues | Usually reject |

**Entailment constraint:** Fixed response must naturally lead to user's next message. If fix breaks continuity → truncate instead.

**If >30% need fixup:** Generation prompts need revision.

**Reference:** [assessment-guide.md#fixup-strategy](assessment-guide.md#fixup-strategy)

---

### Step 5: Slice for Training

Create training examples from full transcripts:

```
50-turn transcript → ~8-10 training examples via slicing
```

**Slicing strategy:**
- Random slice points (seeded by transcript ID for reproducibility)
- Minimum 3 exchanges before first slice
- 2-5 exchange gaps between slices
- Always include final turn

**Token validation:**
- Each slice must be under your token limit (e.g., 16K)
- Long transcripts may need truncation

**Leakage prevention:**
- Split by transcript/persona FIRST
- Then slice within each split
- Never let slices from same transcript in both train and validation

**Reference:** [assessment-guide.md#slicing-strategy](assessment-guide.md#slicing-strategy)

**Optional:** Use `hugging-face-dataset-creator` skill when ready to push `training_data.jsonl` to HF Hub.

---

## Infrastructure

### Checkpointing

Write progress after each transcript, not at the end:

```python
for persona in personas:
    transcript = generate_transcript(persona)
    save_immediately(transcript)  # Don't batch
```

### Retry with Backoff

API failures will happen. Use exponential backoff:
- Claude: 7 attempts, 1-hour max wait
- Google: Extract retry delay from error message
- OpenAI: Standard exponential backoff

### Progress Tracking

Track throughout generation:
- Transcripts generated / target
- Transcripts assessed / generated
- Pass rate (rolling and cumulative)
- Criterion failure breakdown

**Reference:** [assessment-guide.md#infrastructure](assessment-guide.md#infrastructure)

---

## Resources

| Resource | What It Contains |
|----------|------------------|
| [code/SETUP-REFERENCE.md](../code/SETUP-REFERENCE.md) | Script templates: generate.py, assess.py, slice.py |
| [code/infrastructure.py](../code/infrastructure.py) | Copy-paste ready: LLM backend, retry strategies, checkpointing |
| [examples/therapy-domain.md](../examples/therapy-domain.md) | Complete therapy example: prompts, flaw patterns, criteria |

---

## Done When

- [ ] Target training example count reached
- [ ] Pass rate stable across last 2-3 batches (≥70%)
- [ ] Human satisfied with transcript quality
- [ ] Audit patterns within thresholds
- [ ] `training_data.jsonl` validated

---

## Next Phase

→ [finetune-train](../finetune-train/SKILL.md)
