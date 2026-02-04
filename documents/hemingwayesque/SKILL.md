---
name: hemingwayesque
description: Ruthless concision for AI prompts and context - "Not One Word Wasted"
---

# Hemingwayesque: Economy of Language for AI

## Philosophy

Ernest Hemingway wrote with brutal efficiency. Every word earned its place. No word wasted. This skill applies that ruthlessness to AI prompts, context documents, and instructions.

**Why:** AI context is expensive. Every wasted word costs tokens, slows comprehension, dilutes signal. Concision is not just style—it's engineering efficiency.

**Anti-inspiration:** Charles Dickens. Verbose exposition. Excessive adjectives. Meandering sentences. Everything we avoid.

## Core Principles

### 1. Active Voice, Present Tense
**Wrong:** "The system will be using a database that has been configured to store user data."
**Right:** "System stores user data in database."

### 2. Remove Filler Words
Cut: actually, basically, essentially, generally, literally, really, very, quite, just, simply, clearly, obviously.

**Wrong:** "We basically just need to simply verify that the user is actually authenticated."
**Right:** "Verify user authentication."

### 3. Concrete Over Abstract
**Wrong:** "Facilitate the implementation of a solution for managing authentication state."
**Right:** "Manage authentication state."

### 4. Delete Redundancy
**Wrong:** "Each individual user has their own personal preferences."
**Right:** "Users have preferences."

### 5. Prefer Short Words
- Use over utilize
- Start over initiate
- End over terminate
- Get over retrieve
- Make over construct

### 6. One Idea Per Sentence
**Wrong:** "The authentication system validates user credentials and manages session state while also handling token refresh and expiration, plus it logs all authentication attempts for security auditing purposes."

**Right:**
"Authentication system validates credentials, manages sessions, refreshes tokens, logs attempts."

### 7. Cut Ceremony
Skip pleasantries, apologies, hedging:
- ~~"I think maybe we could consider possibly..."~~ → "Do X."
- ~~"Thank you for your patience while..."~~ → [Just do the work]
- ~~"To be completely honest..."~~ → [Everything should be honest]

### 8. Lists Over Prose
**Wrong:** "The system needs to handle user registration, and it also needs to manage user authentication, as well as dealing with password resets, not to mention email verification."

**Right:**
System handles:
- Registration
- Authentication
- Password reset
- Email verification

## Application to AI Prompts

### Bad Prompt
```
I would like you to please help me by analyzing this codebase in order to
identify any potential areas where we might be able to improve the overall
performance characteristics of the system. Specifically, I'm interested in
understanding whether there are any obvious bottlenecks that could be causing
slowdowns, or if there are any particular functions that seem to be taking
longer than they should to execute.
```

### Hemingway Prompt
```
Analyze codebase for performance bottlenecks. Identify slow functions.
```

### Bad Skill Description
```
This skill is designed to provide comprehensive assistance with the task of
implementing test-driven development practices in your codebase. It will help
guide you through the process of writing tests before you write your actual
implementation code.
```

### Hemingway Skill Description
```
Write tests first, then code. Red-green-refactor cycle.
```

## For Command Instructions

Commands should tell Claude exactly what to do. No preamble. No explanation of why commands exist.

**Wrong:**
```markdown
This command helps you create a new feature by first analyzing the requirements
and then helping you design the architecture before you start implementation.
```

**Right:**
```markdown
Analyze requirements. Design architecture. Create implementation plan.
```

## For CLAUDE.md Context

CLAUDE.md documents provide context. Context should be dense, scannable, structured.

**Wrong:**
```markdown
This module is responsible for handling all of the various aspects related to
user authentication within the system, including things like login, logout,
session management, and token handling.
```

**Right:**
```markdown
Handles authentication: login, logout, sessions, tokens.
```

## For Workflow Documents

Workflow phases should state purpose and output. No marketing copy.

**Wrong:**
```markdown
This is an interactive and collaborative design session where we'll work
together to explore the architectural possibilities and come up with the best
possible approach for your feature.
```

**Right:**
```markdown
Interactive design session. Output: architecture decisions, component breakdown.
```

## When to Break the Rules

1. **Technical precision requires it** - "Use async/await" not "Make asynchronous"
2. **Ambiguity would result** - Add words if removing them creates confusion
3. **Context demands formality** - External-facing docs, legal text

But these are rare. Default to ruthless.

## How to Use This Skill

**When writing new content:**
1. Write first draft
2. Invoke hemingwayesque principles
3. Cut 30-50% of words
4. Verify meaning preserved
5. Ship the lean version

**When editing existing content:**
1. Read sentence by sentence
2. Ask: "Does this word earn its place?"
3. Delete ceremony, filler, redundancy
4. Combine sentences with same idea
5. Replace abstract with concrete

**When other skills reference this:**
They should apply these principles automatically when generating prompts, instructions, or documentation.

## Success Criteria

Good hemingwayesque writing:
- Reads fast
- Scans easily
- Conveys maximum meaning with minimum words
- No fluff, no padding
- Every sentence does work

Bad writing (what we eliminate):
- Meanders
- Repeats
- Hedges
- Decorates
- Wastes tokens

## Remember

Not one word wasted. Every word earns its place. Cut ruthlessly. Write tight.

Hemingway would approve.
