---
name: project-retrospective
description: "Generate a LESSONS.md from a finished project: what worked, what didn't, what to reuse, what to retire — formatted for next-project carry-over."
status: stable
category: editing
subcategory: editing
version: 1.0
eval_score: 4.5
tags: [workflow, retrospective, lessons-learned, project-management, editorial-process]
---
# Project Retrospective

## What This Skill Does
Takes raw notes about a finished media project and generates a structured LESSONS.md that captures reusable editorial decisions, workflow fixes, timeline findings, and specific carry-over items for the next project.

## When To Use This Skill
- After a series, season, or multi-episode project wraps and you want to capture what the team learned before everyone moves on to the next thing
- When a project ran over budget, over schedule, or below quality expectations and you need a written record of why, without blame, before the post-mortem meeting
- Before starting a new project that resembles one you finished recently — run the retrospective on the old project first, then use the LESSONS.md as a planning input
- When a freelancer or contributor is leaving the team and their working knowledge needs to be captured before they go
- At the end of a pilot or proof-of-concept phase, to decide whether the format is worth continuing and what must change if it does

## What You Need To Provide
**Required:**
- Project name and format (podcast series, documentary, article series, YouTube channel launch, newsletter run, etc.)
- What the original brief or goal was — in one or two sentences
- What was actually delivered — scope, episode count, word count, whatever the countable output was
- What went well — even rough bullet points are fine
- What went badly or took too long — same level of detail

**Optional:**
- Timeline: planned vs. actual dates for key milestones (commission, first draft, rough cut, delivery)
- Team structure: who did what, and whether roles shifted during the project
- Budget notes: where you overspent, where you underspent, what you wish you had costed differently
- Stakeholder or client feedback: quotes, notes from review rounds, approval friction
- Technical or tooling notes: software, equipment, workflows that helped or caused problems
- Audience reception: ratings, downloads, reader feedback, social response — anything that tells you whether the output landed
- Anything that surprised you, positively or negatively

## How the Assistant Approaches This
1. Reads all the notes you provide and identifies the project's actual arc — what was planned, what happened, and where the two diverged. This is the factual spine of the retrospective.
2. Sorts every finding into one of six categories: editorial decisions, workflow and process, timeline and scheduling, stakeholder management, quality and standards, tooling and infrastructure. Findings that span categories go under the primary one, with a cross-reference note where needed.
3. For each finding, separates the observation (what happened) from the lesson (what to do differently). The observation is evidence; the lesson is the actionable recommendation. Both get written down, because a lesson without its evidence is just an opinion someone will discard six months from now.
4. Identifies carry-over items — specific, concrete things the next project should adopt, avoid, or investigate further. These are formatted as a checklist so they can be pasted directly into a planning document or project brief.
5. Flags any patterns that appear across multiple categories. If the same root cause — unclear briefs, missing sign-off gates, a tool that kept failing — shows up in three different problems, it gets called out as a systemic issue with its own section. These are often the most valuable findings in the entire document.
6. Writes the LESSONS.md in a tone that is direct, specific, and blame-free. Names roles, not people. States facts, not judgments. The document should be useful to someone who was not on the project and has never met the team.
7. Checks the draft against the quality criteria below before delivering. Every lesson must be specific enough that a producer reading it six months from now can act on it without asking anyone what it means.

If the input notes have clear gaps — timeline information is missing, no audience data was provided, the team structure is unknown — the skill will note these gaps in the relevant sections rather than speculating. A retrospective that acknowledges what it does not know is more trustworthy than one that fills every section with confident claims.

## Output Format
The skill produces a single Markdown document called LESSONS.md with this structure:

```
# LESSONS.md — [Project Name]

**Project:** [Name]
**Format:** [Podcast series / Documentary / Article series / etc.]
**Dates:** [Start] — [End]
**Scope:** [What was delivered — episode count, word count, etc.]

## Summary
[3–5 sentences: what the project set out to do, what it delivered, and the
single most important lesson. This paragraph should be useful on its own
as a quick reference.]

## Editorial Decisions
[Findings about content choices: format, tone, structure, guest selection,
story angle, editorial line. What worked and what to change.]

## Workflow and Process
[Findings about how work moved through the team: briefing, drafting,
review rounds, approvals, file management, handoffs.]

## Timeline and Scheduling
[Planned vs. actual. Where time was lost, where buffers helped, where
deadlines created pressure that affected quality.]

## Stakeholder Management
[Client or commissioner interactions: feedback loops, sign-off friction,
scope changes, expectation mismatches.]

## Quality and Standards
[Findings about the finished output: consistency, accuracy, production
values, audience reception. Where standards held and where they slipped.]

## Tooling and Infrastructure
[Software, hardware, platforms, templates, workflows. What helped, what
failed, what to replace.]

## Systemic Issues
[Patterns that appear across multiple categories. Root causes, not
symptoms.]

## Carry-Over Checklist
- [ ] [Specific action item for the next project]
- [ ] [Another specific action item]
...

## Raw Notes
[Optional: the unprocessed input notes, preserved for reference.]
```

**Length:** Typically 800–1,500 words for a mid-sized project (6–12 episodes or equivalent). Shorter for a single article; longer for a multi-season production. The document should be complete but not padded — every paragraph earns its space.

**Tone:** Direct, collegial, blame-free. Written so that someone joining the team for the next project can read it cold and understand both what happened and what to do about it. No corporate euphemisms ("challenges" when you mean "failures"), but no finger-pointing either. The register should sound like a senior producer's internal memo — someone who respects the reader's time and trusts them to act on clear information.

**Formatting:** Standard Markdown. No custom syntax, no frontmatter, no metadata beyond the header block. The document should render cleanly in any Markdown viewer and be readable as plain text.

**Carry-Over Checklist guidelines:** Each checklist item should be phrased as an action ("Create a field recording protocol") rather than a state ("Field recording protocol exists"). Items should include enough context that someone who did not read the full document can understand what the item means and why it is there. Avoid one-word items ("Transcription") — the next producer who reads the checklist needs to know what about transcription needs to change.

**Raw Notes section:** This section is optional but recommended. It preserves the original unprocessed input for reference, so anyone reviewing the LESSONS.md can check whether a finding accurately reflects what was reported. When a project team revisits the document months later, the raw notes often trigger additional memories that the structured findings did not capture.

## Retrospective Framework

The six categories are not arbitrary. Each covers a distinct domain of project decisions, and together they account for where media projects typically succeed or fail. The categories are ordered from most editorial (closest to the content) to most operational (furthest from the content). This ordering helps readers find what they need: producers and editors tend to start from the top; operations and project managers from the bottom.

Not every project will have findings in all six categories. A solo newsletter may have nothing under Stakeholder Management. A commissioned documentary may have little under Tooling. Empty categories are omitted from the output — the skill does not generate placeholder text for sections with no findings.

**Timing matters.** The best time to run a retrospective is within two weeks of project delivery, while the details are still fresh but the emotional heat of any production crunch has cooled. Run it too early (during the final delivery week) and the team cannot distinguish between systemic problems and temporary stress. Run it too late (three months after delivery) and the specific details — the 45-minute pre-interviews, the three different recording devices — will have faded into vague memories of "things that were a bit messy." If you missed the two-week window, run it anyway with whatever notes you have. A late retrospective is always better than none.

### Editorial Decisions
What the project chose to say and how it chose to say it. This is the category closest to the content itself.

**What belongs here:**
- Format selection — why a series instead of a single long-form piece, why interviews instead of narration, why video instead of audio
- Tone and register decisions — formal vs. conversational, expert-facing vs. general audience, and whether the chosen register held across all instalments
- Guest or source selection criteria — who was included, who was passed over, and whether the selection produced the range of perspectives the project needed
- Story structure choices — chronological vs. thematic, single-thread vs. multi-strand, and whether the chosen structure served the material
- What was cut and why — topics, segments, or episodes that were dropped during production, and whether cutting them improved or weakened the final output
- What was added late — late additions often signal either good editorial instincts (responding to what the material revealed) or poor planning (compensating for gaps that should have been caught earlier)

**The question this section answers:** *If we made this project again with the same brief, what editorial choices would we keep and which would we reverse?*

### Workflow and Process
How work moved from assignment to delivery. This category covers the mechanics of production — not what was made, but how it was made.

**What belongs here:**
- Briefing quality — did the initial brief contain enough detail for the team to work from without constant clarification? Did the brief match what the client or commissioner actually wanted?
- Draft-to-final pipeline — how many review rounds, how long each took, where drafts stalled, whether feedback was specific enough to act on in one pass
- Review and approval bottlenecks — who needed to sign off, how long sign-offs took, whether anyone was signing off on things outside their area
- File management — naming conventions (or lack of them), version control, where files lived, whether anyone lost work or worked from the wrong version
- Handoff points — where work passed from one person or role to another, and whether those handoffs were clean (everything the next person needed was provided) or messy (information was lost, context was missing)
- Communication patterns — how the team communicated (email, chat, calls, in-person), how often, and whether the communication cadence matched the pace of production

**The question:** *Where did the process cause delays, errors, or rework that better structure would have prevented?*

### Timeline and Scheduling
The relationship between the plan and what happened. This category is about time — where it was spent, where it was wasted, and where it ran out.

**What belongs here:**
- Milestone accuracy — were estimates right? If not, which phases were underestimated and by how much?
- Buffer allocation — was there enough slack in the schedule to absorb surprises? Was the buffer in the right places (early or late in the schedule)?
- Crunch periods and their causes — any stretch where the team worked longer hours or cut corners to meet a deadline, and what forced the crunch
- Dependencies and bottlenecks — tasks that could not start until another task finished, especially where the dependency was not identified in advance
- External deadlines — broadcast dates, publication schedules, event dates, or client deadlines that were fixed and drove the rest of the schedule
- Parallel workstreams — were team members able to work in parallel, or did the project design force sequential work that stretched the timeline?

**The question:** *How should we schedule the next project of this size and complexity?*

### Stakeholder Management
How the project interacted with everyone outside the core production team. "Stakeholder" here means anyone who had input or authority over the project without doing the daily production work — clients, commissioners, funders, institutional partners, legal departments, distribution platforms.

**What belongs here:**
- Expectations vs. delivery — did the client or commissioner get what they expected? Where expectations and delivery diverged, was the divergence communicated in advance?
- Feedback round structure — how many rounds of feedback, how specific the feedback was, how long each round took, whether feedback contradicted earlier approvals
- Scope changes — anything added, removed, or modified after the initial agreement, and whether the impact on schedule and budget was acknowledged at the time
- Approval authority — was it clear throughout the project who could approve what? Single approver vs. committee approval; whether approvers were available when needed
- Communication frequency and format — how often the team reported to stakeholders, in what format, and whether stakeholders felt informed or blindsided
- Relationship dynamics — whether the working relationship was collaborative, arms-length, or adversarial, and what set the tone early in the project

**The question:** *What would we set up differently in the first meeting with the client or commissioner?*

### Quality and Standards
Whether the output met the bar the team set for itself. This is about the finished product, not the process that created it.

**What belongs here:**
- Consistency across instalments — did all episodes, articles, or segments meet the same quality standard, or did quality vary? If it varied, what caused the dips?
- Factual accuracy — was there a verification process? Did any errors make it into the published output? If so, how were they caught and corrected?
- Production values — audio quality, image quality, copy editing standard, design quality. Were production values where they needed to be, or did budget or time pressure cause visible compromises?
- Audience response — downloads, views, ratings, reader feedback, social media response, complaints, praise. What the audience actually said, as distinct from what the team hoped they would say
- Internal assessment — where the team itself felt the output was strong or weak, separate from audience response. Sometimes the audience likes something the team considers below standard, or vice versa
- Comparison to ambition — how the finished project compares to what the team set out to make. The gap between ambition and delivery is often the most honest measure of a project

**The question:** *Where did the finished work fall short of what we intended, and was the gap caused by time, budget, skill, or a decision we made?*

### Tooling and Infrastructure
The tools, templates, and technical systems the team used. This category is the furthest from the content itself, but tooling problems have a way of rippling upward into editorial quality.

**What belongs here:**
- Recording and editing software — what was used, whether it performed as expected, any compatibility issues between team members using different tools or versions
- Project management tools — task tracking, scheduling, resource allocation. Whether the team used them consistently or abandoned them mid-project
- Communication channels — email, Slack, WhatsApp, phone, shared documents. Whether the number of channels helped (different tools for different purposes) or hurt (information scattered across too many places)
- File storage and sharing — cloud services, local drives, shared folders. Whether there was a single source of truth for project files
- Templates and checklists — pre-built formats for briefs, scripts, shot lists, show notes. Whether they existed, whether they were used, whether they helped
- Automation and AI assistance — any automated workflows, AI transcription, AI-assisted writing or editing. What worked, what produced unreliable output, what required more human oversight than expected

**The question:** *Which tools saved time, which wasted it, and what should we try or drop next time?*

## How To Write Findings

Each finding in the LESSONS.md follows a consistent pattern. This pattern matters because it makes the document scannable and prevents findings from becoming vague advice.

**Pattern: Bold claim. Evidence. Fix.**

1. **Bold opening sentence** — states the finding as a direct claim. This is the lesson in one sentence. It should be bold-formatted so a reader scanning the document can read only the bold lines and understand the key findings.
2. **Evidence** — one to three sentences explaining what happened that supports the claim. Specific numbers, dates, and examples. No generalities.
3. **Fix** — one to two sentences stating what to do differently next time. Begins with "Fix:" for easy scanning. The fix must be specific enough to execute without further discussion.

**Example of the pattern applied:**

> **Pre-interviews ran too long and duplicated editorial work.** Average guest pre-interview lasted 45 minutes; fewer than 10 minutes of usable material came from each. The editorial calls made during pre-interviews (which angles to pursue, which anecdotes to draw out) had to be remade in the recording session because the host had not been present for the pre-interviews. Fix: cap pre-interviews at 20 minutes. Send guests a topic list 48 hours ahead. Have the host present for all pre-interviews, even by phone.

**What to avoid:**
- Findings without evidence: "Communication could have been better." Better how? Between whom? About what?
- Evidence without a fix: "The timeline slipped by four weeks." What should the next project do about it?
- Fixes without evidence: "Use a project management tool." Why? What problem did the absence of one cause on this project?
- Blame disguised as analysis: "The editor was slow with feedback." Instead: "Feedback rounds averaged 8 days against a planned 3 days. Fix: agree on a 72-hour feedback window at project start, with an escalation path if the deadline passes."
- Generic praise: "The team worked really well together." Instead: name the specific practice that worked — "Daily 10-minute stand-ups kept everyone aligned on what was due that day and caught two scheduling conflicts before they became problems."

**Positive findings matter as much as negative ones.** A retrospective that only lists failures is not useful — it tells the next team what to avoid but not what to repeat. When something worked, write it up with the same rigour: bold claim, evidence, and a carry-over note that says "keep doing this" with enough specificity that the next team knows what "this" means. The goal is not to balance criticism with praise for diplomacy's sake; it is to capture working practices that might otherwise be forgotten or accidentally changed.

## Adapting to Project Type

The six-category framework applies to any media project, but the weight and detail of each category shifts depending on what was made. The skill adjusts automatically based on the project format you describe in the input, but understanding the typical weight distribution helps you provide better notes.

**Podcast series:** Editorial Decisions and Workflow tend to dominate. Guest selection, episode structure, and the recording-to-edit pipeline carry most of the lessons. Tooling findings are usually about recording equipment, editing software, and transcription. If the podcast involves field recording or location work, Tooling gains significant weight because equipment and environment issues compound across episodes.

**Documentary or factual TV:** Timeline and Stakeholder Management gain weight. Broadcast deadlines are fixed, commissioner feedback rounds are formal, and post-production is where most schedule pressure lands. Editorial findings often centre on what survived the edit and what was cut — the gap between what was filmed and what made it to screen is where the most useful editorial lessons sit. Budget notes are especially valuable for this format because documentary budgets are tight and overspends in one area always come at the cost of another.

**Article series or long-form journalism:** Editorial Decisions and Quality are the heaviest categories. Story structure, source selection, and factual accuracy carry the most lessons. Workflow findings tend to focus on the draft-review-publish pipeline: how many revision rounds each piece needed, whether feedback was specific enough to act on in one pass, and where pieces stalled between draft and publication. The researcher and editor roles matter more here than in audio or video formats.

**YouTube series:** Tooling and Quality carry more weight than in other formats because production values (thumbnails, editing pace, audio quality, colour grading) directly affect audience retention in a way that is immediately measurable. Audience reception data is usually richer for YouTube than for any other format — watch time, click-through rate, retention curves, subscriber conversion — and deserves more detailed analysis in the Quality section. Editorial findings often focus on hook structure, pacing, and the relationship between title/thumbnail promise and content delivery.

**Newsletter or email series:** Workflow and Stakeholder Management are often thin (small teams, few external stakeholders). Editorial Decisions and Quality dominate — what subjects drove opens, what formats drove clicks, where the editorial voice drifted over the run. Audience data is granular (open rates, click rates, unsubscribe rates by edition) and should be referenced specifically in the Quality section rather than summarised as averages.

**Multi-format projects** (e.g., a podcast with a companion article series and social media campaign): use the full six categories but add a short "Cross-Format Coordination" note under Systemic Issues covering how the formats connected or failed to connect — whether the release schedule was aligned, whether assets were shared between formats, and whether the audience moved between formats as intended or stayed siloed.

**Solo projects:** When one person did everything — researched, recorded, edited, published — the Workflow and Stakeholder sections may be very short or empty. That is fine. The skill will not pad these sections with filler. Focus the notes on Editorial Decisions, Quality, Timeline, and Tooling, which are where solo producers tend to find the most reusable lessons. Solo retrospectives are often shorter (400–800 words) but no less valuable — a solo producer has no team to absorb institutional memory, so the written record is the only record.

## Quality Criteria

The following criteria apply to the generated LESSONS.md. Each must be met before the document is delivered. If a criterion cannot be met because the input notes do not contain enough information, the document should acknowledge the gap rather than fill it with speculation.

- [ ] Every lesson in the document is specific enough to act on without further explanation — no "improve communication" without specifying what communication, between whom, and what improvement looks like
- [ ] Observations and lessons are clearly separated — the reader can distinguish what happened (fact) from what to do about it (recommendation)
- [ ] The carry-over checklist contains only items that belong in a planning document — no vague aspirations, only concrete actions with enough context to execute
- [ ] The document names roles and functions, not individuals — "the sound engineer" not "Alex"
- [ ] The tone is blame-free throughout — states what happened and what to change, never who was at fault
- [ ] Systemic issues are identified where they exist, connecting problems that appear in multiple categories to shared root causes
- [ ] The summary paragraph works as a standalone reference — a reader who only reads those five sentences understands the project's outcome and its most important lesson
- [ ] The document does not invent findings beyond what the input notes support — gaps in the input are acknowledged, not filled with assumptions

## Example

### Input

**Project:** "Street Level" — a 6-part podcast series about urban architecture and public space design.

**Format:** Interview-based podcast, 35–45 minutes per episode, with field recordings from each location.

**Brief:** Commission from an architecture foundation to produce a podcast series that makes urban design accessible to a general audience. Six episodes, each focused on a different city neighbourhood. Goal was to reach listeners outside the architecture community — people who live in these spaces but never think about why they are designed the way they are.

**Delivered:** Six episodes, released weekly over six weeks. Average runtime 42 minutes. Plus a bonus episode (live panel discussion at the foundation's annual event, 58 minutes).

**What went well:**
- The field recordings were the standout element. Listeners mentioned them repeatedly in reviews. Recording on location instead of describing locations in a studio was the right call.
- Guest selection worked. We avoided the usual architecture critics and found people who use the spaces daily — a market stallholder, a skateboarder, a night-shift bus driver. They were more compelling than the experts.
- The foundation gave us full editorial independence. No sign-off friction, no content vetoes.
- Episode 4 (the one about the failed shopping mall redevelopment) was the most downloaded. It had a clear conflict and a narrative arc. The others were more observational.

**What went badly or took too long:**
- Guest pre-interviews ran way too long — 45 minutes on average. Most of that was unusable. We ended up doing the real editorial work twice: once in the pre-interview, once in the edit.
- The field recording workflow was a mess. We recorded on three different devices across six locations. Levels were inconsistent, format was inconsistent. Cleaning it up in post took roughly double what we budgeted.
- Episode 3 about the waterfront park was weak. The interviewees liked the space too much — there was no tension, no disagreement, no narrative. We knew it during production but didn't have time to pivot.
- We underestimated transcription time. Each episode took 3–4 hours to transcribe and clean up. We had budgeted one hour per episode based on a tool demo that turned out to be unrealistic at our audio quality.
- The bonus live episode was a last-minute addition. The foundation asked two weeks before their event. We said yes because the relationship mattered, but it ate a full production week and the episode was our weakest.

**Timeline:**
- Planned: 12 weeks from commission to first episode release.
- Actual: 16 weeks. The delay was mostly in post-production (field recording cleanup and transcription backlog).

**Team:** Producer (full-time), sound engineer (freelance, 2 days/week), researcher (freelance, first 6 weeks only), host/presenter.

**Budget notes:** Overspent on post-production by about 35%. Underspent on research because the researcher finished early. Would have been better to keep the researcher through production for fact-checking.

**Audience reception:** 4,200 average downloads per episode (foundation target was 2,000). Strong listener reviews, particularly praising the field recordings and the non-expert guests. Episode 4 peaked at 7,100 downloads. Episode 3 was lowest at 2,800.

**Surprises:**
- The host's chemistry with non-expert guests was noticeably better than with the two architecture professionals we included. We had expected the opposite.
- Listeners wanted longer episodes, not shorter. We had aimed for 35 minutes and kept running over.
- The foundation's social media team was surprisingly effective at promoting the episodes. They drove more traffic than our own channels.

### Output

```markdown
# LESSONS.md — Street Level

**Project:** Street Level
**Format:** Interview-based podcast series (6 episodes + 1 bonus live episode)
**Dates:** January — April (16 weeks; planned 12)
**Scope:** 7 episodes released, 42 minutes average runtime, 4,200 average downloads/episode

## Summary
Street Level set out to make urban architecture accessible to a general audience through a six-part interview podcast with field recordings. It exceeded its download target by more than double and received strong listener response, particularly for the field recordings and the non-expert guest approach. The four-week schedule overrun was caused almost entirely by post-production problems — inconsistent field recording standards and underestimated transcription time — both of which are fixable with pre-production protocols. The single most important lesson: the non-expert guest format was the project's strongest editorial asset, and the one episode that underperformed (Episode 3) was the one where we could not find a dissenting voice. Tension drives narrative in this format; agreement does not.

## Editorial Decisions

**Non-expert guests outperformed professionals.** The market stallholder, skateboarder, and night-shift bus driver were more engaging on tape than the two architecture professionals. The host's interview rhythm was looser and more curious with non-experts, which produced better material. For future series: lead with non-expert voices. Use professionals only for specific factual context, and keep their segments short.

**Field recordings defined the show.** Listeners cited them as the primary reason they kept listening. Recording on location was more expensive and logistically harder than studio recording, but it gave the series an identity that a studio-based architecture podcast would not have had. This is a format signature worth keeping — and worth budgeting for properly, which this project did not do (see Tooling).

**Episode 4 succeeded because it had conflict.** A failed shopping mall redevelopment gave the episode a narrative arc — ambition, failure, consequences, competing interpretations. The other episodes were observational, which worked but did not produce the same listener engagement. Future series should screen locations partly on narrative potential: is there a disagreement, a failure, a decision with visible consequences?

**Episode 3 failed because it had no tension.** Every interviewee liked the waterfront park. There was nothing to push against. The production team identified this during recording but lacked time to pivot — either by finding a dissenting voice or by restructuring the episode around a different question. Fix: schedule a mid-production editorial checkpoint (see Timeline) and include a "tension test" for each episode: can you state, in one sentence, what the disagreement or unresolved question is? If you cannot, the episode does not have enough narrative material yet.

**Longer episodes were fine.** The 35-minute target was based on industry averages, not audience testing. Actual episodes ran 42 minutes on average, and listener feedback asked for more, not less. For this audience and format, 40–50 minutes is the right window. Fix: set the runtime target at 40–50 minutes for the next series and stop cutting material to hit an arbitrary shorter number.

## Workflow and Process

**Pre-interviews were too long and duplicated editorial work.** Average pre-interview ran 45 minutes. Most of that material was unusable, and the editorial decisions made during the pre-interview (which angles to pursue, which anecdotes to draw out) had to be remade during the actual recording because the host was not present for the pre-interviews. Fix: cut pre-interviews to 20 minutes maximum. Send the guest a written topic list 48 hours before the pre-interview so they arrive focused. Use the pre-interview only to confirm the guest has material and to identify two or three specific threads to follow in the main recording. Have the host on the call, even if only listening.

**Transcription estimates were based on a tool demo, not real conditions.** The demo used clean studio audio. Our field recordings had background noise, overlapping speech, and variable levels. Actual transcription and cleanup took 3–4 hours per episode against a budget of one hour. Fix: test transcription tools against actual project audio quality before budgeting. For field-recorded material, budget 3 hours per episode-hour for transcription and cleanup until you have project-specific data that says otherwise.

**The researcher left too early.** The researcher was contracted for the first six weeks (pre-production and early production). Fact-checking needs continued through post-production, and the producer ended up doing it alongside editing — slower, less thorough, and more expensive per hour. Fix: keep the researcher through post-production at reduced hours (two days per week) for ongoing fact-checking and show notes preparation.

## Timeline and Scheduling

**The project ran four weeks over (16 vs. 12 weeks).** The entire delay sat in post-production. Pre-production and production ran on schedule. The overrun was not caused by scope change or external factors — it was caused by underestimating two internal tasks (field recording cleanup and transcription).

**Post-production was underestimated by roughly 60%.** Two causes: field recording cleanup (double the budgeted time) and transcription (triple the budgeted time). Both were knowable in advance with better pre-production testing. Fix: add a one-week validation phase between pre-production and production (see Systemic Issues) and use it to generate realistic time estimates for every post-production task.

**The bonus live episode consumed a full production week.** The foundation requested it two weeks before their annual event. Saying yes protected the client relationship but left no buffer for the final two regular episodes. The live episode was also the weakest output — panel discussions without preparation tend to produce meandering audio. Fix: build a one-week contingency buffer into the schedule specifically for client requests. If the buffer is not used, it becomes QA time. Agree at the outset on how many unplanned deliverables the project can absorb and what notice period is needed.

**No mid-production editorial checkpoint existed.** The Episode 3 problem (no tension) was identified during recording but could not be addressed because there was no structured point in the schedule to pause, evaluate, and redirect. Fix: schedule a 90-minute editorial review after episodes 2 and 4 to assess whether each episode has enough material to work. This costs three hours of team time across the full project and can save an entire episode from underperformance.

## Stakeholder Management

**The foundation was an ideal client for editorial independence.** No content vetoes, no sign-off friction, no requests to include specific messaging. This is unusual and should be acknowledged in future planning, not assumed as the norm for commissions. When planning the next commissioned series, build in two feedback rounds by default and adjust down if the client demonstrates the same trust.

**The foundation's social media was a better distribution channel than ours.** They had a larger, more engaged following in the target demographic. The foundation's posts consistently outperformed the production team's posts in reach and engagement. Fix: for future projects with institutional partners, build the partner's promotion into the distribution plan from the start. Share episode assets (pull quotes, audiograms, captioned clips, images) in a format the partner's social team can use directly, with a posting schedule aligned to the release calendar.

**The live episode request was handled reactively.** A standing agreement at the start of the project — "we can accommodate up to one additional deliverable with two weeks' notice, at a defined cost and a stated impact on the main schedule" — would have made the conversation easier and protected the timeline for the main series. The foundation asked in good faith; the problem was the absence of a framework for the conversation, not the request itself.

## Quality and Standards

**Audio consistency across episodes was poor.** Three different recording devices, six locations, no shared recording protocol. The sound engineer spent 35% more time than budgeted normalising levels and cleaning up format differences. Some inconsistency was audible in the final mix — listeners did not complain, but the team noticed. Fix: create a one-page field recording protocol before production starts — device model, settings, file format, level targets, room tone capture, minimum recording length for ambient sound. Every person who records anything on the project gets a copy and a five-minute walkthrough.

**The host improved noticeably across the series.** Early episodes had longer preambles and more hedging in questions. By Episode 5, questions were shorter and more direct, and the host was better at following unexpected answers rather than returning to the prepared list. This learning curve is visible in the published episodes. Fix: for the next series, record a two-episode pilot or practice run that is not intended for publication. Use it to let the host find the rhythm before the real episodes start. The cost is two days of recording time; the benefit is a stronger series opening.

**Download numbers exceeded the target but distribution was uneven.** Episode 4 (7,100 downloads) drew more than double Episode 3 (2,800). The gap correlates with narrative strength, not promotion — both episodes received comparable social media support from both the production team and the foundation. The lesson is not that Episode 3 was a failure in absolute terms (it still exceeded the foundation's target) but that the difference between a good episode and a great episode in this format is whether the episode has a clear source of tension.

## Tooling and Infrastructure

**Three recording devices caused format inconsistency.** The producer recorded on a portable recorder, the sound engineer on a separate device, and one guest interview was captured on a phone as a backup that became the primary recording. File formats, sample rates, and levels were different across all three. Fix: standardise on one device and one recording format for all field recording, or at minimum agree on shared settings (sample rate, bit depth, file format) across devices and test compatibility before the first recording day.

**Transcription tool underperformed on field audio.** The tool that was demoed during pre-production produced clean transcripts from the vendor's sample files. It could not handle the background noise, overlapping speech, and variable levels typical of location recordings. Output required 3–4 hours of manual cleanup per episode. Fix: test transcription tools against representative project audio — recorded in actual project conditions — before committing to a tool or budgeting based on its performance claims. If the project involves location recording, assume automated transcription will need significant manual correction and budget accordingly.

**Project files were stored across two cloud services and a local drive.** No single source of truth for episode assets. The sound engineer and producer spent cumulative hours across the project locating the correct version of files. On one occasion, edits were made to the wrong version of an episode script, resulting in a wasted afternoon. Fix: agree on one shared folder structure before production starts, with naming conventions for files (episode number, content type, version number, date) and a rule that working files are uploaded to the shared location at the end of each working day.

## Systemic Issues

**Pre-production testing was insufficient across the board.** The transcription tool was not tested on real audio. The field recording protocol did not exist. The episode runtime target was not validated against the actual format. The pre-interview format was inherited from a previous project without reassessing whether it fit this one. Each of these caused a separate problem in production, but the root cause was the same: pre-production treated planning as scheduling (when things happen) rather than validation (confirming that the planned approach actually works with this project's specific conditions). Fix: add a one-week validation phase between pre-production and production. Use it to test every tool, template, and workflow assumption against real project conditions. Record a test segment on location. Transcribe it with the chosen tool. Run a test pre-interview at the planned length. The week costs five working days; it would have saved the four-week overrun this project experienced.

**Time pressure caused known problems to go unfixed.** The Episode 3 weakness was identified during recording. The field recording inconsistencies were visible after Episode 1. The transcription backlog was growing by Episode 2. None of these were addressed in time because the schedule had no slack and no checkpoint where the team could stop, assess, and redirect. The project kept producing new episodes when it should have paused to fix the pipeline. Fix: a project of this size needs at least one structured checkpoint where the team can stop, review what is working, and make mid-course corrections. The cost of stopping for half a day is always less than the cost of discovering a systemic problem in post-production.

## Carry-Over Checklist
- [ ] Create a field recording protocol (device, settings, format, level targets, room tone) and distribute before the first recording day
- [ ] Cut guest pre-interviews to 20 minutes; send a topic list 48 hours in advance; have the host present
- [ ] Test transcription tools against representative project audio during pre-production, not with vendor demo clips
- [ ] Budget 3 hours per episode-hour for transcription and cleanup on location-recorded projects
- [ ] Schedule 90-minute editorial checkpoints after episodes 2 and 4 to catch weak episodes early enough to redirect
- [ ] Apply a "tension test" to each episode: can you state the disagreement or unresolved question in one sentence?
- [ ] Keep the researcher through post-production, even at reduced hours, for ongoing fact-checking
- [ ] Build a one-week contingency buffer into the schedule for client requests; if unused, repurpose as QA time
- [ ] Agree with the client at project start on additional deliverable terms (notice period, cost, impact on schedule)
- [ ] Set episode runtime target at 40–50 minutes for this format, not 35
- [ ] Record a two-episode pilot or practice run before the published series begins
- [ ] Establish one shared folder structure with file naming conventions before production starts
- [ ] Screen locations partly on narrative potential — is there conflict, disagreement, or a decision with visible consequences?
- [ ] Add a one-week validation phase between pre-production and production to test tools and workflows against real conditions
- [ ] Share episode promotion assets with institutional partners in formats their social team can use directly
- [ ] Build partner promotion into the distribution plan from day one, not as an afterthought

## Raw Notes
[The input notes provided above are preserved here for reference.]
```

## Known Limitations
- The retrospective is only as good as the notes provided. If the input is thin on specifics — "things went badly in post" without saying what or why — the output will reflect that vagueness. The skill will note where information is missing and may ask clarifying questions, but it will not invent findings the notes do not support. A retrospective built from sparse notes will have sparse findings; this is honest, not a flaw.
- The six-category framework fits most media projects well but may not capture every domain. A project with significant legal, rights-clearance, or compliance issues may need an additional category that this framework does not include. The skill will fold such findings into the nearest category (usually Stakeholder Management or Quality and Standards), but a dedicated section may serve better for projects where legal or regulatory issues were a major factor.
- The skill produces a written document, not a facilitated conversation. In teams where the important lessons are held by people who did not contribute to the notes — the freelance sound engineer who left, the intern who noticed a recurring problem — the document will have blind spots. Pair this skill with an actual team debrief where possible. The LESSONS.md works well as the agenda for that conversation or as the written record afterwards, but it is not a substitute for getting the full team in a room.
- Audience reception data is interpreted at face value. The skill does not perform statistical analysis on download numbers, engagement metrics, or audience demographics. If the input says "Episode 4 had the most downloads," the skill will include that as a finding, but it will not calculate statistical significance, control for confounding factors like promotion timing, or account for seasonal variation in listening patterns. For projects where audience data is central to the assessment, supplement the retrospective with a separate analytics review.
- The skill is designed for single-project retrospectives. For multi-season or recurring series, run a separate retrospective for each season. Cross-season patterns are best identified by comparing individual LESSONS.md documents, not by trying to feed multiple seasons into a single retrospective pass.

## Related Skills
- [project-memory](../project-memory/SKILL.md) — for capturing ongoing project context during production, not just at the end
- [structure-flow-checker](../structure-flow-checker/SKILL.md) — useful during production to catch the structural problems that retrospectives often flag too late
- [version-diff-summariser](../version-diff-summariser/SKILL.md) — for tracking what changed between drafts, which can feed into the Workflow section of a retrospective
- [tone-consistency-checker](../tone-consistency-checker/SKILL.md) — for catching the quality inconsistencies that retrospectives often identify as a pattern after the fact
