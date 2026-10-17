---
name: shipcheck
description: "Pre-ship coach: checks env, build, secrets across your fullstack project. Interactive wizard + batch mode. For vibe coders."
trigger: /shipcheck
vibe: true
---

# /shipcheck

## What this is for

Before you ship: 3 critical checks in 30 seconds. The most common deploy blockers are missing environment variables, build errors, and accidental secret leaks. Shipcheck catches them before your CI pipeline does - with coaching on how to fix each one.

## Usage

- `/shipcheck` - interactive wizard (menus, explanations, coaching)
- `/shipcheck quick` - run all 3 checks, no menus, see results
- `/shipcheck env` - environment variables only
- `/shipcheck build` - build health only
- `/shipcheck secrets` - secret leakage only
- `/shipcheck -help` - show full usage and stop

## DIALOG PROTOCOL - STRICT

YOU MUST follow DIALOG.md for all interactive wizard flows.

### Rules

1. Every prompt MUST show numbered options `[N]` + `[0] Exit`
2. Every result MUST include diagnosis + explanation + implementation steps
3. Before any fix: show diff + ask confirmation `[y/n]`
4. Never auto-fix without user consent

## PROTECTION RULE

Read-only by default. No filesystem writes without explicit user confirmation per operation.

## Checks

### 1. env - Environment Variables

**Script:** `check-env.ps1 -ProjectDir <path>`

**What it checks:**
- `.env.example` exists
- `.env` exists
- All keys in `.env.example` present in `.env`
- Values are non-empty (not just `KEY=`)
- No keys in `.env` without `.env.example` entry (drift)

**Output:**
```json
{
  "check": "env",
  "status": "pass|warn|fail",
  "findings": [
    { "key": "DATABASE_URL", "status": "missing|empty|ok|extra",
      "message": "DATABASE_URL is missing from .env" }
  ],
  "summary": { "total": 5, "pass": 3, "warn": 1, "fail": 1 }
}
```

### 2. build - Build Health

**Script:** `check-build.ps1 -ProjectDir <path>`

**What it checks:**
- `package.json` exists
- `node_modules` exists
- Runs `npm run build` with 60s timeout
- Captures errors + warnings from build output

**Output:**
```json
{
  "check": "build",
  "status": "pass|warn|fail|skip",
  "findings": [
    { "type": "error|warning", "file": "src/app/page.tsx",
      "line": 12, "message": "Type 'string' is not assignable..." }
  ],
  "summary": { "errors": 0, "warnings": 2 },
  "exitCode": 0
}
```

### 3. secrets - Secret Leakage

**Script:** `check-secrets.ps1 -ProjectDir <path>`

**What it checks:**
- Regex patterns for: `sk-` (OpenAI), `ghp_` (GitHub PAT), `AKIA` (AWS), `-----BEGIN` (private keys), `password\s*=`, `secret\s*=`, `api[_-]?key\s*=`
- Skips `node_modules`, `.next`, `.git`
- Reports file + line + matched pattern

**Output:**
```json
{
  "check": "secrets",
  "status": "pass|fail",
  "findings": [
    { "file": "src/lib/api.ts", "line": 5, "pattern": "sk-...",
      "snippet": "const apiKey = 'sk-proj-...'",
      "risk": "critical|high|medium" }
  ],
  "summary": { "critical": 0, "high": 1, "medium": 0 }
}
```

## Coaching per Finding

Each finding MUST include three levels:

| Level | What | Example |
|-------|------|---------|
| **Diagnosis** | What the script found | `DATABASE_URL` missing in `.env` |
| **Explanation** | Why it matters | "Without a database URL, any DB query will throw a 500 error in production. Your app will crash on first login." |
| **Implementation** | Steps to fix | "1. Find your DB creds in your dashboard. 2. Add `DATABASE_URL=postgres://...` to `.env`. 3. Restart dev server." |

## Confidence Levels

Assign per finding: **proven** (script evidence), **likely** (strong signal, needs review), **suspected** (weak signal).
