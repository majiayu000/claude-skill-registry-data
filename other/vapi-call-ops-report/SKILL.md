---
name: vapi-call-ops-report
description: Analyze Vapi voice-agent and call performance for call outcomes, lead handling, bookings/transfers, tool execution, failures, latency, cost, conversation quality, prompt/knowledge issues, missed revenue, and operational reliability. Use when the user asks for a Vapi report or audit, provides Vapi call logs/exports/transcripts/JSON/screenshots, wants to inspect agent performance, or needs to understand why calls are failing, expensive, low quality, or not converting.
triggers: vapi, voice agent, call performance, call outcomes, lead handling, bookings, transfers, call failures, latency, cost, missed leads, assistant version, yesterday's calls, call report
---

# Vapi Call Ops Report

Audit Vapi as a revenue and operations system, not merely as a call-volume dashboard.

## Workflow

1. Identify the assistant/phone number/workflow, exact date range, timezone, environment, and available call fields.
2. Accept authorized connector/API data when available, or analyze CSV/JSON/transcripts/screenshots/logs. Never require a fixed Vapi schema; inspect the current fields first.
3. Build a call funnel from the evidence available:
   - attempted -> connected -> qualified -> desired action attempted -> action completed -> downstream outcome.
   - Desired actions may include appointment, transfer, message capture, quote/inquiry capture, or another business goal.
4. Segment by call direction, assistant/version, phone number/campaign, intent, disposition, ended reason, duration, time/day, and outcome where present.
5. Audit quality and failure modes:
   - hangups or premature endings
   - silence/latency/interruption problems
   - hallucinated or incorrect business information
   - failed tool calls, transfers, bookings, or CRM writes
   - loops, repetition, overtalking, poor intent recognition, weak objection handling
   - spam/non-customer traffic
   - transcription or language issues
6. Audit economics:
   - total and per-call cost when available
   - cost per connected call, qualified lead, completed action, and successful downstream outcome where denominators exist
   - expensive failure cohorts and avoidable token/model/telephony waste
7. Inspect transcripts selectively.
   - Prioritize failed high-value calls, anomalous long calls, repeated failure clusters, and representative successes.
   - Quote only short snippets needed to prove a finding.
8. Separate Vapi success from business success. A technically completed call is not a success if the customer failed to get what they needed.
9. Read `references/report-contract.md` and follow its output structure.

## Rules

- Do not invent dispositions from transcripts when evidence is ambiguous; label inferred classifications.
- Do not treat average duration as inherently good or bad.
- Preserve privacy: avoid reproducing unnecessary personal information from callers.
- Prefer cohort evidence over isolated anecdotes.
- When Vapi platform behavior or field semantics matter and may have changed, verify current documentation before making platform-specific claims.

## Useful triggers

Examples: "run a Vapi report", "audit yesterday's calls", "why is the voice agent missing leads?", "which call failures are costing us money?", "compare assistant versions".
