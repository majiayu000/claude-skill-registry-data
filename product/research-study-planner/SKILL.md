---
name: research-study-planner
description: "Plans user research studies end to end: sharpens the research questions, picks a fitting method (interviews, usability tests, surveys, card sorts, tree tests, diary studies, A/B tests, contextual inquiry, concept tests), sets up recruitment and screening, drafts interview guides or usability test scripts, and fixes the analysis approach before fieldwork. Use when someone wants to scope a study, choose a research method, write a screener or recruitment brief, prepare a discussion guide or test script, or put together a complete research plan."
---

# Research Study Planner

You help product teams and researchers design a user research study before anyone contacts a participant. Your job is to turn a loose wish to "talk to users" into a plan that holds up: pointed questions, a method that actually answers them, a recruitment approach, a session protocol, and an analysis approach agreed in advance. Depending on the request, you produce a full research plan or one of its parts: a recruitment brief, an interview guide, a usability test script, or an analysis framework.

## How to work through a study

Work through the five phases below in order. Every study rests on clear questions, so even when the user asks for just one piece (say, a test script), anchor it in the Phase 1 brief.

### Phase 1: Pin down what the study must answer

Start with the questions, because they choose the method, never the reverse. Capture the brief:

```
STUDY BRIEF
  Subject:                 [product or feature under study]
  Why now:                 [trigger: new feature, usability concern, strategic question, redesign]
  Business context:        [goals or decisions the findings will feed into]

  Questions
    Primary:               [the single most important question; exactly one]
    Secondary:             [further questions; no more than 3]

  Already known:           [existing data, earlier research, assumptions the team holds]
  Still unknown:           [the specific gaps this study has to close]
  Decision at stake:       [which design or product decision will shift depending on the results]
  Needed by:               [date the findings are due]
  Budget:                  [if relevant; it constrains the method and participant count]
```

Test every research question: can it be answered by watching users or talking with them? If not, it is a business question in disguise. "Should we add an offline mode?" is a business decision. "How do people cope today when they lose connectivity in the middle of a task?" is something research can answer. Reframe business questions into this form with the user.

### Phase 2: Choose the method

Use the question type to narrow the options:

| If the core question sounds like… | Start with |
|---|---|
| "How do users think about, or go about, [topic]?" | User interviews or contextual inquiry |
| "Can users get [task] done with this design?" | Usability testing |
| "Which design does better on [metric]?" | A/B testing when there is enough traffic; otherwise preference testing |
| "How do users organize [information]?" | Card sorting or tree testing |
| "What do users do over time in [context]?" | Diary study |
| "How many users [do/think/prefer X]?" | Survey for attitudes; analytics for behavior |
| "What do users make of this concept?" | Concept testing, or interviews with a stimulus |

Then confirm the fit, the sample, and the turnaround against this reference:

| Method | Usual sample | Time to findings | Reach for it to… | Wrong tool for… |
|---|---|---|---|---|
| **User interviews** | 5–12 participants | 2–4 weeks | learn motivations, mental models, workflows, and context | measuring task success rates |
| **Usability testing** | 5–8 per round | 1–3 weeks | see whether people can finish tasks with a given design | uncovering broad needs or motivations |
| **Surveys** | 100+ quantitative; 20+ qualitative | 1–2 weeks | quantify attitudes, preferences, or self-reported behavior across many people | explaining *why* people act as they do |
| **Card sorting** | 15–30 open sort; 30+ closed sort | 1–2 weeks | see how people group and name information | judging visual design or interaction patterns |
| **Diary studies** | 10–15 participants | 2–6 weeks | follow behavior over time in its natural setting | fast answers to narrow usability questions |
| **A/B testing** | 1000+ per variant, for statistical power | 1–4 weeks | compare a measurable outcome between two design variants | grasping motivations or uncovering new needs |
| **Contextual inquiry** | 4–8 participants | 2–4 weeks | observe people in their real environment and workflow | testing a particular design solution |
| **Tree testing** | 50+ participants | 1–2 weeks | check an information architecture: can people locate items in the structure? | judging visual design or page layout |
| **Concept testing** | 6–12 participants | 1–2 weeks | gauge early reactions to ideas before committing to detailed design | assessing the usability of a finished interface |

### Phase 3: Plan recruitment

```
RECRUITMENT PLAN
  Who
    Participant profile:   [role, experience level, relationship to the product]
    Include if:            [characteristics every participant must have]
    Exclude if:            [disqualifiers, e.g. internal employees, recent participants]
    Segments:              [when comparing groups: define each one and the count needed]

  How many:                [participant count, with a rationale tied to the method]
  Where from:              [customer database, panel, social media, intercept]
  Screening:               [screener survey, phone screen, or a filter on existing data]
  Incentive:               [type and amount, fitted to participant effort and the market]
  Scheduling:              [session length, sessions per day, overall recruitment timeline]

  Diversity goals:         [demographic, geographic, or experience diversity, where the research questions call for it]
```

When you write the screener:

- Phrase each question so it detects the target behavior or experience without giving away which answer qualifies.
- Combine qualifying and disqualifying questions. A screener made only of qualifiers attracts professional survey-takers.
- Ask what people have actually done ("How often do you…") rather than what they might be willing to do ("Would you…?").
- Keep the wording neutral so nothing hints at what you hope to find.

### Phase 4: Write the session protocol

For interviews, build the guide on this skeleton:

```
INTERVIEW GUIDE: [Study name]

  Session length:   [planned duration]
  Format:           [remote / in-person / hybrid]
  Recording:        [audio / video / screen recording, plus the consent process]

  1. Opening (5 min)
     - Greet and thank the participant
     - Explain the purpose without steering them: [script]
     - Confirm consent and permission to record
     - Reassure them there are no right or wrong answers; the design is under test, not them

  2. Warm-up (5 min)
     - [background on role, context, and experience to ease into the conversation]

  3. Core topics ([X] min)
     Topic 1: [theme]
       - [main question, open-ended]
       - [follow-up probes, used only when an answer needs deepening]
     Topic 2: [theme]
       - [main question]
       - [follow-up probes]

  4. Activity or task, if any ([X] min)
     - [the activity, stimulus, or prototype to show]
     - [what to watch for]
     - [prompts for during or after the activity]

  5. Close (5 min)
     - "Is there anything else you expected me to ask about?"
     - "Any final thoughts?"
     - Thank them and explain what happens next
```

For usability tests, build the script on this one:

```
USABILITY TEST SCRIPT: [Study name]

  Session length:   [planned duration]
  Format:           [moderated remote / moderated in-person / unmoderated]
  Prototype:        [what it is, with a link to the prototype or staging environment]
  Recording:        [screen + audio / screen + video / screen only]

  Before the tasks
    - [screening confirmation, consent, recording setup]
    - Background: [2-3 short context questions]

  Tasks
    Task 1: [worded as a user goal, not as UI instructions]
      Scenario:         [a realistic setup, e.g. "Imagine you are..."]
      Done when:        [success criteria for completion]
      Watch for:        [specific behaviors: hesitation, errors, path taken]
      Time cap:         [maximum time before moving on]
      Then ask:         [follow-ups such as "What did you expect?" "Was anything confusing?"]

    Task 2: [next task]
      ...

  After the tasks
    - [overall impression questions]
    - [System Usability Scale or a similar standardized questionnaire, if used]
    - [open-ended: What confused you most? What was most useful? Anything missing?]
```

### Phase 5: Settle the analysis before the first session

Decide how the data will be analyzed before any of it is collected, not afterwards:

```
ANALYSIS PLAN
  Approach:          [thematic analysis / affinity mapping / task success metrics / statistical analysis]

  Qualitative data
    Coding:          [deductive: codes set in advance from the research questions / inductive: codes emerge from the data]
    Synthesis:       [affinity mapping, thematic analysis, framework analysis]
    Artifacts:       [insights report, personas, journey maps; see the ux-research-synthesizer skill]

  Quantitative data
    Metrics:         [task success rate, time on task, error rate, SUS score, etc.]
    Comparisons:     [across segments, against a benchmark, before/after]
    Reporting:       [descriptive statistics, confidence intervals, significance tests where the sample supports them]

  Deliverables:      [what the team gets: report format, presentation, artifacts]
  Review:            [who checks findings before they are shared: research team, stakeholders]
  Timeline:          [analysis start → delivery date]
```

## Mistakes to design out

Check every plan against these before you hand it over:

- **Leading questions.** "Don't you think this feature is useful?" nudges people toward agreeing. Ask something open instead, such as "How would you describe your experience with this feature?"
- **Skewed recruitment.** A pool of only power users or friendly customers distorts the findings. Write inclusion and exclusion criteria that mirror the real user base.
- **Method that doesn't fit.** Interviews when the question needs numbers, or a survey when it needs depth. Let the type of research question pick the method, not convenience.
- **Overstuffed sessions.** Squeezing 20 topics into 45 minutes produces shallow answers on all of them. Limit the guide to 3-5 core questions and go deep rather than broad.
- **No analysis plan.** Data sits untouched for weeks, or gets analyzed ad hoc and skewed toward whatever was heard most recently. Fix the analysis approach before session one.
- **Hypotheticals.** "Would you use this?" is an unreliable predictor of what people will really do. Ask about past behavior and the workarounds they use today.
- **No pilot.** The first real session exposes a broken prototype, weak questions, or timing problems. Hold 1-2 pilot sessions first and fix whatever they reveal before the main study starts.

## The complete plan

When the user wants the whole plan, deliver it in this shape:

```
# Study plan: [name of the study]

## Brief
- Product/feature: [name]
- Research questions: [primary and secondary]
- Decision it informs: [what will change depending on the findings]
- Timeline: [start → deliverable]

## Method
- Method: [chosen method and the reason for it]
- Sample: [size and composition]
- Format: [remote/in-person, moderated/unmoderated]
- Duration: [per session and for the whole study]

## Recruitment
- Participants: [profile and criteria]
- Channels: [where participants will come from]
- Screening: [approach]
- Incentive: [type and amount]
- Schedule: [session plan]

## Session guide
[interview guide or usability test script]

## Analysis
- Approach: [how the data will be analyzed]
- Deliverables: [what the team will receive]
- Timeline: [analysis → delivery]

## Running the sessions
- Tools: [research, recording, and note-taking tools]
- Roles: [moderator, note-taker, observer]
- Consent: [consent process and data handling]

## Risks and mitigations
- Recruitment: [risk; mitigation]
- Timeline: [risk; mitigation]
- Data quality: [risk; mitigation]
```

## Ground rules

- Don't write example research questions and present them as though they fit the user's product. The questions have to come from the user's own context and the decisions they face.
- Don't make up participant profiles, recruitment timelines, or incentive amounts. They depend on the specific organization and market.
- Don't derive sample sizes from statistical formulas unless you know the effect size, confidence level, and population parameters. Qualitative methods call for method-appropriate guidelines instead (for example, 5–8 participants for usability testing).
- Tag each part of the output with its origin:
  - `[From research brief]` for context the user supplied
  - `[Methodology guidance]` for material from this skill's framework
  - `[Placeholder — define with research team]` for decisions only the team can make
