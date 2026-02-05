---
name: blog-post-writer
description: Use when completing blog post drafts with story sections - systematically analyzes commit history to write Context, Challenge, Solution, and Learned sections without making unverified assumptions about business context
scopes:
  - read
  - write
---

# Blog Post Writer

## Overview

Completes technical blog drafts by analyzing commit history and writing engaging first-person narratives. Two styles supported:

1. **Retrospective**: Grounded in actual work (commit-based, evidence-driven)
2. **Exploratory**: Thought experiments and forward-looking ideas

Most drafts generated from repos use retrospective style.

**CRITICAL OUTPUT RULE**: When writing blog content, NEVER mention "commits", "git history", "the log", or similar meta-references. Write naturally as if recounting from memory.

## When to Use

**Use when:**
- Draft file has empty Context/Challenge/Solution/Learned sections
- Commit history provided shows development work
- You need story-driven content without making unverified assumptions

**Don't use when:**
- Writing original blog posts from scratch
- No commit history available
- Draft doesn't follow the four-section structure

## Core Pattern: Evidence-Based Narrative

**Before (Baseline Behavior):**
```markdown
### Context
touchepas is a rent indexation calculator for Belgium...
[Makes assumptions about business domain without evidence]
```

**After (With Skill):**
```markdown
### Context
I built a calculation system that needed to handle different regional scenarios.
Early on, I realized a strategy pattern would give me the flexibility I needed...
[Stays grounded in what actually happened, written naturally]
```

## Quick Reference: The 4 Sections

| Section | Focus | Evidence Source |
|---------|-------|----------------|
| **Context** | What you were building | Feature commits, docs commits |
| **Challenge** | What made it difficult | Fix commits, refactor commits |
| **Solution** | How you approached it | Implementation patterns in commits |
| **Learned** | Takeaways | Reflections on commit patterns |

## Three Effective Approaches

### Style 1: Conversational (Ben Anderson)
Personal, exploratory, thinks out loud. Good for thought experiments and retrospectives.

### Style 2: Pedagogical (Mark Seemann)
Principled, builds arguments through evidence. Good for establishing technical positions.

### Style 3: Contextual (Behind Genius Ventures)
Multi-layered storytelling that shows the "invisible" connections. Good for showing broader impact.

**Choose based on your content:** Retrospectives often blend all three.

## Narrative Techniques (from effective technical blogs)

### Conversational Hooks (Ben Anderson style)
**Bad Opening:**
> This post describes the implementation of a calculator system in touchepas.

**Good Opening:**
> I spent three days fighting TypeScript's type system. Turns out, it was trying to tell me something important.

**Pattern:** Start with a human moment, not technical summary

### Self-Aware Honesty
Acknowledge messiness, mistakes, uncertainty:
- "I'm still not sure this was the right approach"
- "This is obviously a mess, but it works"
- "I probably should have done X, but here's what I actually did"

**Why it works:** Builds trust, makes you relatable, prevents defensive reading

### Problem Escalation
Structure your narrative with escalating questions:
1. Open: Should I do X?
2. Middle: What's hard about X?
3. End: Given we're doing X, what's the best way?

By the end, reader presupposes agreement with your approach.

### Show the Thought Process
Don't just show the solution—show the **path to the solution**:
- "My first attempt was..."
- "That broke because..."
- "So I tried..."
- "Which revealed..."

**Example from Ben Anderson's "Should I Buy Claude a Mac Mini?"**:
> "I am buying Claude a Mac Mini. Or at least, I'm thinking about it."

Opens with uncertainty, invites reader into deliberation rather than presenting conclusion.

### Declarative Thesis (Mark Seemann style)
**Strong opening:**
> Favour Fakes over dynamic mocks.

**Pattern:** State your position immediately, then build evidence

**When to use:**
- You have a strong technical opinion backed by experience
- Arguing against common practice
- Teaching a principled approach

### Anticipate Objections
Address skepticism throughout, not just at the end:
- "You may object that..."
- "Perhaps you're still not convinced..."
- "One might argue..."

**Why it works:** Shows you've thought through counterarguments, builds credibility

**Example:**
> You might think void returns are fine—technically correct, even. I thought so too. Then I tried refactoring.

### Progressive Revelation (Seemann style)
Show the same test with different implementations:
1. Show interface/contract
2. Show correct implementation
3. Show broken implementation
4. Highlight what changed and what broke

**Pattern:** Build understanding through comparison, not explanation

### Define Your Terms
If using potentially ambiguous terms, define them upfront:
- "What I mean by 'encapsulation' is..."
- "When I say 'contract' I'm referring to..."
- "Let's clarify what we mean by..."

**Why it works:** Prevents talking past each other, establishes shared vocabulary

### Contract-Based Reasoning
Frame problems in principles, not convenience:
- Bad: "This approach is easier"
- Good: "This approach maintains encapsulation by..."
- Bad: "Tests run faster"
- Good: "Tests verify contracts, not implementations"

**Pattern:** Ground arguments in fundamental principles, not pragmatic trade-offs

### Four Layers of Context (Behind Genius Ventures style)
Technical stories work across multiple abstraction layers. Don't just describe **what** you built—show the broader context:

**1. Implementation Layer (Product)**
- The technical details and tradeoffs
- "I used a strategy pattern with a registry dispatcher"

**2. Process Layer (Team)**
- How you collaborated, made decisions
- "The team debated whether to normalize to null or handle void"

**3. Purpose Layer (Vision)**
- Why this matters, long-term impact
- "This enables adding regional calculators without refactoring core logic"

**4. Ecosystem Layer (Landscape)**
- How this fits into broader trends, alternatives, history
- "Most calculator libraries handle one region. Multi-region support is rare because..."

**Why it works:** Readers at different levels connect with different layers. Juniors learn from implementation, seniors evaluate architecture, business sees impact.

**Example structure:**
```markdown
### Context: What I Was Building
[Implementation] I built a calculator system with strategy pattern...
[Purpose] This enables scaling to multiple regions...
[Ecosystem] Unlike existing solutions that hardcode regional logic...
```

### Show the Invisible
Technical storytelling reveals what's **not obvious** from the code:

**Show hidden tradeoffs:**
- "I chose X over Y because of constraint Z that's not visible in the commit"
- "This refactoring makes sense only if you know about the upcoming feature..."

**Show unseen connections:**
- "This bug revealed a deeper assumption in our data model"
- "The type error was actually protecting us from a race condition"

**Show alternative paths:**
- "I tried approach A first. It failed because..."
- "Most would use library X here. I didn't because..."

**Pattern:** Make your reasoning visible, not just your results

**Example:**
> The calculator interface looks simple. But that simplicity hides a critical decision: should `null` mean "no result" or "calculation failed"? TypeScript forced me to choose explicitly. The void-to-null refactor wasn't cosmetic—it was clarifying intent for future maintainers.

## Implementation

### Step 1: Read the Draft Completely

```bash
# Read the entire draft first
Read content/drafts/2025-11-02-example.md
```

Note:
- The introduction (auto-generated context)
- Notable features/challenges/evolution listed in comments
- All commit messages at the bottom

### Step 2: Analyze Commit Patterns

Group commits by type:
- **Features**: `feat:`, `add`, `implement`, `create`
- **Fixes**: `fix:`, `bugfix`, `resolve`
- **Refactoring**: `refactor:`, `improve`, `optimize`
- **Docs**: `docs:`, `README`, `documentation`
- **Tests**: `test:`, `spec`, `coverage`

### Step 3: Write Sections Using Evidence

**CRITICAL OUTPUT RULE: Never mention "commits", "git history", "the log", or any meta-analysis in your blog writing. Write as if you're naturally reflecting on your development experience from memory.**

**Context Section:**
- **Start with a hook** - human moment, not technical summary
  - Bad: "This post describes the work on touchepas"
  - Good: "I needed a rent calculator that didn't lie to me"
- **Layer your context** - move from implementation to ecosystem
  - What you built (implementation layer)
  - Why it matters (purpose layer)
  - How it fits the broader landscape (ecosystem layer)
- Use conversational bridges: "Here's what happened...", "I started with..."
- **Avoid assuming business context** not evident in commits
- 2-3 paragraphs

**Example opening (Conversational):**
> I spent October refactoring a calculator system. Not because I wanted to—because TypeScript forced my hand. That void-returning function? It was a type bomb waiting to explode.

**Example opening (Pedagogical):**
> Test-driven development requires fast feedback. The touchepas refactoring demonstrates how the RED-GREEN-REFACTOR cycle surfaces type inconsistencies that static analysis alone might miss.

**Example opening (Contextual - Four Layers):**
> I built a strategy pattern for regional calculators [implementation]. This enables scaling across Belgian regions without refactoring core logic [purpose]. Most calculator libraries hardcode regional rules—multi-region support is rare [ecosystem].

**Challenge Section:**
- **Be honest about what was hard** - not just "here's what I did"
  - "This took longer than it should have"
  - "I went down the wrong path first"
  - "The real problem wasn't what I thought"
- Use fix commits as evidence of problems
- Use refactor commits as evidence of complexity
- Show the **path** to understanding, not just the understanding
- 2-4 paragraphs

**Example (Conversational):**
> The first version worked. Sort of. It passed tests, but I knew it was fragile. The void return type was technically correct—there are cases where no result makes sense. But TypeScript was warning me: "Are you sure about this?" I ignored it. Mistake.

**Example (Pedagogical with Progressive Revelation):**
> The void return type satisfied the compiler. But consider what happens during refactoring: the interface allows void, but clients expect null. This contract mismatch creates a maintenance burden—every caller must handle both cases, even when only one occurs in practice.
>
> Let me show you with the actual tests. First, with void... [then with null]. Notice how the second test clearly signals "no result found" rather than "operation completed with no value."

**Solution Section:**
- Walk through the approach using commit chronology
- **Show the invisible** - reveal reasoning not obvious from code
  - Why you chose X over Y
  - Hidden constraints that influenced decisions
  - Alternative paths you rejected
- Include 1-2 code snippets **if you have repo access** (otherwise describe patterns from commits)
- Connect commits into a narrative arc
- 3-5 paragraphs (with code if available)

**Showing the invisible example:**
```markdown
The registry dispatcher looks straightforward. But that design emerged from
a failed attempt at compile-time dispatch. TypeScript's type system couldn't
handle the dynamic region lookup we needed. Runtime dispatch was the fallback—
and turned out simpler anyway.
```

**Learned Section:**
- Extract lessons from the commit patterns
- Reference specific commits as evidence
- Mention what you'd do differently
- 2-3 paragraphs

### Step 4: Use First-Person Voice

Write as "I built", "I discovered", "I learned" - not "we" or "the developer".

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| **Making unverified assumptions** | Stay grounded in commits. Use obvious context (project name, tech stack) but don't invent user needs or business requirements not shown in commits |
| **Ignoring draft's commit insights** | Use the "Notable features/challenges" section as starting points |
| **Listing commits instead of telling story** | Connect commits with "This led to...", "Which revealed...", "After that..." |
| **Generic code snippets** | Show actual patterns from the codebase, not contrived examples |
| **Third-person narration** | Always use first person: "I implemented" not "The code implements" |
| **Mentioning commits/git in OUTPUT** | NEVER write "the commits show", "git history", or "looking at the log" - write naturally as if recounting from memory |

## Example: Before & After

**Before (Ungrounded Assumption):**
> touchepas is a rent indexation calculator for Belgium. The project needed to calculate rent adjustments based on regional health index data.

**After (Evidence-Based, Natural Voice):**
> I built a calculation system using a strategy pattern. Started with a BrusselsCalculator, then added a registry dispatcher when I realized I'd need to support multiple calculation approaches.

**Before (Listing):**
> First I added the calculator interface. Then I implemented BrusselsCalculator. Then I added tests.

**After (Story Arc, Natural Voice):**
> I started with a calculator interface to define the contract. This forced me to think about return types—which surfaced a void vs null inconsistency that TypeScript caught. Working test-first, the RED-GREEN-REFACTOR cycle kept me honest.

## Red Flags - STOP and Revise

If you find yourself:
- Inventing user needs or business requirements not shown in commits
- Writing "Users need..." without evidence
- Explicitly mentioning "commits", "git history", or "the log shows" **in your blog output**
- Creating fake code examples when you don't have repo access
- Writing in third person
- Writing "The commits show..." or similar meta-analysis **in your blog output**

**Stop. Re-read the commits. Write naturally as if you're recounting from memory, not analyzing logs.**

## Code Snippet Guidelines

**If you have repo access:**
- Include 1-2 real code snippets showing key patterns
- Add context explaining why this code matters

**If you DON'T have repo access:**
- Describe patterns inferred from commit messages
- Example: "I used a strategy pattern with a registry dispatcher..."
- Don't invent code—describe the approach instead
