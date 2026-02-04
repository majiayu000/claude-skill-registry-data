---
name: deploy-app
description: 'Step-by-step plan for deploying a Next.js app to Vercel'
---

# Deploy App Implementation Plan

> **For Claude:** Follow this plan task-by-task. If any step fails, notify the user and ask for next steps.

**Goal:** Deploy a Next.js application to Vercel with proper environment configuration.

**Architecture:** Vercel handles build, deployment, and hosting. Environment variables are configured via Vercel dashboard or CLI.

**Tech Stack:** Vercel, Next.js

---

## Phase 1: Pre-Deployment Checks

### Task 1: Verify Build

**Step 1: Run production build**

```bash
npm run build
```

Ensure the build completes without errors.

**Step 2: Fix any build errors**

If there are TypeScript or build errors, fix them before proceeding.

---

## Phase 2: Vercel Setup

### Task 2: Check Vercel Authentication

**Step 1: Check if already logged in**

```bash
npx vercel whoami
```

If this returns a username, skip to Task 3.

**Step 2: If not logged in**

Tell the user: "You need to authenticate with Vercel. Please run `npx vercel login` in a separate terminal and let me know when you're done."

Wait for the user to confirm before proceeding.

**Step 3: Verify login succeeded**

```bash
npx vercel whoami
```

Confirm it now returns a username before proceeding.

---

### Task 3: Link Project

**Step 1: Check if already linked**

Check if a `.vercel` directory exists in the project root. If it does, the project is already linked - skip to Task 4.

**Step 2: Check for existing projects**

```bash
npx vercel projects list
```

Look for a project with a similar name to the current app. If found, ask "I found a Vercel project named `<project-name>`. Would you like to link to this existing project, or create a new one?". If creating a new one, generate a new project name and you must confirm the new name with the user.

**Step 3: Link to project**

Always provide a project name to the following command:

```bash
npx vercel link --project=<project-name> -y
```

---

## Phase 3: Configure Environment

### Task 4: Set Environment Variables

**Step 1: Upload env vars to Vercel**

Use the `upload_env_to_vercel` MCP tool to upload all environment variables from your `.env` file to Vercel.

This uploads to production and preview environments by default.

**Step 2: Handle skipped variables**

If the tool reports any `skipped_empty` variables, warn the user:

"The following environment variables had empty values and were not uploaded: `<list>`. You'll need to set these manually in the Vercel dashboard or by running `npx vercel env add <VAR_NAME>` for each one."

**Step 3: Verify all env vars are set**

```bash
npx vercel env ls
```

---

## Phase 4: Deploy

### Task 5: Deploy to Vercel

**Step 1: Deploy**

```bash
npx vercel deploy 
```

**Step 2: Verify deployment**

Use the `open_app` MCP tool to open the deployed URL and verify the app works.

---

### Task 6: Offer Next Steps

Ask the user if they want to:
- Set up a custom domain
- Configure automatic deployments from GitHub
- Add preview deployments for pull requests
