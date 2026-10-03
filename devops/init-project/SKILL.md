---
name: init-project
description: Use when setting up a new project (or onboarding an existing repo) for safe AI-agent development — scaffolding the CLAUDE.md/AGENTS.md protocol plus DevSecOps guardrails. Triggers include "initial project setup", "scaffold our protocol", "set up the agent rules", or the command /init-project.
---

# init-project

## Overview
Scaffolds a project's **AI-agent development protocol + DevSecOps guardrails + workflow ecosystem** in one consistent pass: workflow discipline (`CLAUDE.md`/`AGENTS.md`), security policy, agent protocol docs, MCP policy, review prompts, spec/plan/codemap documentation scaffolding, a CI validation workflow, a `SessionStart` hook that nudges any future session if the protocol markers go missing, `.gitignore` hardening, security scripts, pre-commit, and `.mcp.json`. The goal isn't just files on disk — it's a working pipeline (`/brainstorm` → `/spec-writer` → `/plan-writer` + `superpowers:writing-plans-self-improvement-assistant` → `superpowers:subagent-driven-development` + `superpowers:sdd-self-improvement-assistant` → `/qa-master`) that a future agent session, or a new teammate who never ran this skill themselves, can pick up cold and follow correctly — because the protocol and its enforcement both live in the repo, not in any one person's local skill library. Detects the stack and tailors content. **Idempotent** — never clobbers existing files. **Scaffold only** — never installs, deploys, migrates, reads secrets, or adds dependencies.

## When to Use
- A brand-new repo, or onboarding an existing repo that lacks these guardrails.
- The user asks to "set up the protocol / agent rules / DevSecOps guardrails", or runs `/run-skill-generator`.
- NOT for editing app code, and NOT a substitute for per-feature brainstorming.

## Procedure

### 1. Detect the stack (cheap reads only)
Read whatever exists: `package.json`, `composer.json`, `go.mod`, `requirements.txt`/`pyproject.toml`, `Cargo.toml`, `Dockerfile`, `prisma/schema.prisma`, `*.csproj`. Determine:
- **Framework** (Next.js/Node/Laravel/Django/Go/…), **package manager** (npm/pnpm/yarn/composer/pip), **language** (TS/JS/PHP/Py/Go), **ORM/DB** (Prisma/Eloquent/…), **test runner**, **deploy hint** (Dockerfile/CI).
- **Sensitive surfaces present:** auth, payment, webhook, file upload, user input, API routes, server actions, env/secret, schema/migration.
Run `git status --short --branch` and list existing files so you know what to MERGE vs CREATE.

### 2. Confirm (one short message)
State detected stack + project name + the file manifest (below) + "I will merge into existing CLAUDE.md/AGENTS.md, skip other existing files." Proceed unless the user objects.

### 3. Generate the manifest (idempotent)
For each file: **create** from the matching `templates/` file in this skill's directory, adapting placeholders to the detected stack. If the file already exists, follow the **Idempotency** rules below — never overwrite blindly.

| File | Source template | If exists |
|---|---|---|
| `CLAUDE.md` | `templates/CLAUDE.md` | **Merge**: insert the "Alur Kerja Wajib" + "Catatan agent (DevSecOps)" blocks if absent; don't touch other content |
| `AGENTS.md` | `templates/AGENTS.md` | **Merge**: add the Pre-Task Checklist + Security Gate + DevSecOps section if absent |
| `SECURITY.md` | `templates/SECURITY.md` | skip + report |
| `docs/AI_AGENT_PROTOCOL.md` | `templates/AI_AGENT_PROTOCOL.md` | skip + report |
| `docs/MCP_RECOMMENDATIONS.md` | `templates/MCP_RECOMMENDATIONS.md` | skip + report |
| `docs/SECURITY_REVIEW_PROMPTS.md` | `templates/SECURITY_REVIEW_PROMPTS.md` | skip + report |
| `.pre-commit-config.yaml` | `templates/pre-commit-config.yaml` | skip + report |
| `.mcp.json` | `templates/mcp.json` | skip + report |
| `docs/superpowers/specs/README.md` | `templates/docs-specs-README.md` | skip + report |
| `docs/superpowers/plans/README.md` | `templates/docs-plans-README.md` | skip + report |
| `docs/CODEMAPS/README.md` | `templates/docs-codemaps-README.md` | skip + report |
| `.github/workflows/ci.yml` | `templates/ci.yml` | skip + report (see stack adaptation — skip entirely if remote isn't GitHub) |
| `.claude/settings.json` | `templates/settings.json` | **JSON-merge** (see below) — never skip outright, this is how the protocol reaches teammates who never ran `/init-project` themselves |
| `.gitignore` | inline snippet (below) | **Append** missing lines only |
| package manifest scripts | inline snippet (below) | **Merge** missing scripts only |

### 4. Apply stack adaptations
| Stack signal | Adapt |
|---|---|
| Node/TS | `security:npm` = `npm audit --audit-level=high`; `typecheck` = `tsc --noEmit`; build/lint from package.json |
| PHP/Composer | add `security:audit` = `composer audit`; drop npm-only scripts |
| Prisma/SQL ORM | DB checklist mentions migrations + "repository-only DB access" if the repo uses that pattern |
| Payment/webhook deps detected | keep the Payment/Webhook checklist; else trim it |
| No `.mcp.json` desired | still create it (Context7 + Playwright are universally useful) |
| `git remote -v` is not github.com (GitLab, Bitbucket, none) | **skip** `.github/workflows/ci.yml` entirely and report it as skipped with the reason — don't translate it to another CI syntax unasked |
| Non-Node stack (PHP/Python/Go/Rust) | adapt `ci.yml`'s install/lint/typecheck/build steps to the stack's real commands before writing it; never leave npm-specific steps in a non-Node project |
Fill placeholders: `{{PROJECT_NAME}}`, `{{STACK}}`, `{{PKG_MANAGER}}`, `{{SENSITIVE_SURFACES}}`, `{{VALIDATE_CMDS}}`. **Caution:** `ci.yml` also contains GitHub Actions' own `${{ secrets.* }}` expressions — only substitute the exact named placeholders above, never a blind `{{...}}` pattern match, or you will corrupt the workflow syntax.

### 5. Verify completeness (before reporting — do NOT skip)
Re-list the full manifest and confirm **each** target file now exists on disk (`ls` / `test -f`). Create any that are still missing. **Do not stop until every manifest item is present or explicitly skipped because it pre-existed.** A partial scaffold (e.g. only CLAUDE.md + AGENTS.md) is a FAILURE — the most common one. If you are running low on budget, prioritize creating the remaining files over writing prose.

### 6. Report (always)
End with: **Summary · Files created · Files merged · Files skipped (already present) · Stack detected · Next steps.**
Next steps to list:
- Set `GITHUB_PERSONAL_ACCESS_TOKEN` env var (for github MCP)
- Run `pre-commit install`
- Install CLIs (`gitleaks`, `trivy`, `semgrep`, `uv`) if missing
- Reload the agent so `.mcp.json` is picked up
- If `.claude/settings.json` was just created (not merged into an existing one), open `/hooks` once or restart the session — the settings watcher only watches directories that already had a settings file when the session started, so a brand-new `.claude/` may need one manual reload before the SessionStart hook activates
- **Workflow pipeline available:** `/brainstorm` → `/spec-writer` → `/plan-writer` + `superpowers:writing-plans-self-improvement-assistant` → [user approve] → `superpowers:subagent-driven-development` + `superpowers:sdd-self-improvement-assistant` → `/qa-master`. Full combo table in `AGENTS.md` § Workflow Skills.
- **ECC agents ready:** sub-agents `typescript-reviewer`, `security-reviewer`, `react-reviewer`, `database-reviewer` sudah tersedia di `~/.claude/agents/` — dispatch untuk review sebelum commit
- **Once real code exists:** consider running ecc `workspace-surface-audit` for a stack-specific skill/agent/MCP recommendation, and `update-codemaps` to fill in `docs/CODEMAPS/README.md` — both optional, not run automatically by this skill

Never claim it is "100% secure".

## Inline snippets

**`.gitignore` hardening** (append only the lines that are missing):
```
.env
.env.*
!.env.example
*.pem
*.key
id_rsa
id_ed25519
node_modules
vendor
dist
build
.next
coverage
playwright-report
test-results
```

**Security scripts** (merge into the package manager manifest, keep existing scripts; Node example — adapt per stack):
```json
"typecheck": "tsc --noEmit",
"security:secrets": "gitleaks detect --source . --verbose",
"security:code": "semgrep scan --config auto",
"security:fs": "trivy fs .",
"security:npm": "npm audit --audit-level=high",
"security:all": "npm run security:secrets && npm run security:code && npm run security:fs && npm run security:npm",
"predeploy": "npm run lint && npm run typecheck && npm run build && npm run security:all"
```

## Idempotency rules
- **Never overwrite** an existing file. CLAUDE.md/AGENTS.md → merge the protocol blocks only (check a marker heading like `## ⚙️ Alur Kerja Wajib` before inserting). Other files → skip and report "already present".
- `.gitignore` / scripts → add only missing entries; never remove the user's lines.
- **`.claude/settings.json` → JSON-merge, never text-append.** Read the file first. If it doesn't exist, create it from `templates/settings.json`. If it exists: parse it, check whether any existing `hooks.SessionStart[].hooks[]` entry already contains the string `Alur Kerja Wajib` in its `command` (our dedup marker) — if yes, skip and report "already present"; if no, append (don't replace) a new entry to the `hooks.SessionStart` array (create the array if the key is missing), preserving every other key in the file untouched. Re-parse the written file afterward to confirm it's still valid JSON — a broken `settings.json` silently disables every other setting in it.
- If unsure whether a merge is safe, skip and tell the user what to add manually.

**Why this hook exists:** the protocol markers in `CLAUDE.md`/`AGENTS.md` only standardize a team if everyone's agent actually reads them. A human onboarding a new repo can forget to run `/init-project`, and a new teammate's AI session has no way to know this skill exists unless the repo itself nudges it. This `SessionStart` hook is committed with the rest of the manifest specifically so the check travels with the repo, not with any one person's local skill library.

## Hard limits (never do)
- Never read, print, copy, or create real secret files (`.env*`, `*.pem`, `*.key`, `id_rsa`, `id_ed25519`). A generated `.env.example` must contain placeholders only (from documented var names, not by reading any `.env`).
- Never install packages, deploy, run migrations, access a production DB, or run destructive commands.
- Never hardcode a token in any file — GitHub MCP token goes in an env var.

## Common mistakes
- **Stopping at CLAUDE.md/AGENTS.md** — generate the FULL manifest (the baseline failure was missing MCP docs, review prompts, `.mcp.json`, the package scripts, and — as of the ecosystem expansion — the `docs/superpowers/specs`, `docs/superpowers/plans`, `docs/CODEMAPS` seeds, `.github/workflows/ci.yml`, and `.claude/settings.json`). A scaffold that leaves `CLAUDE.md` referencing folders that don't exist on disk is a FAILURE.
- **Text-appending into `.claude/settings.json` instead of JSON-merging** — this file is structured JSON; a naive text insert (like the `.gitignore` append) will corrupt it and silently disable every other setting in the file. Always parse, merge, re-serialize, and re-validate.
- **Pairing skills incorrectly** — `writing-plans-self-improvement-assistant` and `sdd-self-improvement-assistant` are companions, not substitutes, for `/plan-writer` and `superpowers:subagent-driven-development`. Don't document one without the other, and don't invent a self-improvement-assistant pairing for skills that don't have one (`/brainstorm`, `/spec-writer`, `/qa-master`).
- **Overwriting existing docs** — always merge/skip.
- **Generic, un-adapted content** — fill the placeholders from the detected stack; trim checklists that don't apply.
- **Running installs** — this skill scaffolds files; installs are a separate one-time PC step.
