---
name: "local-setup"
description: "Use when a developer asks how to set up, build, or run this project locally on macOS from scratch. Trigger phrases: local setup, getting started, install dependencies, run locally, first time setup, Mac setup, onboarding, dev environment, Colima, containers, Homebrew, dotnet install, Aspire dashboard, common errors."
argument-hint: "Describe what you're trying to set up or which step you're stuck on."
user-invocable: true
---

## Instructions

Read the full setup guide at `.github/prompts/local-setup.prompt.md` and follow all instructions, constraints, and known-error resolutions defined there.

The `.github/prompts/local-setup.prompt.md` file is the single source of truth for local setup guidance and is shared with GitHub Copilot. Do not duplicate its content here.

## User Input

```text
$ARGUMENTS
```

Use the user input to determine which step or error to focus on. If empty, walk through the full setup sequence from Step 1.
