---
name: kit-go-http-api
description: Implement or change HTTP handlers in a Go service following the project's router and patterns (net/http, chi, gin, or echo), with input validation, context propagation, correct status codes and JSON encoding, and httptest table tests. Use when the user asks to add, change, or fix an endpoint, handler, or middleware in a Go HTTP service. Do not use for gRPC services, for reviewing code (use kit-go-review or kit-code-review), or for database query review (use kit-go-sql-review).
---

# Go HTTP API implementation

## 1. Learn the service's structure

- Find the router (`http.ServeMux` with method and wildcard patterns, which need `go 1.22` or later in `go.mod`; chi, gin, echo), how handlers are registered and grouped, and how dependencies such as the store and logger reach handlers (a server struct, closures).
- Note existing middleware for authentication, request IDs, logging, and recovery, the JSON helpers and error response shape, and how tests build the server.
- Read an existing handler and its test, and follow them.

## 2. Implement the handler

- Register the route with its method next to related routes. Parse path values (`r.PathValue`, `chi.URLParam`) and query parameters, and validate them: return 400 with the project's error shape for bad input.
- Decode JSON bodies with a size limit (`http.MaxBytesReader`) and `DisallowUnknownFields` where the project does; reject trailing data. Validate required fields.
- Use separate request and response structs with `json` tags so internal fields such as password hashes are never encoded.
- Pass `r.Context()` to every store and outbound call. Map domain errors (`errors.Is(err, store.ErrNotFound)`) to 404 and similar; log unexpected errors and return 500 without leaking details.
- Set `Content-Type` and the status code before writing the body, and do not write the header twice. Return right after writing an error response.
- Apply the project's authentication middleware to anything not explicitly public. If no authentication exists and the endpoint exposes user data, say so and ask before shipping it unprotected.

## 3. Test

- Use `httptest.NewRecorder` with the real router (or `httptest.NewServer`) and table-driven cases: success and response shape, validation failures (400), missing resources (404), and authorization failures where relevant.
- Run `go test ./...` (with `-race` if the project uses it) and `go vet ./...`.

## 4. Report

Summarize the routes added or changed, request and response types, error mapping, tests and their results, and assumptions, such as authentication decisions, that the user should confirm.

## Examples

- Use: "Add a POST /users/{id}/deactivate endpoint." "Add pagination to GET /orders."
- Skip: "Review handlers.go." (code review) "Add a gRPC method." (other transport)
