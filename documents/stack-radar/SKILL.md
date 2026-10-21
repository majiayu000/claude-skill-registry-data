---
name: stack-radar
description: Count the technologies my postings ask for, compare with the CV, and save the tags to add and a learning plan per gap.
disable-model-invocation: true
---

# /stack-radar

Files: `templates/`, `scripts/`, `docs/`, `examples/` and `routines/` are in the method root, `${CLAUDE_PLUGIN_ROOT}` (the clone holding this skill when that is not replaced by a path); every other relative path is in the workspace, the current folder. Before acting on the person's behalf, read `profile.md`, `docs/rules.md` and the workspace `rules.md`; the workspace one wins on conflict.

Arguments: `/stack-radar` (last 90 days, target role from `profile.md`), `/stack-radar 180d`, `/stack-radar backfill` (see below).

## 1. Collect

- `list_applications` with `range` = the window, statuses `applied`, `screening`, `interview`, `rejected`. Keep those whose role matches the profile's target roles (loose title match).
- For each, `get_application` and take its `requirements` list and, if present, the description. JobCubby rate-limits per minute; pace the loop, and tell the person how many applications are being read.
- Also read `get_job_stats` for each of the profile's main technologies for market-wide counts and median salary.

## 2. Normalize

Map every spelling to one canonical name before counting, the one the CV uses (TypeScript, Node.js, PostgreSQL, Kubernetes). Counting rules:

- `Next` counts as Next.js only inside a list of technologies.
- Nuxt counts for Vue and on its own line.
- AngularJS is its own line, apart from Angular.
- Apollo counts for GraphQL and on its own line.
- LangChain, LangGraph, OpenAI API, Anthropic API and MCP each count on their own line and together as LLM tooling.

Spellings met that are not obvious go into the report's Aliases section; read the Aliases section of the latest `reports/stack-radar-<date>.md` before counting.

Drop non-technologies (Agile, Scrum, "team player"). Keep tools that postings treat as skills (Figma, Jira) in a separate "tools" group.

## 3. Compare

Read the Technical Skills section of the chosen CV version (`cv/base.md` unless told otherwise). Produce one table:

| Technology | Share of postings | In CV | Action |
|---|---|---|---|

Share = postings mentioning it divided by postings read. Sort by share. Action is one of: `keep`, `add tag`, `move up` (asked for more than its position in the CV suggests), `learn then add`.

Split the proposals:

- **Add now.** Things they have used, even lightly, that are missing or spelled differently. Propose the exact tag and which skills line it goes on.
- **Learn, then add.** For each, a plan: what it is in two lines, the smallest real thing to build with it (two or three hours), what an interviewer asks about it, and the suggested tag wording once done.

Show the table, the two lists, and the market stats (postings and median salary for the main stack). Ask the person, tag by tag, whether they can discuss each "Add now" tag on a call; only a yes makes it confirmed.

## 4. Save

Write `reports/stack-radar-<YYYY-MM-DD>.md`: the table, the market stats, "Add now" with each tag marked confirmed or not, the learning plans, and Aliases. Done when the file exists with every "Add now" tag marked.

Then tell the person: `/cv` adds the confirmed tags to the CV, which needs approving again before `/profiles` takes them to any platform. A learned technology becomes confirmed when the person says they finished its plan; mark it in that report.

## Backfill

`/stack-radar backfill` takes every application in the window with an empty requirements list, opens its posting URL in the Playwright browser, reads the description if the posting is still live, extracts the technologies, and writes them back with `update_application` (requirements, and description if it was empty). Dead postings are skipped with a count. Pace to the rate limit.
