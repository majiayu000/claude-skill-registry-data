---
name: openspec-new-change
description: Start a new OpenSpec change using the experimental artifact workflow. Use when the user wants to create a new feature, fix, or modification with a structured step-by-step approach.
license: MIT
compatibility: Requires openspec CLI.
metadata:
  author: openspec
  version: "1.0"
  generatedBy: "1.3.1"
---

**Project context preflight before workflow actions**: before this skill takes a workflow action, follow the `project-constitution` skill. Read root `CONSTITUTION.md` when present, enforce relevant project rules, stop on material conflicts, and follow the strict missing-constitution bootstrap/diagnostic policy. For architecture-sensitive work, also read `ARCHITECTURE.md`, `adr/README.md`, and relevant in-force `adr/*.md`. Read `.secrets.local.env` only when the current workflow actually needs a listed external system, and never reveal secret values.


**Artifact review session controls**: when `scripts/openspec-session-state` exists, inspect `artifactReview.decision` before key entry workflows create or consume reviewable artifacts. If the decision is `unset`, ask once whether to enable OpenAI-compatible artifact review for this session and record the answer with `--review on|off`; later commands reuse the recorded decision until the user changes it with the `/opsx:review-*` prompts. Session settings are non-secret local overlays and must not edit `.codex/openspec-artifact-review.json` unless the user explicitly asks for a global default change. Ordinary `scripts/openspec-artifact-review` runs use the session-effective config by default; explicit `--config` and `--raw-config` / `--ignore-session` bypass implicit session merge for diagnostics.

Start a new change using the experimental artifact-driven approach.

**Input**: The user's request should include a change name (kebab-case) OR a description of what they want to build.

**Steps**

**Git preflight before mutation**: run `git branch --show-current` and `git status --short` before creating the change. Prefer `main`; stop on unrelated dirty state unless the user explicitly overrides.


1. **If no clear input provided, ask what they want to build**

   Use the **Codex interactive user question tool when available, otherwise a concise Markdown question** (open-ended, no preset options) to ask:
   > "What change do you want to work on? Describe what you want to build or fix."

   From their description, derive a kebab-case name (e.g., "add user authentication" → `add-user-auth`).

   **IMPORTANT**: Do NOT proceed without understanding what the user wants to build.

2. **Determine the workflow schema**

   Use the default schema (omit `--schema`) unless the user explicitly requests a different workflow.

   **Use a different schema only if the user mentions:**
   - A specific schema name → use `--schema <name>`
   - "show workflows" or "what workflows" → run `openspec schemas --json` and let them choose

   **Otherwise**: Omit `--schema` to use the default.

3. **Create the change directory**
   ```bash
   openspec new change "<name>"
   ```
   Add `--schema <name>` only if the user requested a specific workflow.
   This creates a scaffolded change at `openspec/changes/<name>/` with the selected schema.

4. **Show the artifact status**
   ```bash
   openspec status --change "<name>"
   ```
   This shows which artifacts need to be created and which are ready (dependencies satisfied).

5. **Get instructions for the first artifact**
   The first artifact depends on the schema (e.g., `proposal` for spec-driven).
   Check the status output to find the first artifact with status "ready".
   ```bash
   openspec instructions <first-artifact-id> --change "<name>"
   ```
   This outputs the template and context for creating the first artifact.

6. **STOP and wait for user direction**

**Output**

After completing the steps, summarize:
- Change name and location
- Schema/workflow being used and its artifact sequence
- Current status (0/N artifacts complete)
- The template for the first artifact
- Prompt: "Ready to create the first artifact? Just describe what this change is about and I'll draft it, or ask me to continue."

**Guardrails**
- Checkpoint after the change scaffold is created; do not let dependent artifacts consume it until committed or explicitly overridden.
- In session git `auto` mode, safe scaffold checkpoint commits may run automatically after showing paths/message/hash; manual mode stops for approval.
- Do not merge, push, archive, run destructive git operations, or bypass hard gates without explicit user approval.
- Do NOT create any artifacts yet - just show the instructions
- Do NOT advance beyond showing the first artifact template
- If the name is invalid (not kebab-case), ask for a valid name
- If a change with that name already exists, suggest continuing that change instead
- Pass --schema if using a non-default workflow
