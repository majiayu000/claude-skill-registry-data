---
name: grpc
description: Build high-performance gRPC services with Protocol Buffers — service definitions, unary and streaming RPCs, interceptors, error handling, and Node.js/Go implementations
layer: domain
category: backend
triggers:
  - "grpc"
  - "protobuf"
  - "protocol buffers"
  - "proto file"
  - "gRPC streaming"
  - "gRPC service"
  - "rpc call"
  - "grpc-web"
  - "tonic grpc"
  - "connect-rpc"
inputs:
  - Service interface and method definitions
  - Language/runtime (Node.js, Go, Rust, Python)
  - Communication pattern (unary, server-streaming, client-streaming, bidirectional)
  - Authentication and authorization requirements
  - Deployment target (Kubernetes, Cloud Run, bare metal)
outputs:
  - Proto file definitions with message and service schemas
  - Server implementation with interceptors
  - Client stubs with retry and deadline configuration
  - Streaming handler implementations
  - Error handling with gRPC status codes
  - Build configuration for proto compilation
linksTo:
  - api-designer
  - microservices
  - authentication
  - monitoring
linkedFrom:
  - microservices
  - api-designer
preferredNextSkills:
  - monitoring
  - testing-patterns
fallbackSkills:
  - api-designer
riskLevel: low
memoryReadPolicy: selective
memoryWritePolicy: none
sideEffects: []
---

# gRPC Skill

## Purpose

gRPC is a high-performance RPC framework using Protocol Buffers for serialization and HTTP/2 for transport. It provides strongly-typed service contracts, automatic code generation, bidirectional streaming, and efficient binary serialization — making it the standard for service-to-service communication in microservice architectures. This skill covers proto file design, server/client implementation in Node.js and Go, streaming patterns, and production hardening.

## Key Concepts

### gRPC vs. REST

| Aspect | gRPC | REST (JSON) |
|--------|------|-------------|
| Serialization | Protobuf (binary, ~10x smaller) | JSON (text) |
| Transport | HTTP/2 (multiplexed) | HTTP/1.1 or HTTP/2 |
| Contract | `.proto` file (strict) | OpenAPI/informal |
| Streaming | Native (4 patterns) | Workarounds (SSE, WebSocket) |
| Code generation | Built-in for 11+ languages | Optional (openapi-generator) |
| Browser support | Via grpc-web or Connect | Native |
| Debugging | Needs tooling (grpcurl, Evans) | curl, browser |

### Four Communication Patterns

```
1. UNARY (request-response):
   Client ──request──→ Server
   Client ←──response── Server

2. SERVER STREAMING:
   Client ──request──→ Server
   Client ←──stream──── Server (multiple responses)

3. CLIENT STREAMING:
   Client ──stream──→ Server (multiple requests)
   Client ←──response── Server

4. BIDIRECTIONAL STREAMING:
   Client ←──stream──→ Server (both directions)
```

### gRPC Status Codes

| Code | Name | When to Use |
|------|------|-------------|
| 0 | OK | Success |
| 1 | CANCELLED | Client cancelled the request |
| 2 | UNKNOWN | Server threw an unexpected exception |
| 3 | INVALID_ARGUMENT | Client sent bad input (400 equivalent) |
| 5 | NOT_FOUND | Resource does not exist (404 equivalent) |
| 6 | ALREADY_EXISTS | Conflict on create (409 equivalent) |
| 7 | PERMISSION_DENIED | Authenticated but not authorized (403) |
| 13 | INTERNAL | Server bug (500 equivalent) |
| 14 | UNAVAILABLE | Transient failure, retry safe (503) |
| 16 | UNAUTHENTICATED | No valid credentials (401 equivalent) |

## Implementation

### Proto File Definition

```protobuf
// proto/order_service.proto
syntax = "proto3";

package orderservice.v1;

option go_package = "github.com/example/orderservice/v1;orderservicev1";

import "google/protobuf/timestamp.proto";
import "google/protobuf/empty.proto";

// Service definition
service OrderService {
  // Unary: create a new order
  rpc CreateOrder(CreateOrderRequest) returns (CreateOrderResponse);

  // Unary: get order by ID
  rpc GetOrder(GetOrderRequest) returns (Order);

  // Server streaming: watch order status changes in real-time
  rpc WatchOrder(WatchOrderRequest) returns (stream OrderStatusUpdate);

  // Client streaming: bulk import orders
  rpc BulkCreateOrders(stream CreateOrderRequest) returns (BulkCreateOrdersResponse);

  // Bidirectional streaming: real-time order processing pipeline
  rpc ProcessOrders(stream ProcessOrderCommand) returns (stream ProcessOrderResult);
}

// Messages
message CreateOrderRequest {
  string customer_id = 1;
  repeated OrderItem items = 2;
  Address shipping_address = 3;
  string idempotency_key = 4; // Prevent duplicate orders
}

message CreateOrderResponse {
  string order_id = 1;
  OrderStatus status = 2;
  google.protobuf.Timestamp created_at = 3;
}

message GetOrderRequest {
  string order_id = 1;
}

message Order {
  string order_id = 1;
  string customer_id = 2;
  repeated OrderItem items = 3;
  OrderStatus status = 4;
  int64 total_cents = 5;
  Address shipping_address = 6;
  google.protobuf.Timestamp created_at = 7;
  google.protobuf.Timestamp updated_at = 8;
}

message OrderItem {
  string product_id = 1;
  string name = 2;
  int32 quantity = 3;
  int64 price_cents = 4;
}

message Address {
  string line1 = 1;
  string line2 = 2;
  string city = 3;
  string state = 4;
  string postal_code = 5;
  string country = 6;
}

enum OrderStatus {
  ORDER_STATUS_UNSPECIFIED = 0;
  ORDER_STATUS_CREATED = 1;
  ORDER_STATUS_PAID = 2;
  ORDER_STATUS_SHIPPED = 3;
  ORDER_STATUS_DELIVERED = 4;
  ORDER_STATUS_CANCELLED = 5;
}

message WatchOrderRequest {
  string order_id = 1;
}

message OrderStatusUpdate {
  string order_id = 1;
  OrderStatus previous_status = 2;
  OrderStatus new_status = 3;
  google.protobuf.Timestamp timestamp = 4;
}

message BulkCreateOrdersResponse {
  int32 created_count = 1;
  int32 failed_count = 2;
  repeated string failed_ids = 3;
}

message ProcessOrderCommand {
  string order_id = 1;
  string action = 2;
}

message ProcessOrderResult {
  string order_id = 1;
  bool success = 2;
  string message = 3;
}
```

### Go Server Implementation

```go
// server/main.go
package main

import (
	"context"
	"fmt"
	"log"
	"net"
	"time"

	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
	"google.golang.org/protobuf/types/known/timestamppb"

	pb "github.com/example/orderservice/v1"
)

type orderServer struct {
	pb.UnimplementedOrderServiceServer
	orders map[string]*pb.Order
}

func (s *orderServer) CreateOrder(
	ctx context.Context,
	req *pb.CreateOrderRequest,
) (*pb.CreateOrderResponse, error) {
	// Validate input
	if req.CustomerId == "" {
		return nil, status.Error(codes.InvalidArgument, "customer_id is required")
	}
	if len(req.Items) == 0 {
		return nil, status.Error(codes.InvalidArgument, "at least one item is required")
	}

	// Check deadline/timeout
	if deadline, ok := ctx.Deadline(); ok {
		if time.Until(deadline) < 100*time.Millisecond {
			return nil, status.Error(codes.DeadlineExceeded, "insufficient time remaining")
		}
	}

	orderID := generateID()
	var totalCents int64
	for _, item := range req.Items {
		totalCents += item.PriceCents * int64(item.Quantity)
	}

	order := &pb.Order{
		OrderId:         orderID,
		CustomerId:      req.CustomerId,
		Items:           req.Items,
		Status:          pb.OrderStatus_ORDER_STATUS_CREATED,
		TotalCents:      totalCents,
		ShippingAddress: req.ShippingAddress,
		CreatedAt:       timestamppb.Now(),
		UpdatedAt:       timestamppb.Now(),
	}

	s.orders[orderID] = order

	return &pb.CreateOrderResponse{
		OrderId:   orderID,
		Status:    pb.OrderStatus_ORDER_STATUS_CREATED,
		CreatedAt: order.CreatedAt,
	}, nil
}

func (s *orderServer) GetOrder(
	ctx context.Context,
	req *pb.GetOrderRequest,
) (*pb.Order, error) {
	order, ok := s.orders[req.OrderId]
	if !ok {
		return nil, status.Errorf(codes.NotFound, "order %s not found", req.OrderId)
	}
	return order, nil
}

// Server streaming: push status updates
func (s *orderServer) WatchOrder(
	req *pb.WatchOrderRequest,
	stream pb.OrderService_WatchOrderServer,
) error {
	order, ok := s.orders[req.OrderId]
	if !ok {
		return status.Errorf(codes.NotFound, "order %s not found", req.OrderId)
	}

	// Simulate status progression
	statuses := []pb.OrderStatus{
		pb.OrderStatus_ORDER_STATUS_PAID,
		pb.OrderStatus_ORDER_STATUS_SHIPPED,
		pb.OrderStatus_ORDER_STATUS_DELIVERED,
	}

	previousStatus := order.Status
	for _, newStatus := range statuses {
		select {
		case <-stream.Context().Done():
			return status.Error(codes.Cancelled, "client disconnected")
		case <-time.After(2 * time.Second):
			err := stream.Send(&pb.OrderStatusUpdate{
				OrderId:        req.OrderId,
				PreviousStatus: previousStatus,
				NewStatus:      newStatus,
				Timestamp:      timestamppb.Now(),
			})
			if err != nil {
				return err
			}
			previousStatus = newStatus
		}
	}

	return nil
}

func main() {
	lis, err := net.Listen("tcp", ":50051")
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}

	server := grpc.NewServer(
		grpc.UnaryInterceptor(loggingUnaryInterceptor),
		grpc.StreamInterceptor(loggingStreamInterceptor),
	)

	pb.RegisterOrderServiceServer(server, &orderServer{
		orders: make(map[string]*pb.Order),
	})

	log.Println("gRPC server listening on :50051")
	if err := server.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}
```

### Go Interceptors (Middleware)

```go
// interceptors.go
func loggingUnaryInterceptor(
	ctx context.Context,
	req interface{},
	info *grpc.UnaryServerInfo,
	handler grpc.UnaryHandler,
) (interface{}, error) {
	start := time.Now()
	resp, err := handler(ctx, req)
	duration := time.Since(start)

	code := codes.OK
	if err != nil {
		code = status.Code(err)
	}

	log.Printf("unary  method=%s duration=%s code=%s",
		info.FullMethod, duration, code)

	return resp, err
}

func loggingStreamInterceptor(
	srv interface{},
	ss grpc.ServerStream,
	info *grpc.StreamServerInfo,
	handler grpc.StreamHandler,
) error {
	start := time.Now()
	err := handler(srv, ss)
	duration := time.Since(start)

	code := codes.OK
	if err != nil {
		code = status.Code(err)
	}

	log.Printf("stream method=%s duration=%s code=%s",
		info.FullMethod, duration, code)

	return err
}

// Auth interceptor
func authUnaryInterceptor(
	ctx context.Context,
	req interface{},
	info *grpc.UnaryServerInfo,
	handler grpc.UnaryHandler,
) (interface{}, error) {
	md, ok := metadata.FromIncomingContext(ctx)
	if !ok {
		return nil, status.Error(codes.Unauthenticated, "missing metadata")
	}

	tokens := md.Get("authorization")
	if len(tokens) == 0 {
		return nil, status.Error(codes.Unauthenticated, "missing authorization token")
	}

	claims, err := validateToken(tokens[0])
	if err != nil {
		return nil, status.Error(codes.Unauthenticated, "invalid token")
	}

	// Inject claims into context
	ctx = context.WithValue(ctx, "claims", claims)
	return handler(ctx, req)
}
```

### Node.js Server (with @grpc/grpc-js)

```typescript
// server.ts
import * as grpc from '@grpc/grpc-js';
import * as protoLoader from '@grpc/proto-loader';
import path from 'path';

const PROTO_PATH = path.resolve(__dirname, '../proto/order_service.proto');

const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
  keepCase: false,        // Convert to camelCase
  longs: String,          // Use strings for int64
  enums: String,          // Use string names for enums
  defaults: true,
  oneofs: true,
});

const proto = grpc.loadPackageDefinition(packageDefinition) as any;

const orders = new Map<string, any>();

const orderService: grpc.UntypedServiceImplementation = {
  createOrder(
    call: grpc.ServerUnaryCall<any, any>,
    callback: grpc.sendUnaryData<any>
  ) {
    const { customerId, items, shippingAddress, idempotencyKey } = call.request;

    if (!customerId) {
      return callback({
        code: grpc.status.INVALID_ARGUMENT,
        message: 'customer_id is required',
      });
    }

    const orderId = crypto.randomUUID();
    const totalCents = items.reduce(
      (sum: number, item: any) => sum + item.priceCents * item.quantity,
      0
    );

    const order = {
      orderId,
      customerId,
      items,
      status: 'ORDER_STATUS_CREATED',
      totalCents: String(totalCents),
      shippingAddress,
      createdAt: { seconds: Math.floor(Date.now() / 1000) },
      updatedAt: { seconds: Math.floor(Date.now() / 1000) },
    };

    orders.set(orderId, order);

    callback(null, {
      orderId,
      status: 'ORDER_STATUS_CREATED',
      createdAt: order.createdAt,
    });
  },

  getOrder(
    call: grpc.ServerUnaryCall<any, any>,
    callback: grpc.sendUnaryData<any>
  ) {
    const order = orders.get(call.request.orderId);
    if (!order) {
      return callback({
        code: grpc.status.NOT_FOUND,
        message: `Order ${call.request.orderId} not found`,
      });
    }
    callback(null, order);
  },

  watchOrder(call: grpc.ServerWritableStream<any, any>) {
    const order = orders.get(call.request.orderId);
    if (!order) {
      call.destroy({
        code: grpc.status.NOT_FOUND,
        message: `Order ${call.request.orderId} not found`,
      } as any);
      return;
    }

    // Stream status updates
    const statuses = ['ORDER_STATUS_PAID', 'ORDER_STATUS_SHIPPED', 'ORDER_STATUS_DELIVERED'];
    let i = 0;

    const interval = setInterval(() => {
      if (i >= statuses.length) {
        clearInterval(interval);
        call.end();
        return;
      }

      call.write({
        orderId: call.request.orderId,
        previousStatus: i === 0 ? order.status : statuses[i - 1],
        newStatus: statuses[i],
        timestamp: { seconds: Math.floor(Date.now() / 1000) },
      });

      i++;
    }, 2000);

    call.on('cancelled', () => clearInterval(interval));
  },
};

function startServer() {
  const server = new grpc.Server();
  server.addService(proto.orderservice.v1.OrderService.service, orderService);

  server.bindAsync(
    '0.0.0.0:50051',
    grpc.ServerCredentials.createInsecure(),
    (err, port) => {
      if (err) throw err;
      console.log(`gRPC server running on port ${port}`);
    }
  );
}

startServer();
```

### Node.js Client

```typescript
// client.ts
import * as grpc from '@grpc/grpc-js';
import * as protoLoader from '@grpc/proto-loader';

const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
  keepCase: false,
  longs: String,
  enums: String,
  defaults: true,
  oneofs: true,
});

const proto = grpc.loadPackageDefinition(packageDefinition) as any;

const client = new proto.orderservice.v1.OrderService(
  'localhost:50051',
  grpc.credentials.createInsecure(),
  {
    'grpc.keepalive_time_ms': 30000,
    'grpc.keepalive_timeout_ms': 10000,
    'grpc.max_receive_message_length': 4 * 1024 * 1024, // 4MB
  }
);

// Unary call with deadline
function createOrder(request: any): Promise<any> {
  return new Promise((resolve, reject) => {
    const deadline = new Date(Date.now() + 5000); // 5s timeout

    client.createOrder(request, { deadline }, (err: any, response: any) => {
      if (err) {
        console.error(`gRPC error [${err.code}]: ${err.message}`);
        reject(err);
      } else {
        resolve(response);
      }
    });
  });
}

// Server streaming
function watchOrder(orderId: string) {
  const call = client.watchOrder({ orderId });

  call.on('data', (update: any) => {
    console.log('Status update:', update.newStatus);
  });

  call.on('error', (err: any) => {
    if (err.code !== grpc.status.CANCELLED) {
      console.error('Stream error:', err.message);
    }
  });

  call.on('end', () => {
    console.log('Stream ended');
  });

  return call; // Call call.cancel() to stop streaming
}
```

### Proto Compilation (buf.build)

```yaml
# buf.yaml
version: v2
modules:
  - path: proto
    name: buf.build/example/orderservice
lint:
  use:
    - DEFAULT
breaking:
  use:
    - FILE
```

```yaml
# buf.gen.yaml
version: v2
plugins:
  # Go
  - remote: buf.build/protocolbuffers/go
    out: gen/go
    opt: paths=source_relative
  - remote: buf.build/grpc/go
    out: gen/go
    opt: paths=source_relative

  # TypeScript (connect-es for modern TS)
  - remote: buf.build/connectrpc/es
    out: gen/ts
    opt: target=ts
  - remote: buf.build/bufbuild/es
    out: gen/ts
    opt: target=ts
```

```bash
# Generate code
buf generate

# Lint proto files
buf lint

# Check for breaking changes against main branch
buf breaking --against '.git#branch=main'
```

## Best Practices

1. **Always set deadlines on client calls.** A missing deadline means a stuck RPC can hold resources indefinitely. Default to 5-30 seconds depending on the operation.
2. **Use `buf` for proto management.** It handles linting, breaking change detection, and multi-language code generation in a single tool.
3. **Design proto messages for forward compatibility.** Never reuse field numbers. Mark removed fields as `reserved`. Add new fields with new numbers.
4. **Use interceptors for cross-cutting concerns.** Logging, auth, rate limiting, tracing, and metrics belong in interceptors, not service methods.
5. **Prefer server streaming over polling.** If clients repeatedly call an RPC to check for changes, a server-streaming RPC is more efficient.
6. **Use `connect-rpc`** for browser clients instead of grpc-web. Connect supports gRPC, gRPC-web, and a simpler HTTP-based protocol, with first-class TypeScript support.

## Common Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| No deadline set | Stuck RPCs consume connections forever | Always pass a deadline; use interceptor to enforce default |
| Using `int64` without `longs: String` | Precision loss in JavaScript (numbers > 2^53) | Configure proto-loader with `longs: String` or use `BigInt` |
| Proto field number reuse | Silent data corruption after field removal | Use `reserved` for removed fields; never reuse numbers |
| No health check endpoint | Load balancer cannot determine service readiness | Implement gRPC health checking protocol (`grpc.health.v1.Health`) |
| Streaming without backpressure | Memory exhaustion on fast producer / slow consumer | Check `stream.Write` return value in Go; use flow control |
| Large messages without limit | OOM on unexpected payload | Set `grpc.max_receive_message_length` (default 4MB) |
| Missing TLS in production | Plaintext credentials on the wire | Use `grpc.credentials.createSsl()` or mTLS for service-to-service |
| Not handling `UNAVAILABLE` with retry | Transient failures cause user-visible errors | Configure retry policy or use client-side retry interceptor for idempotent RPCs |
