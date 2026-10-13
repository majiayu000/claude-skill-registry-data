---
name: designing-research-surveys
version: "1.0.1"
description: >
  Designs, deploys, and analyzes surveys for four recurring FlashFusion and Loxihart use cases: AI adoption measurement (Loxihart), post-engagement client feedback (FlashFusion), workshop and training feedback (both), and audience/content research (FlashFusion newsletter). Pulls pre-built question templates for each use case, guides SurveyMonkey setup and distribution, and produces a one-page analysis summary from responses.

  Activate when the user mentions: survey, survey design, SurveyMonkey, measure AI adoption, adoption metrics, client feedback survey, post-workshop survey, post-engagement feedback, newsletter audience research, reader survey, NPS, measure impact of AI enablement, feedback form, research my audience, what do readers want, or any request to gather structured feedback from stakeholders, clients, or an audience.
---

# Research Survey Designer

Designs and deploys the right survey for one of four recurring use cases. Pre-built question sets — no starting from scratch.

---

## Use Case Detection

| Context | Survey type |
|---|---|
| Measuring AI adoption at Loxihart, before/after an enablement initiative | **AI Adoption Survey** → Section 1 |
| End of a FlashFusion client engagement (workshop, audit, build, retainer) | **Post-Engagement Client Feedback** → Section 2 |
| End of a training session or workshop (Loxihart or FlashFusion) | **Workshop Feedback** → Section 3 |
| Quarterly newsletter research, content planning input | **Audience Research** → Section 4 |

If unclear, ask one question: "Is this for measuring AI adoption at Loxihart, getting client feedback after a project, end-of-workshop feedback, or researching your newsletter audience?"

---

## Section 1: AI Adoption Survey (Loxihart)

**Purpose:** Establish baseline before an AI enablement initiative. Re-run at 60–90 days to measure change. The delta is your evidence of impact.

**Template:** `templates/ff-ai-adoption-survey.md`

**When to send:** Before any domain unlock, training rollout, or enablement program AND again 60–90 days after. Save the pre-survey data — it's useless without comparison.

**Distribution:** SurveyMonkey link via email or Teams channel. Do not send via Kixie or ticket. Anonymous response preferred — people are more honest about not using tools if there's no attribution.

**Target N:** Aim for 70%+ response rate within the target department or domain. Follow up once after 5 business days.

**Key metrics to track:**
- Adoption rate: % actively using AI tools (weekly or more)
- Confidence score: average of Q3 (1–5 Likert)
- Time savings estimate: average hours/week from Q5
- Barrier distribution: % citing each barrier type from Q6

**Analysis step:** After 60–90 day re-run, compare each metric. A successful enablement initiative should show: adoption rate +15–30 points, confidence score +0.5–1.0, barrier distribution shifting away from "not sure how to start" toward workflow-integration issues (which are addressable with more specific training).

**Reporting format:** Two-column table (Before / After) per metric, plus a one-paragraph narrative. Present to [PERSON] or relevant stakeholder. Drop into a Notion or Loxihart doc page — not a spreadsheet.

---

## Section 2: Post-Engagement Client Feedback (FlashFusion)

**Purpose:** Measure client satisfaction, collect testimonial-quality quotes, surface improvements for the next engagement. Also creates the raw material for case studies.

**Template:** `templates/ff-post-engagement-survey.md`

**When to send:** Within 48 hours of final delivery. Not at the end of a kickoff call. Not "sometime after." Within 48 hours — response rates drop sharply after a week.

**Distribution:** SurveyMonkey link in the project wrap-up email. Four to six questions visible in the email body as a preview (increases opens). Full survey on click-through.

**Target N:** Every client, every engagement, no exceptions. This is not optional for engagements over $500.

**Key metrics:**
- NPS (0–10): track over time as FlashFusion grows. Promoters (9–10), Passives (7–8), Detractors (0–6). NPS = % Promoters − % Detractors.
- Deliverable quality rating (1–5)
- Communication rating (1–5)
- Value-for-cost rating (1–5)

**Analysis step:** After each engagement, add the scores to a running log in Notion (`FlashFusion/Clients/Feedback Log`). At quarterly review, calculate rolling NPS and identify any rating below 3 for follow-up.

**Quote extraction:** Scan open-ended responses for specific, quotable answers to "What was most valuable?" — these go directly into case study drafts and proposal testimonials. Store the best ones in `FlashFusion/Content/Testimonials`.

---

## Section 3: Workshop and Training Feedback (Loxihart + FlashFusion)

**Purpose:** Operational feedback on content quality and delivery. Anonymous. Used to improve the next session, not to evaluate attendance or measure adoption.

**Template:** `ff-workshop-feedback-survey.md`

**When to send:** At the end of the session, before people leave. For remote sessions: drop the link in chat in the last 5 minutes and leave 3–4 minutes for completion. Do not send after the session ends — response rate drops to under 30%.

**Distribution:** SurveyMonkey link in session chat, or QR code displayed on final slide. Five questions, five minutes. Mobile-friendly — people answer on their phones.

**Target N:** Aim for 80%+ of attendees. If you get under 50%, the session probably ran long and people left early.

**Key metrics:**
- Clarity score (1–5)
- Relevance score (1–5)
- Pacing score (1–5)
- "One thing to try" open field — qualitative indicator of whether content translated to action

**Analysis step:** Read open-text responses immediately after the session while context is fresh. Three questions: What landed? What was unclear? Is there a pattern in what they want to try first? Adjust the next session outline based on "unclear" responses. If pacing scores are under 3.5, the session was too fast.

---

## Section 4: Audience Research (FlashFusion)

**Purpose:** Understand what newsletter subscribers and content readers actually want. Feeds directly into `researching-content-opportunities` — this is the qualitative layer that keyword data can't give you.

**Template:** `ff-audience-research-survey.md`

**When to send:** Quarterly, to the full newsletter list. Send on a Tuesday or Wednesday morning. Announce it in the newsletter issue — "This week I'd like 5 minutes from you."

**Distribution:** SurveyMonkey link embedded in the newsletter, plus a standalone follow-up email 5 days later for non-responders. Keep the survey open 10 days.

**Target N:** 15–20% response rate on a newsletter list is solid. Under 10% means the subject line needs work or the list is cold.

**Key metrics:**
- NPS for the newsletter (0–10)
- Topic preference distribution (which content pillars are most requested)
- Format preference (deep dives vs. quick hits vs. tools vs. case studies)
- Audience composition (role distribution — tells you if your readership is drifting from your target)

**Analysis step:** After closing, run `searchfit-seo:keyword-clustering` on verbatim answers to the "biggest challenge with AI" open question. The clusters become content brief seeds — the exact language your audience uses is the language your content should use. Store the NPS and topic distribution in `FlashFusion/Content/Audience Research/{{YYYY-Q}}.md`.

---

## Methodology Principles

Short section. These prevent the most common survey mistakes.

**Question types:**
- **Multiple choice** — for factual questions with known answer categories (role, tool usage, frequency)
- **Likert 1–5** — for subjective ratings (confidence, satisfaction, clarity). Use consistent scale throughout — do not mix 5-point and 7-point in the same survey.
- **NPS 0–10** — for recommendation likelihood only. Always 0–10, never 1–10.
- **Open text** — for "why" and "what would you change." Put open questions last — they require more effort and drop response rates if placed early.

**Ordering:**
- Easy, closed questions first (demographic, factual)
- Rating questions in the middle
- Open-ended questions last
- Sensitive or negative-framing questions at the end of the middle section, never first

**Leading question check:**
Before finalizing any survey, scan each question for embedded assumptions.
- Bad: "How helpful was the training?" (assumes it was helpful)
- Good: "How would you rate the training overall?"
- Bad: "What did you enjoy most about the workshop?"
- Good: "What was most valuable about the workshop — or was there nothing particularly valuable?" (honest version)

**The "would I act on this?" test:**
For every question: if the answer came back negative, would you change something? If not, cut the question. Surveys with questions you won't act on train respondents to stop taking them.

**Length rules:**
- Post-event (workshop, engagement): 5–8 questions, under 5 minutes
- Strategic research (audience, adoption): 8–12 questions, under 10 minutes
- Never send a survey over 15 questions without a strong incentive

---

## SurveyMonkey Workflow

### Creating a new survey

1. SurveyMonkey → Create Survey → Build it myself
2. Copy questions from the relevant template file
3. Set question types to match: multiple choice, rating scale (1–5), Net Promoter Score, open-ended text
4. Add skip logic where applicable (e.g., if Q1 = "Never use AI tools" → skip Q3–Q5 about usage patterns)
5. Add your logo to the header
6. Preview on mobile before publishing — most responses come from phones

### Distribution options by use case

| Use case | Distribution method |
|---|---|
| AI adoption (Loxihart) | Collector link → Teams message or email |
| Post-engagement | Collector link in wrap-up email |
| Workshop feedback | Collector link in session chat + QR code on final slide |
| Audience research | Embed in newsletter + standalone follow-up email |

### Response tracking

Set a close date for all surveys except the post-engagement (which closes automatically after 30 days). Check responses at 48 hours — if under 30%, send a reminder. One reminder only.

### Exporting for analysis

Analyze tab → Individual responses for open-text review. Summary tab for quantitative metrics. Export to CSV if adding to a longitudinal tracking log.

---

## Anti-Patterns

- **Don't send the post-engagement survey more than 48 hours after delivery.** After a week, response rate drops below 20% and the client's impressions are fading.
- **Don't make the workshop feedback survey longer than 5 questions.** People answer it in the last few minutes of a session. Anything over 5 questions gets abandoned.
- **Don't run the AI adoption survey without saving the baseline.** The before data is worthless without the after. Store it immediately in Notion before the initiative starts.
- **Don't skip the "would I act on this?" test.** A survey with 12 questions you won't act on takes the same time to answer as a survey with 12 questions you will. Respondents don't know the difference until they stop responding.
- **Don't use 7-point or 10-point Likert scales for satisfaction ratings.** 1–5 is sufficient for your use cases and easier to interpret. Reserve 0–10 for NPS only.
- **Don't ask open-ended questions about things you already know from ratings.** If clarity rated 4.5/5 average, don't also ask "what was clear?" — use that question slot for something actionable.
