---
name: npid-existing-code
description: Reuse existing Prospect ID code instead of creating new abstractions
---

# NPID Existing Code-First Skill

Repository: `Raycast/prospect-pipeline`

Core principle:
- MOST of what is needed is already within the code.
- ALWAYS try to improve or utilize already working code.

When this skill is active, follow these rules:

## 1. Files to inspect first

Before proposing any implementation:

- `src/python/npid_api_client.py`
- `mcp-servers/npid-search/src/session.ts`
- `mcp-servers/npid-search/src/npid-client.ts`
- `mcp-servers/npid-search/src/season-calculator.ts`
- `src/generate-names.tsx`
- `src/tools/generate-content.ts`
- `docs/plans/2025-11-14-npid-athlete-search-design.md`

Assume the correct pattern already exists in one of these and your job is to connect or extend it minimally.

## 2. Authentication and session

- Reuse `~/.npid_session.pkl` and the shared auth loader in `src/session.ts`.
- Use `loadSession()` and `getAuthHeaders()` for all NPID HTTP calls.
- Do NOT:
  - Create new session managers.
  - Add login flows, remember-me logic, or token expiry logic.
  - Log cookies or auth details.

## 3. Data and positions

- Positions come exactly from the API (pipe-separated abbreviations).
- If position 2 or 3 is missing: leave it blank.
- If no positions exist: return empty string.
- Never manufacture `"NA"` or other placeholders.

## 4. Change strategy

When implementing anything:

1. Find 1–3 similar patterns already in this codebase (Python client, MCP client, Raycast form, content generator).
2. Align with the closest pattern instead of inventing a new one.
3. Prefer changing a single existing file over adding new ones.
4. Keep responses:
   - Diff-only.
   - Minimal lines.
   - No explanations unless explicitly requested with "explain".

Prohibited behaviors in this repo:

- New auth abstractions.
- New "helpful" layers that duplicate existing logic.
- Placeholder data that isn't coming from the API or user input.
