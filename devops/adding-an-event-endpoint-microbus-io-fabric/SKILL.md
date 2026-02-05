---
name: Adding an Event Endpoint
description: Creates or modify an event endpoint of a microservice. Use when explicitly asked by the user to create or modify an outbound event endpoint of a microservice.
---

## Workflow

Copy this checklist and track your progress:

```
Creating or modifying an event endpoint:
- [ ] Step 1: Read local AGENTS.md file
- [ ] Step 2: Define in service.yaml
- [ ] Step 3: Generate Boilerplate Code
- [ ] Step 4: Define Custom Types
- [ ] Step 5: Triggering an Outbound Event
- [ ] Step 6: Test the Trigger
- [ ] Step 7: Document the Microservice
- [ ] Step 8: Versioning
```

#### Step 1: Read local `AGENTS.md` file

Check for and read a local `AGENTS.md` file in that microservice's directory. The local `AGENTS.md` file contains microservice-specific instructions that should take precedence over global instructions.

#### Step 2: Define in `service.yaml`

Define the outbound event in the `events` array in the `service.yaml` of the microservice.
- The `signature` of the outbound event must follow Go function syntax exactly. Do not include a `context.Context` input argument nor an `error` output argument. The name of the event must start with `On`.
- The `description` should explain what circumstances trigger the event. It should start with the name of the event.

```yaml
events:
  - signature: OnMyNewEvent(primitiveParam string, customParam CustomType) (result string)
    description: OnMyNewEvent does X, Y and Z.
```

#### Step 3: Generate Boilerplate Code

If you've made changes to `service.yaml`, run `go generate` to generate the boilerplate code.

#### Step 4: Define Custom Types

If the new event is using non-primitive custom types such as structs, look for their definition in the API directory.
- Define the properties of any custom types as needed. Property names should be in PascalCase.
- Define JSON tags for all properties. JSON tag names should be in camelCase. Include `,omitzero` in all JSON tags.

```go
// CustomType is X, Y, Z
type CustomType struct {
	PropertyName string `json:"propertyName,omitzero"`
}
```

#### Step 5: Triggering an Outbound Event

Use the `MulticastTrigger` in the API package to trigger an outbound event and publish it to all subscribers.

```go
func (svc *Service) DeleteUser(ctx context.Context, id int) (err error) {
    user, err := svc.LoadUser(ctx, id)
    if err != nil {
        return errors.Trace(err)
    }
    // Trigger an event: iterate over the responses
    for resp := range myserviceapi.NewMulticastTrigger(svc).OnBeforeDeleteUser(ctx, user) {
        allow, err := resp.Get()
        if err != nil {
            return errors.Trace(err)
        }
        if !allow {
            return errors.New("deletion disallowed")
        }
    }

    _, err = db.sql.ExecuteContext(ctx, "DELETE FROM users WHERE id=?", id)
    if err != nil {
        return errors.Trace(err)
    }

    // Trigger an event: fire and forget, don't wait for responses
	svc.Go(ctx, func(ctx context.Context) (err error) {
        myserviceapi.NewMulticastTrigger(svc).OnUserDeleted(ctx, id)
        return nil
    })
    
    return nil
}
```

#### Step 6: Test the Trigger

Look for the integration test created in `service_test.go` for the outbound event and implement or adjust it appropriately.
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
