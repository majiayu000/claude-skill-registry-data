---
name: intent-html-renderer-local
description: "Local preserved variant of intent-html-renderer from ~/.agents/skills. Use only when the user explicitly asks for the local variant or wants the newer proof-closure wording preserved alongside the repo baseline. Infer the right browser UI from a user's natural-language intent, goal, task, screenshot inspiration, or desired outcome, then render a usable artifact. Use when the user wants Codex to decide the interface, not specify layout or components: dashboards, workbenches, reports, action-command tools, comparison views, prototypes, widgets, landing pages, or prompt-to-UI surfaces. Prefer detected local UI systems first, especially React, Shadcn, and json-render routes/components; use the global Shadcn render host when the workspace lacks usable UI dependencies; create standalone HTML only for explicit portable-file requests or when the host is unavailable. Do not use for non-UI code changes, pure text answers, or when the user already specified exact implementation details."
---

# Intent UI Renderer (Local Variant)

## Contract

- Treat the user's words as an intent brief, not a UI specification.
- Decide the product surface, information architecture, controls, density, states, and visual hierarchy from the user's goal.
- Detect the local render environment before choosing an output target. If a React/Shadcn/json-render app is available and the user did not ask for a portable file, use the local app path.
- If no usable local UI system exists and the user did not ask for a portable file, prefer the global Shadcn render host over standalone HTML. Bootstrap it with `scripts/ensure_global_shadcn_host.py --install --json` when needed.
- Never default to a bare, neutral, black-and-white UI just because Shadcn components render that way out of the box. If the user explicitly asks for a plain wireframe, austere system screen, or no styling, keep it simple; otherwise infer and apply a deliberate visual treatment.
- When Shadcn is detected, act proactively from the user's intent: inspect the project, choose suitable installed components, choose a style/density direction, add semantic or chart-token visual treatment, and compose a strong UI without asking the user to name components or layouts.
- Prefer the actual usable screen over a page explaining the screen.
- Ask for clarification only when materially different products would be reasonable and choosing silently would likely waste work.
- Ask before applying repo-wide Shadcn presets, reinstalling components, or changing global theme/font/component source. Route-local composition and styling do not need approval.
- Return the absolute artifact path and, when possible, a browser URL or screenshot proof.

## Scope

Use this skill for intent-driven UI generation where Codex must infer the needed interface. Do not use it for ordinary frontend bug fixes, exact mock implementation from a provided spec, non-visual reports, or backend-only changes.

Output one of these target families:

- Native app route/component using the repo's UI system.
- json-render UI tree or preview when the product is a JSON-driven renderer or prompt-to-UI workbench.
- Global Shadcn render host route when the current workspace has no usable UI dependencies and the artifact should still be polished, component-based, and browser-verifiable.
- Standalone HTML/CSS/JS only when requested as a portable artifact, when the global host is unavailable, or when the user explicitly wants a self-contained file.

## Workflow

1. Inspect inputs, screenshots, and local repo guidance. In repos, read `AGENTS.md`, package scripts, existing routes/components, and any Shadcn/json-render evidence before choosing standalone HTML.
2. Run `scripts/detect_ui_target.py --cwd <workspace> --intent "<user request>" --json` when a local workspace exists. If the user explicitly asks for a portable or standalone HTML artifact, that request overrides app/Shadcn detection.
3. If Shadcn is detected, read `references/shadcn-intent-rendering.md`. Run the project package runner with `shadcn@latest info --json` when available; if it fails, run `scripts/extract_shadcn_context.py --cwd <workspace> --json`. Use `shadcn docs <component>` for unfamiliar or complex components when network access is available.
4. Extract intent: target user, job to be done, explicit requirements, implied data, domain, risk, output location, and success state.
5. Choose the UI form without asking the user to design it. Read `references/intent-inference-rubric.md` when the intent is ambiguous.
6. Choose the render target using `references/render-target-selection.md`. If Shadcn/json-render is detected and the user did not ask for portable HTML, do not create standalone HTML. If no local UI target exists, use the global Shadcn render host before considering standalone HTML.
7. Privately sketch the artifact as a small component plan: sections, controls, installed Shadcn primitives, data fixtures, states, interactions, responsive behavior, and Shadcn styling direction. Include at least one concrete visual-treatment decision such as status accents, chart-token washes, semantic token panels, component variants, density, hierarchy, or route-local `color-mix()` accents, unless the user explicitly requested a plain/minimal artifact.
8. Implement with the chosen target:
   - Shadcn/React route: follow `references/next-shadcn-route-pattern.md` and `references/shadcn-intent-rendering.md`; copy from `assets/next-shadcn-page-template.tsx` only as a starting point.
   - Global Shadcn render host route: read `references/global-shadcn-render-host.md`, bootstrap with `scripts/ensure_global_shadcn_host.py --install --json` if needed, and write the artifact under the host's `app/artifacts/<slug>/page.tsx`.
   - json-render tree or prompt-to-UI workbench: read `references/json-render-inspiration.md` and validate saved trees with `scripts/validate_ui_tree.py`.
   - Standalone HTML: copy `assets/standalone-template.html` and validate with `scripts/validate_html_artifact.py`.
9. Run target-appropriate checks before final response. Native app work requires project type-check/build when available plus `scripts/validate_shadcn_route.py` for Shadcn routes. Standalone HTML requires strict HTML validation. In dependency-stripped forks or subagent sandboxes, validate what is available and record the blocked command rather than triggering dependency installs.
10. Browser-check desktop and mobile when possible. Use `references/visual-quality-checklist.md` for final review. Treat browser proof as a state machine, not a boolean: distinguish HTTP reachability, screenshot files written, clean screenshot completion, manual visual inspection, and final visual acceptance. If browser tooling, ports, or screenshots are blocked or partial, use build/type/validator evidence, inspect any written screenshots when possible, and explicitly report the exact proof state.
11. Fix clipping, overlap, blank regions, generic filler, unreadable text, broken interactions, missing local-design-system usage, default-neutral Shadcn output, Shadcn rule violations, and page-level horizontal scrolling before final response.

## Proof Closure Semantics

Do not collapse all proof evidence into "passed" or "failed." Track these states:

```text
route_created -> route_validated -> typecheck/build_passed -> server_http_200
  -> screenshots_written -> screenshots_visually_inspected -> visual_acceptance_passed
```

Rules:

- `server_http_200` is reachability, not visual proof.
- `screenshots_written` is evidence, not acceptance.
- If `browser_proof.py` returns `proofState: partial_visual_evidence`, inspect the written desktop/mobile screenshots with available image tools and report "partial browser proof" unless a clean rerun succeeds.
- If screenshots show clipping, overlap, blank regions, unreadable controls, or page-level horizontal scrolling, fix the artifact, rebuild/recheck, and recapture.
- Claim browser proof complete only when screenshots capture cleanly and visual inspection passes, or state clearly which proof state is missing.

## Resource Index

- `references/render-target-selection.md`: Read before implementation to choose app route, json-render, or standalone HTML.
- `references/global-shadcn-render-host.md`: Read when the current workspace lacks usable local UI dependencies and the artifact should still use real Shadcn-style components.
- `references/intent-inference-rubric.md`: Read when the prompt states an outcome but not a UI.
- `references/next-shadcn-route-pattern.md`: Read when a React/Shadcn app is detected.
- `references/shadcn-intent-rendering.md`: Read when Shadcn is detected; use it to inspect context, choose components/styles, and handle presets safely.
- `references/json-render-inspiration.md`: Read for prompt-to-UI workbenches, JSON-driven previews, and saved UI trees.
- `references/visual-quality-checklist.md`: Read before browser proof and final response.
- `references/pressure-tests.md`: Read when validating or improving this skill.
- `references/forward-test-scenarios.md`: Read when forward-testing the skill with subagents or repeatable scenario prompts.
- `assets/standalone-template.html`: Starting point only for standalone HTML artifacts.
- `assets/next-shadcn-page-template.tsx`: Starting point only for native Next/Shadcn route artifacts.
- `scripts/detect_ui_target.py`: Detect local UI systems and recommended target.
- `scripts/ensure_global_shadcn_host.py`: Create or refresh the global Next/Shadcn render host and optionally install dependencies.
- `scripts/extract_shadcn_context.py`: Extract local Shadcn context when `shadcn info --json` fails.
- `scripts/browser_proof.py`: Capture desktop/mobile screenshots for a URL or standalone HTML file when a Chrome-compatible browser is available.
- `scripts/validate_shadcn_route.py`: Validate a Shadcn route actually uses local UI components.
- `scripts/validate_html_artifact.py`: Validate standalone HTML artifacts.
- `scripts/validate_ui_tree.py`: Validate flat UI tree JSON, optionally against catalog and registry files.
