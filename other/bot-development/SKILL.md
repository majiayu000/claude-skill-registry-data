---
name: bot-development
description: "Use when building or changing an automated bot that responds to messages, events, schedules, or platform APIs to define authorized actions, user consent, scopes, idempotency, rate limits, and failure behavior before connecting a live account. Trigger for chat, community, workflow, monitoring, or platform automation bots."
---

# Bot Development

## Overview

This skill applies when building or changing an automated bot that responds to messages, events, schedules, or platform APIs. Its intended outcome is to define authorized actions, user consent, scopes, idempotency, rate limits, and failure behavior before connecting a live account.

## When to Use

### Preserved source section: When to Use

Use for a software agent that acts through a platform account or reacts to incoming events. Distinguish read-only assistance from posting, moderation, messaging, purchases, or other externally visible actions.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Source boundary statements from: Procedure

4. **Respect platform controls.** Use official APIs, minimum scopes, documented rate limits, backoff for transient failures, and an explicit stop mechanism. Do not bypass access controls, anti-abuse limits, or user privacy settings.

### Source boundary statements from: Output and Acceptance

Document event coverage, permission scopes, write actions, idempotency behavior, rate limits, data retention, test evidence, and the live-activation gate. Accept when duplicate events do not duplicate effects, denied actions fail closed, and the bot's authority matches the approved scope.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs

- Target platform and its official API, event, and policy documentation.
- User roles, event types, commands, permissions, and expected bot behavior.
- Required scopes, secret storage, data retention, rate limits, and confirmation rules.

## Instructions

### Preserved source section: Procedure

1. **Define behavior and authority.** List triggers, allowed actions, prohibited actions, and whether a human must confirm each write. Keep read and write permissions separate.
2. **Build a local handler first.** Normalize one event type, validate its schema, produce a deterministic decision, and test the response without a live account.
3. **Handle retries safely.** Use event IDs or idempotency keys, acknowledge only after durable processing, and prevent duplicate posts or repeated side effects.
4. **Respect platform controls.** Use official APIs, minimum scopes, documented rate limits, backoff for transient failures, and an explicit stop mechanism. Do not bypass access controls, anti-abuse limits, or user privacy settings.
5. **Protect user data.** Minimize stored content, redact logs, limit retention, and restrict who can inspect conversations or identifiers.
6. **Test policy and failure cases.** Cover malformed events, duplicate delivery, permission denial, rate limiting, service outage, unsafe content, and human approval timeout.
7. **Stage activation.** Start in a sandbox or private test channel, observe logs and rate behavior, then request separate approval before enabling live writes.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Output and Acceptance

Document event coverage, permission scopes, write actions, idempotency behavior, rate limits, data retention, test evidence, and the live-activation gate. Accept when duplicate events do not duplicate effects, denied actions fail closed, and the bot's authority matches the approved scope.

## Output Format

### Preserved source section: Output and Acceptance

Document event coverage, permission scopes, write actions, idempotency behavior, rate limits, data retention, test evidence, and the live-activation gate. Accept when duplicate events do not duplicate effects, denied actions fail closed, and the bot's authority matches the approved scope.

## Validation Checklist

- [ ] Verify the source-defined success criteria above.

## Edge Cases and Recovery

### Source edge/failure guidance from: Procedure

3. **Handle retries safely.** Use event IDs or idempotency keys, acknowledge only after durable processing, and prevent duplicate posts or repeated side effects.
4. **Respect platform controls.** Use official APIs, minimum scopes, documented rate limits, backoff for transient failures, and an explicit stop mechanism. Do not bypass access controls, anti-abuse limits, or user privacy settings.
6. **Test policy and failure cases.** Cover malformed events, duplicate delivery, permission denial, rate limiting, service outage, unsafe content, and human approval timeout.

### Source edge/failure guidance from: Output and Acceptance

Document event coverage, permission scopes, write actions, idempotency behavior, rate limits, data retention, test evidence, and the live-activation gate. Accept when duplicate events do not duplicate effects, denied actions fail closed, and the bot's authority matches the approved scope.

## Stop Conditions

### Source stop-related guidance from: Procedure

4. **Respect platform controls.** Use official APIs, minimum scopes, documented rate limits, backoff for transient failures, and an explicit stop mechanism. Do not bypass access controls, anti-abuse limits, or user privacy settings.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Acceptance criteria from source: Output and Acceptance

Document event coverage, permission scopes, write actions, idempotency behavior, rate limits, data retention, test evidence, and the live-activation gate. Accept when duplicate events do not duplicate effects, denied actions fail closed, and the bot's authority matches the approved scope.
