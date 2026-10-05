---
name: markmap-generator
description: Utiliza este skill cuando necesites crear mapas mentales, brainstormings visuales o esquemas jerárquicos interactivos en formato HTML listos para visualizar en el navegador. Intercepta la idea, diseña un documento markdown (.md) como modelo y complila localmente el mapa usando npx markmap-cli.
collection: smart-money-activity
promotable: true
---

# Markmap Generator

This skill enables Claude to generate fully interactive, zoomable HTML mind maps on the user's local machine without needing API keys or deep third-party plugins, relying on the Markdown translation package `markmap-cli`.

## When to Use This Skill

- The user requests a mind map, brainstorming diagram, or concept tree.
- The user wants a standalone HTML file they can easily open in their browser or share.
- The data is hierarchical and suited for bullet-point Markdown representation.

## How to Execute the Workflow

Follow these steps strictly to produce the final diagram:

### 1. Design the Markdown Source
Translate the user's idea or the structure you want to visualize into a strict Markdown unordered list format using `-` (bullets) and proper indentation for nested branches. 
- Use the H1 `#` tag as the root node of the mind map.
- Strictly adhere to `ESTILO_TIPOGRAFICO_SENTENCE_CASE.md` (if available in context) or, generally, use sentence case for the text inside the nodes (capitalizing only the first letter of the first word).

### 2. Write the Temporary Markdown File
Save your generated Markdown content into a temporary file inside the `diagrams/` folder of this skill. Include math equations or inline styles if necessary, but keep it clean.
For example, save to `diagrams/temp_mindmap.md`.

### 3. Compile the Markmap HTML using the Bundled Script
Instead of running raw `npx` commands and handling files manually, use the automated builder script included in this skill.

**Command to run:**
Use the `run_command` tool to execute the Node compilation script located in the `scripts/` directory alongside this SKILL.md. Point to the files in the `diagrams/` folder:
```bash
node "C:\Users\FL2024\.gemini\antigravity\skills\visual-diagramming-export\markmap-generator\scripts\build_map.js" "diagrams/temp_mindmap.md" "diagrams/mindmap_result.html"
```
*(Note: If the terminal returns an error like "node is not recognized", you MUST stop and run `node c:\Users\FL2024\.gemini\antigravity\skills\visual-diagramming-export\scripts\start-skill.js` to trigger the installation wizard for the user).*
*Note: The script compiles the markdown, saves it, and completely handles temporary file cleanup automatically.*

### 4. Provide the Result
1. Inform the user that their interactive HTML mind map (`diagrams/mindmap_result.html`) is ready.
2. Tell them they can double-click the file to zoom, collapse/expand branches, and interact with the mind map visually.
