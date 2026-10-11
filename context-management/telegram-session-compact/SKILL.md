---
name: telegram-session-compact
description: Compact long Telegram chat sessions and prevent silent non-replies caused by high context usage. Use when a Telegram conversation becomes slow, misses replies, or session tokens are high (for example above ~80-85%), and when the user asks to clean, rotate, or shrink Telegram context.
---

# Telegram Session Compact

Compact Telegram sessions before they approach context limits.

## Runbook

1. Identify the Telegram session key.
2. Check token pressure (`session_status` or `openclaw status`).
3. If usage is high or replies are unstable, trigger compaction in that Telegram session with a standalone `/compact` message.
4. Use instruction text to preserve durable context and drop chatter.
5. Ask for a ping to verify reply path recovery.

## Compact Prompt Template

Use this as the `/compact` instruction:

`Keep durable context only: user profile, assistant identity, investment strategy/risk rules, pending tasks, and key decisions. Remove casual chat, duplicate discussion, and stale transient details.`

## Rotation Policy

- Compact at ~80-85% context usage.
- Force compact if there are signs of non-reply or delayed response.
- After compact, continue normal chat and monitor usage trend.

## Optional Preventive Config (Gateway)

If user asks for infra-level prevention, tune `agents.defaults.compaction` in gateway config (reserve/keepRecentTokens, safeguard mode, memoryFlush). Apply only with explicit user approval.
