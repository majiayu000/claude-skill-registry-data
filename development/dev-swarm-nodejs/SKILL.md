---
name: dev-swarm-nodejs
description: Install and configure Node.js, npm, and pnpm using nvm. Use when setting up a Node.js environment.
---

# Node.js Environment Setup

This skill assists in installing and configuring the Node.js environment, including `nvm` (Node Version Manager), Node.js (LTS), and `pnpm`.

## When to Use This Skill

- User needs to set up Node.js development environment
- User wants to install or update Node.js and pnpm
- User asks to configure package management tools

## Prerequisites

- For macOS/Linux: `curl` or `wget`.
- For Windows: PowerShell.

## Your Roles in This Skill

- **DevOps Engineer**: Install and configure Node.js environment using nvm. Set up pnpm package manager through corepack. Verify installations and troubleshoot setup issues. Guide users through platform-specific installation steps. Update project documentation to reflect environment setup.

## Role Communication

As an expert in your assigned roles, you must announce your actions before performing them using the following format:

As a {Role} [and {Role}, ...], I will {action description}

This communication pattern ensures transparency and allows for human-in-the-loop oversight at key decision points.
## Instructions

### 1. Check Existing Installation

Before installing, check if Node.js or pnpm are already installed.

```bash
node --version
pnpm --version
```

If they are installed and meet requirements, you may skip installation steps. Always ask the user for confirmation before overwriting or modifying existing installations.

### 2. Install nvm (Node Version Manager)

**macOS and Linux:**

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
```
*Note: You may need to restart the shell or source the profile file (e.g., `source ~/.zshrc`) to use `nvm`.*

**Windows:**

Download and run the installer from:
https://github.com/coreybutler/nvm-windows/releases/download/1.2.2/nvm-setup.exe

### 3. Install Node.js

Install the latest LTS (Long Term Support) version of Node.js.

```bash
nvm install lts/jod
nvm use lts/jod
```
*(As of this writing, `lts/jod` points to v22.x. Adjust if a specific version is required).*

### 4. Install pnpm

We use `pnpm` instead of `npm` for this project.

Enable `pnpm` via `corepack` (included with recent Node.js versions):

```bash
npm install --global corepack@latest
corepack enable pnpm
```

verify:
```bash
pnpm --version
```

### 5. Executing Packages (dlx)

For any command that typically uses `npx package`, use `pnpm dlx package` in this project.

### 6. Save User Preferences

After successful installation, save the package manager preference to `dev-swarm/user_preferences.md` so future sessions remember to use `pnpm`.

**Example:**

Create or update `dev-swarm/user_preferences.md` with:

```markdown
## Node.js Package Manager
- Use **pnpm** for all Node.js package operations (instead of npm)
- Node.js version: LTS (jod - v22.x)
- For executing packages, use `pnpm dlx` instead of `npx`
```
