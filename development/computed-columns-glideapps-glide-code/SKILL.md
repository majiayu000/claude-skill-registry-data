---
name: computed-columns
description: |
  Create computed columns in Glide - Math, If-Then-Else, Relations, Rollups, Lookups, Templates.
  Use when adding calculations, formulas, lookups, or linking tables with relations.
---

# Glide Computed Columns

Glide uses **computed columns** instead of cell formulas. Each computed column applies its logic to every row in the table.

## Key Concept

Calculations in Glide are columns, not cell formulas. You build complex logic by chaining columns together - one column's output becomes another column's input.

## Creating Computed Columns

1. In Data Editor, click a column header → "Add column right"
2. Name the column
3. Click the Type dropdown
4. **Use the filter** - type the column type (e.g., "math", "relation", "if-then") to find it quickly
5. Configure the column settings
6. Save

## Math Columns

For arithmetic calculations.

**Important**: Use plain, human-readable column names as variables. No special escaping or symbols needed.

Example - calculating a total:
- Column A: "Quantity"
- Column B: "Unit Price"
- Math column formula: `Quantity * Unit Price`

Just type the column names naturally. Glide will recognize them.

Other examples:
- `Price * 1.1` (add 10% markup)
- `Total / Count` (calculate average)
- `End Date - Start Date` (days between dates)
- `Amount - Discount` (apply discount)

**Configure formatting**: After creating a math column, set up proper display formatting:
- **Decimal places**: 0 for counts, 2 for currency
- **Prefix**: $ or € for money
- **Suffix**: %, kg, mi, hrs for units
- **Thousands separator**: Enable for large numbers

This makes the data instantly readable (e.g., "$1,234.56" instead of "1234.56").

## If-Then-Else Columns

For conditional logic. Returns different values based on conditions.

Structure:
- IF [condition]
- THEN [value if true]
- ELSE [value if false]

Examples:
- Status emoji: IF `Status` is "Complete" THEN "✅" ELSE IF `Status` is "In Progress" THEN "🔄" ELSE "⏳"
- Priority color: IF `Priority` is "High" THEN "🔴" ELSE IF `Priority` is "Medium" THEN "🟡" ELSE "🟢"
- Overdue flag: IF `Days Until Due` < 0 THEN "Overdue" ELSE "On Track"
- Discount tier: IF `Total` > 1000 THEN "Gold" ELSE IF `Total` > 500 THEN "Silver" ELSE "Bronze"

You can chain multiple If-Then-Else for complex logic, or nest them.

## Relation Columns

Connect rows between tables based on matching values.

Setup:
1. Create a Relation column
2. Select the target table
3. Choose which columns to match (e.g., "Customer ID" in Orders matches "ID" in Customers)

Types:
- **Single relation**: Returns one matching row
- **Multiple relation**: Returns all matching rows (for one-to-many)

Use relations to enable Lookups and Rollups.

## Lookup Columns

Pull a value from a related row.

Setup:
1. Create a Lookup column
2. Select a Relation column as the source
3. Choose which column to pull from the related table

Example:
- Orders table has Relation to Customers
- Lookup column pulls "Customer Name" from the related Customer row
- Now each order shows the customer's name

## Rollup Columns

Aggregate values across related rows.

Setup:
1. Create a Rollup column
2. Select a Relation column (usually a multiple relation)
3. Choose the aggregation: Count, Sum, Average, Min, Max
4. Select which column to aggregate (for Sum/Average/Min/Max)

Examples:
- Count of tasks per project
- Sum of order amounts per customer
- Average rating per product
- Max price in a category

## Template Columns

Combine text and column values into formatted strings.

Example:
- Template: `Hello, {Name}! Your order total is ${Total}.`
- Columns can be inserted with the column picker

Great for:
- Formatted display text
- Email/message templates
- Generating URLs with dynamic values

## Experimental Columns

### Hero Icons
Generate icons from the Hero Icons library.
- Input: Icon name (e.g., "check-circle", "user", "folder")
- Output: Image URL for the icon
- Combine with If-Then-Else for dynamic icons based on status

### Generate Text (AI)
Use AI to generate text based on other columns.
- Configure a prompt that references column values
- AI generates text for each row

### Other AI Columns
- **Image to Text**: Extract text/info from images
- **Text to Choice**: AI categorization
- **Text to Boolean**: AI yes/no classification

## Column Chaining Pattern

Build complex calculations by chaining simple columns:

```
Example: Order Status with Emoji

1. Relation: "Customer" → links to Customers table
2. Lookup: "Customer Name" → pulls name via Customer relation
3. Math: "Days Until Due" → Due Date - Today
4. If-Then-Else: "Is Overdue" → IF Days Until Due < 0 THEN true ELSE false
5. If-Then-Else: "Status Emoji" → IF Is Overdue THEN "🚨" ELSE IF Status = "Complete" THEN "✅" ELSE "📋"
```

Each column does one thing, and they build on each other.

## Tips

- **Name columns clearly** - they become variables in other calculations
- **Use the type filter** - faster than scrolling through menus
- **Chain simple columns** - easier to debug than one complex column
- **Test with sample data** - verify calculations work before adding more
