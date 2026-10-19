---
name: grpc-protobuf
description: >
  Design, implement, and maintain high-performance gRPC microservices and Protocol
  Buffers v3 schemas. Use when authoring proto3 definitions, applying backward and forward
  compatibility rules, implementing unary and streaming RPCs (client, server, bidirectional),
  handling rich error status codes and details, configuring deadlines and context
  cancellation, implementing interceptors for auth and telemetry, or enforcing linting with buf.
compatibility: >
  Agent Skills-compatible coding agents working with gRPC, Protocol Buffers v3, and buf tooling across Go, Python, Java, or TypeScript. Tooling is required only for executable validation.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "grpc, protobuf, proto3, microservices, rpc, streaming, buf, distributed-systems"
  topics: "software-development"
---

# gRPC & Protocol Buffers v3 Engineering

Protocol Buffers (protobuf) is Google's language-neutral, platform-neutral binary serialization mechanism, paired with gRPC for high-throughput, low-latency remote procedure calls (RPCs) over HTTP/2. In distributed microservice architectures, gRPC provides strongly typed service contracts, efficient multiplexing, bidirectional streaming, and robust cancellation propagation.

## Purpose & Overview

This skill guides the design, contract evolution, implementation, and verification of production gRPC services and Protocol Buffers v3 schemas. It details proto3 syntax standards, field numbering and reserved tags for backwards compatibility, the four RPC communication patterns (unary, client-streaming, server-streaming, bidirectional), rich error propagation (`google.rpc.Status`), deadline enforcement, interceptors for cross-cutting concerns, and automated schema linting with Buf.

---

## Core Principles & Rules

1. **Field tags are permanent identifiers**: Never change, renumber, or reuse a field number once deployed. Tags 1–15 take 1 byte in the wire encoding (reserve them for high-frequency fields); tags 16–2047 take 2 bytes.
2. **Never delete a field without `reserved`**: When deprecating fields or enum values, mark both the tag number and the field name as `reserved` to prevent accidental future collisions.
3. **Always use explicit request/response wrappers**: Every RPC method must accept a dedicated request message (e.g. `CreateOrderRequest`) and return a dedicated response message (e.g. `CreateOrderResponse`). Never use generic wrappers or reuse messages across distinct RPCs.
4. **Propagate context cancellation and deadlines**: Every client call must specify a deadline. Every server handler must monitor context cancellation (`ctx.Done()` in Go, `context.is_active()` in Python) and terminate long-running work immediately when cancelled.
5. **Use standard gRPC status codes and rich error details**: Do not return HTTP 200 with error bodies or ad-hoc strings. Use canonical codes (`NOT_FOUND`, `INVALID_ARGUMENT`, `UNAUTHENTICATED`) augmented with `google.rpc.ErrorInfo` or `google.rpc.BadRequest` details.
6. **Apply Buf for linting and breaking-change detection**: Treat protobuf repositories as contracts. Run `buf lint` on every PR and `buf breaking --against` the main branch to guarantee forward and backward compatibility.
7. **Protect against unbounded streams**: In streaming RPCs, implement flow control, rate limits, and maximum message sizes (`grpc.max_receive_message_length`) to prevent out-of-memory crashes.

---

## Standard Workflows & Procedures

### Workflow 1: Schema Authoring & Evolution

1. Author proto3 files under package directories matching their import path (e.g., `api/v1/orders.proto`).
2. Define package names with semantic versions (`package commerce.order.v1;`).
3. Define dedicated `Request` and `Response` messages for each RPC.
4. Reserve deprecated tags and identifiers explicitly before removing fields.
5. Validate syntax and style with `buf lint`.
6. Verify backwards compatibility against the upstream baseline using `buf breaking --against '.git#branch=main'`.

### Workflow 2: Implementing Handlers with Deadlines and Rich Errors

1. Extract deadlines from incoming contexts; reject immediately with `DEADLINE_EXCEEDED` if expired.
2. Validate incoming fields against constraints.
3. If validation fails, construct a `google.rpc.BadRequest` detail, attach it to a `status.Status` object with `codes.InvalidArgument`, and return the rich status.
4. If downstream dependencies are called, forward the remaining context deadline.

### Workflow 3: Interceptor Pipeline Setup

1. Chain unary and streaming interceptors in order:
   - Panic / Exception Recovery (outermost)
   - Tracing & Distributed Context Injection (OpenTelemetry)
   - Metrics & Access Logging
   - Authentication & Token Extraction
   - Input Validation (innermost)
2. Keep interceptors non-blocking; delegate long operations to async workers or the handler.

---

## Real-World Examples & Patterns

### 1. Robust proto3 Service Definition

```protobuf
syntax = "proto3";

package commerce.order.v1;

option go_package = "github.com/example/commerce/gen/order/v1;orderv1";
option java_multiple_files = true;
option java_package = "com.commerce.order.v1";

import "google/protobuf/timestamp.proto";
import "google/protobuf/duration.proto";

enum OrderStatus {
  ORDER_STATUS_UNSPECIFIED = 0;
  ORDER_STATUS_PENDING = 1;
  ORDER_STATUS_CONFIRMED = 2;
  ORDER_STATUS_SHIPPED = 3;
  ORDER_STATUS_CANCELLED = 4;
}

message OrderItem {
  string sku = 1;
  int32 quantity = 2;
  int64 price_cents = 3;
}

message Order {
  // Frequently accessed fields: tags 1-15
  string id = 1;
  string customer_id = 2;
  OrderStatus status = 3;
  int64 total_cents = 4;
  repeated OrderItem items = 5;
  google.protobuf.Timestamp created_at = 6;
  google.protobuf.Timestamp updated_at = 7;

  // Deprecated fields: explicitly reserved
  reserved 8, 9;
  reserved "tax_amount", "discount_code";
}

message CreateOrderRequest {
  string customer_id = 1;
  repeated OrderItem items = 2;
  string idempotency_key = 3;
}

message CreateOrderResponse {
  Order order = 1;
}

message StreamOrderUpdatesRequest {
  string customer_id = 1;
}

message OrderUpdateEvent {
  string order_id = 1;
  OrderStatus status = 2;
  google.protobuf.Timestamp timestamp = 3;
  string message = 4;
}

service OrderService {
  // Unary RPC
  rpc CreateOrder(CreateOrderRequest) returns (CreateOrderResponse);

  // Server-streaming RPC for live status updates
  rpc StreamOrderUpdates(StreamOrderUpdatesRequest) returns (stream OrderUpdateEvent);
}
```

### 2. Go Server Handler with Deadlines, Context, & Rich Errors

```go
package main

import (
	"context"
	"errors"
	"time"

	"google.golang.org/genproto/googleapis/rpc/errdetails"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"

	orderv1 "github.com/example/commerce/gen/order/v1"
)

type OrderServer struct {
	orderv1.UnimplementedOrderServiceServer
	repo OrderRepository
}

func (s *OrderServer) CreateOrder(
	ctx context.Context,
	req *orderv1.CreateOrderRequest,
) (*orderv1.CreateOrderResponse, error) {
	// 1. Check for incoming deadline or cancellation
	if err := ctx.Err(); err != nil {
		if errors.Is(err, context.Canceled) {
			return nil, status.Error(codes.Canceled, "client cancelled the request")
		}
		return nil, status.Error(codes.DeadlineExceeded, "deadline exceeded before processing")
	}

	// 2. Validate input and construct rich error details if invalid
	if req.GetCustomerId() == "" || len(req.GetItems()) == 0 {
		st := status.New(codes.InvalidArgument, "invalid order request")
		br := &errdetails.BadRequest{}
		if req.GetCustomerId() == "" {
			br.FieldViolations = append(br.FieldViolations, &errdetails.BadRequest_FieldViolation{
				Field:       "customer_id",
				Description: "customer_id is required",
			})
		}
		if len(req.GetItems()) == 0 {
			br.FieldViolations = append(br.FieldViolations, &errdetails.BadRequest_FieldViolation{
				Field:       "items",
				Description: "items array cannot be empty",
			})
		}
		stWithDetails, err := st.WithDetails(br)
		if err == nil {
			return nil, stWithDetails.Err()
		}
		return nil, st.Err()
	}

	// 3. Execute business logic respecting context deadline
	order, err := s.repo.CreateOrder(ctx, req)
	if err != nil {
		if errors.Is(err, ErrCustomerNotFound) {
			return nil, status.Errorf(codes.NotFound, "customer %q does not exist", req.GetCustomerId())
		}
		return nil, status.Errorf(codes.Internal, "failed to persist order: %v", err)
	}

	return &orderv1.CreateOrderResponse{Order: order}, nil
}

// 4. Server-Streaming RPC handler
func (s *OrderServer) StreamOrderUpdates(
	req *orderv1.StreamOrderUpdatesRequest,
	stream orderv1.OrderService_StreamOrderUpdatesServer,
) error {
	ctx := stream.Context()
	sub := s.repo.SubscribeOrderUpdates(req.GetCustomerId())
	defer sub.Close()

	for {
		select {
		case <-ctx.Done():
			return status.FromContextError(ctx.Err()).Err()
		case event, ok := <-sub.Events():
			if !ok {
				return nil // stream finished normally
			}
			if err := stream.Send(event); err != nil {
				return status.Errorf(codes.Unavailable, "failed to send event: %v", err)
			}
		}
	}
}
```

### 3. Client Call with Timeout Deadlines (Go)

```go
func CallCreateOrder(client orderv1.OrderServiceClient, customerID string) (*orderv1.Order, error) {
	// Set a non-negotiable 3-second deadline for the network roundtrip
	ctx, cancel := context.WithTimeout(context.Background(), 3*time.Second)
	defer cancel()

	resp, err := client.CreateOrder(ctx, &orderv1.CreateOrderRequest{
		CustomerId: customerID,
		Items: []*orderv1.OrderItem{
			{Sku: "WIDGET-01", Quantity: 2, PriceCents: 1500},
		},
	})
	if err != nil {
		st := status.Convert(err)
		switch st.Code() {
		case codes.InvalidArgument:
			// Inspect rich error details
			for _, detail := range st.Details() {
				if br, ok := detail.(*errdetails.BadRequest); ok {
					log.Printf("Validation violations: %v", br.GetFieldViolations())
				}
			}
		case codes.DeadlineExceeded:
			log.Println("Call timed out on server")
		default:
			log.Printf("RPC error: %s (%s)", st.Message(), st.Code())
		}
		return nil, err
	}
	return resp.GetOrder(), nil
}
```

### 4. Buf Configuration (`buf.yaml`)

```yaml
version: v2
modules:
  - path: proto
lint:
  use:
    - DEFAULT
  except:
    - PACKAGE_VERSION_SUFFIX
breaking:
  use:
    - FILE
```

Run validation in CI:
```bash
# Verify lint rules and conventions
buf lint

# Ensure backward compatibility against main branch
buf breaking --against '.git#branch=main'
```

---

## Common Anti-Patterns & Pitfalls

| Anti-Pattern | Why It Fails | Remediated Practice |
|---|---|---|
| **Changing or renumbering a field tag** | Existing binary decoders map the old tag into the wrong field, silently corrupting data in flight. | Keep tag numbers permanent. Add new fields with incremented numbers; deprecate old tags with `reserved`. |
| **Omitting RPC deadlines** | Default client calls have infinite deadlines. If a server hangs or network partitions, client connection pools exhaust. | Always specify `context.WithTimeout` or client interceptor deadline defaults on all outbound calls. |
| **Ignoring server context cancellation** | The server keeps computing or querying databases long after the calling client timed out or disconnected. | Check `ctx.Done()` or pass `ctx` through all database and downstream network calls. |
| **Reusing Request/Response messages across RPCs** | Changing the signature for one RPC inadvertently modifies contracts for completely unrelated RPCs. | Always create dedicated `CreateOrderRequest` / `CreateOrderResponse` for each RPC method. |
| **Returning generic `UNKNOWN` or `INTERNAL` errors** | Clients cannot differentiate retryable network failures from bad arguments or unauthorized requests. | Use specific canonical gRPC status codes (`UNAVAILABLE`, `INVALID_ARGUMENT`, `UNAUTHENTICATED`). |
| **Unbounded streaming RPCs without flow control** | Rapid publishers swamp slow subscribers with memory buffering, leading to OOM crashes. | Honor flow control, apply backpressure, and verify subscriber throughput. |

---

## Verification Checklist

- [ ] All proto files begin with `syntax = "proto3";`.
- [ ] Every RPC accepts a distinct `*Request` and returns a distinct `*Response` message.
- [ ] Deprecated field numbers and field names are marked with `reserved`.
- [ ] High-frequency fields use tags 1 through 15 for 1-byte wire encoding.
- [ ] Client calls enforce an explicit deadline via context or channel options.
- [ ] Server handlers monitor context cancellation and terminate work early when cancelled.
- [ ] Rich error structures (`google.rpc.BadRequest`, `ErrorInfo`) are returned for validation and domain errors.
- [ ] `buf lint` passes cleanly with zero violations.
- [ ] `buf breaking` confirms no wire or source-breaking schema changes against main branch.

---

## Tooling & Reference Guides

- **Linters & Toolchains**: `buf` (Buf CLI for linting, breaking change detection, and code generation).
- **Protobuf Compiler**: `protoc` with plugins `protoc-gen-go`, `protoc-gen-go-grpc`, `protoc-gen-grpc-web`.
- **Debugging & Inspection**: `grpcurl` for CLI gRPC calls, `grpcui` for interactive browser-based testing.
- **Specifications**: [Google gRPC Core Concepts](https://grpc.io/docs/what-is-grpc/core-concepts/), [Protocol Buffers Language Guide (proto3)](https://protobuf.dev/programming-guides/proto3/), [Google APIs Error Model](https://cloud.google.com/apis/design/errors).
