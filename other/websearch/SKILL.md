---
name: websearch
description: Search the web for evidence using the available Exa tools. Prefer concise results and stop when the question is answered.
argument-hint: "<query> [--deep|--code|--docs|--debug|--news|--compare|--research|--similar] [filters]"
---

# Web search

Use the live Exa tool schemas, not remembered parameter names. Quick lookup:
one focused search, then answer with citations. Documentation: find the
official page and crawl the relevant section only. Code/debug: use code
context, then broaden only when the first results do not answer the issue.
News: preserve publication dates. Compare: search the actual alternatives.
Research/similar: use supported search parameters; never invent an enum value.

Honor --domain/--exclude, --after/--before, -n, --fresh and requested output
format when the tool supports them; explain unsupported filters. Prefer
short relevant excerpts, not full pages. Crawl a full passage when needed
to verify a key claim. Do not paste raw response metadata twice.

--deep permits targeted follow-ups for named remaining gaps, up to three
passes including the initial search. Stop sooner when answered, saturated or
no new useful evidence appears. No fixed quota of queries or sources. Run
independent tool calls together without launching agents for simple lookups.

Cite each source that supports a claim; distinguish observed facts, inference
and uncertainty. Keep dates honest. Write a report only with --save or an
explicit request. --json returns structured results. --info uses the existing
references/info-text.md.

## Execution policy

Work solo. Ask before any subagent or reviewer, even in auto mode. Explain
the independent scope and expected benefit first. No hidden advisor, nested
delegation, model retuning, repeated successful checks, or progress spam.
Use existing context before asking questions. Stop when the requested result
is delivered. User stops and scope changes override pending steps.
