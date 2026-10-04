---
name: api-design-principles
description: Standards for REST, GraphQL, and RPC interface design. Focuses on developer experience and long-term stability. Use when designing new API surfaces.
version: "1.0.0"
verified_date: 2026-04-29
category: core
---

# API Design Principles

## Purpose
Create APIs that are intuitive, stable, and performant.

## When to Use This Skill
Use during the PLANNING phase of any feature involving a new or modified API endpoint.

## Phase 1: Contract Design
1. Define endpoints, methods, and payload structures.
2. Ensure consistent naming conventions (camelCase vs kebab-case).
3. Plan for versioning if the API is public-facing.

## Phase 2: Security, Rate Limiting & Streaming
1. Define authentication and authorization requirements.
2. Plan rate limiting and input size constraints.
3. Design real-time streaming protocols if applicable (e.g., WebSockets, Server-Sent Events / SSE) for continuous data pipelines.

## Behavior Rules
1. **Consistency is King**. Use the same patterns across the entire API surface.
2. **Fail Gracefully**. Provide clear, actionable error messages.
3. **No Over-fetching**. Return only the data the client needs.

## Output Format / Delivery
- Outputs should be structured API schemas, interfaces, or documented endpoints.

## Maintenance Notes
- Initial global core skill.
