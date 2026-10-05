---
name: plan-create
description: >-
  Create a new plan folder with a plan.md template. Use when the user asks to start, create or open a new plan,
  or runs /plan-create.
license: MIT
---

You are creating a new plan folder for the user.

Fixed rules:

Read the working agreement at [working-agreement.md](../../../working-agreement.md) before step 1 and follow it
for the whole run. If that path does not resolve, look for `working-agreement.md` in the project root, then in
`.github/`. If it cannot be found anywhere, tell the user it is missing and apply the rules listed below.

These rules bind this phase and override any step below that conflicts with them:

1. Ask clarifying questions up front when the request is ambiguous. Do not guess the plan name, the plans folder,
   or what the user means. Guessing here produces the wrong plan.
2. Do not write, edit, or refactor any project code during this phase. This phase produces a plan folder and a
   `plan.md` and nothing else.
3. The plan is not finished until it lists its affected files and how success will be verified. The template
   carries both sections, so do not remove them when filling it in.
4. Be brief. No filler, no preamble, no restating the request. No emojis, no em dashes, no decorative icons.

To do this, follow these steps precisely:

1. Display the following banner before doing anything else:
   ```
   +-------------------------------------------------+
   |  Plan Critique v2.6.1 - Creating new plan       |
   +-------------------------------------------------+
   ```
2. Read `.copilot/plan-critique-config.json` and get `plansFolder` path from settings.
   If that file does not exist, read `.claude/plan-critique-config.json` instead, so a project already using the
   Claude Code plugin keeps the same plans folder.
   If neither file exists or `plansFolder` is not set or is an empty string:
   - Ask the user: "Where would you like to store your plans? Provide a folder path (default `.planning`):".
     By default, the user should be presented with the option `.planning`.
   - Save the path as `plansFolder` in `.copilot/plan-critique-config.json`
   - Create the folder if it doesn't exist
   - Create an `archived/` subfolder inside it
3. Determine the plan name:
   - If the user passed a name in the prompt that invoked this skill, use it directly.
   - Otherwise, ask the user directly, do not offer predefined options like "New Feature" or "Bug Fix"
     because the plan name must be unique: "Enter a name for this plan:"
   The plan name must have at least 3 characters. If it is empty or shorter, respond with
   "Plan name must be at least 3 characters." and ask the user to enter one.
4. Generate a slug from the plan name:
   - Convert to lowercase
   - Replace spaces with hyphens
   - Remove characters that are not alphanumeric or hyphens
   - Trim to max 50 characters
   - Example: "Add User Authentication" becomes `add-user-authentication`
5. Check if `[plansFolder]/[slug]/` already exists.
   If it does: Respond with "A plan with this name already exists at `[plansFolder]/[slug]/`. Choose a different name."
   Ask for a new name and repeat from step 4.
6. Create directory `[plansFolder]/[slug]/`
7. Link this session to the new plan:
   - Get the Copilot CLI session id from the `COPILOT_AGENT_SESSION_ID` environment variable. Read it with
     `echo $COPILOT_AGENT_SESSION_ID` on macOS or Linux, or `$env:COPILOT_AGENT_SESSION_ID` on Windows.
     If the variable is empty, use the literal value `default` instead. Store this as `sessionId`.
   - Create the sessions directory if needed: `[plansFolder]/.sessions/`
   - Write the slug to `[plansFolder]/.sessions/[sessionId]` (plain text, just the slug)
8. Create the plan template at `[plansFolder]/[slug]/plan.md` using the template in
   [plan-template.md](plan-template.md).
9. Respond with confirmation:
   ```
   Created new plan: [plansFolder]/[slug]/
   Edit your plan at: [plansFolder]/[slug]/plan.md
   When ready, run `/plan-critique` to review your plan.
   ```

Notes:

- The slug must be filesystem-safe (no special characters)
- Keep the original plan name with proper casing in the H1 heading of plan.md
- Only create plan.md initially (critique.md is created by `/plan-critique`)
- Always use `plansFolder` from settings as the base directory
- Add `[plansFolder]/.sessions/` to `.gitignore`, these are local session files that should not be committed
