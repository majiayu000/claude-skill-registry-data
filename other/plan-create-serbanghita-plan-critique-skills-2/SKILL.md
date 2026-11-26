---
name: plan-create
allowed-tools: >-
  Read, Write, Edit, Glob, AskUserQuestion, Bash(mkdir:*), Bash(echo $PPID), Bash(echo $COPILOT_AGENT_SESSION_ID),
  Bash(rm:*)
description: >-
  Create a new plan folder with a plan.md template. Use when the user asks to start, create or open a new plan,
  or runs /plan-create.
argument-hint: "[plan name]"
license: MIT
---

On Codex, invoke skills with `$skill-name` (for example, `$plan-create`). Use that form when giving Codex
commands; other clients use `/skill-name`.

This skill helps the user create a new plan folder along with a base `plan.md` file where the user can start
writing the plan manually or with the help of an LLM.

## Working agreement

Read the working agreement at [working-agreement.md](working-agreement.md) before step 1 and follow it for the
whole run. If it cannot be found, tell the user it is missing and apply the rules listed below.

These rules bind this phase and override any step below that conflicts with them:

1. Ask clarifying questions up front when the request is ambiguous. Do not guess the plan name, the plans folder,
   or what the user means.
2. Do not write, edit, or refactor any project code during this phase. This phase produces a plan folder and a
   `plan.md` and nothing else.
3. The plan is not finished until it lists its affected files and how success will be verified. The template
   carries both sections, so do not remove them when filling it in.

## Creating a new plan

Follow these steps precisely:

1. Display the following banner before doing anything else:
   ```
   +-------------------------------------------------+
   |  Plan Critique v3.0.1 - Creating new plan       |
   +-------------------------------------------------+
   ```
2. Resolve `plansFolder` from config:
   - Check the active agent's config file first (`.codex/plan-critique-config.json` for Codex,
     `.claude/plan-critique-config.json` for Claude Code,
     `.gemini/plan-critique-config.json` for Agy/Gemini, or `.copilot/plan-critique-config.json` for Copilot CLI),
     falling back to the other agent configs if the primary file does not exist or `plansFolder` is unset.
   - If no config exists or `plansFolder` is not set or is an empty string:
     - Ask the user: "Where would you like to store your plans? Provide a folder path (default `.planning`):".
       By default, the user should be presented with the option `.planning`.
     - Save `plansFolder` in the active agent's config file.
     - Create the folder if it does not exist, and create an `archived/` subfolder inside it.
   - Always use `plansFolder` from settings as the base directory.
3. Determine the plan name:
   - If a name was passed via `$ARGUMENTS` or in the invoking prompt, use it directly.
   - Otherwise, ask the user directly; do not offer predefined options like "New Feature" or "Bug Fix" because
     the plan name must be unique: "Enter a name for this plan:"
   The plan name must have at least 3 characters. If it is empty or shorter, respond with
   "Plan name must be at least 3 characters." and ask the user to enter one.
4. Generate a slug from the plan name:
   - Convert to lowercase (must be filesystem-safe with no special characters)
   - Replace spaces with hyphens
   - Remove characters that are not alphanumeric or hyphens
   - Trim to max 50 characters
   - Example: "Add User Authentication" becomes `add-user-authentication`
5. Check if `[plansFolder]/[slug]/` already exists.
   If it does: Respond with "A plan with this name already exists at `[plansFolder]/[slug]/`. Choose a different name."
   Ask for a new name and repeat from step 4.
6. Create directory `[plansFolder]/[slug]/`
7. Link this session to the new plan:
   - On Copilot CLI (or when `COPILOT_AGENT_SESSION_ID` is set): read `COPILOT_AGENT_SESSION_ID` via
     `echo $COPILOT_AGENT_SESSION_ID` (macOS/Linux) or `$env:COPILOT_AGENT_SESSION_ID` (Windows); if empty, use the
     literal value `default`. Store as `sessionId`.
   - Otherwise (Codex, Claude Code / Agy): run `echo $PPID` and store as `sessionId`.
   - Create `[plansFolder]/.sessions/` if needed and write the slug to `[plansFolder]/.sessions/[sessionId]`.
8. Create the plan template at `[plansFolder]/[slug]/plan.md` using [plan-template.md](plan-template.md).
   Keep the original plan name with proper casing in the H1 heading of `plan.md`.
   Only create `plan.md` initially (`critique.md` is created by `/plan-critique`).
9. Respond with confirmation:
   ```
   Created new plan: [plansFolder]/[slug]/
   Edit your plan at: [full path to][plansFolder]/[slug]/plan.md
   When ready, run `/plan-critique` to review your plan.
   ```
   (Add `[plansFolder]/.sessions/` to `.gitignore`; local session files should not be committed.)
