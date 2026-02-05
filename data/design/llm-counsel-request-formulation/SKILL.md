---
name: LLM Counsel Request Formulation
description: This skill should be used when Claude needs to "formulate a request for external feedback", "craft a question for ChatGPT or Gemini", "structure a code review request", "write an A/B decision query", or needs guidance on how to effectively ask peer LLMs for counsel on architecture, design, or code decisions.
version: 0.1.0
---

# Formulating Effective Requests for External LLM Counsel

Guide for crafting requests that elicit useful, actionable feedback from ChatGPT or Gemini.

## Core Principles

External LLMs give better responses when requests are:
- **Constrained**: A/B choices or ranked lists, not open-ended
- **Contextualized**: Project goals and priorities stated upfront
- **Excellence-framed**: Appeal to craftsmanship, not just correctness
- **Specific**: Concrete code or decisions, not abstract questions

## Request Structure

### Standard Template

```
[Context Block - 2-3 sentences]
[Project type and goals. Key priorities or constraints.]

[Question Block]
[The specific decision, with options if applicable]

[Response Format]
Please provide:
- [A/B recommendation with rationale, OR]
- [Ranked list of approaches with tradeoffs]

[Excellence Framing]
Our goal is ἀρετή. Please bring your 職人気質.
```

### Context Block Patterns

**Security-focused project:**
> This is a financial services API where security and auditability are paramount. We prioritize correctness over convenience.

**Personal tool:**
> This is a personal productivity tool I use daily. Speed, trustworthiness, and low friction are my top priorities.

**Scalability-focused:**
> This is a data pipeline expected to handle 10M events/day. Throughput and reliability matter more than development speed.

**Startup/iteration:**
> This is an early-stage product where we need to move fast and learn. Flexibility to pivot matters more than optimization.

### Question Block Patterns

**Architecture decision (A/B):**
> We need caching for our API responses. Should we use:
> A) Redis (external dependency, but battle-tested)
> B) In-memory LRU cache (simpler, but per-instance)
>
> Our API runs on 3 instances behind a load balancer.

**Design pattern choice:**
> For creating configuration objects with many optional fields, which pattern fits better:
> A) Builder pattern (fluent, explicit)
> B) Functional options (Go idiomatic, extensible)
>
> Here's the current struct: [code]

**Refactoring approach (ranked list):**
> This 800-line file needs splitting. What's the best decomposition?
> [code excerpt showing structure]
>
> Please rank the approaches from most to least recommended.

**Code review (ranked issues):**
> Please review this code and provide a ranked list of corrections and recommendations, from most to least critical.
> [code]

### Response Format Specifications

**For A/B decisions:**
```
Please provide:
- Your recommendation (A or B)
- Key factors that determined your choice
- When you'd choose the other option instead
```

**For ranked lists:**
```
Please provide a ranked list from most to least [critical/recommended/important], with brief rationale for each.
```

**For code review:**
```
Please provide a ranked list of issues from most to least critical, covering:
- Correctness and bugs
- Security concerns
- Performance implications
- Design/architecture
- Code clarity
```

## The Excellence Framing

### Why It Works

The closing line appeals to craftsmanship values that encourage thoughtful, high-quality responses:

> Our goal is ἀρετή. Please bring your 職人気質.

**ἀρετή** (arete): Greek concept of excellence, virtue, living up to one's full potential

**職人気質** (shokunin kishitsu): Japanese craftsman spirit - pride in work, attention to detail, continuous improvement

This framing signals you want thoughtful counsel, not quick answers.

### Variations

For different tones:

**Formal:**
> We aim for engineering excellence and long-term maintainability.

**Direct:**
> Give me your honest assessment. I want craft, not compromise.

**Collaborative:**
> Help me think through this carefully. Quality matters more than speed.

## Code Review Requests

### Scope Limits

- **Maximum 10 files** per request
- Keep total code under ~2000 lines if possible
- Focus on related files, not scattered snippets

### Structure for Code Reviews

```
[Context]
This is [project type] where [key priorities].

Please review the following code and provide a ranked list of corrections and recommendations.

Our goal is ἀρετή. Please bring your 職人気質.

---

**File 1: path/to/file.go**
```go
[contents]
```

**File 2: path/to/other.go**
```go
[contents]
```

---

Focus areas:
- Correctness and potential bugs
- Security considerations
- Performance implications
- Design clarity
- Idiomatic usage
```

### What to Include

- Full file contents (not snippets) when reviewing design
- Relevant type definitions referenced by the code
- Brief note on what the code does if not obvious

### What to Exclude

- Generated code
- Test files (unless reviewing test quality specifically)
- Configuration files (unless that's the focus)
- Dependencies or vendor code

## Anti-Patterns

### DON'T: Open-ended questions

❌ "What do you think about this code?"
❌ "How should I design this system?"
❌ "Any suggestions for improvement?"

### DO: Constrained questions

✅ "Should we use approach A or B? Here are the tradeoffs I see..."
✅ "Rank these three architectural options for our use case..."
✅ "What are the top 3 issues with this code, ranked by severity?"

### DON'T: Missing context

❌ "Review this function: [code]"

### DO: Provide context

✅ "This is a security-critical auth handler. Review for vulnerabilities: [code]"

### DON'T: Too much scope

❌ "Review our entire codebase"
❌ [20 files attached]

### DO: Focused scope

✅ "Review these 3 related handlers for consistency and correctness"

## Service Selection Guidance

**ChatGPT** tends to excel at:
- Implementation details and code generation
- Practical, hands-on advice
- Step-by-step explanations

**Gemini** tends to excel at:
- Architectural reasoning
- Conceptual tradeoff analysis
- Broader design perspectives

Choose based on whether the question is more implementation-focused (ChatGPT) or architecture-focused (Gemini).

## Quick Reference

| Element | Pattern |
|---------|---------|
| Context | 2-3 sentences: project type + priorities |
| Question | Specific decision with options |
| Format | A/B recommendation OR ranked list |
| Closing | Excellence framing (ἀρετή, 職人気質) |
| Code limit | Max 10 files, ~2000 lines |
