---
name: client-onboard
version: 1.0.0
description: |
  One command bootstraps a per-client repo so Claude Code starts pre-loaded.
  Detects project type (WP theme / React-Next / static / n8n / video) from
  files present → generates a tight CLAUDE.md (<200 lines: stack, architecture
  rationale, conventions + build/deploy commands) with the RIGHT deploy gotcha
  baked in automatically (Hostinger Node app = manual ZIP NOT GitHub; React =
  Vercel; video = NVENC-broken→libx264). Scaffolds .claude/, suggests relevant
  MCP (GHL/Hostinger), adds CLAUDE.local.md to .gitignore, enforces the
  CLAUDE.md-vs-Skill rule, and warns on lowercase claude.md dups.

  Fixes the gap: many client repos (travel, agency site, jewelry, fashion,
  car dealer, health clinic) ship with no CLAUDE.md,
  so Claude re-learns context every session.

  Trigger when user says: "onboard this client", "onboard repo", "bootstrap
  CLAUDE.md", "set up CLAUDE.md", "init client repo", "/client-onboard", or
  opens a client repo with no CLAUDE.md and asks Claude to start work on it.

  Auto-trigger heuristic: cwd is a client project dir AND no CLAUDE.md exists
  at repo root.
license: MIT
compatibility: claude-code
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# client-onboard

## When to use

USE when:

- Opening a client repo that has NO `CLAUDE.md` at root
- Spinning up a new client project (travel site, agency site, jewelry, fashion, car dealer, health clinic, etc.)
- An existing repo's CLAUDE.md is stale/bloated (>200 lines) and needs a rebuild

SKIP when:

- Repo already has a tight, current CLAUDE.md (just edit it, don't regenerate)
- Not a code repo (use `/daily` or brain notes instead)

## Core rule (from claude-code-mastery)

> **CLAUDE.md = facts always true. Skill = procedures you'd re-paste.**

If a step is a repeatable PROCEDURE (deploy dance, audit format, content batch),
do NOT bloat CLAUDE.md with it — note it and **suggest building a Skill**.
CLAUDE.md only holds: the _what_ (stack), the _why_ (architecture rationale),
the _how_ (conventions + the exact build/deploy commands for THIS repo).

Hard limits:

- CLAUDE.md **< 200 lines**. Over = bloat → cut to facts.
- Casing is **ALWAYS `CLAUDE.md`** (uppercase). Never `claude.md` / `Claude.md`.

## Inputs required

1. **Repo path** — defaults to cwd
2. **Client name / slug** — e.g. `your-site`, `travel-client` (infer from dir name, confirm)
3. **Live URL** (optional) — for deploy context + MCP wiring
4. **Is it a video repo?** — only then bake NVENC gotcha (auto-detected, confirm)

If client/stack ambiguous → ASK before writing. Never invent a deploy target.

## The 7-step recipe

### 1. Pre-flight + casing guard

```bash
cd <repo>
git rev-parse --is-inside-work-tree 2>/dev/null && echo "git repo" || echo "NOT a git repo"
# Casing guard: detect lowercase dup that Windows hides but git tracks
git ls-files | grep -iE '(^|/)claude\.md$' || true
ls -la | grep -iE 'claude\.md' || true
```

If a **lowercase `claude.md`** exists → WARN loudly. On case-insensitive Windows
it silently shadows `CLAUDE.md`; Claude Code only auto-loads the uppercase name.
Fix:

```bash
git mv claude.md CLAUDE.md.tmp && git mv CLAUDE.md.tmp CLAUDE.md   # two-step: Windows needs it
```

### 2. Detect project type

Probe files at root (and one level down). First match wins; a repo can be multi-type.

| Type            | Detection signal                                                              |
| --------------- | ----------------------------------------------------------------------------- |
| **wp-theme**    | `style.css` with `Theme Name:` header, or `functions.php`, `wp-content/`      |
| **wp-plugin**   | `*.php` with `Plugin Name:` header in header comment                          |
| **react-next**  | `next.config.*` OR (`package.json` with `next`/`react` dep)                   |
| **vite-static** | `vite.config.*` or `package.json` w/ `vite`, no `next`                        |
| **static**      | `index.html` at root, no `package.json`                                       |
| **n8n**         | `*.json` workflow exports w/ `"nodes"`+`"connections"` keys, or `/workflows/` |
| **video**       | `*.mp4`/`*.mov`/`*.mkv` assets + `ffmpeg`/`.ps1` render scripts               |

```bash
# quick probes
test -f style.css && grep -l "Theme Name:" style.css 2>/dev/null && echo "TYPE: wp-theme"
test -f next.config.js -o -f next.config.mjs -o -f next.config.ts && echo "TYPE: react-next"
test -f package.json && grep -qE '"(next|react)"' package.json && echo "TYPE: react-next"
test -f index.html && test ! -f package.json && echo "TYPE: static"
grep -rlE '"nodes"\s*:' --include='*.json' . 2>/dev/null | head -1 && echo "TYPE: n8n (maybe)"
ls *.mp4 *.mov *.mkv 2>/dev/null | head -1 && echo "TYPE: video (maybe)"
```

### 3. Pull the RIGHT deploy gotcha (the load-bearing step)

Pick deploy block by client + type. NEVER mix these up.

| Client / type                                                                | Deploy truth (bake verbatim)                                                                                                                                                                                                               |
| ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Hostinger Node app** (e.g. main agency site)                               | Deploys via **Hostinger manual ZIP archive upload in hPanel**. **NOT GitHub auto-deploy** — GitHub auto-deploy is hPanel-locked/unavailable here. Build → ZIP → hPanel File Manager → upload → extract. Rollback = re-upload previous ZIP. |
| **WP plugin/login styler** (e.g. travel client on `client-site.example.com`) | WP plugin: bump version header, ZIP the plugin folder, upload via WP admin Plugins → or hosting File Manager. LoginPress coexistence rules apply (style CSS-first, gettext for text, never DOM-surgery on register).                       |
| **react-next** (any)                                                         | Deploys to **Vercel**. `git push` to connected branch = auto-deploy preview; merge to `main` = production. `vercel --prod` for manual.                                                                                                     |
| **vite-static / static**                                                     | Host-dependent — confirm. If Hostinger → manual ZIP (same as the Hostinger Node app rule). If Vercel/Netlify → push-to-deploy.                                                                                                             |
| **n8n**                                                                      | Workflows live in n8n instance, NOT auto-deployed from repo. Import JSON via n8n UI / API. Repo = source of truth backup. Activate manually after creds wired.                                                                             |
| **video**                                                                    | No "deploy" — render then publish via GHL drip (`/ghl-video-drip`).                                                                                                                                                                        |

### 4. Bake video gotcha — ONLY if video repo

If and only if TYPE includes **video**, add to CLAUDE.md:

```
- ffmpeg on this box: NVENC is BROKEN → always encode with libx264.
- Alpha .mov overlays fail → use PNG sequences/stills instead.
- Talking-head: face-safe right-panel pattern (see memory: video-edit-gotchas).
```

Do NOT add this to non-video repos.

### 5. Generate CLAUDE.md (< 200 lines)

Use the template below. Fill every `<...>`. Cut anything that isn't a durable fact.
Procedures → list under "Procedures (build as Skills)" with a one-line pointer, NOT full steps.

### 6. Scaffold `.claude/` + gitignore + MCP note

```bash
mkdir -p .claude
# starter settings (permissions only — keep minimal)
test -f .claude/settings.json || cat > .claude/settings.json <<'JSON'
{ "permissions": { "allow": [], "deny": [] } }
JSON

# CLAUDE.local.md = personal/secret context, never committed
grep -qxF 'CLAUDE.local.md' .gitignore 2>/dev/null || echo 'CLAUDE.local.md' >> .gitignore
grep -qxF '.claude/settings.local.json' .gitignore 2>/dev/null || echo '.claude/settings.local.json' >> .gitignore
```

MCP suggestion (print, don't auto-wire — needs creds):

- Hostinger-hosted client site → suggest `hostinger-mcp` (DNS, deploy WP theme/plugin, File Manager).
- Lead-gen / CRM client → suggest `ghl` MCP (contacts, social posting, conversations).
- React/Next on Vercel → suggest `vercel` auth (deploy logs, env).
- n8n repo → suggest `n8n-mcp` (search/validate nodes, validate workflow).

### 7. Output checklist

Print exactly what was created + next steps (template at bottom).

## CLAUDE.md template (copy-fill, keep < 200 lines)

```markdown
# <Client Name> — <one-line what this repo is>

## Stack (the what)

- Type: <wp-theme | react-next | static | n8n | video>
- Lang/Framework: <e.g. WordPress (PHP), Next.js 14 / React, vanilla HTML+JS>
- Hosting: <Hostinger | Vercel | n8n instance>
- Live URL: <https://...>
- Key deps: <list 3-6 that matter; from package.json / composer.json>

## Architecture rationale (the why)

- <Why this structure. e.g. "Standalone plugin so LoginPress is removable.">
- <Key constraint that shapes the code. e.g. "Italian client → IT copy via gettext, never hardcoded.">
- <Any hard-won decision. e.g. "CSS-first login styling, no DOM surgery on register.">

## Conventions (the how)

- File layout: <where things live>
- Naming: <conventions>
- Do: <repo-specific musts>
- Don't: <repo-specific traps>

## Build & deploy commands

\`\`\`bash
<build cmd, e.g. npm run build | or "no build step">
\`\`\`
DEPLOY (read carefully — this repo's truth):
<paste the exact deploy gotcha block from step 3>

## Gotchas

- <repo-specific landmines>
  <video-only: NVENC broken → libx264; alpha .mov fails → PNG>

## Procedures (build as Skills, NOT in this file)

- <repeatable workflow> → suggest Skill: <name>
```

## Casing rule (enforced)

- Canonical filename is **`CLAUDE.md`** — uppercase, every time.
- Claude Code auto-loads `CLAUDE.md`; a lowercase `claude.md` is silently ignored on load but tracked by git → split-brain.
- On Windows (case-insensitive FS) the dup hides. ALWAYS check `git ls-files | grep -i claude.md` in step 1 and warn.
- `CLAUDE.local.md` = your private, gitignored layer (secrets, personal notes). Never committed.

## Output checklist template

```
CLIENT ONBOARDED: <slug>
Detected type:  <type(s)>
Deploy target:  <Hostinger manual ZIP | Vercel | n8n import | render-only>

Created:
  [x] CLAUDE.md            (<N> lines, < 200 ✓)
  [x] .claude/settings.json
  [x] .gitignore           (+ CLAUDE.local.md, .claude/settings.local.json)
Warnings:
  [<x|->] lowercase claude.md dup  <none | FOUND — renamed>
Suggested MCP (wire with creds):
  - <hostinger-mcp | ghl | vercel | n8n-mcp>
Suggested Skills (procedures, not facts):
  - <skill ideas surfaced during scan>

NEXT:
  1. Review CLAUDE.md — fill any <...> placeholders I couldn't infer.
  2. git add CLAUDE.md .claude/settings.json .gitignore && commit.
  3. Wire suggested MCP if working the live site this session.
  4. Open a fresh session so CLAUDE.md auto-loads.
```

## Known client cheat-sheet (example slugs)

| Slug            | Type                     | Hosting / deploy                                  | Special                                                            |
| --------------- | ------------------------ | ------------------------------------------------- | ------------------------------------------------------------------ |
| your-site       | WP/site                  | **Hostinger MANUAL ZIP** (NOT GitHub auto-deploy) | rollback = re-upload prev ZIP                                      |
| travel-client   | WP plugin (login styler) | WP admin / File Manager ZIP                       | LoginPress coexistence; localized copy; never DOM-surgery register |
| jewelry-client  | site/demo                | confirm host                                      | jewelry niche demo                                                 |
| fashion-client  | site/demo                | confirm host                                      | fashion niche demo                                                 |
| car-dealer      | site/demo                | confirm host                                      | dealer niche demo                                                  |
| health-clinic   | site/demo                | confirm host                                      | health/wellness niche demo                                         |
| social-pipeline | n8n/automation           | n8n instance, manual import+activate              | scraper→n8n→GHL; creds gated                                       |

## Anti-patterns

- ❌ Writing a 400-line CLAUDE.md (it's facts, not docs — cut to < 200)
- ❌ Putting procedures in CLAUDE.md (those become Skills)
- ❌ Saying "deploy via git push" for a Hostinger Node app (it's manual Hostinger ZIP)
- ❌ Baking NVENC/libx264 into a non-video repo
- ❌ Lowercase `claude.md` (won't auto-load; creates a dup)
- ❌ Auto-wiring MCP with no creds (suggest, then let user add tokens)
- ❌ Committing `CLAUDE.local.md` (it's the gitignored private layer)
- ❌ Inventing a deploy target — ASK if host is unknown
