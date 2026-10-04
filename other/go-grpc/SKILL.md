---
name: go-grpc
description: "Building microservices with gRPC and Protobuf. Covers service definition, status codes, interceptors, and client/server implementation."
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Wed, 06 May 2026 06:40:00 GMT
---

## Core Concepts

gRPC uses **Protocol Buffers** (Protobuf) for service definition and serialization. It runs over **HTTP/2**, allowing for multiplexing, streaming, and header compression.

### Workflow
1. Define the service and messages in a `.proto` file.
2. Generate Go code using `protoc` or `buf`.
3. Implement the server interface in Go.
4. Use the generated client to make calls.

## Best Practices

1. **Use Wrapper Messages** — Never use bare types (like `string` or `int32`) as RPC inputs or outputs. Always wrap them in a message (e.g., `GetProductRequest`) so you can add fields later without breaking changes.
2. **Standard Status Codes** — Use `google.golang.org/grpc/status` to return specific codes (e.g., `NotFound`, `PermissionDenied`, `Unavailable`). A raw Go error becomes `codes.Unknown`, which is unhelpful for clients.
3. **Reuse Connections** — gRPC clients are safe for concurrent use and multiplex multiple RPCs over a single connection. Create the client once and reuse it.
4. **Always Set Deadlines** — Use `context.WithTimeout` for every client call. Without a deadline, a slow server can hang your goroutines indefinitely.
5. **Implement Health Checks** — Register the standard gRPC health service so orchestrators like Kubernetes can monitor your pod's readiness.
6. **Graceful Shutdown** — Use `srv.GracefulStop()` to allow in-flight RPCs to complete before the server exits.

## Status Code Cheat Sheet

| Code | Usage |
| --- | --- |
| `OK` | Success. |
| `InvalidArgument` | Client sent bad data (400 equivalent). |
| `Unauthenticated` | Missing or invalid auth token (401). |
| `PermissionDenied` | Valid auth, but lacks permission (403). |
| `NotFound` | Resource not found (404). |
| `Unavailable` | Service down or overloaded; client SHOULD retry. |
| `DeadlineExceeded` | The operation took too long. |
| `Internal` | Unexpected server-side bug (500). |

## Code Example: Server

```go
type UserServer struct {
    pb.UnimplementedUserServiceServer
}

func (s *UserServer) GetUser(ctx context.Context, req *pb.GetUserRequest) (*pb.User, error) {
    if req.Id == "" {
        return nil, status.Error(codes.InvalidArgument, "ID is required")
    }
    user, err := s.db.Find(req.Id)
    if err != nil {
        return nil, status.Errorf(codes.NotFound, "user %s not found", req.Id)
    }
    return user, nil
}
```

## Interceptors (Middleware)

Use interceptors for cross-cutting concerns like logging, auth, and metrics.

```go
srv := grpc.NewServer(
    grpc.UnaryInterceptor(myLoggingInterceptor),
)
```

## Anti-patterns

- ❌ **Returning Raw Errors** — Clients receive `Unknown` error codes and can't implement smart retry logic.
- ❌ **New Connection per Request** — Destroys performance due to repeated TCP/TLS handshakes.
- ❌ **Missing Deadlines** — Causes "zombie" goroutines when upstreams are slow.
- ❌ **Bare Proto Types** — Using `rpc Get(string) returns (User)` makes the API impossible to evolve.
- ❌ **Reflection in Production** — Exposes your entire API schema to anyone. Disable it or gate it.
