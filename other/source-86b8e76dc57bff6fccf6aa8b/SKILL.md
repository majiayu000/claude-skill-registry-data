---
name: industry-benchmark
description: benchmark the user's CONNECTED QuickBooks company against industry peers using their QuickBooks financial data. Use only when the numbers come from the user's connected QuickBooks account — "how does my business compare to similar businesses", "are my margins healthy", "am I spending too much", "benchmark my QuickBooks company". Do NOT use for industry research, for questions about which industries are most profitable in a location, for expected profit for a business type, or when the user supplies their own figures — those are answered by the Intuit QuickBooks benchmarking tools directly.
---

# Industry Benchmark

## Goal
Turn a question about the user's connected QuickBooks company into a concise benchmark briefing by first confirming the user's benchmark choices, then pulling the company's figures from QuickBooks, and explaining whether the business is ahead, behind, or in line with regional peers.

## When not to use this skill
This skill covers only the user's connected QuickBooks company. Do not use it — and do not run the pre-flight — when the user asks about industries generally, about expected profit for a business type, about which industries are most profitable in a location, or when the user supplies their own metric value instead of using QuickBooks data. Those requests are served by the `benchmarking_against_industry` tool, which renders its own widget. Let that tool handle them.

## Pre-flight input
Always run this pre-flight before calling any Intuit QuickBooks tool. Run it even when the user's message already states a metric, period, industry, or location, and even when every value can be inferred confidently. Being able to infer a value is a reason to pre-fill it, never a reason to skip the pre-flight.

Pre-fill the message with everything you can infer from the user's request and from the defaults below, then ask the user to confirm or correct it. The goal is one short confirmation step, not an interrogation — do not ask the user to supply values you already have.

Do not call a benchmarking tool until the user has confirmed, corrected, or explicitly told you to proceed with the defaults.

Ask for these inputs in one concise message:

1. Confirm the benchmark is for the connected QuickBooks company, using its QuickBooks profile and financial data.
2. Metric:
   - Profit, revenue/income, expenses, or profit margin (%).
   - Propose profit if the user has not stated a metric. Show it as the pre-filled choice; do not adopt it silently.
3. Aggregation period:
   - Yearly, monthly, or quarterly.
   - Propose yearly if the user has not stated a period. Show it as the pre-filled choice; do not adopt it silently.
4. Industry:
   - Use the company profile industry when available. If only the NAICS code is known at this preflight step, refer to it as the company's QuickBooks industry category instead of displaying the code.
   - If the profile has no industry, ask for it and, when known, the NAICS code.
5. Location:
   - Ask for state, and county when the user wants a more local comparison.
   - Use a two-letter state code when calling tools.
Do not mention PDF generation in the initial prompt.

## Default assumptions
These are the values used to pre-fill the pre-flight message. They are what you propose to the user, not what you run on. None of them authorises skipping the pre-flight.

- Treat "my business", "my company", and "our business" as the connected QuickBooks company.
- Proposed metric is profit.
- Proposed aggregation period is yearly.
- Use the company's profile industry and location when available. Where industry, NAICS code or state cannot be read from the profile, ask for them in the same pre-flight message rather than as a separate follow-up.
- Keep the answer plain-language, business-owner friendly, and focused on decision usefulness.

## Tool sequence for QuickBooks benchmark data
Use the tools exposed by the Intuit QuickBooks app connector.

Always use the text-only variants of the Intuit QuickBooks benchmarking tools listed below. These return plain text/markdown so you can synthesize the benchmark briefing yourself without rendering interactive widgets.

After the user confirms the plan:

1. For Connected QuickBooks company mode:
   - Call the Intuit QuickBooks `company_info` tool first to establish the QuickBooks connection.
   - Call `benchmarking_quickbooks_account_text` for the selected metric and aggregation period.
   - When the selected metric is `profit`, also make a second call to `benchmarking_quickbooks_account_text` with `metricType=margin` to fetch peer margin data. Include the margin values as a row in `keyNumbers`.
   - If the company profile is missing required industry, location, or NAICS information and the tool asks for it, collect only the missing information and continue.
2. Never call `benchmarking_against_industry` or `benchmarking_against_industry_text` from this skill. Those tools serve industry research and user-supplied figures, which are out of scope here.
3. If a tool is unavailable, returns incomplete data, appears to provide only a UI without enough structured values, or authentication/profile setup blocks the benchmark, explain the gap briefly and continue with the information that succeeded. Do not invent missing numbers.

## Parameter mapping
- "How do I compare to other businesses like mine?" -> in scope; benchmark the connected company.
- "Are my margins healthy?" -> in scope; use metricType `margin` — the tool fetches profit and revenue automatically.
- "Am I spending too much?" -> in scope; benchmark expenses.
- "What should my profit look like for a restaurant in Texas?" -> OUT OF SCOPE. Industry research — let `benchmarking_against_industry` answer it.
- "I made $50K profit in my restaurant in Austin" -> OUT OF SCOPE. The user supplied the figure — let `benchmarking_against_industry` answer it.
- Monthly, quarterly, or annual wording maps to the corresponding aggregation period.

## Synthesis rules
Build a single integrated benchmark briefing instead of listing raw tool output.

Always include the benchmark context near the top of the briefing:
- Company name or research label.
- Benchmark mode.
- Metric and aggregation period.
- Industry and NAICS code when available.
- Region used for the benchmark.
- Whether regional peer comparison was available.

Prioritize these signals:
- Peer position: ahead, behind, or in line with regional peers.
- Magnitude: size of the gap in dollars, percentages, percentiles, or benchmark bands when returned by the tool.
- Directional risk: whether revenue, profit, or expenses are meaningfully above or below peers.
- Actionability: which gaps the business can influence through pricing, cost control, sales mix, staffing, collections, or operating efficiency.

Flag something as a concern when one or more are true:
- Profit is below regional peers.
- Expenses are above peers without a matching revenue advantage.
- Revenue is below peers for the selected industry and region.
- The benchmark result depends on missing, inferred, or broad industry/location inputs.
- The tool output lacks enough structured data to support a precise ahead/behind/in-line conclusion.

Rank "Focus areas" by business severity. Lead with profit or cash-impacting gaps first, then expense gaps, then revenue growth gaps, then data-quality or benchmark-coverage limitations. Include a short severity label such as "High", "Medium", or "Context" when it helps the user prioritize action.

Do not overstate confidence. Use phrases such as "the peer data suggests", "this looks in line with", or "the main gap appears to be" when interpreting patterns.

## Output format

Do not output any briefing text in the chat. The widget renders all sections. Call `industry_benchmark_widget` as the only output step — no text before or after it.

## Widget render (final step)

Call the `industry_benchmark_widget` tool automatically after synthesizing the data.
Do NOT ask the user for permission — call it as the only output step.

Map the briefing sections to tool arguments as follows:
- `companyName`: connected company name from `company_info`.
- `benchmarkMode`: always `"connected_qbo"`.
- `metric`: `"profit"`, `"revenue"`, or `"expenses"` — whichever was benchmarked.
- `period`: the aggregation period label, e.g. `"Yearly"`, `"Monthly"`, `"Quarterly"`.
- `industry`: the industry name used for the benchmark. Use the corresponding industry name instead of a bare NAICS code whenever the tool output provides both.
- `region`: the full state name or region label used, e.g. `"California"` or `"Texas"`. This appears as the bar label in the chart (e.g. "California norm"), so prefer the full name over abbreviations.
- `peerSetAvailability`: derive from the tool output. Use `"Regional only"` when regional values are present and non-zero, and `"No peer data available"` when they are `$0.00`, `N/A`, or absent. The benchmarking API does not return national peer data, so never report national availability.
- `overallRead`: one of `"ahead"`, `"in_line"`, `"behind"`, or `"mixed"`. Use `"mixed"` when peer data is partially or fully unavailable — do not infer ahead/behind without actual peer numbers.
- `overallReadText`: the one-sentence verdict. If no peer data is available, say so plainly, e.g. `"No regional peer data is available for this industry and location."`.
- `keyNumbers`: a list of objects, one per row in the Key Benchmark Numbers table. Each object must have:
  `"area"`, `"companyValue"`, `"regionalPeers"`, and `"read"` string fields.
  Set `"read"` to `"ahead"`, `"in line"`, or `"behind"`. Use `"n/a"` when no peer data is available for that row — do not guess.
- `whereAhead`: the bullets from the **Where you're ahead** section (list of strings). Use an empty list `[]` if no peer data is available.
- `focusAreas`: the bullets from the **Focus areas** section. Each item must have `"severity"` (`"High"`, `"Medium"`, or `"Context"`) and `"text"`. Always add `"actionLabel"` and `"actionPrompt"` for High and Medium items — e.g. `"actionLabel": "Analyze expenses"`, `"actionPrompt": "Break down my operating expenses vs industry peers"`. These render as clickable chips. When peer data is unavailable, include a single `"Context"` item noting the data gap (no action chip needed).
- `whatGapsMean`: the bullets from the **What the gaps mean** section (list of strings).
- `suggestedNextMoves`: the items from the **Suggested next moves** section. Always use objects with `"text"` (required), `"actionLabel"` (short chip label, e.g. `"View Sales report"`), and `"actionPrompt"` (the follow-up message to send, e.g. `"Show me my Sales by Product report"`). Every move that maps to a follow-up question or report must have an action chip. Plain strings are allowed only when no logical follow-up action exists.
- `naicsCode`: NAICS code if available (omit if not).
- `chartData`: raw numbers for the primary bar chart. Extract the actual dollar/number figures from the text tool output — not formatted strings. Pass: `{ "companyValue": <number>, "regionalPeers": <number or null>, "metricLabel": "<period> <metric>", "metricFormat": "percent" | "currency" }`. Set `metricFormat` to `"percent"` when metricType is `margin`, otherwise omit it. Set `regionalPeers` to `null` when the tool shows `$0.00`, `N/A`, or no data — never pass `0`. Omit `chartData` entirely when the company value itself is not available.
- `secondaryChartData`: (**optional**) omit — the backend populates this automatically from `keyNumbers` when margin data is present.

## Style requirements
- Lead with the ahead/in-line/behind answer, not the tool list.
- Use exact numbers from tool outputs when available; otherwise say the metric was not available.
- Round large dollar values for readability, but preserve important precision for percentages, percentiles, and ratios.
- Tie every interpretation to a concrete benchmark value, range, percentile, or tool-returned signal.
- Always include Sales by Product/Service as one of the suggested next moves so the user can drill into item-level drivers behind benchmark gaps.
- Avoid accounting jargon unless it is paired with a plain-language explanation.
- Do not provide tax, legal, investment, lending, or financing advice. Frame recommendations as operational next steps.
