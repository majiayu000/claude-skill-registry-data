---
name: help
description: Explain what slushpile is, what each skill does, what order to run them in, where the workspace files live, and how to set up a voice agent. Use when the user asks how slushpile works, what to run next, or how to fix a workspace problem.
license: MIT
---

# Help

Answer the user's actual question from what follows. Do not print this whole file at them — pick the section that matches what they asked and answer from it in a few lines.

If they asked a general "what is this" or "what do I run", give them the Pipeline section and the single next command for their situation. Check the workspace state before recommending anything: if `preferences.yaml` is absent, the answer is always onboarding, whatever they asked.

## What slushpile is

A job application pipeline. Ten skills and eight agents that take a role from a careers-board listing to a resume and cover letter that have already survived an adversarial review.

The idea it rests on: **you are not graded against the job description, you are graded against the other applications in the same queue.** Every scoring step is anchored to that queue rather than to the posting. This is why the output sometimes says a differentiator the user is proud of is median, and why it reports probabilities per submission channel instead of one verdict.

It never submits anything. Every skill writes files. The user reads them and sends them.

## The pipeline

| Order | Command | What it does |
|---|---|---|
| Once | `/slushpile:onboard` | Builds the workspace: `profile.md`, `preferences.yaml`, `stories.md` |
| Per company | `/slushpile:job-board-search <company\|query>` | Searches, extracts postings, scores pool-anchored fit, runs the contrarian gate, creates role folders. Takes a company name, or a query describing the work and where — a query is resolved into a company list and confirmed before anything is searched |
| As needed | `/slushpile:explore-experience <role folder>` | Interviews to surface experience the user has but never wrote down |
| Per role | `/slushpile:outreach <role folder>` | Finds who they already know at the company, grades the path honestly, drafts the referral ask or the cold note, and writes the contacts into the Referrals table. Run it wherever the warm channel is the highest-EV one and no referrer exists yet |
| Per role | `/slushpile:application-builder <role folder>` | Builds resume and cover letter, iterates against review until stable |
| Per role | `/slushpile:adversarial-review <role folder>` | Seven agents, five in parallel, verdict per channel |
| As needed | `/slushpile:removing-ai-tells <file>` | Strips AI-authorship signals from prose, with gatekeeper review |
| Any time | `/slushpile:redesign-templates` | Restyles the resume and letter templates, holding the ATS constraints fixed |
| Any time | `/slushpile:status` | The queue, what is waiting on them, and whether the pipeline's predictions are holding up |
| Any time | `/slushpile:help` | This |

`application-builder` calls `adversarial-review` itself. Run the review standalone only to check materials that were written elsewhere.

## The workspace

Everything personal lives in the user's own directory. Nothing is hardcoded in the plugin.

```
profile.md          every factual claim the pipeline may make. Nothing goes
                    on a resume that is not in here.
preferences.yaml    constraints: compensation, relocation, work authorization,
                    targeting, and which voice agent to use
stories.md          four to eight tellable stories. Cover letters carry one.
job_search.md       the tracker, including the calibration table
companies.md        one line per company ever looked at
applications/       one folder per role
searches/           one report per careers-board search
```

If a skill says it cannot find `preferences.yaml`, the user is in a different directory than the one they onboarded. Every skill reads the workspace from the current working directory.

## Voice agents

Cover letters are written by a **voice agent** — an agent that writes in one specific person's style, generated from a corpus of their own writing.

slushpile ships `aaddrick-voice` as a working example so the pipeline runs out of the box. **It is the plugin author's voice, not the user's.** Letters written with it will sound like a specific stranger. That is fine for testing the pipeline and wrong for actually applying.

### Making their own

Point them at **https://github.com/aaddrick/written-voice-replication**.

It is a Claude Code pipeline that analyzes a corpus of someone's writing across 25 dimensions — readability, sentence structure, sentiment, personality markers, rhetorical patterns, speech acts — and outputs a voice agent, a voice skill, and a numeric profile with measurable targets. `aaddrick-voice` is that pipeline's own worked example, generated from a Reddit export.

The short version to give the user:

1. Clone that repository and open it in Claude Code.
2. Put their writing samples in the project root. A Reddit or Twitter data export works directly; so does a folder of blog posts, long emails, or forum comments.
3. Tell Claude: `Use the pipeline-orchestrator agent to run the full analysis`.
4. Copy the generated agent into their agents directory, or into a fork of slushpile's `agents/`.
5. Set `voice.agent` in `preferences.yaml` to the new agent's name.

### What makes a usable corpus

Worth saying up front, because the corpus determines everything downstream:

**Good.** Forum and Reddit posts, blog posts, long Slack or Discord messages, emails to colleagues, pull request descriptions, documentation they wrote alone, personal essays.

**Bad.** Anything co-written, anything edited by someone else, anything already run through an LLM, anything in an institutional voice. Marketing copy and performance reviews are the two worst — both are written in a house style rather than the person's.

**Enough of it.** Aim for several thousand words minimum. Below that the analysis converges toward the model's default and produces a generic professional voice, which is exactly what the fatigued reader is trained to bin.

## The eight agents

Seven run the review. One writes.

| Agent | Simulates |
|---|---|
| `slushpile-triage-screener` | 11 seconds, F-pattern, 347 resumes already read today |
| `slushpile-requirements-analyst` | 30 seconds, methodical, every qualification against evidence |
| `slushpile-ats-simulator` | A parser, not a reader. Structure, keywords, years-of-experience math |
| `slushpile-fatigued-reader` | Application #61 of 80. What annoys, what closes the tab |
| `slushpile-pool-analyst` | A recruiter who knows what the queue actually looks like |
| `slushpile-hiring-manager` | The person justifying the interview slot to their skip-level |
| `slushpile-contrarian` | Whoever should have asked if any of this was worth doing |
| `aaddrick-voice` | The example voice agent. Replace it. |

The first five run in parallel and cannot see each other's work. The hiring manager sees all five. The contrarian sees everything and can overrule the hiring manager.

## Reading the output

The three numbers users most often misread:

**Pool position.** A percentile in the realistic applicant pool for that specific role, not a match score. p55 means roughly 45% of that queue looks stronger on paper. It is not a grade on their career.

**Channel verdicts.** Separate probabilities per submission route. The same materials commonly run 1-3% cold and 20-30% through a referral. When those diverge sharply, the finding is *"find a referral"*, not *"the resume needs work"* — and `/slushpile:outreach <role folder>` is the command that acts on it.

**Materials quality vs submission EV.** Two different numbers that routinely disagree. Excellent materials sent to a wrong-fit role still have low expected value. A high materials score with a low EV means stop editing and change the target or the channel.

## Common problems

**Every role comes back killed on compensation.** Open `preferences.yaml`, check `compensation`. With `net_qol` the usual cause is `current_baseline` entered as gross rather than after-tax-after-housing, which makes every offer look worse than it is.

**The review agents report a nearly empty resume.** They read extracted text, not the rendered PDF. Run `pdftotext resume.pdf -`. If that output is empty or scrambled, the resume has a layout problem — multi-column, a text box, contact details in a header — and that is a real finding. An ATS sees what `pdftotext` sees.

**The cover letter reads generic.** They are using the shipped example voice agent, or their corpus was too thin. See Voice agents above.

**Assessments feel too harsh.** They are calibrated against the queue rather than against the posting, which reads as harsh the first few times. The honest check is `/slushpile:status`: it regresses what the pipeline predicted against what actually happened. If it is systematically pessimistic against real outcomes, that report is the evidence, and it writes the corrected priors into `preferences.yaml` where the next search reads them.

**The pipeline said do not apply and the user disagrees.** They should apply. The contrarian is decision support, not an authority, and it is explicitly built to be overruled. Worth recording the override in the role folder's `assessment_history.md` under User corrections, with what happened afterward — that section is the highest-value input to making the priors better, because it is the only place the system records being wrong in a way a human confirmed.

## What to say when they ask "what next"

Check the workspace and answer with one command:

- No `preferences.yaml` → `/slushpile:onboard`
- Workspace exists, no `applications/` → `/slushpile:job-board-search <company>`
- A role whose highest-EV channel is a referral they do not have → `/slushpile:outreach <path>`
- Role folders with no materials → `/slushpile:application-builder <path>`
- Materials built, not submitted → they review and send. The pipeline is done.
- Applications sent, outcomes arriving → record them in the role folders' `application.yaml`, then run `/slushpile:status`. That is what makes the next search better.
- Lost track of where things stand → `/slushpile:status`
