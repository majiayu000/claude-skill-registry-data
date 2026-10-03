---
name: chappie-testing
description: CHAPPiE testing strategy. Use when writing or running standalone tests, changing CI, or validating code, reports and compatibility contracts.
---

# CHAPPiE Testing

## Test model

Tests are standalone scripts run with `python3 tests/test_name.py`. Do not migrate the project to pytest. Offline tests fake providers and use temporary directories; live model tests are explicit and separate.

Install deterministic dependencies with:

```bash
pip install -r requirements/ci.txt
```

## Required architecture checks

```bash
python3 tests/test_runtime_architecture.py
python3 tests/test_api_contract.py
python3 tests/test_local_first_runtime.py
python3 tests/test_chat_ui_formatting.py
python3 tests/test_reasoning_layering.py
python3 tests/test_training_config_ui.py
python3 tests/test_training_daemon_lifecycle.py
```

## Compile, lint and types

```bash
python3 -m compileall -q api brain config life memory web_infrastructure Chappies_Trainingspartner tests
ruff check --config config/ruff.toml --no-cache web_infrastructure api/routers/chat.py brain/steering_manager.py brain/brain_pipeline.py
mypy --config-file config/mypy.ini web_infrastructure/contracts.py web_infrastructure/turn_context.py web_infrastructure/backend_wrapper.py api/schemas
```

The required Mypy scope starts at public runtime and API contracts. Legacy and frozen research evidence are excluded. Do not hide deterministic failures with `continue-on-error` or `|| true`.

## Reports and skill sync

```bash
python3 forschung/report/validate_report_v5_freeze.py
python3 forschung/report/validate_report_v6.py
python3 scripts/validate_skill_sync.py
```

## Frontend

Use `npm ci --legacy-peer-deps` and `npm run build`. Visible UI changes additionally require the project-approved Playwright MCP flow.

Full groups and live-test boundaries are documented in `docs/testing.md` and `tests/README.md`.
