---
name: refresh-orchestrator
description: Decide, before an expensive workflow runs, whether an artifact needs a full rebuild, a partial refresh, a skip, or a recycle. Inspects how old the artifact is and what actually changed underneath it, then returns a section-by-section plan with the token and cost savings. The cheap gate that keeps expensive generation from running on data that did not move. Built for anyone running repeatable AI workflows, customizable to your artifacts and your data sources. Trigger on "should we regenerate this", "refresh the report", "is this still fresh", "what needs updating", "when was this last run", "do we have a fresh brief", or any artifact-refresh question.
---

# Refresh Orchestrator

## What this does
Before you spend tokens rebuilding a brief, report, or analysis, this checks whether anything underneath it actually changed. It returns one of four verdicts (skip, partial, recycle, or full), a section-by-section plan of what to reuse and what to rebuild, and an estimate of what you save by not regenerating the whole thing. It is meant to be cheap, so it can gate expensive work and pay for itself many times over.

## What you'll need
You do not need to connect anything to get value today. Bring the existing artifact and the skill runs now. Connect the tools below and it reads the change signals automatically instead of you pasting them.

- Works today with: the existing artifact (paste it or point at the file) and a note of when it was last generated. The skill runs the freshness logic on what you give it.
- More powerful connected to your data sources: it reads last-modified timestamps and field-level deltas automatically, so the verdict is evidence-backed, not eyeballed.
- Sharper with a meeting or activity tool: catches new events since the last run that should force a refresh.
- Sharper with a product-analytics tool: catches a usage-trend shift that should re-open a section.

## How this runs at your connection level
This skill is never reliant on a connector. It runs on the artifact and dates you give it today and gets sharper as you connect the sources it compares against. When evidence is missing it does not guess fresh; it defaults to a full rebuild, because shipping stale work costs more than the tokens.

- **Bring your data**: paste the artifact and its generation date. The skill runs the freshness call and the section plan today. No connection required.
- **Connect your tools**: the same skill reads last-modified, new activity, and usage trend automatically and proves the verdict with dates. Same output, less effort, sharper.
- **Just exploring**: no artifact yet? Get the framework, the four verdicts, the static-versus-dynamic taxonomy, and a worked example, so you can see the shape before you wire it in.

Every run ends with the one thing that would make the next call sharper: a source to connect so a verdict can be proven instead of assumed.

## Customize this for yourself
This was built to gate a suite of GTM artifacts. Set these to your stack:

| Set this | What it is | Default / Example |
|---|---|---|
| ARTIFACT TYPES | what you regenerate | account brief, weekly report, deal review, pipeline analysis |
| DATA SOURCES | where "did it change" comes from | CRM last-modified, meeting count, usage trend |
| STATIC SECTIONS | reuse, stable 30+ days | company research, buying committee, tech stack |
| DYNAMIC SECTIONS | rebuild every run | activity, current deals, time-bound cards |
| CONDITIONAL SECTIONS | rebuild only when a trigger fires | champion change, fit-score delta, usage-tier shift |
| SKIP_DAYS | age under which unchanged means skip | 7 |
| FULL_DAYS | age over which force a full rebuild | 30 |

## The method

### The four verdicts
Every artifact gets exactly one:
- **SKIP**: age at or under SKIP_DAYS and no underlying data changed. Return the existing artifact, rebuild nothing, cost zero.
- **PARTIAL**: recent, but some sections have stale underlying data. Rebuild only those sections and splice them into the existing artifact. Typical savings 60 to 80 percent.
- **RECYCLE-CORE**: older, but the identity and static sections are unchanged while the dynamic ones are all stale. Reuse the static cards, rebuild the activity-driven ones. Typical savings 30 to 50 percent.
- **FULL**: older than FULL_DAYS, or an identity-level change (acquisition, segment shift, recategorization), or no existing artifact. Run the whole workflow. Cost 100 percent baseline.

### Static vs dynamic sections
Every artifact type splits three ways. STATIC sections are identity-grade and stable for 30+ days (company research, buying committee, tech stack, history). DYNAMIC sections rebuild every run (days-dark, current deal health, time-bound wins, coverage math). CONDITIONAL sections rebuild only when a named trigger fires (a champion job-change, a fit-score delta past threshold, a usage-tier shift). Knowing which section is which is the whole skill; map yours once and the plan writes itself.

### Freshness signals
The verdict reads: artifact age; last-modified on the source record; field-level diffs mapped to the sections each field drives; new activity since the last run; a usage-trend tier shift; a fit-score delta past a threshold. Each signal points at specific sections, not the whole artifact, which is what makes a partial plan possible.

### The savings estimate
Every partial or recycle plan states the estimated token reduction and cost saved versus a full rebuild, so the call is auditable and anyone can see when the gate is being too aggressive.

## Quality gates
- Evidence-first verdicts. Never "the brief is stale." Always "stale because the source changed on {date} and the artifact is from {date}."
- No false-fresh calls. If the evidence is ambiguous (you cannot read the artifact or the source), default to FULL. Better to spend than ship stale.
- Conservative on identity changes. Any identity-level signal (acquisition, segment shift, recategorization) forces FULL regardless of age.
- First run of any new artifact is always FULL. There is nothing to reuse yet.

## Output (example)
```
REFRESH PLAN - account brief for acme.com
Verdict: PARTIAL   (artifact 4 days old)
Reuse:      company research, buying committee, tech stack, history
Rebuild:    days-dark, deal health, top wins
Evidence:   source last-modified 2 days ago; 2 new meetings; usage trend flat
Savings:    ~73% fewer tokens vs a full rebuild
```

## Where the numbers come from
SKIP_DAYS (7), FULL_DAYS (30), and the fit-score delta threshold are defaults from one team's cadence, not laws. A weekly artifact and a quarterly one want different windows. If your work changes slowly, widen the windows; if it moves daily, tighten them. The four-verdict logic does not change. The thresholds are yours.

## Example chat

**You:** Do we need to fully regenerate the acme.com account brief, or can we skip it? Last one ran 4 days ago.

**Claude:** Checked it against the source. Partial rebuild, not full.
```
REFRESH PLAN - account brief for acme.com
Verdict: PARTIAL   (artifact 4 days old)
Reuse:      company research, buying committee, tech stack, history
Rebuild:    days-dark, deal health, top wins
Evidence:   source last-modified 2 days ago; 2 new meetings; usage trend flat
Savings:    ~73% fewer tokens vs a full rebuild
```
The catch worth knowing: I don't call this fresh just because it's recent. I call it PARTIAL because I can point to exactly what changed, 2 new meetings, source modified 2 days ago, and what didn't. If I couldn't see that evidence, the default flips to FULL, because shipping stale work costs more than the tokens.

**You:** What would push this to a full rebuild instead?

**Claude:** Any identity-level signal, an acquisition, a segment shift, a recategorization, forces FULL no matter how fresh the artifact looks. Age alone doesn't do it, the account changing who it is does. Sharpener: connect your CRM's last-modified timestamps directly and I'll prove every verdict against real dates instead of the note you pasted.

## Go further
The manual check proves the gate is worth running. Here is the version that runs itself.

- **Gate every report behind this first.** Wire it in front of your weekly revenue report or account-brief generator so nothing regenerates until this verdict says so.
- **Watch for identity triggers automatically.** Connect Salesforce so an acquisition or segment-shift field change forces FULL the moment it's logged, not at the next scheduled run.
- **Track the savings over a quarter.** Log every verdict and its token estimate to a sheet so you can show finance what the gate is actually worth.

The gate pays for itself the first week it stops a rebuild nobody needed.

## Make it yours
Fork it. Change the artifact types, the static/dynamic split, the windows. The point is not to run someone else's freshness rules. It is to stop paying to rebuild things that did not move. Built by an operator. Customize it, break it, make it better.
