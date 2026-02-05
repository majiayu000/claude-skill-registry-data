---
name: run-provider
description: Build and run the Nomos Terraform Remote State Provider. Use this when testing the provider, verifying functionality, or running the provider binary locally.
license: MIT
---

# Run Provider

This skill provides a consistent way to build and run the Nomos Terraform Remote State Provider, including development workflows, debugging, and deployment scenarios.

## When to Use This Skill

Use this skill when you need to:
- Build the provider binary
- Run the provider locally for testing
- Test provider functionality manually
- Debug provider behavior
- Verify provider starts correctly
- Test gRPC endpoints
- Install the provider system-wide
- Prepare for deployment

## Prerequisites

- Go 1.25.5 or later installed
- Project dependencies installed (`go mod download`)
- Clean test results (`make test`)
- Write access to build directory (`bin/`)

## Build Commands

### 1. Build the Provider

To build the provider binary:

```bash
make build
```

This command:
- Runs `go mod tidy` to ensure dependencies are correct
- Creates the `bin/` directory if it doesn't exist
- Compiles the binary with version information
- Outputs to `bin/nomos-provider-terraform-remote-state`

**Expected output:**
```
Building nomos-provider-terraform-remote-state...
Build complete: bin/nomos-provider-terraform-remote-state
```

**Version Information Embedded:**
- Version: Git tag or "dev"
- Commit: Git commit SHA
- Build time: UTC timestamp

### 2. Build and Run

To build and immediately run the provider:

```bash
make run
```

This command:
- Builds the binary (same as `make build`)
- Executes the provider
- Shows provider output in the terminal

### 3. Clean Build

To remove old build artifacts and rebuild:

```bash
make clean
make build
```

The clean command removes:
- `bin/` directory and contents
- Coverage files (`coverage.out`, `coverage.html`)
- Go build cache
- Go test cache

### 4. Install Provider System-Wide

To install the provider to `$GOPATH/bin`:

```bash
make install
```

This allows running the provider from anywhere:
```bash
nomos-provider-terraform-remote-state
```

**Installation location:** `$(go env GOPATH)/bin/nomos-provider-terraform-remote-state`

## Running the Provider

### Basic Execution

Run the compiled binary directly:

```bash
./bin/nomos-provider-terraform-remote-state
```

### Run with Arguments

The provider accepts command-line arguments:

```bash
# Show version information
./bin/nomos-provider-terraform-remote-state -version

# Run on specific port
./bin/nomos-provider-terraform-remote-state -port 50051

# Enable debug logging
./bin/nomos-provider-terraform-remote-state -debug

# Show help
./bin/nomos-provider-terraform-remote-state -help
```

### Run in Background

To run the provider as a background process:

```bash
# Start in background
./bin/nomos-provider-terraform-remote-state &

# Get process ID
echo $!

# Stop later
kill <PID>
```

### Run with Environment Variables

Configure the provider using environment variables:

```bash
# Set log level
export LOG_LEVEL=debug

# Set port
export PROVIDER_PORT=50051

# Run provider
./bin/nomos-provider-terraform-remote-state
```

## Development Workflow

### Quick Development Cycle

1. **Make code changes**
2. **Run tests:**
   ```bash
   make test
   ```
3. **Build and run:**
   ```bash
   make run
   ```
4. **Verify functionality** (in another terminal)
5. **Stop provider:** `Ctrl+C`

### Full Verification Cycle

For comprehensive verification:

```bash
# 1. Format code
make fmt

# 2. Run static analysis
make vet

# 3. Run tests
make test

# 4. Build provider
make build

# 5. Run provider
make run
```

Or use the complete verification target:

```bash
make verify
```

### Rapid Testing Loop

For quick iteration during development:

```bash
# Terminal 1: Watch mode (requires entr or similar)
ls **/*.go | entr -r make run

# Terminal 2: Test gRPC calls
grpcurl -plaintext localhost:50051 list
```

## Testing Provider Functionality

### Check Provider Health

Using grpcurl (install from https://github.com/fullstorydev/grpcurl):

```bash
# List available services
grpcurl -plaintext localhost:50051 list

# Call health check
grpcurl -plaintext localhost:50051 nomos.provider.v1.Provider/Health
```

### Test Provider Info

```bash
# Get provider information
grpcurl -plaintext localhost:50051 nomos.provider.v1.Provider/Info
```

Expected response:
```json
{
  "alias": "tfstate",
  "version": "0.1.0",
  "type": "state"
}
```

### Test Provider Initialization

```bash
# Initialize with configuration
grpcurl -plaintext -d '{
  "config": {
    "backend": {
      "type": "local",
      "path": "/tmp/terraform.tfstate"
    }
  }
}' localhost:50051 nomos.provider.v1.Provider/Init
```

### Test State Fetching

```bash
# Fetch state
grpcurl -plaintext -d '{
  "query": {
    "path": "outputs.bucket_name"
  }
}' localhost:50051 nomos.provider.v1.Provider/Fetch
```

## Debugging

### Enable Debug Logging

Build with debug flags:

```bash
go build -gcflags="all=-N -l" -o bin/provider-debug ./cmd/provider
```

Run with debugger (using delve):

```bash
# Install delve
go install github.com/go-delve/delve/cmd/dlv@latest

# Run with debugger
dlv exec ./bin/provider-debug
```

### Check Build Information

View embedded version information:

```bash
# Linux/macOS
strings ./bin/nomos-provider-terraform-remote-state | grep version

# Or run with version flag
./bin/nomos-provider-terraform-remote-state -version
```

### View gRPC Traffic

Use grpc-dump or similar tools:

```bash
# Set gRPC debug environment
export GRPC_GO_LOG_VERBOSITY_LEVEL=99
export GRPC_GO_LOG_SEVERITY_LEVEL=info

# Run provider
./bin/nomos-provider-terraform-remote-state
```

### Profile Performance

Run with profiling enabled:

```bash
# CPU profiling
go run -cpuprofile=cpu.prof ./cmd/provider

# Memory profiling  
go run -memprofile=mem.prof ./cmd/provider

# Analyze profiles
go tool pprof cpu.prof
```

## Common Scenarios

### Scenario 1: Quick Test After Code Change

```bash
make test && make run
```

### Scenario 2: Full Build Verification

```bash
make verify && make build && ./bin/nomos-provider-terraform-remote-state -version
```

### Scenario 3: Clean Rebuild

```bash
make clean && make deps && make build
```

### Scenario 4: Test with Real Configuration

```bash
# Create test config
cat > /tmp/provider-config.json <<EOF
{
  "backend": {
    "type": "local",
    "path": "/tmp/terraform.tfstate"
  }
}
EOF

# Run provider with config
./bin/nomos-provider-terraform-remote-state -config /tmp/provider-config.json
```

### Scenario 5: System-Wide Installation

```bash
make install
which nomos-provider-terraform-remote-state
nomos-provider-terraform-remote-state -version
```

## Binary Information

### Binary Location
- **Development:** `bin/nomos-provider-terraform-remote-state`
- **Installed:** `$(go env GOPATH)/bin/nomos-provider-terraform-remote-state`

### Binary Size
Typical binary size: ~15-25 MB (varies by platform and build flags)

### Supported Platforms
- Linux (amd64, arm64)
- macOS (amd64, arm64)
- Windows (amd64)

### Cross-Compilation

Build for different platforms:

```bash
# Linux AMD64
GOOS=linux GOARCH=amd64 go build -o bin/provider-linux-amd64 ./cmd/provider

# macOS ARM64 (Apple Silicon)
GOOS=darwin GOARCH=arm64 go build -o bin/provider-darwin-arm64 ./cmd/provider

# Windows AMD64
GOOS=windows GOARCH=amd64 go build -o bin/provider-windows-amd64.exe ./cmd/provider
```

## Troubleshooting

### Build Fails

**Symptom:** Build fails with dependency errors

**Solution:**
```bash
# Clean and refresh dependencies
make clean
go mod tidy
go mod download
make build
```

### Provider Won't Start

**Symptom:** Binary exits immediately or fails to start

**Solution:**
1. Check for port conflicts:
   ```bash
   lsof -i :50051
   ```
2. Run with debug output:
   ```bash
   ./bin/nomos-provider-terraform-remote-state -debug
   ```
3. Check permissions:
   ```bash
   ls -la ./bin/nomos-provider-terraform-remote-state
   chmod +x ./bin/nomos-provider-terraform-remote-state
   ```

### Binary Not Found After Install

**Symptom:** `command not found` after `make install`

**Solution:**
1. Check GOPATH:
   ```bash
   go env GOPATH
   ```
2. Add to PATH:
   ```bash
   export PATH="$PATH:$(go env GOPATH)/bin"
   ```
3. Verify installation:
   ```bash
   ls -la $(go env GOPATH)/bin/nomos-provider-terraform-remote-state
   ```

### Version Information Missing

**Symptom:** `./bin/provider -version` shows "dev"

**Solution:** This is normal for local builds. Version comes from git tags:
```bash
# Create and tag a release
git tag v0.1.0
make build
./bin/nomos-provider-terraform-remote-state -version
```

### gRPC Connection Refused

**Symptom:** Cannot connect to provider with grpcurl

**Solution:**
1. Verify provider is running:
   ```bash
   ps aux | grep nomos-provider
   ```
2. Check listening port:
   ```bash
   lsof -i :50051
   ```
3. Try localhost variants:
   ```bash
   grpcurl -plaintext localhost:50051 list
   grpcurl -plaintext 127.0.0.1:50051 list
   ```

## Best Practices

1. **Test before building**: Always run `make test` before `make build`
2. **Clean builds periodically**: Run `make clean` to avoid stale artifacts
3. **Use make targets**: Prefer `make build` over direct `go build` commands
4. **Verify version info**: Check version information after building
5. **Install for system-wide access**: Use `make install` for frequent use
6. **Keep dependencies updated**: Run `go mod tidy` regularly
7. **Check binary size**: Monitor binary size for bloat
8. **Document custom flags**: If adding flags, document in README
9. **Use health checks**: Always implement and test health endpoints
10. **Profile in production**: Consider enabling pprof in production builds

## Integration Points

### With Nomos Orchestrator

The provider is designed to run as a subprocess of the Nomos orchestrator:

```bash
# Orchestrator starts provider
nomos-provider-terraform-remote-state

# Provider writes port to stdout
# Orchestrator reads and connects
```

### With Docker

Build and run in Docker:

```dockerfile
FROM golang:1.25-alpine AS builder
WORKDIR /app
COPY . .
RUN go build -o provider ./cmd/provider

FROM alpine:latest
COPY --from=builder /app/provider /usr/local/bin/
CMD ["provider"]
```

### With Kubernetes

Deploy as a Kubernetes service:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nomos-provider-tfstate
spec:
  replicas: 1
  template:
    spec:
      containers:
      - name: provider
        image: nomos-provider-terraform-remote-state:latest
        ports:
        - containerPort: 50051
```

## Related Skills

- **run-tests**: Run tests before building and running
- **update-changelog**: Document changes before releases
