---
name: cost-tracking-anthropic
description: Use when monitoring or optimizing Claude API spend ג€” per-agent cost attribution, prompt caching, token budgeting, alerting on cost spikes. Covers `src/lib/cost-tracker.ts`.
---

# Cost Tracking (Anthropic) skill

## When to invoke

- Adding a new agent or tool that calls the Claude API
- Investigating a cost spike in the Anthropic dashboard
- Designing prompt-caching strategy for long system prompts
- Setting up cost alerts / budget guards

## Model cost tiers (rough, verify in dashboard)

- `claude-opus-4-7` ג€” premium, ~5x Sonnet pricing. Master only.
- `claude-sonnet-4-6` ג€” balanced. Sub-agents default.
- `claude-haiku-4-5-20251001` ג€” cheap, fast. Classification, simple extraction.

## Hard rules

1. **Always log usage** ג€” every Claude API call records agent, model, input_tokens, output_tokens, cached_tokens, cost_estimate to a cost_events table
2. **Use prompt caching** for any system prompt over 1024 tokens that is reused ג€” sub-agent system prompts qualify, mark with cache_control
3. **Never pass full conversation history to Haiku** ג€” Haiku is for one-shot classification; long context defeats its cost advantage
4. **Cap output tokens** per call (max_tokens) ג€” default 1024 for sub-agents, 256 for Haiku, 4096 for Master. Override only with reason
5. **Budget guard**: hard daily cap per customer (default 10 calls/day) ג€” break circuit and escalate when hit

## Attribution dimensions

Track cost by: agent_name, customer_id, tool_name (if tool-use turn), routing_path (Master ג†’ which sub-agent). This lets you answer "which customer is expensive" and "which tool is bloated".

## Prompt-caching pattern

Mark the long static portion of the system prompt with cache_control ephemeral, and keep the dynamic per-customer context outside the cached block. Cached tokens are ~10% the cost of fresh input tokens after the first call within 5 min.

## Alerts

- Daily spend more than 2x the 7-day rolling avg ג†’ Slack alert
- Single customer more than 50 calls/day ג†’ freeze + advisor review
- Any single API call over $1 ג†’ log warning, may indicate runaway loop

## What this skill is NOT

A budgeting policy ג€” actual limits live in env config (COST_DAILY_CAP_USD, COST_PER_CUSTOMER_DAILY_CAP), not in this skill.