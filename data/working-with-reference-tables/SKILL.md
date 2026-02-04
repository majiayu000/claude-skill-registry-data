---
name: working-with-reference-tables
description: Work with Reference Tables (static CSV lookup data) using OPAL to enrich datasets with descriptive information. Use when you need to map IDs to human-readable names, add static metadata from CSV uploads, or perform lookups without temporal considerations. Covers both explicit and implicit lookup patterns, column name matching, and when to choose Reference Tables vs Resources vs Correlation Tags.
---

# Working with Reference Tables

Work with Reference Tables (static lookup data) using OPAL to enrich datasets with descriptive information. Reference Tables store static mappings (max 10MB CSV) that don't track changes over time, providing an alternative to Resources when no temporal aspect is needed.

Use when you need to:
- Map IDs to human-readable names (product IDs → product names, error codes → descriptions)
- Enrich logs/spans with static metadata
- Add dimension data from CSV uploads
- Lookup values without temporal considerations

Covers reference table fundamentals, both explicit and implicit lookup patterns, and when to choose Reference Tables vs Resources vs Correlation Tags.

## Key Concepts

### What Are Reference Tables?

Reference Tables are **static lookup datasets** created from CSV uploads:
- **No timestamps** - Static data
- **No change tracking** - Subsequent uploads of the same table overwrite previous state
- **Max 10MB** CSV file size
- **Uploaded manually** via Observe UI or API
- **Primary key** column for joining
- **Value columns** with descriptive data

**Example**: Product reference table
```
app_product_id,app_product_name
"OLJCESPC7Z","National Park Foundation Explorascope"
"L9ECAV7KIM","Lens Cleaning Kit"
"6E92ZMYYFZ","Solar Filter"
```

### When to Use Reference Tables

- Data is static (doesn't change over time, or if it does change, the state tracking is not required)
- Need simple ID-to-name mappings
- No temporal aspect required
- Dataset size under 10MB

## Lookup Patterns

Reference Tables support **two lookup approaches**: explicit join (recommended) and implicit join (requires column name matching).

### Pattern A: Explicit Lookup (Recommended)

**Most flexible** - specify join condition directly without column name matching:

```opal
# Join Product Logs with Product reference table using alias
lookup @product.app_product_id=product_id, pid:product_id, product_name:@product.app_product_name
| statsby count(), group_by(product_name)
| topk 10, max(product_name)
```

**How it works:**
1. Use alias for reference table: `@product`
2. Specify join condition: `@product.app_product_id=product_id`
3. Select columns to retrieve: `pname:@product.app_product_name`
4. No need to match column names!

**MCP Parameters:**
```json
{
  "primary_dataset_id": "42782295",
  "secondary_dataset_ids": ["42782294"],
  "dataset_aliases": {"product": "42782294"}
}
```

**Key advantages:**
- Column names don't need to match
- Clear and explicit join condition
- Full control over retrieved columns
- No extra `make_col` needed

### Pattern B: Implicit Lookup (Column Name Matching)

**Requires exact column name matching** - simpler syntax but less flexible:

```opal
make_col app_product_id:product_id
| lookup @product_ref
| make_col pid:product_id, pname:app_product_name
| limit 10
```

**How it works:**
1. Reference table has primary key `app_product_id`
2. Source dataset creates matching column: `make_col app_product_id:product_id`
3. `lookup` automatically joins on matching column name
4. All reference table columns added to result

**MCP Parameters:**
```json
{
  "primary_dataset_id": "42782295",
  "secondary_dataset_ids": ["42782294"],
  "dataset_aliases": {"product_ref": "42782294"}
}
```

**Why implicit requires matching:**

**❌ WRONG** - Mismatched names fail:
```opal
lookup @product_ref  # Source has 'product_id', reference has 'app_product_id'
```
**Error**: "implicit lookup requires all primary key columns in the other dataset to match columns in the source dataset; missing columns from the source dataset: app_product_id"

**✅ CORRECT** - Create matching column first:
```opal
make_col app_product_id:product_id
| lookup @product_ref
```

**When to use implicit:**
- Simple joins where column names already match
- When you want automatic inclusion of all reference columns
- Legacy queries or established patterns

**When to use explicit (Pattern A):**
- Column names don't match (most common!)
- Want control over which columns to retrieve
- Clearer, more maintainable queries

### Pattern C: Using on() with Column Bindings

**Full control** over join conditions and column selection:

```opal
# Join with explicit on() syntax
lookup on(product_id=@product.app_product_id), product_name:@product.app_product_name
| statsby count(), group_by(product_name)
```

**Use case**: Complex join conditions or when you need precise control over the join and column bindings

### Lookup Behavior

- **Join type**: Left outer join (keeps all rows)
- **No match**: Reference table columns are NULL
- **Multiple matches**: Returns all matching rows (Cartesian product)
- **Performance**: Fast for small reference tables (<10MB)

## Common Patterns

### Pattern: Enrich with Descriptive Names (Explicit Join)

```opal
# Using explicit lookup - no column name matching needed!
lookup @product.app_product_id=product_id, pname:@product.app_product_name
| filter not is_null(pname)
| make_col pid:product_id, name:pname, service:container
| limit 20
```

**Use case**: Add human-readable product names to logs

**Result**: Logs with "National Park Foundation Explorascope" instead of "OLJCESPC7Z"

**Alternative (implicit join)**:
```opal
make_col app_product_id:product_id
| lookup @product_ref
| filter not is_null(app_product_name)
| make_col pid:product_id, name:app_product_name, service:container
| limit 20
```

### Pattern: Aggregate with Reference Data (Explicit Join)

```opal
# Using explicit lookup - cleaner and more maintainable
lookup @product.app_product_id=product_id, pname:@product.app_product_name
| statsby log_count:count(), group_by(pname)
| sort desc(log_count)
```

**Use case**: Count events by descriptive name

**Result**:
```
pname,log_count
"National Park Foundation Explorascope",864
```

**Alternative (implicit join)**:
```opal
make_col app_product_id:product_id
| lookup @product_ref
| statsby log_count:count(), group_by(app_product_name)
| sort desc(log_count)
```

### Pattern: Browse Reference Table Contents

```opal
make_col id:app_product_id, name:app_product_name
| limit 50
```

**Dataset**: Query reference table directly (use reference table as primary_dataset_id)

**Use case**: See available lookup values

**Result**: Complete list of products in reference table

### Pattern: Handle Missing Lookups (Explicit Join)

```opal
# Using explicit lookup
lookup @product.app_product_id=product_id, pname:@product.app_product_name
| make_col pid:product_id,
          name:if(is_null(pname), "Unknown Product", pname)
| limit 10
```

**Use case**: Provide default value when reference lookup fails

**Behavior**: Shows "Unknown Product" when pname is NULL

### Pattern: Filter to Matched Rows Only (Explicit Join)

```opal
# Using explicit lookup
lookup @product.app_product_id=product_id, pname:@product.app_product_name
| filter not is_null(pname)
| make_col pid:product_id, name:pname
| limit 20
```

**Use case**: Exclude rows without reference table matches

**Behavior**: Only returns rows with successful lookups

## Troubleshooting

### Issue: "Missing columns from source dataset"

**Error**: "implicit lookup requires all primary key columns in the other dataset to match columns in the source dataset; missing columns from the source dataset: app_product_id"

**Cause**: Source dataset doesn't have column matching reference table's primary key

**Solution**: Create matching column with `make_col`:
```opal
make_col app_product_id:product_id
| lookup @product_ref
```

**Key insight**: Column names must match exactly (case-sensitive!)

### Issue: All reference columns are NULL

**Cause**: No matches found (lookup is left outer join)

**Diagnosis**: Check if join values actually exist in reference table:
```opal
filter app_product_id = "OLJCESPC7Z"
| limit 1
```
(Query reference table directly to verify value exists)

**Solutions**:
1. Verify product_id values in source match app_product_id in reference
2. Check for typos or case sensitivity issues
3. Ensure reference table uploaded correctly

### Issue: "Implicit lookup does not support additional arguments"

**Error**: "implicit lookup does not support additional arguments like explicit join predicates or column bindings"

**Cause**: Mixing implicit and explicit syntax:
```opal
lookup @product_ref on product_id = @product_ref.app_product_id  ❌
```

**Solution Option 1**: Use explicit lookup (recommended):
```opal
lookup @product.app_product_id=product_id, pname:@product.app_product_name  ✅
```

**Solution Option 2**: Use implicit lookup with column name matching:
```opal
make_col app_product_id:product_id
| lookup @product_ref  ✅
```

## Key Takeaways

1. **Reference Tables are for static CSV data** (no timestamps, no change tracking)
2. **Three lookup patterns available**:
   - **Explicit (recommended)**: `lookup @product.app_product_id=product_id, pname:@product.app_product_name`
   - **Implicit**: Requires exact column name matching via `make_col`
   - **on() syntax**: Full control with `lookup on(condition), bindings`
3. **Explicit lookup advantages**: No column name matching needed, clearer syntax, full control over retrieved columns
4. **Left outer join behavior** - keeps all rows, NULL when no match
5. **Use for static enrichment** - alternative to Resources when no temporal aspect needed
6. **10MB size limit** per reference table
7. **Fast and efficient** for small lookup datasets
8. **Column matching is case-sensitive** when using implicit lookup
9. **Use `is_null()` to check for failed lookups** - provides default values or filters unmatched rows
10. **Query reference tables directly** to browse available lookup values

## When to Choose Reference Tables vs Resources

| Scenario | Use Reference Tables | Use Resources |
|----------|---------------------|---------------|
| Static data that doesn't change | ✅ | ❌ |
| Data changes over time and you need state history | ❌ | ✅ |
| Simple ID-to-name mappings | ✅ | ❌ |
| Need temporal joins with Events/Intervals | ❌ | ✅ |
| CSV upload (max 10MB) | ✅ | ❌ |
| Track mutable state evolution | ❌ | ✅ |
| Fast lookups without timestamps | ✅ | ❌ |

## References

- Reference Tables created via CSV upload in Observe UI
- Use `lookup` verb with `@` alias for joining
- Explicit lookup: `@alias.ref_column=source_column, result:@alias.value_column`
- Implicit lookup: Requires matching column names (automatic join)
- on() syntax: `lookup on(condition), column_bindings`
- Maximum 10MB CSV size per table
- Interface type typically shows as "unknown" in discovery
