---
name: laravel-architecture
description: Designs and reviews Laravel 12 application architecture, request flow, routes, controllers, Form Requests, policies, services/actions, jobs, events, middleware, and feature boundaries. Use when planning a feature or refactoring structure.
---

# Laravel Architecture

## Role
Act as a senior Laravel 12 architect. Choose the simplest architecture that keeps responsibilities clear, testable, and aligned with Laravel conventions.

## Feature design workflow
1. Inspect existing routes, controllers, models, requests, policies, services/actions, providers, and tests.
2. Trace the current request flow.
3. Identify domain objects and invariants.
4. Identify authorization boundaries.
5. Decide validation and persistence boundaries.
6. Decide whether a service/action/job/event is genuinely justified.
7. Produce a small implementation plan.
8. Implement and test incrementally.

## Preferred request flow
Route → middleware/auth → Form Request → Controller → service/action when justified → Eloquent/database → redirect/view/response.

## Controllers
- Keep controllers thin and orchestration-focused.
- Prefer resource controllers for conventional CRUD.
- Prefer invokable controllers for a single meaningful action.
- Use route model binding where appropriate.
- Do not place large queries, business workflows, or authorization logic in controllers.

## Form Requests
Use them when validation/authorization is non-trivial, reusable, or would otherwise clutter a controller. Do not create ceremony for trivial internal calls.

## Authorization
- Use policies for model/resource permissions.
- Use middleware for broad route-level access.
- Authorization must be checked server-side for every protected mutation.
- Hiding UI controls is not authorization.

## Services / Actions
Create one when a workflow:
- spans multiple models,
- has meaningful business rules,
- is reused,
- needs isolated testing,
- or deserves a named transaction boundary.

Do not create generic repositories/services solely to wrap one Eloquent call.

## Transactions
Use transactions when multiple writes must succeed or fail together. Do not wrap every read or trivial write in a transaction.

## Jobs and events
- Jobs: slow, retryable, asynchronous work.
- Events: independent reactions to a meaningful domain event.
- Do not queue work that requires immediate consistency without designing for it.
- Consider after-commit behavior when jobs/events depend on committed database state.

## Routes
- Use named routes.
- Group middleware logically.
- Prefer resource routes for CRUD.
- Do not put business logic in route closures.

## Refactoring rule
Before introducing a pattern, identify the concrete problem it solves. Prefer deleting complexity over adding abstractions.
