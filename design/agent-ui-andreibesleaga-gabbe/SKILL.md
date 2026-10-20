---
name: agent-ui
description: "Build specialized user interfaces for interacting with Agents. Use when: build agent ui, create tracing dashboard, implement agent front-end."
license: CC-BY-SA-4.0
metadata:
  source: "agents/skills/ai/agent-ui.skill.md"
  tags: "ai"
  core: "false"
  context_cost: "low"
---
# agent-ui

## Goal
Create specialized, responsive, and intuitive UI elements for tracing, visualizing, and interacting with AI agents.

## Steps
1. **Component Design**: Design UI components (e.g., using ShadCN) to visualize agent thoughts, tools, and actions.
2. **State Connection**: Wire components to the backend agent state or streaming endpoints.
3. **UX Enhancement**: Add micro-animations to indicate agent "thinking" or "executing" states.
4. **Verification**: Verify that the UI flawlessly parses and renders unstructured or partially streamed markdown / JSON.

## Security & Guardrails

### 1. Skill Security
- **XSS Prevention**: Vigorously encode all agent output before rendering it in the UI, as LLM responses can contain malicious payloads.
- **Markdown Sandbox**: Ensure the markdown parser disables executable scripts or insecure HTML tags.

### 2. System Integration Security
- **Access Control**: Hide administrative agent actions (e.g., "approve PR", "deploy") behind rigorous user authentication/RBAC.
- **Secret Masking**: The UI must automatically detect and mask sensitive data (like API keys) that the agent might accidentally log or stream.

### 3. LLM & Agent Guardrails
- **Hallucinated Actions**: The UI must not blindly execute client-side functions suggested by the LLM without human confirmation.
- **Status Transparency**: Ensure the UI clearly distinguishes between "Agent generated this" and "Human authored this" for clear accountability.
