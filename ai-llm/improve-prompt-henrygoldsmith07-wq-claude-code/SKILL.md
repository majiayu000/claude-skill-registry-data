---
name: improve-prompt
description: Single-pass rewrite of an LLM prompt — paste a prompt or point at a file (system prompt, prompt template, agent definition, SKILL.md) and get an improved version with a rationale for each change. Use when the user wants a prompt improved, optimized, tightened, or reviewed against prompt-engineering best practices.
argument-hint: [prompt text or file path]
---

# Improve Prompt

Improve the prompt given in `$ARGUMENTS` with a single-pass rewrite. This is the manual, deep counterpart to the automatic per-message improver hook (`.claude/helpers/prompt-improver.cjs`).

## Steps

1. **Resolve the input.** If `$ARGUMENTS` is a file path, Read the file and locate the prompt inside it (a prompt constant, template string, system-prompt field, or the whole file for SKILL.md/agent definitions). Otherwise treat `$ARGUMENTS` itself as the prompt. If it's empty, ask the user to paste a prompt or name a file.

2. **Rewrite the prompt** applying this checklist — change only what improves it, and preserve the author's intent exactly:
   - Clear role/persona up front when the prompt defines an assistant's behavior
   - Explicit goal and expected output format (structure, length, JSON schema if applicable)
   - XML-tagged sections (`<instructions>`, `<context>`, `<examples>`, `<output_format>`) when the prompt mixes instructions with data or context
   - Concrete examples (few-shot) where behavior is otherwise underspecified
   - Constraints stated positively ("do X") rather than as long "don't" lists
   - Ambiguities resolved or surfaced — if intent is unclear, state the assumption inline rather than guessing silently
   - Template variables clearly delimited and documented
   - Dead weight removed: filler, duplicate instructions, hedging

3. **Present the result** as:
   - The improved prompt in a fenced block
   - A table of changes: what changed → why it helps

4. **If the prompt came from a file**, offer to apply the improved version with an Edit — do not modify the file without confirmation.
