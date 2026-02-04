---
name: blog-topic-research
description: |
  Validate topic uniqueness and identify unique angles before writing. Prevents generic content and helps find your specific value.
  Trigger phrases: "topic research", "validate topic", "should I write", "is this unique", "research topic", "check topic"
allowed-tools: Read, Grep, Glob, WebSearch
---

# Blog Topic Research

## When to Use

Trigger when:
- User mentions wanting to write about a topic
- User asks "should I write about X?"
- Before running blog-scaffolding
- User wants to validate an idea

## Purpose

Prevent writing generic content by:
1. Checking what already exists on the topic
2. Identifying what's been covered well by others
3. Finding gaps and unique angles
4. Validating the topic is worth YOUR time

## Research Process

### 1. Internal Search First

Check if you've already written about this:
- Search existing blog posts in `content/en/blog/`
- Search drafts in `content/en/drafts/`
- Look for related tags

**Ask:** "Have you already covered this? If so, is this a follow-up or rehash?"

### 2. External Landscape

Use WebSearch to understand what exists:
- What's the common narrative on this topic?
- What angles are already covered well?
- What gaps exist in existing coverage?
- Who has authority on this topic already?

**Focus:** Not comprehensive research - just enough to understand the landscape.

### 3. Find YOUR Angle

This is the critical part. Ask:
- What's YOUR specific experience with this?
- What problem did YOU encounter that others might not discuss?
- What did YOU learn that contradicts common advice?
- What unique implementation/approach do YOU have?

**Red flags:**
- "I think this would be interesting" (but no personal experience)
- "People should know about X" (but you haven't used it)
- "This is a trending topic" (but you have nothing unique to add)

**Green flags:**
- "I built X and discovered Y"
- "Everyone says X but I found Y"
- "I tried the common solution and it failed because Z"
- "Here's my implementation that handles edge case W"

### 4. Unique Value Assessment

Compare what exists vs. what you can offer:

**Proceed if:**
- You have hands-on experience others don't discuss
- You found problems with common solutions
- You built something that solves a gap
- Your perspective adds genuine value

**Don't proceed if:**
- You'd just be summarizing others' work
- You haven't actually tried it yourself
- The topic is well-covered and you have nothing new
- You're writing it because you "should" not because you experienced it

## Response Format

Present findings conversationally:

```
I searched for existing content on [topic]. Here's what I found:

**Already well-covered:**
- [Common angle 1 with examples]
- [Common angle 2 with examples]

**Potential unique angles from your experience:**
- [Your specific implementation/discovery]
- [Edge case you encountered]
- [Contrarian finding]

**Recommendation:**
[Proceed with unique angle] OR [This might be too generic - consider X instead]

What's your specific experience with this that would add value?
```

## Integration with Other Skills

**Before blog-scaffolding:**
- Topic research validates the idea
- Scaffolding uses the unique angle to structure the post

**During scaffolding conversation:**
- Reference the unique angle identified
- Push for personal experience on that specific angle
- Avoid generic content based on research gaps

## Anti-patterns

**Don't:**
- Write the post for them based on research
- Accept "I think people should know" without experience
- Do comprehensive research that belongs in the post itself
- Approve topics just because they're trending

**Do:**
- Surface what already exists
- Push for personal, specific experience
- Validate uniqueness before investing in writing
- Suggest pivoting if the angle isn't unique enough

## Examples

### Good Validation

**Topic:** "Building a custom deployment script for X"

**Research findings:**
- Generic tutorials exist (common approach Y)
- Manual configuration patterns covered
- No automation examples found

**User's unique angle:**
- Built automated solution that handles edge case Z
- Implements pattern nobody else discusses
- Integrates with tool W in a novel way
- Has battle scars from production failures

**Recommendation:** ✅ Proceed - implementation details and lessons learned are unique

### Bad Validation

**Topic:** "Getting started with popular tool X"

**Research findings:**
- Official docs cover this extensively
- Multiple tutorials exist
- Getting started guides are thorough

**User's unique angle:**
- "I think people should know about X"
- "It's a cool tool"
- (No specific experience or problems encountered)

**Recommendation:** ❌ Don't proceed - this would be generic. Unless you have specific daily workflow experience, unique integration challenges, or discovered non-obvious problems.

## Key Principle

**The blog exists to share experience, not summarize knowledge.**

If you haven't lived it, struggled with it, built it, or learned something surprising about it - it's not ready to be a post yet.
