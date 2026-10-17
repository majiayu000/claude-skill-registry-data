---
name: polish
description: "AI residue removal coach: console.log, any types, missing fallbacks, magic strings, dead imports, AI hallucination patterns."
trigger: /polish
vibe: true
---

# /polish

## What this is for

AI-generated code leaves traces: debug logs, `any` types, missing fallbacks, hardcoded values, dead imports, and hallucinated packages. Polish finds and fixes them - 6 checks in 1 minute. The coaching dialog walks you through each finding with fix options.

## Usage

- `/polish` - interactive coaching wizard
- `/polish quick` - all 6 checks at once
- `/polish consolelog` - single check
- `/polish -help` - show full usage and stop

## DIALOG PROTOCOL - STRICT

YOU MUST follow the decision tree in DIALOG.md. This is a COACHING dialog, not a gate. There is no pass/fail - only "found" or "not found".

### Rules

1. Every prompt MUST show numbered options + `[0] Exit`
2. Every finding MUST include: **Diagnosis** → **Explanation** (1 sentence) → **Implementation** (3 steps max)
3. Base options per finding: `[F] Fix` `[S] Skip` `[N] Next` `[0] Exit`
4. Check-specific extras when applicable:
   - `consolelog`: `[R] Replace with logger`
   - `anytype`: `[U] Suggest unknown` `[E] Add type`
   - `nofallback`: `[K] Add key=` `[B] Add ErrorBoundary`
   - `magic`: `[C] Extract to constant` `[V] Move to env`
   - `deadimport`: `[R] Remove import`
   - `aismell`: `[E] Explain why this is a problem`
5. Before any fix: show diff + ask confirmation `[y/n]`

## PROTECTION RULE

Read-only by default. No writes without explicit user confirmation per operation.

## Checks

### 1. consolelog - Debug Residue

**Script:** `check-consolelog.ps1 -ProjectDir <path>`

Finds `console.log`, `console.warn`, `console.error` calls outside a logger utility. These are debug leftovers that bloat production output and may leak data.

### 2. anytype - Type Escape

**Script:** `check-anytype.ps1 -ProjectDir <path>`

Finds `: any` type annotations, `as any` casts, and `<any>` generic params in `.ts/.tsx` files. Each `any` disables TypeScript - a sign of "make it compile" AI shortcuts.

### 3. nofallback - Missing Fallbacks

**Script:** `check-nofallback.ps1 -ProjectDir <path>`

Finds three common UX gaps:
- `.map()` without `key=` prop
- Component exports without `ErrorBoundary` wrapper
- `fetch`/`axios` calls without `loading` state tracking

### 4. magic - Magic Values

**Script:** `check-magic.ps1 -ProjectDir <path>`

Finds hardcoded URLs, port numbers, and long string literals that should be extracted to config or environment variables.

### 5. deadimport - Dead Imports

**Script:** `check-deadimport.ps1 -ProjectDir <path>`

Finds import statements where the imported symbol is never used in the file body. A common AI pattern: imports added "just in case" that never get used.

### 6. aismell - AI Smell Detector (LLM)

**Script:** `check-aismell.ps1 -ProjectDir <path>` (raw data collector)

**YOU (the LLM) analyze the collected data** to detect:
- **Unused dependencies** - in `package.json` but never imported
- **Hallucinated imports** - imported package not in `package.json`
- **Overly long files** - >200 lines, sign of AI-generated boilerplate
- **Missing types** - async functions without return types
- **Over-engineering** - unnecessary abstractions for simple tasks

Assign each smell a confidence level: **proven** (script evidence), **likely** (strong signal), **suspected** (weak signal).

## Coaching per Finding

Each finding MUST include three levels:

| Level | What | Example |
|-------|------|---------|
| **Diagnosis** | What the script found | `console.log` in `src/lib/fetch.ts:12` |
| **Explanation** | Why it matters (1 sentence) | "Debug logs in production can leak API responses to the browser console." |
| **Implementation** | Steps to fix (1-3) | "1. Remove the line, or 2. Replace with `logger.info()`" |

## Confidence Levels

Assign per finding: **proven** (script evidence), **likely** (strong signal, needs review), **suspected** (weak signal).
