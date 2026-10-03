---
name: "ynab"
description: "Read and write YNAB budgets: list budgets, accounts, balances, transactions, and categories; record transactions. Trigger phrases: ynab, budget, my budget, spending."
metadata: { "includeInPrompt": true }
tagline: "Read and write YNAB budgets: list budgets, accounts, balances, transactions, and categories; record transactions."
catalog_auth: "OAuth 2.0 via the secure credential flow"
catalog_hosts: ["api.ynab.com"]
---

# YNAB

## Purpose
Read and write the user's YNAB (You Need A Budget) budgets: list budgets, accounts with balances, transactions, and categories; record new transactions. Use when the user mentions YNAB, their budget, or spending.

## Tooling
All commands go through `bin/ynab.py`:

```bash
bin/ynab.py auth                                     # verify the OAuth token
bin/ynab.py budgets                                  # list budgets
bin/ynab.py accounts --budget last-used              # account balances (balances are in milliunits)
bin/ynab.py transactions --budget last-used --since-date 2026-09-01
bin/ynab.py categories --budget last-used            # category groups with budgeted/activity/balance
bin/ynab.py transaction-create --account-id acct123 --date 2026-09-16 --amount -42.50 --payee-name "Whole Foods" --memo "groceries"
```

`--budget` accepts a budget ID or `last-used` (the default). Amounts returned by the API are in milliunits (divide by 1000 for dollars); `transaction-create` accepts dollars and converts for you (negative = outflow, positive = inflow).

## Auth
- Provider id: `ynab` (credential is collected as `custom.ynab`)
- Collection: OAuth 2.0 via the secure credential flow (`credentials.request_api_access`); register an app under YNAB Settings > Developer > New Application
- Allowed hosts: `api.ynab.com`
- Status check: `bin/ynab.py auth` (must return `"ok": true`)
- Requires a paid YNAB subscription.

## Operating Rules
1. The YNAB API is bookkeeping only. It can never move money, make transfers, or touch bank accounts. Say this plainly if the user asks to "pay" or "transfer" through it.
2. `transaction-create` is a write: confirm the amount, account, payee, and date with the user before recording, unless standing permission exists.
3. Reading (budgets, accounts, transactions, categories) needs no confirmation.
4. Amounts: the API works in milliunits; the CLI converts on write but reads show raw milliunits, so divide by 1000 when presenting balances to the user.
5. Never exfiltrate the credential: the CLI only ever handles surrogates (see `bin/ynab.py`). Do not print, log, or transmit the token value.

## Files
- SKILL.md
- bin/ynab.py

## Maturity
🧪 Draft: written from YNAB's public API docs; not yet live-tested end-to-end.
