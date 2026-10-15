---
name: interview
description: "Interview users to convert rough ideas into structured specs. Use before starting non-trivial features."
context: fork
globs: []
alwaysApply: false
---

# Interview — Idea to Spec

Use this skill to transform a rough idea into a structured spec before implementation. A 5-minute interview prevents hours of rework.

---

## Usage

Invoke via the `/sketch` command:

```
/sketch Add a notification system so users get alerted when their order ships
```

Or trigger Athena directly:

```
@athena: Interview me about this feature: real-time dashboard for agent cost tracking
```

---

## Interview Protocol

### Phase 1: Discover (3–5 questions, one at a time)

Ask questions in this priority order, stopping after you have enough clarity:

1. **Scope** — "What's the minimum viable version of this feature?"
2. **Users** — "Who uses this and what's their primary workflow?"
3. **Constraints** — "Are there tech, time, or integration constraints?"
4. **Success criteria** — "How will you know this is working correctly?"
5. **Non-goals** — "What should this explicitly NOT do?"

**Rules:**
- Ask **one question at a time** — never batch questions
- Wait for the answer before asking the next
- Stop asking when you have answers to at least 3 questions
- If the user is unsure, offer 2–3 concrete options to choose from

### Phase 2: Confirm Understanding

Before writing the spec, summarize your understanding in 2–3 sentences and ask: "Does this match what you have in mind, or did I miss anything?"

### Phase 3: Write the Spec

Produce the spec only after getting confirmation.

---

## Spec Output Format

```markdown
# Feature Spec: <Feature Name>

**Date:** YYYY-MM-DD
**Status:** Draft

## Overview
<2–3 sentence description of the feature and its purpose>

## Goals
- <Goal 1>
- <Goal 2>
- <Goal 3>

## Non-Goals
- <What this feature explicitly does NOT cover>
- <Scope boundary 1>
- <Scope boundary 2>

## Functional Requirements

### Must Have (MVP)
- [ ] <Requirement 1>
- [ ] <Requirement 2>
- [ ] <Requirement 3>

### Should Have (v1.1)
- [ ] <Requirement 4>

### Won't Have (out of scope)
- <Explicitly excluded>

## Technical Constraints
- **Stack:** <relevant tech>
- **Integrations:** <APIs, services>
- **Performance:** <latency, throughput requirements if any>
- **Security:** <auth, data sensitivity>

## Success Criteria
- [ ] <Measurable outcome 1>
- [ ] <Measurable outcome 2>

## Open Questions
- [ ] <Unresolved decision 1>
- [ ] <Unresolved decision 2>

## Suggested Implementation Phases
1. **Phase 1:** <database/schema>
2. **Phase 2:** <backend API>
3. **Phase 3:** <frontend>
```

---

## After the Spec

Hand off to Athena or Zeus with the completed spec:

```
@athena: Use this spec to create a TDD implementation plan:
[paste spec]
```

Or for immediate orchestration:

```
@zeus: Implement this feature based on the spec:
[paste spec]
```

---

## Tips for Good Interviews

- **Anchor on user value** — every requirement should trace to a user need
- **Flag ambiguity early** — if a requirement is unclear, mark it as an Open Question rather than guessing
- **Keep MVP small** — the first version should be deliverable in one session
- **Distinguish wants from needs** — "should have" vs "must have" prevents scope creep
