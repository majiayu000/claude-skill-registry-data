---
name: collect-feedback
description: Use this skill whenever the user wants to get feedback on their MVP, find testers, prepare outreach messages, create test scripts for users, analyze user feedback, or convert feedback into feature specs. Also trigger when the user mentions testers, user research, validation, feedback collection, or wants to know what to build next based on real user input. Use this even when the user says things like "I just built this, now what?" or "should I add more features?" — redirect them to collecting feedback first.
---

# Collect Feedback

Help the user get actionable feedback on their MVP from real people and convert that feedback into buildable specs.

This skill has two modes. Figure out which one the user needs based on context:

- **PLAN mode**: User has a working MVP and needs to find testers and prepare outreach. They don't have feedback yet.
- **ANALYZE mode**: User has collected feedback (in a feedback log or pasted into chat) and needs to extract patterns and generate specs.

If unclear, ask: "Do you need help finding testers and preparing outreach, or do you already have feedback to analyze?"

---

## PLAN Mode

The user has a working MVP and needs to get it in front of real people.

### Step 1: Understand the MVP

Before generating anything, gather context:

- Read PROJECT.md for what the product does and who it's for
- Scan the codebase to understand which features are built and testable
- Identify the core value — the one thing a user should accomplish

If PROJECT.md doesn't clearly state who the target user is or what problem it solves, ask the user before proceeding. The outreach and test script depend on this.

### Step 2: Generate the Feedback Plan

Produce a single markdown document with these 5 sections. Be specific to this project — no generic templates.

**Section 1 — Tester Profile**
One sentence describing the ideal tester. Not "users" — specific: "freelancers who send 5+ invoices per month" or "developers who maintain open-source projects."

**Section 2 — Where to Find Them**
3 specific places:
- 2 Reddit subreddits with exact names (verify they exist and are active). For each: a search query to find relevant recent posts (people who posted about the problem this product solves in the last 30 days).
- 1 additional community (Discord server, Slack group, forum, Twitter/X hashtag) where this type of person is active.

For each source, estimate: "DM/message N people, expect M responses."

**Section 3 — Outreach Messages**
Generate 3 copy-paste messages. Read `references/outreach-templates.md` for the structural patterns, then customize to this specific product:
- Reddit DM (under 80 words, references their type of post, asks for 5 minutes of criticism)
- Community post (under 80 words, for Discord/Slack/forum, offers the problem context, asks for negative feedback)
- Direct message (under 60 words, casual, for someone the user knows personally)

Every message must: name the specific problem the product solves, set time expectations, and explicitly ask for what's broken or confusing — not for praise.

**Section 4 — Test Script**
4-6 steps that walk a tester through the core value of the product. Each step is a specific action the tester performs, not a feature tour.

Rules for the test script:
- Step 1 is always "Sign up" or "Open [URL]"
- Final step shows the outcome that proves the core value works
- Note which steps are most likely to cause confusion (based on current UI state)
- Must be completable in under 5 minutes

**Section 5 — Follow-Up Questions**
Exactly 5 questions targeting different feedback types:
1. UX friction — "Where did you get stuck or confused?"
2. Expectation gaps — "What did you expect to happen that didn't?"
3. Priority signal — "What's the first thing you'd want to change?"
4. Core value test — "Would you use this tomorrow? Why or why not?"
5. Willingness to pay — "What would make you pay for this?"

### Step 3: Create the Feedback Log

Copy `assets/feedback-log.md` to the project directory (e.g., `/feedback/feedback-log.md`). This is where the user records tester responses.

Tell the user: "I created a feedback log at [path]. Fill in one section per tester as responses come in. When you have 3+ responses, come back and I'll analyze the patterns and generate specs."

### Step 4: Output

Save the complete feedback plan as `/feedback/feedback-plan.md` in the project. Present it to the user with a summary: how many testers to target, where to find them, and estimated timeline (expect responses within 24-48 hours).

---

## ANALYZE Mode

The user has feedback — either in the feedback log file or pasted into chat.

### Step 1: Load Feedback

Check for a feedback log file in the project (e.g., `/feedback/feedback-log.md`). If it exists, read it. If not, ask the user to paste their feedback or describe what testers said.

Parse each tester's responses into structured data:
- Tester ID (name/handle)
- Whether they completed the test script (yes/partial/no)
- Their answer to each of the 5 questions
- Any direct quotes worth preserving
- Stuck points (specific steps where they had trouble)

### Step 2: Run Pattern Analysis

Execute `scripts/analyze_feedback.py` if the feedback is in the structured log format. If the user pasted unstructured feedback, do the analysis inline.

Apply the pattern filter:
- **Mentioned by 3+ testers** → SPEC IT (real problem, generate a feature or fix spec)
- **Mentioned by 2 testers** → NOTE IT (probably real, add to backlog)
- **Mentioned by 1 tester** → IGNORE (individual preference, not validated)

Group findings into categories:
- **UX blockers** — steps where testers got stuck (from question 1 + test script completion data)
- **Missing features** — things testers expected but couldn't do (from question 2)
- **Priority features** — what testers said they'd change first (from question 3)
- **Core value signal** — whether the product actually solves the problem (from question 4)
- **Revenue signal** — what testers would pay for (from question 5)

### Step 3: Generate Specs

For each pattern that hit the 3+ threshold:

**UX blockers → Fix specs**
Short, focused specs that fix the specific friction point. Format:
```
# Fix: [Description]
## Context
- Users get stuck at [step] because [what they see vs. what they expect]
## Requirements
1. Change [specific element] to [match user expectation]
## Constraints
- Do NOT change other parts of the flow
## Acceptance
- [ ] Tester can complete [step] without confusion
```

**Missing features → Feature specs**
Full 5-section specs (Issue 03 format). Read PROJECT.md and existing skills before generating. Reference real files, tables, and components. Omit requirements covered by existing skills.

**Priority features → Ranked backlog**
If a feature was the "first thing to change" for 3+ testers, it goes to the top of the backlog even if it also appeared as a missing feature.

Save all generated specs to `/specs/` directory. Save the analysis summary to `/feedback/analysis.md`.

### Step 4: Present Results

Show the user:
1. Pattern summary — what testers agreed on, disagree on, and what surprised you
2. Generated specs — list them with priority order
3. Build recommendation — "Based on feedback, build these 2-3 things next" with reasoning
4. Core value verdict — does the product solve the problem? (from question 4 responses)
5. Revenue signal — is there willingness to pay? For what specifically?

If fewer than 3 testers responded, warn the user: "With only N responses, these are directional signals, not validated patterns. Try to get 2 more testers before building."

---

## Important Principles

- Never tell the user to skip feedback and keep building. The instinct to add features without validation is the problem this skill exists to solve.
- Outreach messages must ask for criticism, not praise. "What do you think?" produces useless responses.
- The pattern filter is strict. 1 tester's opinion is not a spec. Hold the line.
- Specs generated from feedback reference real project files — they're ready for the agent to build, not generic templates.
- If the user doesn't have a working MVP yet, redirect them to build first. Feedback on wireframes or ideas is dramatically less useful than feedback on something people can try.
