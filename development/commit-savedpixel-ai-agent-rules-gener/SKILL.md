---
name: commit
description: Stage, commit, and push code changes with branch safety and explicit staging. Use when ready to commit work. Invoked by saying "commit", "push", or "commit and push".
---

# Commit Your Changes

Stage, commit, and push **only the files you modified in this session** to the **current working branch**.

---

## Branch Safety (BLOCKING GATE)

1. **Check the current branch** — run `git branch --show-current`.
2. **If on `master` or `main`** — **STOP immediately**. Do not stage, commit, or push. Tell the user and wait.
3. **If on `dev`** — you may commit, but **do NOT push automatically**. After committing, ask: "Committed. Ready to push to dev?" Wait for explicit approval.
4. **Stay on the branch you started on.** Never switch branches just to commit.
5. Never push or commit directly to `master` or `main` unless explicitly instructed.

---

## Verification Gate (BLOCKING)

Before committing, confirm that **ALL** required verification steps from the task plan have passed. If any verification is blocked or incomplete, do **NOT** commit. Report the blocker. See `AGENTS.md` → Blocker Protocol.

---

## Steps

1. **Check `git status --short`** — Review all modified/untracked files. Identify which ones you touched.

2. **Stage only your files** — Use `git add` with explicit file paths. Never use `git add -A` or `git add .`.

3. **Write a high-quality commit message** using **multiple `-m` flags**.

   ### Subject Format
   ```
   <type>(<optional-scope>): <action-oriented summary>
   ```

   **Allowed Types:** `feat`, `fix`, `refactor`, `docs`, `style`, `data`, `config`, `chore`, `merge`

   **Rules:**
   - Keep subjects under ~80 characters
   - Use lowercase for type and scope
   - Start with a clear verb
   - Be specific, not generic

   ### Body
   - 2–3 `-m` flags max
   - Summarize key changes in 3–5 sentences
   - End with `Files: <key files>`

   ### Quick Rewrite Guide
   - `Updated gateway` → `feat(gateway): add support for digital wallet payments`
   - `fix stuff` → `fix(checkout): correct redirect URL for cancelled payments`

4. **Push to the current working branch** — If on `dev`, ask before pushing.

---

## Rules

- **Never stage files you did not change.**
- **Never use `git add .` or `git add -A`.**
- **Never use a vague commit subject.**
- **Do not include Copilot co-author trailers unless explicitly requested.**
- **Never force push.**
- **One commit per session batch.**
- **ALWAYS present 3 commit message options** (numbered 1–3, concise → descriptive). Wait for user to pick.
- **ALWAYS ask before pushing.**
