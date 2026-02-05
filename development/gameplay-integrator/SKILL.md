---
name: gameplay-integrator
description: Integrate new or updated gameplay modes into the existing game app end-to-end, including lobby registration, navigation wiring, state persistence, assets, gameplay rules, performance guardrails, and verification. Use when adding a mini-game/mode, refactoring gameplay logic, wiring assets, or ensuring state/controls remain stable across flows.
---

# Gameplay Integrator

## Overview
Integrate or refactor gameplay modes without breaking existing modes, while preserving state, assets, performance, and build stability.

## Workflow Decision Tree
- Architecture gate (must happen first): inspect `app/src/main/java/com/xenogenics/app/MainActivity.java` and determine whether UI is WebView/HTML, native Compose, or hybrid.
- If WebView-based, default to shipping screens as HTML/CSS/JS and wiring via WebView routes + JS bridge. Only add native UI when explicitly requested.
- If the request touches UI or navigation, locate existing lobby and routing patterns before adding new ones.
- If the project lacks the requested architecture (e.g., Compose, NavGraph, ViewModel), stop and ask how to proceed.
- If tests are missing, add minimal pure logic tests for gameplay rules.

## Workflow

### 1) Intake and Constraints
- Parse the request for: mode name, flow entry points, rules, assets, settings to preserve, and performance limits.
- Confirm constraints in `references/project-standards.md`.

### 2) Locate Integration Points
- Identify the lobby entry, mode registry, navigation wiring, and state persistence layer.
- Follow patterns in `references/integration-patterns.md`.

### 3) Gameplay and State
- Implement or refactor game logic: win/lose, turns, input, pause/resume, game-over flows.
- Persist and restore: selected character/piece set, difficulty/level, audio/vibration, accessibility settings.
- Never change persistence keys unless explicitly requested.

### 4) Assets and Resource Mapping
- Map visuals and audio to real assets; add them via the existing pipeline.
- Keep assets optimized and in correct directories; avoid mystery files.

### 5) Performance and Stability
- Avoid heavy work on the main thread.
- Limit recomposition triggers and mutable state in UI.
- Prevent unbounded coroutines, loops, or particle effects.
- Add low-end device guardrails when the project supports them.

### 6) Verification
- Run the project build/tests (prefer `./gradlew :app:assembleDebug`).
- If no tests exist, add minimal unit tests for game rules and key transitions.
- Fix failures and rerun until green.

### 7) Output
- Provide a concise change log with file paths and a checklist:
  - Integrated into lobby
  - Navigation wiring
  - State persistence
  - Assets
  - Performance guardrails
  - Verification

## Guardrails
- Do not delete existing modes or routes.
- Do not change `applicationId` or package names.
- Only modify files required for the request.
- No placeholders, TODOs, or dead controls.
- All visible UI actions must be wired to real logic.

## References
- `references/project-standards.md`
- `references/repo-scan.md`
- `references/integration-patterns.md`
- `references/asset-pipeline.md`
- `references/performance-policies.md`
- `references/test-requirements.md`

## Golden Path Pointers
- Entry point: `app/src/main/java/com/xenogenics/app/MainActivity.java`
- Web UI: `app/src/main/assets/www/index.html`, `app/src/main/assets/www/script.js`, `app/src/main/assets/www/style.css`
