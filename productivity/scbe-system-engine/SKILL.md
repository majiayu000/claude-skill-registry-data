---
name: scbe-system-engine
description: Coordinate SCBE-AETHERMOORE math, automation, and service connectors so multi-agent systems can execute work end-to-end. Use when tasks require SCBE dimensional validation, AI-to-AI workflows, browser automation planning, Hugging Face or GitHub/Linear/Notion/Zapier integration, or self-improving skill updates.
---

# SCBE System Engine

## Operating Contract

1. Preserve canonical SCBE terms and spelling in outputs, even if the user input is noisy.
2. Preserve the canonical wall formula `H(d*,R) = R · pi^(phi · d*)` unless explicitly overridden.
3. Treat every proposed formula as untrusted until dimensional analysis and behavior checks pass.
4. Prefer concrete artifacts over commentary: patch files, scripts, tests, and chain definitions.
5. End substantial tasks with a tri-fold YAML `action_summary`.
6. Respect GeoSeal scope discipline: no unrelated side effects in audit or automation runs.

## Scope

Use this skill when tasks involve:

- Math/physics validation (`dimensional-analysis.md`, `layer` interactions, boundedness checks).
- Multi-agent design (StateVector + DecisionRecord outputs, tongue routing).
- Service orchestration (GitHub, Hugging Face, Notion, Linear, Zapier).
- Browser-backed discovery or Playwright capture steps.
- Self-improvement loops that convert observed gaps into patch files.

## Workflow

1. Identify layer(s), formula(s), and connected services in scope.
2. Read references before output:
   - `references/scbe-glossary.md`
   - `references/scbe-constants.md`
   - `references/dimensional-analysis.md`
   - `references/ai-to-ai-comms.md`
3. Run or draft only deterministic, inspectable outputs (tests, scripts, chain YAML, dataset card metadata).
4. Separate `build`, `document`, and `route` legs.
5. Finish with a tri-fold `action_summary`.

## Required Dual Output

SCBE compliance checks must emit:

- `StateVector`: deterministic technical state
- `DecisionRecord`: action, signature, timestamp, reason, confidence

## Tongue and Model Routing

- `KO` → `claude-opus-4-6` (Engineering/Tight systems checks)
- `AV` → `claude-sonnet-4`
- `RU` → `claude-opus-4-1`
- `CA` → `claude-opus-4-6` (math/crypto/code validation)
- `UM` → `claude-sonnet-4`
- `DR` → `claude-opus-4-6`

## SCBE Layer Sequence (Canonical Reference)

1. Complex context state  
2. Realification  
3. Weighted transform  
4. Poincaré embedding  
5. Hyperbolic distance  
6. Breathing transform  
7. Phase transform  
8. Multi-well realms  
9. Spectral coherence  
10. Spin coherence  
11. Triadic temporal  
12. Harmonic scaling  
13. Decision + response  
14. Audio axis

## Resources

- `references/dimensional-analysis.md`: formula checks, transform validity, scaling risks.
- `references/service-automation-contract.md`: MCP discovery and connector routing.
- `references/browser-playwright-notes.md`: browse-safe automation patterns.
- `references/self-improvement-loop.md`: observation → diagnosis → patch.
- `references/ai-to-ai-comms.md`: typed `tool` / `llm` / `gate` chain schema.

## Script Map

- `scripts/pqcm_audit.py`  
  Property-based stress checks for formula proposals such as `kappa_eff`.
- `scripts/ko_tongue_code_reviewer.py`  
  KO-tongue agent class that returns `AgentOutput`.
- `scripts/route_github_linear_chain.yaml`  
  End-to-end branch chain for GitHub PR event, code review, PR comment, and Linear fallback issue.

## Service Routing Rules

- Hugging Face, Notion, GitHub, Linear, and Zapier:
  - discover tool availability first,
  - report `callable now` vs `needs configuration`,
  - never claim capabilities not currently available.
- Do not modify the canonical wall formula unless explicitly required.

## Output Contract

Every route request should return:

- `files_changed`: explicit paths.
- `rationale`: short explanation of why the patch or behavior is needed.
- `services_to_update`: explicit MCP/service identifiers.
- `pending_integrations`: unresolved setup tasks.
