---
name: grpc-patterns
description: gRPC service implementation patterns. Use when building gRPC services.
---

# gRPC Patterns Skill

gRPC service implementation for Go.

## When to Use

Use when building gRPC services.

## Protocol Buffer Definition

```protobuf
syntax = "proto3";

package user.v1;

option go_package = "github.com/user/project/proto/user/v1;userv1";

service UserService {
  rpc GetUser(GetUserRequest) returns (User);
  rpc ListUsers(ListUsersRequest) returns (stream User);
  rpc CreateUser(CreateUserRequest) returns (User);
}

message GetUserRequest {
  int32 id = 1;
}

message User {
  int32 id = 1;
  string name = 2;
  string email = 3;
}

message ListUsersRequest {
  int32 page_size = 1;
  string page_token = 2;
}

message CreateUserRequest {
  string name = 1;
  string email = 2;
}
```

## Service Implementation

```go
type server struct {
    userv1.UnimplementedUserServiceServer
    service *Service
}

func (s *server) GetUser(ctx context.Context, req *userv1.GetUserRequest) (*userv1.User, error) {
    user, err := s.service.GetUser(ctx, int(req.Id))
    if err != nil {
        return nil, status.Errorf(codes.NotFound, "user not found: %v", err)
    }

    return &userv1.User{
        Id:    int32(user.ID),
        Name:  user.Name,
        Email: user.Email,
    }, nil
}

func (s *server) ListUsers(req *userv1.ListUsersRequest, stream userv1.UserService_ListUsersServer) error {
    users, err := s.service.ListUsers(stream.Context(), int(req.PageSize))
    if err != nil {
        return status.Errorf(codes.Internal, "failed to list users: %v", err)
    }

    for _, user := range users {
        if err := stream.Send(&userv1.User{
            Id:    int32(user.ID),
            Name:  user.Name,
            Email: user.Email,
        }); err != nil {
            return err
        }
    }

    return nil
}
```

## Server Setup

```go
func main() {
    lis, err := net.Listen("tcp", ":50051")
    if err != nil {
        log.Fatalf("failed to listen: %v", err)
    }

    s := grpc.NewServer(
        grpc.UnaryInterceptor(loggingInterceptor),
    )

    userv1.RegisterUserServiceServer(s, &server{
        service: NewService(),
    })

    log.Println("Server listening on :50051")
    if err := s.Serve(lis); err != nil {
        log.Fatalf("failed to serve: %v", err)
    }
}
```

## Interceptors (Middleware)

```go
func loggingInterceptor(ctx context.Context, req interface{}, info *grpc.UnaryServerInfo, handler grpc.UnaryHandler) (interface{}, error) {
    start := time.Now()
    resp, err := handler(ctx, req)
    log.Printf("method=%s duration=%v error=%v", info.FullMethod, time.Since(start), err)
    return resp, err
}
```

## Client Usage

```go
conn, err := grpc.Dial("localhost:50051", grpc.WithInsecure())
if err != nil {
    log.Fatal(err)
}
defer conn.Close()

client := userv1.NewUserServiceClient(conn)

user, err := client.GetUser(context.Background(), &userv1.GetUserRequest{Id: 1})
if err != nil {
    log.Fatal(err)
}
fmt.Println(user)
```

## Best Practices

- Use proper error codes (codes.NotFound, codes.InvalidArgument)
- Implement interceptors for cross-cutting concerns
- Use streaming for large datasets
- Set timeouts on client calls
- Handle metadata for auth
- Implement health checks
