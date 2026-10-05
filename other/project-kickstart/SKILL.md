---
name: project-kickstart
description: >
  Scaffold any project in seconds. Generate boilerplate for Next.js, React,
  Python CLI, Express, FastAPI, static sites, and more. Pre-configured with
  git, linting, CI, README, and license. Use when the user starts a new project.
  Triggers on: "new project", "start a project", "scaffold", "create a new app",
  "init project", "boilerplate", "kickstart".
tags:
  - scaffold
  - boilerplate
  - starter
  - template
  - project
  - init
  - create
  - new-project
---

# Project Kickstart

You scaffold new projects with best-practice defaults so the user can start coding in 60 seconds.

## Core Behavior

When the user describes what they want to build, detect the best stack and generate the project structure with all configuration files.

## Supported Stacks

| Stack | Trigger | What's Generated |
|-------|---------|-----------------|
| **Next.js + TypeScript** | "next app", "react website" | next.config.ts, tsconfig, tailwind, eslint, app/ router |
| **React + Vite** | "react app", "SPA" | vite.config, tsconfig, tailwind, src/ structure |
| **Python CLI** | "python tool", "CLI tool" | pyproject.toml, click/typer, src/, tests/ |
| **FastAPI** | "python API", "backend" | main.py, requirements.txt, Dockerfile, tests/ |
| **Express + TypeScript** | "node API", "express" | tsconfig, src/, routes/, middleware/ |
| **Static HTML** | "landing page", "static site" | index.html, styles.css, script.js |
| **OpenClaw Skill** | "openclaw skill", "agent skill" | SKILL.md, README.md with frontmatter |

## What Every Project Gets

Regardless of stack:
1. **`.gitignore`** — language-appropriate
2. **`README.md`** — project name, description, quick start, license
3. **`LICENSE`** — MIT by default (ask if user wants different)
4. **`.github/workflows/ci.yml`** — basic CI (lint + test)
5. **`git init`** — initialized with first commit

## Workflow

### Step 1: Ask (if not clear)
```
What are you building?
1. Web app (Next.js)
2. API (FastAPI/Express)
3. CLI tool (Python)
4. Static site
5. OpenClaw skill
6. Something else (describe it)
```

### Step 2: Generate
Create all files with the appropriate content. Don't use placeholder text — write real, working starter code.

### Step 3: Report
```
Project created: my-awesome-app/

  my-awesome-app/
  ├── .github/workflows/ci.yml
  ├── .gitignore
  ├── LICENSE (MIT)
  ├── README.md
  ├── package.json
  ├── tsconfig.json
  ├── src/
  │   └── app/
  │       ├── layout.tsx
  │       └── page.tsx
  └── tailwind.config.ts

Next steps:
  cd my-awesome-app
  npm install
  npm run dev
```

## Rules
- Write REAL working code, not "TODO" placeholders
- Use the latest stable version of every dependency
- Default to TypeScript for JS projects
- Default to Tailwind for CSS
- Default to MIT license
- Always init git with a clean first commit
- Keep it minimal — don't add auth, database, or features unless asked
