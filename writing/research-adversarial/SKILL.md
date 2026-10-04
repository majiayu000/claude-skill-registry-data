---
name: research-adversarial
description: Skeptical pushback on the research dossier before it feeds the outline. Asks whether claims are cited, whether surprising findings are actually surprising, whether we missed the strongest competitor angle. One revision pass on FAIL (BLOG_AGENT_RESEARCH_REVISION_BUDGET, default 1).
allowed-tools: Read, Write, Bash, Task
---

# Research Adversarial Skill

Phase 3 of PLEAA-392 (PLEAA-418, 2026-05-06). The research dossier is the
single source of truth that flows into outline → draft → cited draft. If the
dossier missed the strongest competitor angle or didn't cite a load-bearing
claim, every downstream stage inherits that flaw.

The orchestrator dispatches this skill **after** stage 1 (`/research`) writes
`content-pipeline/1-research/{slug}.md` and **before** stage 3 (`/outline`)
reads it. Stage 2 (`/brand-reference`) is independent and can run in parallel
either way. If the adversarial verdict is `FAIL` and budget remains, the
orchestrator re-dispatches `/research` with the critique, then re-runs this
skill.

## Input

For slug `{slug}`:

- `content-pipeline/1-research/{slug}.md` (the dossier to push back on)
- `content-pipeline/1-research/{slug}-deep.md` (if present — the deep-research
  appendix from OpenRouter)
- `content-pipeline/1-research/{slug}-data.json` (chartable numbers — do they
  match what the prose dossier claims?)
- `content-pipeline/0-context/{slug}.md` (if present — Neo's context string)
- `brand-config.md` (audience + voice)

## Process

1. Spawn a `Task` sub-agent with the brief below.
2. Combine into `content-pipeline/quality-checks/{slug}-research-adversarial.md`
   in the format under **Output**.
3. Print the verdict + CRITICAL count.

## Adversarial sub-agent brief

> You are a skeptical research lead reviewing the dossier at
> `content-pipeline/1-research/{slug}.md` before it feeds an outline. The
> writer hasn't seen this dossier yet — your job is to make sure they don't
> build on a weak foundation.
>
> Read in order:
> 1. `content-pipeline/1-research/{slug}.md`
> 2. `content-pipeline/1-research/{slug}-deep.md` (if it exists)
> 3. `content-pipeline/1-research/{slug}-data.json` (the chartable numbers)
> 4. `content-pipeline/0-context/{slug}.md` (if it exists — Neo's context)
> 5. `brand-config.md`
>
> Push back on five questions. Be specific — quote the dossier's own
> sentences, point at section headers, name URLs:
>
> 1. **Citations.** Does every numerical claim and every surprising statement
>    cite a source URL or an internal Semrush/Strapi reference? List up to 3
>    uncited load-bearing claims by quoting them.
> 2. **Surprising findings.** The dossier should surface 3 surprising findings.
>    Are they actually surprising to a reader who already knows this niche, or
>    are they table-stakes facts dressed up as insights? Name each "surprise"
>    and rate it `actually-surprising` or `dressed-up-table-stakes`.
> 3. **Strongest competitor angle missed.** Look at the SERP top-5 the dossier
>    summarized. Which competitor angle is the strongest, and does the dossier
>    capture how to beat it — or just acknowledge it exists? Name the angle
>    and the URL.
> 4. **Data consistency.** Open `{slug}-data.json` and spot-check 3 keys
>    against the prose dossier. Do the numbers match? Any key in the JSON the
>    prose never mentions, or any prose number not in the JSON?
> 5. **Brand fit.** Does the dossier surface enough material the brand can
>    *own* (Pleasur.AI-specific data, internal modules from
>    `2-reference/{slug}.md`, the 4 product pillars from brand-config) — or is
>    it a generic survey?
>
> Output:
>
> - 5–8 specific findings tagged `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`.
>   - `CRITICAL` = drafting on this will produce a citation-thin or
>     wrong-angle article. Examples: load-bearing stat with no source, a
>     dressed-up "surprise" that's actually a 5-year-old fact, missing the
>     strongest competitor angle entirely, JSON keys that contradict the prose.
>   - `HIGH` = the dossier is correct but thin in a way that will hurt the
>     draft.
> - 1 thing that works.
> - A one-line **Verdict: PASS** or **Verdict: FAIL**.
>
> Do NOT rewrite the dossier or suggest new sources. Under 600 words.

## Output

Write `content-pipeline/quality-checks/{slug}-research-adversarial.md` with the
same skeleton as the outline-adversarial skill. The `## Verdict:` line MUST be
exactly `## Verdict: **PASS**` or `## Verdict: **FAIL**`.

## How the orchestrator handles FAIL

Same loop as outline-adversarial, but using stage key `research`:

1. `python scripts/adversarial_runlog.py can-revise {slug} research`
2. If exit 0 (budget remains): increment, re-dispatch `/research` with the
   adversarial CRITICAL list as a revision brief, then re-run this skill.
3. If exit 1 (exhausted): write `content-pipeline/9-needs-review/{slug}.md`
   and HALT.

## Why this skill exists

The dossier is upstream of every other stage. A bad dossier produces a bad
outline produces a bad draft. Editing prose downstream can't recover from
"this article was built on the wrong angle." Catch the angle problem here.

## When the adversarial sub-agent says everything is fine

Same calibration rule as outline-adversarial: re-run with a stronger brief if
the critique has fewer than 3 specific findings.
