---
name: civiltekk-nextjs-skill
description: >-
  Next.js engineering, four routes. scaffold: scaffold standardized Next.js
  16 demos — shadcn, Tailwind v4, src directory with path aliases, React
  Compiler, Tekk-prefixed components. runtime-diagnosis: next-devtools-mcp —
  Next.js 16+ runtime diagnosis via MCP (get_errors, get_logs, get_routes,
  server actions); config and workflows. image-usage: proper Next.js 16
  Image component usage with configuration for remote domains, responsive
  images, and breaking changes from previous versions. threejs: Three.js +
  Next.js (App Router, React 19) integration — SSR pitfalls, GLSL bundling,
  hydration, WebGL context loss, R3F/drei, WebXR, companion-library decision
  tree; version detection first.
license: Apache-2.0
compatibility: opencode
metadata:
  pattern: "mcp-diagnosis, image-implementation"
category: Framework-Specific
---

Consolidates nextjs-standard-setup-skill + nextjs-devtools-mcp-skill +
nextjs-image-usage-skill + threejs-nextjs-skill (#604). Alias: formerly
those four skills.

## What I do

Next.js 16 engineering across four routes:

1. **Detect the route** (§Routes) — explicit > inferred > ask-once.
   Explicit: the request names the activity ("create next.js app",
   "scaffold next.js", "new next.js demo" → `scaffold`; "next.js errors",
   "debug next.js", "server action not working", "nextjs mcp" →
   `runtime-diagnosis`; `<img>` in Next 16 code, "remote image domains",
   "images.remotePatterns" → `image-usage`; "three.js", "R3F", "drei",
   "WebGL canvas", "WebXR" → `threejs`). Inferred: the artifact shape (a
   new project or a house-structure standardization → `scaffold`; a
   running app's errors/routes/logs/metadata → `runtime-diagnosis`; image
   tags or image config → `image-usage`; 3D/WebGL scene code → `threejs`).
   Ambiguous ("make this Next.js app work") → ask once per run, then
   proceed on the answer.
2. **Load the route's values file** (§Side files) and apply its contract.
   The §Runtime-diagnosis availability gate below applies BEFORE any
   `runtime-diagnosis` MCP call — it lives here, not in a values file.
3. The routes compose — a scaffold pass applies route `image-usage` rules
   from the start (`next/image` everywhere); a diagnosis on a Three.js app
   walks `runtime-diagnosis` then `threejs` for scene-specific pitfalls.
   Load per request, not all four up front.

## Runtime-diagnosis availability gate (hard)

`runtime-diagnosis` MCP tools work ONLY when ALL of these hold — check
before the first tool call, not after a failure:

| Requirement | Status |
|-------------|--------|
| Next.js 16+ (built-in `/_next/mcp` endpoint) | project dependency |
| Running Next.js dev server (`npm run dev`) | required for live features |
| `next-devtools` server in `opencode.json` `mcp.servers` | required for MCP tool access |
| `permissions` rule `{ "action": "next-devtools*", "resource": "*", "effect": "allow" }` | **no rule by default** — user must opt in |

If ANY requirement is unmet, MCP tools return connection errors — that is
an environment gap, not an app bug; do not retry-loop it.

**File-based fallback (always available, no MCP needed):**

- **Routes:** glob `app/**/page.{tsx,ts,jsx,js}` and `app/**/route.{tsx,ts,jsx,js}` + `pages/**/*.{tsx,ts,jsx,js}` for Pages Router
- **Page metadata:** read page files directly to detect `'use client'` directives and `export const metadata`
- **Server Actions:** grep for `'use server'` to locate action files
- **Errors:** cannot be replicated — instruct the user to share error output or enable MCP

The exact `opencode.json` config values, tool inventory, and workflows
live in `references/devtools-mcp.md` (load it once the gate passes, or to
guide the user through enabling the server).

## Side files (load rules)

| Read | When | Use |
|------|------|-----|
| `references/setup.md` | route `scaffold` | house-standard bootstrap command, `src/` layout, Tekk naming/export rules, React Compiler, project OpenCode LSP wiring |
| `references/devtools-mcp.md` | route `runtime-diagnosis` (gate passed, or guiding enablement) | `opencode.json` config values, the 6 MCP tools, diagnosis/route/audit workflows, common MCP failures and fixes |
| `references/image.md` | route `image-usage` | `<img>` → `<Image />` auto-convert policy, Next 16 breaking-change table, `remotePatterns` config, failure → fix map |
| `references/threejs.md` | route `threejs` | version-detection-first rule + dated version matrix, version-sensitive areas, pitfall catalog (SSR / hydration / bundler / dispose), companion-library decision tree |

Side files carry VALUES only; this file carries the METHOD plus the
availability gate and file-based fallback above.

## Routes

| Situation | Route |
|-----------|-------|
| "create next.js app", "next.js setup", "scaffold next.js", "new next.js project", "initialize next.js"; standardizing an existing project onto the house structure | `scaffold` |
| "next.js errors", "nextjs debugging", "debug next.js", "next.js build failing", "server action not working", "next.js hydration error", "nextjs mcp"; route mapping, page/project metadata, project audits | `runtime-diagnosis` |
| Any `<img>` tag in (or proposed for) Next.js 16 code; remote images fail to load / `next/image` config errors; external image domains or responsive layouts; migrating from Next.js 13/14/15 | `image-usage` |
| Three.js / R3F / drei / WebXR in a Next.js App Router + React 19 project; SSR failures, GLSL bundling under Turbopack, hydration mismatches, WebGL context loss | `threejs` |
| Ambiguous | ask once (§What I do step 1), then route |

## Boundaries

- The four routes were formerly peer skills that cross-referenced each
  other (the setup member pointed at the image member; the image and
  Three.js rules interact) — that boundary is internal now; the
  route table above is the boundary logic.
- Internal exception: inside drei `<Html>` portals, plain `<img>` is
  sanctioned (route `threejs` pitfall `next-image-inside-drei-html`) —
  route `image-usage`'s auto-convert rule does not apply there.
- React correctness/perf (hooks/render anti-patterns, bundle size,
  re-renders) → `civiltekk-react-quality-skill`; unit tests →
  `civiltekk-test-generation-skill` (route `nextjs`); AWS Amplify deployment →
  `amplify-nextjs-deployment-skill`; accessibility →
  `accessibility-a11y-skill`; Python backend equivalent →
  `civiltekk-python-backend-skill` (route `scaffold`).
- `nextjs-specialist-subagent` is the agent that loads this skill by mode
  (scaffolding → `scaffold`, diagnosis → `runtime-diagnosis`, audit →
  `runtime-diagnosis` over routes/metadata).

## Agent behavior rules

- **Version-sensitive claims first** (`threejs`): never give
  version-specific code before confirming versions — follow
  `references/threejs.md` §Version detection first. Generic architectural
  guidance (e.g. "use `'use client'`") is safe without versions; concrete
  imports/JSX are not.
- **Auto-convert, don't ask** (`image-usage`): when an `<img>` tag is
  proposed in Next.js 16 code, convert it per the house rule without
  asking — the conversion policy is not a decision point.
- **Gate before calling** (`runtime-diagnosis`): run the availability gate
  §above before the first MCP tool call; on failure, fall back to
  file-based inspection and note the limitation in the Return Contract.
- Headless/CI: no asks — read the route from the delegation prompt, use a
  documented default, or return `Status: partial` with the gap.

## Return Contract

```
**Status:** [success | partial | failed]
**Output:** [file path(s) / key result, one line]
**Summary:** route `{route}` — [2–3 sentences max]
**Issues:** [blockers, incl. MCP availability gaps, or "None"]
```
