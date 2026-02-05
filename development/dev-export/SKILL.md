---
name: dev-export
description: Standards for exporting artifacts to Obsidian Inbox. Focuses on safe copying and minimal friction.
---

# Dev Export Standards

## Purpose
To create a "Bridge" between Development environments and Semantic Knowledge Bases (Obsidian).

## Core Philosophy: "Dump First, Organize Later"
Do not try to organize, rename, or structure files inside the export utility. Just get them safely into the Inbox.

## Export Rules

### 1. Target Location
- **Always**: `[Obsidian_Vault_Root]/00_Inbox/`
- **Naming**: `{Project_Name}_Export` (e.g., `ClaudeSkills_Export`)

### 2. Safety
- **No Delete**: Never delete files from the source.
- **Overwrite Warning**: If the target folder exists, prompt or create a versioned folder (e.g., `_Export_v2`).

### 3. Log
- Output a summary of what was copied to the terminal.
