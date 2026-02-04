---
name: financial-summary
description: Parse and analyze personal financial transaction CSV exports to calculate account totals and generate detailed breakdowns. Use when the user asks to analyze transaction data, generate financial summaries, calculate account balances, or review spending from CSV exports. Supports account grouping (Galicia, Mercado Pago, Quiena, LLC/Relay, HSBC, Crypto), automatic internal transfer detection, and detailed transaction listings.
---

# Financial Summary

Process transaction CSV files and generate comprehensive financial summaries with account grouping and internal transfer detection.

## When to Use

Use this skill when the user:
- Asks to analyze or summarize financial transactions from a CSV file
- Wants to calculate totals for specific account groups
- Needs to review spending or income across multiple accounts
- Requests detailed transaction breakdowns by account group

## CSV Format Requirements

The CSV file must be semicolon-separated (`;`) with these columns:
- `account`: Account name
- `category`: Transaction category
- `currency`: ARS or USD
- `amount`: Transaction amount (negative for expenses)
- `type`: Income or Expenses
- `transfer`: true or false
- `date`: Transaction date

## Account Groups

The script organizes accounts into these groups:

| Group | Accounts |
|-------|----------|
| Galicia | Galicia Mas - Caja de ahorro |
| Mercado Pago | Mercado Pago |
| Quiena | Quiena |
| LLC | Relay Checking Account, Relay Saving Account |
| HSBC | HSBC Current Account, HSBC Saving Account |
| Crypto | Fiwind, Uglycash, Nexo |

## Usage

### Generate Financial Summary

To generate a complete financial summary:

```bash
python scripts/process_transactions.py <path-to-csv-file>
```

Example:
```bash
python scripts/process_transactions.py ~/Downloads/report_2025-11-30.csv
```

The script will output:
- Summary totals for each account group
- Transaction counts
- Warnings for unknown accounts not mapped to groups
- Values formatted without thousand separators using decimal points

### View Detailed Transactions

To see all transactions for a specific account group:

```bash
python scripts/process_transactions.py <path-to-csv-file> --details=<GROUP>
```

Available groups: `Galicia`, `Mercado Pago`, `Quiena`, `LLC`, `HSBC`, `Crypto`

Example:
```bash
python scripts/process_transactions.py ~/Downloads/report.csv --details=LLC
```

This shows:
- Date, account, currency, amount, type, and notes for each transaction
- Transfer markers `[T]` for transfer transactions
- Totals by currency (ARS and USD)

## Key Features

### Internal Transfer Detection

The script automatically identifies and excludes internal transfers between accounts in the same group (e.g., transfers between Relay Checking and Relay Saving). This prevents double-counting when calculating withdrawal totals.

Internal transfers are detected by matching:
- Same date
- Same currency
- Opposite amounts (within 0.01 tolerance)
- Both marked as transfers

### Account Group Calculations

**ARS Accounts:**
- Bank account (Galicia): Sum of all ARS transactions
- Mercado Pago FCI: Sum of all ARS transactions

**Quiena (USD):**
- Posición: Transfer income transactions
- Incremento de valor: Financial investment category, non-transfers
- Dividendos: Always 0
- Retiros: Always 0

**LLC/Relay (USD):**
- Ganancia: "Wage, invoices" category transactions
- Gastos: Expense transactions that are not transfers
- Retiros: Transfer expense transactions (excluding internal transfers)

**HSBC (USD):**
- Ingresos: Transfer income transactions (excluding internal transfers)
- Retiros: Transfer expense transactions (excluding internal transfers)
- Gastos: Expense transactions that are not transfers

**Crypto (USD):**
- Posición: Transfer income transactions
- Incremento de valor: Financial investment category, non-transfers
- Retiros: All expense transactions (transfers + non-transfers)

## Workflow

1. Ask the user for the path to their transaction CSV file
2. Run the script to generate the summary
3. Review the output and check for unknown accounts
4. If unknown accounts are found, ask the user how they should be categorized
5. If the user needs detailed transaction breakdowns, run the script again with `--details=<GROUP>`
6. Present the results clearly to the user

## Output Formatting

When presenting the financial summary to the user:
- Use the raw numeric format from the script output (without thousand separators)
- Use decimal points (.) for decimals, not commas
- Example: `246325.62` NOT `246,325.62`
- Keep the same format as the script provides - do not add formatting
