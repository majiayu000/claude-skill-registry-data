---
name: nomos-provider-protocol
description: Guide for working with Nomos provider protocol buffers including modifying .proto files, buf workflow, code generation, versioning, and protocol evolution. Use this when modifying the gRPC contract, adding RPC methods, regenerating code, or managing protocol compatibility.
---

# Nomos Provider Protocol Development

This skill guides you through working with the Nomos provider gRPC protocol, from modifying .proto files to managing protocol versioning and compatibility.

## When to Use This Skill

- Modifying the provider gRPC contract (.proto files)
- Adding new RPC methods or message fields
- Regenerating Go code from proto definitions
- Checking protocol compatibility (breaking changes)
- Versioning the protocol (v1 → v2)
- Debugging protobuf compilation issues
- Understanding provider lifecycle and error codes

## Protocol Overview

**Location:** `libs/provider-proto/proto/nomos/provider/v1/provider.proto`

**Architecture:** Subprocess + gRPC communication
1. Compiler spawns provider executable
2. Provider starts gRPC server on random port
3. Provider prints `PORT=<number>` to stdout
4. Compiler connects as gRPC client
5. Lifecycle: Init → Fetch (multiple) → Shutdown

**Service Contract - Five RPC Methods:**
- `Init` - Initialize provider with config (called once)
- `Fetch` - Retrieve data at path (primary method, called multiple times)
- `Info` - Return provider metadata (can be called anytime)
- `Health` - Check operational status (for monitoring)
- `Shutdown` - Graceful cleanup (best-effort)

## Buf Workflow

Nomos uses [Buf](https://buf.build/) for protocol buffer management.

### Standard Workflow

```bash
cd libs/provider-proto

# 1. Lint proto files
buf lint

# 2. Check for breaking changes
buf breaking --against .git#branch=main

# 3. Generate Go code
buf generate
# Or use Makefile:
make generate

# 4. Test generated code
go test ./...
```

### Configuration Files

**buf.yaml** - Module configuration:
```yaml
version: v2
modules:
  - path: proto
lint:
  use:
    - STANDARD
breaking:
  use:
    - FILE
```

**buf.gen.yaml** - Code generation:
```yaml
version: v2
managed:
  enabled: true
plugins:
  - plugin: buf.build/protocolbuffers/go
    out: gen/go
    opt: paths=source_relative
  - plugin: buf.build/grpc/go
    out: gen/go
    opt: paths=source_relative
```

## Modifying Proto Files

### Adding Optional Fields

**Safe (non-breaking):**

```protobuf
message InitRequest {
  string alias = 1;
  google.protobuf.Struct config = 2;
  string source_file_path = 3;
  
  // ✅ Add new optional field at next available number
  string workspace_root = 4;  // NEW: Optional workspace root path
  
  reserved 5 to 10;  // Update reservation
}
```

**Rules:**
- Use next available field number
- Optional by default in proto3
- Update reserved range if needed
- Add comment explaining purpose

### Adding Required Fields

**Breaking change (avoid if possible):**

```protobuf
message FetchRequest {
  repeated string path = 1;
  
  // ⚠️ BREAKING: This becomes required for all providers
  string context_id = 2;  // Required context identifier
}
```

**If you must:**
1. Create new message version (e.g., `FetchRequestV2`)
2. Deprecate old message
3. Support both during transition
4. Document migration path

### Adding New RPC Method

**Safe (non-breaking):**

```protobuf
service ProviderService {
  rpc Init(InitRequest) returns (InitResponse);
  rpc Fetch(FetchRequest) returns (FetchResponse);
  rpc Info(InfoRequest) returns (InfoResponse);
  rpc Health(HealthRequest) returns (HealthResponse);
  rpc Shutdown(ShutdownRequest) returns (ShutdownResponse);
  
  // ✅ Add new optional RPC method
  // Validate checks provider configuration without executing.
  // Returns validation errors if configuration is invalid.
  //
  // Error codes:
  //   - InvalidArgument: Configuration is invalid
  //   - FailedPrecondition: Provider not initialized
  rpc Validate(ValidateRequest) returns (ValidateResponse);
}

message ValidateRequest {
  // config to validate (same structure as Init.config)
  google.protobuf.Struct config = 1;
}

message ValidateResponse {
  // is_valid indicates if configuration is valid
  bool is_valid = 1;
  
  // errors contains validation error messages if not valid
  repeated string errors = 2;
}
```

**Considerations:**
- Document when method should be called in lifecycle
- Specify which error codes to use
- Old providers won't implement new method (OK for optional features)
- Compiler must handle `Unimplemented` status gracefully

### Deprecating Fields

**Gradual deprecation:**

```protobuf
message InitRequest {
  string alias = 1;
  google.protobuf.Struct config = 2;
  
  // DEPRECATED: Use source_file_path instead
  // Will be removed in v2
  string legacy_path = 3 [deprecated = true];
  
  string source_file_path = 4;
}
```

**Process:**
1. Mark field as `deprecated = true`
2. Add deprecation comment with timeline
3. Update documentation
4. Remove in next major version

### Field Number Reservation

**Always reserve deleted field numbers:**

```protobuf
message FetchRequest {
  repeated string path = 1;
  
  // Field 2 removed: was timeout_seconds (removed in v1.2.0)
  reserved 2;
  
  // Ranges reserved for future use
  reserved 3 to 10;
}
```

**Why:** Prevents field number reuse which breaks binary compatibility.

## Protocol Versioning

### When to Create v2

Create new version when:
- Multiple breaking changes accumulated
- Major architectural shift
- Field removals needed
- Message restructuring required

**Current:** `nomos.provider.v1`  
**Future:** `nomos.provider.v2`

### Version Migration Strategy

1. **Create v2 directory:**
   ```
   proto/nomos/provider/
   ├── v1/
   │   └── provider.proto
   └── v2/
       └── provider.proto
   ```

2. **Update package declaration:**
   ```protobuf
   package nomos.provider.v2;
   option go_package = "...gen/go/nomos/provider/v2;providerv2";
   ```

3. **Maintain v1 compatibility:**
   - Keep v1 generated code
   - Compiler supports both v1 and v2 providers
   - Gradually migrate providers

4. **Deprecate v1:**
   - Document migration guide
   - Set sunset timeline
   - Eventually remove v1 support

## Code Generation

### Generate Go Code

```bash
cd libs/provider-proto

# Using buf
buf generate

# Or using Makefile
make generate

# Verify generation
ls -la gen/go/nomos/provider/v1/
# Should see:
# - provider.pb.go        (protobuf messages)
# - provider_grpc.pb.go   (gRPC service stubs)
```

### Generated Files

**DO commit:**
- `gen/go/nomos/provider/v1/*.pb.go` - Generated Go code

**DO NOT commit:**
- `bin/` - Compiled binaries

**After generation:**
```bash
go mod tidy
go test ./...
```

### Regeneration Triggers

Regenerate when:
- .proto file modified
- buf.gen.yaml changed
- After Git merge (if proto files changed)
- Buf version upgraded

## Error Code Conventions

Use standard gRPC status codes consistently:

### Init Method

```go
// ✅ Correct error code usage
func (p *myProvider) Init(ctx context.Context, req *providerv1.InitRequest) (*providerv1.InitResponse, error) {
    // Missing required config field
    if req.Config == nil {
        return nil, status.Error(codes.InvalidArgument, "config is required")
    }
    
    // External dependency unavailable
    if !p.canConnectToBackend() {
        return nil, status.Error(codes.Unavailable, "backend service unreachable")
    }
    
    // Permission denied
    if !p.hasPermission() {
        return nil, status.Error(codes.PermissionDenied, "insufficient permissions")
    }
    
    // Provider cannot function
    if p.isBroken() {
        return nil, status.Error(codes.FailedPrecondition, "provider cannot initialize")
    }
    
    return &providerv1.InitResponse{}, nil
}
```

### Fetch Method

```go
func (p *myProvider) Fetch(ctx context.Context, req *providerv1.FetchRequest) (*providerv1.FetchResponse, error) {
    // Init not called yet
    if !p.initialized {
        return nil, status.Error(codes.FailedPrecondition, "Init must be called before Fetch")
    }
    
    // Path doesn't exist
    if !p.pathExists(req.Path) {
        return nil, status.Error(codes.NotFound, fmt.Sprintf("path not found: %v", req.Path))
    }
    
    // Invalid path format
    if !p.isValidPath(req.Path) {
        return nil, status.Error(codes.InvalidArgument, "path contains invalid characters")
    }
    
    // Operation timed out
    if ctx.Err() == context.DeadlineExceeded {
        return nil, status.Error(codes.DeadlineExceeded, "fetch operation timed out")
    }
    
    // Temporary failure
    if p.isTemporarilyUnavailable() {
        return nil, status.Error(codes.Unavailable, "data source temporarily unavailable")
    }
    
    // Success
    value, _ := structpb.NewStruct(data)
    return &providerv1.FetchResponse{Value: value}, nil
}
```

### Complete Error Code Reference

- `InvalidArgument` - Bad input (config, path format)
- `NotFound` - Resource doesn't exist (path not found)
- `FailedPrecondition` - Cannot proceed (Init not called, broken state)
- `Unavailable` - Temporary failure (network down, service restarting)
- `PermissionDenied` - Access denied (auth failure, insufficient permissions)
- `DeadlineExceeded` - Timeout (slow operation, large data)
- `Internal` - Provider bug (unexpected error, panic recovery)
- `Unimplemented` - Method not supported (old provider, optional RPC)

## Data Structure Compatibility

### Using google.protobuf.Struct

Fetch responses use `google.protobuf.Struct` for flexibility:

```go
import "google.golang.org/protobuf/types/known/structpb"

// Map to Nomos value types
data := map[string]interface{}{
    // Scalars
    "name":    "example",          // string
    "port":    float64(8080),      // number (always float64)
    "enabled": true,               // boolean
    "timeout": nil,                // null
    
    // Collections
    "tags": []interface{}{         // array
        "prod", "web",
    },
    "config": map[string]interface{}{  // nested map
        "host": "localhost",
        "port": float64(5432),
    },
}

value, err := structpb.NewStruct(data)
if err != nil {
    return nil, status.Error(codes.Internal, err.Error())
}

return &providerv1.FetchResponse{Value: value}, nil
```

**Important:** Numbers must be `float64` for structpb compatibility.

## Testing Protocol Changes

### Contract Tests

```go
// contract_test.go
func TestProviderContract(t *testing.T) {
    tests := []struct {
        name string
        test func(t *testing.T, client providerv1.ProviderServiceClient)
    }{
        {
            name: "Init with valid config",
            test: func(t *testing.T, client providerv1.ProviderServiceClient) {
                config, _ := structpb.NewStruct(map[string]interface{}{
                    "key": "value",
                })
                
                resp, err := client.Init(ctx, &providerv1.InitRequest{
                    Alias:  "test",
                    Config: config,
                })
                
                if err != nil {
                    t.Fatalf("Init failed: %v", err)
                }
                if resp == nil {
                    t.Fatal("Init returned nil response")
                }
            },
        },
        {
            name: "Fetch before Init fails",
            test: func(t *testing.T, client providerv1.ProviderServiceClient) {
                _, err := client.Fetch(ctx, &providerv1.FetchRequest{
                    Path: []string{"test"},
                })
                
                if status.Code(err) != codes.FailedPrecondition {
                    t.Errorf("expected FailedPrecondition, got %v", status.Code(err))
                }
            },
        },
    }
    
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            server := newTestServer(t)
            client := newTestClient(t, server)
            tt.test(t, client)
        })
    }
}
```

### Integration Tests

```go
// grpc_integration_test.go
func TestGRPCIntegration_FullLifecycle(t *testing.T) {
    // Start provider server
    server, addr := startTestServer(t)
    defer server.Stop()
    
    // Create client
    conn, err := grpc.Dial(addr, grpc.WithInsecure())
    require.NoError(t, err)
    defer conn.Close()
    
    client := providerv1.NewProviderServiceClient(conn)
    
    // Test full lifecycle
    t.Run("Init", func(t *testing.T) {
        config, _ := structpb.NewStruct(map[string]interface{}{
            "directory": "./testdata",
        })
        
        _, err := client.Init(ctx, &providerv1.InitRequest{
            Alias:  "test",
            Config: config,
        })
        require.NoError(t, err)
    })
    
    t.Run("Fetch", func(t *testing.T) {
        resp, err := client.Fetch(ctx, &providerv1.FetchRequest{
            Path: []string{"config", "database"},
        })
        require.NoError(t, err)
        require.NotNil(t, resp.Value)
    })
    
    t.Run("Shutdown", func(t *testing.T) {
        _, err := client.Shutdown(ctx, &providerv1.ShutdownRequest{})
        require.NoError(t, err)
    })
}
```

## Common Tasks

### Task 1: Add Optional Field to InitRequest

```protobuf
message InitRequest {
  string alias = 1;
  google.protobuf.Struct config = 2;
  string source_file_path = 3;
  
  // NEW: Workspace root for resolving paths
  string workspace_root = 4;
  
  reserved 5 to 10;  // Updated
}
```

```bash
buf lint
buf breaking --against .git#branch=main  # Should pass (non-breaking)
buf generate
go test ./...
```

### Task 2: Add New RPC Method

See "Adding New RPC Method" section above for complete example.

```bash
buf lint
buf breaking --against .git#branch=main  # Should pass (non-breaking)
buf generate
go test ./...
# Add contract tests for new method
```

### Task 3: Create Protocol v2

```bash
# 1. Create v2 directory
mkdir -p proto/nomos/provider/v2

# 2. Copy and modify v1 proto
cp proto/nomos/provider/v1/provider.proto proto/nomos/provider/v2/

# 3. Update package declaration in v2/provider.proto
# package nomos.provider.v2;
# option go_package = ".../v2;providerv2";

# 4. Make breaking changes in v2

# 5. Generate both versions
buf generate

# 6. Test both versions
go test ./...
```

## Troubleshooting

### Error: "buf: command not found"

**Install buf:**
```bash
# macOS
brew install bufbuild/buf/buf

# Linux
curl -sSL https://github.com/bufbuild/buf/releases/download/v1.28.0/buf-$(uname -s)-$(uname -m) \
  -o /usr/local/bin/buf
chmod +x /usr/local/bin/buf
```

### Error: Breaking change detected

**Example:**
```
Field "3" on message "InitRequest" changed type from "string" to "int32"
```

**Solutions:**

1. **If intentional breaking change:**
   ```bash
   # Skip breaking check (document why)
   buf generate  # Generate without breaking check
   
   # Update CHANGELOG with BREAKING: prefix
   # Plan protocol v2 migration
   ```

2. **If unintentional:**
   ```bash
   # Revert the change
   git diff proto/
   # Fix the type back to original
   ```

### Error: Generated code out of sync

**Symptom:** Compilation errors after pulling changes

**Solution:**
```bash
cd libs/provider-proto
buf generate
go mod tidy
go test ./...
```

### Error: Invalid field number

**Symptom:** `buf lint` fails with field number error

**Causes:**
- Field number < 1 or > 536,870,911
- Using reserved field number
- Duplicate field numbers

**Solution:**
```protobuf
message Example {
  // ❌ Wrong
  string field = 0;  // Must be >= 1
  
  // ✅ Correct
  string field = 1;
  
  reserved 2;  // Don't reuse
  string other = 3;
}
```

## Best Practices

1. **Always run buf breaking check** before committing proto changes
2. **Add comments** documenting field purpose and RPC usage
3. **Reserve deleted field numbers** to prevent reuse
4. **Use semantic versioning** - breaking changes require new major version
5. **Document error codes** in RPC method comments
6. **Test generated code** after every regeneration
7. **Add contract tests** for new RPC methods
8. **Keep v1 working** during v2 development
9. **Update CHANGELOG** with protocol changes
10. **Commit generated code** for reproducibility

## Reference Documentation

For more details, see:
- [Provider Proto README](../../libs/provider-proto/README.md)
- [Provider Proto AGENTS.md](../../libs/provider-proto/AGENTS.md)
- [Provider Authoring Guide](../../docs/guides/provider-authoring-guide.md)
- [Buf Documentation](https://buf.build/docs)
- [gRPC Status Codes](https://grpc.io/docs/guides/status-codes/)
