---
name: pricing-benchmark
description: Compare what a local business charges against its real competitors on a like-for-like unit — normalizing different bundles, labeling how every price was sourced, and handling the common case where competitors don't publish prices at all. Use when an owner asks "am I charging too little", "what does everyone else charge for a gel manicure", "can I raise prices", or a buyer asks "is this place priced right". Any US metro, via the free Brick & Mortar MCP server's pricing_benchmark tool.
---

# Pricing benchmark

**In the owner's words:** "Am I undercharging?" · "What does a 60-minute massage go for around
here?" · "Nobody posts prices — how do I know where I stand?"

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

`pricing_benchmark` — required `category` ("massage spa") and `city_metro` ("Wichita, KS");
optional `services` (`["30-min massage", "gel manicure"]`) to benchmark specific items —
otherwise the procedure derives a comparable bundle.

## What comes back, and the one way to get it wrong

This tool **fetches no data**. It returns a research framework with these keys:
`framework` (the method, named), `research_procedure` (numbered steps), `output_schema` (the
shape of the finished deliverable), `quality_rubric` (`good_looks_like`, `common_failure_modes`)
and `caveats`. **You execute the procedure with your own web search, then write the deliverable
in the `output_schema` shape and check it against the rubric.** Handing the framework back to
the user as though it were the finding is the failure this skill exists to prevent.

The method is two ladders scored for every price point. **Comparability:** define one
comparable unit in a sentence (price per minute, per ounce, base price with add-ons stripped)
and show the arithmetic for every conversion; anything that can't be converted goes in an
explicit exclusions list instead of being forced into the range. **Confidence:** label each
price by how it was found — published price list > booking/ordering platform > a dollar figure
in a review > review sentiment only — with its sample size and date.

Then: assemble the table, compute the range (and the subject business's position in it),
weighting the higher-confidence prices; re-check outliers for a conversion miss before reporting
them; and anchor the table against category price inflation (the nearest CPI item) and local
labour cost.

## Rules

- Fewer than ~4 businesses with real numbers is a **low-confidence read**, however clean the math.
- Flag anything older than ~12 months as possibly stale; say when a menu is undated.
- Public prices are list prices — happy hours, memberships and promos are invisible.
- A local CPI exists for only about two dozen metros; elsewhere the figure is a census-region
  aggregate and must be labeled as one.

## Finish

- Check the draft against `quality_rubric.common_failure_modes` before answering.
- State the `caveats` that applied. What public signal cannot show is part of the answer.
- Date-stamp anything that moves (ratings, review counts, prices, multiples).
- For a client-ready document, pass your finished write-up(s) to `compose_report`
  (`business_name`, `audience`: owner | broker | buyer | investor | general,
  `completed_analyses: [{tool, summary}]`). It returns the section order (verdict first), a
  contradiction ledger across analyses, and citation rules; you write the report. Pass your
  **finished** analysis as `summary`, never the raw framework.
