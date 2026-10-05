---
name: cjis-foreclosure-puller
description: >
  Pull court case filings from the Stark County CJIS portal (starkcjis.org) and build a structured Excel spreadsheet with property addresses. Use this skill whenever Sean asks to pull, download, grab, or refresh courthouse data — whether he says "pull today's foreclosures," "get fresh filings from Stark County court," "update my leads spreadsheet from CJIS," "run the daily court pull," "what got filed today," or anything about extracting new case records from starkcjis.org. Also triggers for phrases like "first to market data," "new filings today," "run the court pull," or "how many foreclosures were filed." Default case type is foreclosures, but also works for other civil case types if requested.
---

# Stark County CJIS Court Data Puller

## What this skill does

Pulls civil case filings from the Stark County CJIS portal at `https://www.starkcjis.org`. Fetches case details including property addresses, then builds a multi-sheet Excel workbook optimized for real estate wholesaling lead generation.

## Before you start — ask the user

1. **What case type?** Default: foreclosures. Other options: probates, tax liens, general civil.
2. **What date range?**
   - Today only (default — use this for "daily pull" or "run the pull")
   - Last N days
   - Specific month
   - Full year-to-date
3. **Is starkcjis.org already open in Chrome?** If not, navigate there first.

---

## Critical technical constraint

**Python cannot reach CJIS APIs directly** — the sandbox VM's outbound requests are blocked (ProxyError). All API calls must be made via JavaScript injected into the user's Chrome browser using the `javascript_tool`. Never attempt `requests.get()` or `urllib` against starkcjis.org.

---

## Step 1: Navigate to the portal

Make sure Chrome is on:
```
https://www.starkcjis.org/#/search
```

---

## Step 2: Query the Search API

Stark County CJIS Advanced Search endpoint:
```
GET /api/search/advanced?criteria={JSON}&isDocket=true
```

**⚠️ Hard cap of 1,000 rows per query.** If pulling more than ~2–3 weeks of foreclosures, chunk by month (one query per month) and merge results.

### Building the criteria

```javascript
// Standard foreclosure query — today only (daily pull default)
const today = new Date().toISOString().split('T')[0]; // e.g. "2026-04-14"
const criteria = JSON.stringify({
  "scCode": "E",   // 'E' = foreclosure in CPC (Common Pleas); 'F' = foreclosure in municipal courts
  "dateRange": { "startDate": today, "endDate": today }
});
const resp = await fetch(`/api/search/advanced?criteria=${encodeURIComponent(criteria)}&isDocket=true`);
const data = await resp.json();
console.log('Total:', data.totalCount, '| Returned:', data.cases?.length);
```

### Known Stark County scCodes (verified)

| Case Type | Court | scCode |
|-----------|-------|--------|
| Foreclosure | CPC (Common Pleas) | `E` |
| Foreclosure | Municipal (CMC/MMC/AMC) | `F` |

For an unfamiliar case type, verify the scCode first by looking up a known case:
```javascript
const r = await fetch('/api/search/advanced?criteria=' + 
  encodeURIComponent(JSON.stringify({"caseNumber": "2026CV00741"})) + '&isDocket=true');
const d = await r.json();
console.log(d.cases?.[0]?.scCode); // confirms "E" for CPC foreclosure
```

### Court filtering

To get **all courts** (CPC + all municipal), run two queries and merge:
1. CPC: add `"court": "CPC"` to criteria
2. Municipal: use `scCode: "F"` without court filter

Or omit scCode entirely and filter client-side:
- CPC case numbers match: `2026CVnnnnn` (no F)
- Municipal case numbers match: `2026CVFnnnnn`

### Chunking by month for large date ranges

```javascript
async function fetchMonth(year, month) {
  const start = `${year}-${String(month).padStart(2,'0')}-01`;
  const end = new Date(year, month, 0).toISOString().split('T')[0];
  const criteria = JSON.stringify({
    "scCode": "E",
    "dateRange": { "startDate": start, "endDate": end }
  });
  const r = await fetch(`/api/search/advanced?criteria=${encodeURIComponent(criteria)}&isDocket=true`);
  const d = await r.json();
  return d.cases || [];
}
// Example: pull Jan–Apr 2026
const allCases = (await Promise.all([1,2,3,4].map(m => fetchMonth(2026, m)))).flat();
```

---

## Step 3: Extract case data from results

For each case in `data.cases`, capture:
- `_id` — MongoDB ObjectId (needed for address lookup in Step 4)
- `caseNumber` — e.g. `2026CV00741` or `2026CVF00277`
- `fileDate` — ISO date string
- `court.code` — CPC, CMC, MMC, AMC, etc.
- `parties[0].name` — plaintiff / lender
- `parties[1].name` — defendant / homeowner

Build a map: `{ caseNumber → _id }` for the address fetch step.

---

## Step 4: Fetch property addresses

The search API does NOT include addresses. Hit the case detail endpoint for each case:

```
GET /api/case/{mongoObjectId}
```

The defendant's `participants[].address` is the property address. Find the defendant participant (role contains "defendant"), or fall back to `participants[1]`.

**Batch 10 at a time:**

```javascript
// Store results globally so they survive across JS tool calls
window._addrMap = {};

async function fetchAddressBatch(entries) {  // entries = [[caseNum, mongoId], ...]
  await Promise.all(entries.map(async ([cn, id]) => {
    const r = await fetch(`/api/case/${id}`);
    const d = await r.json();
    const def = d.participants?.find(p =>
      p.role?.toLowerCase().includes('def')
    ) || d.participants?.[1];
    const a = def?.address;
    window._addrMap[cn] = a
      ? [a.line1, a.city, a.state, a.zip].filter(Boolean).join(', ')
      : 'ADDRESS UNKNOWN';
  }));
}

// Call in a loop, 10 at a time:
const entries = Object.entries(caseIdMap);
for (let i = 0; i < entries.length; i += 10) {
  await fetchAddressBatch(entries.slice(i, i + 10));
}
Object.keys(window._addrMap).length; // confirm count
```

---

## Step 5: Transfer data from browser to Python

**⚠️ The JS tool truncates output at ~1,400 characters.** Never return a large JSON object directly — it will be silently cut off. Always use the chunked transfer pattern.

```javascript
// Encode all case data as pipe-delimited lines
const lines = window._cases.map(c =>
  [c.caseNumber, c.fileDate, c.court, c.plaintiff, c.defendant,
   window._addrMap[c.caseNumber] || ''].join('|')
).join('\n');

// Break into ~800-char chunks stored in a global array
window._chunks = [];
for (let i = 0; i < lines.length; i += 800) {
  window._chunks.push(lines.slice(i, i + 800));
}
window._chunks.length; // returns chunk count — read this first
```

Then read chunks one at a time in separate JS tool calls:
```javascript
window._chunks[0]   // chunk 0
window._chunks[1]   // chunk 1
// ... up to window._chunks[N-1]
```

Parse in Python:
```python
all_lines = []
for chunk in chunks:        # list of strings you read from browser
    all_lines.extend(chunk.strip().split('\n'))

cases = []
for line in all_lines:
    if '|' not in line:
        continue
    case_num, file_date, court, plaintiff, defendant, address = line.split('|', 5)
    cases.append({...})
```

---

## Step 6: Build the Excel workbook

Use `openpyxl`. Four-sheet structure:

| Sheet | Contents |
|-------|----------|
| **All Cases** | Every case: Case #, Court, Full Court Name, File Date, Type, Plaintiff/Lender, Defendant/Homeowner, Property Address, CJIS Link |
| **By Lender** | Ranked plaintiff counts — useful for spotting the most active servicers/banks |
| **Monthly Trend** | Filing counts by month (Total / Mortgage / Tax) |
| **CPC Mortgage Leads** | CPC cases only, filtered to mortgage/lender types — the highest-value lead list |

### Classify lender type (for color coding and the Leads sheet filter):
```python
def lender_type(name):
    n = name.upper()
    if any(x in n for x in ['TREASURER', 'TAX EASE']):
        return 'Tax Foreclosure'
    if any(x in n for x in ['BANK', 'MORTGAGE', 'SERVICING', 'LOAN', 'LENDING',
                              'FINANCE', 'FUND', 'SAVINGS', 'CREDIT UNION']):
        return 'Mortgage / Lender'
    return 'Foreclosure'
```

### Style constants:
```python
HDR   = PatternFill('solid', start_color='1F4E79')   # dark blue header
TAX   = PatternFill('solid', start_color='FFF2CC')   # yellow = tax foreclosure
MTGE  = PatternFill('solid', start_color='E2EFDA')   # green = mortgage
WHITE = PatternFill('solid', start_color='FFFFFF')
```

### Save location
```python
# Always save to the user's mounted Claude folder
out = '/sessions/.../mnt/Claude/Stark_County_Foreclosures_2026.xlsx'
# For daily snapshots: Stark_County_Foreclosures_2026-04-14.xlsx
```

---

## Step 7: Present the file

Use `mcp__cowork__present_files` after saving. Report:
- Total cases found and date range
- How many have property addresses
- How many landed in the CPC Mortgage Leads sheet

---

## Daily pull behavior

When the user says "run the daily pull" or "pull today's filings":
- Date range = today only
- File name = `Stark_County_Foreclosures_{YYYY-MM-DD}.xlsx`
- If zero cases were filed today (common on weekends/holidays), say so clearly rather than producing an empty file

For ongoing use, consider keeping a **master YTD file** that new daily records get appended to (de-duplicate by case number). Ask the user which they prefer.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `totalCount` is 0 | Verify scCode by looking up a known case (see Step 2). Try without scCode to see what's returned. |
| Results capped at exactly 1,000 | Chunk by month — you're hitting the row cap |
| JS output appears cut off | You're not using the chunked pattern — store in `window._chunks` and read sequentially |
| Address is a servicer's office address | Normal for some cases — include as-is |
| `ADDRESS UNKNOWN` | Filed without address (common for estates/unknown heirs) — include as-is |
| Python `ProxyError` on CJIS URLs | Expected — you cannot call CJIS from Python. JS in Chrome only. |
