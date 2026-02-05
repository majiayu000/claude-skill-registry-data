---
name: Adding a new microservice
description: Creates and initializes a new microservice. Use when explicitly asked by the user to create a new microservice.
---

## Workflow

Copy this checklist and track your progress:

```
Creating a new microservice:
- [ ] Step 1: Create a Directory for the New Microservice
- [ ] Step 2: Create `doc.go` with Code Generation Directive
- [ ] Step 3: Generate Initial `service.yaml`
- [ ] Step 4: Fill in `service.yaml`
- [ ] Step 5: Generate Microservice File Structure
- [ ] Step 6: Add the Microservice to the Main Application
- [ ] Step 7: Propose Features
```

#### Step 1: Create a Directory for the New Microservice

Each microservice is kept in a separate directory. Create a new directory for the new microservice.

```bash
mkdir -p myservice
cd myservice
```

#### Step 2: Create `doc.go` with Code Generation Directive

Create `doc.go` with the directive to trigger the code generator.

```go
package myservice

//go:generate go run github.com/microbus-io/fabric/codegen

```

#### Step 3: Generate Initial `service.yaml`

Run `go generate` to create the initial `service.yaml` file.

**Important** Do not attempt to create `service.yaml` yourself from scratch. Always let the code generator initialize it.

#### Step 4: Fill in `service.yaml`

The `service.yaml` file is the blueprint of your microservice. Fill in the `general` section:
- The `host` defines the host name under which this microservice will be addressable. It must be unique across the application. Use reverse domain notation, e.g. `myservice.myproject.mycompany`.
- The `description` should explain what this microservice is about.

```yaml
general:
  host: myservice.myproject.mycompany
  description: My microservice does X, Y, and Z
```

**Important**: Do not fill in any other section of `service.yaml` unless explicitly asked to do so by the user.

#### Step 5: Generate Microservice File Structure

Run `go generate` again to generate the file structure of the microservice.

#### Step 6: Add the Microservice to the Main Application

Add the new microservice to the `app` in `main.go`, if not already added.
Note that `main.go` is typically located in the `main` directory of the project, not inside the directory of the microservice.
The order is important: add the new microservice after the core infrastructure microservices are added, and before the HTTP ingress proxy is added.

```go
func main() {
	app := application.New()

	// The configurator must be first
	app.Add(
		configurator.NewService(),
	)

	// Infrastructure services
	app.Add(
		httpegress.NewService(),
		openapiportal.NewService(),
		metrics.NewService(),
	)

	// Add your solution microservices here
	app.Add(
		myservice.NewService(),
	)

	// HTTP ingress proxy is last
	app.Add(
		httpingress.NewService(),
	)

	err := app.Run()
	if err != nil {
		fmt.Fprintf(os.Stderr, "%+v", err)
		os.Exit(19)
	}
}
```

#### Step 7: Propose Features

If you have an idea for what the microservice should include, prepare a proposal categorizing them by feature:
- Configuration properties
- Functional endpoints (RPCs)
- Outbound events
- Inbound event sinks
- Web handler endpoints
- Tickers (recurring operations)
- Metrics

Save the proposal in `AGENTS.md`, then show it to the user and seek additional instructions.
