---
name: firefly-iii
description: Manage personal finances via Firefly III API. Use when user asks about budgets, transactions, accounts, categories, piggy banks, subscriptions, recurring transactions, or financial reports. Supports creating, listing, updating transactions; managing accounts and balances; setting budgets; tracking savings goals.
---

# Firefly III

Firefly III is a self-hosted personal finance manager. This skill provides API access for managing finances.

## Configuration

Required environment:
- `FIREFLY_URL`: Base URL (e.g., `https://budget.example.com`)
- `FIREFLY_TOKEN`: Personal Access Token (stored at `~/.firefly_token`)

Get token: Profile → OAuth → Personal Access Tokens → Create new token

## API Basics

```bash
TOKEN=$(cat ~/.firefly_token)
BASE="$FIREFLY_URL/api/v1"
curl -s "$BASE/endpoint" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json"
```

## Core Endpoints

### Accounts
```bash
# List accounts
curl "$BASE/accounts?type=asset" # asset|expense|revenue|liability
# Create account
curl -X POST "$BASE/accounts" -d '{
  "name": "Bank Account",
  "type": "asset",
  "account_role": "defaultAsset",
  "currency_code": "EUR"
}'
```

Account types: `asset`, `expense`, `revenue`, `liability`
Asset roles: `defaultAsset`, `savingAsset`, `sharedAsset`, `ccAsset`

### Transactions
```bash
# List transactions
curl "$BASE/transactions?type=withdrawal&start=2026-01-01&end=2026-01-31"
# Create withdrawal (expense)
curl -X POST "$BASE/transactions" -d '{
  "transactions": [{
    "type": "withdrawal",
    "date": "2026-01-15",
    "amount": "50.00",
    "description": "Groceries",
    "source_name": "Bank Account",
    "destination_name": "Supermarket",
    "category_name": "Groceries"
  }]
}'
# Create deposit (income)
curl -X POST "$BASE/transactions" -d '{
  "transactions": [{
    "type": "deposit",
    "date": "2026-01-01",
    "amount": "3000.00",
    "description": "Salary",
    "source_name": "Employer",
    "destination_name": "Bank Account",
    "category_name": "Salary"
  }]
}'
# Create transfer
curl -X POST "$BASE/transactions" -d '{
  "transactions": [{
    "type": "transfer",
    "date": "2026-01-05",
    "amount": "500.00",
    "description": "Savings",
    "source_name": "Bank Account",
    "destination_name": "Savings Account"
  }]
}'
```

Transaction types: `withdrawal`, `deposit`, `transfer`

### Categories
```bash
# List categories
curl "$BASE/categories"
# Create category
curl -X POST "$BASE/categories" -d '{"name": "Groceries"}'
```

### Budgets
```bash
# List budgets
curl "$BASE/budgets"
# Create budget
curl -X POST "$BASE/budgets" -d '{"name": "Food", "active": true}'
# Set budget limit for period
curl -X POST "$BASE/budgets/{id}/limits" -d '{
  "start": "2026-01-01",
  "end": "2026-01-31",
  "amount": "500.00"
}'
```

### Piggy Banks (Savings Goals)
```bash
# List piggy banks
curl "$BASE/piggy-banks"
# Create piggy bank
curl -X POST "$BASE/piggy-banks" -d '{
  "name": "Vacation Fund",
  "target_amount": "2000.00",
  "accounts": [{"account_id": "1"}],
  "start_date": "2026-01-01",
  "target_date": "2026-12-31",
  "transaction_currency_code": "EUR"
}'
# Add money to piggy bank
curl -X POST "$BASE/piggy-banks/{id}/events" -d '{"amount": "100.00"}'
```

### Subscriptions (Bills)
```bash
# List subscriptions
curl "$BASE/subscriptions"
# Create subscription
curl -X POST "$BASE/subscriptions" -d '{
  "name": "Netflix",
  "amount_min": "12.99",
  "amount_max": "12.99",
  "date": "2026-01-15",
  "repeat_freq": "monthly",
  "currency_code": "EUR"
}'
```

Repeat frequencies: `weekly`, `monthly`, `quarterly`, `half-year`, `yearly`

### Recurring Transactions
```bash
# List recurring transactions
curl "$BASE/recurrences"
# Create recurring transaction
curl -X POST "$BASE/recurrences" -d '{
  "type": "withdrawal",
  "title": "Rent",
  "first_date": "2026-01-01",
  "repeat_until": "2026-12-31",
  "repetitions": [{
    "type": "monthly",
    "moment": "1"
  }],
  "transactions": [{
    "amount": "1000.00",
    "description": "Monthly rent",
    "source_id": "1",
    "destination_name": "Landlord",
    "category_name": "Rent"
  }]
}'
```

### Rules (Auto-categorization)
```bash
# List rules
curl "$BASE/rules"
# Create rule
curl -X POST "$BASE/rules" -d '{
  "title": "Categorize groceries",
  "trigger": "store-journal",
  "active": true,
  "strict": false,
  "triggers": [
    {"type": "description_contains", "value": "ALDI"}
  ],
  "actions": [
    {"type": "set_category", "value": "Groceries"}
  ]
}'
```

Trigger types: `description_contains`, `description_starts`, `description_ends`, `amount_less`, `amount_more`, `source_account_is`, etc.
Action types: `set_category`, `set_budget`, `add_tag`, `set_description`, etc.

### Tags
```bash
# List tags
curl "$BASE/tags"
# Create tag
curl -X POST "$BASE/tags" -d '{"tag": "vacation"}'
```

### Reports & Summary
```bash
# Account balance over time
curl "$BASE/accounts/{id}/transactions?start=2026-01-01&end=2026-01-31"
# Get current balances
curl "$BASE/accounts" | jq '.data[] | {name: .attributes.name, balance: .attributes.current_balance}'
```

## Common Tasks

### Get spending by category
```bash
curl "$BASE/categories" | jq '.data[] | {name: .attributes.name, spent: .attributes.spent}'
```

### Get budget progress
```bash
curl "$BASE/budgets" | jq '.data[] | {name: .attributes.name, spent: .attributes.spent}'
```

### Search transactions
```bash
curl "$BASE/search/transactions?query=groceries&limit=25"
```

## Error Handling

- `422 Unprocessable Entity`: Check required fields in error response
- `401 Unauthorized`: Token expired or invalid
- `404 Not Found`: Resource doesn't exist

## Tips

- Use `source_name`/`destination_name` to auto-create expense/revenue accounts
- Categories are different from budgets (categories for classification, budgets for limits)
- Piggy banks require linking to an asset account
- Use rules to auto-categorize transactions on creation
