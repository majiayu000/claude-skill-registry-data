---
name: create-highrise-studio-ui
description: Create and edit UI components for Highrise Studio projects. You can't create or edit them without this skill.
---

# Create Highrise Studio UI components

This guide covers how to create and edit Highrise Studio UI components.

## Context

A Highrise Studio UI component consists of three parts:
- A UXML file, which defines the UI's structure.
- A Lua script, which handles interaction and data-based rendering.
- A USS file, which defines the UI's styles.

You must create all three parts to have a functional UI component. There is **no** HTML or CSS.

## Instructions

Add the following steps to your todo list:
1. Search for and read any relevant scripts in the project, if needed.
2. Ask the user for any information that is needed to solve the request.
3. If creating a new UI component, copy the [entire template directory](resources/MyUIElement/) (not just its contents) from this plugin to the project's `Assets/UI` folder. Rename the directory all of its contents to the desired UI component name in `PascalCase`.
4. Write the UXML file, starting from the template.
    - Rely on the `research-highrise-studio-lua-api` skill to determine what elements exist and how to use them. Valid elements will inherit from `VisualElement` or a subclass thereof.
    - When you are done, remove guidance comments that were copied over from the template.
5. Write the Lua script, starting from the template.
    - Rely on the `research-highrise-studio-lua-api` skill to understand the Highrise Studio API.
    - Do **not** use Unity C#, MonoBehaviour, or Roblox APIs unless specified in the Highrise Studio API docs. **There is no such thing as `task`.**
    - Avoid browser or DOM references (`document`, `window`, `addEventListener`, etc.).
    - If you are ever unsure about how to do something, **read the docs.**
    - You may have access to the `mcp__ide__getDiagnostics` tool to read syntax errors in the Lua scripts you work with. Use it to check for errors, if available.
    - When you are done with the Lua script, remove section headers that have no content and non-header guidance comments that were copied over from the template.
6. Write the USS file, starting from the template. When you are done, remove guidance comments that were copied over from the template.
    - Ensure that all class names specified in the UXML file are defined in the USS file.
7. If requested, add the UI component to the scene using the `use-unity-editor` skill.
    - A UI component is added by attaching the Lua script component to a GameObject in the scene, like any other component. The UXML and USS will be pulled in automatically at runtime.
