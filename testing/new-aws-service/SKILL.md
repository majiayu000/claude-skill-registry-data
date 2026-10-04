---
name: new-aws-service
description: Scaffold a new AWS service wrapper in pkg/aws/<servicename>/ following the established cloudformationservice pattern
disable-model-invocation: false
---

When the user asks to add a new AWS service wrapper (or invokes `/new-aws-service <servicename>`), create the full package at `pkg/aws/<servicename>/` following the `pkg/aws/cloudformationservice/` pattern.

## Steps

1. **Determine the service name** from `$ARGUMENTS` or ask the user.

2. **Read the canonical example** to understand the pattern:
   - `pkg/aws/cloudformationservice/service.go` — interface + implementation
   - `pkg/aws/cloudformationservice/mock_client_test.go` — mock of the AWS client interface
   - `pkg/aws/cloudformationservice/service_test.go` — unit tests using mocks
   - `pkg/aws/cloudformationservice/service_integration_test.go` — LocalStack integration tests

3. **Create `pkg/aws/<servicename>/service.go`**:
   - Define an interface for the AWS SDK client methods you need (keeps the dependency mockable)
   - Define a `<ServiceName>Service` struct that wraps the client
   - Implement the public methods the rest of the app will call
   - Return structured errors using `fmt.Errorf("context: %w", err)` wrapping

4. **Create `pkg/aws/<servicename>/mock_client_test.go`**:
   - Hand-write a mock struct that implements the client interface
   - Include configurable return values for each method

5. **Create `pkg/aws/<servicename>/service_test.go`**:
   - Use the mock client to test each method in isolation
   - Cover happy path and key error cases

6. **Create `pkg/aws/<servicename>/service_integration_test.go`**:
   - Gate with `//go:build integration`
   - Use `testhelpers.StartLocalStack()` to spin up a container
   - Test the critical end-to-end path against real LocalStack

7. **Wire it up** in `internal/dependencies/dependencies.go` alongside existing clients.

8. After scaffolding, run `go test ./pkg/aws/<servicename>/...` to confirm unit tests pass, and remind the user to run integration tests with `-tags integration` once Docker is available.
