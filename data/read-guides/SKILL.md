---
name: read-guides
description: Instructions for checking the available guides in the ai4space repository and reading them.
---
# Read Guides

This skill helps the user find and read the documentation available in the `guides/` directory.

## Instructions

When the user asks to "read guides", "list guides", or asks for help on a specific topic covered by the guides, follow these steps:

1.  **List Available Guides**:
    If the user asks what guides are available, list the following files located in `guides/`:

    -   `guides/INTRODUCTION.MD` - General introduction and project goals.
    -   `guides/TOOLS_AND_SERVICES.MD` - Overview of tools (Godot, Lunar Sim) and services used.
    -   `guides/BLENDER_TO_GODOT_WORKFLOW.MD` - Workflow for importing assets from Blender to Godot.
    -   `guides/ADVANCED_GIT_SETUP.MD` - Advanced Git configuration and best practices.

2.  **Read a Specific Guide**:
    If the user asks to read a specific guide (e.g., "how to use blender", "intro"), use your file reading tools to read the content of the corresponding markdown file from the list above.

3.  **Contextual Help**:
    If the user asks a question that seems to be answered by one of these guides, proactively read the relevant guide and use its content to answer the user's question, citing the guide as the source.
