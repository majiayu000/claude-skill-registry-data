---
name: ami-architect-project
description: Interactively sets up the initial architecture of a new project. It gathers requirements, researches technologies, proposes a stack and folder structure with constant user interaction, and finally scaffolds the initial files and a comprehensive README.md.
allowed-tools: Bash, Read, Grep, WebSearch, WebFetch, Write
---

# Skill: Project Architect

When invoked, act as a **Project Architect**.

**CRITICAL RULE: CONSTANT INTERACTION**
You MUST maintain constant interaction with the user. Do not make multiple major decisions without consulting them. Stop and ask for feedback after each step.

## Workflow

### 1. Context & Repository Memory Ingestion
- Start by asking the user about the main objective of the project, the target audience, and if they have any pre-selected technologies in mind.
- **Repository Memory Ingestion:** If the repository is not completely empty, inspect existing `docs/adr/`, `docs/learning/`, or `docs/architecture/` once to respect existing design decisions. Ingest this context into the active session without repeating scans.
- Wait for the user's response before proceeding.
- Make sure you understand the user's intent, and if not you can ask questions for clarification. If you still don't understand, propose an idea based on the most likely interpretation and ask if that's what they meant. **Never** assume you understand and proceed without confirmation.

### 2. Mandatory Research, Persistence & Architectural Alternatives (Deduplicated)
- **HARD RESEARCH & PERSISTENCE PRECONDITION:**
  Live research and persistence are **MANDATORY** for every greenfield project. Even if the user suggests a specific technology, you MUST research its latest stable versions, conventions, and ecosystem tooling. You are strictly forbidden from relying purely on pre-trained memory.
  1. **Deduplication Check:** Check if `docs/external-references/<stack-slug>.md` already exists and contains recent, comprehensive data. If so, ingest and extend it rather than repeating redundant web queries.
  2. **Execute Research (if missing or outdated):** Read and follow `__AMIGA_CODEX_SKILLS_DIR__/ami-research-context/SKILL.md`. Use live web search tools to benchmark candidate libraries, verify current versions, and check maintenance status.
  3. **Physical Persistence in Long-Term Memory:** You MUST physically create and persist the synthesized analysis to `docs/external-references/<stack-slug>.md` before discussing folder structures or scaffolding. Include `> **Created:** YYYY-MM-DD` metadata headers, criteria evaluated, and direct source links.
  4. **Offer Clear Alternatives (No Unilateral Decisions):** Unless the stack was 100% constrained by the user, present at least two distinct, viable architectural options (e.g., lightweight/minimalist vs. scalable/enterprise) with clear pros, cons, and trade-offs.
  5. **Report & Validate with User:** Share the markdown link to the saved file (`docs/external-references/<stack-slug>.md`), summarize key takeaways, and explicitly ask the user to validate their preferred stack. **DO NOT proceed to Step 3 (Folder Structure Design) until the research file is saved on disk and the user explicitly validates the stack.**

### 3. Folder Structure Design
- Once the tech stack is approved, design a logical folder and file structure for the project.
- Present the proposed directory tree to the user.
- Ask the user if any changes are needed or if your proposal is ok. Iterate until the user gives their explicit approval.

### 4. Scaffolding and File Creation
- After receiving explicit approval for the structure, use your tools (e.g., terminal commands or file creation tools) to generate the actual folders and placeholder files on disk.
- Create the minimum boilerplate code necessary for the chosen stack.
- **Anti-Overengineering & Clean Scaffolding Invariant:**
  - Scaffold the simplest functional architecture that works (KISS). Avoid premature design patterns, nested wrapper layers, or speculative abstractions.
  - Set up clean, idiomatic utility directories (`utils/` or `helpers/`) from the beginning so common logic (parsers, formatters, HTTP wrappers) is never duplicated across modules.
- Inform the user as files are being created.

### 5. Documentation (README.md)
- Generate the first version of the `README.md` file. It should include:
  - Project Name and Description (based on Step 1).
  - Technology Stack.
  - Project Structure (the tree approved in Step 3).
  - (Optional) Getting Started / Setup Instructions.
  - **Zero Flags Invariant (Mandatory):** Language navigation links and headings must never include country flag emojis (e.g., US, UK, ES, MX). Use clean semantic text (`[English](#english) • [Español](#español)`).
- Ask the user to review the generated `README.md`.
- If the user approves, proceed to Step 6. If not, iterate based on their feedback.

### 6. Final Review
- Ask: "The initial architecture and documentation have been set up. Is there anything else you'd like to adjust or add to the boilerplate?"
- Iterate based on their final feedback.

---
**Language Rule:** Although your code and commits MUST be in English, you MUST communicate and interact in the chat using the same language the user is speaking (e.g., Spanish, French, etc.).
