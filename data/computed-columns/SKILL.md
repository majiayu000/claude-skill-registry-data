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

**CRITICAL CONCEPT**: Rollups should almost always operate on a **Relation column**, not an entire table. This is because rollups on relations automatically filter to only the related rows.

### Why Use Relations with Rollups

**The pattern:**
```
Relation Column → Rollup Column (operates on the relation)
```

**What happens:**
- **Rollup on a Relation**: Counts/sums/averages only the rows that are related
- **Rollup on a Table**: Counts/sums/averages ALL rows in that table (rarely useful)

### Example: Order System

**Tables:**
- Orders table
- Order Items table

**Goal:** Count how many items are in each order

**❌ WRONG approach:**
```
In Orders table:
  Rollup column → Select "Order Items" table → Count rows

Result: Every order shows the TOTAL count of all items in the entire table
```

**✅ RIGHT approach:**
```
In Orders table:
  Step 1: Relation column → Match Order ID to Order Items table
  Step 2: Rollup column → Select the Relation column → Count

Result: Each order shows only its own item count
```

### Example: CRM System

**Goal:** In Companies table, show count of contacts and sum of deal amounts

**✅ Correct setup:**
```
Companies table:
  1. Relation: "Related Contacts" → Links to Contacts where Company ID matches
  2. Rollup: "Contact Count" → Operates on "Related Contacts" relation → Count

  3. Relation: "Related Deals" → Links to Deals where Company ID matches
  4. Rollup: "Total Deal Amount" → Operates on "Related Deals" relation → Sum of Amount
```

### When to Use Rollup on Whole Table

Rarely needed, but valid when:
- You want a constant value (e.g., "Total Users" displayed on every row)
- You're creating a dashboard row that shows global stats

**Example:**
```
Dashboard table (single row):
  Rollup → Select Users table → Count rows
  Result: Shows total user count
```

### Setup Steps

1. **Create a Relation column first** (unless using whole table)
2. Create a Rollup column
3. Select the **Relation column** as the source (not the table directly)
4. Choose the aggregation: Count, Sum, Average, Min, Max
5. Select which column to aggregate (for Sum/Average/Min/Max)

### Common Rollup Patterns

| Pattern | Relation | Rollup Configuration |
|---------|----------|---------------------|
| Count tasks per project | Project → Tasks | Count rows in relation |
| Sum order amounts per customer | Customer → Orders | Sum of "Amount" column |
| Average rating per product | Product → Reviews | Average of "Rating" column |
| Max price in category | Category → Products | Max of "Price" column |
| Count activities per contact | Contact → Activities | Count rows in relation |

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

## Big Table Limitations

When using **Big Tables** (not native Glide Tables), computed columns have limitations for filtering, sorting, and rollups.

**Supported for filtering/sorting/rollups in Big Tables:**
- Math columns
- If-Then-Else columns
- Lookup columns (single relation, basic columns only)
- Template columns (static template string only)

**NOT supported for filtering/sorting/rollups in Big Tables:**
- Rollup columns
- Multi-relation columns
- Query columns
- Plugin-based columns

**Lookup requirements in Big Tables:**
- Single relation only (not multi-relation)
- Relation column must be basic (non-computed)
- Target table must be a Big Table
- Target column must be basic (non-computed)
- Target column cannot be user-specific

**Template requirements in Big Tables:**
- Template string must be constant (not computed)

**Rollup/Lookup row limit:** Maximum 100 matching rows in Big Tables.

See the `data-modeling` skill for full Big Table documentation.

## Tips

- **Name columns clearly** - they become variables in other calculations
- **Use the type filter** - faster than scrolling through menus
- **Chain simple columns** - easier to debug than one complex column
- **Test with sample data** - verify calculations work before adding more
- **Consider Big Table limits** - if using Big Tables, check column type compatibility
