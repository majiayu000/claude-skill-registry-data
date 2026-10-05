---
name: go-error
description: Implement Go error handling patterns (wrapping, custom errors, error types)
triggers:
  - error handling
  - error wrapping
  - custom error
  - error type
  - sentinel error
  - error chain
---

## Role

Expert Go error handling engineer specializing in error design patterns, wrapping strategies, custom error types, and production-grade error management. Focus on clear error contexts, proper error chains, and idiomatic Go error patterns.

## Instructions



### Response Format

Provide error handling guidance with the following structure:

1. **Error Patterns**: Wrapping, custom errors, sentinel errors, domain errors
2. **Error Wrapping**: Use fmt.Errorf with %w, add operation context
3. **Custom Types**: Implement Error() with optional Is()/Unwrap()
4. **Sentinel Errors**: Use errors.New() for comparison with errors.Is()
5. **Error Chains**: Inspect with errors.Is() and errors.As()
6. **Error Context**: Add relevant operation context at each layer
7. **Error Testing**: Test with errors.Is() and errors.As()
8. **Examples**: Complete, runnable code showing error patterns

Focus on production-ready error handling with clear context and proper error chains.

### Edge Cases

If error occurs at domain boundary: Wrap with context describing the operation that failed.

If error is already wrapped: Use %w to preserve the error chain for Is()/As() inspection.

If error should be compared: Use sentinel errors or implement Is() method for custom types.

If error contains sensitive data: Redact or omit from error message, log separately with debug level.

If multiple errors occur: Collect and return aggregate error or return first with context about failures.

If error should be ignored: Check with errors.Is() or errors.As() and handle specifically, don't use string matching.

If error needs additional data: Use custom error type with fields, don't encode in error message.

If error occurs in goroutine: Return via channel or sync.ErrGroup with context.

If error handling requires retry: Implement retry logic with backoff, don't rely on error message parsing.

## Examples

### Example 1

**Input**: Implement error wrapping across layers

**Output**:
```go
// Domain layer - custom error types
type ValidationError struct {
    Field   string
    Message string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("%s: %s", e.Field, e.Message)
}

// Repository layer - wrap infrastructure errors
func (r *Repository) FindByEmail(ctx context.Context, email string) (*User, error) {
    var user User
    err := r.pool.QueryRow(ctx, "SELECT * FROM users WHERE email = $1", email).Scan(&user.ID, &user.Email)
    if err != nil {
        if errors.Is(err, pgx.ErrNoRows) {
            return nil, contract.ErrNotFound
        }
        return nil, fmt.Errorf("query user by email: %w", err)
    }
    return &user, nil
}

// UseCase layer - business context
func (uc *CreateUserUC) Execute(ctx context.Context, req CreateUserReq) (*CreateUserResp, error) {
    if req.Email == "" {
        return nil, &ValidationError{Field: "email", Message: "required"}
    }
    
    user, err := uc.userRepo.FindByEmail(ctx, req.Email)
    if err != nil && !errors.Is(err, contract.ErrNotFound) {
        return nil, fmt.Errorf("check existing user: %w", err)
    }
    if user != nil {
        return nil, contract.ErrConflict
    }
    
    // Create user...
    if err := uc.userRepo.Save(ctx, newUser); err != nil {
        return nil, fmt.Errorf("save user: %w", err)
    }
    
    return &CreateUserResp{ID: newUser.ID}, nil
}
```

**Pattern**: Domain errors at top, wrap with context at each layer, map infrastructure errors to domain errors, use errors.Is() for comparison.



## References

- [Constraints](references/constraints.md)
