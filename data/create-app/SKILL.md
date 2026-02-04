---
name: create-app
description: 'Use this skill whenever creating a new application. IMPORTANT: This should be the FIRST thing you read when starting a new project. IMPORTANT: Read this before planning or brainstorming.'
---

# Create App Implementation Plan

> **For Claude Code:** Follow this plan phase-by-phase. If any step fails, notify the user and ask for next steps.

**Phase Summary Template:** At the end of each phase, output to the user a detailed summary (2-3 paragraphs) that includes:
- What was accomplished in this phase
- Key files/directories created or modified
- Important values to remember (service_id, schema names, etc.)
- Brief preview of what's coming next

**Goal:** Scaffold a production-ready fullstack web application with database, optional auth, and polished UI.

**Architecture:** T3 stack (Next.js + tRPC + Drizzle) with Timescale Cloud database and shadcn/ui components.

**Tech Stack:** Next.js, tRPC, Drizzle ORM, Timescale Cloud (PostgreSQL), Better Auth, shadcn/ui, Tailwind CSS

---

## Getting Started

Tell the user:

"Let's build a minimal v0/demo version of your app. We'll focus on the core features needed to get something working, then iterate from there.

Here's how we'll build this:
- 🎯 **Phase 1: Understand the product** - I'll ask a few questions about what you're building
- 🏗️ **Phase 2: Scaffold the app** - Create a cloud database and app with Next.js, tRPC, and Drizzle
- 🔐 **Phase 3: Configure auth** (if needed) - Set up user authentication
- 🗄️ **Phase 4: Design the database** - Create tables for your data
- ⚙️ **Phase 5: Build the backend** - Create API endpoints with tRPC
- 🎨 **Phase 6: Build the frontend** - Create pages and components with shadcn/ui
- ✅ **Phase 7: Run, verify, and commit** - Make sure everything works and save to git

**Optional hardening (after commit):**
- 🧪 **Phase 8: Add testing** - Integration tests with Vitest
- 🔍 **Phase 9: Strict checks** - Stricter TypeScript and linting

Let's go!"

---

## Phase 1: Understand the Product

**Key Principles:**
- One question at a time - Don't overwhelm with multiple questions
- Multiple choice preferred - Easier to answer than open-ended when possible
- YAGNI ruthlessly - Remove unnecessary features from all designs
- Explore alternatives - Always propose 2-3 approaches before settling
- Incremental validation - Present design in sections, validate each
- Be flexible - Go back and clarify when something doesn't make sense

1. **Determine app type** - If not clear from the prompt, ask: "Is this a multi-user app (requires user accounts/login)?"

2. **Gather auth requirements (if multi-user)** - Ask the user: "Which authentication methods do you want? Pick one or more:" Email signup, GitHub OAuth, Google OAuth

3. **Confirm app name** - Propose a sensible app name based on the user's request. The name should be lowercase, use hyphens instead of spaces (e.g., `todo-app`, `fitness-tracker`), and appropriate for a directory name. Ask: "I'll name the project `<proposed-name>`. Does that work, or would you prefer something else?"

4. **Understand what product you are building** - Try to understand the project from the user prompt then ask questions one at a time to refine the idea. Focus on what the product will do, NOT technical details.

Once you understand what you're building, present the **product brief** to the user for confirmation:

1) **App type**: Single-user or multi-user
2) **Authentication** (if multi-user): Which methods (email, GitHub, Google)
3) **Product description**: A one to three paragraph description of what the project will do
4) **Minimal features for v0/demo**: A short bulleted list - just enough to get a working application

Example product brief:
```
**App type:** Multi-user

**Authentication:** Email signup

**Product description:**
A collaborative to-do app where users can create personal to-do lists and share them with other users. Users sign up with email, create tasks, and can invite collaborators to view or edit their lists together.

**Minimal features for v0/demo:**
- Email signup/login
- Create, edit, delete, and complete to-dos
- Share a to-do list with another user by email
- Collaborators can view and edit shared lists
```

Ask the user: "Is this product brief correct?"

After the user confirms the product brief, ask: "Are there any features not in the v0/demo that might affect how we build this? For example: offline support, real-time sync, multi-tenancy, or specific integrations. These won't be built now, but knowing them helps us make the right architectural choices upfront."

If yes, create and confirm a list of "future features".

---

## Phase 2: Project Setup

1. Use the `create_database` MCP tool to provision a new Timescale Cloud database
2. Store the returned `service_id` - you'll need it later
3. Use the `create_web_app` MCP tool with:
   - `app_name` confirmed in Phase 1
   - `use_auth: true` if multi-user app
   - `product_brief` from Phase 1
   - `future_features` from Phase 1 (if any)
4. Change into the app directory: `cd <app_name>`
5. Output a  phase summary to the user using the template.

---

## Phase 3: Auth Configuration (If Multi-User)

Skip this phase if the app is single-user.

1. Pass the drizzle schemas into `drizzleAdapter` in `src/server/better-auth/config.ts`:
   ```typescript
   import * as schema from "~/server/db/schema";

   drizzleAdapter(db, {
     provider: "pg",
     schema,
   })
   ```
2. Update the Better Auth configuration to enable only the providers the user requested (email, GitHub, Google)
3. Update `src/env.js`, `.env`, and `.env.example` with the required environment variables for the auth providers
4. Output a  phase summary to the user using the template.

---

## Phase 4: Database Schema

1. Check that the database status is `READY` using the `service_get` MCP tool with the `service_id` from Phase 2. If not ready, poll every 10 seconds for up to 2 minutes.

2. Use the `setup_app_schema` MCP tool with:
   - `application_directory`: "."
   - `service_id` from Phase 2
   - `app_name` (use the same name, converted to lowercase with underscores)

   This creates a PostgreSQL schema and user, and writes `DATABASE_URL` and `DATABASE_SCHEMA` to `.env`

3. In `src/env.js` add DATABASE_SCHEMA variable (use the `schema_name` returned by `setup_app_schema` as default) to both the server and runtimeEnv sections

4. Modify `drizzle.config.ts` to remove the tablesFilter and add a schemasFilter with the value of the DATABASE_SCHEMA env variable

5. In `src/server/db/schema.ts`, remove pgTableCreator pattern and instead create all tables (including auth tables, if present) using:
   ```typescript
   export const dbSchema = pgSchema(env.DATABASE_SCHEMA);
   const createTable = dbSchema.table;
   ```
   Note: make sure the schema is exported

6. Delete the example `post` table definition - it was only there as a template

7. Based on the user's app requirements, add the necessary Drizzle table definitions to `src/server/db/schema.ts`

8. Push schema to database: `npm run db:push`

9. Output a  phase summary to the user using the template.

---

## Phase 5: Backend Implementation

1. Remove any example/post router that references the old post model
2. Create tRPC routers for CRUD operations on the app's data models in `src/server/api/routers/`
3. Register new routers in `src/server/api/root.ts`
4. Verify with `npx tsc --noEmit -p tsconfig.server.json` (checks only server code, avoids frontend errors)
5. Output a  phase summary to the user using the template.

---

## Phase 6: Frontend Implementation

1. Install and configure shadcn:
   ```bash
   npx shadcn@latest init --base-color=neutral
   cp src/styles/globals.css.orange src/styles/globals.css
   ```

2. Install required shadcn components (button, card, input, form, table, etc.):
   ```bash
   npx shadcn@latest add <component1> <component2> ...
   ```

3. Build the pages needed for the app using shadcn components (ensure all buttons have a type attribute)

4. Connect pages to the backend using tRPC hooks to fetch and mutate data

5. Create a sign-in form component at `src/components/auth/sign-in-form.tsx` (if multi-user) supporting all requested auth methods (email, GitHub, Google)

6. Replace hardcoded T3 template colors with shadcn CSS variables:
   - `bg-gradient-to-b from-slate-900 to-slate-800` → `bg-background`
   - `text-white` → `text-foreground`
   - `bg-white/10` → `bg-muted`
   - `border-white/20` → `border-border`

7. Verify with `npm run build` and fix any errors

8. Output a  phase summary to the user using the template.

---

## Phase 7: Run, Verify, and Commit

1. Run `npm run check:write` to auto-fix formatting issues, then verify `npm run check` passes

2. Start the dev server: `npm run dev`

3. Use the `open_app` MCP tool to open http://localhost:3000 in a browser and verify the app works as expected

4. Use the `write_claude_md` MCP tool to generate the project guide:
   - `application_directory`: "."
   - `app_name`: from Phase 1
   - `use_auth`: Whether auth is enabled
   - `product_brief`: from Phase 1
   - `future_features`: from Phase 1 (if any)
   - `db_schema`: from `setup_app_schema` in Phase 4
   - `db_user`: from `setup_app_schema` in Phase 4

5. Read the generated `CLAUDE.md` file. Make sure it is accurate. Fix if needed.

6. Ask the user "Do you want to commit this initial version to git?". If yes:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: <app_name>"
   ```

7. Tell the user:

"🎉 Congrats! Your app is set up and committed. You have a working demo you can iterate on.

**Next steps:**
- 🛡️ **Harden** - Add testing and stricter checks (recommended)
- 🧠 **Brainstorm** - Plan your next features
- 🚀 **Deploy** - Ship to Vercel

**Why harden?** These checks act like a reward signal for AI-assisted development - they catch mistakes early and help guide me toward correct solutions faster. Without them, bugs can compound silently.

Shall we add hardening now?"

If the user wants to skip hardening, the skill is complete.

---

## Phase 8: Backend Testing (Optional Hardening)

Ask the user (yes/no): "Do you want to add backend testing?"

If no, skip this phase.

1. Use the `view_skill` MCP tool to read the `add-backend-testing` skill
2. Follow the skill with `service_id` from Phase 2
3. Offer to git commit these changes

---

## Phase 9: Stricter Checks (Optional Hardening)

Ask the user (yes/no): "Do you want to enable stricter TypeScript checks?"

If no, skip this phase.

1. Use the `view_skill` MCP tool to read the `add-strict-checks` skill
2. Follow the skill
3. Offer to git commit these changes
