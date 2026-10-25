---
name: ami-plan-commits
description: Analyzes the working tree for uncommitted work, proposes a structured set of commits, waits for user approval, and executes them.
allowed-tools: Bash, Read
---

# Skill: Commit Planner

When this skill is invoked (either by the user or by an agent), you must act as a Git Commit Strategist. Your goal is to group related changes into meaningful commits and propose a clear and concise commit plan to the user for approval. Clear commits makes it easier to find regressions and revert unwanted changes.

## Workflow
1. **Analyze Worktree Context, Working Tree State & Local History:** 
   - Check the current active worktree path (`git rev-parse --show-toplevel`) and checked-out branch (`git branch --show-current`).
   - List all registered worktrees (`git worktree list --porcelain`). If multiple worktrees exist, inspect if pending uncommitted changes are present in other linked worktrees (`git -C "<path>" status --short`). If changes reside in a different worktree, clearly inform the user and request confirmation on which worktree to target.
   - Run `git status --porcelain` to identify all uncommitted modified, added, untracked, and deleted files.
   - **Binary & Asset Recognition Rule:** Never assume `0 insertions, 0 deletions` means "no changes". Inspect all status flags (`M`, `??`, `A`, `D`) for binary assets (`.ico`, `.png`, `.icns`, fonts, media, datasets) as well as text files.
   - Use `git diff`, `git diff --cached`, and `git log @{u}..HEAD` (or `git log -n 5 --oneline`) to inspect textual diffs and unpushed local commits.
2. **Security, Data Leak & Untracked File Vetting:**
   - Scan all untracked files (`??`) against common exclusion patterns: build directories (`dist/`, `build/`, `out/`), package/virtual environments (`node_modules/`, `.venv/`), temporary caches, logs, and sensitive environment files (`.env`, `.env.local`).
   - If any untracked build artifacts or private files are detected, **ABORT** commit staging, alert the user, and propose updating `.gitignore` first.
   - **UI Mockups & Scratch Asset Vetting:** If untracked mockups exist outside `docs/mockups/` (e.g., in `<scratch>/` or workspace root), ask the user whether to formalize them under `docs/mockups/<feature-slug>.html` as living visual specifications or delete them before committing.
   - Actively scan all diffs and uncommitted files to ensure no sensitive credentials (API keys, tokens, passwords, private certificates, PII) are staged. If any leak is detected, abort immediately and refuse to commit.
3. **Structure & Group Changes:** Carefully analyze the modifications and group them into logical, distinct commits. Avoid lumping unrelated changes into a single monolithic commit. Consider the following grouping strategies:
   - **Amend Strategy:** If the current uncommitted work consists of minor fixes, typos, or additions to the most recent **unpushed** commit, propose amending it (`git commit --amend`) instead of adding a redundant commit.
   - **Squash / Consolidation Strategy:** If there are multiple unpushed local commits that represent iterative WIP or fragmented fixes for a single feature/component, propose squashing them into a single clean commit.
   - **By Conventional Commit Type:** Separate new features (`feat:`), bug fixes (`fix:`), refactors (`refactor:`), documentation updates (`docs:`), and maintenance chores (`chore:`). Approved interactive mockups in `docs/mockups/*.html` must be committed as documentation living specs (`docs(mockups): add interactive UI mockup for <feature>`).
   - **By Component or Architectural Layer:** Group changes related to a specific domain (e.g., frontend UI versus backend logic, or a specific module).
   - **By Distribution & Package Scope (Product vs. Internal/Docs):** Separate distributed package/product code (`feat:`, `fix:`) from repository-internal instructions and local developer/AI configurations (such as `.agents/`, `.claude/`, `.cursor/`, `.gemini/` guidelines or workspace settings), setup tooling, and project documentation (`docs:`). Internal developer guidelines and standalone documentation should not be grouped into product package commits unless strictly coupled.
   - **By Feature or Logical Unit:** Group files that work together to solve a single problem or complete a specific sub-task.
   *Note: If all changes are tightly coupled and represent a single cohesive unit of work, grouping them into a single commit (or amending) is perfectly acceptable. Avoid over-fragmenting commits unnecessarily.*
4. **Draft Messages & Plan:** For each proposed commit group (or amend/squash operation), formulate a clear and descriptive commit message in English. You **must** use the appropriate Conventional Commit prefix (`feat:`, `fix:`, `docs:`, `chore:`, `refactor:`, `test:`, `style:`). List the specific files associated with each commit. Your messages should be concise but highly descriptive, explaining *why* the change was made, not just *what* changed.
   - **Internal Planning Reference Prohibition (Phases, Stages, Options):** Commit messages MUST NEVER reference internal execution phases, stages, steps, or design options (e.g., 'Phase 1', 'Stage 2', 'Etapa 3', 'Option A', 'Opción B', 'Step 2 of plan') from internal planning dialogues, scratchpads, prompt plans, or task checklists not exposed in the repository (and it is not necessary to expose them, only not reference them). Commit messages become permanent repository history; describe changes strictly from an architectural, domain, and functional perspective.
5. **Request Approval:** Present the complete commit plan to the user in the chat, explicitly declaring the active worktree path and branch (including security audit confirmation and any proposed amend/squash operations). Ask for their approval and iterate if necessary. **NEVER** stage, commit, amend, or rebase anything until the user gives their explicit approval.
6. **Execute:** Once approved, use `git add`, `git commit`, `git commit --amend`, or rebase/squash commands to execute the plan exactly as agreed.
7. **Reporting:** After executing the plan, show the user the commits you just created using the `git log -n 5 --oneline` command to confirm the changes and that the skill worked as expected.

---
**Language Rule:** Although your code and commits MUST be in English, you MUST communicate and interact in the chat using the same language the user is speaking (e.g., Spanish, French, etc.).
