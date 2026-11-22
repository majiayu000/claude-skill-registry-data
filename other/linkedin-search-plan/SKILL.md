---
name: linkedin-search-plan
description: Translate a job-search brief into focused role and location queries, ordinary LinkedIn search links and a bounded Scout search proposal. Use when the user wants to plan or improve a LinkedIn job search, rather than evaluate a particular vacancy.
---
# LinkedIn Search Plan

Use the user's existing brief. If none exists, collect the target role and geography and only the missing preferences that change results. A CV is optional for query planning. Keep desired role titles separate from skills, exclusions and logistics; do not combine every preference into an overly narrow query.

Propose a small useful set of primary title queries and evidence-backed synonyms. Explain why an adjacent title is included. Keep location text unambiguous, such as `United Kingdom` rather than `UK`. Country-wide remote is a work mode, not proof of permission to work remotely from any country.

For manual LinkedIn browsing, generate ordinary job-search URLs using URL-encoded keywords and location:

`https://www.linkedin.com/jobs/search/?keywords=Product%20Analyst&location=Berlin`

These are navigation aids, not discovered vacancies. Prefer the user setting other filters in LinkedIn over claiming undocumented URL parameters are stable. Do not automate a browser, retrieve cookies or ask for LinkedIn credentials.

If Scout is connected, inspect `get_scout_status` and `prepare_search` schemas. Use `prepare_search(brief, source)` to validate and store the plan. Its current brief supports `target_titles`, `locations`, `workplace`, `posted_within`, `easy_apply_only`, `max_results` and `max_charge_usd`. Easy Apply defaults to false: ordinary research should include external-application roles too. Do not add unsupported filters such as company headcount or salary to the tool call; retain them as later review criteria.

Describe the source, search criteria, maximum results and run-charge cap in the conversation before any live search. Preparing the plan itself makes no paid call. Use the user's own configured Apify account; credentials are not tool arguments or chat content. When the user requested only a plan, stop at the plan. When the user already requested a bounded search, continue within that scope after making the caps visible; do not turn every routine step into another confirmation request.

For a demo, select source `demo` explicitly and describe the output as synthetic. Without Scout, provide the searches directly in chat and explain that the plan has not queried current listings. A plan, a search link and an observed vacancy are distinct outputs.
