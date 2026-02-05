---
name: constitution-reader
description: Read and summarize constitution principles for the AI-Native Robotics Textbook project. Use when checking project rules, validating compliance, or understanding constraints.
allowed-tools: Read, Grep
---

# Constitution Reader

## Instructions

When this skill is invoked, help the user understand the project constitution:

1. Read the constitution file at `.specify/memory/constitution.md`
2. Summarize the relevant principles based on the user's query
3. Highlight any constraints or requirements that apply
4. Reference specific sections when providing guidance

## Key Sections to Reference

- **Section III**: Strict Technical Stack (allowed frameworks and libraries)
- **Section IV**: Pedagogical Layers (L1-L5 definitions)
- **Section VII**: Content Agents Specification
- **Section VIII**: Software-Building Agents Specification
- **Section IX**: Quality & Verification requirements

## Examples

**User asks**: "What tech stack is allowed for the backend?"
**Response**: Reference Section III - Only FastAPI, Qdrant, BetterAuth are permitted.

**User asks**: "How should content be structured?"
**Response**: Reference Section VII - Content must include "Try With AI" final section.

## Reference

For the full constitution, see [reference.md](reference.md).
