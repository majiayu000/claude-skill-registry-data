---
name: new-package
type: Skill
title: "new-package — create or majorly grow an @ai-matrx package, the right way"
description: "Runbook for creating or majorly growing an @ai-matrx TypeScript npm package. Use when invoked as /new-package <name or capability>, or for a new @ai-matrx/* package, extracting code into one, or a major growth wave. NOT for a routine fix inside an existing package (THE SAME-SESSION LAW)."
tags: [packages, typescript, npm, extraction, runbook, architecture]
timestamp: 2026-08-30
---

<!-- SYNCED COPY — do not edit here.
     Canonical: common-docs/skills/new-package/SKILL.md
     This file is distributed to every consuming repo by
     common-docs/meta/scripts/sync_skills.py. Edit the canonical, run the
     sync, and commit each repo. Edits made here are overwritten and lost. -->

# new-package — create or majorly grow an @ai-matrx package, the right way

**Invocation: `/new-package <name or capability>`.** Use for: a NEW `@ai-matrx/*` package,
extracting existing code into one, or a major growth wave on a shipped one.
**NOT for:** a routine fix/addition inside an existing package — that is
[THE SAME-SESSION LAW](/policies/typescript-package-standard.md) (fix in-package, release,
adopt, one session; no ceremony).

## Step 0 — which side?

A **Python** package (pip, `aidream/packages/matrx-*`) → STOP: walk the Gate in
`aidream/docs/packages/PACKAGE_DOCTRINE.md` instead. This skill governs **TypeScript
`@ai-matrx/*` npm packages** only (authored at `aidream/apps/shared/<name>`).

## Step 1 — the law stack (read ALL before designing anything)

1. [`/policies/typescript-package-standard.md`](/policies/typescript-package-standard.md) —
   the ENTIRE policy: THE ALL-INCLUSIVE LAW, THE LATEST LAW, THE CATCH-UP RULE, THE
   SAME-SESSION LAW, ONE SYSTEM ONE VERSION, mechanics, gates, release procedure.
2. [`/projects/npm-package-extraction/DECISIONS.md`](/projects/npm-package-extraction/DECISIONS.md)
   — C1–C31 are SETTLED; re-litigating one is an error. Headline: C8 split-out · C9 full
   elimination · C10 persistence boundary · C19 inlined SVGs · C21 direct-on-main + fleet
   testing prompt · C22 hard parts in the package · C23 all-inclusive · C25 bindings at the
   first real consumer · C26 token contract · C28 catch-up · C29 same-session.
3. [`/policies/package-vs-implementation.md`](/policies/package-vs-implementation.md) —
   the package is CAPABLE, the implementation CHOOSES; broken in both directions before.
4. **The exemplar: `aidream/apps/shared/tap-target`** — the retrofit register's one
   "passes" row (own CSS shipped, inlined glyphs, 20-line host setup). Copy its shape.
5. Touching a shipped package? Current live state first:
   [`/projects/npm-package-extraction/ALL-INCLUSIVE-RETROFIT.md`](/projects/npm-package-extraction/ALL-INCLUSIVE-RETROFIT.md)
   + [`STATUS.md`](/projects/npm-package-extraction/STATUS.md).

## Step 2 — census LIVE, then the design doc (before any code)

Per C14: pull latest `main` in every touched repo first; any measurement older than a day
is unverified. Census the real code: source files, line counts, literal-import consumer
counts, the coupling edges to invert.

Write `<NAME>-PACKAGE-DESIGN.md` in `/projects/npm-package-extraction/`. It MUST declare:

- **Scope + the three C23 tests** (likely to fail / needs tuning / must be perfect → IN the
  package) and what ships COMPLETE: polished UI, hooks, integrations, a working DEFAULT for
  every port — hosts inject only identity (auth source, org/env values, navigation, sinks).
- **What it deliberately does NOT absorb** (C8) — every proposal states its split-outs.
- **Persistence boundary** (C10), one of: owns-persistence · persistence-injected ·
  no-persistence.
- **The port table**: required/optional, a defined degradation for each, a shipped default
  for each (C22/C23).
- **Demanded schema** (owns-persistence packages): the exact RPC/table contract + a
  falsifiable probe (the associations `assertDemandedSchema` precedent — it must be able
  to FAIL).
- **Wire shapes verified against aidream SERVER source** — never guessed from a client.
- **Sibling deps**: ordinary dependencies, never peers (only react/react-dom/react-native
  stay peers); the graph stays a DAG — `node aidream/scripts/check_ts_sibling_graph.mjs`.
- **Styling per C26** (structural CSS ships; token CONTRACT enforced; default token sheet;
  token VALUES host-owned) and **icons per C19** (own inlined SVGs, no icon-library dep).
- **Open questions WITH recommendations** at the bottom.

## Step 3 — Arman's approval, per package, by name (C5)

Creating a package is an architecture decision: the NAME and scope are his explicit call,
raised single-topic — never embedded in a broader plan's approval. Interview format: facts
→ your recommendation → options; at most two decisions per turn; record answers into
DECISIONS.md immediately. No code before the go.

## Step 4 — build

Author at `aidream/apps/shared/<name>`. The policy's Authoring rules section is the
contract; the traps that have actually bitten:

- **Behavior ports VERBATIM; only coupling seams invert.** A real defect found in the
  original is fixed in-package AND CHANGELOG'd — never silently, never "preserved."
- Dual ESM+CJS with matching `.d.ts`/`.d.cts`; no framework imports in package source.
- `"use client"` per-entry, never global; tsup `treeshake: false` or the banner drops —
  verify the stamp per chunk.
- **Module-level mutable state is BANNED** → `globalThis` under
  `Symbol.for("ai-matrx.<pkg>.<name>")` (dual-loader graphs split module state).
- TS strict + `exactOptionalPropertyTypes` + `noUncheckedIndexedAccess`, zero `any`;
  branded types for identity values; host-generated JSON boundaries typed over `unknown`.

## Step 5 — gates (ALL of them, before release)

Strict typecheck · behavioral tests · publint + attw · **packed-tarball canary**: install
the `.tgz` into an empty project and `import` AND `require` every public entry · the host
app's typecheck/tests/build · a real browser smoke for device/permission behavior. A green
source build is NOT package proof.

## Step 6 — release

Bump + CHANGELOG — **with a `Consumer action` section whenever adoption requires host
changes (C28)**; a breaking release without one is a defect. Commit, push, then tag
`npm/<DIRECTORY-name>/v<version>` — the directory name, not the npm name (the
`npm/matrx-agents/v*` lesson). Trusted publishing does the rest. A **brand-new** package
needs Arman's one-time 2FA bootstrap publish + trusted-publisher binding — hand it to him
as a guided session (one link, what to click, what to report); it is the only manual
release that package will ever have.

## Step 7 — adoption IS the definition of done (C9, same session)

Publication is not done. Same session (C29): swap a real consumer, **DELETE the
originals**, prove zero remnants by re-grep, run the host type gate + touched suites, live
smoke the render paths. Per C21 the swap lands direct on main and ships with a
**fleet-testing prompt** for Arman's Sonnet/Codex agents (concrete routes, actions,
expected behavior, known deltas, bug classes to hunt); register the QA re-test row. A
package whose swap has not run is a bullshit package — two live copies is the named
disaster (the scraper lesson).

## Step 8 — the paper trail (same session)

Package README (external consumer guide) + `FEATURE.md` beside the code · a row in
`aidream/apps/shared/README.md`'s catalog · the campaign
[`STATUS.md`](/projects/npm-package-extraction/STATUS.md) board ·
close/open the register rows you touched. Commit and push everything — unpushed work
doesn't exist.

## Change log

- **2026-08-30** — Created at Arman's request as the trigger for package creation/growth,
  distilling the typescript-package-standard policy + campaign rulings C1–C31 into the
  ordered runbook (census → design doc → approval → build → gates → release → C9 adoption
  → paper trail).
