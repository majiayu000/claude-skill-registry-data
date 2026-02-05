---
name: Adding a Configuration Property
description: Creates or modify a configuration property of a microservice. Use when explicitly asked by the user to create or modify a configuration property of a microservice, or when it makes sense to externalize a certain setting of the microservice.  
---

## Workflow

Copy this checklist and track your progress:

```
Creating or modifying a configuration property:
- [ ] Step 1: Read local AGENTS.md file
- [ ] Step 2: Define in service.yaml
- [ ] Step 3: Generate Boilerplate Code
- [ ] Step 4: Accessing the Configuration Property
- [ ] Step 5: Move Implementation and Test if Renamed
- [ ] Step 6: Handle the Callback
- [ ] Step 7: Test the Callback
- [ ] Step 8: Document the Microservice
- [ ] Step 9: Versioning
```

#### Step 1: Read local `AGENTS.md` file

Check for and read a local `AGENTS.md` file in that microservice's directory. The local `AGENTS.md` file contains microservice-specific instructions that should take precedence over global instructions.

#### Step 2: Define in `service.yaml`

Define the configuration property in the `configs` array in the `service.yaml` of the microservice.
- The `signature` of the configuration property must follow Go function syntax exactly. Do not include any input argument and return a single output argument of type `string`, `int`, `bool`, `time.Duration` or `float`.
- The `description` should explain the purpose of the configuration property. It should start with the name of the configuration property.
- A `default` value may be set for the configuration property.
- An optional `validation` rule can be set to validate any values set for the configuration property.
- `secret` indicates if the configuration property is a secret.
- A `callback` can be enabled to catch changes to the value of the configuration property, for example, in order to reopen a connection to an external resource.

```yaml
configs:
  - signature: MyNewConfig() (value int)
    description: MyNewConfig is X, Y and Z.
    default: 1
    validation: int (1,100]
    secret: false
    callback: false
```

Validation rules can be any of the following:
- `str` followed by a regexp: `str ^[a-zA-Z0-9]+$`
- `bool`
- `int` followed by an open, closed or mixed interval: `int [0,60]`
- `float` followed by an open, closed or mixed interval: `float [0.0,1.0)`
- `dur` followed by an open, closed or mixed interval of Go durations: `dur (0s,24h]`
- `set` followed by a pipe-separated list of values: `set Red|Green|Blue`
- `url`
- `email`
- `json`

#### Step 3: Generate Boilerplate Code

If you've made changes to `service.yaml`, run `go generate` to generate the boilerplate code.

#### Step 4: Accessing the Configuration Property

The getter function of the configuration property is exposed via the `svc` receiver.

```go
func (svc *Service) processWithRetries(ctx context.Context) error {
	maxRetries := svc.MaxRetries() // Generated getter from config

	for i := 0; i < maxRetries; i++ {
		err := svc.attemptOperation(ctx)
		if err == nil {
			return nil
		}
		svc.Log().Warn("Operation failed, retrying", "attempt", i+1, "error", err)
	}

	return errors.New("max retries exceeded")
}
```

#### Step 5: Move Implementation and Test if Renamed

If a `callback` is enabled, and you made a change to the name of the configuration property in the `signature` field, you need to move over the implementation of the callback in `service.go` from under the old name to the new name. Similarly, you'll need to move over the implementation of the tests in `service_test.go`. 

#### Step 6: Handle the Callback

If you enabled a `callback`, look for the `OnChangedMyConfig` function in `service.go` and implement the handling of the new value of the property.

For example:

```go
func (svc *Service) OnChangedDatabaseConnectionString(ctx context.Context) error {
    svc.db.Close()
    svc.db, err = sql.Open("mysql", svc.DatabaseConnectionString())
    if err != nil {
        return errors.Trace(err)
    }
    return nil
}
```

#### Step 7: Test the Callback

If you enabled a `callback`, look for the integration test created in `service_test.go` and implement or adjust it appropriately.
- Follow the pattern recommendation in the code
- Add downstream microservices or their mocks to the testing app

```go
func TestMyservice_OnChangedMyNewConfig(t *testing.T) {
	// Implement testing here
}
```

#### Step 8: Document the Microservice

Generate documentation for this microservice that captures its purpose, context, and design rationale. Focus on the reasons behind decisions rather than describing what the code does. Explain design choices, tradeoffs, and the context needed for someone to safely evolve this microservice in the future. Store the result in the microservice's local `AGENTS.md` file.

#### Step 9: Versioning

Run `go generate` to version the code.
