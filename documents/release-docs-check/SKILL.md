---
name: release-docs-check
description: Pre-release documentation and metadata check. Use when asked to "docs check", "/release-docs-check", or to audit README / package.json / .env.example / .gitignore / LICENSE consistency before release.
---

# Pre-Release Documentation & Metadata Check

Before publishing the project, verify README, package.json, and related docs are in a correct state.

## Procedure

Run the sections below in order. Report any issue as `file:line`.

---

## 1. package.json

Read `package.json` and verify:

| Field | Check |
|-------|-------|
| `name` | lowercase, hyphen-separated |
| `version` | semver (e.g. `0.1.0`) |
| `description` | present, no unauthorised product / competitor names, written in English |
| `license` | valid SPDX identifier |
| `author` | present |
| `repository.url` | correct git URL, no placeholders |
| `bugs.url` | correct issues URL |
| `homepage` | correct URL |
| `keywords` | at least 5 entries |
| `engines` | Node.js version specified |

**Prohibited patterns:**
- Hardcoded competitor / other product names (e.g. `"WordPress"`, `"Ghost"`, `"Contentful"`)
- Placeholder URLs (`"your-repo"`, `"example.com"`, `"TODO"`, etc.)
- `private: true` when the project is intended for npm publish (only relevant if publishing)

---

## 2. README.md

Read `README.md` and verify:

| Item | Check |
|------|-------|
| Title / intro | First paragraph explains what the product is |
| Setup steps | Can be set up in ~5 minutes |
| Requirements | Node.js version and other prerequisites are spelled out |
| Env vars | References `.env.example` or describes configuration |
| Screenshots | Admin UI / theme images are present (warn if none) |
| License | License name / link is stated |
| False statements | No nonexistent features or unrelated product descriptions |
| Stale paths | No obsolete references like `settings/site.json` |

---

## 3. .env.example

Read `.env.example` and verify:

| Item | Check |
|------|-------|
| Obsolete paths | No references to old architecture like `settings/*.json` |
| Secret values | No real API keys / secrets (placeholders only) |
| Required vars | Variables marked `[REQUIRED]` have explanations |
| Comment accuracy | Comments match the current architecture (Admin UI → Settings) |

---

## 4. .gitignore

Read `.gitignore` and confirm these are excluded:

- `.env`, `.env.local`, `.env.*` (except `.env.example`)
- `data/` (SQLite DB)
- `logs/`
- `*.pem`, `*.key`
- `*credentials*.json`
- `.session-secret`
- `node_modules/`
- `.next/`

---

## 5. Source code residue

Grep for the following:

- `console.log` — any remaining under `app/baan-admin/api/`
- Japanese error messages — any appearing in API responses under `app/baan-admin/api/` (exclude `i18n.ts`)
- Hardcoded production URLs / secrets; stray `TODO`, `FIXME`, `HACK` comments

---

## 6. LICENSE

Read `LICENSE`:

- File exists
- Matches the `license` field in package.json
- Year and author are correct

---

## Output format

Clean: `✅ OK`
Issue: `❌ file:line — description`
Warning: `⚠️ file — recommendation`

End with an **overall verdict**:
- `🟢 READY` — everything passes
- `🟡 CAUTION` — minor issues (can ship, but flag them)
- `🔴 NOT READY` — serious issues (fix before shipping)
