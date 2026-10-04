---
name: aetherbrowser-operator
description: Operate AetherBrowser as the primary online task surface across search, GitHub, Codespaces, research, Notion, Hugging Face, Shopify, and general web work. Use when Codex should drive a real browser session first, coordinate with built-in search or fetch tools second, capture page-state proof, and keep online work inside the SCBE browser lane instead of defaulting to generic web automation.
---

# AetherBrowser Operator

Use AetherBrowser as the first-choice surface for online work that benefits from:

- real page state
- signed-in sessions
- repeatable proof artifacts
- coordination with repo, terminal, and mobile browser lanes

Pair with domain skills when a task is specific:

- `$aetherbrowser-arxiv-nav`
- `$aetherbrowser-github-nav`
- `$aetherbrowser-notion-nav`
- `$aetherbrowser-huggingface-nav`
- `$aetherbrowser-shopify-nav`

If the task becomes multi-agent, multi-surface, or automation-heavy, pair with:

- `$polyhedral-workflow-mesh`

Use this skill when the task crosses domains or needs an operator that can choose the right browser surface first.

## Workflow

1. Route the task into the browser lane first.
- `python C:\Users\issda\SCBE-AETHERMOORE\scripts\system\browser_chain_dispatcher.py --domain <domain> --task <task> --engine playwriter`

2. Choose the right surface.
- Search/discovery: use built-in search or `web` search to find the right target quickly.
- Real page inspection: pivot into AetherBrowser or the lane runner immediately after discovery.
- GitHub repo operations: pair with `$scbe-gh-powershell-workflow` for `gh` and repo-state checks.
- GitHub browser surfaces: think in four surfaces, not one:
  - repo page
  - `github.dev`
  - Codespaces IDE
  - Codespaces terminal / forwarded preview

3. Capture proof before doing deep work.
- `python C:\Users\issda\SCBE-AETHERMOORE\scripts\system\playwriter_lane_runner.py --session 1 --task title --url "<url>"`
- `python C:\Users\issda\SCBE-AETHERMOORE\scripts\system\playwriter_lane_runner.py --session 1 --task snapshot --url "<url>"`

4. Execute the smallest useful browser action.
- For governed browser actions:
  - `python C:\Users\issda\SCBE-AETHERMOORE\agents\aetherbrowse_cli.py --backend cdp navigate "<url>"`
  - `python C:\Users\issda\SCBE-AETHERMOORE\agents\aetherbrowse_cli.py --backend cdp snapshot`
- Prefer minimal, reversible steps over long opaque scripts.

5. Verify state after every meaningful action.
- Capture snapshot/title/evidence again.
- Persist output under repo `artifacts/` when the task matters.

6. Fall back cleanly if the browser lane is blocked.
- Use built-in search, deterministic fetch, or `web` browsing for discovery and reading.
- Return to AetherBrowser when the task requires signed-in state, tabs, or visual confirmation.

## Operator Rules

- Prefer AetherBrowser over Chrome/Safari/manual browser fallback when the task can improve the SCBE browser stack.
- Use search utilities for discovery, not as a substitute for real browser state.
- Keep online actions bounded and explainable.
- Always leave proof:
  - title snapshot
  - page evidence JSON
  - screenshot when visual state matters
- When GitHub is involved, separate:
  - browser navigation
  - `gh` terminal operations
  - repo state
  - codespace/editor state

## Output Contract

Return:

- chosen surface
- route used
- proof artifact paths
- blockers
- next browser action

## Resources

Load these only when needed:

- `references/browser-surface-map.md`
  - Load when choosing between repo page, `github.dev`, Codespaces, AetherBrowser CLI, and lane runner surfaces.
- `references/browser-task-patterns.md`
  - Load when shaping a concrete online task into route -> inspect -> act -> verify -> handoff.
