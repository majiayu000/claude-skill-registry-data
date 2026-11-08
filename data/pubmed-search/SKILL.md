---
name: pubmed-search
description: Build, run, and review PubMed literature searches. Use when someone asks for studies, papers, evidence, citations, or a literature search on a biomedical or health topic, or asks to improve a PubMed query.
license: GPL-3.0-or-later
compatibility: "Works everywhere for query preparation. Live search needs one of these: the PubMed connector in Claude, the bundled E-utilities API plugin in Microsoft 365 Copilot, an MCP server you supply in ChatGPT, or Python 3 with network access in a coding agent."
metadata:
  agentprise-kind: skill
---

# PubMed Search

## Purpose

Help people find biomedical and health literature in PubMed. Turn a plain-language question into a careful Boolean search, run it when a PubMed tool is available, and review what comes back without overstating it.

PubMed is the National Library of Medicine (NLM) citation database. It holds citations and, for many records, abstracts. It does not hold most full texts.

## Always say which mode you are in

This skill has three modes. Every reply that contains a search, a result, or a review starts with one of these labels, exactly as written:

| Mode | Label | When |
|---|---|---|
| Query preparation | **Prepared search strategy (not executed)** | No PubMed tool returned results in this conversation. |
| Live search | **Search completed on <date>** | A PubMed tool returned results in this conversation. Use the retrieval date in YYYY-MM-DD form. |
| Live search, web route | **Web discovery** | Records came from a general or site-scoped web search, not from a PubMed query. |
| Abstract review | **Abstract review** | You are reading abstracts that a tool returned or the person pasted. Keep the search label above it as well. |

Never use "Search completed" unless a tool actually ran the query and returned a count or a list of PMIDs (PubMed identifiers) in this conversation. Writing a query is not running it. A web search is not a PubMed search.

## Mode 1: Query preparation

This mode works with no tool at all. Use it whenever no PubMed tool is available, when a tool call fails, or when the person only wants a query.

### Steps

1. **Clarify the question.** Find the population or setting, the main concepts, outcomes if any, date range, language, and how broad the person wants to go. Ask at most two short questions if the answer would change the query. Otherwise state your assumptions and continue.
2. **Split the question into concept blocks.** Most searches need two or three blocks, for example "device" AND "condition". Do not add a block for every word in the question; each extra AND block removes records.
3. **Fill each block with synonyms joined by OR.** For each concept, combine:
   - a MeSH (Medical Subject Headings) term tagged `[mh]`, when a suitable one exists;
   - text words tagged `[tw]` or `[tiab]` for the plain words authors use, spelling variants, brand names, and plurals;
   - truncation with `*` where it helps, keeping at least four letters before the asterisk.
4. **Join the blocks with AND** and wrap each block in parentheses.
5. **Add filters only when asked or clearly needed:** dates `[dp]`, language `[la]`, publication type `[pt]`, species, or an affiliation `[ad]`. Each filter can drop relevant records, so say so once when you add one.
6. **Check the query before you show it.** Go through the checklist below.
7. **Explain the main choices in two or three sentences:** what each block covers, and any trade-off between finding everything and finding only relevant records.
8. **Output the query and a PubMed link** in the format below.

### Pre-flight checklist

- Boolean operators are in capital letters: `AND`, `OR`, `NOT`. A lowercase "and" or "or" is searched as a word.
- Parentheses are balanced, and each OR group sits inside its own parentheses.
- Every term that needs a field tag has its own tag. `covid-19[ti] vaccine[ti]` tags two terms; `covid-19 vaccine[ti]` searches a phrase.
- Phrases use straight double quotes (`"`), not curly quotes. Replace any curly quotes the person pasted.
- No truncated stem is shorter than four letters before the `*`. PubMed silently drops a shorter wildcard and searches the bare letters instead.
- Truncation and quoted phrases turn off automatic term mapping. Where the concept has a MeSH term, add the MeSH term as a separate OR term so indexed records are still found.
- When you want one exact MeSH heading, put it in quotes, for example `"wearable electronic devices"[mh]`. Quotes stop PubMed from mapping the tagged term to other MeSH headings.
- No private information is in the query. Never put names, record numbers, or other details about a real person into a search; the query is sent to an outside service.

### Output format

Use this structure:

```
**Prepared search strategy (not executed)**

Question: <one line, in the person's words or a close restatement>

Query (paste into PubMed):
<the full query on one line, in a code block>

Run it in PubMed: <link>

Why this query: <two or three sentences>

Not run yet: I have not run this search, so I cannot tell you how many results it returns.
```

Build the link as `https://pubmed.ncbi.nlm.nih.gov/?term=<url-encoded query>`. Encode the query so it survives in a link: spaces become `+`, `"` becomes `%22`, `[` becomes `%5B`, `]` becomes `%5D`, `(` becomes `%28`, `)` becomes `%29`, and `#` becomes `%23`. Example:

- Query: `"smart ring*"[tw] AND sleep[mh]`
- Link: `https://pubmed.ncbi.nlm.nih.gov/?term=%22smart+ring*%22%5Btw%5D+AND+sleep%5Bmh%5D`

Browsers limit link length. For a very long query, still give the link, and tell the person that if it does not open correctly they can paste the query into the PubMed search box instead.

### When the person pastes results back

If the person runs the query and pastes the result count, the Search Details from PubMed's Advanced Search page, or a page of results, revise the query:

- Too many results: narrow with a `[ti]` tag instead of `[tw]`, a major-topic tag `[majr]`, a date range, or another concept block.
- Too few results: drop the narrowest block, add synonyms, switch `[ti]` to `[tiab]` or `[tw]`, or add the MeSH term.
- Odd translation: see "Read the query translation" in references/pubmed-syntax-guide.md.

Keep the "Prepared search strategy (not executed)" label on every revised query until a tool runs it. The count the person reports is theirs; you may repeat it and say they reported it.

## Mode 2: Live search

Use this mode only when a PubMed tool listed in the "Tools available in this setup" section, or a PubMed connector in the conversation, actually returned results. Use the first route that works. If every route fails, switch to query preparation and say in one sentence why, for example "The PubMed tool is not reachable from this workspace, so here is a query you can run yourself."

### What to send

1. Prepare the query exactly as in Mode 1, including the pre-flight checklist.
2. Send that exact query. Do not let the tool rewrite it without saying so.
3. Ask for 20 records by default. Ask for more only when the person needs them, and never more than 100 in one call.
4. Then fetch summaries (title, authors, journal, date) for the PMIDs you will show. Fetch in groups of 20 or fewer.

### What to record

Record all of these, every time, and show them in a short "Search record" block under the results:

- **Query sent:** the exact string, character for character.
- **Date:** the retrieval date (YYYY-MM-DD).
- **Tool:** which tool ran it, for example "PubMed connector" or "scripts/pubmed.py".
- **Filters and settings:** date limits, language, publication types, sort order, and how many records you asked for.
- **Result count:** the total number PubMed reported, not just the number you displayed.
- **PMIDs returned:** the list of PMIDs the tool gave back, in order.
- **Query translation:** how PubMed translated the query, when the tool reports it.
- **Warnings and errors:** anything PubMed reported, such as phrases not found, quoted phrases not found, or "No items found."

### Check the translation before you trust the count

Compare the query translation with what you meant:

- A quoted phrase listed as "not found" was searched as separate words. Say so, and consider a proximity search or different wording.
- A term listed as "not found" matched nothing.
- PubMed may not flag a made-up field tag; in testing it kept the unknown tag in the translation without a warning. If a tagged term appears unchanged in the translation, check the tag against references/pubmed-syntax-guide.md.
- A truncated stem that shows up without its `*` was too short to truncate.

If something is wrong, fix the query, run it again, and record both runs.

### Output format

```
**Search completed on <YYYY-MM-DD>**

<one or two sentences: what was searched and the total count>

<numbered list of records: title, first author, journal, year, PMID, link https://pubmed.ncbi.nlm.nih.gov/<PMID>/>

Search record:
- Query sent: ...
- Date: ...
- Tool: ...
- Filters and settings: ...
- Result count: ...
- PMIDs returned: ...
- Query translation: ...
- Warnings: ... (or "none reported")
```

List only records the tool actually returned, with the details the tool gave. Never fill in a title, author, year, or DOI from memory. If summaries could not be fetched, list the PMIDs with their links and say that titles were not retrieved.

### Web discovery

Some setups can only run a web search scoped to pubmed.ncbi.nlm.nih.gov. Results from that route:

- carry the label **Web discovery**, never "Search completed";
- have no result count and no query translation, so do not report either;
- may be incomplete or out of date, so say that once;
- should come with a prepared query (Mode 1) the person can run in PubMed for a reproducible search.

## Mode 3: Abstract review

Use this mode when abstracts are available, either from a tool in this conversation or pasted by the person.

1. **Mark every record** as one of:
   - **abstract-read**: you read the abstract text in this conversation;
   - **metadata-only**: you saw only the title, authors, journal, or date.
2. **Draw conclusions only from abstracts you have read.** Never describe a study's methods, sample, or findings from its title alone. A citation that appeared in search results is not evidence for what the study found.
3. **Say when a claim needs the full text.** Abstracts often leave out effect sizes, subgroups, harms, and limitations. When an answer depends on those, say that the full text needs to be checked.
4. **Keep quotation short.** PubMed abstracts may be protected by copyright. Summarize in your own words and quote only a short phrase when exact wording matters.
5. **Keep the search label.** An abstract review of live results sits under "Search completed on <date>". A review of pasted abstracts sits under "Prepared search strategy (not executed)" or states that the abstracts were supplied by the person.

A simple review table works well:

| PMID | Status | Design (from abstract) | Main finding (from abstract) | Needs full text for |
|---|---|---|---|---|

## Systematic reviews and other formal reviews

If the person mentions a systematic review, scoping review, meta-analysis, umbrella review, clinical guideline, or wants a search that finds "everything", recommend that a health sciences librarian or informationist review the search strategy before it is used. Give this recommendation once, early, in plain words. Then still help: prepare the best query you can, label it, and note that a formal review usually searches more than one database and documents every search. Never describe your search as exhaustive or complete.

## Tools

The "Tools available in this setup" section, when present, lists the PubMed routes for this product in order of preference. Use the first one that is available in the conversation. Common routes:

- **A PubMed connector** (for example in Claude): use its search, metadata, and abstract tools directly.
- **The bundled script** `scripts/pubmed.py`: needs Python 3, network access to eutils.ncbi.nlm.nih.gov, and the `NCBI_EMAIL` environment variable. Commands:
  - `python3 scripts/pubmed.py search --query '<query>' --retmax 20`
  - `python3 scripts/pubmed.py summary --ids 12345678,23456789`
  - `python3 scripts/pubmed.py abstract --ids 12345678,23456789`
  Each prints one JSON object. If it exits with an error, read the message, and fall back to query preparation if the network call failed.
- **The bundled API plugin** `openapi/pubmed-eutils.yaml` (for example in Microsoft 365 Copilot): operations `searchPubMed`, `getSummaries`, and `getAbstracts`.
- **An MCP server named "pubmed"** that the person or their organization supplies (for example in ChatGPT).

If none of these is available, use query preparation. Never imply that a tool ran when it did not.

## Reference files

Read these when you need them:

- references/pubmed-syntax-guide.md: Boolean logic, quotes, truncation, field tags, automatic term mapping, MeSH explosion, common filters, and how to read the query translation. Read it before writing any non-trivial query.
- references/mobile-tech-search-blocks.md: tested search blocks for mobile health technology, devices, and domains such as sleep and cardiovascular health, from the University of Michigan Mobile Tech Publication Search Starter Kit. Use these blocks when the question is about wearables, smartphones, or other mobile devices.
- references/query-test-cases.md: example questions with the queries this skill should produce. Use them as models.

## Quick rules

- Say which mode you are in, with the exact label.
- Never claim a search ran unless a tool returned results in this conversation.
- Record the exact query, date, filters, count, PMIDs, translation, and warnings for every live search.
- Mark each record as abstract-read or metadata-only, and draw conclusions only from abstracts you read.
- Recommend a librarian review before a search is used for a systematic review.
- Never put private information about a person into a search.
