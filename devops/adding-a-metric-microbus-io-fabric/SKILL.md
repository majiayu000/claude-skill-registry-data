---
name: Adding a Metric
description: Creates or modify a metric of a microservice. Use when explicitly asked by the user to create or modify a custom metric for a microservice, or when it makes sense measure a certain operation taken by the microservice.
---

## Workflow

Copy this checklist and track your progress:

```
Creating or modifying a metric:
- [ ] Step 1: Read local AGENTS.md file
- [ ] Step 2: Define in service.yaml
- [ ] Step 3: Generate Boilerplate Code
- [ ] Step 4: Setting the Value of the Metric
- [ ] Step 5: Move Implementation and Test if Renamed
- [ ] Step 6: Handle the Callback
- [ ] Step 7: Test the Callback
- [ ] Step 8: Document the Microservice
- [ ] Step 9: Versioning
```

#### Step 1: Read local `AGENTS.md` file

Check for and read a local `AGENTS.md` file in that microservice's directory. The local `AGENTS.md` file contains microservice-specific instructions that should take precedence over global instructions.

#### Step 2: Define in `service.yaml`

Define the custom metric in the `metrics` array in the `service.yaml` of the microservice.
- The `signature` of the metric must follow Go function syntax exactly. The first input argument must be either of type `int`, `float64` or `time.Duration`. Additional input arguments can be added to represent labels of the metric, these have to be of type `string` or otherwise be convertible to a `string`. Do not include any output arguments.
- The `description` should explain what the metric is measuring. It should start with the name of the metric.
- The `kind` of the metric can be either `counter` (default), `gauge` or `histogram`.
- For histograms, `buckets` define the bucket boundaries.
- A `callback` can be enabled to observe the value of the metric just in time, for example, when reporting a gauge whose value is expensive to produce such as available disk space or memory.

```yaml
metrics:
  - signature: MyNewMetric(value int, label string)
    description: MyNewMetric measures X.
    kind: Histogram
    buckets: [1,2,5,10,100]
	callback: false
```

#### Step 3: Generate Boilerplate Code

If you've made changes to `service.yaml`, run `go generate` to generate the boilerplate code.

#### Step 4: Setting the Value of the Metric

The setter function of the custom metric is exposed via the `svc` receiver. For counters the setter is named `AddMyMetric` while for gauges and histograms it is `RecordMyMetric`.

```go
func (svc *Service) ProcessFile(ctx context.Context, content []byte) error {
	err := svc.process(ctx, content)
	if err != nil {
		svc.AddFileSizeBytes(len(content), "failed") // Add to the counter FileSizeBytes, with a label
		return errors.Trace(err)
	}
	svc.AddFileSizeBytes(len(content), "success") // Add to the counter FileSizeBytes, with a label
	return nil
}
```

#### Step 5: Move Implementation and Test if Renamed

If a `callback` is enabled, and you made a change to the name of the custom metric in the `signature` field, you need to move over the implementation of the callback in `service.go` from under the old name to the new name. Similarly, you'll need to move over the implementation of the tests in `service_test.go`. 

#### Step 6: Handle the Callback

If you enabled a `callback`, look for the `OnObserveMyNewMetric` function in `service.go` and implement it to record the value of the corresponding metric.

```go
func (svc *Service) OnObserveFreeMemory(ctx context.Context) error {
	mem, err := svc.calculateFreeMemory()
	if err != nil {
		return errors.Trace(err)
	}
	svc.RecordFreeMemoryBytes(mem) // Record the gauge FreeMemoryBytes
	return nil
}
```

#### Step 7: Test the Callback

If you enabled a `callback`, look for the integration test created in `service_test.go` and implement or adjust it appropriately.
- Follow the pattern recommendation in the code
- Add downstream microservices or their mocks to the testing app

```go
func TestMyservice_OnObserveMyNewMetric(t *testing.T) {
	// Implement testing here
}
```

#### Step 8: Document the Microservice

Generate documentation for this microservice that captures its purpose, context, and design rationale. Focus on the reasons behind decisions rather than describing what the code does. Explain design choices, tradeoffs, and the context needed for someone to safely evolve this microservice in the future. Store the result in the microservice's local `AGENTS.md` file.

#### Step 9: Versioning

Run `go generate` to version the code.
