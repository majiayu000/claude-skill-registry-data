---
name: repo-scanner
description: Scans a GitHub repository to understand its tech stack, hosting, monitoring, integrations, and current production readiness. Use when the user asks to "audit", "check", or "scan" their repo. Don't use for code review or bug detection.
---

# Repo Scanner

Scans any repository to build a complete picture of the current technical setup and scores production readiness.

## How It Works

1. Read the root directory tree to identify project type and structure
2. Detect the tech stack from config files
3. Check for production infrastructure (CI/CD, Docker, hosting)
4. Check for observability (monitoring, error tracking, logging)
5. Check for developer experience (documentation, agent config, tooling)
6. Output a structured scan report using the EXACT format below

## Step-by-Step Procedure

### Step 1: Read Directory Structure
```bash
find . -type f -not -path './.git/*' -not -path './node_modules/*' -not -path './.next/*' -not -path './dist/*' -not -path './__pycache__/*' -not -path './venv/*' | head -200
```

### Step 2: Detect Tech Stack

Check for these files to determine the stack:

| File | Stack |
|------|-------|
| `package.json` | Node.js / JavaScript / TypeScript |
| `tsconfig.json` | TypeScript |
| `next.config.*` | Next.js |
| `vite.config.*` | Vite |
| `requirements.txt` / `pyproject.toml` | Python |
| `go.mod` | Go |
| `Cargo.toml` | Rust |
| `Gemfile` | Ruby |

Read `package.json` or equivalent to understand dependencies and scripts.

### Step 3: Check Production Infrastructure

| Check | How |
|-------|-----|
| **CI/CD** | Look for `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile` |
| **Docker** | Look for `Dockerfile`, `docker-compose.yml`, `.dockerignore` |
| **Hosting** | Look for `vercel.json`, `railway.toml`, `fly.toml`, `render.yaml`, `serverless.yml` |
| **Environments** | Look for `.env.example`, `.env.local`, `.env.production` |
| **Build** | Check for build scripts in `package.json` or `Makefile` |

### Step 4: Check Observability

| Check | How |
|-------|-----|
| **Error tracking** | Grep for `sentry`, `@sentry/`, `posthog`, `datadog`, `bugsnag` in deps or code |
| **Analytics** | Grep for `gtag`, `analytics`, `mixpanel`, `amplitude` |
| **Logging** | Check for structured logging (winston, pino, structlog, loguru) |
| **Health checks** | Look for `/health`, `/healthz`, `/api/health` endpoints |

### Step 5: Check Developer Experience

| Check | How |
|-------|-----|
| **Root README** | Does `README.md` exist with setup instructions? |
| **Directory READMEs** | `find . -name "README.md" -not -path './node_modules/*' | wc -l` |
| **Agent config** | Look for `AGENTS.md`, `.cursorrules`, `.cursor/rules/`, `.claude/` |
| **Linting** | Look for `.eslintrc`, `.prettierrc`, `ruff.toml` |
| **Testing** | Look for `__tests__/`, `tests/`, `spec/`, test scripts |
| **Git hygiene** | Check `.gitignore` exists and covers common patterns |

### Step 6: Check Security
```bash
grep -rn "sk-\|api_key\s*=\s*['\"].\+['\"]" --include="*.ts" --include="*.js" --include="*.py" --include="*.env" . 2>/dev/null | grep -v node_modules | grep -v '.env.example' | head -20
```

## MANDATORY Output Format

**You MUST use this exact markdown structure. Do not invent your own format.**

````markdown
## 🔍 Repo Scan: {project-name}

**Tech Stack:** {e.g. React 18 + TypeScript, Flask + Python 3.11}
**Hosting:** {e.g. Vercel, AWS, Railway, or "Not configured"}
**Framework:** {e.g. Next.js 14, Vite 5, FastAPI}

---

## 📊 Production Readiness Score: {X}/10

| # | Category | Status | Details |
|---|----------|--------|---------|
| 1 | Environment Setup | {✅/⚠️/❌} | {one-line detail} |
| 2 | CI/CD Pipeline | {✅/⚠️/❌} | {one-line detail} |
| 3 | Documentation | {✅/⚠️/❌} | {one-line detail} |
| 4 | Error Tracking | {✅/⚠️/❌} | {one-line detail} |
| 5 | Deployment | {✅/⚠️/❌} | {one-line detail} |
| 6 | Security | {✅/⚠️/❌} | {one-line detail} |
| 7 | Cost Awareness | {✅/⚠️/❌} | {one-line detail} |
| 8 | Integration Health | {✅/⚠️/❌} | {one-line detail} |
| 9 | LLM-Readiness | {✅/⚠️/❌} | {one-line detail} |
| 10 | Code Organization | {✅/⚠️/❌} | {one-line detail} |

**Scoring: ✅ = 1 point, ⚠️ = 0.5 points, ❌ = 0 points**

---

## 🚨 Top 3 Issues

1. **{Issue title}** — {Why it matters. File:line reference if applicable.}
2. **{Issue title}** — {Why it matters.}
3. **{Issue title}** — {Why it matters.}

---

## 🛠️ Recommended Next Steps

Run these vibe-to-prod skills to fix the issues above:

1. `skills/{skill-name}/` — {what it will fix}
2. `skills/{skill-name}/` — {what it will fix}
3. `skills/{skill-name}/` — {what it will fix}
````

**Rules for the output:**
- Use the EXACT table format above with ✅/⚠️/❌ status icons
- Score is X/10 where ✅=1, ⚠️=0.5, ❌=0
- Top 3 issues must include specific file:line references when possible
- Recommended next steps must reference actual skill directory names
- Keep the entire output under 100 lines
- Do NOT add extra sections, executive summaries, or risk assessments
