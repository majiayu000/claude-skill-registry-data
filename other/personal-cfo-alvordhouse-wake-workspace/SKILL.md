---
name: personal-cfo
description: AI-powered personal finance management system - track expenses, manage budgets, analyze spending patterns, and get smart financial recommendations
tags: [finance, personal-finance, budget, expense-tracker, budget-management, financial-analytics, money-management, ai-finance]
---

# Personal CFO

Your AI-powered Chief Financial Officer for personal finance management.

## Installation

### Step 1: Install the Skill

```bash
clawhub install personal-cfo
```

### Step 2: Install the CLI Tool

**Via npm (Recommended)**

```bash
npm install -g openclaw-personal-cfo
```

**Via GitHub**

```bash
git clone https://github.com/ZhenRobotics/openclaw-personal-cfo.git
cd openclaw-personal-cfo
npm install
npm run build
```

### Step 3: Verify Installation

```bash
cfo help
```

---

## When to Use This Skill

**AUTO-TRIGGER** when user's message contains:

- Keywords: `budget`, `expense`, `income`, `finance`, `spending`, `money`, `financial`, `预算`, `支出`, `收入`, `财务`
- Asks about tracking expenses or managing money
- Wants to analyze spending patterns
- Needs financial recommendations
- Requests budget reports or summaries

**TRIGGER EXAMPLES**:
- "Track my expenses"
- "I spent $50 on food today"
- "What's my monthly budget status?"
- "Show me my spending analysis"
- "帮我记录今天的支出"
- "我的预算还剩多少？"

**DO NOT USE** when:
- Only general financial advice (use general knowledge)
- Stock/crypto trading (use specialized tools)
- Tax calculation (use tax tools)

---

## Core Features

Complete personal finance management solution:

- 💰 **Transaction Tracking** - Record income and expenses with 15+ categories
- 📊 **Budget Management** - Set and monitor budgets by category and period
- 📈 **Financial Analytics** - Analyze spending patterns and trends
- 💡 **Smart Recommendations** - AI-powered financial suggestions
- 📄 **Reports Generation** - Monthly and yearly financial reports
- 🔒 **Privacy-First** - Local JSON storage, no cloud required

---

## Agent Usage Guide

### Important Notes

Personal CFO uses local JSON storage at `~/openclaw-personal-cfo/data/` by default.

All commands are available through three CLI aliases:
- `openclaw-personal-cfo` (full name)
- `personal-cfo` (simplified)
- `cfo` (short alias)

### Primary Commands

#### Add Transaction

**Add Income**:
```bash
cfo add income <amount> <category> [description]
```

**Add Expense**:
```bash
cfo add expense <amount> <category> [description]
```

**Example**:
```bash
cfo add income 5000 salary "Monthly salary"
cfo add expense 50 food "Lunch at restaurant"
```

#### List Transactions

```bash
cfo list [limit]
```

Default shows last 10 transactions.

#### Set Budget

```bash
cfo budget set <category> <amount> <period>
```

**Example**:
```bash
cfo budget set food 500 monthly
cfo budget set entertainment 200 monthly
```

#### Check Budget Status

```bash
cfo budget status
```

Shows all budgets with current spending and status (safe/warning/exceeded).

#### Generate Reports

**Monthly Report**:
```bash
cfo report monthly [year] [month]
```

**Yearly Report**:
```bash
cfo report yearly [year]
```

**Financial Analysis**:
```bash
cfo analyze
```

Provides comprehensive analysis with recommendations.

---

## Categories

### Income Categories
- `salary` - Regular employment income
- `freelance` - Freelance/contract work
- `investment` - Investment returns
- `gift` - Gifts and red envelopes
- `other-income` - Other income sources

### Expense Categories
- `food` - Food and dining
- `housing` - Rent, mortgage, utilities
- `transportation` - Transit, fuel, car maintenance
- `entertainment` - Movies, games, hobbies
- `healthcare` - Medical expenses
- `utilities` - Electricity, water, internet
- `shopping` - Clothing, electronics
- `education` - Books, courses, tuition
- `travel` - Trips and vacations
- `other-expense` - Other expenses

---

## Budget Periods

- `daily` - Daily budget
- `weekly` - Weekly budget
- `monthly` - Monthly budget (most common)
- `yearly` - Annual budget

---

## Usage Examples

### Example 1: Daily Expense Tracking

User: "I spent $50 on lunch and $30 on coffee today"

Agent executes:
```bash
cfo add expense 50 food "Lunch"
cfo add expense 30 food "Coffee"
```

### Example 2: Monthly Budget Setup

User: "Set monthly budget: $500 food, $200 entertainment, $1000 housing"

Agent executes:
```bash
cfo budget set food 500 monthly
cfo budget set entertainment 200 monthly
cfo budget set housing 1000 monthly
```

### Example 3: Financial Analysis

User: "How am I doing financially this month?"

Agent executes:
```bash
cfo analyze
```

Shows spending breakdown, budget status, and recommendations.

### Example 4: Generate Report

User: "Show me my financial report for January 2026"

Agent executes:
```bash
cfo report monthly 2026 1
```

---

## Data Storage

### Default Location
- Transactions: `~/openclaw-personal-cfo/data/transactions.json`
- Budgets: `~/openclaw-personal-cfo/data/budgets.json`
- Config: `~/openclaw-personal-cfo/data/config.json`

### Custom Data Directory

Set custom location via environment variable:
```bash
export CFO_DATA_DIR="/path/to/custom/data"
```

---

## Technical Specifications

- **Platform**: Node.js >= 18.0.0
- **Language**: TypeScript
- **Storage**: JSON files (local)
- **Currency**: USD (default), configurable
- **Date Format**: ISO 8601

---

## Programmatic Usage

Personal CFO can also be used as a library:

```typescript
import { PersonalCFO } from 'openclaw-personal-cfo';

const cfo = new PersonalCFO();

// Add transaction
await cfo.transactions.createTransaction(
  'expense',
  'food',
  50,
  'Lunch',
  new Date()
);

// Set budget
await cfo.budgets.createBudget('food', 500, 'monthly');

// Generate report
const report = await cfo.reports.generateMonthlyReport(2026, 1);
console.log(report);
```

---

## Troubleshooting

### Issue 1: Command Not Found

**Error**: `command not found: cfo`

**Solution**:
```bash
npm install -g openclaw-personal-cfo
```

### Issue 2: Data Directory Permission

**Error**: `EACCES: permission denied`

**Solution**:
```bash
mkdir -p ~/openclaw-personal-cfo/data
chmod 755 ~/openclaw-personal-cfo/data
```

### Issue 3: Invalid Category

**Error**: `Invalid category`

**Solution**: Check available categories with:
```bash
cfo help
```

---

## Agent Behavior Guidelines

When using this skill, agents should:

**DO**:
- ✅ Parse user input for amounts, categories, and descriptions
- ✅ Confirm transactions before adding them
- ✅ Provide clear summaries after operations
- ✅ Suggest budget setup for new users
- ✅ Offer insights from analysis

**DON'T**:
- ❌ Make financial decisions without user confirmation
- ❌ Modify existing transactions without permission
- ❌ Share financial data externally
- ❌ Assume currency (always confirm if unclear)

---

## Privacy & Security

- 🔒 All data stored locally
- 🔒 No cloud sync or external API calls
- 🔒 No tracking or analytics
- 🔒 User controls all data
- 🔒 Open source, auditable code

---

## Full Documentation

- **GitHub**: https://github.com/ZhenRobotics/openclaw-personal-cfo
- **NPM**: https://www.npmjs.com/package/openclaw-personal-cfo
- **Quick Start**: See README.md in repository
- **API Docs**: See docs/ directory in repository

---

## Version History

### v1.0.0 (2026-03-08)

Initial release with core features:
- Transaction tracking (income/expense)
- Budget management
- Financial analytics engine
- Report generation
- CLI interface
- OpenClaw agent integration

---

**Project Status**: ✅ Production Ready

**License**: MIT

**Author**: @ZhenStaff

**Support**: https://github.com/ZhenRobotics/openclaw-personal-cfo/issues

**ClawHub**: https://clawhub.ai/ZhenStaff/personal-cfo
