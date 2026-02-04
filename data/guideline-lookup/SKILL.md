---
name: guideline-lookup
description: Look up Fannie Mae underwriting guidelines for income, assets, credit, or collateral verification. Use when questions involve DTI, income documentation, asset requirements, credit standards, or any B3/B4 guideline references. Reads guidelines dynamically from configs/guidelines/ - never hardcodes content.
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
---

# Fannie Mae Guideline Lookup

## Purpose
Query Fannie Mae Selling Guide sections for underwriting requirements without hardcoding guideline content.

## Instructions

### Step 1: Check if guidelines exist
```bash
ls configs/guidelines/
```

If the directory is empty or missing, instruct the developer:
```bash
make fetch-guidelines
```

### Step 2: Identify the relevant section
Guidelines are organized by domain:

| Section | Directory | Guideline IDs |
|---------|-----------|---------------|
| Income | `configs/guidelines/income/` | B3-3.1-01 through B3-3.2-02 |
| Assets | `configs/guidelines/assets/` | B3-4.1-01 through B3-4.3-03 |
| Credit | `configs/guidelines/credit/` | B3-5.1-01 through B3-5.4-03 |
| Collateral | `configs/guidelines/collateral/` | B4-1.1-01 through B4-1.3-02 |

### Step 3: Read the relevant guideline file
```bash
# List available guidelines in a section
ls configs/guidelines/income/

# Read a specific guideline
cat configs/guidelines/income/b3-3.1-01.md
```

### Step 4: Quote directly from the file
- Always quote the exact text from the markdown file
- Include the guideline ID (e.g., B3-3.1-01) in your response
- Note the effective date if present

## Common Topics by Guideline

### Income (B3-3.1 through B3-3.2)
- B3-3.1-01: General income information
- B3-3.1-02: Employment documentation standards
- B3-3.1-03: Base pay, salary, hourly, bonus, overtime
- B3-3.1-04: Commission income
- B3-3.1-05: Secondary/seasonal employment
- B3-3.1-06: IRS Form 4506-C requirements
- B3-3.1-07: Verbal verification of employment
- B3-3.1-08: Rental income
- B3-3.1-09: Other income sources
- B3-3.2-01: Self-employed borrower underwriting
- B3-3.2-02: Business structures

### Assets (B3-4.1 through B3-4.3)
- Asset documentation requirements
- Gift fund guidelines
- Reserves requirements

### Credit (B3-5.1 through B3-5.4)
- Credit score requirements
- Credit history evaluation
- Debt-to-income calculations

### Collateral (B4-1.1 through B4-1.3)
- Appraisal requirements
- Property eligibility
- Title requirements

## Important
- NEVER hardcode guideline content in responses
- ALWAYS read from `configs/guidelines/` files
- Guidelines may be updated - always read the current file
- Reference `internal/guidelines/fetcher.go:SectionConfig` for URL mappings
