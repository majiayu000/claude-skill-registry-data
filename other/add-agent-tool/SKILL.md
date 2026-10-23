---
name: add-agent-tool
description: Add a tool function to the Medox agent. Use when creating a tool file, registering it in the API loop, and writing its test.
argument-hint: "<tool-name>"
---

# Skill: Add a New Agent Tool

## Steps

1. **Create the tool file** at `src/medox/agent/tools/tool_<name>.py`:
   ```python
   """One-line description of the data source and lookup strategy."""

   from medox.pipeline.config_pipeline import PipelineSettings

   def <tool_name>(<param>: str) -> str:
       """
       <What this tool does — written for the LLM, not a human developer.>

       Include:
       - What the parameter means and expected format
       - Example values or class names the LLM should pass
       - What the tool returns and how to interpret it

       Example: pass 'ANTIVITAMINES K' for warfarine, 'STATINES' for simvastatine.
       """
       settings = PipelineSettings()
       # ... implementation
   ```

2. **Register the tool** in `src/medox/api/agent.py` (`TOOLS`) and in `_dispatch_tool` in `src/medox/api/app.py`.

3. **Docstring rules** (critical — the LLM uses this to decide when/how to call the tool):
   - Written in English
   - Explain *when* to use this tool vs other tools
   - Give concrete input examples (especially for ANSM class names)
   - Describe the return format

4. **Write the test** at `tests/agent/test_tool_<name>.py`:
   ```python
   def test_<tool_name>_returns_expected():
       result = <tool_name>.invoke({"<param>": "<known_value>"})
       assert "<expected_substring>" in result

   def test_<tool_name>_handles_unknown():
       result = <tool_name>.invoke({"<param>": "nonexistent_xyz"})
       assert result  # returns graceful message, not exception
   ```

5. **Update `.claude/rules/agent.md`** — add the tool to the tools table.

6. **Validate**:
   ```bash
   uv run pytest tests/agent/test_tool_<name>.py -v
   uv run pytest tests/agent/ -v
   ```

## Rules

- Tool file name: `tool_<name>.py` — matches the `@tool` function name
- One `@tool` per file
- Never raise exceptions — return a descriptive string on error
- Requires Docker stack running for PostgreSQL tools
