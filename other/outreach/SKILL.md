---
name: outreach
description: Open the warm channel for a role the pipeline already assessed. Finds who the user already knows at the company, researches named targets from public professional presence when they know nobody, grades each path honestly, drafts the ask through the voice agent, and writes the contacts into the Referrals table in job_search.md.
argument-hint: "<role folder path>"
license: MIT
---

# Outreach

Find the warm path into one company, grade it honestly, and draft the message that uses it.

Everything upstream of here scores warm referral several times above cold submission, records which channel unlocks the tier, and then builds cold-portal materials anyway. Nothing in the pipeline ever went and found a referrer, so the warm row stayed informational forever and the user got measured against the channel the tool happened to support. This skill is what opens the other one.

**Announce at start:** "Finding a warm path into $COMPANY for $ROLE. Public professional sources only. Nothing is sent from here."

**Arguments:**
- `$1` — path to a role folder containing `role_analysis.md` and `application.yaml`

**Example:**
```
/slushpile:outreach applications/Acme/Engineering/Staff-SRE
```

## What a referral is worth

The premium comes from the vouch, not from the button. A person who can describe the user's work from memory changes how the resume is read before anyone opens it. A person who met them once and clicks refer produces a cold submission with a name attached, which converts a little above cold and spends a relationship to do it.

So what this skill produces is a graded path, a drafted ask, and a strength recorded where the next assessment reads it. It does not produce a referral, and recording one before a person has agreed to be it is how the tier gets inflated. Grade the path that exists, never the one the user is hoping for.

## Prerequisites

Read these before deciding anything. The first two are what stop this skill from spending an ask on a role that was already killed.

- The role's `role_analysis.md` and `application.yaml` — the tier, the channel matrix, and which channel the tier came from
- The role's `job_description.md` — the team, the org, and any named hiring contact
- `job_search.md` — the Referrals table, the cooldowns, and this company's history
- `profile.md` — every employer, school, program, project, and venue the user has passed through. This is the raw material for finding a tie, and it is the file nobody thinks to read for one.
- `preferences.yaml` — `identity.links`, `application_policy.posture`, and `voice.agent`
- `companies.md` — whether this company has been approached before, and how it went

If `role_analysis.md` does not exist, stop and run `/slushpile:job-board-search` for this company first. An ask sent for a role nobody scored is an ask spent at random, and the relationship does not come back.

**Check `voice.is_mine` in `preferences.yaml` before drafting.** If it is false, the messages are about to go out in a stranger's voice, to a named person, over the user's own name. Say so once and point at `https://github.com/aaddrick/written-voice-replication`. The stakes are higher here than on a cover letter: a hiring manager reading an off-voice letter thinks the writing is stiff, and a former colleague reading an off-voice email notices it is not the person they know.

## Phase 1: Whether this role deserves an ask

### 1a. Read the numbers out

From `application.yaml`: `fit.tier`, `fit.tier_via_channel`, `highest_ev_channel`, the `p_interview` on `channel_ev.warm_referral` and on `channel_ev.cold_submission`, and `kill_criteria.triggered`.

State all of them in one line before going further. A skill that decides silently is one the user cannot overrule, and this decision spends something they cannot get back this month.

### 1b. Stop conditions

Each of these ends the run. Name which one fired.

1. **The role was passed or hard-killed.** A cleared referral gate does not revive a role killed on compensation, location, or a hard requirement. The gate was never what stopped it.
2. **The company is inside `application_policy.reapplication_cooldown_days`.** Check `job_search.md`. Asking someone to refer the user to a company that rejected them six weeks ago puts the referrer in front of that record, not the user.
3. **A stronger unasked role is open at the same company.** Read the sibling role folders. If a higher-tier role there has no ask recorded, name it and stop. One person can be asked for one thing, and the ask should be the best seat available rather than the folder that happened to be typed.
4. **The warm and cold probabilities are within a few points.** Say the numbers and stop. The ask buys almost nothing here and costs a relationship, and the role analysis already said so — this is the case where reading the matrix beats acting on it.

Under `posture: selective`, also stop where `channel_ev.warm_referral.p_interview` does not clear what the search's own report called a real conversion path for this company. Compare like with like: `by_company` in `calibration_priors` records channel-blind conversion, so putting a channel-conditional estimate against it passes everything and guards nothing. Under `volume`, the cap in Anti-Pattern 7 still holds: a posture that says apply broadly is not permission to message six people at one employer.

### 1c. Report the checks that passed

List every stop condition that was checked and did not fire, with what it was checked against. A check that only reports failures is indistinguishable from one that did not run, and the cooldown check is the one that goes missing.

## Phase 2: Who the user already knows

Run this before researching a single stranger. A remembered former colleague converts at the referral rate. A stranger found through good research converts at roughly the cold-outreach rate, which the matrix in the role analysis already prices at a fraction of it. Spending the research budget first inverts the order of the two.

### 2a. Read the Referrals table

`job_search.md` holds who the user knows where, how strong the relationship is, and whether it has been used. Pull every row for this company.

A table whose fourth column is headed `Used?` predates the strength and status vocabularies. Rewrite the header to `Status` and normalize the values before adding rows, and say you did — a workspace scaffolded before this skill existed still has the old header, and half a table in each vocabulary is worse than either one. Pull the rows for its acquirers, its subsidiaries, and the companies people leave to join it — a contact who moved is still a contact, and the table records where they were rather than where they are.

### 2b. Read `profile.md` for overlap surfaces

Every one of these is a place the user shares history with someone who might work here now:

- Employers, including contract and vendor relationships
- Customers and suppliers, which is the overlap most people forget they have
- Schools, programs, cohorts, and bootcamps
- Open-source projects, working groups, and standards bodies
- Conferences spoken at or organized, and communities moderated

List the overlaps you find with a name for each. "The user spent four years at a company that this team recruits from" is a lead. "The user has a professional network" is not.

### 2c. Ask the user, once

One message, with what you found and what you are missing:

- The overlaps from 2b, so they are answering a specific question rather than searching their own memory unprompted
- Anyone they know at the company, at any level, however loosely
- Anyone who used to work there
- Anyone who knows someone there well enough to make an introduction

**This is the only step in the pipeline that can read what is not in a file.** Nobody writes their weak ties down, the tie that lands is usually one the user forgot they had, and no amount of public research substitutes for the question.

If they name someone, skip Phase 3 entirely and go to Phase 4 with that person. A known contact of any strength outranks the best stranger this skill could find.

## Phase 3: Named targets, when nobody is known

Only reached when Phase 2 came back empty. The channel this produces is `cold_outreach`, and it is priced accordingly in the matrix.

### 3a. Where to look

Public professional presence, and nothing else:

- The company's own site, engineering blog, and team pages
- The posting itself — many name the hiring manager or the recruiter
- Talks, papers, and conference programs from that team
- Public repositories and the accounts that commit to them
- Professional network profiles, read as published

### 3b. Who to aim at, in order

1. **The hiring manager**, when the posting or a team page names them. They own the slot and they are the only person who can convert a message into an interview directly.
2. **Someone doing the job the user would be doing.** They know whether the posting describes the work, and a forward from them reads to a recruiter as a peer's judgment rather than as an application.
3. **The recruiter named on the requisition.** Responsive, and the least able to vouch. Fine as a second message, weak as the only one.

Not an executive several levels above the role. The message either does not get read or gets forwarded down with the sender's name attached to a misjudged escalation.

### 3c. Never invent a person

Every name, title, and team comes from a source you can cite in the report. No inference from a naming convention, no plausible-sounding job title, no guessed team from a product name.

This is the grounding rule from the cover letter with the stakes moved. A hallucinated product name embarrasses the candidate in front of a reader who may not check. A hallucinated person produces a message addressed to someone about a job they do not hold, sent to a real inbox, and the recipient now has direct evidence that the sender does not verify anything before writing to strangers.

If a name cannot be confirmed from a source you can name, it does not go in a draft.

### 3d. Do not construct an address the company has not published

Deriving an address from the company's format is guessing, and it fails in both directions that matter: it bounces, or it reaches the wrong person with that name. Either outcome makes the first contact look automated, which is the exact read the message is trying to avoid.

Use the channel the person publishes for professional contact — the network's own messaging, a contact form, the address on their own site, the mailing list they post to. When there is no published channel, there is no target. Record it and move to the next one.

### 3e. Stop at what a professional profile prints

Current role, history, public work, published writing, and public speaking. Nothing else. Personal accounts, home location, family, and non-work history are off limits regardless of how findable they are.

The boundary is what the recipient will conclude, and they conclude it from the detail you chose to use. A message showing the sender went through someone's private life reads as surveillance, and it converts at zero from a reader who is now uncomfortable.

**Log every source you opened, not only the ones a claim came from.** It goes in `outreach.md` under Sources consulted. A rule about what you may read is otherwise unobservable: a page that only shaped the tone leaves no trace, so a run that ignored this line and a run that followed it produce identical output. The log is what makes the difference visible, to the user and to you on the next run.

### 3f. Two or three targets, not ten

A short list you can say something specific to beats a long one you cannot. Anti-Pattern 7 caps the drafts at two per company regardless, so a list of ten is eight names nobody writes to and two messages that got a tenth of the attention each.

## Phase 4: Grade the path

This is where the skill either feeds the scoring model good data or corrupts it, so it is the part most worth getting right.

| Strength | What it means | What it actually unlocks |
|---|---|---|
| **`strong`** | Worked together directly. Can describe the user's work from memory without being reminded. | A real referral: the internal form with a written recommendation attached. This is the channel the premium is measured on. |
| **`moderate`** | Same employer or same program without direct overlap, or sustained contact since. Knows the user is competent, cannot cite an example. | A referral submission with a thin vouch. Above cold, well below strong. |
| **`weak`** | One conversation, a mutual acquaintance, a conference exchange. | An introduction request, addressed to the person in the middle. Not a referral. |
| **`none`** | Identified from public sources. Never spoken. | Cold outreach. Score it as cold outreach. |

Record the strength you can defend, not the one that helps. The evidence is the specific thing the person could say about the user's work — if you cannot write that sentence, the path is not `strong`.

**A stranger recorded as a referral breaks the tier.** `job-board-search` reads this table, and its rule is that the tier is the highest across *available* channels. Grade a cold contact as warm here and the next assessment unlocks Tier 1 on a channel that does not exist, which is the gaming its Anti-Pattern 11 exists to catch — arriving from the one skill it has no reason to distrust.

**A `none` contact never reaches the Referrals table at all.** Grading them honestly is most of the protection and not all of it. The skills reading that table check the strength column, and a reader who skims to the row count instead gets the wrong answer from a table that is technically correct. Keeping strangers out means the count and the column agree. They belong in `outreach.md`, which is where their draft lives anyway; the tracker holds people the user actually knows.

## Phase 5: Draft

Three different messages for three different situations. Sending the referral ask to a stranger is the single most common way this goes wrong, and it reads exactly as what it is.

### 5a. The referral ask — `strong` or `moderate`

Dispatch the agent named in `voice.agent`:

```
Write a referral ask to [name], who [the relationship, in one line], about
[role title] at [company].

What the recipient has to be able to do after reading this: decide in under a
minute, and already have in front of them the sentence they would put in the
internal referral form.

Required, in order:
1. Say what the role is, in one line, with the link and the requisition ID.
2. Give them the out explicitly, early, and without apology.
3. One or two sentences about what the user did that this person saw
   firsthand. Written so they can paste it.
4. Offer the resume rather than attaching it.

Under 150 words. No preamble about how long it has been.

Context on the shared history:
[the specific overlap, from profile.md or the Referrals table]
```

The out is not politeness. Referral programs pay the referrer and reflect on their judgment, so a person who feels cornered says yes and files a lukewarm one, which is worse than a no and unrecoverable.

### 5b. The introduction request — `weak`

Addressed to the person in the middle, never to the target. Ask them to make an introduction, give them the one-line reason it is worth their name, and let them decide whether to forward it.

Same voice agent, same length ceiling. The one addition: say what the user wants from the target, so the person in the middle is not inventing the pitch on the user's behalf.

### 5c. The cold note — `none`

```
Write a short note to [name], [their title] at [company], about [the specific
thing of theirs the user read, watched, or used].

Rules:
1. Ask a question the user actually wants answered, about the work. Do not ask
   for a referral. Nobody vouches for a person they met one sentence ago, and
   the ask is what makes the message deletable in one motion.
2. Say why this person specifically. Name the talk, the post, the commit, or
   the paper. A note that would work addressed to anyone gets treated as
   something that was.
3. Under 120 words.
4. Say in one clause that the user is looking at a role there. One clause,
   early, not a pitch. A person who answers a friendly question and later
   works out it was step one of a referral path has a fair complaint, and it
   lands on the user rather than on this pipeline.
5. No flattery opener and no credentials paragraph.

Context on the user, only what is relevant to the question:
[the relevant lines from profile.md]
```

The conversion path here is that the recipient answers, the user replies well, and a referral becomes possible three messages later. Writing it as a referral ask collapses that path on contact.

### 5d. Ground every claim about the recipient

Same discipline as the cover letter's company grounding, applied to a person. Their title, their team, the talk being cited, the repository, the post. Verify each against the source you found it in, and cut anything that cannot be verified.

A message that gets a former team wrong is worse than a generic one. The recipient reads it as research that was done badly, which is a stronger signal than no research at all.

### 5e. Strip the tells

Run `/slushpile:removing-ai-tells` on each draft.

**Do not skip this because the messages are short.** A 120-word note has no room for the specific detail that makes longer prose read as written by a person, so the generic constructions have nothing to hide behind and sit at the highest density anywhere in the pipeline. This is the same argument the builder makes about screening answers, and it is stronger here, because the reader is one person who was not expecting mail.

### 5f. Where the drafts go

Write `outreach.md` in the role folder:

```markdown
# Outreach — {Company}, {Role}

**Date:** {YYYY-MM-DD}
**Tier:** {tier} via {channel} · **Warm p(interview):** {n}% · **Cold:** {n}%

## Paths found

| Contact | How found | Strength | Basis for the vouch | Channel to use |

## Drafts

### {Contact} — {referral ask | introduction request | cold note}
{the message, ready to send}

**Sources for every claim about them:** {links}

## Not pursued
{What the shortlist was cut from, without names. "Four engineers on the team
page, none with public work to cite" carries the whole finding. A shortlist
with no record of what it was cut from reads as the entire field.}

## Sources consulted
{Every page opened during Phase 3, including the ones nothing was used from.}

## Sent
| Contact | Date sent | Reply | Outcome |
```

The Sent table starts empty and the user fills it. Nothing in this pipeline can observe an email being sent, so a field this skill writes optimistically is a field that is wrong from the moment it is written.

## Phase 6: Write it back

A draft nobody records is an ask the next run makes again.

### 6a. `job_search.md`

Add one row per **`strong`, `moderate`, or `weak`** contact: company, contact, the strength from Phase 4, the status, and a note carrying the basis for the vouch. A `none` contact stays in `outreach.md`, per Phase 4.

The template documents both vocabularies — `strong`, `moderate`, `weak`, `none` for strength, and `not asked`, `asked YYYY-MM-DD`, `agreed`, `declined`, `used YYYY-MM-DD` for status. Use them literally. A status written in free text is one the next run has to interpret, and it will interpret an unanswered ask as a live one.

This is the write that matters most, and not because of this role. `job-board-search` reads this table when it builds the channel matrix, and `status` reads it when it decides whether to rank a role on its warm number or its cold one. Until a `strong` or `moderate` row exists here, both of them price the warm channel as unavailable for every role at this company, correctly, forever.

### 6b. `application.yaml`

Two writes, and nothing else in the file.

- Add a dated `log` entry naming the contact, the graded strength, and the channel drafted. `log` is the only free-form field here and it is the whole record this skill needs. The `fit` and `channel_ev` blocks are the search's, the `adversarial_review` block is the review's, and a skill that edits a block it does not own leaves the template's own provenance comments lying.
- **Set `channel_used` only when the application actually goes through that channel.** Not on a draft, not on a sent message, not on a yes. `status` groups every calibration rate by this field, and a `warm_referral` recorded for a submission that went through the portal puts a cold outcome in the warm row — which corrupts the one table in the system built to catch exactly that kind of optimism.

### 6c. Do not touch the tier

The tier belongs to `job-board-search`, and this skill leaves it exactly as it found it, including after a referrer agrees.

The temptation is real and worth naming, because it looks safe. The tier is defined as the highest across available channels, a referrer clears the warm channel's gate, so raising the tier reads like flipping a flag rather than re-scoring anything. It is not. `role_analysis.md` records one probability and one verdict per channel and **no tier per channel**, and `job-board-search` derives the tier from the pool percentile, which a referrer does not change. There is no withheld number to take. A tier written here would be a fresh estimate produced by the skill that never looked at the pool, landing in the file the builder and every review agent read as current fact.

What to do instead: record the agreement in the Referrals table, say in the report that the warm channel is now open and that the role's tier was set without it, and let the next assessment of that role use it. Say the same thing about `application.yaml` — `fit` is written by the search, and nothing here edits it.

### 6d. `companies.md`

Note the approach in the company's row: who was contacted, when, and through what. Six months from now this is what answers "have I already asked someone here?" before the user asks the same person twice.

## Phase 7: Report

1. **The paths found**, with strength and the basis for each
2. **What was drafted**, where it is, and which channel each message goes out on
3. **What the user has to do** — every message is theirs to send, from their own account, after they read it
4. **What changes if someone says yes** — which channel opens, and that the role's tier was set without it. Name re-running `/slushpile:job-board-search` for that company as what makes the tier catch up, and say it is optional.
5. **Whether materials already exist for this role.** If `files.resume` in `application.yaml` is filled and a warm path just opened, say so and name `/slushpile:application-builder`. A cold submission and a referral want different documents, and materials built before the channel moved are aimed at the channel that lost.
6. **The single next action**

If `identity.links` in `preferences.yaml` is empty, say so here. A cold note asks a stranger to form an opinion, and a recipient with nothing to open forms it from the message alone. Filling that block, or shipping something public, is worth more than another draft.

**This skill never sends anything.** It writes files. The user reads them, edits them, and sends them from their own account, which is also the only way the reply arrives somewhere they will see it.

## Anti-Patterns

1. **Do not invent a person, a title, or a team.** Every claim about a recipient traces to a source named in `outreach.md`. A message to someone about a job they do not hold is unrecoverable with that person.
2. **Do not record a stranger as a referral, and do not put a `none` contact in the Referrals table at all.** Downstream reads the strength column, and a table where the row count and the column disagree gets read wrong by whichever consumer skims.
3. **Do not ask a stranger for a referral in the first message.** Ask a question about the work, and say in one clause that the user is looking at a role there. The referral becomes possible after they reply, and never before.
4. **Do not construct an email address the company has not published.** Use a channel the person publishes, or record that there is no target.
5. **Do not research past what a professional profile prints.** The recipient judges the message by which detail you chose to use.
6. **Do not spend an ask on a lower-tier role** while a higher-tier one at the same company sits unasked.
7. **Do not draft more than two messages per company in one run**, and tell the user in the handoff to space them by a few days. They talk to each other, and a simultaneous pair reads as a blast rather than as interest in the team. The draft cap is this skill's to enforce; the spacing is the user's, because nothing here can observe a send.
8. **Do not write a tier, a pool percentile, or a channel probability anywhere.** They are `job-board-search`'s, they are derived from the pool, and a referrer does not change the pool. See 6c.
9. **Do not skip the tells pass because the message is short.** Short messages carry the highest tell density in the pipeline.
10. **Do not set `channel_used` before the submission actually goes through that channel.** It is the field every calibration rate is grouped by.
11. **Do not send anything.** No skill here touches an inbox, a portal, or a form.
