---
name: supabase-artifact-connection
description: Connect Supabase databases to Claude Desktop artifacts with read-only queries and live data visualization.
---

# Supabase Artifact Connection

## Core Principle

**Enable live database connections in artifacts using Supabase client library with enforced read-only access.**

## When to Activate

This skill activates when:
- User mentions "Supabase" + "artifact" or "dashboard"
- User provides Supabase credentials (URL + anon key)
- User wants to query database data in an interactive artifact
- User asks to "connect to Supabase" or "load data from Supabase"

## Connection Pattern

### Required Credentials

User must provide:
```javascript
SUPABASE_URL = 'https://[project-id].supabase.co'
SUPABASE_ANON_KEY = 'eyJhbGc...' // Public anon key
```

### Standard Initialization

Always use this exact pattern in artifacts:

```html
<!-- Supabase Client Library -->
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>

<script>
  // Initialize Supabase client
  const SUPABASE_URL = 'USER_PROVIDED_URL';
  const SUPABASE_ANON_KEY = 'USER_PROVIDED_KEY';

  const supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

  // Query example
  async function loadData() {
    const { data, error } = await supabase
      .from('table_name')
      .select('*')
      .limit(100);

    if (error) {
      console.error('Supabase query error:', error);
      return null;
    }

    return data;
  }
</script>
```

## Read-Only Access Rules

**CRITICAL: NEVER generate code that writes to Supabase.**

### ✅ ALLOWED Operations:
- `.select()` - Query data
- `.from()` - Specify table
- Filters: `.eq()`, `.gt()`, `.lt()`, `.in()`, `.not()`, `.like()`, `.ilike()`
- Ordering: `.order()`
- Limits: `.limit()`, `.range()`
- Aggregations: `.count()`, `.sum()`, `.avg()`, `.min()`, `.max()`

### ❌ FORBIDDEN Operations:
- `.insert()` - Create records
- `.update()` - Modify records
- `.upsert()` - Insert or update
- `.delete()` - Remove records
- Any mutation operations

**If user requests write operations, respond:**
> "This skill only supports read-only queries to protect database integrity. For write operations, use Supabase Dashboard or a dedicated backend service."

## Query Patterns

### Basic Query
```javascript
const { data, error } = await supabase
  .from('products')
  .select('*');
```

### Filtered Query
```javascript
const { data, error } = await supabase
  .from('products')
  .select('name, price, category')
  .eq('category', 'Electronics')
  .gt('price', 100)
  .order('price', { ascending: false })
  .limit(50);
```

### Count Query
```javascript
const { count, error } = await supabase
  .from('products')
  .select('*', { count: 'exact', head: true });
```

### Related Data (Join)
```javascript
const { data, error } = await supabase
  .from('orders')
  .select(`
    id,
    created_at,
    customer:customers(name, email),
    items:order_items(product_name, quantity)
  `)
  .limit(20);
```

## Artifact Structure

Generate artifacts with this structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Supabase Data Viewer</title>

  <!-- Supabase Client -->
  <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>

  <style>
    body {
      font-family: system-ui, -apple-system, sans-serif;
      margin: 0;
      padding: 20px;
      background: #f5f5f5;
    }

    .container {
      max-width: 1200px;
      margin: 0 auto;
      background: white;
      padding: 30px;
      border-radius: 8px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }

    .loading {
      text-align: center;
      padding: 40px;
      color: #666;
    }

    .error {
      background: #fee;
      border: 1px solid #fcc;
      padding: 15px;
      border-radius: 4px;
      color: #c33;
    }

    table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 20px;
    }

    th, td {
      text-align: left;
      padding: 12px;
      border-bottom: 1px solid #ddd;
    }

    th {
      background: #f8f8f8;
      font-weight: 600;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>Supabase Data</h1>
    <div id="content">
      <div class="loading">Loading data...</div>
    </div>
  </div>

  <script>
    // Initialize Supabase
    const SUPABASE_URL = 'USER_PROVIDED_URL';
    const SUPABASE_ANON_KEY = 'USER_PROVIDED_KEY';
    const supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

    // Load and display data
    async function loadData() {
      const contentDiv = document.getElementById('content');

      try {
        const { data, error } = await supabase
          .from('table_name')
          .select('*')
          .limit(100);

        if (error) throw error;

        if (data.length === 0) {
          contentDiv.innerHTML = '<p>No data found.</p>';
          return;
        }

        // Create table
        const columns = Object.keys(data[0]);
        let html = '<table><thead><tr>';
        columns.forEach(col => html += `<th>${col}</th>`);
        html += '</tr></thead><tbody>';

        data.forEach(row => {
          html += '<tr>';
          columns.forEach(col => html += `<td>${row[col] ?? ''}</td>`);
          html += '</tr>';
        });

        html += '</tbody></table>';
        contentDiv.innerHTML = html;

      } catch (error) {
        contentDiv.innerHTML = `<div class="error">Error loading data: ${error.message}</div>`;
      }
    }

    // Load on page load
    loadData();
  </script>
</body>
</html>
```

## Error Handling

Always include error handling:

```javascript
try {
  const { data, error } = await supabase
    .from('table_name')
    .select('*');

  if (error) throw error;

  // Process data
  console.log('Data loaded:', data);

} catch (error) {
  console.error('Supabase error:', error);
  // Show user-friendly error message
  alert('Failed to load data. Check console for details.');
}
```

## Common Errors

**Error: "Invalid API key"**
- Check SUPABASE_ANON_KEY is correct
- Ensure key starts with `eyJhbGc...`

**Error: "Table not found"**
- Verify table name spelling
- Check table exists in Supabase Dashboard
- Ensure anon key has read permissions

**Error: "Row Level Security policy violation"**
- Table has RLS enabled but no policy for anon access
- Add policy in Supabase Dashboard or disable RLS for testing

**Error: "CORS error"**
- Should not occur with official Supabase CDN
- If using self-hosted, check CORS configuration

## Performance Tips

1. **Limit results:** Always use `.limit()` for large tables
   ```javascript
   .limit(100) // Don't fetch more than needed
   ```

2. **Select specific columns:** Avoid `SELECT *` when possible
   ```javascript
   .select('id, name, created_at') // Only fetch needed columns
   ```

3. **Use filters:** Apply filters server-side, not client-side
   ```javascript
   .eq('status', 'active') // Filter in query, not in JavaScript
   ```

4. **Cache data:** Store results in variables to avoid re-querying
   ```javascript
   let cachedData = null;

   async function getData() {
     if (cachedData) return cachedData;
     const { data } = await supabase.from('table').select('*');
     cachedData = data;
     return data;
   }
   ```

## Testing Checklist

Before sharing artifact with user:
- ✅ Supabase client library loaded from CDN
- ✅ Connection initialized with user's credentials
- ✅ Query uses read-only operations only
- ✅ Error handling included
- ✅ Loading state shown to user
- ✅ Data displayed in readable format
- ✅ No console errors on page load

## Success Criteria

Artifact is successful when:
- ✅ Loads Supabase data without errors
- ✅ Displays data in user-friendly format
- ✅ No write operations in code
- ✅ Error messages are clear and helpful
- ✅ Works as standalone HTML file (no build step required)

## Example Use Cases

**Simple Data Table:**
```javascript
// Load and display all records
const { data } = await supabase.from('customers').select('*').limit(50);
```

**Filtered Dashboard:**
```javascript
// Show active users only
const { data } = await supabase
  .from('users')
  .select('name, email, created_at')
  .eq('status', 'active')
  .order('created_at', { ascending: false });
```

**Search Interface:**
```javascript
// Search by name (case-insensitive)
const { data } = await supabase
  .from('products')
  .select('*')
  .ilike('name', `%${searchTerm}%`);
```

**Analytics View:**
```javascript
// Get aggregated data
const { count } = await supabase
  .from('orders')
  .select('*', { count: 'exact', head: true })
  .gte('created_at', '2025-01-01');
```

## Next Steps After Connection

Once basic connection works:
1. Add interactive filters (dropdowns, search)
2. Implement data visualization (charts, graphs)
3. Add export functionality (CSV, JSON)
4. Create multi-table views (related data)
5. Build custom UI components (AG Grid, etc.)

**Remember:** Always start with basic connection, then enhance incrementally based on user needs.
