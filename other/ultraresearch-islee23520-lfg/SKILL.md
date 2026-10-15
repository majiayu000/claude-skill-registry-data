---
name: ultraresearch
description: "Legacy alias for ulw-research. MUST USE when the user asks for ultraresearch, /ultraresearch, or /ultraresearch; immediately load and follow the ulw-research skill."
---

## GrokBuild Tool Mapping

On Grok Build with lfg installed, translate OpenCode/Codex subagent examples to GrokBuild `spawn_subagent` calls. Prefer host built-ins when they fit: read-only search → `subagent_type: "explore"`; catch-all → `"general-purpose"`. Use lfg OMO personas (`explorer`, `librarian`, `coding`, …) only when OMO prompts/models matter. This contract is GrokBuild-only (`coding_tool_adapter` = `grok`).

| Intent | GrokBuild tool to use |
| --- | --- |
| Search/read-only worker | `spawn_subagent({ subagent_type: "explore", background: true, description: "...", prompt: "TASK: ..." })` (host built-in; use `"explorer"` only for OMO persona) |
| Planning worker | `spawn_subagent({ subagent_type: "plan", background: true, description: "...", prompt: "TASK: ..." })` |
| Implementation or QA worker | `spawn_subagent({ subagent_type: "hephaestus" or "coding", background: true, description: "...", prompt: "TASK: ..." })` |


# Ultraresearch Alias

`ultraresearch` is the legacy name for `ulw-research`.

When this skill is selected, immediately load `../ulw-research/SKILL.md` and follow it as the source of truth. Treat `/ultraresearch`, `/ultraresearch`, and plain `ultraresearch` exactly like `/ulw-research`, `/ulw-research`, and plain `ulw-research`.
