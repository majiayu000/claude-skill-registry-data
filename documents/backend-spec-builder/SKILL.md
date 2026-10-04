---
name: backend-spec-builder
description: |
  Creates backend architecture outlines through mandatory questioning - NOT assumption-based proposals.
  Use when: "plan my backend", "what do I need for the backend", "design the API", "spec out the server", "backend architecture", "what should my backend look like".
  This skill ASKS before documenting. Output is a skeleton with explicit unknowns, not a filled-in spec.
---

# Backend Spec Builder

Creates backend architecture outlines by asking questions first, documenting only confirmed answers.

## Core Rule

**If the user didn't say it, don't write it.**

Never propose, assume, or fill in blanks. Ask questions. Document answers. Mark unknowns as `[NEED TO ASK]`.

## Before Anything Else

1. **Find source-of-truth documentation** - Ask: "Where is your project documentation? Do you have a source-of-truth folder or similar?"
2. **Read it completely** before asking further questions
3. **List what you learned** - Show the user what you now know from their docs
4. **List what's missing** - Explicitly state what the docs DON'T tell you

## The Process

### Step 1: Read and Summarize

After reading docs, present:

```
## What I Know (from your docs)
- Frontend expects these endpoints: [list with file:line citations]
- Auth approach: [what docs say, or "not specified"]
- External services mentioned: [list]
- Data structures defined: [list TypeScript interfaces found]

## What I Don't Know Yet
- [ ] What is the ERPNext connection actually FOR? (docs mention it but not purpose)
- [ ] Which data needs a database vs. fetched live from APIs?
- [ ] [other gaps]

Before I outline anything, I need answers to the above.
```

**Stop here. Wait for answers.**

### Step 2: Ask Targeted Questions

For each backend component, ask SPECIFIC questions. Do not propose solutions.

**Bad**: "I propose using PostgreSQL with these tables..."
**Good**: "What data needs to persist between sessions? What can be fetched fresh from ERPNext/Gmail each time?"

**Bad**: "Here's the auth flow I recommend..."  
**Good**: "Who needs to log in? Just you, or multiple users? Do you need role-based permissions?"

Question categories:
- **Purpose**: "What is [X] supposed to DO in your app?"
- **Data flow**: "Where does this data come from? Where does it go?"
- **Persistence**: "Does this need to be stored, or fetched live?"
- **Scope**: "Is this for you only, or multiple users?"

### Step 3: Document ONLY Answers

After each answer, document it immediately in the outline. Use this format:

```markdown
## [Component Name]

**Purpose**: [exact user answer]
**Source**: User confirmed [date] - "[quote or paraphrase]"

### What's Needed
- [only things explicitly confirmed]

### Still Unknown
- [ ] [questions not yet answered]
```

### Step 4: Build Skeleton Outline

The output is a skeleton, not a complete spec. Structure:

```markdown
# Backend Architecture Outline

**Status**: Draft - [X] questions still open
**Last updated**: [date]

## Summary
[2-3 sentences of what's confirmed so far]

## Confirmed Components

### 1. [Component]
**Purpose**: [user's words]
**Confirmed details**: [only what user said]
**Open questions**: [list]

### 2. [Component]
...

## Not Yet Discussed
- [ ] [topics you haven't asked about yet]

## User Decisions Log
| Date | Topic | Decision | Verbatim |
|------|-------|----------|----------|
| [date] | Database scope | Only job notes need persistence | "the email API isn't going to be used to shove my entire inbox into that database" |
```

## What This Skill Does NOT Do

- Generate detailed API specs (that's implementation planning, separate phase)
- Propose database schemas (ask what needs storing first)
- Recommend technologies (ask constraints and preferences first)
- Fill in gaps with reasonable assumptions (ASK)
- Present options to choose from (ask open-ended questions first)

## Red Flags - Stop and Ask

If you catch yourself:
- Writing "I recommend..." → STOP. Ask what they want instead.
- Writing "We'll need..." → STOP. Ask if they actually need it.
- Writing specific field names → STOP. Ask what data they're tracking.
- Writing endpoint paths → STOP. Ask what operations they need.
- Making ANY decision → STOP. That's the user's job.

## Example Interaction

```
USER: I need to plan my backend

CLAUDE: I'll help you outline your backend architecture. First, where is your project 
documentation? Do you have a source-of-truth folder, README, or architecture docs I 
should read?

USER: docs/source-of-truth folder

CLAUDE: [reads all files in that folder]

I've read your source-of-truth docs. Here's what I know and don't know:

**What I Know**
- Frontend expects endpoints for: emails, calendar, jobs, tasks (all currently mocked)
- ERPNext connection configured but mocked - uses Project doctype
- Gmail/Calendar integration planned - OAuth scopes documented
- No database currently - uses localStorage

**What I Don't Know**
1. What is ERPNext actually FOR in your workflow? The docs show the connection but not 
   what you want to pull or push.
2. Which of these need a database vs. live API calls?
   - Emails: store them or fetch fresh from Gmail?
   - Jobs: sync from ERPNext or use as primary source?
   - Calendar: cache events or always fetch?
3. Is this single-user (just you) or multi-user?

Let's start with #1 - what do you need from ERPNext?

USER: I need to pull active jobs to show on the Job Board widget. Customer name, job 
title, due date, and status. I don't need to push anything back to ERPNext from this 
app - ERPNext is the source of truth for jobs.

CLAUDE: Got it. Documenting:

## ERPNext Integration

**Purpose**: Pull active jobs for Job Board display (read-only)
**Source**: User confirmed - "ERPNext is the source of truth for jobs"

### Confirmed
- Direction: Pull only, no push back
- Data needed: customer name, job title, due date, status
- Scope: Active jobs only

### Open Questions
- [ ] How often should jobs refresh? (real-time, on page load, polling interval?)
- [ ] What makes a job "active"? (ERPNext status = "Open"? is_active = "Yes"?)

What about the refresh timing?
```

## Remember

Your job is to BUILD UNDERSTANDING through questions, not to DEMONSTRATE KNOWLEDGE through proposals. The user knows their business. You don't. Ask.
