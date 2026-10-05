---
name: research-first-development
description: Research-first implementation workflow — before writing any code, find the best existing open-source solution. Triggered by "不重复造轮子", "找现成方案", "用什么库", "调研方案", "有没有现成的".
tags: [workflow, implementation, research, philosophy]
category: workflow
---

# Research-First Development

## Core Principle

> **Every requirement → search for existing best solution → integrate. Never write your own unless no viable option exists.**

This is not just a preference — it's the defining philosophy of how implementation work is done. Violating it means re-implementing something that already exists, better-tested, in the open-source ecosystem.

## When This Applies

- ANY implementation task (feature, handler, utility, encoding fix, UI component)
- Choosing a library or dependency
- Solving a technical problem ("how do I decode GB2312?")

**The ONLY exceptions:**
- Glue code that wires existing solutions together
- Trivial one-liners (a `useState` call, a CSS class toggle)
- Things that literally don't exist yet (novel UX patterns)

## The Research-First Workflow

```
Requirement arrives
    │
    ▼
Step 1: SEARCH — web_search/brave for "best <topic> library npm browser 2024"
    │
    ▼
Step 2: COMPARE — extract npm pages, GitHub READMEs. Evaluate:
    • Browser compatibility (no Node-only APIs!)
    • Bundle size (prefer <50KB for PWA)
    • Maintenance (recent commits? npm dependents?)
    • API simplicity (does it do ONE thing well?)
    • License (MIT/Apache preferred)
    │
    ▼
Step 3: PICK — choose the best fit, justify with data
    │
    ▼
Step 4: INSTALL + INTEGRATE — npm install, write a handler/wrapper
    │
    ▼
Step 5: VERIFY — build passes, no browser console errors
```

## Anti-Pattern: The "I'll Just Write It" Reflex

```typescript
// ❌ BAD: Hand-writing encoding detection
function detectEncoding(buffer: ArrayBuffer): string {
  // 20 lines of heuristic byte-checking...
  // (This is what I did before the user corrected me)
}

// ✅ GOOD: Using existing battle-tested solution
import chardet from 'chardet';
const results = chardet.analyse(new Uint8Array(buffer));
```

The hand-written version took 20 lines, handled 2 encodings, and was wrong for edge cases. `chardet` took 3 lines, handles 25 encodings, and is used by 1,477 other projects.

## Decision Framework

For each candidate, score:

| Criterion | Weight | Question |
|-----------|--------|----------|
| Browser-ready | 🔴 MUST | Does it work in browser ESM without `global`/`process`/`fs`? |
| Bundle impact | 🟡 HIGH | How many KB gzipped? Prefer <50KB for PWA. |
| Maintenance | 🟡 HIGH | Last commit <6 months? npm dependents >100? |
| API fit | 🟢 MEDIUM | Does it do exactly what we need, nothing more? |

## Known Good Swaps

| Need | ❌ Bad (Node-only) | ✅ Good (browser) |
|------|-------------------|-------------------|
| TOML parsing | `@iarna/toml` | `smol-toml` (1.6KB, ESM) |
| Encoding detection | hand-written heuristic | `chardet` (22KB, 25 encodings) |
| Compression | `zlib` (Node built-in) | `fflate` (30KB, ZIP+GZIP+DEFLATE) |
| PDF viewing | hand-written canvas render | `react-pdf` (pdfjs-dist wrapper) |
| CSV parsing | hand-written split(',') | `papaparse` (already in project) |
| Keyboard shortcuts | hand-written keydown listener | `react-hotkeys-hook` (<3KB) |
| i18n | custom translation object | `react-i18next` (~5KB gzip) |
| Dark/light theme | manually toggling `dark:` classes per element | Tailwind v4 `@theme` design tokens (CSS custom properties, single `.dark {}` block) |

## Verification

After integrating a library:
- [ ] `npm run build` succeeds
- [ ] No browser console errors (`Uncaught ReferenceError`, `global is not defined`)
- [ ] Bundle size increase is acceptable
- [ ] Feature works end-to-end

---

## References

- `references/research-comparisons-phase3.md` — Full comparison tables from open-any Phase 3 (encoding, compression, PDF, media, shortcuts, i18n, theme)
- `references/tailwind-v4-theme-tokens.md` — Tailwind v4 `@theme` design token pattern for dark/light mode
- `references/browser-library-pitfalls.md` — 7 common bugs from integrating browser libraries (PDF worker URL, blob URL revocation, useMemo focus loss, sync APIs, encoding detection, keyboard shortcuts, React 19 act)

## Pitfalls

- **Node-only packages**: Vite/Rolldown converts CJS→ESM but can't fix `global`/`process`/`fs` references. Always test in browser.
- **npm uninstall cascade**: `npm uninstall <pkg>` may remove 95+ transitive deps. Prefer `npm install <new> && npm uninstall <old>`.
- **Over-researching**: 3-5 candidates is enough. Don't spend 30 minutes comparing 15 alternatives.
- **"Obvious" solutions still need research**: Before implementing what seems obvious (theme toggle = toggle a class), search for "best practice <topic> <framework> 2025". The obvious solution is often the amateur one. Example: theme toggle → Tailwind v4 `@theme` design tokens, not manually replacing every color class. Date check keywords (2024/2025) to avoid stale approaches.
- **Verify fixes before declaring victory**: A bug may have multiple root causes. If your first fix doesn't solve it, there's a deeper cause. Test in the actual runtime (browser, not just `npm run build`). Example: PDF "Failed to load" — first fix (CDN→Vite worker) looked correct but didn't work; real cause was blob URL + Web Worker incompatibility, only discoverable by checking the browser console error message.
- **Don't start work until the user has stated what they want**: When the user opens with context or materials but hasn't yet stated the task, present what you found and WAIT — don't assume and jump into implementation. The user will tell you what to do. This applies even when the next step seems obvious to you.
- **先看完再动手（Look before you leap）**: When given data or a situation, fully understand it first. Read the file, examine the structure, present findings. Only then discuss approach. Never start importing/processing/modifying before the user confirms the direction. "先看完再说" is a direct signal you violated this.
- **New library? Check docs BEFORE writing code**: When working with an unfamiliar library or framework, search Context7, web_search, and official docs first — not after hitting errors. A 5-minute doc scan (API patterns, breaking changes, recommended approach) prevents hours of blind debugging. Example: hitting 3 PaddlePaddle 3.3 API changes (label shape, numpy scalar, astype) that Context7 docs would have revealed instantly.
- **Web Workers can't access blob URLs**: Libraries that use Web Workers internally (pdfjs-dist, ffmpeg.wasm) run in a separate thread. Blob URLs created via `URL.createObjectURL()` in the main thread are NOT accessible from the worker. Pass raw data: `{ data: new Uint8Array(buffer) }` — the worker receives it via `postMessage` structured clone, not URL fetch.
