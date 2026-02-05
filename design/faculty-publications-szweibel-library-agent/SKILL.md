---
name: faculty-publications
description: Ensure the library has collected all publications by faculty in a department - a collection completeness requirement
---

# Faculty Publications Collection Completeness

## Your Role

Ensure the library owns all publications authored by faculty in a department. This is a **collection requirement** - the library must collect the scholarly output of its own faculty.

## Primary Use Case: Departmental Collection Completeness

When asked to verify faculty publications for a department:

1. **Get Faculty List**
   - Ask user for list of faculty names in the department
   - Or search if department name is provided
   - Clarify time scope if needed (e.g., "publications from last 5 years" or "all time")

2. **Search Each Faculty Member's Publications**
   - Use `search_openalex(query="[faculty name] [institution/department]")`
   - For books: also use `search_worldcat(query="[faculty name]")`
   - Set appropriate `limit` (start with 50, increase if needed)

3. **Create Master Table Immediately**
   - Columns: author, title, year, type, venue, doi, isbn, holdings_status, _status
   - Include ALL publications from ALL faculty members
   - Sort by author, then year (most recent first)

4. **Check Holdings for Each Item**
   For each row:
   - `set_row_status(rowIndex, "Checking holdings...")`
   - If ISBN exists: `search_primo(field='isbn', query=isbn)`
   - If no ISBN but has DOI: `search_primo(query=title, operator='exact')`
   - Update holdings_status: "Owned" or "NOT OWNED"
   - For books without ISBN: `lookup_isbn(title=..., author=...)` then check again
   - `set_row_status(rowIndex, "✓")`

5. **Identify Gaps**
   - Filter/highlight all items with holdings_status = "NOT OWNED"
   - These are the collection gaps that need to be filled
   - Prioritize by: recent publications, books, highly cited works

6. **Provide Acquisition Recommendations**
   - Create separate table or section for items to acquire
   - Include: title, author, year, ISBN, publisher URL, justification
   - **Critical**: Verify ISBNs are correct for ordering
   - Note any items that cannot be acquired (conference proceedings chapters, preprints, etc.)

## Example Workflow

```
User: "Check if we have everything published by our History department faculty"

1. Get faculty list (user provides or you search)
   Faculty: Dr. Jane Smith, Dr. John Doe, Dr. Maria Garcia

2. Search each faculty member:
   search_openalex(query="Jane Smith History University", limit=50)
   search_openalex(query="John Doe History University", limit=50)
   search_openalex(query="Maria Garcia History University", limit=50)
   search_worldcat(query="Jane Smith")  # for books
   search_worldcat(query="John Doe")
   search_worldcat(query="Maria Garcia")

3. Combine all results into one table (e.g., 87 publications total)

4. Check holdings for each:
   Row 0: Smith, J. (2023). "Climate History..." → search_primo → "Owned"
   Row 1: Smith, J. (2022). "Book Title" → search_primo → "NOT OWNED" ⚠
   Row 2: Doe, J. (2024). "Article..." → search_primo → "Owned"
   ...

5. Summarize gaps:
   "Found 87 publications. Library owns 71. MISSING 16 items:
   - 8 books
   - 5 journal articles (may have electronic access through databases)
   - 3 book chapters"

6. Recommend acquisition:
   Create filtered table of 16 missing items with ISBNs and acquisition details
```

## Key Principles

**This is a requirement, not optional:**
- The library MUST collect faculty publications
- Missing items represent collection failures that need to be corrected
- Prioritize recent work and books (articles may be accessible via subscriptions)

**Be thorough:**
- Don't skip items - check every single publication
- Search multiple sources (OpenAlex AND WorldCat for books)
- Verify author affiliations to avoid false matches
- Check name variations (e.g., "J. Smith" vs "Jane Smith" vs "Jane A. Smith")

**Focus on actionable gaps:**
- Clearly identify what's missing
- Provide ISBNs for ordering
- Distinguish between books (must acquire) and articles (may have access)
- Note items that can't be acquired individually

## Holdings Status

- **Owned**: Confirmed in library catalog
- **NOT OWNED**: Not in catalog - acquisition needed ⚠
- **Electronic Access**: Not in catalog but may have database access
- **Unable to Verify**: Missing identifiers, need manual check

## What Can/Cannot Be Acquired

**Can acquire:**
- Books (monographs)
- Edited volumes
- Journal issues (if faculty edited)

**Cannot acquire individually:**
- Journal articles (library likely has journal subscription)
- Book chapters (must buy whole book)
- Conference proceedings papers (unless proceedings volume available)
- Preprints/working papers (not published)

**Verify before recommending:**
- Check if journal article access exists through databases
- For chapters, recommend acquiring the entire edited volume
- Flag items that need manual review

## Progress Tracking

Since this can involve many faculty and publications:
- Use `set_row_status` to show progress
- Process systematically (one faculty member at a time, or all publications row-by-row)
- Keep user informed: "Checking 87 publications... 45/87 complete..."
- Summarize periodically: "So far found 12 items not owned..."

## Final Deliverable

Provide a clear acquisition list:
1. Table of missing items with acquisition details
2. Summary statistics (total pubs, owned, missing)
3. Breakdown by type (books vs articles vs chapters)
4. Prioritized recommendations

Your goal is to ensure complete collection coverage of faculty scholarly output and identify specific gaps for acquisition.
