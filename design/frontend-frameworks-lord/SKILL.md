---
name: frontend-frameworks-lord
always: true
description: Deep mastery of React, Vue.js, Angular, and Svelte.
triggers:
  - frontend frameworks lord
  - react

---
[SKILL] frontend-frameworks-lord
[OBJ] Architect and optimize frontend stacks across React, Vue, Angular, Svelte.
[RULES]
1. [CMD] IDs: React `/reactjs/react.dev`, Vue `/websites/vuejs`, Angular `/websites/angular_dev`, Svelte `/websites/svelte_dev_svelte`; Tailwind CSS `/tailwindlabs/tailwindcss.com`; page sections `page-sections-lord`.
2. [REQ] Pillar coverage: component architecture, reactivity models, state management, routing/navigation, rendering strategies (CSR/SSR/SSG/islands), performance, DX/build tooling, accessibility/i18n, testing.
3. [REQ] Query framework ID with full question + topic (hooks, signals, routing, performance).
4. [REQ] For landing-page/section-based UIs, query `page-sections-lord` and `backend-frameworks-lord`; render blocks by `type` with one component per section; keep props flat under `data`.
5. [REQ] Compare frameworks by API and rendering behavior, not brand.
6. [REQ] Mention version-sensitive APIs; default to latest stable major.
7. [REQ] Reactivity models are the deep difference: React = re-render on state change (immutability + memo discipline), Vue = proxy-based fine-grained (mutate, framework tracks), Svelte = compile-time reactivity (assignments are updates), Angular = signals + RxJS coexistence. State advice must match the model — mutating state in React or spreading-rebuilding in Vue is fighting the framework.
8. [REQ] React specifics: hooks rules are architectural (conditional hooks break state); effects are for syncing with EXTERNAL systems — derived data = compute in render/memo, not effect-chains; Server Components change the data-flow model (server by default, `'use client'` boundaries deliberate); concurrent features (transitions, Suspense) are the modern path.
9. [REQ] State placement: URL for sharable/navigation state, server cache (TanStack Query/SWR) for remote data, context for low-churn cross-cutting, store (Zustand/Pinia/NgRx) only for true shared client state. The biggest perf bug is usually state living too high or in the wrong taxonomy.
10. [REQ] Rendering strategy per route: SSG content pages, SSR/streaming for personalized public, SPA for auth-gated apps, islands/partial hydration for mostly-static pages. Hydration cost + bundle per route are budgets.
11. [REQ] List & input perf: keyed lists always (index keys = state bugs under reorder), virtualize >~100 rows, debounce search inputs, uncontrolled inputs where re-render cost matters, form libraries (RHF/VeeValidate/Angular Reactive) over hand-rolled for non-trivial forms.
12. [REQ] Component boundaries: presentational vs container split where complexity demands, props down/events up (React/Angular) vs v-model/emits (Vue), slots/content-projection for composition. Shared primitives in a design system, page components stay thin.
13. [REQ] Framework selection honesty: React = ecosystem + hiring + RSC direction; Vue = gentlest learning curve + best template ergonomics; Angular = batteries-included enterprise (DI, RxJS, opinionated — heavier ramp); Svelte = least runtime + best DX, smaller ecosystem. Pick for team + app shape, not hype.
14. [REQ] Testing per model: component tests in the framework's idiom (RTL/Vue Test Utils/TestBed), interaction tests over implementation details, E2E thin layer on critical flows only.
15. [PROHIBIT] Effect-chains for derived data, global stores for server cache, conditional hooks, index keys on dynamic lists, `any` to silence framework typing, or mixing paradigm-adjacent patterns (RxJS-style streams inside React renders).
