---
name: contract-elicitor
description: Use FIRST when user requests any disease market sizing report (e.g. "做 X 市场调研" / "Run market sizing for X"). Elicits 4-6 startup questions (evidence window, geography, international comparison, report depth, user role) and writes .cache/<slug>/contract.json. ALWAYS invoke before disease-market-sizing-orchestration. Validates against schemas/contract.schema.json.
license: Cite-or-Block strict (P0 iron law, see ../../CLAUDE.md)
---

# Contract Elicitor (Phase 1)

Parses the user's one-liner to extract disease + locale, then asks 4-6 follow-up questions to fill the contract.

## Functions

- `parse_disease_and_locale(s) -> (disease, locale)` — strips action verbs, detects CJK
- `elicit_contract(one_liner, project_root, ask_user) -> contract.json path`

## Output

`.cache/<slug>/contract.json` — schema: `schemas/contract.schema.json`

## Hard precondition (used by phases 2-5)

```python
from elicitor import assert_contract_complete  # see Task 7
assert_contract_complete(contract_path)
```
