---
allowed-tools: AskUserQuestion, Write
argument-hint:
    - instructions
description: Interview user in-depth to create a detailed spec. Use when the user wants to brainstorm a feature, plan an implementation, or needs help thinking through requirements. Triggers on requests like "interview me about", "help me spec out", "let's plan", or explicit /interview calls.
metadata:
    targets:
        - antigravity
name: interview_KM
user-invocable: true
---
# Interview Skill

## Purpose
Conduct a thorough, in-depth interview with the user to extract detailed requirements and create a comprehensive specification document.

## Instructions

Follow the user instructions and interview me in detail using the AskUserQuestion tool about literally anything:

- Technical implementation details
- UI & UX considerations
- Edge cases and error handling
- Concerns and potential issues
- Tradeoffs and alternatives
- Performance requirements
- Security considerations
- Integration points
- Data models and structures
- User flows and interactions

**Important guidelines:**
- Make sure the questions are not obvious - dig deep into the details
- Be very in-depth and thorough
- Continue interviewing continually until the topic is fully explored
- Ask follow-up questions based on previous answers
- Challenge assumptions and probe for edge cases
- Don't accept vague answers - ask for specifics

## Output

When the interview is complete, write a detailed spec file that captures:

1. **Overview** - What we're building and why
2. **Requirements** - Functional and non-functional requirements
3. **Technical Design** - Architecture, data models, APIs
4. **UI/UX** - User interface and experience details
5. **Edge Cases** - Error handling and edge case behavior
6. **Tradeoffs** - Decisions made and alternatives considered
7. **Open Questions** - Any remaining uncertainties

Write the spec to a file in the current directory (e.g., `spec.md` or `<feature-name>-spec.md`).

<instructions>$ARGUMENTS</instructions>
