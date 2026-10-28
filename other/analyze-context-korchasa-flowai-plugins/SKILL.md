---
name: analyze-context
description: >-
  Estimate total token usage and cost across conversation history, system
  prompts, and active rules. Use when the user asks how much context or how many
  tokens are in use, to audit context size, or to estimate session cost.
model: sonnet
effort: low
---

# Analyze Context (Total Cost Estimation)

## Instructions

1.  **Scope**: Analyze **ALL** components that contribute to the context window and cost. This includes:
    - **Conversation History**: User messages, Assistant responses, Tool calls, and Tool outputs.
    - **System Context**:
        - **System Prompts**: The core instructions defining the agent's behavior.
        - **Active Rules**: Content from `AGENTS.md` and any active `.cursor/rules`.
        - **Skill/Tool Definitions**: The descriptions of available tools and skills (often a significant overhead).
        - **Attached Context**: Any `<open_and_recently_viewed_files>`, `<git_status>`, or other automatic context blocks.

2.  **Estimation Method**:
    - Calculate the token count based on the number of characters for each component.
    - **Formula**: `Token Count = Character Count * Multiplier`
    - **Multiplier**: Use **0.3** (approx. 1 token per 3.3 characters).

3.  **Procedure**:
    1.  **Conversation**: Estimate chars in the visible chat history.
    2.  **System/Rules**: Read `AGENTS.md` and any active rule files to estimate their size.
    3.  **Overhead**: Add a heuristic buffer for Tool/Skill definitions and hidden system prompts (typically **2000-5000 chars** or **~1000 tokens** depending on the number of tools).
    4.  **Total**: Sum all components.
    5.  **Report**: Provide a breakdown of the estimated usage.

4.  **Tools**:
    - Use the script for calculation:
      ```bash
      deno run scripts/count_tokens.ts "TEXT_snippet"
      ```
    - Or manual calculation: `Total Chars * 0.3`.

## Examples

**User:** "How many tokens are we using?"
**Action:**
1.  **Chat**: ~5000 chars (User + AI messages).
2.  **System**: `AGENTS.md` (~3000 chars) + Rules (~1000 chars).
3.  **Overhead**: ~3000 chars (Tool definitions).
4.  **Total Chars**: 12,000.
5.  **Calc**: `12,000 * 0.3 = 3,600 tokens`.
6.  **Report**:
    "**Estimated Context Usage:** ~3,600 tokens
    - **Conversation:** ~1,500 tokens
    - **System & Rules:** ~1,200 tokens
    - **Tool Definitions:** ~900 tokens"
