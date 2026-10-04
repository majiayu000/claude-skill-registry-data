---
name: product-sense-interviews
description: Practice Product Sense PM interviews. Use when someone wants to practice a Product Sense interview, get coached on their PS interview template, or learn the PS interview framework. Can act as the candidate (user plays interviewer) or as a coach (user submits their template for scoring).
---

# Product Sense Interview Practice

Help the user practice Product Sense PM interviews using Ben Erez's framework. This skill supports two modes: **AI as candidate** (user plays interviewer) and **AI as coach** (user submits a filled-out template for scoring).

## How to Help

When the user invokes this skill:

1. **Determine the mode** - Ask if they want you to be the candidate (they play interviewer) or if they want coaching on their own submission
2. **For candidate mode** - Ask for a PS interview question, then work through the full framework with interviewer check-ins
3. **For coaching mode** - Ask them to share their filled-out template, then score it section by section
4. **Default company** - Unless specified otherwise, assume the interview is at Meta

## Candidate Mode: Interview Framework

Each chat is a Product Sense interview. Work through the question following the structured framework below. Stop and check in with the interviewer after each milestone. Each check-in should ask if things make sense and state where you'd like to go next. **Wait for the user to respond before continuing.**

Assume you speak 120 words per minute. Append the speaking time at the end of each message (e.g., "3.5 minutes").

### Milestones (check in after each)

1. Stating up-front assumptions
2. Walking through your game plan
3. Product motivation and mission
4. Ecosystem players
5. Segmentation within ecosystem players
6. Problem identification
7. Solution development and MVP

### Opening Game Plan

Before diving in, state something like: "Before I dive in, I'd like to walk you through my plan for our time together: I'll start by describing the product/experience and why it matters. Then I'll break down the target audience and define a segment to focus on. From there, I'll identify key problems for that segment and prioritize one. I'll then brainstorm solutions and pick one. If we have time, I'd love to describe a v1 implementation of that solution. Does this plan sound good to you?"

### Assumptions (<1 min)

State no more than 3 assumptions. Be careful not to constrain the solution space prematurely. Potential assumptions:

- **Role and context**: Your assumed role and the company/product context
- **Geographic focus**: Specific market or region
- **Platform and constraints**: Technical or strategic constraints that focus the solution

### Product Motivation (<5 min)

- Describe industry trends, relevant competitors, strategic rationale, and "why now" - do NOT describe actual product functionality yet
- Explain how this experience contributes to the parent company's mission
- Share why the company is uniquely positioned relative to existing market options
- Share an example use case of the current product/experience in the real world
- Wrap up with a clearly defined mission statement (single sentence, under 25 words, captures core purpose)

### Ecosystem Players

- List the 4-5 most important ecosystem players
- Select one with brief rationale
- Check in before developing segments: "I'd like to focus on [chosen player] for these reasons. Before I dive into segments, I want to pause to make sure this line of thinking is making sense?"

### Segmentation

Before listing segments, state the segmentation heuristics you'll use:

- Primary motivations (fundamental goals driving behavior)
- Behavioral patterns (frequency and interaction methods)
- Context of use (where, when, how they engage)
- Expertise level (novice, intermediate, expert)
- Resource constraints (time, money, knowledge, space)
- Goals and outcomes (specific results they're trying to achieve)

Define **three mutually exclusive segments** using primary motivation plus 1-2 additional heuristics. Each segment gets three sub-bullets:

- Segment description
- Reach: Low/Medium/High
- Underserved degree: Low/Medium/High (relative to product mission)

**Important**: Segments must be primarily distinct based on different motivations and behaviors, not just different scenarios or activities. Test: "Would the same person typically fit into multiple segments?"

Prioritize one segment, explain alignment with company strategy, then create a concrete persona (common regional name, matching age, a few interesting details related to the product mission). Spend no more than 30 seconds on the persona.

### User Journey

Map the persona's journey to realizing product value. Think broadly about the core user need — not just how they might use the specific product being proposed. Visualize a "day in the life" rather than generic pre/during/post journeys. The goal is setting up meaningful problem identification.

Remember: Needs are desires ("I want beautiful flowers"). Problems are specific obstacles ("It's challenging to find flowers that thrive in my apartment's limited lighting").

### Problem Identification (<10 min)

Focus on emotional and psychological pain points, not purely functional issues. Ask: "What deeper user need or motivation is being frustrated here?"

List **three problems** with sub-bullets:

- Problem description (framed as "[persona] struggles to ___")
- Frequency: Low/Medium/High
- Severity: Low/Medium/High

Prioritize based on severity and frequency. Summarize rationale and tie to the product mission statement.

### Solution Development (<10 min)

Generate **three distinct solutions** exploring different angles/mechanisms (not variations on the same idea). Each with sub-bullets:

- Solution description
- Impact: Low/Medium/High
- Effort: Low/Medium/High

Prioritize based on impact (high = better) and effort (low = better). Summarize rationale and tie to mission. Check in before describing v1.

### V1 Implementation and Risks (<1.5 min)

- Outline a concrete v1 with enough detail to demonstrate feasibility
- Tell a clear story about the user experience (not a feature list)
- Explain discovery, engagement, and integration with existing products
- Identify 2-3 critical risks with succinct mitigation strategies
- Connect solution back to the product mission (complete the narrative arc)

### After Completion

Offer to score your performance. When recapping, include a summary of minutes spent on each section (based on 120 words/minute).

## Coaching Mode: Scoring Submissions

When the user submits a filled-out PS interview template, score it section by section using these rubrics.

### Segmentation (Weight: 25%)

- **5/5**: Clear motivational/behavioral differences with strong strategic value
- **4/5**: Good segmentation with minor issues in distinction or strategic value
- **3/5**: Adequate segmentation showing clear attempt at meaningful differentiation
- **2/5**: Weak segmentation that confuses scenarios/activities with user types
- **1/5**: Purely demographic or completely scenario-based segmentation

### Problem Identification (Weight: 25%)

- **5/5**: Problems connect to deep emotional/psychological needs with clear mission ties
- **4/5**: Strong emotional components with good strategic alignment
- **3/5**: Some depth beyond tactical issues with reasonable mission connection
- **2/5**: Primarily tactical/functional with limited emotional insight
- **1/5**: Entirely operational/tactical with no connection to user motivations

### Solution Development (Weight: 20%)

- **5/5**: Highly relevant solutions directly addressing the problem with clear strategic rationale
- **4/5**: Good solutions with strong problem alignment and reasonable strategic thinking
- **3/5**: Adequate solutions addressing the problem with some strategic consideration
- **2/5**: Weak connection between solutions and prioritized problem
- **1/5**: Solutions don't address the stated problem or lack strategic thinking

### Product Motivation & Mission (Weight: 20%)

- **5/5**: Clear product fundamentals, strong company mission connection, compelling market gaps, deep "why now" insight, specific actionable mission statement
- **4/5**: Covers most elements with clear mission and strategic positioning
- **3/5**: Basic product description with some mission thinking and limited competitive context
- **2/5**: Superficial overview with weak or missing mission statement
- **1/5**: Confused product understanding, no mission statement

### Communication Structure (Weight: 10%)

- **5/5**: Clear section transitions, regular check-ins, efficient time management, structured thinking
- **4/5**: Good structure with minor pacing issues
- **3/5**: Adequate structure with some rambling or missed check-ins
- **2/5**: Poor time management or unclear structure
- **1/5**: No discernible structure

### Evaluation Principles

- A score of 3 is passing. Must pass ALL dimensions.
- Focus on quality of thinking and strategic approach, not perfection
- Strong PM thinking can take multiple valid forms
- There is no expectation of covering specific metrics in a Product Sense interview

## Key Interview Strategy Tips

- **Own the interview** — this is your meeting to drive
- **Strategic pauses**: 30-60 seconds between sections; 1-2 minutes acceptable
- **Don't share your screen** — wastes time, exposes thinking prematurely
- **No right answer** — as long as assumptions are reasonable and rationale is followable
- **Don't contradict yourself**
- **Nudges from interviewers are help** — pause, reconsider, clarify or pivot. "Double nudges" = strong signal to reconsider
- **Backtracking is OK** — call it out explicitly
- **Rule of 3s**: 3 segments, 3 problems, 3 solutions. Evaluate on 2 dimensions each
- **Maintain a through-line**: Mission → ecosystem → segments → problems → solutions
- **Minimize time on rejected options** — focus on chosen path
- **Don't discuss metrics** — save for AT interviews
- **No wireframes needed** — describe MVP verbally

## Deep Dive

For the complete question bank, company mission statements, evaluation framework, and example interviews, see `references/interview-guide.md`

## Related Skills

- Analytical Thinking Interviews
- Conducting Interviews
- Evaluating Candidates
