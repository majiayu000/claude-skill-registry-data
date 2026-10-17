---
name: guardscan
description: "Security primitive scanner: detects missing RLS, hardcoded secrets, client-only auth, missing CSRF, unprotected routes, missing security headers, and unvalidated environment variables."
trigger: /guardscan
vibe: true
---

# /guardscan

## What this is for

AI-generated code skips security layers. Guardscan finds the 7 most common missing security primitives in React/Next.js projects - prioritized by production impact. No security expertise needed. Every finding includes a real-world breach incident as context.

## Usage

- `/guardscan` - interactive wizard (HIGH first)
- `/guardscan high` - only HIGH impact checks
- `/guardscan quick` - all 7 checks
- `/guardscan secrets` - single check
- `/guardscan -help` - show full usage and stop

## DIALOG PROTOCOL - STRICT

Follow DIALOG.md. Findings are IMPACT-prioritized: always show HIGH first.

### Rules

1. Every prompt MUST show numbered options + `[0] Exit`
2. Show severity badge before each finding: `[HIGH]` / `[MEDIUM]` / `[LOW]`
3. Every finding MUST include: **Incident** (real-world breach) → **Diagnosis** → **Fix**
4. Base options per finding: `[F] Fix` `[S] Skip` `[N] Next` `[0] Exit`
5. Before any fix: show diff + ask confirmation `[y/n]`

## PROTECTION RULE

Read-only by default. No writes without explicit user consent per operation.

## Checks

### HIGH Impact - ships with known vulnerabilities

### 1. rls - Row Level Security Check

**Script:** `check-rls.ps1 -ProjectDir <path>`

Detects Supabase tables created without `ENABLE ROW LEVEL SECURITY`. Users can read/write any row across tenants. Linked to the Moltbook breach (1.5M API keys exposed).

### 2. secrets - Hardcoded Secrets

**Script:** `check-secrets.ps1 -ProjectDir <path>`

Detects API keys, tokens, passwords, and private keys hardcoded in source files. Also checks `.gitignore` for missing `.env` entry. 14% of AI-generated projects ship with leaked secrets (Quality Clouds 2026).

### 3. clientauth - Client-Only Authorization

**Script:** `check-clientauth.ps1 -ProjectDir <path>`

Detects authentication/authorization logic that only runs in client components - no server-side enforcement. Linked to the Lovable breach (18,000+ users across 170 apps with inverted access control).

### MEDIUM Impact - should fix before production

### 4. csrf - Missing CSRF Protection

**Script:** `check-csrf.ps1 -ProjectDir <path>`

Detects forms and API mutation endpoints without CSRF tokens or SameSite cookie configuration. 100% of vibe-coded apps tested by AppSec Santa had zero CSRF protection.

### 5. authmiddleware - Unprotected API Routes

**Script:** `check-authmiddleware.ps1 -ProjectDir <path>`

Detects `app/api/` route handlers without authentication checks. No auth middleware means any authenticated - or unauthenticated - user can call the endpoint.

### 6. headers - Missing Security Headers

**Script:** `check-headers.ps1 -ProjectDir <path>`

Detects missing Content-Security-Policy, Strict-Transport-Security, X-Content-Type-Options, and X-Frame-Options in middleware or config.

### LOW Impact

### 7. envvalidation - Unvalidated Environment Variables

**Script:** `check-envvalidation.ps1 -ProjectDir <path>`

Detects `process.env.X` usage without null/undefined checks or fallback values. Missing env vars cause silent production failures.

## Confidence Levels

Assign per finding: **proven** (script evidence, deterministic match), **likely** (strong signal, needs review), **suspected** (weak pattern, manually verify).
