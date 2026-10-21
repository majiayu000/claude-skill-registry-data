---
name: token-step-tracker
description: Estimate and report token consumption after each completed step of a multi-step agent task, maintain a cumulative estimate, show configurable threshold alerts, identify the main token driver, and suggest one practical way to reduce future usage. Use when users ask to track, monitor, display, audit, alert on, optimize, save, or reduce tokens or context usage during a task. All figures must be labeled as estimates unless the runtime explicitly supplies usage data.
---

# Token Alerts Not for Virgos

Track approximate token usage without interrupting the task or claiming billing accuracy.

## Start tracking

1. Break the task into meaningful outcome-based steps. Keep the existing plan if one already exists.
2. State once that token figures are estimates and exclude hidden system, reasoning, and platform overhead.
3. Read a positive integer alert interval from the user's request, such as `5000` in "alert every 5000 tokens." Use `1000` when the user requests alerts without specifying an interval. State the active interval once.
4. Set the next alert threshold to one interval and advance it by the interval after each alert.
5. Do not make extra tool calls, reread files, or generate additional content solely to improve an estimate.

## Report each completed step

Append this compact checkpoint after reporting the step's useful result:

```text
Token checkpoint · Step {n}: {name}
This step: ≈{low}–{high} tokens | Cumulative: ≈{low}–{high}
Main driver: {largest observable source}
Save next: {one actionable suggestion or "No worthwhile change—keep the current approach."}
```

Count a step only when it produces a meaningful result. Do not create checkpoints for status messages, approvals, waits, or trivial internal actions.

## Show threshold alerts

After each checkpoint, compare the midpoint of the cumulative range with the next alert threshold. When it reaches or exceeds the threshold, append:

```markdown
> :red_circle: TOKEN ALERT | **{threshold} estimated tokens used**
```

Use a red circle plus bold digits as the portable fallback. If the host supports safe inline HTML colors, render the value as `<span style="color:#d00"><strong>{threshold}</strong></span>`; never emit raw terminal escape codes. A pure skill cannot create an operating-system notification or guarantee text color, so call this an alert, not a system popup.

If one step crosses multiple thresholds, emit one alert for the highest crossed threshold and advance the next threshold beyond the cumulative midpoint. Never repeat an already emitted threshold.

## Estimate consistently

Estimate from observable content processed or produced during the step:

- English prose: roughly 1 token per 4 characters.
- Chinese prose: roughly 1 token per 1.5–2 characters.
- Code and structured data: roughly 1 token per 3 characters.
- Include relevant prompt text, newly read tool output, generated content, and context visibly reused for the step.
- Avoid double-counting the same artifact within one step.
- Use a range at least ±25% wide; widen it when context reuse is unclear.
- Round bounds to sensible values. Prefer `≈800–1,200`, not `≈917–1,143`.
- Add step ranges to maintain the cumulative range.

Never infer hidden reasoning tokens, platform instructions, cache behavior, billing, or monetary cost. If the runtime explicitly provides usage, report it separately as exact runtime usage rather than mixing it into the estimate.

## Recommend savings

Give at most one recommendation per checkpoint. Target the largest observed avoidable cost:

- Large file reads: search first, then read only matching sections.
- Repeated reads or searches: reuse the result already obtained.
- Broad tool output: narrow paths, fields, date ranges, or result counts.
- Oversized context: summarize stable findings before continuing.
- Long generated output: request or produce a tighter format when detail is unnecessary.
- Repeated failures: inspect the error and change the approach before retrying.
- Excessive examples: keep one representative example unless comparison is required.

Do not recommend skipping validation, security checks, required evidence, or user-requested detail merely to reduce tokens. If no meaningful saving exists, say so instead of inventing advice.

## Finish tracking

Include a short summary after the task's final result:

```text
Token estimate summary
Steps: {count} | Total: ≈{low}–{high} tokens
Largest step: {step name} (≈{low}–{high})
Alert interval: {interval} tokens | Alerts emitted: {count}
Best next-run saving: {single highest-impact suggestion}
Accuracy: Estimate only; excludes hidden system, reasoning, cache, and platform overhead.
```

Keep checkpoints and the summary secondary to the user's actual task.
