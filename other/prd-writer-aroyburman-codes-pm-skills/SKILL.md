---
name: prd-writer
description: "Generate structured Product Requirements Documents (PRDs) from a feature brief, idea, or problem statement. Covers problem definition, user stories, requirements, success metrics, and launch plan. Adapts to AI/ML product contexts."
argument-hint: "[feature idea or problem statement]"
---

# PRD Writer Skill

Generate a complete, structured PRD from a feature idea, problem statement, or brief description.

## When to Use
- User needs to write a PRD for a new feature
- User has an idea and wants it turned into a structured spec
- User says `/prd-writer` followed by a feature description
- Any time a product requirement needs to be documented

## Framework: PRD Structure

### 1. Overview
- **Feature name**: Clear, descriptive name
- **Author**: [to be filled]
- **Date**: Current date
- **Status**: Draft / In Review / Approved
- **One-liner**: What this feature does in one sentence

### 2. Problem Statement
- **What problem are we solving?** Describe the user pain point or business need
- **Who has this problem?** Primary user segment
- **How big is this problem?** Estimated impact (users affected, frequency, severity)
- **Why solve it now?** Urgency, strategic alignment, competitive pressure

### 3. Goals & Non-Goals

**Goals:**
- 3-5 specific, measurable goals this feature should achieve
- Each goal maps to a user need or business objective

**Non-Goals:**
- Explicitly list what this feature will NOT do
- Prevents scope creep and sets expectations

### 4. User Stories
Write 3-5 user stories in the format:
> As a [user type], I want to [action] so that [benefit].

Include acceptance criteria for each:
- Given [context], when [action], then [expected result]

### 5. Detailed Requirements

**Functional Requirements:**
| ID | Requirement | Priority (P0/P1/P2) | Notes |
|----|------------|---------------------|-------|
| FR-1 | | | |
| FR-2 | | | |

**Non-Functional Requirements:**
- Performance: Latency, throughput, scalability targets
- Security: Auth, data handling, compliance
- Accessibility: WCAG level, screen reader support
- Reliability: Uptime, error handling, graceful degradation

**For AI/ML features, also include:**
- Model requirements: Accuracy, latency, cost per inference
- Data requirements: Training data, eval data, data pipeline
- Safety requirements: Content policy, guardrails, fallback behavior
- Eval criteria: How model quality will be measured

### 6. UX & Design
- **User flow**: Step-by-step walkthrough of the primary flow
- **Key screens/states**: Describe the main UI states (loading, empty, error, success)
- **Edge cases**: What happens when things go wrong?
- **Design references**: Links to mockups/wireframes (placeholder)

### 7. Technical Approach
- **Architecture**: High-level system design
- **Dependencies**: APIs, services, teams needed
- **Data model**: Key entities and relationships
- **Migration**: Any data migration or backward compatibility concerns

### 8. Success Metrics
- **Primary metric**: The one number that tells us this feature worked
- **Secondary metrics** (3-4): Supporting indicators
- **Guardrail metrics** (2-3): What must NOT regress
- **Measurement plan**: How and when to measure

### 9. Launch Plan
- **Rollout strategy**: Feature flag → internal → beta → GA
- **Launch criteria**: What must be true before each stage
- **Rollback plan**: How to revert if something goes wrong
- **Communication**: Who needs to know and when

### 10. Open Questions
- List unresolved questions that need stakeholder input
- Include who should answer each question

## Output Format
Generate as clean markdown, ready to paste into Notion, Confluence, Google Docs, or any doc tool. Use tables for requirements. Be specific and actionable — avoid vague language.

## Research-First Workflow
1. **Research** — Search for comparable features from competitors, best practices, and relevant technical approaches.
2. **Generate** the complete PRD following the structure above.
3. **Flag** open questions and assumptions that need validation.
