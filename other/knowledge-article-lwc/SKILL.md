---
name: knowledge-article-lwc
description: "Use this skill when building Lightning Web Components that query, display, or accept feedback on Salesforce Knowledge articles — covering Knowledge__kav SOQL/SOSL retrieval via Apex, caching strategy, and Experience Cloud guest access. NOT for Knowledge admin setup (article types, data categories, channels), Einstein Article Recommendations configuration, or Flow-based article surfacing."
category: lwc
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Security
  - Performance
  - Reliability
triggers:
  - "How do I display a Knowledge article body in an LWC on an Experience Cloud site?"
  - "How do I query Knowledge__kav from Apex and wire it to a Lightning Web Component?"
  - "How do I let Experience Cloud guests search and vote on Knowledge articles without giving them too much access?"
tags:
  - knowledge
  - knowledge-article
  - lwc
  - experience-cloud
  - soql
  - sosl
  - apex
  - wire
inputs:
  - "Knowledge article object API name (usually Knowledge__kav or a custom ArticleType__kav)"
  - "Target surface: internal app, Experience Cloud authenticated, or Experience Cloud guest"
  - "Whether article voting or feedback is required"
  - "Data category structure for the org (required for Experience Cloud visibility)"
outputs:
  - "Apex controller with @AuraEnabled(cacheable=true) methods for article retrieval"
  - "LWC component files (HTML, JS, meta) for rendering article content"
  - "Apex DML methods for voting / feedback submission"
  - "Permission and sharing configuration notes for Experience Cloud guest access"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-06
---

# Knowledge Article LWC

Use this skill when a Lightning Web Component must retrieve and render Salesforce Knowledge article content, or accept user feedback such as thumbs-up/thumbs-down voting. It covers the correct Apex-backed retrieval pattern, Experience Cloud guest access requirements, and voting via custom Apex endpoints.

---

## Before Starting

Gather this context before working on anything in this domain:

- **Article object name**: Confirm whether the org uses the standard `Knowledge__kav` or a legacy custom article type (e.g. `FAQ__kav`). The object API name affects every SOQL query.
- **Target surface**: Determine whether the component will run inside an internal app (authenticated user, full sharing rules), an Experience Cloud site with authenticated members, or an Experience Cloud site with guest user access. Guest access is the most constrained case and drives significant design decisions.
- **Data category structure**: If the org uses data categories, identify which category groups and values articles are assigned to. Data category visibility settings control which articles are visible to which users, including guests. Missing category visibility is the most common reason articles do not appear for guest users.
- **Article fields needed**: Rich text body fields (`Body__c` on custom types, or the standard `Body` field) render HTML. Identify all fields needed upfront to avoid extra round trips.
- **Voting / feedback requirement**: If users should rate articles, a custom Apex method with `without sharing` or an explicit sharing declaration is required — there is no platform-native wire adapter for Knowledge voting.

---

## Core Concepts

### No Dedicated Wire Adapter for Knowledge

Salesforce does not provide a Lightning Data Service wire adapter specifically for Knowledge articles. There is no `@wire(getKnowledgeArticle)` equivalent in the platform wire service. All Knowledge article retrieval must go through one of two paths:

1. `@wire(getRecord, { recordId, fields })` — works for single article records when you have a record ID and the running user has read access via sharing and data category visibility. Cannot be used for search-based retrieval.
2. A custom `@AuraEnabled(cacheable=true)` Apex method that executes SOQL or SOSL against `Knowledge__kav` (or the custom article type) and returns the result. This is the standard pattern for all search-driven or list-based retrieval.

The `cacheable=true` annotation on Apex is mandatory for methods wired with `@wire`. Methods called imperatively (e.g., on button click) must NOT be annotated `cacheable=true` if they perform DML or call non-deterministic logic.

### Knowledge__kav SOQL and SOSL Queries

`Knowledge__kav` represents published article versions. The key fields and constraints are:

- `PublishStatus = 'Online'` — always filter to this value to return only live articles. Omitting this filter returns draft, archived, and online versions.
- `Language = 'en_US'` — filter by language code when the org has multi-language Knowledge enabled.
- `IsVisibleInApp`, `IsVisibleInPkb`, `IsVisibleInCsp`, `IsVisibleInPrm` — channel visibility flags. For Experience Cloud (formerly Community), `IsVisibleInPkb` must be `true`.
- `DataCategorySelections` — a child relationship, not directly queryable in a standard SOQL `WHERE` clause. Data category filtering in SOQL uses the special `WITH DATA CATEGORY` clause: `SELECT Id, Title FROM Knowledge__kav WHERE PublishStatus = 'Online' WITH DATA CATEGORY Products__c ABOVE 'All'`.
- SOSL with `FIND` supports full-text search across article content fields and respects data category visibility automatically when run in the user's context.

Guest users execute queries in the Guest User context. Sharing rules for Knowledge in guest contexts are controlled by the org-wide default for Knowledge and by Guest User data category visibility settings in Setup > Channels > Data Category Visibility.

### Experience Cloud Guest Access and Data Category Visibility

Experience Cloud guest users are unauthenticated visitors. They share a single Guest User record. For a Knowledge article to be visible to a guest user, ALL of the following must be true:

1. The Knowledge org-wide sharing default allows read access to guests (Setup > Sharing Settings > Knowledge, or the site's guest sharing override).
2. The article's `IsVisibleInPkb` field is `true`.
3. The Guest User has data category visibility for the category the article is filed under (Setup > Data Category Visibility in Experience Workspaces, or org-level Guest Category Visibility).
4. The Apex controller class must be marked `without sharing` or use an explicit `with sharing` declaration that permits guest access; otherwise the guest user context will deny the query.

Misconfiguring any one of these four conditions silently returns zero results rather than throwing an error, which makes this extremely difficult to debug without systematically checking each layer.

### Voting and Feedback via Custom Apex

The standard Knowledge `KnowledgeArticleViewStat` and `KnowledgeArticleVoteStat` objects are read-only aggregates computed by the platform. To record a user vote, use the `KbManagement.PublishingService` Apex class (available in API 30+):

```apex
KbManagement.PublishingService.rateKnowledgeArticle(articleId, rating, userId);
```

Where `rating` is an integer from 1–5. There is no direct DML on `KnowledgeArticleVoteStat`. This method must be called from a non-cacheable `@AuraEnabled` Apex method (not wired) triggered by an explicit user action. The call counts against governor limits as a DML statement equivalent.

---

## Common Patterns

### Pattern: Wired SOSL Search Component

**When to use:** A search bar LWC where the user types a query and the component surfaces matching Knowledge articles in real time or on submit.

**How it works:**

1. The LWC captures the user's search string from an input event.
2. On input change (debounced) or on form submit, the component calls an imperative Apex method (not wired, because the search string is dynamic) decorated with `@AuraEnabled(cacheable=true)`.
3. The Apex method runs a SOSL query against `Knowledge__kav` scoped to `PublishStatus = 'Online'` and the appropriate channel visibility flag.
4. The Apex method returns a `List<Knowledge__kav>` (or a wrapper DTO) to the component.
5. The component renders results using `for:each` iteration in the HTML template.

**Why not the alternative:** Using `@wire` with a reactive property for the search string works, but it fires immediately on every keystroke. An imperative call with client-side debounce gives better UX and reduces Apex invocations.

### Pattern: Single Article Display via getRecord Wire

**When to use:** A detail page component where the article ID is available via `@api recordId` from the record page (e.g., an Experience Cloud article detail page).

**How it works:**

1. Declare the component with `@api recordId`.
2. Use `@wire(getRecord, { recordId: '$recordId', fields: FIELDS })` where `FIELDS` is an array of field references imported from `@salesforce/schema`.
3. Extract field values using `getFieldValue` from `lightning/uiRecordApi`.
4. Render the body HTML using `lightning-formatted-rich-text` (not `innerHTML` — see anti-patterns).

**Why not the alternative:** A custom SOQL Apex call for a single known record ID introduces unnecessary overhead. `getRecord` is served from Lightning Data Service cache and does not count against Apex limits for simple field reads.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Single article detail page, record ID in URL | `@wire(getRecord)` with `lightning/uiRecordApi` | Uses LDS cache, no Apex limits consumed |
| Search-driven article list | Imperative `@AuraEnabled(cacheable=true)` Apex + SOSL | Dynamic input cannot be wired declaratively without complex reactive property management |
| Filtered article list (category, channel) | `@AuraEnabled(cacheable=true)` Apex + SOQL with `WITH DATA CATEGORY` | Only SOQL supports structured data category filtering |
| Experience Cloud guest users | Apex controller marked `without sharing`, guest data category visibility configured | Guest user context lacks sharing privileges; declarative visibility must be set explicitly |
| User voting / rating | Non-cacheable `@AuraEnabled` Apex calling `KbManagement.PublishingService.rateKnowledgeArticle` | No DML or LDS mutation API for Knowledge votes; platform service method is the only supported path |
| Rendering rich text article body | `lightning-formatted-rich-text value={bodyField}` | Prevents XSS from unescaped HTML; never use `innerHTML` for Knowledge body content |

---

## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner working on this task:

1. **Confirm the article object and fields**: Identify the article type API name (`Knowledge__kav` or custom), required fields (Title, Summary, Body, channel flags, language), and whether multi-language is enabled. Check Setup > Knowledge Settings.
2. **Determine the target surface and access model**: Identify whether the component runs on an internal app page, an Experience Cloud authenticated page, or a guest-accessible page. For guest access, check Guest User data category visibility and sharing settings before writing any code.
3. **Choose the retrieval pattern**: Use `@wire(getRecord)` for single known-record-ID detail pages. Use an imperative `@AuraEnabled(cacheable=true)` Apex method with SOSL for search, or SOQL with `WITH DATA CATEGORY` for category-scoped list views.
4. **Write the Apex controller**: Implement `@AuraEnabled(cacheable=true)` retrieval methods. For Experience Cloud guest scenarios, declare the class `without sharing` and filter `IsVisibleInPkb = true`. For voting, implement a separate non-cacheable `@AuraEnabled` method calling `KbManagement.PublishingService.rateKnowledgeArticle`.
5. **Build the LWC**: Import Apex methods with `@salesforce/apex`. Use `@wire` for cacheable methods bound to reactive properties, or call methods imperatively inside event handlers. Render body content exclusively with `lightning-formatted-rich-text`.
6. **Test Experience Cloud guest access end to end**: Preview the site as a guest user, not just as an admin. Admin previews bypass sharing and category visibility. A dedicated guest-context test is mandatory before marking complete.
7. **Write Apex tests**: Cover both the happy path and the case where no articles match (empty list return). Test `without sharing` methods explicitly. Aim for 90%+ coverage on the Apex controller.

---

## Review Checklist

Run through these before marking work in this area complete:

- [ ] SOQL/SOSL queries filter `PublishStatus = 'Online'` and the correct channel visibility flag
- [ ] Rich text body fields rendered exclusively via `lightning-formatted-rich-text`, not `innerHTML`
- [ ] Experience Cloud guest scenarios: data category visibility and `IsVisibleInPkb` confirmed in Setup
- [ ] Apex controller sharing declaration is appropriate for the target user context
- [ ] Voting/feedback uses `KbManagement.PublishingService.rateKnowledgeArticle`, not DML on vote stat objects
- [ ] Apex test classes cover empty-result scenarios and achieve 90%+ coverage
- [ ] Component tested in the actual target surface (guest preview for Experience Cloud, not admin preview)

---

## Salesforce-Specific Gotchas

Non-obvious platform behaviors that cause real production problems:

1. **No wire adapter for Knowledge content** — There is no platform-provided `@wire` adapter for Knowledge articles beyond `getRecord`. Developers who search LWC docs for a dedicated Knowledge wire adapter will not find one; all search and list retrieval must go through custom Apex.
2. **Guest user silently returns zero records** — When data category visibility is not configured for the Guest User profile, SOQL queries against `Knowledge__kav` return an empty list without throwing an exception. This masquerades as "no matching articles" when the real issue is a missing visibility grant.
3. **`WITH DATA CATEGORY` clause cannot be combined with all SOQL features** — `WITH DATA CATEGORY` is mutually exclusive with aggregate functions and certain subqueries. Attempting `SELECT COUNT(Id) FROM Knowledge__kav WITH DATA CATEGORY ...` throws a compile-time error.
4. **`KnowledgeArticleVoteStat` is read-only** — There is no DML path to insert or update vote records. The only supported method to record a vote is `KbManagement.PublishingService.rateKnowledgeArticle`. LLMs frequently generate `insert` or `upsert` statements against this object, which fail at runtime.
5. **Admin Experience Cloud preview bypasses sharing** — Testing a Knowledge LWC as a site administrator in Experience Builder preview does not replicate guest user sharing or category visibility. Articles that appear in admin preview can be invisible to actual guest users. Always test in an incognito browser session against the live or preview site URL.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| `KnowledgeArticleController.cls` | Apex class with `@AuraEnabled(cacheable=true)` retrieval methods and a non-cacheable voting method |
| `KnowledgeArticleControllerTest.cls` | Apex test class with happy path and empty-result coverage |
| `knowledgeArticleList/` | LWC bundle for search and list display of Knowledge articles |
| `knowledgeArticleDetail/` | LWC bundle for single article detail rendering |
| Setup checklist | Documented data category visibility and guest sharing configuration steps |

---

## Related Skills

- `admin/knowledge-setup` — Knowledge Settings, article types, data categories, and publishing workflows; required prerequisite before building LWC retrieval
- `lwc/experience-cloud-guest-access` — Broader Experience Cloud guest user sharing patterns beyond Knowledge
- `agentforce/einstein-copilot-for-service` — Einstein Article Recommendations and Copilot-driven article surfacing; distinct from custom LWC retrieval
