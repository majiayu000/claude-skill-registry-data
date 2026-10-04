---
name: status
description: Read every application.yaml in the workspace and report the state of the search — the ranked queue, what is waiting on you, what has gone quiet, and the regression of the pipeline's own predictions against actual outcomes. Writes the calibration findings back into job_search.md and preferences.yaml.
argument-hint: "[company or path to narrow the report]"
license: MIT
---

# Status

Every other skill in this pipeline writes `application.yaml`. This one reads them all back.

Two questions, answered together on purpose:

**Where does the search stand?** What is in flight, what is waiting on the user, what has gone silent past the point of hope, and which of the assessed-not-applied roles is worth the next slot.

**Is the pipeline any good?** The regression of what the review predicted against what actually happened. A pipeline that grades most applications INTERVIEW and converts five percent is not producing signal, it is producing optimism, and nothing else in the system will ever contradict it.

**Announce at start:** "Reading every application.yaml in the workspace. Reporting queue state and pipeline calibration."

**Arguments:**
- `$1` — optional. A company name or a path, to narrow the report. With nothing, the whole workspace.

**Example:**
```
/slushpile:status
/slushpile:status Acme
```

## Why Calibration Lives Here

The calibration regression was originally its own command, run monthly. It did not get run.

A maintenance ritual with no forcing function competes against whatever the user actually opened the terminal to do, and it loses every time — most reliably when the pipeline is drifting, because a drifting pipeline is one that keeps saying encouraging things. Folding it into the command someone runs to see their queue means the drift arrives whether or not they asked for it.

The cost is that this skill does two jobs. That is the intended trade.

## Prerequisites

- `applications/**/application.yaml` — the corpus. Everything here is read from these.
- `job_search.md` — the tracker, and where the calibration table is written back
- `preferences.yaml` — for `calibration_priors`, which this skill maintains

If no `application.yaml` files exist, say so and stop. There is nothing to report on and a status page assembled from zero records looks the same as one assembled from a healthy search.

## Phase 1: Read the Corpus

Find every `application.yaml` under `applications/`. Read each one.

Record per role, and **name the files that failed to parse rather than skipping them silently.** A malformed YAML that quietly drops out of the denominator inflates every rate in this report, and the inflation is invisible.

From each file: company, role title, level, status, `date_applied`, `channel_used`, `fit.pool_percentile`, `fit.tier`, `highest_ev_channel`, the `channel_ev` probability for that channel, `adversarial_review.hm_verdict_by_channel`, `adversarial_review.contrarian_net`, `submission_expectations.expected_outcome`, and the whole `outcome` block.

**Flag records that are structurally incomplete**, because they are the ones that corrupt the calibration:

- `status: applied` with no `date_applied` — cannot age it, cannot compute days-to-response
- A resolved outcome with `response_received: null` — silently counts as still-in-flight and inflates the denominator forever
- `status: applied` with no `channel_used` — cannot attribute the outcome to a channel, which is the only cut that matters

List these as "records needing attention" with the specific missing field. This is the most useful output in the report for a search more than a month old.

## Phase 2: The Queue

### 2a. In flight

Everything with `status` of `applied`, `screening`, or `interviewing`. Sort by days since `date_applied`, oldest first.

Mark anything past 30 days with no response as **effectively closed**. Say it plainly rather than leaving it in the active table looking alive. A tracker full of month-old submissions with no movement reads as a pipeline in progress and is actually a pipeline that ended, and the difference decides whether the user applies to more things this week.

### 2b. Waiting on the user

`status: materials_ready` — built, reviewed, never sent. Sort by the `channel_ev` probability of the `highest_ev_channel`, highest first.

This table is usually the finding. Materials that survived a seven-agent review and were never submitted are the most expensive artifact in the workspace, and they accumulate quietly because nothing else surfaces them.

### 2c. The ranked queue

Everything at `status: assessed` that has not been passed, ranked by the probability on its highest-EV channel.

**Rank on `channel_ev[highest_ev_channel].p_interview`, not on pool percentile and not on tier.** Pool position is an input to that probability, not a substitute for it, and a role at p70 that only converts through a referral the user does not have is worth less than a p55 role with a live warm channel. Ranking on the percentile puts them in the wrong order, and it does it in exactly the case where the ordering matters.

Do not compute a composite score across channels. A single number per role collapses the channel-conditional model back into the thing it was built to replace: the same materials convert at wildly different rates cold and warm, and one scalar cannot say so. Show the channel and its probability, side by side.

Where the highest-EV channel is `warm_referral` and the Referrals table in `job_search.md` holds no `strong` or `moderate` contact at that company, show the cold number as the actionable one and mark the referral row unavailable. A weak tie in that table is an introduction to chase, not a referrer. The tier was allowed to reflect the best available channel; the queue ranking is about what the user can do this afternoon.

**Then name `/slushpile:outreach` against those roles.** Unavailable is a state somebody can change, and for the roles at the top of this list it is usually the highest-value hour available. A queue that reports the referral row as unavailable and moves on is telling the user their best channel is closed without mentioning that opening it is a command.

### 2d. Cooldowns clearing

Companies whose `reapplication_cooldown_days` window closes within 30 days, from `job_search.md`.

## Phase 3: Calibration

This is the regression. Run it whenever five or more applications have resolved.

A resolved application is one where `outcome.stage_reached` is set to anything other than an empty value, **or** where it was submitted more than 30 days ago with no response — those are auto-rejections that nobody recorded, and excluding them is the single largest source of optimism in a table like this. Count them as `no_response` and say how many were inferred that way.

Below five resolved, print the counts and say the sample is too small to regress. Do not produce a table. A rate computed from two outcomes is noise wearing the costume of calibration, and once it is in a table nobody remembers the denominator.

### 3a. Predicted against actual

| Predicted verdict | Applications | Responses | Interviews | Actual rate | Pipeline's estimate | Delta |

Group by `adversarial_review.hm_verdict_by_channel[channel_used]` — the verdict for the channel actually used, not the best-case one. Grading a cold submission against the warm-referral verdict is how a pipeline convinces itself it was right.

### 3b. By channel

| Channel | Sent | Responses | Interviews | Actual rate | Pipeline's estimate | Delta |

The pipeline's estimate is the mean of the `channel_ev` probabilities it assigned to applications actually sent through that channel.

A channel with no rows has never been used, which is a finding rather than a blank. Say which channels are empty and how many applications went through the one that is not. A warm-referral row that has been empty across thirty applications means the estimate on the channel the pipeline calls best has never once been tested, and the correction for that is `/slushpile:outreach` rather than another cold submission.

### 3c. The outliers

Individual applications where the prediction was sharply wrong in either direction. Both directions matter and only one is comfortable:

- An INTERVIEW verdict that auto-rejected inside 72 hours — the review missed something a filter caught in seconds
- A REJECT or portfolio-only verdict that converted — the review was too harsh, and every role it talked the user out of since then is a cost that never appears anywhere

Name the specific applications. An aggregate delta says the pipeline is off; a named case says how.

### 3d. Where it is wrong, in one sentence

Not "the pipeline is miscalibrated." That is unactionable and no agent can consume it.

Name the direction, the segment, and the size: *"INTERVIEW verdicts on cold submissions to frontier labs converted 0 of 7, against an estimated 12%."*

## Phase 4: Write the Findings Back

A calibration report the user reads and closes changes nothing. The findings have to reach the agents, and the agents cannot be edited — their definitions ship with the plugin and an edit there is reverted by the next update, silently, leaving a pipeline that was tuned and no longer is.

So they go to user-owned data instead.

### 4a. `job_search.md`

Rewrite the Calibration section with the tables from Phase 3, and add dated drift notes. This is the human-readable record.

### 4b. `preferences.yaml`

Update `calibration_priors`. This is the machine-readable one — `/slushpile:job-board-search` reads it at scoring time, and `/slushpile:adversarial-review` passes it to the pool analyst and the contrarian at dispatch.

- `observed_conversion` per channel, and `sample_size`
- `drift_notes` — the Phase 3d sentences. Write the segment and the number into the note. A prior an agent cannot act on is a prior that does nothing.
- `by_company` where a specific company diverges sharply from its type prior

**Only write rates backed by five or more resolved applications on that channel.** Leave the rest null. A null prior means the agents use their shipped defaults and label the estimate uncalibrated, which is the correct behavior. A prior computed from two outcomes moves the scoring further from reality than no prior does, and it arrives labelled as empirical.

**Show the user the diff before writing `preferences.yaml`.** It is their constraints file, this skill is changing how every future assessment scores, and a scoring change nobody was told about is indistinguishable from the pipeline drifting on its own.

## Phase 5: Report

In this order:

1. **One line of headline** — in flight, waiting on the user, assessed and unqueued, resolved
2. **Waiting on you**, if anything is there. It goes above the in-flight table because it is the only section with an action attached.
3. **In flight**, with ages, and the effectively-closed ones marked
4. **The ranked queue**, top ten, with the channel and probability
5. **Calibration**, or the reason there is not enough data for it
6. **Records needing attention** — the incomplete YAML from Phase 1
7. **The single next action**

Keep it to one screen. A status report that requires scrolling to find the action gets skimmed, and the sections that get skipped are the honest ones.

## Anti-Patterns

- **Do not rank the queue on pool percentile.** Rank on the probability of the highest-EV channel. Percentile is an input to that number, and a role that only converts through an unavailable channel sorts far too high on percentile alone.
- **Do not compute a single composite score per role.** One scalar per application is the verdict collapse the channel-conditional model exists to prevent. The same materials are a poor bet cold and a good one warm, and a composite cannot say that.
- **Do not count unresolved applications as successes-in-waiting.** A submission with no response after 30 days is an auto-rejection nobody wrote down. Counting it as in-flight is how the interview rate stays reassuring indefinitely.
- **Do not write a prior from a small sample.** Below five resolved on a channel, leave it null. An uncalibrated estimate labelled as uncalibrated is useful; one presented as empirical is not.
- **Do not edit an agent definition to apply a calibration finding.** They ship with the plugin and are overwritten on update. The finding goes in `preferences.yaml`, which the user owns and which the dispatching skills already read.
- **Do not report only the aggregate delta.** Name the specific applications where the prediction was sharply wrong. The aggregate says the pipeline is off; the named case is the only thing that says how to fix it.
- **Do not soften the direction.** If REJECT verdicts have been converting, the pipeline has been talking the user out of roles they would have gotten, and that costs more than the over-optimistic direction because it leaves no evidence.
