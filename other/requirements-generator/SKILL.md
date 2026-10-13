---
name: requirements-generator
description: Generates structured requirements documents with functional and non-functional requirements, Gherkin acceptance criteria, edge cases, and out-of-scope items.
argument-hint: "[--interview] [feature description]"
allowed-tools: Read, Write, Glob, Grep
---

# Requirements Generator

Take a project idea, feature description, or user story and generate a structured requirements document with functional requirements, non-functional requirements, Gherkin acceptance criteria, edge cases, and out-of-scope items.

## Instructions

**Two modes:**
- **Description mode** (default): user provides a free-form description or pastes a Jira/Confluence URL. Claude generates requirements from that.
- **Interview mode** (`/requirements-generator --interview`): Claude asks a structured set of questions one at a time, then generates requirements from the answers.

1. **Gather input.** Ask the user what they want to build if no description has been provided. Accept any of:
   - A pasted feature description or user story
   - A Jira ticket URL or Confluence page URL (read via available MCP tools if present)
   - A brief verbal description of the feature

   Prompt: _"Describe the feature or system you want to build. Include the user need it addresses and any known constraints."_

   If the user invoked with `--interview`, skip this prompt and proceed to the **Interview Mode** section below instead.

2. **Understand the existing codebase** (if one exists). Use Glob on `*` to detect the project structure. Read `package.json`, `pyproject.toml`, or `go.mod` to identify the tech stack. Read 3–5 representative files from `src/` or `app/` — entry points first (`index.*`, `main.*`, `app.*`), then one route/handler file and one model/schema file — to understand patterns and conventions. Do not read the whole source tree. This ensures requirements fit what already exists.

3. **Check for existing requirements.** Use Glob on `docs/requirements/**/*.md`. If matching files exist, read them to avoid duplicating requirements already captured. Note any related requirements in the new document.

4. **Determine the feature name.** Derive a kebab-case feature name from the description (e.g., "user authentication" → `user-authentication`). This becomes the output filename.

5. **Generate the requirements document** with the following sections:

   ### Overview
   One paragraph summarizing what is being built, the user need it addresses, and why it matters.

   ### Stakeholders

   A table of who uses this feature and what they need from it.

   | Stakeholder | Role | Primary Need |
   |-------------|------|-------------|
   | End User | ... | ... |

   ### Functional Requirements
   Numbered list using the prefix `FR-NNN` (e.g., FR-001, FR-002). Each requirement must be:
   - Specific and testable
   - Implementation-agnostic (describe _what_, not _how_)
   - Written in the form: "The system shall..."

   ### Non-Functional Requirements
   Cover all four dimensions:
   - **Performance**: specific response time targets (e.g., "API responses under 200ms at p95")
   - **Security**: authentication requirements, data sensitivity classification, encryption requirements
   - **Accessibility**: WCAG AA compliance, keyboard navigation, screen reader support
   - **Scalability**: expected concurrent users, request volume, data growth projections

   ### Acceptance Criteria
   Gherkin format (Given/When/Then) — one scenario per key functional requirement. Use this format exactly:

   ```gherkin
   Scenario: <short description>
     Given <precondition>
     And <additional precondition if needed>
     When <action>
     Then <expected outcome>
     And <additional outcome if needed>
   ```

   ### Edge Cases & Error Scenarios
   Bulleted list covering:
   - Invalid or malformed input
   - System failures (database down, third-party API timeout)
   - Concurrent access and race conditions
   - Boundary conditions (empty state, maximum limits)
   - Unauthorized access attempts

   ### Out of Scope
   Explicitly list what this feature does NOT include. This prevents scope creep during implementation. Be specific.

   ### Assumptions
   List any assumptions made during requirements generation. For each:
   - State the assumption clearly
   - Note what would change if the assumption is wrong

   ### Open Questions
   List questions that require stakeholder input before implementation can begin. For each question, note:
   - Who is the right person to answer it
   - What the impact is if it is not answered before development starts

6. **Write the document.** Ensure `docs/requirements/` exists (it may need to be created). Use Write to save the document to `docs/requirements/<feature-name>-requirements.md`.

7. **Offer Jira/Confluence integration** (if MCP tools for Atlassian are available in the session). Ask: _"Would you like me to publish this to Confluence or create a Jira epic?"_ If yes, use the available MCP tools to do so.

8. **Confirm completion.** Tell the user the file path, how many functional requirements were generated, and how many acceptance criteria scenarios were written.

## Interview Mode

When invoked with `--interview`, conduct a structured interview by asking each question below one at a time. Wait for the user's full answer before proceeding to the next question. Do not ask multiple questions at once.

1. **Who is the primary user?** "Describe the person or system that will use this feature. What is their role, technical level, and what are they trying to accomplish?"

2. **What problem does this solve?** "What is the user currently unable to do, or what pain point does this address? What happens today without this feature?"

3. **What does success look like?** "How will you know this feature is working correctly? What would a user be able to do that they couldn't before?"

4. **What are the constraints?** "Are there technology choices already made (language, framework, cloud provider)? Any performance requirements? Any compliance or regulatory constraints (GDPR, HIPAA, SOC2)?"

5. **What is explicitly out of scope?** "What are you deliberately NOT building in this version? What might people assume is included but isn't?"

6. **What could go wrong?** "What edge cases or error scenarios do you anticipate? What happens if the user provides invalid input? What if a dependency is unavailable?"

7. **Who else is affected?** "Are there other systems, teams, or users impacted by this change? Any backwards compatibility concerns?"

After collecting all answers, generate the full requirements document using the same format as description mode (FR-NNN requirements, NFRs, Gherkin scenarios, etc.), grounded in the interview answers. Include an **Interview Summary** section at the very top of the generated document (before Overview) that captures each answer in 1–2 sentences.

```markdown
## Interview Summary

**Primary user:** ...
**Problem being solved:** ...
**Success criteria:** ...
**Constraints:** ...
**Out of scope:** ...
**Risk areas:** ...
**Other affected parties:** ...
```

Then continue with the standard sections (Overview, Stakeholders, Functional Requirements, etc.) as defined in the Output Format Reference.

## Output Format Reference

```markdown
# Requirements: <Feature Name>

**Version**: 1.0
**Date**: <today's date>
**Status**: Draft

---

## Overview
...

## Stakeholders
| Stakeholder | Role | Primary Need |
...

## Functional Requirements

**FR-001**: The system shall...
**FR-002**: The system shall...

## Non-Functional Requirements

### Performance
...

### Security
...

### Accessibility
...

### Scalability
...

## Acceptance Criteria

```gherkin
Scenario: ...
  Given ...
  When ...
  Then ...
```

## Edge Cases & Error Scenarios
- ...

## Out of Scope
- ...

## Assumptions
- ...

## Open Questions
- ...
```
