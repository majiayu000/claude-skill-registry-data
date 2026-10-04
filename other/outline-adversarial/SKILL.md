---
name: outline-adversarial
description: Skeptical pushback on the outline before drafting starts. Asks whether the outline is MECE, BLUF, problem-agitate-solution; whether it covers the topic better than the SERP top-5; whether sections duplicate; whether each section earns its visual. One revision pass on FAIL (BLOG_AGENT_OUTLINE_REVISION_BUDGET, default 1).
allowed-tools: Read, Write, Bash, Task
---

# Outline Adversarial Skill

Phase 3 of PLEAA-392 (PLEAA-418, 2026-05-06). Neo's brief:

> There's something I really like — pushback where the blog says something and a skill basically pushed back, and then he can make multiple drafts. It's like a thing kind of pushed back, and maybe if something is wrong, he can rethink it. I like that.

The orchestrator dispatches this skill **after** stage 3 (`/outline`) writes
`content-pipeline/3-outlines/{slug}.md` and **before** stage 4
(`/product-mentions`) annotates it. If the adversarial verdict is `FAIL` and a
revision budget remains, the orchestrator re-dispatches `/outline` with the
critique as a brief, then re-runs this skill. The runlog at
`.runs/{slug}-budgets.json` keeps the count.

## Input

For slug `{slug}`:

- `content-pipeline/3-outlines/{slug}.md` (the outline to push back on)
- `content-pipeline/1-research/{slug}.md` (so the adversarial knows what the
  SERP top-5 covered and what the angle is supposed to be)
- `content-pipeline/2-reference/{slug}.md` (so the adversarial knows what
  internal modules already exist; outlines that re-explain owned material lose)
- `templates/editorial-principles-visuals.md` (the 9-step "does this section
  earn a visual?" rule)
- `brand-config.md` (audience, voice, forbidden patterns)

## Process

1. Spawn a `Task` sub-agent with the brief below. The agent reads the inputs
   and returns a critique. Do NOT let the agent rewrite the outline — its only
   job is to push back.

2. Combine the agent's output into
   `content-pipeline/quality-checks/{slug}-outline-adversarial.md` with the
   exact format described under **Output**.

3. Print the verdict + CRITICAL count to stdout so the orchestrator can read it
   in the agent return.

## Adversarial sub-agent brief

> You are a skeptical content editor pushing back on the outline at
> `content-pipeline/3-outlines/{slug}.md`. The article hasn't been drafted yet
> — your only job is to make sure the structure is sound BEFORE someone burns
> 2,000 words on a bad spine.
>
> Read these in order:
> 1. `content-pipeline/3-outlines/{slug}.md`
> 2. `content-pipeline/1-research/{slug}.md` (note the SERP top-5 + the
>    recommended angle)
> 3. `content-pipeline/2-reference/{slug}.md` (existing brand articles)
> 4. `templates/editorial-principles-visuals.md`
> 5. `brand-config.md`
>
> Push back on five questions. Be specific — point at H2s by name and line
> ranges, not vague impressions:
>
> 1. **MECE.** Are the H2s mutually exclusive and collectively exhaustive? Any
>    overlap between sections? Any obvious gap a competing SERP article covers
>    that this outline doesn't?
> 2. **BLUF on every opener.** Does each H2 stub start with a clear "answer
>    first" sentence, or do any of them throat-clear ("In today's world…")?
> 3. **Problem-agitate-solution arc.** Does the outline take the reader from
>    pain to resolution, or is it a flat list of facts?
> 4. **Differentiation vs SERP top-5.** Does this outline cover the topic
>    *better* than the SERP top-5 the research dossier surfaced, or just match
>    them? Name at least one angle a competitor takes that this outline
>    duplicates and one angle this outline takes that competitors miss.
> 5. **Visuals earn their place.** For each section with a non-`none` Visual,
>    does the section actually *need* one per the 9-step rule, or is it a
>    decorative placeholder? Which sections without a visual should have one?
>
> Output:
>
> - 5–8 specific findings, each tagged `CRITICAL`, `HIGH`, `MEDIUM`, or `LOW`.
>   - `CRITICAL` = drafting on top of this will produce a worse article than
>     the SERP top-5 or violate brand-config rules. Examples: missing H2 the
>     SERP all cover, two H2s that say the same thing, BLUF that contradicts
>     the visual, comparison section without honest verdicts on Pleasur.AI.
>   - `HIGH` = the article will pass quality gates but feel weak.
>   - `MEDIUM`/`LOW` = polish.
> - 1 thing that genuinely works (so you stay calibrated, not contrarian for
>   its own sake).
> - A one-line **Verdict: PASS** or **Verdict: FAIL**. PASS = no CRITICAL
>   findings. FAIL = at least one CRITICAL.
>
> Do NOT rewrite the outline, suggest replacement H2s, or be polite. Under 600
> words.

## Output

Write `content-pipeline/quality-checks/{slug}-outline-adversarial.md`:

```markdown
# Outline Adversarial — {slug} (Pass {N})

## Verdict: **PASS** or **FAIL**

Pass {N} of {budget+1} (revision budget BLOG_AGENT_OUTLINE_REVISION_BUDGET={budget}).

## Findings

### CRITICAL

- [section/line] one-line finding. Why it kills the draft.

### HIGH

- ...

### MEDIUM

- ...

### LOW

- ...

## What Works

- [section/line] one specific thing that's good.

## Recommendation

- If Verdict is PASS: advance to stage 4 (/product-mentions).
- If Verdict is FAIL: re-dispatch /outline with the CRITICAL items as the
  revision brief (orchestrator handles this), then re-run this skill.
```

The `## Verdict:` line MUST be exactly that format (markdown bold) so
`pipeline_gate.py` can parse it.

## How the orchestrator handles FAIL

The orchestrator (`/blog-pipeline`) calls this skill after stage 3 and reads
the verdict. On FAIL:

1. Read `.runs/{slug}-budgets.json` (or call
   `python scripts/adversarial_runlog.py used {slug} outline`).
2. If `used < budget`:
   - Increment via `python scripts/adversarial_runlog.py increment {slug} outline`.
   - Re-dispatch stage 3 (`/outline`) with the adversarial critique as the
     revision brief — specifically the CRITICAL findings.
   - Re-run this skill.
3. If `used >= budget`:
   - Write `content-pipeline/9-needs-review/{slug}.md` with the CRITICAL list +
     "outline adversarial budget exhausted".
   - HALT — do not advance to stage 4. The pipeline_gate will also enforce
     this independently.

## Why this skill exists

Without it, structural problems surface only at stage 6 (quality-check) AFTER
2,000 words have been drafted. Catching MECE violations and missing-from-SERP
gaps at the outline stage saves a full revision cycle later — drafting on a
broken spine and then editing prose can't fix structure.

## When the adversarial sub-agent says everything is fine

Be skeptical of all-praise critiques. Re-run the sub-agent with a stronger
brief if the critique has fewer than 3 specific findings or zero `MEDIUM`+
items. An outline with literally zero structural concerns is rare; more often
the agent isn't being adversarial enough.
