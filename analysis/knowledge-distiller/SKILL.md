---
name: knowledge-distiller
description: Analyzes conversation sessions to extract key insights, decisions, and technical details, then saves them to the knowledge base. Use this skill when asked to "summarize what I learned today," "record key points from recent sessions," or "sync current project context to long-term memory."
---

# Knowledge Distiller

This skill provides a systematic workflow for retrieving conversation sessions, extracting valuable information (entities, relationships, and insights), and persisting them in the Knowledge Base. It transforms transient dialogue into structured, long-term memory.

## Prerequisites

- The agent session must have the optional `history` and `knowledge` builtin services enabled. If tool calls fail with a "not enabled" error, enable them via Assistants settings or `agent__updateAgent` before running this workflow.
- Runtime tool names use the `server__tool` format shown below (for example `history__listSessions`, `knowledge__recordKnowledge`). Match names from the session tool list.

## Execution Triggers

Use this skill when the user says:
- "Summarize my learnings from today's sessions."
- "Extract important technical decisions from my recent work."
- "Update the knowledge base with the context we just discussed."
- "Keep track of the project preferences established in this session."

## Workflow

### 1. Define the Analysis Scope
Determine which sessions to analyze based on the user's request:
- **Temporal**: Today (from 00:00:00 to 23:59:59 ISO-8601).
- **Recent**: The last N sessions from the history.
- **Current**: Focus only on the active or most recent session.

Use `history__listSessions` to retrieve the relevant `sessionId` list if the scope is broader than the current session.

### 2. Context Preview & Filtering
For each target session:
1. Use `history__readSession` to preview message summaries.
2. Filter for high-value content such as:
   - Architecture decisions or design patterns discussed.
   - Specific error causes and their confirmed resolutions.
   - Library versions, API endpoints, or configuration keys.
   - Explicit user preferences or project-specific naming conventions.

### 3. Deep Extraction (Distillation)
If a session contains valuable information, use `history__readMessage` for full detail.
Identify and structure the following components:
- **Entities**: Technologies (e.g., "Tauri 2.0"), Projects (e.g., "LibrAgent"), or Concepts.
- **Relationships**: Link entities (e.g., "LibrAgent" `USES` "SeaORM").
- **Content**: A concise, stand-alone summary of the knowledge.

### 4. Structured Recording
Use the `knowledge__recordKnowledge` tool to persist the findings:
- **content**: The distilled summary.
- **entities/relationships**: Structured data for the graph.
- **source**: Reference the source `sessionId` or date for traceability.
- **tags**: Include `["distilled", "auto-knowledge", "context-sync"]`.

## Safety & Efficiency
- **De-duplication**: Before recording, use `knowledge__searchKnowledge` to check if similar knowledge already exists to avoid redundant entries.
- **Relevance**: Skip sessions that are purely social or don't contain reusable technical/project context.

## References

- [Extraction patterns](references/extraction-patterns.md)
- [Knowledge schema](references/knowledge-schema.md)
