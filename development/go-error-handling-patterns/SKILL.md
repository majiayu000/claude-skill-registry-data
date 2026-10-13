---
name: go-error-handling-patterns
description: >
  Use this when designing error types for a Go service, mapping domain errors to
  HTTP/NATS responses, building an error catalog, or reviewing error code for
  PII safety and consistency. Covers AppError hierarchy, fmt.Errorf %w wrapping,
  sentinel errors, errors.Is/As precedence, and PII-safe messages.
  Triggers: mapErr, sentinel switch, precedence order, errors.Is, fmt.Errorf %w chain.
---



# Go Error Handling Patterns

Standardizes error handling across all microservices. Every service uses a consistent AppError hierarchy that maps cleanly to HTTP status codes, log levels, and user-safe messages while preserving stack traces for debugging.

## When to Activate
- When designing error types for a new service
- When mapping domain errors to HTTP or NATS responses
- When implementing an error catalog for a microservice
- When reviewing error handling for PII safety and consistency
- Used by: sdk-designer, interface-designer, component-designer, coding-guidelines-generator

## AppError Type Hierarchy

All services share a common `AppError` type from the shared SDK.

```go
// pkg/errors/apperror.go
package errors

import (
	"fmt"
	"net/http"
	"runtime"
)

// Code represents a machine-readable error classification.
type Code string

const (
	CodeNotFound       Code = "NOT_FOUND"
	CodeConflict       Code = "CONFLICT"
	CodeValidation     Code = "VALIDATION"
	CodeUnauthorized   Code = "UNAUTHORIZED"
	CodeForbidden      Code = "FORBIDDEN"
	CodeInternal       Code = "INTERNAL"
	CodeTimeout        Code = "TIMEOUT"
	CodeRateLimit      Code = "RATE_LIMIT"
	CodeTenantMismatch Code = "TENANT_MISMATCH"
)

// AppError is the standard error type for all services.
// Uses msgpack tags for NATS inter-service communication (MsgPack is the sole wire format).
// json tags retained only for external API responses at the API Gateway boundary.
type AppError struct {
	Code       Code   `json:"code"    msgpack:"code"`
	Message    string `json:"message" msgpack:"message"`    // User-safe (no PII)
	Detail     string `json:"-"       msgpack:"-"`           // Internal detail (may contain PII, never serialized)
	HTTPStatus int    `json:"-"       msgpack:"-"`           // Mapped HTTP status code
	Cause      error  `json:"-"       msgpack:"-"`           // Wrapped underlying error
	Stack      string `json:"-"       msgpack:"-"`           // Captured call stack
}

// Error implements the error interface.
func (e *AppError) Error() string {
	if e.Cause != nil {
		return fmt.Sprintf("%s: %s: %v", e.Code, e.Message, e.Cause)
	}
	return fmt.Sprintf("%s: %s", e.Code, e.Message)
}

// Unwrap supports errors.Is and errors.As.
func (e *AppError) Unwrap() error {
	return e.Cause
}

// captureStack records the caller's stack at the point of error creation.
func captureStack(skip int) string {
	buf := make([]byte, 4096)
	n := runtime.Stack(buf, false)
	return string(buf[:n])
}
```

## Error Constructor Functions

Each error code has a dedicated constructor that captures the stack.

```go
// pkg/errors/constructors.go
package errors

import "net/http"

// NotFound creates an error for missing resources.
func NotFound(resource, id string) *AppError {
	return &AppError{
		Code:       CodeNotFound,
		Message:    fmt.Sprintf("%s not found", resource),
		Detail:     fmt.Sprintf("%s with id=%s not found", resource, id),
		HTTPStatus: http.StatusNotFound,
		Stack:      captureStack(2),
	}
}

// Validation creates an error for invalid input.
func Validation(message string) *AppError {
	return &AppError{
		Code:       CodeValidation,
		Message:    message,
		HTTPStatus: http.StatusBadRequest,
		Stack:      captureStack(2),
	}
}

// Unauthorized creates an error for missing or invalid credentials.
func Unauthorized(detail string) *AppError {
	return &AppError{
		Code:       CodeUnauthorized,
		Message:    "authentication required",
		Detail:     detail,
		HTTPStatus: http.StatusUnauthorized,
		Stack:      captureStack(2),
	}
}

// Forbidden creates an error for insufficient permissions.
func Forbidden(detail string) *AppError {
	return &AppError{
		Code:       CodeForbidden,
		Message:    "insufficient permissions",
		Detail:     detail,
		HTTPStatus: http.StatusForbidden,
		Stack:      captureStack(2),
	}
}

// Internal wraps an unexpected error with a safe message.
func Internal(cause error) *AppError {
	return &AppError{
		Code:       CodeInternal,
		Message:    "an internal error occurred",
		Detail:     cause.Error(),
		HTTPStatus: http.StatusInternalServerError,
		Cause:      cause,
		Stack:      captureStack(2),
	}
}

// TenantMismatch creates an error for cross-tenant access attempts.
func TenantMismatch(expected, actual string) *AppError {
	return &AppError{
		Code:       CodeTenantMismatch,
		Message:    "access denied",
		Detail:     fmt.Sprintf("tenant mismatch: expected=%s actual=%s", expected, actual),
		HTTPStatus: http.StatusForbidden,
		Stack:      captureStack(2),
	}
}
```

## Error Wrapping

Use `fmt.Errorf` with `%w` to add context while preserving the error chain.

```go
// internal/adapters/outbound/postgres/order_repo.go
func (r *OrderRepo) FindByID(ctx context.Context, tenantID, orderID uuid.UUID) (*model.Order, error) {
	row := r.pool.QueryRow(ctx, query, tenantID, orderID)

	o := &model.Order{}
	if err := row.Scan(&o.ID, &o.TenantID, &o.CustomerID); err != nil {
		if errors.Is(err, pgx.ErrNoRows) {
			return nil, apperrors.NotFound("order", orderID.String())
		}
		return nil, fmt.Errorf("scanning order row: %w", apperrors.Internal(err))
	}
	return o, nil
}
```

## Sentinel Errors

Define sentinel errors for domain-level conditions that callers check with `errors.Is`.

```go
// internal/domain/model/errors.go
package model

import apperrors "github.com/yourorg/shared/pkg/errors"

// Domain-level sentinel errors.
var (
	ErrAlreadyClosed     = apperrors.Conflict("entity is already closed")
	ErrDeadlineBreached  = apperrors.Validation("deadline has been breached, cannot reassign")
	ErrInvalidTransition = apperrors.Validation("invalid status transition")
)
```

Usage at call sites:

```go
if errors.Is(err, model.ErrAlreadyClosed) {
	// handle specific domain error
}
```

## Error to HTTP Status Mapping

| Error Code | HTTP Status | Log Level |
|-----------|-------------|-----------|
| `NOT_FOUND` | 404 | `warn` |
| `VALIDATION` | 400 | `warn` |
| `CONFLICT` | 409 | `warn` |
| `UNAUTHORIZED` | 401 | `warn` |
| `FORBIDDEN` | 403 | `warn` |
| `TENANT_MISMATCH` | 403 | `error` (potential security event) |
| `RATE_LIMIT` | 429 | `warn` |
| `TIMEOUT` | 504 | `error` |
| `INTERNAL` | 500 | `error` |

### HTTP Error Response Handler

```go
// internal/adapters/inbound/http/error_handler.go
package http

import (
	"errors"
	"net/http"

	"github.com/vmihailenco/msgpack/v5"
	apperrors "github.com/yourorg/shared/pkg/errors"
	"go.uber.org/zap"
)

// ErrorResponse is the envelope for error responses.
// Uses msgpack tags for NATS inter-service communication, json tags for HTTP responses.
type ErrorResponse struct {
	Code    apperrors.Code `json:"code"    msgpack:"code"`
	Message string         `json:"message" msgpack:"message"`
}

// WriteError translates an AppError to an HTTP response.
// It never leaks Detail or Cause to the client.
func WriteError(w http.ResponseWriter, logger *zap.Logger, err error) {
	var appErr *apperrors.AppError
	if !errors.As(err, &appErr) {
		appErr = apperrors.Internal(err)
	}

	logError(logger, appErr)

	w.Header().Set("Content-Type", "application/x-msgpack")
	w.WriteHeader(appErr.HTTPStatus)
	msgpack.NewEncoder(w).Encode(ErrorResponse{
		Code:    appErr.Code,
		Message: appErr.Message,
	})
}

func logError(logger *zap.Logger, appErr *apperrors.AppError) {
	fields := []zap.Field{
		zap.String("error_code", string(appErr.Code)),
		zap.String("detail", appErr.Detail),
		zap.String("stack", appErr.Stack),
	}
	if appErr.Cause != nil {
		fields = append(fields, zap.Error(appErr.Cause))
	}

	switch appErr.Code {
	case apperrors.CodeInternal, apperrors.CodeTimeout, apperrors.CodeTenantMismatch:
		logger.Error(appErr.Message, fields...)
	default:
		logger.Warn(appErr.Message, fields...)
	}
}
```

## PII-Safe Error Messages

The `Message` field is user-facing and MUST NOT contain PII (emails, IDs of other tenants, stack traces). Internal details go in `Detail` (never serialized to JSON).

```go
// GOOD: Message is safe for the client, Detail has debugging info.
apperrors.NotFound("order", orderID.String())
// Message: "order not found"
// Detail:  "order with id=abc-123 not found" (server-side only)

// BAD: Leaking user email in the message field.
// apperrors.NotFound("user", "john@example.com")
```

## Error Catalog Pattern

Each service defines its domain-specific errors in one file for discoverability.

```go
// internal/domain/errors.go
package domain

import apperrors "github.com/yourorg/shared/pkg/errors"

// Order domain errors.
var (
	ErrOrderNotFound      = func(id string) *apperrors.AppError { return apperrors.NotFound("order", id) }
	ErrOrderAlreadyClosed = apperrors.Validation("order is already closed")
	ErrInvalidTransition  = apperrors.Validation("invalid status transition")
	ErrDuplicateOrder     = apperrors.Conflict("an order with this external ID already exists")
)

// Billing domain errors.
var (
	ErrInvoiceNotFound   = func(id string) *apperrors.AppError { return apperrors.NotFound("invoice", id) }
	ErrPaymentFailed     = apperrors.Validation("payment processing failed")
	ErrQuotaExceeded     = apperrors.Validation("usage quota exceeded for this billing period")
)
```

## Examples

### GOOD
```go
// Proper error wrapping: adds context, preserves chain, uses AppError.
func (s *Service) CompleteOrder(ctx context.Context, tenantID, orderID uuid.UUID) error {
	order, err := s.repo.FindByID(ctx, tenantID, orderID)
	if err != nil {
		return fmt.Errorf("completing order: %w", err)
	}
	if order.Status.IsTerminal() {
		return model.ErrAlreadyClosed
	}
	completed := order.WithStatus(model.StatusDelivered)
	if err := s.repo.Update(ctx, completed); err != nil {
		return fmt.Errorf("persisting completed order: %w", err)
	}
	return nil
}
```

### BAD
```go
// WRONG: String error, no wrapping, leaks internal state, swallows context.
func (s *Service) CompleteOrder(ctx context.Context, tenantID, orderID uuid.UUID) error {
	order, err := s.repo.FindByID(ctx, tenantID, orderID)
	if err != nil {
		return fmt.Errorf("error: %v", err) // loses error chain (%v not %w)
	}
	if order.Status == "closed" {
		return fmt.Errorf("order %s for tenant %s is already closed, assigned to %s",
			orderID, tenantID, order.AssigneeEmail) // leaks PII
	}
	return nil
}
```

## Common Mistakes

1. **Using `%v` instead of `%w` in `fmt.Errorf`** -- `%v` converts the error to a string, breaking `errors.Is` and `errors.As` chains. Always use `%w` to wrap errors while preserving the chain.

2. **Leaking PII in the `Message` field** -- User emails, internal IDs of other tenants, or stack traces must never appear in `Message`. Put debugging details in `Detail`, which is excluded from JSON serialization (`json:"-"`).

3. **Returning raw `error` from adapters without wrapping in `AppError`** -- Raw `pgx` or `nats` errors lack HTTP status mapping. Convert infrastructure errors to `AppError` at the adapter boundary so upper layers have consistent error metadata.

4. **Silently discarding errors** -- Never use `_ = someFunc()` for functions that return errors. Handle every error explicitly or, if truly unrecoverable, log and fail fast.

5. **Creating error types per service instead of using the shared SDK** -- All services must use `pkg/errors.AppError` from the shared SDK. Service-specific errors are built by composing SDK constructors, not by defining new error structs.
