---
name: bdbdesignpro
description: "Use when choosing an animation engine, defining motion tokens, adding scroll effects or micro-interactions, or auditing motion for accessibility and performance. Covers engine selection (GSAP, Motion.dev, Anime.js, React-Spring, Three.js, CSS Native), DTCG motion tokens, and the anti-slop/a11y quality gate."
category: design-ui-ux
user-invocable: true
risk: safe
date_added: "2026-09-05"
---

# `/bdbdesignpro` — Motion Engine Router & Anti-Slop Gate

Routes creative-motion decisions to the right engine and enforces motion quality policy (timing tokens, spring physics, accessibility, anti-slop). It does not teach any third-party library's API — that's the vendor's job, or an installed upstream skill's (see [engine-routing.md](./references/engine-routing.md)).

---

## 🎯 When to Use
- Choosing between GSAP, Motion.dev, Anime.js, React-Spring, Three.js, or CSS Native for a specific interaction.
- Defining or applying DTCG motion tokens (durations, easing, spring curves).
- Auditing existing motion for `prefers-reduced-motion`, layout thrashing, or cleanup leaks.
- Scaffolding the **Interaction & Motion Strategy** section of a `01_frontend_spec.md` during `/startcycle`.

---

## 🔄 The 4-Phase Flow

```
[1. Stack & Context Scan] ──▶ [2. Interaction Thesis] ──▶ [3. Engine Routing]
                                                                   │
                        [4. Anti-Slop & a11y Audit] ◀──────────────┘
```

### Phase 1: Stack & Environment Scan
1. Framework & runtime: React 19, Next.js App Router, Vite, Astro, Svelte, Vue, or vanilla.
2. Check `package.json` for already-installed motion libraries (`gsap`, `motion`, `framer-motion`, `animejs`, `@react-spring/web`, `three`, `@react-three/fiber`) — **and their exact version.** Anime.js v3 and v4 are not API-compatible; never assume a version.
3. For Next.js App Router, confirm animated components declare `'use client'`.

### Phase 2: The Interaction Thesis Gate
Never inject animation blindly. Before writing code, state:
- **Role & purpose:** what does this motion communicate — spatial orientation, hierarchy, feedback, narrative?
- **Timing tier:** micro (150ms), state transition (300ms, ceiling 400ms), or scroll-scrubbed (no fixed duration). See [bdb-motion-tokens.md](./references/bdb-motion-tokens.md).
- **Reduced-motion fallback:** the zero-motion alternative, defined now, not retrofitted later.

### Phase 3: Engine Routing
Full routing table, decision flowchart, and anti-patterns: [engine-routing.md](./references/engine-routing.md).
The only engine documented in this skill directly is **CSS Native** ([css-native-patterns.md](./references/css-native-patterns.md)) — no vendor owns plain CSS. Every other engine's API detail is owned by its vendor docs or an installed upstream skill (e.g. `greensock/gsap-skills` for GSAP); this skill routes to it, it does not re-teach it.

### Phase 4: Anti-Slop & a11y Audit
Four mechanically-checkable gates, with grep commands: [antislop-gate.md](./references/antislop-gate.md).
1. Zero layout thrashing (GPU-accelerated properties only)
2. Deterministic cleanup (no leaked timelines/observers)
3. `prefers-reduced-motion` honored — with a real fallback, not just a mention
4. ≤400ms for standard UI transitions

---

## 🔗 Ecosystem Integrations

* **In `/bdbrainstorm`:** runs the Interaction Thesis Interview during Pillar 5 before architectural sign-off. See [bdbrainstorm-hook.md](./integrations/bdbrainstorm-hook.md).
* **In `/startcycle`:** feeds motion tokens, engine choice, and a11y fallback into `01_frontend_spec.md`; Reviewer applies `antislop-gate.md`'s four checks. See [startcycle-hook.md](./integrations/startcycle-hook.md).
* **Agent wiring:** listed in `godmode-ui-ux`'s `skills:` — verify this is still true after any agent-roster change; an unwired skill is a stale claim, not a feature.
