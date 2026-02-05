---
name: Adding a Functional Endpoint
description: Creates or modify a functional endpoint of a microservice. Use when explicitly asked by the user to create or modify a functional or RPC endpoint of a microservice.
---

## Workflow

Copy this checklist and track your progress:

```
Creating or modifying a functional endpoint:
- [ ] Step 1: Read local AGENTS.md file
- [ ] Step 2: Define in service.yaml
- [ ] Step 3: Generate Boilerplate Code
- [ ] Step 4: Define Custom Types
- [ ] Step 5: Move Implementation and Test if Renamed
- [ ] Step 6: Implement the Business Logic
- [ ] Step 7: Test the Function
- [ ] Step 8: Document the Microservice
- [ ] Step 9: Versioning
```

#### Step 1: Read local `AGENTS.md` file

Check for and read a local `AGENTS.md` file in that microservice's directory. The local `AGENTS.md` file contains microservice-specific instructions that should take precedence over global instructions.

#### Step 2: Define in `service.yaml`

Define the functional endpoint in the `functions` array in the `service.yaml` of the microservice.
- The `signature` of the functional endpoint must follow Go function syntax exactly. Do not include a `context.Context` input argument nor an `error` output argument.
- The `description` should explain what the function is doing. It should start with the name of the function.
- A `method` restricts requests to a specific HTTP method such as `GET`, `POST`, `DELETE`, `PUT`, `PATCH`, `OPTIONS` or `HEAD`. The default `ANY` accepts all requests regardless of the method.

```yaml
functions:
  - signature: MyNewFunction(primitiveParam string, customParam CustomType) (result string)
    description: MyNewFunction does X, Y and Z.
	method: ANY
```

#### Step 3: Generate Boilerplate Code

If you've made changes to `service.yaml`, run `go generate` to generate the boilerplate code.

#### Step 4: Define Custom Types

If the new function is using non-primitive custom types such as structs, look for their definition in the API directory.
- Define the properties of any custom types as needed. Property names should be in PascalCase.
- Define JSON tags for all properties. JSON tag names should be in camelCase. Include `,omitzero` in all JSON tags.

```go
// CustomType is X, Y, Z
type CustomType struct {
	PropertyName string `json:"propertyName,omitzero"`
}
```

#### Step 5: Move Implementation and Test if Renamed

If you made a change to the name of the method in the `signature` field, you need to move over its implementation in `service.go` from under the old name to the new name. Similarly, you'll need to move over the implementation of the tests in `service_test.go`. 

#### Step 6: Implement the Business Logic

Look for the function declaration in `service.go` and implement or adjust its logic appropriately.

```go
func (svc *Service) MyNewFunction(ctx context.Context, primitiveParam string, customParam CustomType) (result string, err error) {
	// Implement logic here
	return result, err
}
```

#### Step 7: Test the Function

Look for the integration test created in `service_test.go` for the function and implement or adjust it appropriately.
- Follow the pattern recommendation in the code
- Add downstream microservices or their mocks to the testing app

```go
func TestMyservice_MyNewFunction(t *testing.T) {
	// Implement testing here
}
```

#### Step 8: Document the Microservice

Generate documentation for this microservice that captures its purpose, context, and design rationale. Focus on the reasons behind decisions rather than describing what the code does. Explain design choices, tradeoffs, and the context needed for someone to safely evolve this microservice in the future. Store the result in the microservice's local `AGENTS.md` file.

#### Step 9: Versioning

Run `go generate` to version the code.
