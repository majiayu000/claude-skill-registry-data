---
name: code-splitting
description: "next/dynamic code splitting and build-graph cost; first stop for build failures. Use before lazy-loading or deferring a heavy component, adding a dynamic import, React.lazy, or ssr: false; on 'window is not defined' or a hydration mismatch; shrinking the bundle; or on 'build failed', OOM, SIGKILL, a slower build, or 'Collecting page data'."
---

# code-splitting — `next/dynamic` done right

One job: keep heavy **client** code out of the server render and out of the initial load, fetching its chunk only when actually needed. Done wrong it's pure cost (extra waterfalls, blank screens, hydration mismatches) with none of the win.

**Routing:** adding, removing, or moving a dynamic import → this file, top to bottom. **Also read [build-time-bloat.md](build-time-bloat.md) when** the build failed (OOM / SIGKILL / "Collecting page data") or build time grew (start at rule 3 and the anti-patterns table here), **or before** replacing a `dynamic()` with a static import, or statically importing a heavy client module into a Server Component, layout/provider, shell, or barrel — that exact change took the prod build 15 → 24 min, and its leak signature lives only there. The fragmentation campaign's measured incident, diagnosis order, and fix pattern: [docs/handoffs/build-graph-fragmentation-campaign.md](docs/handoffs/build-graph-fragmentation-campaign.md).

## The one mental model

`dynamic(() => import(...))` does **three separable things**. Confusing them is every mistake below:

1. **Creates a separate chunk** — happens always, just from the `import()`. Not "in the main bundle."
2. **`ssr: false` → excludes it from the server render** — happens whenever you pass `ssr:false`, conditional or not. This is what keeps browser-only deps (anything touching `window`, canvas, editors, jspdf, maps) off the server and kills hydration mismatches.
3. **Defers the *client* fetch until render** — only pays off when the component is **conditionally rendered**. Render it unconditionally on mount and the chunk fetches immediately anyway — often as an extra waterfall.

So `dynamic()` itself saves nothing. The **`ssr:false`** earns benefit #2; the **condition you render it behind** earns benefit #3. Name which one you're after before you write it.

**Build time is a fourth, separate axis — and conditions are INVISIBLE to it.** The bundler creates chunks by static analysis alone; a render condition, click gate, `useEffect` check, or `loading:` fallback changes nothing about the build. What the build pays for a module ≈ **size × compilation passes × route entries whose static graph reaches it** (~1,000 entries in this app; statically-reachable = server AND client pass; behind `ssr:false` = client only). An `import()` boundary cuts entries to zero and passes to one — that is the entire build win. Conditions only move the browser *fetch*.

## The six rules

1. **A Server Component cannot use `dynamic({ ssr: false })`.** Next.js throws. A server file stays a thin static shell; the heavy widget *below* it owns its own splitting inside a `"use client"` child. See the prose contract in [app/Providers.tsx](app/Providers.tsx) — it documents exactly this.

2. **Never stack `ssr:false` boundaries down one render path.** One boundary covers everything beneath it. A second one close below = a sequential **waterfall** (load chunk A → only then discover & fetch chunk B), a fragmented chunk graph, and **zero** extra benefit. See the warning baked into [lazyOverlay.tsx](features/overlays/boundary/lazyOverlay.tsx).

3. **THE FRAGMENTATION LAW — fewer boundaries, at the edge. Never mass-convert `React.lazy` → `next/dynamic`.** Every `next/dynamic` call manufactures a loadable component: a react-loadable-manifest entry with chunk-group resolution computed per consuming context. `React.lazy` is just an async edge inside the parent's EXISTING chunk graph — no manifest entry, no new chunk groups. Build memory and build time scale with chunk-group count, which is a DIFFERENT axis from bundle size. **Measured 2026-07-27:** converting ~190 lazy sites to `dynamic(ssr:false)` (408→~600 loadables) OOM-killed a build that had 30 straight green runs — verified by a clean 3-way experiment on identical 60GB machines: baseline green 12m; baseline+conversions **OOM (DNF)**; baseline+the-same-surfaces-CONSOLIDATED (~90 lazy/dynamic sites → all-static inside ONE `dynamic` edge per surface, 5 edges total) **green in 8m, −108MB output — 33% faster than the untouched baseline**. The model is [MarkdownStream.tsx](components/MarkdownStream.tsx): a giant feature compiled as ONE piece behind ONE edge. So: a registry of N `dynamic()` entries is a defect unless the N items genuinely open one-at-a-time on user action (lazyOverlay's windows); a set that belongs to one surface goes STATIC inside an Impl with a single `dynamic` front door. `React.lazy` living inside an already-gated graph is CHEAPER for the build than `dynamic` — leave it, or better, consolidate it to static; only a truly server-reachable site whose SSR you must kill warrants a new `dynamic(ssr:false)`, and then exactly ONE, at the edge.

4. **A dynamic import without a condition does nothing (benefit #3).** If you `dynamic()` something and then always render it, you paid the split cost for no deferral. Gate it (modal open, tab, route, `useIdleReady`, feature flag) — or, if it genuinely must always be live, keep it only for the `ssr:false` reason (benefit #2) and say so.

5. **`loading` and an error boundary are not optional for user-triggered chunks.** A bare `dynamic()` whose chunk stalls or fails renders **nothing**, silently. For overlays/windows that's solved for you — see Method B. Elsewhere, at minimum pass `loading: () => …` (use `() => null` only when nothing-until-ready is correct).

6. **A click handler's machinery loads at click time when the handler module is shell-reachable.** An action registry statically imported by the sidebar/shell (e.g. [navActions.ts](features/shell/navigation/navActions.ts)) is in EVERY route entry's static graph — its imports are multiplied across all of them. Thunks and services go `await import()` **inside the handler body**; only ids, router, toast, and redux hooks stay static. One static thunk edge there once dragged the 420-module war-room engine into ~630 entries; deferring it cut the prod build **2.5 min** (2026-07). The file's BUILD-GRAPH LAW header is the contract. **CAVEAT — `await import()` is NOT free when the importer is ubiquitous AND the target is a mega-cluster.** The async edge still creates a chunk-group split multiplied across every context that reaches the importer. Canonical incident (D115, 2026-07-28): ONE `await import("@/features/content-ir/registry/component-registry")` inside `toolStateEffects.ts` (statically reachable via `process-stream.ts` from ~every route) added **+14 GB peak build RSS and +50% compile time**, OOM-killing 12 straight Vercel builds (v0.4.199-210); bisect-proven by revert (v0.4.212 → 12 min, clean). In that shape, **invert the dependency instead**: the big cluster registers an invalidation/action callback into a tiny shared registry at its own init (it is already initialized wherever its output can render), and the ubiquitous module fires the callback by name — zero import edge in either direction beyond the tiny registry. **A "correct" front-door `dynamic()` gate is NOT a fix for this shape either** — measured (ProTextarea→AgentPanel, v0.4.225, bracket-reverted same day): one gate from a ~106-context importer to the 1,569-module engine cost **+1.0min compile / +1.1GB RSS on every build** in exchange for −3MB first-load. If no inversion exists (in-place panel, no route), shipping the gate is a deliberate page-weight-vs-build-cost product decision for Arman, never a drive-by optimization.

## Two ways to do it

### Method A — split in place (conditional)

The consuming **client** component declares the dynamic component at module scope and renders it **only behind a condition**. Best when one component conditionally reveals something heavy.

```tsx
"use client";
import dynamic from "next/dynamic";

const RecoveryWindowImpl = dynamic(() => import("./RecoveryWindowImpl"), {
  ssr: false,
  loading: () => null,
});

export function RecoveryWindow() {
  const { isOpen } = useRequestRecovery();
  if (!isOpen) return null;        // ← the condition is the whole point
  return <RecoveryWindowImpl />;
}
```

Real exemplars: [RecoveryWindow.tsx](features/request-recovery/components/RecoveryWindow.tsx) (gated on `isOpen`), [DeferredIslands.tsx](features/shell/islands/DeferredIslands.tsx) (three imports behind **one** `useIdleReady` gate — batch, don't fan out boundaries).

### Method B — split once in a wrapper (the "front door")

For a heavy component used in **many** places, don't make every callsite remember to `dynamic()` it. Do the split **once** in a wrapper and:

- **Export only the wrapper.** Rename the heavy core to something nobody would import — convention here is **`*Impl`**.
- **Export the props type from the wrapper shell**, so consumers get types without pulling the impl into their graph.

```tsx
// MarkdownStream.tsx — the only importable name
import dynamic from "next/dynamic";
export interface MarkdownStreamProps { /* … types live in the shell … */ }

const MarkdownStream = dynamic(() => import("./MarkdownStreamImpl"), { ssr: false });
export default MarkdownStream;          // MarkdownStreamImpl is never imported directly
```

Real exemplars:
- [MarkdownStream.tsx](components/MarkdownStream.tsx) → `MarkdownStreamImpl` — the canonical case. Hides a huge rich-document engine; type lives in the shell.
- [UploadGuardHost.tsx](features/files/upload/UploadGuardHost.tsx) → `*Impl` — wrapper also re-exports the **imperative API** (`requestUpload`) statically, so callers get the API without the dialog tree. (Always-rendered host: benefit #2 only — that's the right call for an app-shell singleton.)
- [lazyOverlay.tsx](features/overlays/boundary/lazyOverlay.tsx) — the **system-level** Method B: one primitive wraps ~90 overlays with `ssr:false` + canonical `loading` + error boundary + a load-timeout that converts a hung `import()` into a catchable error. **Every overlay/window goes through `lazyOverlay`, never a bare `dynamic()`.** (See the `overlay-system` and `window-panels` skills.)

**Pick B when:** the component is heavy AND used in 2+ places, OR it's a singleton host, OR it must stay off the server render everywhere. **Pick A** for a one-off conditional reveal.

### Method C — render-all bundle (wrapper → core)

For a set of components that **always render together** (app-shell singletons, a provider group), do NOT give each its own `dynamic()` — that's N boundaries, N fetches, N chunk-graph entries for zero deferral. Package them: a thin `"use client"` wrapper holds every gate (client-only mount, `useIdleReady`) and **ONE** `dynamic(() => import("./XCore"), { ssr: false })`; the core statically imports and directly renders everything. Measured: converting the deferred-singletons tree from ~10 sibling dynamics to one wrapper→core cut the build **30–40 s** (2026-07).

- Exemplar: [DeferredSingletonWrapper.tsx](app/DeferredSingletonWrapper.tsx) → `DeferredSingletonCore.tsx` — the split contract is documented in the wrapper's header (incl. why the bundle-leak guard's side-effect import must stay in the shell).
- **Provider variant** (the component wraps `{children}` / owns a context): the shell keeps the context object, hook, value type, and an **inert default**, and renders the provider element IMMEDIATELY — children mount at once and never remount. The core is a null-rendering sibling *inside* the provider that publishes the live value up via `onValue`. Exemplar: [WindowPersistenceManager.tsx](features/window-panels/WindowPersistenceManager.tsx) → `WindowPersistenceCore.tsx`.

**B vs C in one line:** Method B (id → chunk, like `lazyOverlay`'s 110 windows) is for things rendered **selectively** — split per item so each loads alone. Method C is for things rendered **all together** — one boundary for the whole set. Applying B's per-item splitting to an always-rendered set is pure cost.

## What NOT to do — verified anti-patterns

| Anti-pattern | Where | Why it's wrong |
|---|---|---|
| **Stacked `ssr:false` on one path** | [AssistantCardStack.tsx:37](packages/chat/src/agents/components/agent-widgets/chat-assistant/AssistantCardStack.tsx#L37) `dynamic(AgentAssistantMessage)` — itself inside the `lazyOverlay(AgentChatAssistant)` boundary, and rendering `MarkdownStream` (a third `ssr:false`). Same shape in the importer-less `features/cx-chat/components/messages/MessageList.tsx` and `packages/chat/src/cx-conversation/MessageList.tsx` | Three boundaries, one render path → extra waterfalls. `AgentAssistantMessage` also renders for **every** assistant message, so benefit #3 ≈ 0. Fix: import `AgentAssistantMessage` statically; the overlay boundary above and the `MarkdownStream` boundary beneath already do the split. Removing a `dynamic()` anywhere NOT already under such a boundary → read [build-time-bloat.md](build-time-bloat.md) first. |
| **Dynamic but unconditional** | same file, [line 204](packages/chat/src/agents/components/agent-widgets/chat-assistant/AssistantCardStack.tsx#L204) — `AgentAssistantMessage` renders whenever `msg.role === "assistant"` | Chunk fetches on every assistant open regardless. Split cost, no deferral. |
| **Mass `lazy` → `dynamic` conversion (fragmentation)** | the reverted 2026-07-27 campaign (v0.4.124–132): peek registry ×19, settings `lazyTab` ×39, artifact-renderers ×30, +67 long-tail | Each conversion added a loadable/chunk-group per consuming context; +~190 loadables OOM-killed a 30-green-streak build. Rule 3 (Fragmentation Law): consolidate to static inside ONE edge instead — measured 33% FASTER than baseline. |
| **`dynamic({ssr:false})` in a Server Component** | guarded against in [app/Providers.tsx](app/Providers.tsx) | Build error. Push the dynamic import into a `"use client"` child. |
| **Bare `dynamic()` for an overlay/window** | — | Bypasses `loading`/error/timeout. Use `lazyOverlay`. |
| **Static thunk/service import in a shell-reachable action module** | navActions.ts, fixed 2026-07 (rule 6) | Multiplied the 420-module war-room engine across ~630 route entries (+2.5 min build). `await import()` in the handler body. |
| **N sibling `dynamic()`s for an always-rendered set** | old `DeferredSingletons.tsx`, replaced 2026-07 | 10 boundaries for components that all mount anyway = 10 fetches, no deferral. Method C: one wrapper→core (−30–40 s build). |
| **`await import()` of a mega-cluster from a ubiquitous module** | `toolStateEffects.ts` → content-ir registry, reverted in v0.4.212 (D115) | The handler-body pattern (rule 6) detonates when the importer is in ~every context AND the target is a huge graph: +14 GB build RSS, +50% compile, 12 OOM'd builds from ONE line. Invert via a tiny callback registry (rule 6 caveat) instead. |

## Build-time bloat — the recurring leak: hunt it, then guard it

**Build failed, OOM/SIGKILL, or build time grew — OR you are replacing a `dynamic()` with a static import, or statically importing a heavy client module into a Server Component, layout/provider, shell, or barrel → read [build-time-bloat.md](build-time-bloat.md)** — Step 0 (prove the regression is in the tree), the leak signature and its 15 → 24 min incident, blast-radius ranking, the hunt method, the eslint guard, and the analyzer fallback when the hunt comes back clean.

**Measure before moving: `pnpm lab:graph`** ([scripts/build-lab/](scripts/build-lab/README.md)) computes the whole law deterministically in seconds — THE COMPILE BILL (every cluster's size × entry-context multiplicity) and every dynamic edge ranked by the D115 product. Run it before AND after any graph change; `pnpm lab:run <label>` ground-truths a ref with a full local build (peak RSS is the trustworthy metric — single-run compile time has ±1.5-2min noise, which is how five plausible "fixes" (v0.4.217-221) all shipped as regressions). Never test a build hypothesis by pushing to Vercel.

## Before you ship — checklist

- [ ] **Which benefit am I buying?** `ssr:false` (off the server) and/or a real **condition** (deferred fetch). If neither, delete the `dynamic()` and import statically.
- [ ] **Is there already an `ssr:false` boundary above me on this path?** If yes, import statically — don't stack.
- [ ] **Server Component?** Then no `ssr:false` here — move it into a client child.
- [ ] **Many callsites / a singleton / a heavy core?** Use Method B (`*Impl` + wrapper + type in the shell), not a `dynamic()` at every site.
- [ ] **A set that always renders together?** ONE wrapper→core boundary (Method C), never N sibling `dynamic()`s.
- [ ] **Handler in a shell-reachable action module?** Its machinery is `await import()`ed inside the handler body (rule 6) — **unless the target is a mega-cluster (registry, whole-feature graph): then invert via callback registry (rule 6 caveat / D115), never an import edge.**
- [ ] **Tempted to convert `React.lazy` → `next/dynamic`, or to add a registry of dynamics?** STOP — rule 3 (Fragmentation Law). Consolidate to static inside one edge boundary instead; only a server-reachable site you must keep off SSR gets a (single, edge) `dynamic`.
- [ ] **User-triggered?** Has a `loading` fallback (overlays/windows → `lazyOverlay`, which adds error + timeout too).
