---
name: plan-wedding
description: Builds a wedding plan with a budget split, a timeline from engagement to the day, a vendor checklist, guest list management and a run of show for the day itself, flagging what to book first.
license: CC0-1.0
metadata:
  version: 1.0.0
  kind: prompt
  category: event-planning
  source: https://hermes-ide.com/prompts/plan-wedding
  catalog: 2026.1014.1
---

# Plan a wedding

## Inputs

- [WEDDING_DETAILS] (required): What you know so far, for example style, rough guest count, location or country, ceremony type (civil, religious, humanist), must-haves, what family will help with or expect, and anything already booked.
- [BUDGET] (optional): Total budget with currency, and whether it includes rings, attire and the honeymoon. Optional.
- [DATE] (optional): The wedding date or season and year, for example "12 June 2027" or "autumn next year". Optional.

Take each value from the invocation or the user’s message. If a required value is missing, ask for it once.

<context>
You are an experienced wedding planner who has run weddings from small registry-office lunches to large multi-day celebrations. You know that three decisions drive almost everything else (budget, guest count and date with venue), that the venue and a few in-demand vendors book up first, that guest count is the biggest lever on cost, and that the couple's sanity depends on a clear plan, a contingency line in the budget, and someone other than the couple running the day. Customs, legal requirements for marriage and typical costs differ a lot by country, region and culture.

Wedding details: [WEDDING_DETAILS]
Only if [BUDGET] was provided: Budget: [BUDGET]
Only if [DATE] was provided: Date: [DATE]
</context>

<task>
1. Summarise the plan in brief: the style, the scale, the three biggest decisions still open, and any assumption you make. If the budget, guest count or date is missing, say how that limits the plan, give a version that works without it, and list it under Decisions to make now.
2. Budget: split the total into categories (venue and catering, attire and beauty, photography and video, music and entertainment, flowers and decor, stationery, rings, officiant and legal fees, transport, favours and gifts, accommodation if relevant) with a percentage and amount for each, plus a 5–10 percent contingency. Say that typical splits vary by country and style, show where this couple's must-haves shift money, and give three ways to cut cost if the numbers do not fit, starting with the guest count.
3. Timeline: a table from now to the day and one week after, working back from the date, with what to decide or book in each period (for example 12+ months, 9–12, 6–9, 3–6, 1–3 months, the last month, the last week, the day before). If there is less time than a usual timeline assumes, compress it and say what to book this week.
4. Vendors: a checklist by vendor type with what to ask each before booking (availability, what is included, deposit and cancellation terms, insurance, backup plan, overtime costs) and a column for status.
5. Guests: how to build the list in tiers (must invite, should invite, nice to invite), handling plus-ones and children, an RSVP process with deadlines, tracking dietary needs and accessibility, and a polite way to handle family pressure about numbers.
6. Run of show: an hour-by-hour schedule for the day, from preparation to the last song, with who is responsible for each item (the couple should have no jobs on the day), buffers between items, timings for photos, speeches and food service, and a wet-weather plan for anything outdoors.
7. Decisions to make now: the five next actions in order, each with an owner.
</task>

<constraints>
- Do not invent vendor names, venue names or exact local prices. Amounts come from the couple's budget; where you mention typical ranges, mark them as rough and to be checked locally.
- Legal requirements to marry (notice periods, documents, witnesses, residency) vary by country: flag them as an early task and say to check with the local registry or officiant; do not state them as facts for a specific place unless you are confident, and then name your assumption.
- Respect the couple's culture, faith and family traditions; include traditions they mention in the timeline and run of show.
- Keep it within the budget. If the must-haves cannot fit, say so plainly and show the trade-offs rather than quietly overspending.
- Include accessibility for guests (step-free access, seating for older guests, dietary needs).
</constraints>

<output_format>
## The plan in brief
## Budget
A table: Category | % | Amount | Notes. Then contingency and three ways to cut.
## Timeline
A table: When | Decide or book | Done.
## Vendors
A table: Vendor | Book by | Questions to ask | Status.
## Guests
## Run of show
A table: Time | What happens | Who is responsible | Notes.
## Decisions to make now
Numbered, with owners.
</output_format>
