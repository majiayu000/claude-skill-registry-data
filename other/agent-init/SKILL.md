---
name: agent-init
description: Interactive project setup wizard — creates agent.yaml, .workflow/ scaffold, and .gitignore entries for the Claude Agent framework
---

# Agent Init Skill

When this skill is invoked with `/agent-init`, run the interactive project setup
wizard below. Do NOT skip steps. Do NOT write any files until you have confirmed
all values with the user in Step 4.

---

## Step 0: Detect Project Mode

Recursively search the current directory tree for `.git/` directories. Use:
```
find . -type d -name ".git" -not -path "*/.git/*"
```
Strip the trailing `/.git` from each result to get the repo root paths.
Exclude the current directory itself (`./.git`) — that means the current
directory is already a repo and should be treated as single-repo mode.
Collect every subdirectory path that contains a `.git/`.

- If **no subdirectories contain `.git/`**: run in **single-repo mode**
  (proceed to Step 1-S).
- If **one or more subdirectories contain `.git/`**: list them (relative paths)
  and ask:
  > "Found git repos in subfolders: `<list>`. Set this up as a multi-repo
  > project? [Y/n]"
  - Answer **Y** → **multi-repo mode** (proceed to Step 1-M).
  - Answer **N** → **single-repo mode** on the current directory (proceed to Step 1-S).

---

## Stack Detection Helper

Use this logic whenever you need to detect the stack for a directory. Read
these files in priority order using your Read tool:

1. Any `*.xcodeproj` or `*.xcworkspace` directory → **ios**
2. `Cargo.toml` → **rust**
3. `Package.swift` → **swift**
4. `gradlew` OR `settings.gradle` OR `settings.gradle.kts` → **android**
5. Any `*.csproj` or `*.sln` file → **dotnet**
6. `manage.py` → **django**
7. `package.json` → **node**
8. `requirements.txt` OR `setup.py` OR `pyproject.toml` OR `Pipfile` → **python**
9. `CMakeLists.txt` OR (`Makefile` without `package.json`) → **c**
10. `project.godot` → **godot**
11. else → **base**

**Stack defaults:**

| Stack | test_command | test_dir | test_pattern | build_command | container |
|---|---|---|---|---|---|
| rust | `cargo test` | `tests/` | `*_test.rs` | `cargo build --release` | rust |
| swift | `swift test` | `Tests/` | `*Tests.swift` | `swift build` | swift |
| ios | *(disabled — built on remote Mac)* | `<Project>Tests/` | `*Tests.swift` | *(empty — built on remote Mac)* | base |
| android | `./gradlew test` | `app/src/test/` | `*Test.kt` | `./gradlew assembleDebug` | android |
| dotnet | `dotnet test` | `tests/` | `*Tests.cs` | `dotnet build` | dotnet |
| django | `python manage.py test` | `tests/` | `test_*.py` | `` | base |
| node | `npm test` | `tests/` | `*.test.ts` | `npm run build` | node |
| python | `pytest -v` | `tests/` | `test_*.py` | `` | python |
| c | `make test` | `tests/` | `test_*.c` | `make` | c |
| godot | `godot --headless --quit` | `tests/` | `test_*.gd` | `` | godot |
| base | `` | `tests/` | `test_*` | `` | base |

**Default code standards by stack** (shown to user in Group F, editable):

- **node**: TypeScript strict mode enabled. Source in `src/`. Tests in `tests/` with Jest or Vitest. ESLint + Prettier for formatting. No `console.log` in production code. Pin dependencies with package-lock.json.
- **python**: Type hints required. Docstrings on all public functions. Black formatter. Ruff linter. No bare `except:`. Use pathlib over os.path.
- **rust**: Safe Rust only (no `unsafe` without a comment explaining why). `clippy` must pass. `rustfmt` for formatting. Document all public items.
- **django**: Follow Django coding style. Use class-based views. All DB queries go through the ORM. No raw SQL unless unavoidable. All endpoints require authentication unless explicitly public.
- **android**: Kotlin preferred over Java. Coroutines for async. ViewModel + LiveData or StateFlow for UI state. Follow Google's Android Architecture Guidelines.
- **dotnet**: C# nullable reference types enabled. Async/await throughout. Follow Microsoft's .NET coding conventions.
- **swift**: Swift concurrency (async/await) preferred. No force-unwrapping without a comment. Follow Swift API Design Guidelines.
- **c**: ANSI C99 or C11. All allocations checked for NULL. No global mutable state. Valgrind-clean.
- **godot**: GDScript 4 with static typing. Signals for decoupled communication. No direct node path strings — use exports.
- **base**: Follow the conventions already established in this codebase.

---

## Single-Repo Mode

### Step 1-S: Detect Stack and Git State

1. Run stack detection on the current directory.
2. Read `.git/HEAD` to get the current branch name (default: `main` if no `.git/`).
3. Run `git config --global user.name` and `git config --global user.email`.

If no `.git/` directory exists, note this — you will warn the user in Step 6-S.

### Step 2-S: Ask Questions

Ask questions one group at a time. Show the detected default in brackets.
The user presses Enter to accept a default.

**Group A — Identity**
1. "Project name? [`<dir basename>`]"
2. "One-sentence description of what this project does?"

**Group B — Co-author** (show as confirmation if git config was found)
3. "Your name for commit co-authorship? [`<git config user.name>`]"
4. "Your email? [`<git config user.email>`]"

**Group C — Stack confirmation**
5. "Detected stack: **`<stack>`** (from `<file>`). Is this correct? [Y/n]"
   - If no: "Options: rust / swift / android / dotnet / django / node / python / c / godot / base. Which one?"

**Group D — Testing**
6. "Testing enabled? [Y/n]"
7. (If yes) "Test command? [`<stack default>`]"
8. (If yes) "Test directory? [`<stack default test_dir>`]"

**Group E — Build** (skip if stack has no build command)
9. "Build command? [`<stack default>`]" (press Enter to leave empty)

**Group F — Code standards**
10. "Here are default code standards for `<stack>`:

    `<show the code standards block for this stack from the table above>`

    Edit these or press Enter to accept:"

**Group G — Design tokens** (only for node, django, python stacks — UI-likely)
11. "Does this project have a UI with design tokens? [y/N]"
    - If yes, ask in sequence:
      - "Primary color? (hex or CSS, e.g. #3B82F6)"
      - "Secondary color?"
      - "Background color?"
      - "Surface color?"
      - "Text color?"
      - "Heading font family?"
      - "Body font family?"
      - "Monospace font family?"
      - "Visual mood? (e.g. clean and minimal, bold and energetic, warm and friendly)"

**Group H — GitHub** (optional)
12. "GitHub repo in `owner/repo` format for issue triage? [skip]"
13. (If provided) "Labels to exclude from triage? [question, wontfix, duplicate, invalid]"

**Group I — Workflow backend**
14. "Workflow backend?
    (a) `markdown` — track work in local `.workflow/*.md` files (default; what every existing project uses).
    (b) `github_project` — track work on a GitHub Project board (FEATURE/CHANGE/BUG issues, sub-issue tasks, plans posted as comments).
    Choice [a/b]?"

15. (Only if `github_project` was chosen) Collect:
    - "GitHub owner (user or org)? [`<auto-detected from git remote>`]"
    - "Repo (`owner/repo`)? [`<auto-detected>`]"
    - "Existing project number? [blank to create new]"
    - (If creating) "Project title? [`<project name> board`]"

    Then verify `gh auth status` shows the `project` scope. If missing,
    print: "GitHub token is missing the `project` scope. Run
    `gh auth refresh -s project` and re-run `/agent-init`." and exit
    without writing anything.

### Step 3-S: Confirm

Show a YAML preview of `agent.yaml` before writing anything. Ask:
"Write these files to the current directory? [Y/n]"

If `agent.yaml` already exists in the current directory:
"⚠️ `agent.yaml` already exists. Overwrite it? [y/N]"

### Step 4-S: Write Files

**`agent.yaml`:**

```yaml
project:
  name: "<PROJECT_NAME>"
  description: "<PROJECT_DESCRIPTION>"

git:
  default_branch: "<DEFAULT_BRANCH>"
  feature_prefix: "feature/"
  commit_style: "conventional"
  co_author: "<CO_AUTHOR>"

workflow:
  plans_dir: ".workflow/plans"
  reports_dir: ".workflow/reports"
  logs_dir: ".workflow/logs"
  worktrees_dir: ".workflow/worktrees"
  backlog_file: ".workflow/BACKLOG.md"
  todo_file: ".workflow/TODO.md"
  done_file: ".workflow/DONE.md"
  bugs_file: ".workflow/BUGS.md"
  backend: "<BACKEND>"  # markdown | github_project

testing:
  enabled: <TESTING_ENABLED>
  command: "<TEST_COMMAND>"
  test_dir: "<TEST_DIR>"
  test_pattern: "<TEST_PATTERN>"

build:
  command: "<BUILD_COMMAND>"

code_standards: |
  <CODE_STANDARDS_BLOCK>

container:
  template: "<CONTAINER_TEMPLATE>"
  memory: "8G"
  cpus: "4"

agents:
  default_type: "coder"
  tasks_dir: ".workflow/tasks"
  max_workers: 3
```

Omit the `design:` block if the user said no to design tokens.
If design tokens were collected, insert before `container:`:
```yaml
design:
  colors:
    primary: "<PRIMARY>"
    secondary: "<SECONDARY>"
    background: "<BACKGROUND>"
    surface: "<SURFACE>"
    text: "<TEXT>"
  fonts:
    heading: "<HEADING_FONT>"
    body: "<BODY_FONT>"
    mono: "<MONO_FONT>"
  mood: "<MOOD>"
```

If GitHub repo was provided, append at the end:
```yaml
github:
  repo: "<GITHUB_REPO>"
  exclude_labels:
    - question
    - wontfix
    - duplicate
    - invalid
```

If backend = `github_project`, ALSO insert under the `workflow:` block:
```yaml
  github_project:
    owner: "<GITHUB_OWNER>"
    number: <PROJECT_NUMBER>
    repo: "<GITHUB_REPO>"
```

**Markdown workflow files (only when `backend == markdown`).** Skip these
four files entirely if backend = `github_project` — the GitHub Project board
becomes the source of truth and these would just drift.

**`.workflow/BACKLOG.md`:**
```markdown
# Backlog

Raw, unprocessed features and ideas. Items here have not been researched,
planned, or estimated. This is the intake queue.

Add items as `[ ]` checkbox entries under the appropriate section. The
Coordinator runs the Refinement stage (Architect → Designer → Manager) to
research, plan, and decompose items into tasks, then moves them to TODO.md.

---

## Features

New functionality that does not currently exist.

- [ ] First feature or task (describe it clearly)

## Changes

Updates or improvements to existing functionality.

## Issues

Possible bugs, regressions, or things that feel broken or degraded.
```

**`.workflow/TODO.md`:**
```markdown
# TODO

Stakeholder-approved work ready for worker agents. Items here have been
researched, planned, and approved — they are ready to implement.

Worker agents (coder, designer, automation, qa, code-reviewer) pick up
`[ ]` items from this file.

---

```

**`.workflow/DONE.md`:**
```markdown
# Done

Completed work. Features moved here after implementation, review, and merge
to the default branch.

---

```

**`.workflow/BUGS.md`:**
```markdown
# Bugs

Known bugs discovered by QA and Code Reviewer agents. Each bug should have
enough detail for a Coder agent to reproduce and fix it.

Bugs here follow the same approval flow as features — the stakeholder moves
approved fixes to TODO.md (removing them from this file).

---

```

**Directories** (create with `.gitkeep`, both backends):
- `.workflow/plans/`
- `.workflow/reports/`
- `.workflow/logs/`
- `.workflow/worktrees/`
- `.workflow/tasks/`
- `.workflow/container/`
- `.workflow/temp/` (board-man scratch — auto-gitignored)

**`.gitignore`** — append these lines if not already present (check before appending):
```
# Agent worktrees (created and destroyed at runtime)
.workflow/worktrees/*
!.workflow/worktrees/.gitkeep

# Claude project-level memory (contains local paths and session data)
.claude/projects/

# board-man scratch space (downloaded plan comments, ID cache, write lock)
.workflow/temp/

# OS
.DS_Store
Thumbs.db

# Editor
*.swp
*.swo
*~
.vscode/
.idea/

# Agent container config (regenerated per run)
.workflow/container/docker-compose.yml
```

### Step 4b-S: Provision the GitHub Project (only when `backend == github_project`)

Skip this step entirely for `markdown` backend.

1. **Provision the board.** Locate the framework directory: `$CLAUDE_AGENT_HOME`
   if set, otherwise default to `$HOME/.claude-agent`. Run:
   ```
   <framework>/scripts/board-man-setup.sh --owner <GITHUB_OWNER> --repo <GITHUB_REPO> [--number <PROJECT_NUMBER>] [--title "<TITLE>"] --project-root <pwd>
   ```
   This creates the project (if no number was given), provisions labels
   (FEATURE, CHANGE, BUG, TASK, parallel-group/0..9), ensures Status options
   BACKLOG/READY/TODO/IN-PROGRESS/DONE, ensures the Parallel Group number
   field, and writes `.workflow/temp/.board-man-cache.json`.

   If the script exits non-zero, surface the stderr and stop. The project
   board cannot be partially provisioned safely.

2. **Per-project install.** Copy the framework skills + agents into this
   project so the project pins to a specific framework commit:
   ```
   <framework>/scripts/install-skills-local.sh <pwd>
   ```
   This writes `.claude/skills/<n>/SKILL.md`, `.claude/agents/<n>/CLAUDE.md`,
   and a `.claude/skills/.framework-version` stamp.

3. **Issue templates.** Copy the FEATURE/CHANGE/BUG/TASK forms:
   ```
   mkdir -p .github/ISSUE_TEMPLATE
   cp -n <framework>/templates/.github/ISSUE_TEMPLATE/*.yml .github/ISSUE_TEMPLATE/
   ```
   Use `cp -n` so existing project templates are never clobbered.

### Step 5-S: Report

List all files created (✓) or skipped (↷). Then:

**If `backend == markdown`:**
"**Next steps:**
1. Add your first feature to `.workflow/BACKLOG.md`
2. Run `/agent` to work through features as a standalone agent
3. Run `/coordinator` to use the full orchestrated pipeline"

**If `backend == github_project`:**
"**Next steps:**
1. Open the project board: https://github.com/users/<GITHUB_OWNER>/projects/<PROJECT_NUMBER>
   (or https://github.com/orgs/<GITHUB_OWNER>/projects/<PROJECT_NUMBER> for org-owned).
2. File your first item via https://github.com/<GITHUB_REPO>/issues/new/choose
   — pick the FEATURE / CHANGE / BUG template.
3. Run `/coordinator` — it will pick up BACKLOG items via board-man and
   drive the full pipeline against the board.
4. Skills + agents were copied to `.claude/` (frozen at the current framework
   commit). Re-run `<framework>/scripts/install-skills-local.sh <pwd>` after
   pulling framework updates to refresh."

If no `.git/` directory was found:
"⚠️ No git repository detected. Run `git init` before using the agent workflow — worktrees and branching require git."

---

## Multi-Repo Mode

### Step 1-M: Shared Identity

Ask once for the whole project:
1. "Project name? [`<root dir basename>`]"
2. "One-sentence description of the overall system?"
3. "Your name for commit co-authorship? [`<git config user.name>`]"
4. "Your email? [`<git config user.email>`]"

### Step 2-M: Per-Repo Configuration

For each detected subproject repo, in turn, first ask whether it's a
mono-repo parent (one repo containing multiple independently-built
sub-projects, e.g. `mobile/` with `ios/`, `android/`, `device_lib/`):

"**`<subdir>/`** — Is this a mono-repo parent with its own sub-projects? [y/N]"

**If NO (leaf repo):** run stack detection on that subdir and ask:

"**`<subdir>/`** — Detected stack: `<stack>` (from `<file>`). Correct? [Y/n]"

**Fastlane check (iOS and Android stacks only).** If the detected stack is
`ios` or `android`, check for fastlane by looking for `fastlane/Fastfile`
or a root-level `Fastfile`. If found:
- Grep the Fastfile for `lane :<name>` lines to collect lane names.
- If a `test` lane exists, propose `fastlane test` as the default test command.
- If a `build` lane exists, propose `fastlane build` as the default build command.
  Otherwise, fall back to the first non-test lane that looks build-shaped
  (`beta`, `release`, `adhoc`, `archive`) and propose `fastlane <that lane>`.
- Tell the user: "Detected fastlane with lanes: <list>. Use
  `fastlane <name>` for testing/build? [Y/n]"
- If the user declines, fall back to the stack defaults below.

Then ask for that repo:
- "Testing enabled? [Y/n]"
- (If yes) "Test command? [`<fastlane default or stack default>`]"
- (If yes) "Test directory? [`<default>`]"
- "Build command? [`<fastlane default or stack default>`]" (skip if no build cmd for stack)
- "Code standards for `<subdir>/`?" (show pre-filled block, invite edits)
- "UI project? [y/N]" → if yes: colors + fonts (same as Group G above)
- (If stack is `ios` or `swift`-with-an-xcodeproj) "Mac build SSH host for
  this iOS target? (e.g. `builder@mac-pool-1.internal`) [skip]"
- (If the Mac host was provided) "Mac build scratch workspace?
  [`/tmp/claude-agent-builds`]"

**If YES (mono-repo parent):** enumerate immediate sub-directories. For each
one, recurse the *leaf* question set above (stack, testing, build, code
standards, iOS Mac host if applicable). Record each sub-project's id
(sub-directory name), stack, path (relative to the mono-repo), and gathered
config. Also ask:
- "Cross-sub-project code standards for `<subdir>/`? (API contracts, FFI
  rules — rules that apply across sub-projects, not to any one stack)"

Only one level of mono-repo nesting is supported. A sub-project cannot
itself be a mono-repo.

Ask once at the end:
- "GitHub repo in `owner/repo` format? [skip]"
- "Labels to exclude from triage? [question, wontfix, duplicate, invalid]"

### Step 3-M: Confirm

Show a summary table. Mono-repo parents are listed with their sub-projects
indented beneath them:

| Repo | Stack | Testing | Build | Mac host |
|------|-------|---------|-------|----------|
| backend/ | django | python manage.py test | (none) | — |
| mobile/ | mono-repo | — | — | — |
| · ios | ios | (disabled) | (remote) | builder@mac-pool-1 |
| · android | android | ./gradlew test | ./gradlew assembleDebug | — |
| · device_lib | rust | cargo test | cargo build | — |

Also preview the root `agent.yaml` `repos:` block. Ask:
"Write all files? [Y/n]"

If any `agent.yaml` or `agent-build.yaml` already exists in the listed
subdirs: name them and ask to overwrite.

### Step 4-M: Write Per-Repo Files

For each **leaf** sub-repo (and each sub-project of a mono-repo), write into
its directory:
- `agent-build.yaml` — slim per-repo build config, based on the stack's
  `templates/<stack>/agent-build.yaml.tmpl`. Fields: `mono-repo: false`,
  `stack`, `testing`, `build`, `code_standards`. For iOS leaves, also
  include the `mac_build.host/workspace` gathered in Step 2-M.

For each **mono-repo parent**, write into that directory:
- `agent-build.yaml` — mono-repo shape, based on
  `templates/mono-repo/agent-build.yaml.tmpl`. Fields: `mono-repo: true`,
  `stack: mono-repo`, `projects:` (list of `{id, stack, path, build}` for
  each sub-project), and the cross-sub-project `code_standards` gathered
  in Step 2-M.

**Do not write a full per-repo `agent.yaml` into sub-repos.** The root
`agent.yaml` is authoritative for project-level config (git, workflow,
agents, github). Per-repo config is confined to `agent-build.yaml`.

Write `.workflow/` scaffolds only at the project root (Step 5-M), not per
repo — the coordinator runs against the root and resolves sub-repo paths
on demand.

Append `.gitignore` entries at the project root only (same list as Step 4-S).

### Step 5-M: Write Root Files

Write root `agent.yaml`:

```yaml
project:
  name: "<PROJECT_NAME>"
  description: "<PROJECT_DESCRIPTION>"
  type: multi-repo

git:
  default_branch: "main"
  feature_prefix: "feature/"
  commit_style: "conventional"
  co_author: "<CO_AUTHOR>"

workflow:
  global_workspace: "<absolute path to root directory>"
  plans_dir: ".workflow/plans"
  reports_dir: ".workflow/reports"
  logs_dir: ".workflow/logs"
  worktrees_dir: ".workflow/worktrees"
  backlog_file: ".workflow/BACKLOG.md"
  todo_file: ".workflow/TODO.md"
  done_file: ".workflow/DONE.md"
  bugs_file: ".workflow/BUGS.md"
  push_enabled: false

repos:
  - id: <subdir1>
    path: <subdir1>
    stack: <stack1>
    build: <subdir1>/agent-build.yaml
  - id: <mono-parent>
    path: <mono-parent>
    stack: mono-repo
    build: <mono-parent>/agent-build.yaml
    # Sub-projects are defined in the mono-parent's agent-build.yaml.
    # Task files reference them via dotted form: `Repo: <mono-parent>.<subproject>`

agents:
  default_type: "coder"
  tasks_dir: ".workflow/tasks"
  max_workers: <number of leaf sub-repos + sub-projects>
```

**Do not write a root-level `mac_build` block.** iOS Mac hosts live in each
iOS leaf's `agent-build.yaml`.

If GitHub repo was provided, add:
```yaml
github:
  repo: "<GITHUB_REPO>"
  exclude_labels:
    - question
    - wontfix
    - duplicate
    - invalid
```

Write root `.workflow/` scaffold (coordinator uses this for plans/tasks/logs):
- `.workflow/BACKLOG.md`, `TODO.md`, `DONE.md`, `BUGS.md`
- `.workflow/plans/`, `reports/`, `logs/`, `worktrees/`, `tasks/`, `container/`

### Step 6-M: Report

List all files created per repo. Then:

"**Next steps:**
- Run `/agent` from any subproject folder to work on it independently
- Run `/coordinator` from the root directory to orchestrate the full stack"
