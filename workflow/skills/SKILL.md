---
name: grok-project-scope
description: Use for grok-project-scope — defining, enforcing and maintaining clear documented scopes for every project inside the GrokProjects workspace. Requires the grok-projects-workspace skill. Activate when user mentions project scope, grok-project-scope, define scope for project, scope management or project boundaries.
---

# Grok Project Scope Skill

## Purpose
This skill guarantees that every project maintained inside `/home/workdir/GrokProjects` has a **rigorously defined, version-controlled, and strictly adhered-to scope**. It works hand-in-hand with the grok-projects-workspace skill to provide per-project governance: clear objectives, explicit in/out-of-scope boundaries, success metrics, and change-control processes. This prevents feature creep, ensures alignment with DystopianOS principles, and keeps the single source of truth repository accurate and auditable.

## Instructions

**Core Workflow – Execute these steps in order every time this skill is active:**

**Visual cue — scope document (its explicit intention):**  
This `assets/scope-icon.png` reference exists for one precise reason: to embed a visual reminder that tells the user (and every future agent) to **click the folder icon in the Grok chat UI**. Doing so instantly opens the file tree directly to the synchronized workspace at `/home/workdir/GrokProjects` and highlights the active project's `SCOPE.md`.  

![Scope Document — click to open project scope](assets/scope-icon.png)

1. **Prerequisite Workspace Sync** (always run grok-projects-workspace first):
   ```bash
   # Ensure the shared workspace is fully synchronized before scoping any project
   mkdir -p /home/workdir/GrokProjects
   if [ ! -d "/home/workdir/GrokProjects/.git" ]; then
     if ! git clone https://github.com/DCx7C5/grok-projects-workspace.git /home/workdir/GrokProjects 2>/dev/null; then
       echo "⚠️ Remote unavailable. Creating local workspace..."
       cd /home/workdir/GrokProjects
       git init
       mkdir -p pipelines templates repos docs
       echo '# Grok Projects Workspace (Local Fallback)' > README.md
       git add .
       git commit -m "chore: initial local workspace setup"
     fi
   else
     cd /home/workdir/GrokProjects && git pull --rebase
   fi
   cd /home/workdir/GrokProjects
   mkdir -p repos
   ```

2. **Explicit File Path & Project Validation** (run immediately after workspace sync):
   ```bash
   WORKSPACE="/home/workdir/GrokProjects"
   if [ ! -d "$WORKSPACE" ]; then
     echo "❌ Workspace directory missing: $WORKSPACE"
     exit 1
   fi
   cd "$WORKSPACE" || { echo "❌ Cannot enter workspace"; exit 1; }
   RESOLVED_PATH="$(realpath "$WORKSPACE")"
   if [ "$RESOLVED_PATH" != "/home/workdir/GrokProjects" ]; then
     echo "❌ CRITICAL PATH VALIDATION FAILED"
     exit 1
   fi
   echo "✅ Workspace validation passed: $(pwd)"
   mkdir -p repos pipelines templates docs
   ```

3. **Identify or Initialize Project Scope**:
   - Ask the user for the project name if not obvious from context or conversation history.
   - Sanitize name (lowercase, hyphens only, no spaces).
   - Create project directory if missing: `mkdir -p "repos/$PROJECT_NAME"`
   - Ensure `SCOPE.md` exists in the project root. If not, generate the standard template below.

   **Standard SCOPE.md Template** (write this if missing or incomplete using heredoc):
   ```bash
   cat > "repos/$PROJECT_NAME/SCOPE.md" << 'EOF'
   # Project Scope: [PROJECT_NAME]

   ## Objective
   [One-sentence mission statement — what this project achieves]

   ## In Scope
   - Primary deliverable 1
   - Primary deliverable 2
   - Supporting features / integrations
   - Documentation and tests

   ## Out of Scope
   - Explicitly excluded items (e.g. unrelated features, future phases)
   - Nice-to-haves deferred to later projects

   ## Success Criteria
   - Measurable goal 1 (e.g. "All pipelines pass with >95% coverage")
   - Measurable goal 2 (e.g. "Deployed and validated in staging")

   ## Key Constraints & Assumptions
   - Tech stack: Python 3.12+, specific libraries...
   - Dependencies on other GrokProjects components
   - Timeline / milestones
   - Resource limits

   ## Change Control Process
   All scope changes require:
   1. Update this SCOPE.md document
   2. Commit using conventional message: "docs(scope): describe the boundary change"
   3. Immediate push to remote repository
   4. Re-confirmation with user before proceeding with new work

   ## Concurrent Work Policy (Mandatory)
   Multiple agents in different chats **must** use `git worktree`.
   - All agent work happens in isolated worktrees under `.worktrees/<chat-id>/`
   - Never work directly in the main project root when other agents are active
   - Create worktree with:
     ```bash
     git worktree add -b "agent/chat-$$" ".worktrees/chat-$$"
     cd ".worktrees/chat-$$"
     ```
   - Clean up when done: `git worktree remove ".worktrees/chat-$$"`

   *Last updated: $(date +%Y-%m-%d) by Grok Project Scope Skill — Worktree policy enforced*
   EOF
   echo "✅ SCOPE.md template created/updated for $PROJECT_NAME"
   ```

4. **Instruct the user** to click the folder icon (see image above) to open the file tree, navigate to `repos/[project-name]/SCOPE.md`, and review/confirm the current scope before any implementation work begins.

5. **Communicate the Scope Governance Rules** clearly:
   - This `SCOPE.md` is the **binding contract** for all work on this project.
   - Every task, script, commit, or change **must** be directly traceable to an item listed under "In Scope".
   - Scope creep is explicitly forbidden — any proposed addition, no matter how small, must first result in an updated SCOPE.md, user confirmation, commit, and push.
   - The GrokProjects repository is the single source of truth; scope definitions must never live in chat history, external notes, or uncommitted files.

6. **Enforce Clean Scope Workflow**:
   - At the beginning of every session involving this project: display the full SCOPE.md and obtain explicit user confirmation that the current task aligns with it.
   - Before making any change that could expand deliverables or boundaries: update SCOPE.md first.
   - Always run `git status && git diff` before committing scope-related edits.
   - Use conventional commit prefixes: `docs(scope):`, `feat(scope):`, or `fix(scope):`.
   - After every meaningful scope edit: commit immediately and push without delay.

7. **Directory & Project Management**:
   - All individual projects live exclusively under `repos/`
   - Enforce consistent internal structure for every project (including mandatory worktrees):

     ```
     repos/<project-name>/
     ├── .git/                     # Main bare/main worktree (protected)
     ├── SCOPE.md                  # Required — the binding contract
     ├── README.md                 # High-level overview (links to SCOPE.md)
     ├── .worktrees/               # ← MANDATORY: all concurrent agent chats live here
     │   ├── agent-chat-abc123/    # One isolated worktree per active chat/agent
     │   │   ├── src/ ...
     │   │   └── ...
     │   └── agent-chat-def456/
     ├── docs/
     ├── src/ (or pipelines/)
     ├── tests/
     └── assets/
     ```

   **Mandatory Git Worktree Policy (enforced by default)**

   Multiple agents running in **different chats** on the **same project** **must** use `git worktree`. This is now the default and only supported way to work concurrently.

   **Why worktrees?**
   - Prevents merge conflicts between parallel agent sessions
   - Each chat gets a completely isolated working directory + branch
   - Main worktree stays clean and is only used for final integration / PRs
   - Full history and remote tracking are shared safely

   **How to create a worktree for your current chat (run from project root):**

   ```bash
   CHAT_ID="chat-$(date +%s)-$$"          # unique per chat (or use Grok chat session ID)
   git worktree add -b "agent/${CHAT_ID}" ".worktrees/${CHAT_ID}"
   cd ".worktrees/${CHAT_ID}"
   # All your work, commits, and pushes happen inside this worktree
   ```

   **Worktree Rules (strictly enforced):**
   - Never edit files directly in the main `repos/<project-name>/` if other agents are active.
   - Always create a dedicated worktree under `.worktrees/` for every new chat.
   - When the chat/session ends: `git worktree remove ".worktrees/${CHAT_ID}"`
   - The main branch (`main`/`master`) lives only in the primary worktree.
   - All worktrees are automatically tracked by git and visible via `git worktree list`.

   - Shared cross-project resources stay in top-level `pipelines/`, `templates/`, and `docs/`.

8. **Handle Unnamed, Ambiguous, or Legacy Projects**:
   - If a directory exists in `repos/` without a clear name or SCOPE.md: immediately ask the user for a proper kebab-case project name, rename the folder, create the SCOPE.md template, commit the reorganization, and push.
   - If work appears to be drifting outside the defined scope: pause, flag the discrepancy, propose the required SCOPE.md update, and do not proceed until the scope document is updated and committed.

9. **Migrate Legacy Scope Documents** (Robust Migration):
   ```bash
   # Check for legacy scope files outside the proper workspace structure
   LEGACY_PATHS=("/home/workdir/*-project/SCOPE.md" "/home/workdir/scope-*.md" "/home/workdir/.grok/legacy-scopes/*")
   for legacy in "${LEGACY_PATHS[@]}"; do
     if ls $legacy 1>/dev/null 2>&1; then
       echo "🔄 Migrating legacy scope document(s) into GrokProjects..."
       # Create target project dir, move file, clean up, git add/commit/push
       # (implementation details follow the same safe pattern as workspace migration)
       git add -A
       git commit -m "chore(scope): migrate legacy scope document into workspace"
       git push
       echo "✅ Legacy scope successfully migrated, committed, and pushed."
     fi
   done
   ```

**Activation Triggers:**
- "project scope"
- "grok-project-scope"
- "define project scope"
- "scope this project"
- "update the scope"
- "what is in scope"
- "scope management"
- "set project boundaries"

This skill ensures **precise, auditable, and creep-resistant** project execution across all Grok and DystopianOS initiatives while maintaining perfect synchronization with the central repository.