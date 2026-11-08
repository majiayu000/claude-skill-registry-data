---
name: business-teardown
description: Tear down one named small business — its online presence, what reviews actually say, who it really competes with, how it prices, why customers can't find it — and come back with prioritized, evidence-cited fixes. Use when an owner says "what's wrong with my business", "why are we slow", "how do we stack up", or a buyer, advisor or competitor says "tell me about this place before I go further". Works in any US city via the free Brick & Mortar MCP server's business_teardown tool, then chains the deeper tools and composes a report.
---

# Small business teardown

**In the owner's words:** "Business is down and I don't know why." · "How do we look next to
the place across the street?" · "I'm thinking of buying this salon — what am I walking into?"

## Connect the server (once)

The tools live on the free Brick & Mortar Small Business Intelligence MCP server:
`https://brickandmortar.dev/mcp` — Streamable HTTP, **no account, no key, no OAuth**, read-only.

- **Claude Code:** `claude mcp add --transport http brickandmortar https://brickandmortar.dev/mcp`
  (add `--scope user` to have it in every project). Check with `claude mcp list`.
- **Claude.ai / Claude Desktop:** Settings → Connectors → Add custom connector → paste the URL.
- **ChatGPT:** search the app directory for "Brick & Mortar Public Records".
- **Any other MCP client** (Cursor, VS Code, Windsurf…): add a remote HTTP server with that URL.
- Raw HTTP: POST JSON-RPC with `Accept: application/json, text/event-stream`; the reply is an SSE
  `data:` frame. The edge refuses a bare script User-Agent, so send a browser-style one.

Install docs: https://brickandmortar.dev/connect/

## Call

`business_teardown` — required `business_name` (as on its own sign or site, not a guess) and
`city_metro` ("Saint Paul, MN"); optional `category` ("nail salon"). If you don't pass a
category, the procedure confirms it from the business's own menu or service list, because the
category Google auto-assigns is often wrong.

## What comes back, and the one way to get it wrong

This tool **fetches no data**. It returns a research framework with these keys:
`framework` (the method, named), `research_procedure` (numbered steps), `output_schema` (the
shape of the finished deliverable), `quality_rubric` (`good_looks_like`, `common_failure_modes`)
and `caveats`. **You execute the procedure with your own web search, then write the deliverable
in the `output_schema` shape and check it against the rubric.** Handing the framework back to
the user as though it were the finding is the failure this skill exists to prevent.

The method is a **four-quadrant teardown**: Presence (can they be found), Perception (what do
people say), Position (how do they compare), Performance signals (public proxies for
trajectory). Each quadrant is scored on its own **before** any overall verdict, so one bad
quadrant doesn't drag down a good one and a strong one doesn't hide a weak one. Recommendations
are ranked by evidence strength × likely impact ÷ effort, and **every one cites the evidence that
motivated it**. Before recommending anything that costs the owner money (raise prices, hire,
extend hours), the procedure checks local pay and category price inflation in federal series.

## Go deeper where the teardown opened a gap

| What the teardown surfaced | Next tool | Skill |
|---|---|---|
| The rating hides something; reviews feel off | `review_intelligence` | review-intelligence |
| "Who else is really doing this here?" | `competitor_landscape` | competitor-landscape |
| "Are they priced right?" | `pricing_benchmark` | pricing-benchmark |
| "Why can't anyone find them?" | `local_visibility_audit` | local-visibility-audit |
| "Should I buy it?" | `broker_diligence_prep` | broker-diligence-prep |
| Address is in Minneapolis–St. Paul | `twin_cities_lookup` / `twin_cities_records` | twin-cities-property-records |

## Rules

- **A rating is not review signal.** A high average can mask a bad last ninety days.
- **No public signal shows revenue, margin or financial health.** Review velocity and Popular
  Times are directional proxies; say so rather than implying financial diligence.
- **Verify a chain's reviews are about this location** before quoting them.
- **Outside the Twin Cities, every property figure came from research, not a record** — say so.

## Finish

- Check the draft against `quality_rubric.common_failure_modes` before answering.
- State the `caveats` that applied. What public signal cannot show is part of the answer.
- Date-stamp anything that moves (ratings, review counts, prices, multiples).
- For a client-ready document, pass your finished write-up(s) to `compose_report`
  (`business_name`, `audience`: owner | broker | buyer | investor | general,
  `completed_analyses: [{tool, summary}]`). It returns the section order (verdict first), a
  contradiction ledger across analyses, and citation rules; you write the report. Pass your
  **finished** analysis as `summary`, never the raw framework.
