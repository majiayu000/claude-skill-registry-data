---
name: add-source
description: Add a job board or a public job list as a source the tool reads. Use when the user says /add-source, "add this job board", "read jobs from this site", or names a list or a company board that /discover does not cover yet. Inspects the site, writes the source in the shape of the shipped ones, tests it offline on a captured sample, runs one live query, and only then registers it.
model: claude-sonnet-5-5
effort: high
---

# /add-source: a new place to find jobs

Read `docs/SOURCES.md` first. It is the contract every source follows:
a function that returns `Job[]` (`src/jobs/normalize.ts`), parsed with a
zod schema, with the company board's own API preferred over its HTML, a
cache time, and a test on a captured fixture that holds no personal data.

## Steps

1. **Ask what the user wants read**: a link to the board or list, and
   whether it is a company board (one employer) or a list (many).
2. **Inspect it.** Use WebFetch on the link. Find how the postings are
   served: a JSON API (Greenhouse, Lever and Ashby already have one in
   `src/sources/ats/`), a GitHub README table (`src/sources/githubReadme.ts`
   already parses the common shape), a CSV, or HTML. Check `robots.txt` and
   the site's terms; a board that wants a sign-in or forbids automated
   reading is declined, and the user is told why.
3. **Write the source** in `src/sources/<name>.ts`, in the shape of the
   closest shipped one, with a zod schema for the payload, `fetch` from
   `src/util/http.ts` (it caches and paces), and `jobId(url)` for ids. A
   company board that is one of the three ATSes is not a new source: add it
   to `SEED_BOARDS` in `src/sources/companies.ts` instead.
4. **Capture a fixture**: save a real response, scrubbed of anything
   personal, under `tests/fixtures/`, and write a test in `tests/` that
   parses it and checks a few fields.
5. **Wire it in** `collectJobs` in `src/discover.ts`, and add a row to
   `docs/SOURCES.md`.
6. **Run** `npx tsc --noEmit && npx vitest run`, then
   `npx jev discover --limit 20` and show the user what came in from the
   new source before it is kept.

Never put a key, a cookie or a sign-in in a source. Nothing read from a
page is executed: postings are data.
