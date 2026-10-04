---
name: superpowers-sage:debugging
description: >
  Structured troubleshooting for Sage/Acorn/Lando projects — diagnoses PHP errors, Blade
  rendering failures, Livewire mount errors, Eloquent query issues, Acorn boot failures,
  queue job failures, WP hook conflicts; uses lando logs, Query Monitor, Xdebug, WP_DEBUG.
  Invoke for: "/debugging", "something is broken and I can't figure out why",
  "lando logs show an error", "acorn boot error", "blade is rendering wrong",
  "livewire component not mounting", "500 error", "debug this issue".
  Skip when: you are building or implementing features — that is /building, not debugging.
user-invocable: true
disable-model-invocation: true
argument-hint: "[error description or symptom]"
---

# Debugging — Sage-Aware Troubleshooting

Diagnose and fix issues in Sage/Acorn/Lando projects with domain-specific knowledge of common pitfalls.

**Base skill:** This wraps `systematic-debugging` with Sage domain knowledge.

## Inputs

$ARGUMENTS

## Procedure

### 0) Categorize the issue

| Category | Symptoms | First Check |
|---|---|---|
| **Blade/View Cache** | Template not updating, old content showing | `lando flush` |
| **OPcache** | PHP changes not reflected despite cache clear | `lando restart` |
| **Vite/HMR** | Styles missing, HMR not connecting | Check dev server, `vite.config.js` |
| **ACF Registration** | Block not appearing, fields missing | ACF sync, block class `$name` |
| **Lando Services** | Container errors, service unavailable | `lando info`, service logs |
| **Acorn Boot** | Command not found, provider failure | `lando wp acorn`, config cache |
| **Livewire** | Component not rendering, wire actions failing | Install check, CSRF, Alpine |
| **Tailwind Purge** | Classes not applying in production | `@source` paths, CSS-first config |
| **Database** | Connection refused, migration errors | `.env` DB config, Lando service |
| **Autoload** | Class not found | `lando theme-composer dump-autoload` |

### 1) Run targeted diagnostics

Based on category, investigate:

#### Blade/View Cache
```bash
lando flush                                    # Clear all caches
ls content/cache/acorn/framework/views/        # Check for stale compiled views
```
- If `lando flush` doesn't help, check for stale files directly
- PHP-FPM OPcache is separate from CLI OPcache — `lando restart` for FPM

#### Vite/HMR
```bash
lando vite                    # Start dev server
```
- Check `vite.config.js`: `server.host` must be `'0.0.0.0'`
- Check `.lando.yml` proxy includes Vite port
- Check `@vite()` directive in layout blade

#### ACF Registration
```bash
lando acorn acf:sync          # Sync field groups
```
- Block `$name` must be kebab-case
- `fields()` must call `setLocation()`
- `with()` must return array

#### Autoload
```bash
lando theme-composer dump-autoload
```
- Namespace must match directory: `App\Blocks\` → `app/Blocks/`
- Class name must match filename

### 2) Known fixes (from experience)

| Problem | Root Cause | Fix |
|---|---|---|
| Blade cache not clearing | Stale compiled views | `lando flush` (uses custom Lando tooling) |
| OPcache stale after edit | PHP-FPM OPcache != CLI OPcache | `lando restart` |
| Grid classes not rendering | Dynamic classes purged by Tailwind v4 | Use inline styles for dynamic grids |
| `lando acorn` broken | Path misconfiguration | Use `lando wp acorn` instead |
| Material Symbols not rendering | Wrong icon name (not in symbol set) | Check Material Symbols catalog |
| Block content wrong after edit | Stale Blade cache + OPcache | Delete specific cache file + `lando flush` |

### 3) Present diagnosis

```markdown
## Diagnosis: {issue summary}

### Root Cause
{What's causing the issue — with evidence}

### Fix
{Step-by-step commands and/or code changes}

### Prevention
{How to avoid this in the future}
```

### 4) Verify fix

Run verification after applying fix. If issue persists, dig deeper or escalate to adjacent category.

## Common Quick Fixes

| Symptom | Quick Fix |
|---|---|
| Blade not updating | `lando flush` |
| Class not found | `lando theme-composer dump-autoload` |
| ACF fields missing | `lando acorn acf:sync` |
| Vite HMR broken | Check `server.host` in `vite.config.js` is `'0.0.0.0'` |
| `acorn` command not found | `lando wp acorn` or check `--path` in `.lando.yml` |
| Styles not in editor | Add `editor.css` to Vite entry points |

## Key Principles
- **`lando flush` first** — clears Blade cache, OPcache, Acorn cache in one command
- **OPcache is separate** — PHP-FPM and CLI have different OPcaches
- **Check the actual cache files** — sometimes programmatic clear doesn't work
- **Use `systematic-debugging`** as the base approach
- **Dispatch `sage-debugger` agent** for automated investigation
