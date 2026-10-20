---
name: git-commit-push
description: >-
  Safe, structured git commit and push workflow with format script error gating,
  strict no-force-push, no pre-push test runs, Git LFS / large file warnings,
  surgical staging, and auto-commit with conventional commit messages. Use whenever
  the user asks to commit, push, save changes to git, or triggers /commit or /git-commit-push.
---

# Git Commit & Push Workflow

A reliable, guardrail-protected workflow for formatting, staging surgically, committing with conventional messages, and safely pushing changes across Git repositories.

> [!NOTE]
> **Branch Confirmation**: Handled by the **Pre-Modification & Commit Branch Confirmation Guard** in `GEMINI.md`. If the active branch has not yet been confirmed in this conversation (e.g. committing pre-existing changes), ensure the user confirms the branch once before staging and committing.

---

## 1. Pre-Push Formatting Check (NO Tests)

### A. Check & Execute Format Script
Before staging and committing, check the project root for existing code formatting scripts:
- **Node.js / npm / yarn / pnpm**: Check `package.json` for scripts named `"format"`, `"prettier"`, `"fmt"`, or `"lint:fix"`:
  ```bash
  npm run format   # or yarn format / pnpm format
  ```
- **Rust**: Check for `Cargo.toml` -> run `cargo fmt`
- **Python**: Check for `pyproject.toml` / `ruff.toml` / `.black` -> run `ruff format` or `black .`
- **Go**: Run `gofmt -w .`
- **C# / .NET**: Run `dotnet format`
- **If No Format Script**: If none of these scripts exist in the repository, skip directly to Section 2.

### B. STRICT ERROR GATE: Stop if Format Script Fails
- If `npm run format` (or equivalent) exits with an error (non-zero exit code):
  - **STOP COMMITTING AND PUSHING IMMEDIATELY.**
  - Output the formatting/linter error message to the user.
  - Do NOT stage, commit, or push until syntax or formatting errors are addressed.
- If the format script succeeds:
  - If the formatter modified any files, include those updated files in the surgical staging step so formatting is kept clean and consistent.

### C. STRICT CONSTRAINT: Do NOT Run Tests Before Push
- **DO NOT** execute test suites (`npm test`, `pytest`, `cargo test`, `go test`, etc.) prior to pushing.
- Keep the commit & push process fast, lean, and non-blocking unless the user explicitly asks to run tests.

---

## 2. Safety, Secret Leak & Git LFS / Large File Warnings

Before staging any files:

### A. Secret & Sensitive File Leak Detection
Scan `git status -s` and diffs for sensitive files:
- Environment configs: `.env`, `.env.local`, `*.env`, `.env.*.local`
- Keys & certificates: `*.pem`, `*.key`, `*.pkcs12`, `*.pfx`, `id_rsa`, `id_ed25519`
- Cloud & API secrets: `credentials.json`, `service-account*.json`, `token.txt`
- User configs: `.npmrc` (with auth tokens), `.pypirc`
- OS/editor junk: `.DS_Store`, `Thumbs.db`, `.idea/`, `.vscode/settings.json` (if workspace-specific)
> **ACTION**: If any sensitive file is detected, **ABORT** staging immediately, alert the user, and ensure the file is added to `.gitignore`.

### B. Git LFS & Large File Warning
- **Size Threshold**: Scan modified or untracked files for any file exceeding **5 MB**.
- **Binary & Model Assets**: Check for large binary blobs (`.bin`, `.onnx`, `.tar.gz`, `.zip`, `.mp4`, `.psd`, `.iso`, `.sqlite`, `.parquet`).
- **LFS Check**:
  - Check if the repository uses Git LFS (`git lfs status` or `.gitattributes`).
  - If a large file is **not** tracked by Git LFS:
    > ⚠️ **Large File / Git LFS Warning**: File `<file_path>` is `<size>MB` and not tracked by Git LFS. Committing it directly will bloat repository history permanently.
    - Warn the user before staging and ask whether to track it with Git LFS (`git lfs track "<pattern>"`) or add it to `.gitignore`.

---

## 3. Surgical Staging Over Blind Wildcards

**Strictly avoid `git add .` or `git add -A`.** Blind wildcards frequently introduce unintended debug logs, scratch files, or collateral edits into git history.

1. **Explicit File Staging**:
   Stage only the specific, relevant files for the current change:
   ```bash
   git add path/to/file1.ts path/to/file2.ts
   ```
2. **Review Staged State**:
   - Check staged status: `git status -s`
   - Inspect staged diff summary: `git diff --cached --stat`
   - Ensure zero collateral or unintended files are staged.
3. **Diff Sanity Scan**:
   Scan staged changes (`git diff --cached`) for leftover debug code:
   - `console.log`, `debugger`, `print()`, `dump()`, `binding.pry`, or temporary commented-out blocks.

---

## 4. Conventional Commits & Auto-Commit

Craft high-quality commit messages following the Conventional Commits specification:

### Format
```text
<type>(<optional-scope>): <short imperative description>

[optional body with concise bullet points explaining WHY and WHAT changed]

[optional footer(s): BREAKING CHANGE:, Closes #123]
```

### Allowed Types
- `feat`: New feature or user-facing functionality
- `fix`: Bug fix
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `perf`: Performance improvement
- `docs`: Documentation updates only
- `style`: Formatting, missing semicolons, whitespace (no logic change)
- `test`: Adding or correcting tests
- `chore`: Build tasks, package updates, repo configuration, metadata
- `ci`: CI/CD workflow updates

### Rules & Auto-Commit Execution
- First line MUST be under 72 characters.
- Use imperative mood in title ("add", not "added" or "adds").
- Focus the body on the *rationale* and *impact*, not a line-by-line code repetition.
- **Auto-Commit**: The agent can **automatically execute the commit** with the generated Conventional Commit message without an extra confirmation round on the message text.
- Always display the commit message and commit hash clearly in the final response.

---

## 5. Push Execution & Divergence Guard (STRICT: NO FORCE PUSH)

### A. STRICT: Never Force Push
- **NEVER** use `--force`, `-f`, or `--force-with-lease`.
- Force pushing risks overwriting collaborator work and destroying remote git history.
- If a push is rejected due to remote divergence (non-fast-forward):
  - **STOP immediately**.
  - Inform the user:
    > ⚠️ **Push Rejected**: Remote contains work not present locally.
  - Advise the user to pull and rebase cleanly:
    ```bash
    git pull --rebase origin <branch>
    ```

### B. Execution Steps
Once format check passes, files are surgically staged, and conventional commit message is generated:

1. **Auto-Commit**:
   ```bash
   git commit -m "<generated conventional commit message>"
   ```
2. **Push**:
   - Check if upstream branch is configured:
     ```bash
     git rev-parse --abbrev-ref --symbolic-full-name @{u}
     ```
   - If upstream tracking exists:
     ```bash
     git push
     ```
   - If no upstream tracking exists (new branch):
     ```bash
     git push -u origin <branch>
     ```
3. **Post-Push Summary**:
   Output a concise summary:
   - Commit hash (`git rev-parse --short HEAD`)
   - Branch pushed
   - Remote URL/repo
   - List of committed files
