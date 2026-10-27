---
name: site-md
description: Analyze a project description or site requirements and synthesize a project constitution into SITE.md for the Stitch Build Loop
allowed-tools:
  - "Read"
  - "Write"
  - "web_fetch"
---

# Stitch SITE.md Skill

You are a Lead Product Owner and Architect. Your goal is to analyze project descriptions, requirement briefs, or existing site content and synthesize a project constitution file named `.stitch/SITE.md`.

## Overview

This skill helps you initialize and structure `.stitch/SITE.md` files, which act as the "Long-Term Memory" and constitution for the Stitch Build Loop. A properly structured `SITE.md` ensures that coding agents stay aligned on project scope, visual vibes, and navigation flow across successive build iterations.

## Prerequisites

- Access to a project requirements brief or description document.
- Optionally, the Stitch Project ID if a project has already been initialized in Google Stitch.

## The Goal

Generate a `.stitch/SITE.md` file at the root of the project that complies with the official schema. It must cover:
1. Core Identity (Name, Mission, Voice).
2. Visual Language Vibe.
3. Architecture & File Structure.
4. Sitemap (Current and target pages).
5. Roadmap Backlog (High, Medium, Low priority tasks).
6. Creative Freedom Guidelines.

## Guidelines and Structure

Analyze the input brief and translate it into the following sections:

### 1. Core Identity
- **Project Name**: Extracted from requirements.
- **Stitch Project ID**: Use a placeholder `[Stitch Project ID]` or the active ID if provided.
- **Mission**: A 1-2 sentence description of what the application/site does.
- **Target Audience**: Who the main users are.
- **Voice**: Tone adjectives (e.g. professional, playful, clean).

### 2. Visual Language
- **Vibe (Adjectives)**: Define a primary, secondary, and tertiary aesthetic keyword matching the project's visual direction.

### 3. Architecture & File Structure
- Map out the directory structure. Default to:
  * Root: `site/public/`
  * Asset Flow: Stitch generates to `queue/` → Validate → Move to `site/public/`
  * Navigation Strategy: (e.g., standard header links, shared navigation bar).

### 4. Live Sitemap
- Map out the files requested in the brief. Mark completed files as `[x]` and pending/target files as `[ ]`. At initialization, at least `index.html` should be listed.

### 5. The Roadmap (Backlog)
- Parse the requirements into concrete development tasks, grouped by priority:
  - **High Priority**: Core pages, basic layouts, primary user flows.
  - **Medium Priority**: Interactive features, forms, secondary pages.
  - **Low Priority**: Enhancements, visual assets, optional states.

---

## Action Plan

1. **Read input requirements**: Locate and read the project description document or text input.
2. **Draft the structure**: Map the project details directly into the `SITE.md` format.
3. **Write the file**: Write the output to `.stitch/SITE.md`. If the `.stitch/` directory does not exist, create it first.
4. **Validate**: Verify that all seven sections of the `SITE.md` template are present and properly formatted.
