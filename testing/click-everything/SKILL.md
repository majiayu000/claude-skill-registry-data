---
name: click-everything
description: Test your app one module at a time by looking at it like a user does. Your agent lists every route from the router, screenshots every route and state, clicks the buttons, makes the app produce real output and reads it, fixes what doesn't make sense, adds replayable end-to-end tests, and reports. Use when you say "test every page", "/click-everything", "sweep the app", "visually test this module", or when there is no other work queued.
---

# Test every page

The instruction behind this skill, in short: when you run out of work, start visual testing. Find every route, child route and grandchild route. Screenshot them and judge whether they make sense. Click each button and check it does the right thing. Break it up by module: finish one module completely, add replayable end-to-end tests for it, fix every issue, report, then move to the next. **Only when there is no other work.**

It works for any app with routes or screens: a web app, an admin console, a desktop app, a mobile app (screens from its navigator instead of URLs).

## When to run this

**Only when the queue is empty**, or when the user asks for a sweep. It is the fallback, not a detour from real work. If there is a live defect, a user request or a roadmap item in flight, do that instead.

## The rule that makes this worth doing

**List routes from the router. Never type a route from what a screen is called.**

Guessed URLs come back 404 and get filed as product defects. Guessed table names produce false findings. A sweep that invents its own targets manufactures findings, which is worse than not sweeping. The same goes for tables and API paths: read the schema and the API folder, don't guess them.

Where the routes live, by stack: a file-based router's folder (`app/` or `pages/` in Next.js, Nuxt, SvelteKit, Remix), the route config (React Router, Vue Router, Angular), the server's route table (Rails `routes.rb`, Django `urls.py`, Express routers), or the navigator definitions on mobile (React Navigation stacks, Flutter routes, SwiftUI or Compose navigation).

## Use one harness

Find out if the project already has a crawler or a sweep script (search `scripts/`, `e2e/`, `tests/` for Playwright, Cypress, Puppeteer, Detox, Maestro). If it has one, use it and extend it. If it has none, write ONE, and keep it:

- It generates its route list from the router (the folder or config above), so the list is never kept by hand.
- It visits static routes, and dynamic routes filled with real ids found from the list pages' links.
- It clicks in-page states (tabs, sub-navigation, disclosures) and follows links breadth first.
- It runs a desktop pass and a mobile pass (for example 390x844).
- It is READ-ONLY: it never clicks Save, Delete, Run or Publish.

Never write a second crawler next to an existing one. Extend the one there is.

## Per-module procedure

1. **List.** Generate the module's routes from the router. Record the count: it is the denominator for the report.
2. **Crawl and screenshot** every route and every in-page state, desktop and mobile.
3. **Read every screenshot.** This is the part that cannot be automated away. Real defects are found by looking, not by assertions: raw JSON where a table belongs, a heading that contradicts its own query, a scope picker shown as if it were a project, a button pushed off screen by a flex child that can't shrink.
4. **Press the buttons** a user would press. Safe ones first (tabs, disclosures, filters, pagination). Destructive ones (Save, Delete, Run, Publish) only against a throwaway record you created for the purpose.
5. **Fix what does not make sense**, at the source. A heading that disagrees with its query is a code bug, not a copy bug.
6. **Add the end-to-end test** so the fix is replayable. Assert the CROSSING, not the sides: the thing that actually broke.
7. **Report** (below), then move to the next module.

## What counts as "does not make sense"

Treat each as a checklist item:

- **Raw JSON on screen** where a person must read data (`[{"id":1,…}]`, `{"columns":[…],"rows":[[…]]}`).
- **A heading that contradicts its query:** "for this pipeline" while filtering by another id; "All chats" showing only chats with *no* project.
- **Engineering words a user shouldn't see:** internal type names, raw ids, database, queue or vendor names. Keep a list and a check script for them if they keep coming back.
- **An empty state that is actually a bug:** "0 attached" while the data exists under a different scope. Check the database before believing an empty state, and check the QUERY before believing the database.
- **Placeholder content shown as real:** "sample query 3" where the record's own name belongs. Worse than empty: it averages meaningless rows into a score.
- **Layout:** content pushed outside its container (a flex child that can't shrink, `min-width: 0` missing), a narrow centered column wasting a wide screen, horizontal page scroll.
- **Duplicate entries** in a picker, usually a filter broader than its label (a "library" filter that really means "anything with no owner").
- **A score with no evidence behind it:** "3/3 passed" that cannot name the three rules.

## Report format

```
MODULE: <name>          routes <n> (static <a>, dynamic <b>)   states captured <c>
FIXED       defect → root cause → the assertion that now guards it
OPEN        defect → where it is → why it was not fixed
NEEDS OWNER decisions only a person can make (data, policy, ambiguity)
E2E         test files added, and what each one pins down
```

State the denominator. "Swept 23 of 23 Workspace routes" is evidence; "swept Workspace" is not.

If you want the user to see the screens, publish them with `show-me` and point at each problem with numbered marks.

## The verification standard

Verify as a principal UI and UX specialist with 20 years of building products for this app's users would: does this make sense, is it consistent, is it easy to understand, and is it the best experience? In a regulated or high-trust product (finance, health, insurance, enterprise), also ask whether a careful reviewer would trust it.

**This is a judgement, not a measurement.** The failure it corrects: checking the cheapest thing that plausibly goes with the goal, then reporting the GOAL as verified.

| What was checked | What was claimed | What was actually true |
|---|---|---|
| `grep -c min-w-0` | "the sheet is fixed" | The class was there; the sheet still looked wrong |
| `count(DISTINCT app_id) = 11` | "all apps have evals" | The rows existed; the screen showed "0 attached" |
| Add button's x ≤ viewport width | "fixed" | Inside the viewport, and still crude |
| `/signin` returned 200 | "deployed" | One route answered; a committed fix was never built |

Each of those is the same defect: a stand-in taking the place of evidence. A score with no cases behind it. A green gate that can't name its rules. "Sent" for mail that never left.

**So ask, of every screen, in this order:**
1. **Does it make sense?** Would the intended user know what this is for without being told?
2. **Is it consistent?** Same spacing, control heights, empty states and words as its siblings. Mismatched control heights read as broken before anyone reads a word.
3. **Is it easy to understand?** Is the main action obvious, and does every label mean what it says?
4. **Is it the best experience available?** Not merely "not broken". A working screen that looks crude is not done, especially where the UI is what earns trust.
5. **Would a careful reviewer trust it?** Placeholder data, an unexplained refusal, or a number with no evidence behind it loses trust faster than a missing feature.

A measurement can support this judgement. It can never replace it. "The button is inside the viewport" is not "this is a good panel".

## Honesty bar

Report the gate; never inflate it. A screenshot you did not read is not a verified screen, and a database count is not a verified screen either.

## The blind spot: routes are not output

A sweep can visit every route, screenshot every one, report the module done, and still miss what the user finds in a minute: say, a citation under a chat answer that names no document, shows an internal chunk index, claims 0% relevance for a source it is citing, and can't be clicked.

**It was never in a screenshot because it doesn't exist until a run produces it.** Route lists capture SHELLS: the page, its empty state, its panels. What a user actually reads and is asked to trust is GENERATED: an answer with citations, a run's step-by-step evidence, a compiled spec, a review's risk levels, an exported report, a sent email. A sweep that only visits URLs will pass a module whose whole output layer is wrong.

So a module is not swept until, for every surface that produces output, the sweep has **made real output exist and then read it**:

- Send a message that actually retrieves, and read the citations: names, links, scores.
- Run a job end to end, and read every step's evidence, not just the run list.
- Trigger the empty, the partial and the failed version. A failed read must never show as "no rows", and an unknown number must never show as `0`.
- Follow every link the output offers. A link that 404s, or points at an id of the wrong kind, is the same defect as no link. Check what kind of id a route expects before you link to it.

If a surface's output can't be produced in the sweep, list it in the report as an unswept surface. Don't let "all routes screenshotted" stand in for "the module works": that is the same stand-in-for-the-goal mistake as above, one level up.
