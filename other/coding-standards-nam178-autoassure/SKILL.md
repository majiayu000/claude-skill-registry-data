---
name: coding-standards
description:
  MUST load this BEFORE writing or editing any code file, or PLANNING code
  changes.
---

# General

- MUST use inline variables when possible.
- MUST use immutable types when possible.
- MUST declare request/response type in controllers (Task<IActionResult> is too
  ambiguous)
- MUST not use ! operator. Throw instead.
- Class and function names MUST be specific. Good: ToDynamoDbRow (), class
  ShippingRules. Bad: ToItem (), class BusinessUtils.
- MUST mark method as static if it does not use any class member.
- CLEAR function parameter names, "runId", "runName" instead of "id" and "name"

# Documentation &  Comments

- DO NOT WRITE ANY XML DOCS AND INLINE COMMENTS BY DEFAULT. 
- ONLY PRODUCE XML DOCS FOR:
  - If a function/method/interfaces throws, MUST document the throw, including
    throws from downstream services. BOTH in interfaces and implementation. (/// <exception cref=".." /> syntax)
  - Something non-obvious that requires explaination, examples:
    - "The user triggers this run, or NULL when it's triggered by system"
    - "How many times a document is updated, regardless of whenever content changes or not"
- Prefer better name over documentation:
Bad:
```
/// <summary>When a worker claimed this Run. Null while it is still Pending.</summary>
public DateTimeOffset? StartedAt;
```

Good:
```
public DateTimeOffset? WorkferClaimedAt;
```

# Error Raising & Handling Strategies

- When invoking functions with documented throw: 1/ AVOID invoking it in the way
  that cause it to throw. 2/ Catch-Wrap-log-Rethrow 3/ Do nothing, but document
  the throw.
- AVOID throw if possible, express error a compile-time type. Example: "User?"
  means it's null when the user not found. Example 2: TryCreate () returns false
  when dup.

# Models (Domain Layer)

- Business models are stored in Models folders.
- No external deps, API calls etc.
- Can have pure business logic methods (Good: Order.CalculateOrderDiscount ())
- Add XML doc. DO NOT MENTION anything about infra, storage. Discuss business
  domain, Good: "Customer can place maximum of 3 orders..", Bad: "This model
  stored in DynamoDB.."

# Repositories (Data Layer)

- Repository methods MUST be dumb, no business logic.
- MUST Hide storage and database implementation details.
- SHOULD reference domain models. Good: AddUser (User); Bad: InsertUser
  (UserRecord);
- MUST include OrganizationId in every query, as this is multi-tenant SaaS.
- MUST use mapper to convert domain model <-> DynamoDB, including individual
  fields. Mapping functions located at DynampDbMapper.cs,
  DynamoDbMapper.Application.cs, etc.
- MUST use consistent read by default.
- MUST use naming convention:
  - SaveX ()/TrySaveX () - create or update the object as a whole
  - TryUpdateX () - update ONLY certain fields. MUST update ONLY specific fields
    and document the fields being changed. Better, use typed args:
    FooUpdatableFields. MUST use conditional check and return false or any value
    to indicate the object was not exist.
  - TryDeleteX() - returns false when object does not exist
  - GetX (), ListX ()..
- If an entity has a relationship, like Scenario belongs to App, MUST check if
  the other entity exist when insert/updating with ConditionExpression.
- Repository methods should support filtering. This is so upper layers can
  decide whenever to filter out deleted/archived rows.
- Lifecycle state and deletion have their own protocol — See `entity-lifecycle`
  skill.
- DynamoDB can handle empty string. But can't handle empty string within a set.
  Watch out.
- In each query, MUST handle exception EXPLICITLY instead of having a "shared"
  private method for exception handling.
- MUST document limits (max 25 items per update etc)
- If data from database don't match the format in-memory (null, wrong
  type/shape, etc.), throw CorruptedDynamoDbRowException. Don't fix it or map to
  a default value. AutoAssure has not been released yet.

# Services (Business Logic Layer)

- AVOID indeterminisic code, like DateTimeOffset.UtcNow. Hard to unit-test.
  Repositories is fine as they are integration tested, but strictly MUST NOT use
  in services code.

# Controllers & Contracts (API Layer)

- MUST be well documented (XML doc) similar to AWS API Docs.
- Contracts:
  - MUST be pure, easy to understand, friendly naming.
  - MUST NOT reference domain models.
  - MUST have a reasonable length, range, and/or regex limits for EVERY
    parameter.
  - Contract <-> Model mapping is a Controller job. MUST use extension methods
    in Controllers/ContractMapper.cs, ContractMapper.Environments.cs, etc.
    (mirrors DynamoDbMapper.cs).
  - MUST use C# records using get/init accessors (NOT positional record style).
- Controllers:
  - Must specify operation name, example: [HttpPost (Name =
    "CreateApplication")]
  - If an entity has LifecycleState:
    - List API MUST return only `Active`. Add "/archived" sibling API for return
      only archived.
    - Get API MUST return only `Active` or `Archived`, and 404 for `Deleting`.
  - Non-success HTTP status codes:
    - MUST use ErrorResponse for response body, with user friendly message.
    - Must document with [ProducesResponseType (typeof (ErrorResponse), ...]
    - MUST document with XML the EXACT condition that causes the error, so
      frontend can avoid it Good: "Returns 400 when Tags has more than 10 items
      or an item is longer than 50 chars". Bad: "Tags are invalid." Bad:
      "Returns 400 when input is invalid."

# Enums & Switches

- MUST NOT use `_` (discard) in a switch over an enum. List every named enum
  value. Adding a new enum value later then breaks the build (CS8509) instead of
  silently falling into the wrong branch.
- Add a final `_ => throw new UnreachableException(...)` only to satisfy CS8524
  (unnamed enum values from a cast) — not as a stand-in for a real case.

# Functions & Methods

- Most important parameter FIRST. Good: GetUser (userId, options); Bad: GetUser
  (options, userId).
- Param name SHOULD match their type. Good: Sync (GoogleIdentity
  googleIdentity); Bad: Sync (GoogleIdentity identity).
- MUST start with verb.
