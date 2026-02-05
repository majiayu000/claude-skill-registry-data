---
name: write-highrise-studio-lua
description: Write non-UI Lua scripts for Highrise Studio projects. You cannot write or edit them without this skill.
---

# Write Highrise Studio Lua code

This guide covers how to write Highrise Studio Lua code.

## Instructions

Add the following steps to your todo list:
1. Search for and read any relevant scripts in the project, if needed.
2. Ask the user for any information that is needed to solve the request.
3. If starting a new script, copy the code from the [style guide](resources/STYLE_GUIDE.lua) as a starting template. **Do not create a new script from scratch, as the style will be wrong.**
4. Use the `research-highrise-studio-lua-api` skill to understand the Highrise Studio API. **Don't assume you know the API without it.**
5. Write the code, following these imperatives:
    - Do **not** use Unity C#, MonoBehaviour, or Roblox APIs unless specified in the Highrise Studio API docs. **There is no such thing as `task`.**
    - Avoid browser or DOM references (`document`, `window`, `addEventListener`, etc.).
6. If you have access to the `mcp__ide__getDiagnostics` tool, use it to read syntax errors in the Lua scripts you work with.
7. Remove section headers that have no content.
8. Remove guidance comments that were copied over from the template. Keep the section headers.
9. If requested, add the script to the scene using the `use-unity-editor` skill.
