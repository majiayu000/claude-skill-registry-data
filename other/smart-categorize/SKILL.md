---
name: smart-categorize
description: >
  Auto-categorize uncategorized transactions using vendor pattern matching.
---

# Smart Categorize

## Overview
Automatically categorize uncategorized transactions by matching vendor/description patterns against known rules. Uses existing categorization rules first, then suggests new rules for unmatched transactions based on common vendor names.

## Wilson Tools Used
- `categorize` — apply pattern-based categorization rules to transactions
- `transaction_search` — find uncategorized transactions

## Workflow
1. Use `transaction_search` to find all transactions where `category` is null or empty.
2. Run `categorize` to apply existing categorization rules (pattern matching on description field).
3. Report how many transactions were categorized by existing rules.
4. For remaining uncategorized transactions, group by vendor/description similarity.
5. Suggest category assignments for each vendor group (e.g., "SPOTIFY" -> Entertainment, "SHELL OIL" -> Transportation).
6. Ask the user to confirm or adjust the suggested categories.
7. Apply confirmed categories and optionally save new categorization rules for future imports.

## Without Wilson
You can categorize transactions manually in a spreadsheet:

### Setting Up Category Rules in Excel/Sheets
1. Create a reference sheet called "Rules" with two columns: `Pattern` and `Category`.
2. Add your vendor patterns:
   | Pattern | Category |
   |---------|----------|
   | AMAZON | Shopping |
   | WHOLE FOODS | Groceries |
   | SHELL | Transportation |
   | NETFLIX | Entertainment |
   | STARBUCKS | Dining |

3. In your transactions sheet, use a lookup formula in the Category column:
   - **Excel**: `=IFERROR(INDEX(Rules!B:B,MATCH("*"&"AMAZON"&"*",Rules!A:A,0)),"Uncategorized")` — but this only works for exact matches.
   - **Better approach with Excel**: Use a helper column with `=SUMPRODUCT` or VBA macro to do partial matching.
   - **Google Sheets**: `=IFERROR(VLOOKUP("*"&A2&"*",Rules!A:B,2,FALSE),"Uncategorized")` does not support wildcards in VLOOKUP.
   - **Practical Google Sheets approach**:
     ```
     =IF(REGEXMATCH(A2,"(?i)amazon"),"Shopping",
      IF(REGEXMATCH(A2,"(?i)whole foods|trader joe"),"Groceries",
      IF(REGEXMATCH(A2,"(?i)shell|chevron|exxon"),"Transportation",
      "Uncategorized")))
     ```

### Common Category Mapping
| Vendor Pattern | Suggested Category |
|---|---|
| AMAZON, TARGET, WALMART | Shopping |
| WHOLE FOODS, TRADER JOE, KROGER, SAFEWAY | Groceries |
| UBER EATS, DOORDASH, GRUBHUB | Dining |
| NETFLIX, SPOTIFY, HULU, DISNEY+ | Entertainment |
| SHELL, CHEVRON, BP, EXXON | Transportation |
| AT&T, VERIZON, T-MOBILE, COMCAST | Utilities |
| CVS, WALGREENS, PHARMACY | Healthcare |
| VENMO, ZELLE, PAYPAL (person-to-person) | Transfers |

## Important Notes
- Pattern matching is case-insensitive and matches against any part of the transaction description.
- Rules are applied in the order they were created. If a transaction matches multiple rules, the first match wins.
- Categorization does not overwrite transactions that already have a category unless you explicitly ask.
- Wilson stores rules in the `categorization_rules` table so they persist across sessions and apply to future imports automatically.
