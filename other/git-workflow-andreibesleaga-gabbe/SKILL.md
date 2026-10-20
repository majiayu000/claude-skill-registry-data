---
name: git-workflow
description: "Conventional commits, PR creation, and quality gate verification. Use when: commit, PR, branch, push, conventional commit, create pull request, git."
license: CC-BY-SA-4.0
metadata:
  source: "agents/skills/coding/git-workflow.skill.md"
  tags: "coding"
  core: "true"
  context_cost: "low"
---
# Git Workflow Skill

## Goal
Create well-structured commits following Conventional Commits spec, pass all quality gates before pushing, and create a descriptive PR for human review.

## Steps

1. **Verify quality gates** (all must pass before committing)
   ```bash
   [test command]       # All tests pass
   [typecheck command]  # No type errors
   [lint command]       # No lint errors
   [security_scan]      # No new critical/high CVEs (on dependency changes)
   ```
   If any fail: fix them before continuing. Do NOT commit with failing gates.

2. **Stage changes**
   ```bash
   git status           # Review what's changed
   git diff             # Review the actual changes
   git add [specific files]  # Never: git add -A (risk of including .env or build artifacts)
   ```

3. **Write a Conventional Commit message**

   **Format:** `<type>(<scope>): <subject>`

   | Type | When to use |
   |---|---|
   | `feat` | New feature |
   | `fix` | Bug fix |
   | `docs` | Documentation only |
   | `style` | Formatting, no logic change |
   | `refactor` | Code restructure, no behavior change |
   | `test` | Adding or fixing tests |
   | `chore` | Build process, tooling, deps |
   | `perf` | Performance improvement |
   | `sec` | Security fix |
   | `deps` | Dependency updates |

   **Good examples:**
   ```
   feat(auth): add OAuth2 Google login with refresh tokens
   fix(api): resolve N+1 query in users list endpoint
   sec(deps): update lodash 4.17.20 -> 4.17.21 (CVE-2021-23337)
   test(domain): add unit tests for Order aggregate invariants
   refactor(application): extract CreateOrderUseCase from OrderController
   ```

   **Bad examples (avoid):**
   ```
   fix stuff            # No scope, no description
   WIP                  # Work in progress should not be committed
   update code          # No context
   temp                 # Never commit temporary code
   ```

4. **Create the commit**
   ```bash
   git commit -m "feat(auth): add email verification flow

   - Add email_verified_at column to users table
   - Send verification email on registration
   - Add /auth/verify endpoint
   - Block login for unverified accounts

   Closes #42"
   ```

5. **Create a feature branch** (if working on main without a branch)
   ```bash
   git checkout -b feat/[issue-number]-[brief-description]
   # Example: git checkout -b feat/42-email-verification
   ```

6. **Push and create PR**
   ```bash
   git push origin [branch-name]

   # Create PR with gh CLI (preferred):
   gh pr create \
     --title "feat(auth): add email verification flow" \
     --body "$(cat <<'EOF'
   ## Summary
   - Add email verification requirement for new user accounts
   - Users must verify email before they can log in

   ## Changes
   - Database: adds `email_verified_at` column to users
   - API: adds `POST /auth/verify` endpoint
   - Auth: blocks unverified accounts from login

   ## Test Plan
   - [ ] Run unit tests: `[test command]`
   - [ ] Test registration flow end-to-end
   - [ ] Test that unverified users cannot log in
   - [ ] Verify verification email is sent

   ## Breaking Changes
   None — existing verified users are not affected.

   ## Security Notes
   Verification tokens expire after 24 hours.
   EOF
   )"
   ```

7. **Post-PR checklist**
   - Add reviewers if team is set up for it
   - Link to the relevant task in project/TASKS.md or issue tracker
   - Update task status in project/TASKS.md → DONE (or IN_REVIEW)
   - Add entry to AUDIT_LOG.md

## Branch Naming Conventions
```
feat/[issue]-[description]     # New features
fix/[issue]-[description]      # Bug fixes
refactor/[description]         # Refactoring
chore/[description]            # Tooling, deps
sec/[description]              # Security fixes
docs/[description]             # Documentation
```

## Constraints
- NEVER push directly to main/master — always use feature branches
- NEVER commit without all quality gates passing
- NEVER include .env files, credentials, or build artifacts in commits
- PR title must be a valid Conventional Commit message

## Output Format
Commit created + PR URL. Report: "Committed: [message]. PR: [URL]. All [N] quality gates passed."

## Security & Guardrails

### 1. Skill Security (Git Workflow)
- **Silent Gate Override**: Step 1 requires all quality gates to pass. If a test is flaky, the agent might decide to selectively bypass the test suite locally (`--no-verify` or `git commit -n`) to push the code and ask for human review. The workflow script MUST intercept and physically block any invocation of `git commit` or `git push` that attempts to disable pre-commit hooks or CI validation gates.
- **Secret Staging (The `git add .` Trap)**: Step 2 explicitly warns against `git add -A`. An attacker who compromises a sub-module might create a `.env.local` file containing production secrets. If an LLM agent gets lazy and executes a wildcard add (`git add .`), those secrets are permanently etched into the repository history. The agent must explicitly define `-- path/to/file` arguments for every file it stages, categorically rejecting any form of wildcard staging.

### 2. System Integration Security
- **Branch Name Injection**: In Step 5, the agent creates a branch using the issue number and description (`feat/[issue]-[description]`). If the source issue title contains malicious shell characters or path traversal sequences (e.g., `Issue #42: Fix ../../../etc/shadow`), constructing the `git checkout -b` command dynamically will lead to command injection. The agent must strictly normalize and strictly sanitize all branch names to alphanumeric and hyphen characters before executing the shell command.
- **PR Description XSS / Payload Delivery**: In Step 6, the agent constructs a PR description via the `gh pr create --body` command. If the commit relates to a bug fix for a malicious payload, the agent might blindly copy the payload into the "Summary" section to provide context. When developers open the PR on GitHub/GitLab, the payload might execute in their browser context. The agent must HTML-encode and neutralize all user-provided data included in the PR body string.

### 3. LLM & Agent Guardrails
- **Artificial PR Approval (Sockpuppeting)**: The agent operates within a swarm. A compromised agent persona might attempt to use the Git workflow to push malicious code, and another compromised persona might automatically approve it. The Git Workflow must strictly define that only authenticated Human identities (via cryptographic signatures or specific GitHub accounts) can review and merge PRs generated by an autonomous agent.
- **Hallucinated Semantic Versioning**: The LLM generates the Conventional Commit prefix (`feat:`, `fix:`). If the LLM incorrectly classifies a breaking change (e.g., changing an API response format) as a simple `chore` or `fix`, automated semantic release pipelines will fail to increment the major version, breaking downstream consumers. The agent must run an automated "Breaking Change Detection" AST diff script prior to generating the commit type, vetoing the LLM's classification if a public contract was mutated.
