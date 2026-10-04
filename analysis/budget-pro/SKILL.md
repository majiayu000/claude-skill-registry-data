---
name: budget-pro
description: Personal budget management with privacy-first local storage. Use when user mentions setting a budget, tracking spending, logging expenses, checking budget status, or managing money by category. Tracks income, expenses, and category budgets with proactive alerts. NEVER accesses bank accounts or external financial services.
---

# Budget

Personal budgeting system with proactive tracking. Private. Simple. Effective.

## Critical Privacy & Safety

### Data Storage (CRITICAL)
- **All budget data stored locally only**: `memory/budget/`
- **No external APIs** for financial data
- **No bank account connections** - manual entry only
- **No data transmission** to financial apps or services
- User controls all data retention and deletion

### Safety Boundaries (NON-NEGOTIABLE)
- ✅ Track expenses by category with manual entry
- ✅ Alert on budget thresholds (70%, 90%, 100%)
- ✅ Generate reports and spending insights
- ✅ Suggest reallocation between categories
- ❌ **NEVER connect to bank accounts** or credit cards
- ❌ **NEVER access external financial services**
- ❌ **NEVER make financial recommendations** beyond budget reallocation
- ❌ **NEVER store sensitive financial credentials**

## Quick Start

### Data Storage Setup
Budget data stored in your local workspace:
- `memory/budget/budget.json` - Monthly budget limits by category
- `memory/budget/expenses.json` - All logged expenses
- `memory/budget/income.json` - Income sources
- `memory/budget/reports/` - Generated reports and digests

Use provided scripts in `scripts/` for all data operations.

## Core Workflows

### Set Budget
```
User: "My food budget is $500 per month"
→ Use scripts/set_budget.py --category food --limit 500 --period monthly
→ Store budget limit
```

### Log Expense
```
User: "I spent $45 on groceries"
→ Use scripts/log_expense.py --amount 45 --category food --description "groceries"
→ Check against budget, alert if thresholds crossed
```

### Check Budget Status
```
User: "How is my budget this month?"
→ Use scripts/budget_status.py --period month
→ Show all categories with spent/remaining/status
```

### Category Query
```
User: "What can I still spend on dining?"
→ Use scripts/category_status.py --category dining
→ Show remaining budget for specific category
```

### Handle Overage
```
User: "I went over on entertainment"
→ Use scripts/overage_analysis.py --category entertainment
→ Show overage amount and suggest recovery options
```

### Generate Report
```
User: "Show me my spending report"
→ Use scripts/generate_report.py --type weekly
→ Generate detailed spending analysis
```

## Module Reference

For detailed implementation of each module:
- **Budget Setup**: See [references/budget-setup.md](references/budget-setup.md)
- **Expense Tracking**: See [references/expense-tracking.md](references/expense-tracking.md)
- **Alerts & Thresholds**: See [references/alerts.md](references/alerts.md)
- **Reports & Analysis**: See [references/reports.md](references/reports.md)
- **Overage Recovery**: See [references/overage-recovery.md](references/overage-recovery.md)

## Scripts Reference

All data operations use scripts in `scripts/`:

| Script | Purpose |
|--------|---------|
| `set_budget.py` | Set or update budget for category |
| `log_expense.py` | Log an expense |
| `delete_expense.py` | Remove/correct an expense |
| `budget_status.py` | Show overall budget health |
| `category_status.py` | Show specific category status |
| `list_expenses.py` | View expense history |
| `overage_analysis.py` | Analyze and suggest recovery for overages |
| `reallocate_budget.py` | Move budget between categories |
| `generate_report.py` | Generate spending reports |
| `export_data.py` | Export budget data (CSV/JSON) |

## Default Categories

| Category | Typical Budget | Common Expenses |
|----------|---------------|-----------------|
| Housing | 25-35% income | Rent, mortgage, insurance |
| Food | 10-15% income | Groceries, dining out |
| Transport | 10-15% income | Gas, transit, maintenance |
| Utilities | 5-10% income | Electric, gas, internet, phone |
| Entertainment | 5-10% income | Movies, hobbies, subscriptions |
| Health | 5-10% income | Insurance, medical, gym |
| Shopping | 5-10% income | Clothing, household items |
| Savings | 10-20% income | Emergency fund, investments |

Custom categories can be added as needed.

## Disclaimer

This skill provides budget tracking and organization only. It does not provide financial advice, investment recommendations, or tax guidance. For financial planning, consult a qualified financial advisor.
