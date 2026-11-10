---
name: api-contract
description: Change an HTTP route that a live client depends on without breaking it, and update the contract snapshots when a change is intended. Use when editing any route in points, storefront, calendar, auth, public, users or organizations.
---

thesoda.io (asusoda/website) and the `dashboard/` app call the API directly. `docs/api-contract.md` lists every route a client depends on, and `tests/contract/test_contract.py` checks each one's status code and JSON shape against `tests/contract/snapshots.json`.

1. Before changing a route, find it in `docs/api-contract.md` and in `CASES` in `test_contract.py`.
2. Keep the path, method, status codes and response keys. Add fields rather than renaming or removing them.
3. Run `uv run pytest tests/contract -q`. A failing contract case means a client breaks.
4. When a break is intended and the client is updated in the same release, regenerate with `UPDATE_CONTRACT=1 uv run pytest tests/contract/test_contract.py`, and name the client and its change in the PR.
5. Access checks start in report mode: a new refusal is logged as `access decision=would_deny` until `ACCESS_ENFORCE=true`. Do not turn a report-mode check into a hard refusal in the same change.

Routes added for new modules are not in the contract until a client depends on them.
