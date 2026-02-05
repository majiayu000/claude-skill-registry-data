---
name: conestoga-game-dev
description: Use for Conestoga game development, validation/fallback handling, UI headless toggle, and test workflow in this repo. Covers make/uv commands, Gemini fallback patterns, and Pygame headless settings.
---

# Conestoga Game Dev Skill

## Quick Context
- Code: `src/conestoga/game/` (`runner.py`, `gemini_gateway.py`, `events.py`, `state.py`, `ui.py`, `validators.py`, `fallback_monitor.py`).
- Entry: `conestoga` script or `uv run python -m conestoga.main`.
- Tests: `uv run pytest` (CI defaults headless), headless toggle via `UI_HEADLESS=1` or `CI=1`; set `UI_HEADLESS=0` for visible window.
- Make targets: `make install-dev`, `make lint`, `make format`, `make test`, `make run`.

## Gemini & Fallback Rules
- Only Gemini 3 models via `GeminiGateway`; offline/quota sets `resource_exhausted`.
- Validator enforces 2–3 choices, unique IDs/text, and effect targets (allowed resources, catalog items).
- FallbackMonitor tracks fallback source/reason; UI logs fallback/timeout; `gemini_online` flag controls offline badge.
- Modify resources only via `GameState.modify_resource` (raises on unknown fields).

## Testing
- Run `uv run pytest`; optional SHACL test skips if pyshacl missing.
- Scripts: `scripts/test-pre.sh` / `scripts/test-post.sh` (Docker opt-in via `RUN_DOCKER=1`, compose file `docker-compose.test.yml`, temp dir `TEST_RUN_DIR`).
- Headless UI tests set `UI_HEADLESS=1`; use `UI_HEADLESS=0` locally to view windows.

## Key Files
- Validation/fallback: `src/conestoga/game/validators.py`, `fallback_monitor.py`, `gemini_gateway.py`, `runner.py`.
- UI: `src/conestoga/game/ui.py` (headless toggle, logging).
- Tests: `tests/test_game.py`, `tests/test_ui_headless.py`, `tests/test_audit.py`, `tests/test_ontology.py`.
- Docs: `README.md` headless note; ontology `ontology/conestoga.ttl`.

## Patterns to Preserve
- Prefetch-first events, on-demand resolutions.
- Validate before mutation; fallback on validation/timeout/quota.
- UI logs choices, outcomes, fallback usage.
