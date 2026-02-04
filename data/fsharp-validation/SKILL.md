---
name: fsharp-validation
description: |
  Create validation logic for F# backends with error accumulation and async validation.
  Use when: "add validation", "validate X", "input validation", "complex validation",
  "business rules", "check email", "required fields", "async validation",
  "database uniqueness", "cross-field validation", "validation errors".
  Creates validators in src/Server/Validation.fs. Use for complex scenarios;
  basic validation patterns are in fsharp-backend skill.
allowed-tools: Read, Edit, Write, Grep
---

# F# Validation Patterns

## When to Use This Skill

Activate when:
- User requests "add validation for X"
- Implementing API endpoints (always validate at boundary)
- Need complex validation rules
- Validating create/update requests
- Checking business rules or constraints

## Core Principle

**Validate at the API boundary, before any processing.**

## Basic Validator Helpers

**Location:** `src/Server/Validation.fs`

```fsharp
module Validation

open System
open System.Text.RegularExpressions

// Single field validators return Option<string>
// None = valid, Some errorMessage = invalid

let validateRequired (fieldName: string) (value: string) : string option =
    if String.IsNullOrWhiteSpace(value) then
        Some $"{fieldName} is required"
    else
        None

let validateLength (fieldName: string) (minLen: int) (maxLen: int) (value: string) : string option =
    let len = value.Length
    if len < minLen then
        Some $"{fieldName} must be at least {minLen} characters"
    elif len > maxLen then
        Some $"{fieldName} must be at most {maxLen} characters"
    else
        None

let validateRange (fieldName: string) (min: int) (max: int) (value: int) : string option =
    if value < min || value > max then
        Some $"{fieldName} must be between {min} and {max}"
    else
        None

let validateEmail (email: string) : string option =
    let emailPattern = @"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    if Regex.IsMatch(email, emailPattern) then None
    else Some "Invalid email format"

let validateUrl (url: string) : string option =
    match Uri.TryCreate(url, UriKind.Absolute) with
    | true, _ -> None
    | false, _ -> Some "Invalid URL format"

let validatePositive (fieldName: string) (value: int) : string option =
    if value > 0 then None else Some $"{fieldName} must be positive"

let validateNonNegative (fieldName: string) (value: int) : string option =
    if value >= 0 then None else Some $"{fieldName} cannot be negative"

let validatePattern (fieldName: string) (pattern: string) (value: string) : string option =
    if Regex.IsMatch(value, pattern) then None
    else Some $"{fieldName} has invalid format"
```

## Entity Validation

### Multiple Errors (Accumulate All)
```fsharp
let validateTodoItem (item: TodoItem) : Result<TodoItem, string list> =
    let errors = [
        validateRequired "Title" item.Title
        validateLength "Title" 1 100 item.Title

        match item.Description with
        | Some desc -> validateLength "Description" 0 500 desc
        | None -> None

        validatePositive "Id" item.Id
    ] |> List.choose id

    if errors.IsEmpty then Ok item else Error errors

// Convert to single error string for API
let validateTodoItemString (item: TodoItem) : Result<TodoItem, string> =
    match validateTodoItem item with
    | Ok item -> Ok item
    | Error errors -> Error (String.concat "; " errors)
```

### Conditional Validation
```fsharp
let validateUser (user: User) : Result<User, string list> =
    let errors = [
        validateRequired "Name" user.Name
        validateEmail (EmailAddress.value user.Email)

        // Only validate password if it's being changed
        if user.IsPasswordChange then
            yield! [
                validateLength "Password" 8 100 user.Password
                if not (Regex.IsMatch(user.Password, @"[A-Z]")) then
                    Some "Password must contain uppercase letter"
                if not (Regex.IsMatch(user.Password, @"[0-9]")) then
                    Some "Password must contain number"
            ] |> List.choose id
    ] |> List.choose id

    if errors.IsEmpty then Ok user else Error errors
```

### Cross-Field Validation
```fsharp
let validateDateRange (start: DateTime) (endDate: DateTime) : string option =
    if endDate < start then
        Some "End date must be after start date"
    else
        None

let validateEvent (event: Event) : Result<Event, string list> =
    let errors = [
        validateRequired "Title" event.Title
        validateDateRange event.StartDate event.EndDate

        // Custom business rule
        if event.MaxParticipants < event.CurrentParticipants then
            Some "Max participants cannot be less than current participants"
        else
            None
    ] |> List.choose id

    if errors.IsEmpty then Ok event else Error errors
```

## Request Validation

### Create Request
```fsharp
type CreateTodoRequest = {
    Title: string
    Description: string option
    Priority: Priority
}

let validateCreateRequest (req: CreateTodoRequest) : Result<CreateTodoRequest, string list> =
    let errors = [
        validateRequired "Title" req.Title
        validateLength "Title" 1 100 req.Title

        match req.Description with
        | Some desc when not (String.IsNullOrWhiteSpace(desc)) ->
            validateLength "Description" 1 500 desc
        | _ -> None
    ] |> List.choose id

    if errors.IsEmpty then Ok req else Error errors
```

### Update Request
```fsharp
let validateUpdateRequest (req: UpdateTodoRequest) : Result<UpdateTodoRequest, string list> =
    let errors = [
        validatePositive "Id" req.Id

        match req.Title with
        | Some title ->
            yield! [
                validateRequired "Title" title
                validateLength "Title" 1 100 title
            ] |> List.choose id
        | None -> ()
    ] |> List.choose id

    if errors.IsEmpty then Ok req else Error errors
```

## Business Rules

```fsharp
let validateBusinessRule (order: Order) : Result<Order, string list> =
    let errors = [
        // Check inventory
        if order.Quantity > order.AvailableStock then
            Some "Insufficient stock"

        // Check minimum order
        if order.TotalAmount < 10.0m then
            Some "Minimum order amount is $10"

        // Check business hours
        let now = DateTime.Now
        if now.Hour < 9 || now.Hour > 17 then
            Some "Orders can only be placed during business hours (9 AM - 5 PM)"

        // Check discount eligibility
        if order.DiscountPercent > 0 && not order.Customer.IsEligibleForDiscount then
            Some "Customer is not eligible for discount"
    ] |> List.choose id

    if errors.IsEmpty then Ok order else Error errors
```

## Async Validation (Database Checks)

```fsharp
let checkEmailUnique (email: string) : Async<string option> =
    async {
        let! existing = Persistence.getUserByEmail email
        return
            match existing with
            | Some _ -> Some "Email already registered"
            | None -> None
    }

let validateUserRegistration (req: RegisterRequest) : Async<Result<RegisterRequest, string list>> =
    async {
        // Sync validations first
        let syncErrors = [
            validateRequired "Username" req.Username
            validateLength "Username" 3 20 req.Username
            validateEmail req.Email
            validateLength "Password" 8 100 req.Password
        ] |> List.choose id

        if not syncErrors.IsEmpty then
            return Error syncErrors
        else
            // Async validations
            let! emailCheck = checkEmailUnique req.Email

            let asyncErrors = [emailCheck] |> List.choose id

            if asyncErrors.IsEmpty then
                return Ok req
            else
                return Error asyncErrors
    }
```

## Integration with API

```fsharp
// src/Server/Api.fs
let todoApi : ITodoApi = {
    create = fun request -> async {
        // Validate request
        match Validation.validateCreateRequest request with
        | Error errors ->
            return Error (String.concat "; " errors)
        | Ok validRequest ->
            let todo = Domain.processNewTodo validRequest
            let! saved = Persistence.insertTodo todo
            return Ok saved
    }

    update = fun request -> async {
        match Validation.validateUpdateRequest request with
        | Error errors ->
            return Error (String.concat "; " errors)
        | Ok validRequest ->
            match! Persistence.getTodoById validRequest.Id with
            | None -> return Error "Todo not found"
            | Some existing ->
                let updated = Domain.updateTodo existing validRequest
                do! Persistence.updateTodo updated
                return Ok updated
    }
}
```

## Testing Validation

```fsharp
// src/Tests/Server.Tests/ValidationTests.fs
module ValidationTests

open Expecto
open Validation

[<Tests>]
let tests =
    testList "Validation" [
        testCase "Valid todo passes" <| fun () ->
            let todo = validTodo
            let result = validateTodoItem todo
            Expect.isOk result "Should be valid"

        testCase "Missing title fails" <| fun () ->
            let todo = { validTodo with Title = "" }
            let result = validateTodoItem todo
            Expect.isError result "Should fail"

        testCase "Multiple errors accumulated" <| fun () ->
            let todo = { validTodo with Title = ""; Id = -1 }
            match validateTodoItem todo with
            | Error errors ->
                Expect.isGreaterThan errors.Length 1 "Should have multiple errors"
            | Ok _ -> failtest "Should have failed"
    ]
```

## Best Practices

### ✅ Do
- Validate at API boundary
- Accumulate all errors
- Return specific error messages
- Use reusable validators
- Test validation thoroughly

### ❌ Don't
- Skip validation on updates
- Return generic errors
- Validate in domain logic
- Let invalid data reach persistence
- Use exceptions for validation

## Verification Checklist

- [ ] Validation helpers defined
- [ ] Entity validators created
- [ ] Required fields validated
- [ ] Length/range constraints checked
- [ ] Format validation (email, URL, etc.)
- [ ] Business rules validated
- [ ] Async validation if needed
- [ ] Errors accumulated
- [ ] Clear error messages
- [ ] Integrated with API layer
- [ ] Tests written

## Related Skills

- **fsharp-backend** - Integration with API
- **fsharp-shared** - Type definitions
- **fsharp-tests** - Testing validation
