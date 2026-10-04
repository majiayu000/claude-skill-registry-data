---
name: Developer Onboarding
description: "Guided onboarding workflow for new developers joining the simpler-grants-gov project. Walks through environment setup, architecture understanding, toolkit configuration, and making a first PR. Use when a new developer joins the team or when someone needs to understand the project from scratch."
model: inherit
---

## When to Use

Invoke this skill when:
- A new developer is joining the simpler-grants-gov project
- Someone needs to understand the project architecture from scratch
- Setting up a development environment for the first time
- Onboarding to the AI Coding Toolkit

## Step-by-Step Instructions

### Step 1: Environment Setup
Follow `setup-checklist.md` to get the development environment running:
- Clone the monorepo
- Install dependencies (API + Frontend)
- Configure environment variables
- Set up Cursor IDE with plugins
- Verify MCP servers are working

### Step 2: Architecture Tour
Follow `architecture-tour.md` for a guided walkthrough:
- Understand the monorepo structure
- Learn the API layer architecture (routes → services → database)
- Learn the frontend architecture (pages → components → hooks → services)
- Understand how the forms domain spans both
- Review key ADRs that explain architectural decisions

### Step 3: Toolkit Familiarization
- Run `/tooling-health-check` to verify your setup is complete and all dependencies are installed
- Explore available slash commands (`/debug`, `/refactor`, `/new-endpoint`, etc.)
- Understand how rules auto-activate based on file paths
- Try invoking an agent on a sample task
- Review the MCP tools available

### Step 4: First PR
Follow `first-pr-guide.md` to make a first contribution:
- Pick a good first issue
- Use the appropriate agent to help
- Run the quality gate pipeline
- Submit the PR following team conventions

## Conventions and Best Practices

- Start with the setup checklist before anything else
- The architecture tour is designed to be done with Cursor's AI — ask questions as you go
- Use `/explain-architecture` command at any point to understand specific files
- The first PR should be small and focused — the goal is to learn the workflow, not ship a big feature
