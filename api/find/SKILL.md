---
name: find
description: Find the looot endpoints that do a job and compare them by price, measured success rate and speed, without running or paying for anything. Use when the person asks which data APIs can do something, or what a lookup would cost.
---

# Find a data API with looot

The job to find: the job the person asked for

If no job was given, ask in one line what they need, for example "verify an email" or "backlinks for
a domain".

1. Call `search` with the job in plain words as `query` and `"limit": 5`. Searching is free.
2. Show the rows that have `access: "runs_now"` as a table: provider, what it does (`name`),
   `estimatedPrice` in dollars with its `priceBasis`, success rate (`works.rate`, or "new" when
   `works.thin` is true) and `endpointId`.
3. Call `inspect` with `{"endpointId": "<the top row>", "detail": "run"}` (free). Give its required
   inputs and `estimatedMaxCost`, the most one call can cost.
4. If `items` is empty, say looot has no endpoint for that job yet, and offer to file it with
   `capability_request`.
5. End with one line: the run you would make (job id or endpoint id, and the inputs it needs), and ask
   if they want it run. Do not call `run` from this skill.
