---
name: usaspending-api-helper
description: Expert knowledge of USA Spending API integration including filter building, award type codes, agency tiers, and API endpoints. Use when modifying API requests, adding search filters, debugging API responses, or extending search functionality.
---

# USA Spending API Helper

This skill provides expert knowledge of the USA Spending API integration used in this project.

## API Endpoints

**Production Base**: `https://api.usaspending.gov`

**Proxied Endpoints in server.js**:
- `POST /api/search` → proxies to `/api/v2/search/spending_by_award/`
- `POST /api/count` → proxies to `/api/v2/search/spending_by_award_count/`

## Award Type Codes

### Contracts
- **A**: BPA Call (Blanket Purchase Agreement)
- **B**: Purchase Order
- **C**: Delivery Order
- **D**: Definitive Contract

### Grants
- **02**: Block Grant
- **03**: Formula Grant
- **04**: Project Grant
- **05**: Cooperative Agreement

### IDVs (Indefinite Delivery Vehicles)
- **IDV_A**: GWAC (Government-Wide Acquisition Contract)
- **IDV_B**: IDC (Indefinite Delivery Contract)
- **IDV_B_A**: IDV_B_A
- **IDV_B_B**: IDV_B_B
- **IDV_B_C**: IDV_B_C
- **IDV_C**: IDV_C
- **IDV_D**: IDV_D
- **IDV_E**: IDV_E

## Filter Building Logic (buildFilters() in script.js)

### Agency Filters
The application supports two-tier agency filtering:
- **Toptier**: Main department level (e.g., Department of Defense)
- **Subtier**: Sub-agency level (e.g., Army, Navy)

**Agency Filter Structure**:
```javascript
{
  name: "agency_code",      // Agency code from API
  tier: "toptier|subtier",  // Agency tier level
  type: "awarding|funding"  // Agency relationship to award
}
```

**Logic**:
1. Check if toptier or subtier agency is selected
2. Determine if it's awarding or funding agency
3. Add to appropriate filter array

### Date Ranges
- **Default**: Last 180 days if no dates specified
- **Format**: YYYY-MM-DD
- **Structure**:
```javascript
time_period: [{
  start_date: "YYYY-MM-DD",
  end_date: "YYYY-MM-DD"
}]
```

### Award Types
- **Default Behavior**: If no award type selected, defaults to contracts A-D
- **Multiple Selection**: User can select multiple award types
- **Validation**: Award types are validated against known codes

### Keywords
- Searches across award descriptions and recipient names
- Case-insensitive matching
- Supports partial matches

## Response Fields

Standard fields requested from the API (see `buildFilters()` fields array):

**Award Information**:
- `Award ID`
- `Award Amount`
- `Award Type`
- `Description`

**Recipient Information**:
- `Recipient Name`
- `recipient_uei`
- `recipient_id`

**Agency Information**:
- `Awarding Agency`
- `Awarding Sub Agency`
- `awarding_agency_code`
- `Funding Agency`
- `Funding Sub Agency`
- `funding_agency_code`

**Additional Fields**:
- `Place of Performance`
- `Infrastructure Outlays`
- `Infrastructure Obligations`
- `Last Modified Date`
- `Base Obligation Date`

## Common Tasks

### Adding a New Search Filter

1. **Update HTML form** (`public/index.html`):
   ```html
   <input type="text" id="newFilterField" placeholder="New Filter">
   ```

2. **Modify buildFilters()** (`public/script.js`):
   ```javascript
   const newFilterValue = document.getElementById('newFilterField').value;
   if (newFilterValue) {
     filters.new_filter = newFilterValue;
   }
   ```

3. **Test filter combinations** to ensure compatibility

4. **Update documentation** if user-facing change

### Modifying API Response Fields

1. **Locate fields array** in `buildFilters()` function
2. **Add/remove fields** as needed:
   ```javascript
   fields: [
     "Award ID",
     "Award Amount",
     "New Field Name"  // Add here
   ]
   ```
3. **Update renderResults()** to handle new fields in table
4. **Test with various search queries**

### Debugging API Issues

**Common Issues**:
1. **No results returned**: Check date range and award type defaults
2. **API errors**: Check server.js console logs for detailed error messages
3. **Filter not working**: Verify filter structure matches API expectations
4. **Pagination issues**: Ensure limit and page parameters are correct

**Debugging Steps**:
1. Open browser console to see request payload
2. Verify filter structure in Network tab
3. Check server.js logs for API response errors
4. Test query directly against USA Spending API if needed
5. Compare working queries with failing ones

### Testing API Queries

**Test Cases to Consider**:
- Empty search (should use defaults)
- Single award type selection
- Multiple award type selection
- Agency filtering (toptier and subtier)
- Date range filtering
- Keyword search
- Pagination (page 1, 2, last page)
- Edge cases (no results, max results)

## Implementation Patterns

### Error Handling
```javascript
try {
  const response = await fetch('/api/search', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(filters)
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.statusText}`);
  }

  const data = await response.json();
  // Process data
} catch (error) {
  console.error('Error fetching results:', error);
  // Display user-friendly error
}
```

### Pagination Pattern
```javascript
const limit = 10;  // Records per page
const offset = (currentPage - 1) * limit;

const filters = {
  ...buildFilters(),
  limit: limit,
  page: currentPage
};
```

### Dynamic URL Generation
The application generates usaspending.gov URLs for recipients:
```javascript
const params = new URLSearchParams({
  hash: recipientHash,
  award_type: selectedAwardTypes
});
const url = `https://www.usaspending.gov/recipient/${recipientId}?${params}`;
```

## Best Practices

1. **Always validate filter inputs** before sending to API
2. **Use meaningful default values** (e.g., last 180 days)
3. **Log errors with context** for easier debugging
4. **Handle empty results gracefully** with user-friendly messages
5. **Test pagination edge cases** (first page, last page, single page)
6. **Keep award type codes synchronized** with USA Spending API documentation
7. **Cache agency lists** if fetching from API to reduce requests
8. **Validate date ranges** (start_date <= end_date)

## File Locations

- **Server proxy**: `server.js` lines 15-42
- **Client filter logic**: `public/script.js` buildFilters() function
- **Search form**: `public/index.html`
- **Result rendering**: `public/script.js` renderResults() function

## Resources

- **USA Spending API Documentation**: https://api.usaspending.gov/docs/
- **Award Data Dictionary**: https://www.usaspending.gov/data-dictionary
- **Agency Codes**: Available via `/api/v2/references/toptier_agencies/` endpoint
