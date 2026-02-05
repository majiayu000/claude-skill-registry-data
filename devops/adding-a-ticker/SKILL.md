---
name: Adding a Ticker
description: Creates or modify a ticker of a microservice. Use when explicitly asked by the user to create or modify a ticker or a recurring operation for a microservice.
---

## Workflow

Copy this checklist and track your progress:

```
Creating or modifying a ticker:
- [ ] Step 1: Read local AGENTS.md file
- [ ] Step 2: Define in service.yaml
- [ ] Step 3: Generate Boilerplate Code
- [ ] Step 4: Move Implementation and Test if Renamed
- [ ] Step 5: Implement the Business Logic
- [ ] Step 6: Test the Ticker
- [ ] Step 7: Document the Microservice
- [ ] Step 8: Versioning
```

#### Step 1: Read local `AGENTS.md` file

Check for and read a local `AGENTS.md` file in that microservice's directory. The local `AGENTS.md` file contains microservice-specific instructions that should take precedence over global instructions.

#### Step 2: Define in `service.yaml`

Define the recurring operation in the `tickers` array in the `service.yaml` of the microservice.
- The `signature` of the ticker must follow Go function syntax exactly. Do not include any input arguments nor any output arguments.
- The `description` should explain what the recurring operation is doing. It should start with the name of the ticker.
- The `interval` determines the duration between consecutive iterations of the ticker.

```yaml
tickers:
  - signature: MyNewTicker()
    description: MyNewTicker does X, Y and Z.
    interval: 5m
```

#### Step 3: Generate Boilerplate Code

Run `go generate` to create the boilerplate code of the new ticker.

#### Step 4: Move Implementation and Test if Renamed

If you made a change to the name of the method in the `signature` field, you need to move over the implementation of the ticker in `service.go` from under the old name, to the newly-created declaration under the new name. Similarly, you'll need to move over the implementation of the tests in `service_test.go`. 

#### Step 5: Implement the Business Logic

Look for the ticker declaration in `service.go` and implement or adjust its logic appropriately.

```go
func (svc *Service) MyNewTicker(ctx context.Context) (err error) {
	// Implement logic here
	return err
}
```

#### Step 6: Test the Ticker

Look for the integration test created in `service_test.go` for the ticker and implement or adjust it appropriately.
- Follow the pattern recommendation in the code
- Add downstream microservices or their mocks to the testing app

```go
func TestMyservice_MyNewTicker(t *testing.T) {
	// Implement testing here
}
```

#### Step 7: Document the Microservice

Generate documentation for this microservice that captures its purpose, context, and design rationale. Focus on the reasons behind decisions rather than describing what the code does. Explain design choices, tradeoffs, and the context needed for someone to safely evolve this microservice in the future. Store the result in the microservice's local `AGENTS.md` file.

#### Step 8: Versioning

Run `go generate` to version the code.
