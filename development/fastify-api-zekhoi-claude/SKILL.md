---
name: fastify-api
description: Implement or change HTTP endpoints in a Fastify application following Fastify's conventions and the project's own patterns, with JSON schemas, correct async replies, error handling, and inject-based tests. Use when the user asks to add, change, or fix a route, plugin, hook, or API endpoint in a project that uses Fastify. Do not use for Express, Koa, or other frameworks, for reviewing code (use agent-kit:code-review), or for database query design.
---

# Fastify API implementation

## 1. Learn the application's structure

- Find how the app is built (a `buildApp` or `app.ts` factory), how routes are registered (route plugins, `@fastify/autoload`, prefixes), and which type provider or schema style is used (plain JSON Schema, TypeBox, Zod).
- Note existing hooks for authentication and authorization, error handling (`setErrorHandler`, `@fastify/sensible` HTTP errors), decorators, and logging.
- Read an existing route and its tests, and follow them.

## 2. Implement the route

- Register routes inside a plugin, matching the existing layout. Use `fastify-plugin` only for plugins that must share decorators or hooks with their parent; route plugins normally stay encapsulated.
- Declare schemas for `params`, `querystring`, `body`, and `headers` so Fastify validates input, and a `response` schema for each status code so serialization never leaks fields the schema does not list.
- In an `async` handler, either return the payload or call `reply.send()`, never both. Set status codes with `reply.code()` and return the body.
- Return 4xx errors for client mistakes and missing resources using the project's error helpers; let unexpected errors reach the error handler instead of swallowing them.
- Apply the project's authentication and authorization hooks (`onRequest` or `preHandler`) to anything that is not explicitly public. If no auth exists and the endpoint exposes user data, say so and ask before shipping it unprotected.
- Use `request.log` for logging, never `console.log`, and never log credentials or tokens.

## 3. Test

- Test through `app.inject()` without listening on a port, using a fresh app per test or suite, and close it afterwards.
- Cover the success response and its shape, validation failures (400), missing resources (404), and authorization failures where relevant.
- Run the project's tests and type check.

## 4. Report

Summarize the routes added or changed, the schemas and hooks used, the tests and their results, and any assumptions, such as authentication decisions, that the user should confirm.

## Examples

- Use: "Add a POST /users/:id/deactivate endpoint." "Add pagination to GET /orders."
- Skip: "Review routes/users.js." (code review) "Add an Express middleware." (other framework)
