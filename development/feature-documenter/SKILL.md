---
name: feature-documenter
description: |
  Create clear feature documentation for non-professional developers. Use PROACTIVELY when documenting new features, significant code changes, creating technical specifications, or when a feature isn't covered in the original project spec. Triggers on requests like "document this feature", "create feature docs", "write technical specification", "document these changes", or any request to explain what code does for future reference.

  Invoke with: /document-feature, /document-feature-simple, /document-feature-full, or say "use the feature-documenter skill to..."
---

# Feature Documenter

Create comprehensive feature documentation that helps non-professional developers understand and maintain code.

## Design Philosophy

### Documentation as Future Kindness

Every line of documentation is a gift to your future self. Six months from now, you will not remember why you structured the API that way or what edge case the validation handles. Documentation is not overhead; it is insurance against amnesia.

### The Non-Developer Audience

This skill creates documentation for "non-professional developers" — people who can code but may not have deep context on the codebase. This means:
- Explain the "why" before the "what"
- Assume familiarity with programming, not with THIS code
- Prefer concrete examples over abstract descriptions

### Living Documents

Feature documentation is not a monument. It is a map. Maps get updated when the territory changes. If the code changes and the documentation doesn't, the documentation becomes a lie.

### Progressive Disclosure

Start with what people need most. Overview first, then details. A reader should be able to understand the feature at three levels:
1. **Skim:** What does this do? (30 seconds)
2. **Read:** How does it work? (5 minutes)
3. **Study:** How do I modify it? (30 minutes)

---

## Anti-Patterns: Documentation That Fails

### The Code Comment Copier
**Symptom:** Documentation that just repeats what the code already says.
**Problem:** `// increments counter` is not documentation. It is a waste of bytes.
**Solution:** Explain WHY the counter is incremented, WHEN it matters, and WHAT breaks if it doesn't.

### The Jargon Dump
**Symptom:** "The middleware intercepts the flux capacitor to hydrate the Redux store."
**Problem:** This helps no one who doesn't already understand. Documentation is for learners.
**Solution:** Start with plain language. Introduce jargon only when necessary, with definitions.

### The Obsolete Artifact
**Symptom:** Documentation describing a feature that was refactored six months ago.
**Problem:** Wrong documentation is worse than no documentation. It actively misleads.
**Solution:** Include a "Last Verified" date. Set calendar reminders to review.

### The Reference Manual
**Symptom:** Complete API documentation but zero explanation of how to USE the API.
**Problem:** Readers can see WHAT functions exist. They can't see HOW to combine them.
**Solution:** Include at least one complete example showing a real use case end-to-end.

### The Orphan Document
**Symptom:** Documentation that exists but nobody can find it.
**Problem:** Undiscoverable documentation might as well not exist.
**Solution:** Link from code comments. Add to README. Include in onboarding.

---

## Documentation Style Selection

Choose based on audience and purpose:

### Style A: Narrative
- **When:** Explaining complex systems, onboarding new developers
- **Format:** Prose with sections, reads like a story
- **Example:** Architecture Decision Records (ADRs)
- **Strength:** Context and reasoning preserved

### Style B: Reference
- **When:** API documentation, configuration options
- **Format:** Tables, lists, specifications
- **Example:** OpenAPI/Swagger docs
- **Strength:** Quick lookup, comprehensive coverage

### Style C: Tutorial
- **When:** Teaching how to accomplish a specific task
- **Format:** Numbered steps, expected outcomes
- **Example:** "How to add a new endpoint"
- **Strength:** Actionable, verifiable

### Style D: Explanation
- **When:** Answering "why" questions, design decisions
- **Format:** Problem/solution structure, trade-off discussion
- **Example:** "Why we chose PostgreSQL"
- **Strength:** Preserves institutional knowledge

---

## Workflow

1. **Determine template complexity**
   - Quick overview or simple feature? → Use simplified template (see `references/template-simple.md`)
   - Detailed specification or complex feature? → Use comprehensive template (see `references/template-comprehensive.md`)

2. **Gather context before documenting**
   - Check `./docs/system-design/` for existing specifications
   - Search for related GitHub issues or requirements documents
   - Use Grep/Glob to find related components in the codebase
   - Review existing feature documentation for consistency

3. **Create documentation**
   - Start with core sections: Problem Statement, Solution Overview, Core Components
   - Expand progressively as the feature develops
   - Save to project's `/docs` or `.claude/docs` directory

## Template Selection Guide

**Use simplified template when:**
- Documenting a small, self-contained feature
- Creating quick reference documentation
- Time is limited and basic coverage is sufficient
- The feature has minimal dependencies

**Use comprehensive template when:**
- Documenting complex features with multiple components
- Creating specifications for features spanning multiple systems
- Documentation will be referenced by multiple team members
- The feature has significant architectural implications
- Risk assessment and testing strategies are needed

## Key Principles

- Write for developers who may not have context on the codebase
- Focus on the "why" as much as the "what"
- Include concrete examples and test scenarios
- Keep documentation as living documents—update as features evolve
- Use clear, straightforward language without unnecessary jargon

---

## External Resources

- **Diátaxis Framework:** [Documentation structure methodology](https://diataxis.fr/) — Tutorials, how-tos, explanations, reference
- **Write the Docs:** [Community best practices](https://www.writethedocs.org/guide/) — Technical documentation guidance
- **Google Developer Style Guide:** [Technical writing standards](https://developers.google.com/style) — Industry-standard conventions
- **ADR GitHub Repo:** [Architecture Decision Records](https://adr.github.io/) — Template for capturing design decisions

---

## Your Mission

You are not writing documentation. You are building a bridge between the developer who wrote the code and the developer who will maintain it. Often, these are the same person separated by time.

Every feature you document is a conversation with the future. Make it worth having.
