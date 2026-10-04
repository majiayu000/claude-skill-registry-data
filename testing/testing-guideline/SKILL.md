---
name: testing-guideline
description:
  MUST load this BEFORE writing or editing any unit test or integration test in
  this repo.
---

## Overall

- Test method format: <MethodName>_When<SomeConditions>_<SomeExpectedResult>()
- Setup-test-verify pattern. Use inline comment: // setup, // test, // verify

## Unit Testing

- Assemby: A2.Server.UnitTests
- Not everything should be unit tested:
  - Test only functions, methods that have well defined input, output or
    behaviour.
  - Test pure functions/classes only. No controllers

## Local Integration Testing

- Assemby: A2.Server.Tests
- MUST use ASP.NET integration tests (`WebApplicationFactory`, real HTTP
  client).
- MUST fake downstream deps (realistic in-memory, no external calls), never
  mocks/stubs.
- To fake DynamoDB, MUST use DynamoDB local.
- Duplication across tests is fine — don't extract shared helpers.
- MUST produce four types of tests:
  - Type 1: Realistic test data, happy path.
  - Type 2: Bad data: extra long string, too short, large integer, negative
    integer.
  - Type 3: Invalid shape data: nulls for required fields, (might need to send
    RAW json), missing fields, wrong data types etc.
  - Type 4: Unauthorized and/or unauthenticaed access.
