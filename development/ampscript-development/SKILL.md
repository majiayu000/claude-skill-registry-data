---
name: ampscript-development
description: "Use this skill when writing, debugging, or reviewing AMPscript in Marketing Cloud email bodies, subject lines, preheaders, SMS, push notifications, or Cloud Pages — including Lookup/LookupRows data retrieval, IF/ELSEIF conditional blocks, FOR loops over rowsets, and inline personalization. NOT for Server-Side JavaScript (SSJS), REST API calls from content, SQL Query Activities, or Journey Builder configuration."
category: apex
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Performance
  - Reliability
  - Security
triggers:
  - "how do I personalize an email with data from a data extension in Marketing Cloud"
  - "AMPscript LookupRows returns empty or null even though records exist in the DE"
  - "how to loop over multiple rows from a data extension inside an email send"
  - "what is the difference between Lookup and LookupRows in AMPscript"
  - "AMPscript variable not declared error when sending an email"
  - "how to show different content per subscriber based on a field value in Marketing Cloud"
  - "AMPscript FOR loop syntax to iterate over a rowset"
tags:
  - ampscript
  - marketing-cloud
  - personalization
  - data-extension
  - email-studio
  - cloud-pages
inputs:
  - "Target channel: email body / subject line / preheader / SMS / push / Cloud Page"
  - "Data Extension name(s) involved and their primary key fields"
  - "Subscriber attribute or sendable DE field used as the lookup key"
  - "Desired output: single value, multi-row list, or conditional content block"
outputs:
  - "AMPscript code block (%%[ ... ]%%) with correct variable declarations and function calls"
  - "Inline output expressions (%%= v(@var) =%%) placed in the correct location"
  - "Validated FOR loop structure with Row(@rows, @i) field access pattern"
  - "Documented decision on AMPscript vs SSJS for the use case"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-10
---

# AMPscript Development

This skill activates when a practitioner needs to write or debug AMPscript — the Marketing Cloud server-side scripting language evaluated at send time — to retrieve data from Data Extensions, apply conditional logic per subscriber, iterate over multi-row results, or embed dynamic personalization in email, SMS, push, or Cloud Page content. It does not cover SSJS, SQL Query Activities, or Journey Builder entry configuration.

---

## Before Starting

Gather this context before working on anything in this domain:

- **Channel:** AMPscript syntax is identical across channels (email, SMS, push, Cloud Page), but subject lines and preheaders support only inline `%%= ... =%%` expressions — block syntax `%%[ ... ]%%` in subject lines causes send failures.
- **Data Extension structure:** Confirm the DE name (exact, case-sensitive in some contexts), the primary key field(s), and which field holds the subscriber's match value. Non-PK fields used in `Lookup` or `LookupRows` trigger full table scans on large DEs.
- **Subscriber context:** For email sends, the sendable DE or All Subscribers list provides the subscriber key. `AttributeValue("FieldName")` reads from the sendable DE row for the current subscriber; `Lookup()` reads from any other DE.
- **Common wrong assumption:** Practitioners assume AMPscript variables are available across `%%[ ... ]%%` blocks without re-declaration. Variables declared in one block are available in subsequent blocks in the same content area, but not across separate content areas in a template.
- **Limits:** `LookupRows()` returns a maximum of 2,000 rows. `LookupOrderedRows()` accepts a count cap as its second argument. Neither function paginates — design DEs so subscriber-scoped queries return well under 2,000 rows.

---

## Core Concepts

### AMPscript Execution Model

AMPscript is evaluated server-side at send time — once per subscriber per send. It is not evaluated when the email is designed, previewed without a subscriber context, or when the template is saved. The implication: preview with a specific test subscriber selected, not the generic preview, or personalization strings and Lookup calls will return empty.

Code blocks use `%%[ ... ]%%` syntax. Multiple blocks in a single content area execute sequentially in document order. Inline output uses `%%= expression =%%` or the equivalent `%%=v(@variable)=%%` shorthand.

### Variables and Declaration

Every variable must be declared with `SET` before use:

```
%%[
SET @firstName = AttributeValue("FirstName")
SET @loyaltyTier = Lookup("Loyalty_DE", "Tier", "SubscriberKey", _subscriberkey)
]%%
```

Referencing `@firstName` before the `SET` statement causes a runtime error and may suppress the entire email. AMPscript is case-insensitive for variable names but case-sensitive for DE names and field names in Lookup calls on case-sensitive (`CS`) function variants.

### Lookup Functions

Four lookup functions cover the main retrieval patterns:

| Function | Returns | When to Use |
|---|---|---|
| `Lookup(DE, returnField, matchField, matchValue)` | Single scalar value | Fetch one field from one matching row |
| `LookupRows(DE, matchField, matchValue)` | Rowset (all matches) | Fetch all matching rows for iteration |
| `LookupOrderedRows(DE, count, sortField, sortOrder, matchField, matchValue)` | Rowset (capped, sorted) | Fetch top-N rows in order |
| `LookupCS(...)` / `LookupRowsCS(...)` | Same as above | Case-sensitive match — required when match values include mixed case and the DE is case-sensitive |

`Lookup()` returns the value of `returnField` from the first matching row only. If multiple rows match, only the first is returned (undefined ordering unless the DE has a single PK match). Use `LookupRows()` when multiple rows may match.

### FOR Loops Over Rowsets

Iterating over a `LookupRows()` result uses a numeric FOR loop with `Row(@rowset, @index)` to dereference each row:

```
%%[
SET @rows = LookupRows("Order_DE", "SubscriberKey", _subscriberkey)
SET @rowCount = RowCount(@rows)

FOR @i = 1 TO @rowCount DO
  SET @row = Row(@rows, @i)
  SET @orderNum = Field(@row, "OrderNumber")
  SET @total = Field(@row, "Total")
  /* output handled inline below */
NEXT @i
]%%
```

The inline output for each iteration must be placed between `DO` and `NEXT @i` or use separate inline expressions. `RowCount()` returns 0 when no rows match — always guard with an `IF @rowCount > 0` check before the loop to avoid rendering empty list markup.

---

## Common Patterns

### Pattern: Conditional Content Block by Subscriber Attribute

**When to use:** Show different email body sections based on a field value in the sendable DE or a related DE (e.g., loyalty tier, product preference, region).

**How it works:**
```
%%[
SET @tier = AttributeValue("LoyaltyTier")
]%%

%%[ IF @tier == "Gold" THEN ]%%
  <p>As a Gold member, enjoy 20% off your next order.</p>
%%[ ELSEIF @tier == "Silver" THEN ]%%
  <p>As a Silver member, enjoy 10% off your next order.</p>
%%[ ELSE ]%%
  <p>Join our loyalty program to start earning rewards.</p>
%%[ ENDIF ]%%
```

**Why not the alternative:** Dynamic Content blocks in Email Studio are configured via the UI and evaluated before send — they cannot use AMPscript expressions as their conditions, only data filter rules. Use AMPscript `IF/ELSEIF` when conditions are data-driven and require arithmetic, string concatenation, or nested lookups.

### Pattern: Multi-Row Order / Product List in Email Body

**When to use:** Render a subscriber-specific list (recent orders, product recommendations, event registrations) fetched from a non-sendable DE.

**How it works:**
```
%%[
SET @subKey = _subscriberkey
SET @orders = LookupOrderedRows("RecentOrders_DE", 5, "OrderDate", "DESC", "SubscriberKey", @subKey)
SET @orderCount = RowCount(@orders)
]%%

%%[ IF @orderCount > 0 THEN ]%%
<ul>
%%[ FOR @i = 1 TO @orderCount DO ]%%
  %%[ SET @row = Row(@orders, @i) ]%%
  <li>%%=Field(@row, "OrderNumber")=%% — %%=Field(@row, "Total")=%%</li>
%%[ NEXT @i ]%%
</ul>
%%[ ELSE ]%%
<p>No recent orders found.</p>
%%[ ENDIF ]%%
```

**Why not the alternative:** SSJS can perform the same retrieval via `Platform.Load("Core", "1")` and `DataExtension.Init()`, but SSJS is evaluated once per page/send context and has a higher runtime cost. For per-subscriber rendering AMPscript is preferred. Use SSJS only when making HTTP API calls or manipulating complex data structures unavailable in AMPscript.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Per-subscriber field personalization from sendable DE | `AttributeValue()` or personalization string `%%FieldName%%` | Direct access to sendable DE row; no extra query cost |
| Fetch a single value from another DE | `Lookup()` | Returns scalar value; lightest-weight retrieval |
| Fetch multiple rows from another DE | `LookupRows()` or `LookupOrderedRows()` | Returns iterable rowset; use FOR loop for rendering |
| Condition depends on subscriber data at send time | AMPscript `IF/ELSEIF/ELSE` | Evaluated per subscriber; Dynamic Content blocks cannot use runtime expressions |
| Need to call a REST API or perform HTTP fetch | SSJS | AMPscript has no HTTP call functions; use `HTTPGet` in AMPscript only for simple URL fetches with no auth headers |
| Case-sensitive field match required | `LookupCS()` / `LookupRowsCS()` | Default Lookup variants are case-insensitive; CS variants force exact case matching |
| Subject line or preheader personalization | Inline `%%= AttributeValue("Field") =%%` | Block syntax `%%[ ]%%` not supported in subject/preheader |

---

## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner working on this task:

1. **Identify the channel and content area** — confirm whether the AMPscript will live in the email body, subject line, preheader, SMS, push, or Cloud Page. Subject lines and preheaders support inline expressions only.
2. **Map the data source** — identify the Data Extension name(s) and field(s) needed. Note whether the lookup field is the DE primary key (fast) or a non-PK field (full table scan risk on large DEs).
3. **Choose the retrieval function** — use `AttributeValue()` for sendable DE fields, `Lookup()` for a single value from another DE, `LookupRows()` or `LookupOrderedRows()` for multi-row results. Use `CS` variants only if case-sensitive matching is required.
4. **Write and declare all variables before use** — place all `SET` statements at the top of the `%%[ ... ]%%` block. Never reference a variable before it is declared.
5. **Build the FOR loop with null guard** — always check `RowCount(@rows) > 0` before entering a FOR loop. Access each row with `Row(@rows, @i)` and each field with `Field(@row, "FieldName")`.
6. **Preview with a real subscriber context** — use the Preview tab with a subscriber selected or a test send to a seed list. Generic preview does not evaluate Lookup calls.
7. **Validate output and fallback paths** — confirm the ELSE branch renders correctly when no data matches, and that required fields are never null in output positions.

---

## Review Checklist

Run through these before marking work in this area complete:

- [ ] All variables declared with `SET` before first use
- [ ] `LookupRows()` results guarded with `IF RowCount(@rows) > 0` before FOR loop
- [ ] FOR loop uses `Row(@rows, @i)` and `Field(@row, "FieldName")` — not direct array notation
- [ ] Subject line and preheader use only inline `%%= ... =%%` syntax, not block syntax
- [ ] Lookup field is the DE primary key or has a documented performance note if non-PK
- [ ] All string literals use straight quotes (`"`) not smart/curly quotes
- [ ] Fallback/ELSE content is present and renders correctly when no data matches
- [ ] Tested with a real subscriber via preview or test send — not generic preview only

---

## Salesforce-Specific Gotchas

Non-obvious platform behaviors that cause real production problems:

1. **Primary key immutability post-creation** — Once a Data Extension is created, its primary key field(s) cannot be changed. If the wrong field is set as the PK, the DE must be recreated and all historical data migrated. This frequently affects teams that set `Email` as the PK and later need to switch to `ContactKey`.
2. **Generic preview suppresses Lookup errors** — Previewing an email without selecting a specific subscriber returns empty strings for all `Lookup()` and `AttributeValue()` calls rather than an error. Teams ship broken personalization to production because generic preview "worked." Always preview with a real subscriber or send to a test seed list.
3. **Block syntax in subject lines silently breaks the send** — Using `%%[ SET @x = ... ]%%` in a subject line field does not produce an error in the UI; it renders the literal `%%[...]%%` text to subscribers. Marketing Cloud only evaluates inline `%%= ... =%%` syntax in subject and preheader fields.
4. **LookupRows cap at 2,000 rows with no error** — If a subscriber has more than 2,000 matching rows, `LookupRows()` silently returns 2,000 rows with no warning. Loops that depend on a complete dataset will silently produce incomplete output. Use `LookupOrderedRows()` with an explicit count to make the cap intentional.
5. **Smart quotes cause parse failures** — Copying AMPscript from Word, Google Docs, or a rich-text editor frequently introduces curly/smart quotes (`"` `"`). Marketing Cloud's parser treats these as invalid characters, and the error message is often generic ("script error") rather than pointing at the quote character.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| AMPscript code block | `%%[ ... ]%%` block with variable declarations, lookup calls, and conditional/loop logic |
| Inline output expression | `%%= v(@var) =%%` or `%%=Field(@row, "Field")=%%` placed in HTML content |
| Decision note | Documentation of AMPscript vs SSJS choice rationale for the use case |
| Test subscriber record | Seed list entry or test data record used to validate personalization at send time |

---

## Related Skills

- `data-extension-design` — design DEs with appropriate PKs and indexing before writing AMPscript Lookup calls against them
- `email-studio-administration` — configure sendable DEs, All Subscribers list, and send classification before writing subscriber-context AMPscript
- `marketing-cloud-data-sync` — set up Synchronized Data Extensions (SDEs) used as lookup sources in AMPscript personalization
