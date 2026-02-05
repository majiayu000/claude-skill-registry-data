---
name: go-grpc
description: Build gRPC services with Go - protobuf, streaming, interceptors
sasmp_version: "1.3.0"
bonded_agent: 07-go-microservices
bond_type: PRIMARY_BOND
---

# Go gRPC Skill

Build high-performance gRPC services with Go.

## Overview

Complete guide for gRPC development including protobuf design, streaming, interceptors, and error handling.

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| streaming | string | no | "unary" | Type: "unary", "server", "client", "bidi" |
| auth | string | no | "none" | Auth: "none", "jwt", "mtls" |

## Core Topics

### Protobuf Definition
```protobuf
syntax = "proto3";
package api.v1;
option go_package = "github.com/example/api/v1;apiv1";

service UserService {
    rpc GetUser(GetUserRequest) returns (GetUserResponse);
    rpc ListUsers(ListUsersRequest) returns (stream User);
    rpc CreateUser(CreateUserRequest) returns (CreateUserResponse);
}

message User {
    int64 id = 1;
    string name = 2;
    string email = 3;
    google.protobuf.Timestamp created_at = 4;
}
```

### Server Implementation
```go
type userServer struct {
    apiv1.UnimplementedUserServiceServer
    store UserStore
}

func (s *userServer) GetUser(ctx context.Context, req *apiv1.GetUserRequest) (*apiv1.GetUserResponse, error) {
    user, err := s.store.FindByID(ctx, req.Id)
    if err != nil {
        if errors.Is(err, ErrNotFound) {
            return nil, status.Error(codes.NotFound, "user not found")
        }
        return nil, status.Error(codes.Internal, "internal error")
    }

    return &apiv1.GetUserResponse{
        User: toProtoUser(user),
    }, nil
}

func (s *userServer) ListUsers(req *apiv1.ListUsersRequest, stream apiv1.UserService_ListUsersServer) error {
    users, err := s.store.List(stream.Context(), req.PageSize)
    if err != nil {
        return status.Error(codes.Internal, "failed to list users")
    }

    for _, user := range users {
        if err := stream.Send(toProtoUser(user)); err != nil {
            return err
        }
    }
    return nil
}
```

### Interceptors
```go
func LoggingInterceptor(logger *slog.Logger) grpc.UnaryServerInterceptor {
    return func(ctx context.Context, req interface{}, info *grpc.UnaryServerInfo, handler grpc.UnaryHandler) (interface{}, error) {
        start := time.Now()

        resp, err := handler(ctx, req)

        logger.Info("grpc call",
            "method", info.FullMethod,
            "duration", time.Since(start),
            "error", err,
        )

        return resp, err
    }
}

func RecoveryInterceptor() grpc.UnaryServerInterceptor {
    return func(ctx context.Context, req interface{}, info *grpc.UnaryServerInfo, handler grpc.UnaryHandler) (resp interface{}, err error) {
        defer func() {
            if r := recover(); r != nil {
                err = status.Errorf(codes.Internal, "panic: %v", r)
            }
        }()
        return handler(ctx, req)
    }
}
```

### Client with Retry
```go
func NewClient(addr string) (apiv1.UserServiceClient, error) {
    conn, err := grpc.Dial(addr,
        grpc.WithTransportCredentials(insecure.NewCredentials()),
        grpc.WithUnaryInterceptor(
            grpc_retry.UnaryClientInterceptor(
                grpc_retry.WithMax(3),
                grpc_retry.WithBackoff(grpc_retry.BackoffExponential(100*time.Millisecond)),
                grpc_retry.WithCodes(codes.Unavailable, codes.ResourceExhausted),
            ),
        ),
    )
    if err != nil {
        return nil, err
    }

    return apiv1.NewUserServiceClient(conn), nil
}
```

## gRPC Status Codes

| Code | Use Case |
|------|----------|
| OK | Success |
| INVALID_ARGUMENT | Bad input |
| NOT_FOUND | Resource missing |
| ALREADY_EXISTS | Duplicate |
| DEADLINE_EXCEEDED | Timeout |
| UNAVAILABLE | Service down |
| INTERNAL | Server bug |

## Troubleshooting

### Debug Commands
```bash
grpcurl -plaintext localhost:50051 list
grpcurl -plaintext -d '{"id": 1}' localhost:50051 api.v1.UserService/GetUser
```

## Usage

```
Skill("go-grpc")
```
