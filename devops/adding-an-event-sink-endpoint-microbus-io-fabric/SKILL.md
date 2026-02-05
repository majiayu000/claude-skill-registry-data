---
name: Adding an Event Sink Endpoint
description: Creates or modify an event sink endpoint of a microservice. Use when explicitly asked by the user to create or modify an inbound event sink endpoint of a microservice.
---

## Workflow

Copy this checklist and track your progress:

```
Creating or modifying a sink endpoint:
- [ ] Step 1: Read local AGENTS.md file
- [ ] Step 2: Define in service.yaml
- [ ] Step 3: Generate Boilerplate Code
- [ ] Step 4: Move Implementation and Test if Renamed
- [ ] Step 5: Implement the Business Logic
- [ ] Step 6: Test the Inbound Event Sink
- [ ] Step 7: Document the Microservice
- [ ] Step 8: Versioning
```

#### Step 1: Read local `AGENTS.md` file

Check for and read a local `AGENTS.md` file in that microservice's directory. The local `AGENTS.md` file contains microservice-specific instructions that should take precedence over global instructions.

#### Step 2: Define in `service.yaml`

Locate the definition of the outbound event in its source microservice.

Define the inbound event sink in the `sinks` array in the `service.yaml` of the microservice.
- The `signature` of the inbound event sink must be an exact copy of the outbound event of the microservice that's firing it.
- The `description` should explain what circumstances trigger the event. Copy it from the definition of the outbound event of the microservice that's firing it.
- The `source` is the package import path to the microservice that's firing the event.

```yaml
sinks:
  - signature: OnMyNewEvent(primitiveParam string, customParam CustomType) (result string)
    description: OnMyNewEvent does X, Y and Z.
    source: package/path/of/another/microservice
```

#### Step 3: Generate Boilerplate Code

If you've made changes to `service.yaml`, run `go generate` to generate the boilerplate code.

#### Step 4: Move Implementation and Test if Renamed

If you made a change to the name of the sink in the `signature` field, you need to move over its implementation in `service.go` from under the old name to the new name. Similarly, you'll need to move over the implementation of the tests in `service_test.go`. 

#### Step 5: Implement the Business Logic

Look for the function declaration in `service.go` and implement or adjust its logic appropriately.

```go
func (svc *Service) OnMyNewEvent(ctx context.Context, primitiveParam string, customParam CustomType) (result string, err error) {
	// Implement logic here
	return result, err
}
```

#### Step 6: Test the Inbound Event Sink

Look for the integration test created in `service_test.go` for the inbound event sink and implement or adjust it appropriately.
- Follow the pattern recommendation in the code
- Add downstream microservices or their mocks to the testing app

```go
func TestMyservice_OnMyNewEvent(t *testing.T) {
	// Implement testing here
}
```

#### Step 7: Document the Microservice

Generate documentation for this microservice that captures its purpose, context, and design rationale. Focus on the reasons behind decisions rather than describing what the code does. Explain design choices, tradeoffs, and the context needed for someone to safely evolve this microservice in the future. Store the result in the microservice's local `AGENTS.md` file.

#### Step 8: Versioning

Run `go generate` to version the code.
