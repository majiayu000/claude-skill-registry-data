---
name: adversarial-review
description: Run a seven-agent adversarial pipeline against a resume and cover letter before submission. Produces channel-conditional verdicts anchored to the realistic applicant pool, separates materials quality from submission expected value, and ends with a contrarian pass that can overturn the verdict.
argument-hint: "<role folder path>"
license: MIT
---

# Adversarial Review

Seven agents try to reject the application before a recruiter gets the chance.

The output is deliberately not a single yes or no. The same materials convert at wildly different rates through a cold portal submission than through a referral, and a review that collapses those into one verdict is telling the user something false in a format that sounds authoritative.

**Announce at start:** "Running adversarial review for $ROLE. Extracting materials, launching five specialists in parallel."

**Arguments:**
- `$1` — path to a role folder containing at minimum a resume and `job_description.md`

**Example:**
```
/slushpile:adversarial-review applications/Acme/Engineering/Staff-SRE
```

## The Pipeline

| # | Agent | Model | When |
|---|---|---|---|
| 1 | `slushpile-triage-screener` | sonnet | parallel |
| 2 | `slushpile-requirements-analyst` | sonnet | parallel |
| 3 | `slushpile-ats-simulator` | sonnet | parallel |
| 4 | `slushpile-fatigued-reader` | sonnet | parallel |
| 5 | `slushpile-pool-analyst` | opus | parallel |
| 6 | `slushpile-hiring-manager` | opus | after 1-5 |
| 7 | `slushpile-contrarian` | opus | after 6 |

Stages 1 through 5 run concurrently. Dispatch them in a single message with five tool calls.

**On a harness without subagent dispatch:** run the seven personas sequentially in one context, reading each agent definition from the plugin's `agents/` directory and adopting it in turn. Write each report out before starting the next, and do not let a later persona see an earlier one's conclusion except where the pipeline says it should — the hiring manager gets all five specialist reports, the contrarian gets everything, and the five specialists get nothing from each other. Contamination between the parallel stages is the main thing that degrades in a sequential run, and it degrades quietly.

## Why It Is Shaped This Way

Four failure modes drove the design. Each maps to a stage.

**Single-perspective sycophancy.** Every reviewer in a naive pipeline works for the candidate. None of them models the queue. The pool analyst exists to force comparative reasoning: not "are these materials good" but "are they better than the other seventy applications this week."

**Verdict collapse.** One INTERVIEW / MAYBE / PASS number hides that the same materials have a 2% conversion cold and a 35% conversion through a referral. Those are different decisions. The hiring manager produces one verdict per channel.

**Synthetic AI-detection concern.** An AI-detector agent flags patterns based on hypothetical reader doubt, and it will override grounded judgment about what a real reader notices. Replaced by the fatigued reader, which asks the answerable question: would this annoy someone on their sixty-first application of the day?

**No falsification step.** Nothing asked "what would have to be true for this to be a waste of cycles?" The contrarian asks it, last, with permission to overturn everything upstream.

Use this as decision support, not as a rubber stamp. It is built to be usable when it says no.

## Prerequisites

Read before dispatching anything:

- The role's `job_description.md`
- The role's `role_analysis.md` if it exists — for level, comp band, and prior company research
- The resume: extract text with `pdftotext <file>.pdf -`. Use the extracted text, not the LaTeX or Markdown source. The agents must see what an ATS and a recruiter see.
- The cover letter, if one exists
- `preferences.yaml` — the contrarian needs the compensation method, the application posture, and any stated constraints, and both it and the pool analyst need the `calibration_priors` block
- `job_search.md` — for prior application history at this company, which the pool analyst and contrarian both need

If the resume is a `.tex` or `.docx` file with no compiled PDF, build it first. Reviewing source is reviewing a document nobody will ever read.

## Step 1: Gather Materials

Extract everything. Determine the role level from `role_analysis.md`, or from the posting, or by inference from the responsibilities — and say which, because a level inferred from prose is less reliable than one stated, and every downstream scope judgment depends on it.

Note any prior applications to this company from `job_search.md`. A prior rejection at a **higher** level is materially important: the recruiter sees the whole ATS history, and a later application at a lower level reads as a multi-level drop. Pass this to the pool analyst and the contrarian explicitly.

## Step 2: Dispatch Five Specialists in Parallel

Each gets only what it needs. Do not hand a specialist another specialist's output at this stage.

**1. Triage screener** — resume text, role title, company, level. Nothing else. It is simulating eleven seconds and must not have read the cover letter.

**2. Requirements analyst** — resume text, cover letter, full JD, level.

**3. ATS simulator** — resume text, full JD. Also pass the source file if it is `.tex` or `.docx`, so it can identify layout structures that plain text hides: tables, columns, header and footer placement.

**4. Fatigued reader:**

```
Review these materials as a fatigued recruiter on application #61 of 80 today.

Role: [title] at [company] (Level: [level])

Resume (as extracted by ATS):
[pdftotext output]

Cover letter:
[text, or "No cover letter provided"]

Identify what gets read carefully, what gets skimmed, what annoys, what feels
try-hard, and what would make a tired reader close the tab. Do not assess
whether this was AI-written — that is a different question and it is not yours.
```

**5. Pool analyst:**

```
Estimate the realistic applicant pool for this role and locate the candidate in it.

Role: [title] at [company] (Level: [level], Posted band: [band])

Job description:
[full JD text]

Role analysis (prior research on competitive dynamics):
[role_analysis.md, or "none"]

Resume (as extracted by ATS):
[pdftotext output]

Cover letter:
[text, or "No cover letter provided"]

Candidate's claimed differentiators, from preferences.yaml
`targeting.claimed_differentiators`:
[list]

Prior application history at this company:
[from job_search.md, or "none"]

Observed conversion from this candidate's own resolved applications, from
preferences.yaml calibration_priors:
[the observed_conversion rates and sample_size, the drift_notes verbatim, and
any by_company entry for this company — or "none recorded yet"]

Characterize the median, 75th, and 90th percentile applicants for this specific
role. Locate the candidate. Say which claimed differentiators are pool-rare and
which are pool-median. Estimate channel-specific conversion. Give the hiring
manager calibration notes so it does not grade in absolute terms.

Where an observed rate is given above with a sample size of five or more, use
it in place of your own company-type prior for that channel and say that you
did. It is the only data here that is about this candidate rather than about
candidates in general. Below five, or with none recorded, use your priors and
say they are uncalibrated.
```

**Pass the priors verbatim, and pass them empty when they are empty.** Summarizing them into "the candidate converts poorly" strips the sample size, which is the only thing that says how much weight the number deserves. Silently omitting the block when it is unset reads to the agent as an ordinary run rather than an uncalibrated one, and an uncalibrated estimate that is not labelled as one is worse than no estimate — it is indistinguishable from a calibrated one downstream.

## Step 3: Dispatch the Hiring Manager

After all five return. Pass all five reports, the full JD, the cover letter text (it needs this for the swap test), the level, and the posted band.

```
You are the final decision-maker. Produce channel-conditional verdicts anchored
to the applicant pool.

[role, JD, cover letter, all five specialist reports, clearly labelled]

Anchor on the pool analyst's findings. Produce a separate verdict and probability
for each plausible channel. Separate materials quality from submission EV. Run
the kill-criteria check. Surface sunk-cost risk if you see it.
```

## Step 4: Dispatch the Contrarian

Automatic, not optional. A pipeline whose falsification step is conditional on the orchestrator feeling uncertain will skip it exactly when it is most needed.

Pass the condensed specialist reports, the full hiring manager synthesis, the full materials, the JD, and `preferences.yaml` — including the `calibration_priors` block, which is what lets it check the hiring manager's probabilities against outcomes the user actually had rather than against its own priors.

The agent definition carries its own binding scope limits. Do not restate them in the prompt and do not add new ones — an orchestrator that improvises extra constraints per run is the reason findings stop being comparable across applications.

`calibration_priors` is data, not a constraint, which is why it goes in the prompt while the scope limits stay in the definition. It changes what the agent knows. It does not change what the agent is allowed to say.

`application_policy.posture` travels with the file on the same footing. How the agent weighs it is in its definition; the value is data. Do not paraphrase the posture into an instruction — "the user is applying aggressively, so lean toward SUBMIT" is the orchestrator improvising a constraint, and it produces a pass whose probabilities move with the user's mood.

## Step 5: Gatekeeper Review

You are the gatekeeper. The agents are deliberately harsh and some of what they produce is wrong. Read all seven outputs and apply judgment.

**Pool analyst.** Are the percentile estimates calibrated for this specific company tier? A frontier AI lab pool and a regional manufacturer pool differ enormously and generic priors flatten them. Did it adjust, or reach for a default?

**Triage screener.** Did it simulate eleven seconds, or did it over-read? A triage report that cites something from the third page did not stay in character. Did its sameness check name what fired, or did it report a suspicion that the document was machine-written? The second one is the concern this review retired, arriving from the one stage that still has a field for it.

**Requirements analyst.** Are the "So What?" failures genuine, or is the context present somewhere the agent did not look? Did it grade in absolute terms when the pool says otherwise?

**ATS simulator.** Did it flag formatting that modern ATS handles fine? Are the "missing" keywords actually missing, or present in phrasing that NLP matching would catch?

**Fatigued reader.** Did it stay on "would this annoy me" and off "is this AI"? Did it flag a deliberate voice marker as a defect? Check its findings against the user's voice agent before acting on any of them — a distinctive habit documented there is not a flaw, and removing it is how a letter drifts back toward generic.

**Hiring manager.** Did it produce per-channel verdicts, or collapse to a binary? Did it anchor on the pool? Are the conversion estimates honest — low single digits for a stretch cold submission — or inflated? Did it run the kill-criteria check at all?

**Contrarian.** Its job is to push. Are the specific findings grounded, or is it being contrarian to look useful? Where it disagrees with the hiring manager, which is better grounded? Default to the contrarian when the HM's reasoning leans on "asymmetry favors applying" or any other argument that is true of every application ever sent.

### Strike out-of-scope kills before they reach the net call

The contrarian is trusted on calibration. It is not trusted on scope.

If its DO_NOT_SUBMIT rests on **offer-stage contract terms** — relocation funding, sign-on, equity, start date, buying out a clawback — strike that leg. Those are negotiated after an offer exists. Killing an application over money that is still negotiable, at the stage where the candidate has the least leverage, is a category error.

If it rests on **a neighbouring requisition that has not been fully assessed**, strike that leg too. Each req stands on its own. Cross-req sequencing is the user's call.

Re-derive the net call from what survives. Record both the struck legs and the surviving ones in `role_analysis.md` under "Contrarian Review" — the struck ones are how this gate gets better, and they are invisible if you only record the outcome.

### Verify a decisive claim before adopting it

When one finding flips the verdict, check it against the workspace before acting: `job_search.md`, `profile.md`, sibling role folders. Adopt it only if it survives. A confident agent assertion that contradicts the user's own records is wrong more often than the records are.

## Step 6: Present and Record

Show the user, in this order:

1. **Pipeline summary** — one line per specialist, the HM's channel verdicts, the contrarian's net call
2. **The five specialist reports**, labelled
3. **HM synthesis** — channel verdicts, materials quality versus submission EV, kill criteria, recommendations
4. **Contrarian challenge** — findings, net call, honest expected outcome
5. **Gatekeeper notes** — false positives you struck, context the agents missed, where the contrarian wins and where it loses
6. **Prioritized action list** — ordered by impact on the highest-EV channel, not by which agent shouted loudest

Then update `application.yaml` in the role folder if one exists:

```yaml
adversarial_review:
  rounds: {n}
  ats_score: {0-100}
  materials_quality: {1-10}
  hm_verdict_by_channel:
    cold_submission: "REJECT (1-3%)"
    warm_referral: "MAYBE (15-25%)"
    cold_outreach: "..."
  swap_tests: {company: PASS, name: FAIL, jd: PASS}
  contrarian_net: "SUBMIT_AS_PORTFOLIO_ONLY"
  contrarian_legs_struck: ["comp gate built on relocation funding"]
highest_ev_channel: "warm_referral"
```

If no `application.yaml` exists, skip it. `/slushpile:application-builder` owns creating that file.

## Step 7: Iterate

If the user changes the materials, re-run the whole pipeline with fresh agent instances. Never reuse a report across rounds — an agent that has already seen its own verdict cannot re-derive it independently.

Compare across runs:

- ATS score delta
- Materials quality delta
- Channel verdict deltas, especially whether cold submission moved off REJECT
- **Issues flagged in multiple rounds are real. Issues flagged once are noise.** This is the most reliable signal the pipeline produces and it only exists if you run more than once.

Three rounds is the ceiling. If the verdict has not moved by round three, the gap is structural and no further editing of the materials will close it. Say that plainly rather than running a fourth.

## Gatekeeper Principles

- **Defend deliberate choices.** A formatting or phrasing decision the user made for a documented reason is not a defect because an agent flagged it.
- **Trust pool calibration over absolute grading.** When a specialist disagrees with the pool analyst, the pool wins absent a specific reason.
- **Trust the contrarian on queue rivalry.** The HM is structurally biased toward decisiveness; the contrarian toward falsification. On expected-value calibration the contrarian is right more often.
- **Amplify consensus.** When several agents flag the same thing, do not soften it.
- **Resume and cover letter are held to different standards.** Resumes are legitimately transferable. Cover letters must be company-specific. Failing the JD swap on a resume is minor; failing the company swap on a cover letter is not.
- **Weight ATS findings correctly.** A parsing failure is critical — it means no human ever sees the document. Keyword optimization matters, and matters less than human readability.
- **Report honest probabilities.** Do not soften "1-3% via cold submission" into "INTERVIEW with caveats." The user is better served by arithmetic than by encouragement, and they will find out either way.
