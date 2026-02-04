---
name: obsi-project-kickoff
description: Standards for creating new Obsidian projects with consistent structure and metadata.
---

# Project Kickoff Standards

## Purpose
To transform random folders into **Managed Projects** with clear goals, status, and navigation.

## Naming Conventions
- **Project Folder**: `10_Projects/{Project_Name}`
- **Format**: `PascalCase` (e.g., `AntigravityAgent`) or `snake_case` (e.g., `antigravity_agent`).

## Project Types & Structure
1.  **Study/Learning**:
    - `docs/plans/`: For `dev-study_planner`
    - `notes/`: Raw learning notes
2.  **Development**:
    - `src/`, `docs/`: Standard coding structure
    - `git init`: Recommended

## Core Files
- **Overview.md**: The "Home Page" of the project. Must contain tags (`#status/active`) and links to key docs.
- **task.md**: Actionable items.
