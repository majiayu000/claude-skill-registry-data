---
name: pstack-benchmark-checklist
description: "Validate performance measurements and before/after claims. Use when benchmarking latency, throughput, query performance, build or test duration, or a claimed speedup."
license: MIT
metadata:
  upstream: https://github.com/cursor/plugins/tree/ccb5507cec1546dc88135c1139c811e6c59115ba/pstack/skills/benchmark-checklist
  upstream-commit: ccb5507cec1546dc88135c1139c811e6c59115ba
  adaptation: portable-chat-inherited
---

# Benchmark checklist

Test the measurement claim before using it to choose or report an improvement.

## Environment contract

Use the active chat model and its current reasoning settings. Delegate only when supported and authorized; omit model and effort overrides when omission inherits the chat settings. If the host cannot guarantee that inheritance, do the work in the current chat. Sequential passes are a fallback, not independent reviewers.

Use available file, search, terminal, browser, history, and connector tools. Follow the user's scope, authorization, repository instructions, and local resource controls. A skill invocation does not authorize publication, unrelated changes, or external messages.

## Define the experiment

Write the claim with its unit, workload, and measured interval. Inspect the measurement code: what starts the clock, ends it, counts as one sample, and stays outside it.

Record exact versions or SHAs, dataset, concurrency, build mode, cache state, pool settings, and machine load. Use platform-appropriate counters. Keep the prescribed resource launcher and worker limits. Avoid stopping unrelated processes.

## Validate each side

- Work happened inside the timed region. Requests reached the server, generators were consumed, promises awaited, and outputs used.
- Count successes, errors, retries, and timeouts. Compare output correctness as well as elapsed time.
- Tune both sides comparably for the adoption decision. An untuned side supports only a narrowly stated configuration comparison.
- Profile separately from reported timing runs. Find the measured bottleneck and check the load generator.
- Check physical and arithmetic bounds. Removing a 10% component cannot cut end-to-end duration by 50%.

For a rough estimate explicitly requested, one run may suffice; label it as such. For a before/after decision, use repeated interleaved runs, normally at least five per side, and report median and spread. Match cold and warm scenarios rather than accidentally mixing them. Respect a user instruction not to rerun prior checks; report the resulting limitation.

Measure the path the user waits on beside microbenchmarks. API latency excludes browser rendering unless both are timed. Test counts are not coverage, and lower duration is not proof of equivalent protection.

## Deliver

State faster, slower, no measurable difference, or inconclusive. Include the primary number, unit, run count, spread, correctness/error results, and bottleneck evidence. Do not claim a difference smaller than observed noise. Preserve artifacts for scrutiny; publish them only within the authorized delivery.
