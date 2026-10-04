---
name: find-all
description: Write "Find all..." and query the public web like a database. Returns structured rows with a source URL under every single field, routed through Bright Data's indexed datasets when one covers the entity and through live multi-query search when none does. Triggers on "find all", "list every", "who are all the", "build me a table of", "which companies/people/products", or /find-all.
---

# Find All

You describe rows. The skill returns rows.

`Find all Series B fintechs in Germany hiring a Head of Compliance` is a database query written in English. The public web holds the answer, spread across company pages, job boards, funding records and profiles. This turns that into a table.

**Never fill a cell from memory.** A plausible table with invented cells is worse than a short honest one, because nobody can tell which half is real.

## Before you start

This skill needs the Bright Data MCP connected. If no Bright Data tools are available, stop and say so in one line, with the setup link: https://brdta.com/toolmonsters (free tier, 5,000 requests a month, no credit card). Do not fall back to memory or to another search tool.

## The two moves that make this sharp

**Use the database when a database exists.** Most "find all companies" tools pull links out of search results, which is slow, lossy and stops at whatever page one gave you. Bright Data ships indexed datasets for companies and people that take real filters and paginate. For those two entity types, this skill queries the index and gets thousands of matches with a filter tree, instead of ten links. For everything else it falls back to live multi-query search. Knowing which mode a request belongs to is most of the skill.

**One source per field, not one source per row.** The failure mode of "the web as a database" is a beautiful table where the model quietly filled the gaps. Attaching a URL to each individual cell makes that impossible to hide: a cell either carries the page it came from or it stays empty. Empty cells are the honesty mechanism, not a defect.

## Routing

Decide the mode before spending anything.

| The rows are... | Mode | Tools |
|---|---|---|
| Companies | **Indexed** | `search_dataset` on `gd_l1vikfnt1wgvvqz95w` |
| People | **Indexed** | `search_dataset` on `gd_l1viktl72bvl7bjuj0` |
| Anything else (products, tools, venues, papers, grants, events, announcements) | **Live** | `search_engine_batch` + `scrape_batch` |
| A known platform appears in the row (Amazon listing, Crunchbase page, job listing, Reddit thread, YouTube video) | **Enrich** | the matching `web_data_*` tool, per row |

Indexed mode is faster, deeper and cheaper. Live mode is the only option for everything the datasets do not cover, which is most of the world.

**If `search_dataset` is not among your tools**, the connector was added without the dataset tools. Run the request in live mode, say so in the coverage line, and tell the user they can add `&tools=search_dataset,list_dataset_fields` to their Bright Data connector URL.

## Indexed mode

Call `list_dataset_fields` first. Field names are not guessable.

Filter is a tree: a group `{operator:"and"|"or", filters:[...]}` or a leaf `{name, value, operator}`, max depth 3. Leaf operators: `=`, `!=`, `<`, `<=`, `>`, `>=`, `in`, `not_in`, `includes`, `not_includes`, `array_includes`, `not_array_includes`, `is_null`, `is_not_null`. Use `includes` on text fields holding lists such as `industries`, `=` on exact values such as `country_code`.

**Every `search_dataset` call runs in a subagent** when subagents are available. Measured: 3 records returned 121,362 characters, 10 records returned 374,874. There is no `fields` parameter to trim the response, so calling it directly destroys the working context before any table gets built. The subagent runs the query and returns only the requested columns.

**Where subagents are not available** (for example in the Claude apps), request at most 3 records per call, write down only the requested columns and their sources right after each call, and never hold raw records across calls.

Page size is capped at 10. Paginate with `search_after`.

**Joining companies to people:** the key is the company's `id` (the slug, `acd-groupe`), not its numeric `company_id` (`10021965`). The people dataset's `current_company_company_id` holds the slug. Verified: the numeric ID returns 0 hits, the slug `google` returns 334,377. The wrong key returns an empty list rather than an error, so it reads like the company has no employees.

## Live mode

1. **Decompose.** Turn one request into 5 to 10 distinct queries that attack from different angles: by category, by attribute, by adjacent term, by "list of" and "best" phrasings, by the year, by licence or price or whatever the columns demand. `search_engine_batch` runs 10 at once and each angle surfaces rows the others miss.
2. **Read.** `scrape_batch` pulls up to 10 pages per call. Read the pages, do not summarize the snippets. Snippets are truncated and drafting from them invents facts.
3. **Dedupe on the entity, not the URL.** The same company appears on five listicles. Merge to one row and keep every source.
4. **Check claims at the source.** Roundups and trackers are for finding candidates, not for filling cells. When a row depends on what a company said, find the company's own statement or a report quoting it. If the only support is an anonymous source, a reporter's framing or a roundup, reject the row and say why.

**Do not call `discover`.** In our runs it returned **HTTP 410 Gone**, on a bare one-parameter call as well as a full one. `search_engine_batch` with several well-chosen angles covers the same ground.

**Live reads are a context bomb too.** A `scrape_batch` of 3 GitHub repository pages returned 83,254 characters. Any multi-page read runs in a subagent that returns extracted fields, never raw pages. Without subagents, read at most 3 pages per call and extract immediately.

**Do not use the `site:` operator.** Verified: `site:reddit.com <query>` returned zero results on this search tool while the same question in plain language returned four real pages. Write queries the way a person would type them.

## Building the table

- **The user names the columns.** If they did not, propose them and confirm before spending requests.
- **Every filled cell carries the URL it came from.** In a rendered table, footnote them. In CSV or JSON, use a parallel `_source` field per column.
- **Unknown stays blank.** Never "N/A", never a guess, never a range you inferred. Blank is a finding: it says the public web does not say.
- **Conflicts get both values.** When two sources disagree, show both with their sources rather than picking. This happens constantly on headcount and funding.
- **Rejected rows are listed.** When a candidate fails the request (wrong date, wrong reason, unverifiable claim), put it in a REJECTED section with a one-line reason. This is often what the user needed most.
- **Stamp the date.** Every row is a snapshot of the day it was collected.

## Coverage, and saying so honestly

This is the part most tools skip, and it is the part that makes the output trustworthy.

**The datasets are a sample, not a census.** Filtering the people dataset for one senior title across the entire United States returned 56 records. The real number is in the thousands. A result count is never a market size.

**Live mode is bounded by what search surfaced.** Ten queries is ten angles, not the whole web.

Every output ends with a coverage line naming what was searched, how many rows survived, and what was not covered or failed to load. If the user asked for "all" and you returned 40, the output says these are the 40 found, not that 40 exist.

## Known data traps

Carried from real runs, not from the docs.

- **The two headcount fields contradict each other.** In one 10-record query, 8 records disagreed with themselves, including `employees_in_linkedin: 423` against `company_size: "5,001-10,000 employees"`. Show both, never average, never pick.
- **`updates[].title` is not the post.** It holds only the company's own name. The post body is in `updates[].text`, alongside `date`, `likes_count` and `post_url`.
- **`additional_information` is not open roles.** It returns global job counts. Real hiring comes from `web_data_linkedin_job_listings`.
- **`timestamp` arrives in two formats in the same field**, epoch milliseconds and ISO strings. Handle both or half your dates break.
- **Null funding means unknown**, never unfunded.
- **`position` is free text and often holds a bio.** One profile listed "Graduate of Biola University | Editor, Director, Filmmaker" as its position. The filter matches the string, not the seniority.
- **Bright Data returns no email addresses.** No field carries one, and the contact-enriched people dataset returns a 404. A Find All row never carries an inbox.
- **"AI" roundups overclaim.** In a run on 2026 layoffs attributed to AI, most names on the lists failed at the source: cuts in other functions, other years, anonymous attribution, or companies that said outright that AI was not the reason.

## The output

```
Find All: "Series B fintechs in Germany hiring a Head of Compliance"
Indexed mode · 3 dataset pages · checked 2026-08-18
1,294 matched the filter · 40 returned · 5 columns

| Company     | HQ       | Headcount | Last round           | Compliance role open |
| Northwind   | Berlin   | 340 ¹ ²   | Series B, Mar 2026 ³ | Yes ⁴                |
| Kalder      | Munich   | 610 ¹     |                      | Yes ⁴                |
| Vasari      | Hamburg  | 210 ¹     | Series B, Nov 2025 ³ |                      |

¹ company dataset record  ² company_size reads "201-500", conflicts with 340
³ crunchbase.com/organization/northwind  ⁴ job listing URL

BLANKS
Kalder last round: no public funding record found.
Vasari compliance role: no matching listing found.

REJECTED
(rows that looked like matches and failed, with the reason)

COVERAGE
Filtered on industry, country and headcount. This is what the dataset holds,
not the whole German fintech market. Records last collected 2025-11 to 2026-08.
```

The blanks section is not padding. It tells the reader exactly where the web went quiet, which is often the most useful line in the table.

## Good to know

**Ask for fewer columns than you want.** Every extra column is another field to source. A five-column table with real sources beats a twelve-column table half full of blanks.

**"Find all X that recently Y" is the strongest shape.** Recency narrows the set enough that the sources stay findable, and a recent event is usually the reason you are asking.

**Re-run it later and diff.** The same query a month on shows who entered, who left, and what changed. The diff is usually the point.

**Export it.** Rows are meant to leave. Offer CSV or JSON with the parallel source columns intact.

## What this skill does NOT do

- Use any MCP other than Bright Data. It is fully self-contained.
- Fill a cell without a source. Blank is the honest answer.
- Claim the result is exhaustive. Every output states its coverage.
- Hold raw dataset records or raw pages in the main context.
- Use the `site:` operator. It returns nothing on this search tool.
- Return email addresses. Bright Data does not have them.
- Resolve conflicts by picking a side. Both values ship, with both sources.
