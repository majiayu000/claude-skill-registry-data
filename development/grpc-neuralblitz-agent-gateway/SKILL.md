---
name: grpc
description: gRPC framework best practices and implementation
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: api-design
---
## What I do
- Define Protocol Buffer schemas
- Implement gRPC services
- Handle streaming
- Implement authentication
- Handle errors properly
- Manage versioning
- Test gRPC services
- Scale gRPC deployments

## When to use me
When implementing gRPC services or working with Protocol Buffers.

## Protocol Buffer Definition
```protobuf
syntax = "proto3";

package user.v1;

option go_package = "github.com/company/api/user/v1";

import "google/protobuf/timestamp.proto";
import "google/protobuf/empty.proto";


// Service definition
service UserService {
  // Unary RPC
  rpc GetUser(GetUserRequest) returns (User);
  
  // Server streaming
  rpc ListUsers(ListUsersRequest) returns (stream User);
  
  // Client streaming
  rpc CreateUsers(stream CreateUserRequest) returns (CreateUsersResponse);
  
  // Bidirectional streaming
  rpc StreamUserUpdates(stream UserUpdateRequest) returns (stream User);
  
  // Health check
  rpc HealthCheck(google.protobuf.Empty) returns (HealthCheckResponse);
}


// Message types
message GetUserRequest {
  string user_id = 1;
}

message User {
  string id = 1;
  string email = 2;
  string name = 3;
  UserStatus status = 4;
  google.protobuf.Timestamp created_at = 5;
  google.protobuf.Timestamp updated_at = 6;
}

enum UserStatus {
  USER_STATUS_UNSPECIFIED = 0;
  USER_STATUS_ACTIVE = 1;
  USER_STATUS_INACTIVE = 2;
  USER_STATUS_SUSPENDED = 3;
}

message ListUsersRequest {
  int32 page_size = 1;
  string page_token = 2;
  UserStatus status_filter = 3;
}

message CreateUserRequest {
  string email = 1;
  string name = 2;
  string password = 3;
}

message CreateUsersResponse {
  repeated User users = 1;
  int32 failed_count = 2;
}

message UserUpdateRequest {
  string user_id = 1;
  string name = 2;
}

message HealthCheckResponse {
  bool healthy = 1;
  string version = 2;
}
```

## Go gRPC Server
```go
package main

import (
	"context"
	"log"
	"net"

	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/credentials"
	"google.golang.org/grpc/metadata"
	"google.golang.org/grpc/status"
	"google.golang.org/protobuf/types/known/timestamppb"

	pb "github.com/company/api/user/v1"
)

type UserServer struct {
	pb.UnimplementedUserServiceServer
	userStore UserStore
}

type UserStore interface {
	GetUser(ctx context.Context, id string) (*pb.User, error)
	ListUsers(ctx context.Context, filter *pb.UserStatus, limit int) ([]*pb.User, error)
	CreateUser(ctx context.Context, user *pb.User) error
}

func NewUserServer(store UserStore) *UserServer {
	return &UserServer{userStore: store}
}

func (s *UserServer) GetUser(
	ctx context.Context,
	req *pb.GetUserRequest,
) (*pb.User, error) {
	// Extract metadata for logging
	md, ok := metadata.FromIncomingContext(ctx)
	if ok {
		log.Printf("GetUser request: user_id=%s, from=%v", req.UserId, md.Get("x-forwarded-for"))
	}

	// Validate request
	if req.UserId == "" {
		return nil, status.Error(codes.InvalidArgument, "user_id is required")
	}

	// Fetch user
	user, err := s.userStore.GetUser(ctx, req.UserId)
	if err != nil {
		return nil, status.Errorf(codes.NotFound, "user not found: %s", err)
	}

	return user, nil
}

func (s *UserServer) ListUsers(
	req *pb.ListUsersRequest,
	stream pb.UserService_ListUsersServer,
) error {
	ctx := stream.Context()

	// Parse pagination
	pageSize := int(req.PageSize)
	if pageSize <= 0 {
		pageSize = 10
	}
	if pageSize > 100 {
		pageSize = 100
	}

	users, err := s.userStore.ListUsers(ctx, req.StatusFilter, pageSize)
	if err != nil {
		return status.Errorf(codes.Internal, "failed to list users: %v", err)
	}

	// Stream users to client
	for _, user := range users {
		if err := stream.Send(user); err != nil {
			return status.Errorf(codes.Internal, "failed to send user: %v", err)
		}
	}

	return nil
}

func (s *UserService) CreateUsers(
	stream pb.UserService_CreateUsersServer,
) error {
	ctx := stream.Context()
	var users []*pb.User
	var failedCount int32

	for {
		req, err := stream.Recv()
		if err != nil {
			if err.Error() == "EOF" {
				break
			}
			return status.Errorf(codes.Internal, "failed to receive request: %v", err)
		}

		user := &pb.User{
			Email:     req.Email,
			Name:      req.Name,
			Status:    pb.UserStatus_USER_STATUS_ACTIVE,
			CreatedAt: timestamppb.Now(),
		}

		if err := s.userStore.CreateUser(ctx, user); err != nil {
			failedCount++
			log.Printf("Failed to create user: %v", err)
			continue
		}

		users = append(users, user)
	}

	return stream.SendAndClose(&pb.CreateUsersResponse{
		Users:       users,
		FailedCount: failedCount,
	})
}

func (s *UserServer) StreamUserUpdates(
	stream pb.UserService_StreamUserUpdatesServer,
) error {
	ctx := stream.Context()

	for {
		select {
		case <-ctx.Done():
			return ctx.Err()
		default:
			req, err := stream.Recv()
			if err != nil {
				return err
			}

			user, err := s.userStore.GetUser(ctx, req.UserId)
			if err != nil {
				continue
			}

			if err := stream.Send(user); err != nil {
				return err
			}
		}
	}
}

// Server reflection for debugging
func init() {
	// Enable reflection
	// reflection.Register(grpcServer)
}
```

## gRPC Client
```go
package main

import (
	"context"
	"log"
	"time"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
	"google.golang.org/grpc/metadata"

	pb "github.com/company/api/user/v1"
)

type UserClient struct {
	conn   *grpc.ClientConn
	client pb.UserServiceClient
}

func NewUserClient(addr string) (*UserClient, error) {
	conn, err := grpc.Dial(
		addr,
		grpc.WithTransportCredentials(insecure.NewCredentials()),
		grpc.WithUnaryInterceptor(loggingInterceptor),
		grpc.WithStreamInterceptor(streamLoggingInterceptor),
	)
	if err != nil {
		return nil, err
	}

	return &UserClient{
		conn:   conn,
		client: pb.NewUserServiceClient(conn),
	}, nil
}

func (c *UserClient) GetUser(ctx context.Context, userId string) (*pb.User, error) {
	// Add metadata for tracing
	ctx = metadata.AppendToOutgoingContext(ctx, "x-request-id", "req-123")

	ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
	defer cancel()

	return c.client.GetUser(ctx, &pb.GetUserRequest{
		UserId: userId,
	})
}

func (c *UserClient) ListActiveUsers(ctx context.Context) ([]*pb.User, error) {
	ctx, cancel := context.WithTimeout(ctx, 30*time.Second)
	defer cancel()

	stream, err := c.client.ListUsers(ctx, &pb.ListUsersRequest{
		PageSize:  100,
		StatusFilter: pb.UserStatus_USER_STATUS_ACTIVE,
	})
	if err != nil {
		return nil, err
	}

	var users []*pb.User
	for {
		user, err := stream.Recv()
		if err != nil {
			if err.Error() == "EOF" {
				break
			}
			return nil, err
		}
		users = append(users, user)
	}

	return users, nil
}

func (c *UserClient) Close() error {
	return c.conn.Close()
}

// Interceptors
func loggingInterceptor(
	ctx context.Context,
	method string,
	req, reply interface{},
	cc *grpc.ClientConn,
	invoker grpc.UnaryInvoker,
	opts ...grpc.CallOption,
) error {
	start := time.Now()
	
	err := invoker(ctx, method, req, reply, cc, opts...)
	
	log.Printf("gRPC call: %s, duration: %v, error: %v",
		method, time.Since(start), err)
	
	return err
}

func streamLoggingInterceptor(
	ctx context.Context,
	desc *grpc.StreamDesc,
	cc *grpc.ClientConn,
	method string,
	stream grpc.ClientStream,
	opts ...grpc.CallOption,
) error {
	start := time.Now()
	
	err := stream.RecvMsg(nil)
	
	log.Printf("gRPC stream: %s, duration: %v, error: %v",
		method, time.Since(start), err)
	
	return err
}
```

## Error Handling
```go
package status

import (
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
)

// Custom error codes
const (
	ErrCodeUserNotFound = "USER_NOT_FOUND"
	ErrCodeInvalidInput = "INVALID_INPUT"
	ErrCodeUnauthorized = "UNAUTHORIZED"
)

func UserNotFound(id string) error {
	return status.Errorf(codes.NotFound, "user not found: %s", id)
}

func InvalidInput(field, reason string) error {
	return status.Errorf(codes.InvalidArgument, "invalid %s: %s", field, reason)
}

func Unauthorized(reason string) error {
	return status.Errorf(codes.Unauthenticated, "unauthorized: %s", reason)
}
```

## gRPC Best Practices
```
1. Use Protocol Buffers for schema
   - Define contracts explicitly
   - Enable backwards compatibility

2. Handle errors properly
   - Use gRPC status codes
   - Include error details

3. Implement interceptors
   - Logging, auth, metrics

4. Use streaming appropriately
   - Server streaming for lists
   - Bidirectional for real-time

5. Set timeouts
   - Always use context with timeout

6. Enable reflection
   - For debugging and tools

7. Version your APIs
   - Include version in package name
   - Support multiple versions

8. Use proper authentication
   - Token-based or mTLS

9. Monitor and trace
   - Add interceptors for metrics
   - Use OpenTelemetry

10. Test thoroughly
    - Unit tests with mock stores
    - Integration tests
```
