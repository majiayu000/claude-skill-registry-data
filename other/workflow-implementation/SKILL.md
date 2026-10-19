---
name: workflow-implementation
description: >
  Implement domain workflows as composable pipelines (C# by default, F# on request) following "Domain Modeling Made Functional."
  Use this skill whenever implementing a workflow, composing pipeline steps, doing dependency injection
  via partial application, handling errors with Result/bind/map, or building computation expressions.
  Trigger on: "implement workflow", "compose pipeline", "Result type", "bind", "map", "mapError",
  "railroad oriented", "two-track", "partial application", "dependency injection functional",
  "computation expression", "asyncResult", "implement validation step", "implement pricing",
  "compose functions", "function adapter", "composition root". Also trigger when the user has
  domain types (from dmf:domain-modeling) and needs to write the implementation code.
---

# Implementing Workflows as Pipelines (DMF Methodology)

This skill covers implementing domain workflows by composing small, focused functions
into pipelines. It assumes domain types already exist (see dmf:domain-modeling skill).

## Language

Code in this skill is F#, the notation of the book.
Write C# unless the user asks for F# or the project is an F# project: **read** `${CLAUDE_PLUGIN_ROOT}/references/csharp-mapping.md` first and express every pattern below with it.
The project profile's Mapping section names the functional library and wins over the mapping's defaults.

## Core Architecture

A workflow is a pipeline of transformations:

```
UnvalidatedOrder
  |> validateOrder        -- UnvalidatedOrder -> Result<ValidatedOrder, ValidationError>
  |> priceOrder           -- ValidatedOrder -> Result<PricedOrder, PricingError>
  |> acknowledgeOrder     -- PricedOrder -> OrderAcknowledgmentSent option
  |> createEvents         -- PricedOrder -> ... -> PlaceOrderEvent list
```

Each step:
1. Is a standalone, stateless function
2. Takes explicit dependencies as parameters
3. Documents its effects in the return type
4. Can be tested in isolation with fake dependencies

## Implementation Sequence

Follow this order when implementing a workflow:

1. **Simple type constructors** - `OrderId.create`, `String50.create`, etc.
2. **Helper functions** - `toCustomerInfo`, `toAddress`, `toValidatedOrderLine`, etc.
3. **Each pipeline step** - `validateOrder`, `priceOrder`, `acknowledgeOrder`, `createEvents`
4. **Pipeline composition** - The top-level `placeOrder` function
5. **Composition root** - Wire up real dependencies

## Step 1: Implement Without Effects First

Start by implementing each step WITHOUT `Result` or `Async`. Use exceptions for errors.
This lets you focus on the transformation logic and composition.

```fsharp
// First pass: no Result, just throw on error
let validateOrder : ValidateOrder =
    fun checkProductCodeExists checkAddressExists unvalidatedOrder ->
        let orderId =
            unvalidatedOrder.OrderId |> OrderId.create  // throws if invalid
        let customerInfo =
            unvalidatedOrder.CustomerInfo |> toCustomerInfo
        let shippingAddress =
            unvalidatedOrder.ShippingAddress |> toAddress checkAddressExists
        let lines =
            unvalidatedOrder.Lines
            |> List.map (toValidatedOrderLine checkProductCodeExists)
        {
            OrderId = orderId
            CustomerInfo = customerInfo
            ShippingAddress = shippingAddress
            BillingAddress = billingAddress
            Lines = lines
        }
```

Then add `Result` back in a second pass (see Step 4).

## Step 2: Helper Functions

Each helper converts an unvalidated sub-structure to a domain type.

```fsharp
let toCustomerInfo (customer: UnvalidatedCustomerInfo) : CustomerInfo =
    let firstName = customer.FirstName |> String50.create
    let lastName = customer.LastName |> String50.create
    let emailAddress = customer.EmailAddress |> EmailAddress.create
    let name : PersonalName = { FirstName = firstName; LastName = lastName }
    { Name = name; EmailAddress = emailAddress }

let toAddress (checkAddressExists: CheckAddressExists) unvalidatedAddress =
    let checkedAddress = checkAddressExists unvalidatedAddress
    let (CheckedAddress checkedAddress) = checkedAddress
    let addressLine1 = checkedAddress.AddressLine1 |> String50.create
    // ... remaining fields ...
    { AddressLine1 = addressLine1; (* ... *) }
```

**Key pattern:** Dependencies that a helper needs are passed as parameters to that
helper, NOT accessed globally.

## Step 3: Function Adapters

When a function's output doesn't match the next function's input, create an adapter.

### Predicate to Passthrough

Convert `'a -> bool` to `'a -> 'a` (returns the input if predicate passes, else fails):

```fsharp
let predicateToPassthru errorMsg f x =
    if f x then x
    else failwith errorMsg

// Usage: adapt checkProductCodeExists from bool-returning to passthrough
let toProductCode (checkProductCodeExists: CheckProductCodeExists) productCode =
    let checkProduct productCode =
        let errorMsg = sprintf "Invalid: %A" productCode
        predicateToPassthru errorMsg checkProductCodeExists productCode
    productCode
    |> ProductCode.create
    |> checkProduct
```

### Tee (dead-end adapter)

Convert `'a -> unit` to `'a -> 'a` (call the function for side effects, return input):

```fsharp
let tee f x =
    f x
    x
// Usage: slot logging into a pipeline
// x |> tee (fun order -> log "Processing order %A" order.OrderId)
```

Read `references/function-adapters.md` for the full catalog.

## Step 4: Add Result-Based Error Handling

### The Result Module

```fsharp
module Result =
    let bind f = function
        | Ok success -> f success
        | Error failure -> Error failure

    let map f = function
        | Ok success -> Ok (f success)
        | Error failure -> Error failure

    let mapError f = function
        | Ok success -> Ok success
        | Error failure -> Error (f failure)

    let sequence (results: Result<'a,'e> list) : Result<'a list, 'e> =
        let prepend firstR restR =
            match firstR, restR with
            | Ok first, Ok rest -> Ok (first :: rest)
            | Error e, _ -> Error e
            | _, Error e -> Error e
        List.foldBack prepend results (Ok [])
```

### The `result` Computation Expression

```fsharp
type ResultBuilder() =
    member _.Return(x) = Ok x
    member _.Bind(x, f) = Result.bind f x
    member _.ReturnFrom(x) = x

let result = ResultBuilder()
```

### Rewriting with `result { }`

```fsharp
let validateOrder : ValidateOrder =
    fun checkProductCodeExists checkAddressExists unvalidatedOrder ->
        result {
            let! orderId =
                unvalidatedOrder.OrderId
                |> OrderId.create
                |> Result.mapError ValidationError
            let! customerInfo =
                unvalidatedOrder.CustomerInfo |> toCustomerInfo
            let! shippingAddress =
                unvalidatedOrder.ShippingAddress
                |> toAddress checkAddressExists
            let! lines =
                unvalidatedOrder.Lines
                |> List.map (toValidatedOrderLine checkProductCodeExists)
                |> Result.sequence
            return {
                OrderId = orderId
                CustomerInfo = customerInfo
                ShippingAddress = shippingAddress
                Lines = lines
            }
        }
```

**Key rules:**
- `let!` unwraps a `Result` - use for any step that can fail
- `let` (no bang) for steps that always succeed
- All errors in the block must be the same type → use `Result.mapError` to lift
- `return` wraps the final value in `Ok`

### Converting Error Types with `mapError`

Each step may have its own error type. The pipeline needs a common error type.

```fsharp
type PlaceOrderError =
    | Validation of ValidationError
    | Pricing of PricingError
    | RemoteService of RemoteServiceError

let placeOrder : PlaceOrderWorkflow =
    fun unvalidatedOrder ->
        result {
            let! validatedOrder =
                validateOrder checkProductExists checkAddressExists unvalidatedOrder
                |> Result.mapError PlaceOrderError.Validation
            let! pricedOrder =
                priceOrder getProductPrice validatedOrder
                |> Result.mapError PlaceOrderError.Pricing
            let acknowledgmentOption =
                acknowledgeOrder pricedOrder
            let events =
                createEvents pricedOrder acknowledgmentOption
            return events
        }
```

### Handling Lists of Results

When mapping produces `Result<'a,'e> list` but you need `Result<'a list, 'e>`:

```fsharp
let! lines =
    unvalidatedOrder.Lines
    |> List.map (toValidatedOrderLine checkProductCodeExists)  // Result list
    |> Result.sequence  // list Result → Result of list
```

For better performance, combine map + sequence into `traverse`.

## Step 5: Dependency Injection via Partial Application

Dependencies flow top-down: top-level function receives all deps, passes them to children.

```fsharp
// Low-level: needs checkProductCodeExists
let toProductCode checkProductCodeExists productCode = ...

// Mid-level: also needs it (to pass to toProductCode)
let toValidatedOrderLine checkProductCodeExists unvalidatedOrderLine = ...
    let productCode = unvalidatedOrderLine.ProductCode |> toProductCode checkProductCodeExists
    ...

// Top-level: receives ALL deps, passes them down
let validateOrder : ValidateOrder =
    fun checkProductCodeExists checkAddressExists unvalidatedOrder -> ...
```

### Baking in Dependencies with Partial Application

Before composing the pipeline, partially apply dependencies:

```fsharp
let placeOrder
    checkProductExists        // dependency
    checkAddressExists        // dependency
    getProductPrice           // dependency
    createAcknowledgmentLetter // dependency
    sendOrderAcknowledgment   // dependency
    : PlaceOrderWorkflow =

    fun unvalidatedOrder ->
        let validatedOrder =
            unvalidatedOrder
            |> validateOrder checkProductExists checkAddressExists
        let pricedOrder =
            validatedOrder |> priceOrder getProductPrice
        let acknowledgmentOption =
            pricedOrder
            |> acknowledgeOrder createAcknowledgmentLetter sendOrderAcknowledgment
        let events = createEvents pricedOrder acknowledgmentOption
        events
```

### Pre-building Dependencies

If a dependency itself has sub-dependencies, bake those in before passing:

```fsharp
// checkAddressExists needs endpoint + credentials
let checkAddressExists endPoint credentials address = ...

// Bake in before passing to the workflow
let placeOrderWorkflow =
    let endPoint = config.AddressServiceEndpoint
    let credentials = config.AddressServiceCredentials
    let checkAddressExists = checkAddressExists endPoint credentials
    placeOrder checkProductExists checkAddressExists getProductPrice ...
```

## Step 6: The Composition Root

The top-level function that wires real implementations to all dependencies.

```fsharp
let app : WebPart =
    // Set up real services
    let checkProductExists = ProductService.checkExists connectionString
    let checkAddressExists = AddressService.check endPoint credentials
    let getProductPrice = PricingService.getPrice connectionString
    let createAcknowledgmentLetter = AcknowledgmentService.createLetter
    let sendOrderAcknowledgment = EmailService.send smtpConfig

    // Wire up the workflow
    let placeOrder =
        PlaceOrderWorkflow.placeOrder
            checkProductExists
            checkAddressExists
            getProductPrice
            createAcknowledgmentLetter
            sendOrderAcknowledgment

    // Set up routing
    choose [
        POST >=> path "/placeOrder"
            >=> deserializeOrder
            >=> placeOrder
            >=> postEvents
            >=> toHttpResponse
    ]
```

## Step 7: Adding Async

For the full async+result pipeline, use `AsyncResult` and `asyncResult { }`:

```fsharp
type AsyncResult<'success, 'failure> = Async<Result<'success, 'failure>>

module AsyncResult =
    let ofResult x = async { return x }
    let map f x = async { let! r = x in return Result.map f r }
    let bind f x = async { let! r = x in match r with Ok s -> return! f s | Error e -> return Error e }
    let mapError f x = async { let! r = x in return Result.mapError f r }
```

Read `references/function-adapters.md` for the full adapter catalog.
Read `references/error-handling.md` for the complete railroad-oriented programming guide.

## Testing

All dependencies are fake-able because they're function parameters:

```fsharp
[<Test>]
let ``If product exists, validation succeeds``() =
    // Arrange: stub dependencies
    let checkAddressExists address = CheckedAddress address
    let checkProductCodeExists productCode = true
    let unvalidatedOrder = { ... }

    // Act
    let result =
        validateOrder checkProductCodeExists checkAddressExists unvalidatedOrder

    // Assert
    match result with
    | Ok _ -> ()  // pass
    | Error e -> Assert.Fail(sprintf "Expected Ok, got Error: %A" e)

[<Test>]
let ``If product doesn't exist, validation fails``() =
    let checkProductCodeExists productCode = false  // always fail
    // ... rest of test
```

No mocking libraries needed. Just define lambdas.

## Checklist

- [ ] Each step is a pure, stateless function
- [ ] All dependencies are explicit function parameters
- [ ] Error types are aligned via `mapError` before composition (C#: every failure is built from the workflow's error union)
- [ ] `result { }` or `asyncResult { }` hides the bind/map plumbing (C#: LINQ query syntax or a fluent chain)
- [ ] Lists of results use `Result.sequence` (C#: the project's `Sequence` helper, or `F.HarvestErrors` to report every failure)
- [ ] Composition root is the only place real implementations are wired
- [ ] Each step is independently testable with fake dependencies

## Output Format

Save the output as **`06-workflow-pipelines.md`** in the design directory `cc-docs/design/<topic>/` (see `${CLAUDE_PLUGIN_ROOT}/references/design-directory.md` for choosing `<topic>`).
Start the file with a `> Source:` line naming the files it consumed (used for staleness checks).

**Input files:** `04-domain-model.md` (domain types + workflow type signatures) + `05-call-chains.md` §7 if it exists (workflow-to-service mapping from the `lowy` plugin, showing which service chain implements each workflow).
If `05-call-chains.md` does not exist, organize the output by the workflows in `01-domain-discovery.md` §6 (if it exists) and the workflow signatures in `04-domain-model.md`, place each workflow in the bounded context that owns it, wire dependencies in the composition root, and say in the output that no call-chain mapping was used.

**Output file:** `06-workflow-pipelines.md` - consumed by Phase 8 (`dmf:serialization-persistence` - to identify I/O points that need bridging).

Organize the output by workflow. For each workflow, include:
1. Pipeline overview (step sequence with type signatures)
2. Each step's implementation (function body)
3. Adapter functions (shape mismatches resolved)
4. Error type unification (`mapError` to common pipeline error; C#: the error union and its `ToError()` adapter)
5. Composed pipeline (the full chain with partial application)
6. Composition root wiring (how dependencies are injected at the top level)
7. Test examples (fake dependencies, expected inputs/outputs)
