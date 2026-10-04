---
name: quality-check
description: Benchmark-relative quality gate. Scores the draft against the research dossier's beat spec (depth, consensus coverage, evidence) plus AI-tell and voice signals, runs an adversarial read armed with the SERP benchmark, and emits the verdict that gates the pipeline.
allowed-tools: Read, Write, Bash, Task
---

# Quality Check Skill

Reads the draft and produces a quality scorecard + a punch list of specific fixes. **The question this skill answers is not "does the draft comply with our rules" — it's "a reader opens this article and the #1 ranking result side by side: which one do they keep?"** A draft can be perfectly compliant and still lose; that's a FAIL.

History (why this skill looks the way it does): the previous rubric weighted forbidden phrases + voice metrics + BLUF heuristics and let a 1,100-word, 4-item, no-table listicle score 95 against a SERP of 2,500-word, 9-item, table-bearing competitors. Benchmark-relative dimensions now dominate the score.

## Input

For slug `{slug}`:
- `content-pipeline/5-drafts/{slug}.md` (the draft to score)
- `content-pipeline/1-research/{slug}.md` (**the BEAT SPEC + benchmark — required**; if it lacks a BEAT SPEC section, flag the dossier as legacy and recommend re-running /research)
- `content-pipeline/3-outlines/{slug}.md` (coverage map, word targets)
- `brand-config.md` (forbidden phrases, audience)
- `examples/voice/*.md` (voice baseline)
- `.claude/skills/draft/references/voice-guide.md`

## Process

1. **Run the mechanical metrics script:**
   ```bash
   python .claude/skills/quality-check/scripts/quality_check.py "<slug>"
   ```
   (Use `--stage cited` when re-running after /verify-claims.) This writes `content-pipeline/quality-checks/{slug}-metrics.md` with subscores for: depth vs benchmark (25), consensus coverage (20), AI tells (25), evidence (15), structure (15) — plus CRITICAL findings and a mechanical score.

2. **Voice + judgment read (your 0–100, worth 40% of the final).** Read 1–2 articles from `examples/voice/` and then the draft, as an editor. Judge:
   - Would the byline survive on a serious blog? Does it sound like the examples or like an AI?
   - Specificity: does every section teach something concrete, or does it gesture?
   - Product mentions: demonstrated naturally, or bolted on?
   - Information gain: is the `[GAIN]` section genuinely not on page 1 (check against the dossier's top-page summaries)?

3. **Run the adversarial read — armed with the benchmark.** Spawn a Task sub-agent:
   > Read `content-pipeline/1-research/{slug}.md` (note the BEAT SPEC and the top-page summaries), then read the draft at `content-pipeline/5-drafts/{slug}.md` as a skeptical industry expert who has read every page-1 result for "{keyword}". The brand is {brand}; the audience is {audience}. Answer first: **if this draft and the current #1 were side by side, which would you keep, and why — in 3 sentences.** Then list the 5 weakest things about the draft relative to what's ranking. Be specific — sentences, sections, missing material. Include 1 thing that genuinely works. Do NOT rewrite or be polite.

   Save to `content-pipeline/quality-checks/{slug}-adversarial.md`. Be skeptical of all-praise critiques shorter than 200 words — re-run with a sharper brief.

4. **Combine into the report** at `content-pipeline/quality-checks/{slug}.md`:
   - **Verdict** at top: final score = 0.6 × mechanical + 0.4 × judgment. `PASS` (≥85 **and** no CRITICAL finding **and** no mechanical dimension below 60% of its weight **and** the adversarial read doesn't conclude "keep the competitor"), `BORDERLINE` (70–84 or adversarial-negative), `FAIL` (<70 or any CRITICAL).
   - Metrics summary (numbers, not raw dumps)
   - Adversarial critique
   - **Punch list** — specific fixes ordered by severity, each pointing at a section
   - **Recommendation** — proceed to `/verify-claims`, send back to `/draft` (voice/prose problems), or send back to `/outline` / `/research` (depth/coverage problems — do NOT ask /draft to fix a structural deficit)

5. **On FAIL:**
   - **Autonomous mode (`BLOG_AGENT_AUTONOMOUS=1`)**: don't stop; emit verdict + punch list and return cleanly. The orchestrator owns the retry budget (`BLOG_AGENT_REVISION_BUDGET`). Route matters: depth/coverage CRITICALs → the revision brief targets the **outline** and re-drafts affected sections; prose CRITICALs → the revision brief targets the draft.
   - **Interactive mode**: stop and tell the user what failed and where to re-enter the pipeline.

## Output

- `content-pipeline/quality-checks/{slug}.md` (combined report, verdict at top)
- `content-pipeline/quality-checks/{slug}-metrics.md` (mechanical)
- `content-pipeline/quality-checks/{slug}-adversarial.md` (adversarial)

## Scoring dimensions

| Dimension | Weight | What kills it |
|---|---|---|
| Depth vs benchmark | 25 (mech) | <70% of target words; item shortfall; missing required table |
| Consensus coverage | 20 (mech) | any must-cover topic absent |
| AI tells | 25 (mech) | forbidden phrases; crutch phrase ≥4×; uniform rhythm; throat-clearing openers |
| Evidence | 15 (mech) | low claim density; <8 real links; naked `[link]` post-citation |
| Structure | 15 (mech) | flat H2 structure; missing intro/conclusion |
| Judgment overlay | 40% of final | sounds AI; no information gain; salesy mentions; loses the side-by-side |

**A perfect-compliance thin article cannot pass.** Depth floors bind no matter how clean the prose is.

## Why this skill exists

Without it, thinness and AI tells get caught at the board's review — the most expensive place. Catching them here means the orchestrator can regenerate before `/verify-claims` spends citation work on prose that was going to be rewritten anyway.
