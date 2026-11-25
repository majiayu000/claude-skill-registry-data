---
name: define-slos
description: Defines SLIs, SLOs and an error-budget policy from a service's user journeys, with multi-window burn-rate alert rules. Use when alerting is noisy or reliability targets are vague.
license: CC0-1.0
metadata:
  version: 1.0.1
  kind: prompt
  category: incident
  source: https://hermes-ide.com/prompts/define-slos
  catalog: 2026.1014.1
---

# Define SLOs and burn-rate alerts

## Inputs

- [SERVICE] (required): The service, its users, its architecture at a high level and the monitoring stack (for example Prometheus, Datadog, Cloud Monitoring).
- [USER_JOURNEYS] (required): The journeys users care about, e.g. "log in", "search the catalog", "checkout", with any known expectations.
- [CURRENT_METRICS] (optional): Existing metric names and recent performance (success rate, latency percentiles, traffic volume).

Take each value from the invocation or the user’s message. If a required value is missing, ask for it once.

<context>
Teams write SLOs that measure servers instead of users ("CPU below 80%"), pick 99.99% because it sounds good, and alert on raw error rate, which pages for blips and misses slow burns. A good SLO measures what users experience on a journey, sets a target the service can meet and users would accept, and alerts on how fast the error budget is burning.
</context>

<task>
Define SLOs for [SERVICE] from these user journeys:
[USER_JOURNEYS]
Only if [CURRENT_METRICS] was provided: 
Current metrics and performance:
[CURRENT_METRICS]

1. For each journey, choose 1 or 2 SLIs written as good events divided by valid events: availability, latency below a threshold, freshness or correctness. Say where each is measured (load balancer, server, client) and the trade-off. Define valid events explicitly, for example excluding health checks and client errors the user caused.
2. Set a target and a window (a 28- or 30-day rolling window by default). Base the target on current performance and user need. If current metrics are missing, mark targets "provisional" and propose a 2 to 4 week baseline measurement.
3. Compute the error budget in allowed bad events and in minutes of full outage per window.
4. Write an error-budget policy: what happens at 50%, 75% and 100% consumed (for example: slow down risky launches, prioritise reliability work, freeze non-critical changes), the exceptions, and who decides.
5. Write multi-window, multi-burn-rate alerts for a 30-day window: page at 14.4x burn over 1 hour (with a 5-minute short window), page at 6x over 6 hours (30-minute short window), and open a ticket at 1x over 3 days (6-hour short window). Adjust the numbers if the window differs and show the calculation.
6. Write the alert rules in the syntax of the user's monitoring stack (PromQL recording and alerting rules by default). Note the low-traffic problem and a mitigation if any journey has little traffic.
</task>

<constraints>
- No target of 100%, and no target tighter than the service's dependencies allow without saying how.
- Use the metric names given; where none are given, use clearly named placeholders and say so.
- Prefer few SLOs that matter over full coverage. Three per service is often enough.
- Separate what you verified from what you inferred. Mark inferences as such.
- When you do not know, say "I don't know" once and state what would settle it.
</constraints>

<output_format>
## SLOs
A table: journey, SLI (good / valid), measured at, target, window, error budget.
## Rationale
One short paragraph per SLO: why this SLI and target.
## Error-budget policy
Thresholds, actions, exceptions, decision owner.
## Alert rules
Fenced code blocks with the rules, then a table: alert, burn rate, long window, short window, budget consumed when it fires, page or ticket.
## Open questions
What to confirm with product owners or measure first.
</output_format>
