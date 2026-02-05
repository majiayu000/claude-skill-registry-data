---
name: protobuf-design
description: Protocol Buffers and Interface Definition Languages for service contracts
allowed-tools: Read, Glob, Grep, Write, Edit, mcp__perplexity__search, mcp__context7__resolve-library-id, mcp__context7__query-docs
---

# Protocol Buffers Design Skill

## When to Use This Skill

Use this skill when:

- **Protobuf Design tasks** - Working on protocol buffers and interface definition languages for service contracts
- **Planning or design** - Need guidance on Protobuf Design approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Protocol Buffers (protobuf) and Interface Definition Languages for typed service contracts and efficient serialization.

## MANDATORY: Documentation-First Approach

Before creating protobuf definitions:

1. **Invoke `docs-management` skill** for API contract patterns
2. **Verify proto3 syntax** via MCP servers (context7 for latest spec)
3. **Base all guidance on Google's Protocol Buffers documentation**

## Why Protocol Buffers?

| Benefit | Description |
|---------|-------------|
| **Efficient** | Binary format, 3-10x smaller than JSON |
| **Typed** | Strong typing with code generation |
| **Versioned** | Built-in backward/forward compatibility |
| **Cross-Language** | Supports C#, Java, Python, Go, etc. |
| **gRPC Integration** | Native service definition for gRPC |

## Proto3 Syntax

### Basic Structure

```protobuf
// order_service.proto
syntax = "proto3";

package ecommerce.orders.v1;

option csharp_namespace = "ECommerce.Orders.V1";
option java_package = "com.ecommerce.orders.v1";
option go_package = "github.com/ecommerce/orders/v1;ordersv1";

import "google/protobuf/timestamp.proto";
import "google/protobuf/wrappers.proto";
import "google/protobuf/empty.proto";

// Order service definition
service OrderService {
  // Create a new order
  rpc CreateOrder(CreateOrderRequest) returns (CreateOrderResponse);

  // Get order by ID
  rpc GetOrder(GetOrderRequest) returns (Order);

  // List orders with pagination
  rpc ListOrders(ListOrdersRequest) returns (ListOrdersResponse);

  // Submit order for processing
  rpc SubmitOrder(SubmitOrderRequest) returns (Order);

  // Cancel an order
  rpc CancelOrder(CancelOrderRequest) returns (Order);

  // Stream order status updates
  rpc WatchOrderStatus(WatchOrderStatusRequest) returns (stream OrderStatusUpdate);
}

// Enumerations
enum OrderStatus {
  ORDER_STATUS_UNSPECIFIED = 0;
  ORDER_STATUS_DRAFT = 1;
  ORDER_STATUS_SUBMITTED = 2;
  ORDER_STATUS_PAID = 3;
  ORDER_STATUS_SHIPPED = 4;
  ORDER_STATUS_DELIVERED = 5;
  ORDER_STATUS_CANCELLED = 6;
}

// Messages
message Order {
  string id = 1;
  string customer_id = 2;
  OrderStatus status = 3;
  repeated LineItem items = 4;
  Money subtotal = 5;
  Money tax = 6;
  Money total = 7;
  google.protobuf.Timestamp created_at = 8;
  google.protobuf.Timestamp updated_at = 9;
  optional string tracking_number = 10;
}

message LineItem {
  string id = 1;
  string product_id = 2;
  string product_name = 3;
  int32 quantity = 4;
  Money unit_price = 5;
  Money line_total = 6;
}

message Money {
  int64 units = 1;      // Whole units (e.g., dollars)
  int32 nanos = 2;      // Nano units (10^-9)
  string currency = 3;  // ISO 4217 currency code
}

// Request/Response messages
message CreateOrderRequest {
  string customer_id = 1;
  repeated CreateLineItemRequest items = 2;
}

message CreateLineItemRequest {
  string product_id = 1;
  int32 quantity = 2;
}

message CreateOrderResponse {
  Order order = 1;
}

message GetOrderRequest {
  string id = 1;
}

message ListOrdersRequest {
  int32 page_size = 1;
  string page_token = 2;
  optional string customer_id = 3;
  optional OrderStatus status = 4;
}

message ListOrdersResponse {
  repeated Order orders = 1;
  string next_page_token = 2;
  int32 total_count = 3;
}

message SubmitOrderRequest {
  string id = 1;
}

message CancelOrderRequest {
  string id = 1;
  optional string reason = 2;
}

message WatchOrderStatusRequest {
  string order_id = 1;
}

message OrderStatusUpdate {
  string order_id = 1;
  OrderStatus previous_status = 2;
  OrderStatus current_status = 3;
  google.protobuf.Timestamp timestamp = 4;
  optional string message = 5;
}
```

### Well-Known Types

```protobuf
import "google/protobuf/timestamp.proto";
import "google/protobuf/duration.proto";
import "google/protobuf/wrappers.proto";
import "google/protobuf/any.proto";
import "google/protobuf/struct.proto";
import "google/protobuf/empty.proto";
import "google/protobuf/field_mask.proto";

message Example {
  // Timestamp for date/time
  google.protobuf.Timestamp created_at = 1;

  // Duration for time spans
  google.protobuf.Duration timeout = 2;

  // Wrappers for nullable primitives
  google.protobuf.StringValue optional_name = 3;
  google.protobuf.Int32Value optional_count = 4;
  google.protobuf.BoolValue optional_flag = 5;

  // Any for dynamic typing
  google.protobuf.Any payload = 6;

  // Struct for JSON-like data
  google.protobuf.Struct metadata = 7;

  // FieldMask for partial updates
  google.protobuf.FieldMask update_mask = 8;
}
```

### Advanced Patterns

#### Oneof (Union Types)

```protobuf
message PaymentMethod {
  oneof method {
    CreditCard credit_card = 1;
    BankAccount bank_account = 2;
    PayPalAccount paypal = 3;
  }
}

message CreditCard {
  string number = 1;
  string expiry = 2;
  string cvv = 3;
}

message BankAccount {
  string routing_number = 1;
  string account_number = 2;
}

message PayPalAccount {
  string email = 1;
}
```

#### Maps

```protobuf
message Product {
  string id = 1;
  string name = 2;
  map<string, string> attributes = 3;  // key-value attributes
  map<string, Money> prices_by_region = 4;
}
```

#### Nested Messages

```protobuf
message Customer {
  string id = 1;
  string email = 2;

  message Address {
    string street = 1;
    string city = 2;
    string state = 3;
    string postal_code = 4;
    string country = 5;
  }

  Address shipping_address = 3;
  Address billing_address = 4;
}
```

## gRPC Service Patterns

### Unary RPC

```protobuf
// Simple request-response
rpc GetOrder(GetOrderRequest) returns (Order);
```

### Server Streaming

```protobuf
// Server sends multiple responses
rpc ListOrderHistory(ListOrderHistoryRequest) returns (stream Order);
```

### Client Streaming

```protobuf
// Client sends multiple requests
rpc BatchCreateOrders(stream CreateOrderRequest) returns (BatchCreateResponse);
```

### Bidirectional Streaming

```protobuf
// Both client and server stream
rpc OrderChat(stream OrderMessage) returns (stream OrderMessage);
```

## C# Implementation

### Generated Code Usage

```csharp
// Using generated client
using ECommerce.Orders.V1;
using Grpc.Net.Client;

public sealed class OrderClient
{
    private readonly OrderService.OrderServiceClient _client;

    public OrderClient(string address)
    {
        var channel = GrpcChannel.ForAddress(address);
        _client = new OrderService.OrderServiceClient(channel);
    }

    public async Task<Order> CreateOrderAsync(
        string customerId,
        IEnumerable<(string ProductId, int Quantity)> items,
        CancellationToken ct = default)
    {
        var request = new CreateOrderRequest
        {
            CustomerId = customerId,
            Items = { items.Select(i => new CreateLineItemRequest
            {
                ProductId = i.ProductId,
                Quantity = i.Quantity
            })}
        };

        var response = await _client.CreateOrderAsync(request, cancellationToken: ct);
        return response.Order;
    }

    public async Task<Order> GetOrderAsync(string id, CancellationToken ct = default)
    {
        var request = new GetOrderRequest { Id = id };
        return await _client.GetOrderAsync(request, cancellationToken: ct);
    }

    public async IAsyncEnumerable<OrderStatusUpdate> WatchStatusAsync(
        string orderId,
        [EnumeratorCancellation] CancellationToken ct = default)
    {
        var request = new WatchOrderStatusRequest { OrderId = orderId };
        using var call = _client.WatchOrderStatus(request, cancellationToken: ct);

        await foreach (var update in call.ResponseStream.ReadAllAsync(ct))
        {
            yield return update;
        }
    }
}
```

### Server Implementation

```csharp
using ECommerce.Orders.V1;
using Grpc.Core;

public sealed class OrderServiceImpl : OrderService.OrderServiceBase
{
    private readonly IOrderRepository _orders;
    private readonly ILogger<OrderServiceImpl> _logger;

    public OrderServiceImpl(
        IOrderRepository orders,
        ILogger<OrderServiceImpl> logger)
    {
        _orders = orders;
        _logger = logger;
    }

    public override async Task<CreateOrderResponse> CreateOrder(
        CreateOrderRequest request,
        ServerCallContext context)
    {
        var order = Domain.Order.Create(
            request.CustomerId,
            request.Items.Select(i => new Domain.LineItem(i.ProductId, i.Quantity)));

        await _orders.AddAsync(order, context.CancellationToken);

        return new CreateOrderResponse { Order = MapToProto(order) };
    }

    public override async Task<Order> GetOrder(
        GetOrderRequest request,
        ServerCallContext context)
    {
        var order = await _orders.GetByIdAsync(request.Id, context.CancellationToken);

        if (order is null)
        {
            throw new RpcException(new Status(
                StatusCode.NotFound,
                $"Order {request.Id} not found"));
        }

        return MapToProto(order);
    }

    public override async Task<ListOrdersResponse> ListOrders(
        ListOrdersRequest request,
        ServerCallContext context)
    {
        var (orders, nextToken, total) = await _orders.ListAsync(
            pageSize: request.PageSize,
            pageToken: request.PageToken,
            customerId: request.HasCustomerId ? request.CustomerId : null,
            status: request.HasStatus ? MapToDomain(request.Status) : null,
            ct: context.CancellationToken);

        return new ListOrdersResponse
        {
            Orders = { orders.Select(MapToProto) },
            NextPageToken = nextToken ?? "",
            TotalCount = total
        };
    }

    public override async Task WatchOrderStatus(
        WatchOrderStatusRequest request,
        IServerStreamWriter<OrderStatusUpdate> responseStream,
        ServerCallContext context)
    {
        await foreach (var update in _orders.WatchStatusAsync(
            request.OrderId,
            context.CancellationToken))
        {
            await responseStream.WriteAsync(new OrderStatusUpdate
            {
                OrderId = update.OrderId,
                PreviousStatus = MapToProto(update.PreviousStatus),
                CurrentStatus = MapToProto(update.CurrentStatus),
                Timestamp = Timestamp.FromDateTimeOffset(update.Timestamp),
                Message = update.Message ?? ""
            });
        }
    }

    private static Order MapToProto(Domain.Order order) =>
        new()
        {
            Id = order.Id.ToString(),
            CustomerId = order.CustomerId.ToString(),
            Status = MapToProto(order.Status),
            Items = { order.Items.Select(MapToProto) },
            Subtotal = MapToProto(order.Subtotal),
            Tax = MapToProto(order.Tax),
            Total = MapToProto(order.Total),
            CreatedAt = Timestamp.FromDateTimeOffset(order.CreatedAt),
            UpdatedAt = Timestamp.FromDateTimeOffset(order.UpdatedAt),
            TrackingNumber = order.TrackingNumber ?? ""
        };

    private static LineItem MapToProto(Domain.LineItem item) =>
        new()
        {
            Id = item.Id.ToString(),
            ProductId = item.ProductId.ToString(),
            ProductName = item.ProductName,
            Quantity = item.Quantity,
            UnitPrice = MapToProto(item.UnitPrice),
            LineTotal = MapToProto(item.LineTotal)
        };

    private static Money MapToProto(Domain.Money money) =>
        new()
        {
            Units = (long)money.Amount,
            Nanos = (int)((money.Amount - (long)money.Amount) * 1_000_000_000),
            Currency = money.Currency
        };

    private static OrderStatus MapToProto(Domain.OrderStatus status) =>
        status switch
        {
            Domain.OrderStatus.Draft => OrderStatus.Draft,
            Domain.OrderStatus.Submitted => OrderStatus.Submitted,
            Domain.OrderStatus.Paid => OrderStatus.Paid,
            Domain.OrderStatus.Shipped => OrderStatus.Shipped,
            Domain.OrderStatus.Delivered => OrderStatus.Delivered,
            Domain.OrderStatus.Cancelled => OrderStatus.Cancelled,
            _ => OrderStatus.Unspecified
        };

    private static Domain.OrderStatus MapToDomain(OrderStatus status) =>
        status switch
        {
            OrderStatus.Draft => Domain.OrderStatus.Draft,
            OrderStatus.Submitted => Domain.OrderStatus.Submitted,
            OrderStatus.Paid => Domain.OrderStatus.Paid,
            OrderStatus.Shipped => Domain.OrderStatus.Shipped,
            OrderStatus.Delivered => Domain.OrderStatus.Delivered,
            OrderStatus.Cancelled => Domain.OrderStatus.Cancelled,
            _ => throw new ArgumentOutOfRangeException(nameof(status))
        };
}
```

### ASP.NET Core Registration

```csharp
// Program.cs
var builder = WebApplication.CreateBuilder(args);

builder.Services.AddGrpc();
builder.Services.AddGrpcReflection(); // For tooling like grpcurl

var app = builder.Build();

app.MapGrpcService<OrderServiceImpl>();
app.MapGrpcReflectionService();

app.Run();
```

### .csproj Configuration

```xml
<Project Sdk="Microsoft.NET.Sdk.Web">
  <PropertyGroup>
    <TargetFramework>net10.0</TargetFramework>
  </PropertyGroup>

  <ItemGroup>
    <Protobuf Include="Protos\**\*.proto" GrpcServices="Server" />
  </ItemGroup>

  <ItemGroup>
    <PackageReference Include="Grpc.AspNetCore" Version="2.68.0" />
    <PackageReference Include="Google.Protobuf" Version="3.29.3" />
  </ItemGroup>
</Project>
```

## Schema Evolution

### Backward/Forward Compatibility

```protobuf
// Version 1
message OrderV1 {
  string id = 1;
  string customer_id = 2;
  OrderStatus status = 3;
}

// Version 2 - Adding fields (backward compatible)
message OrderV2 {
  string id = 1;
  string customer_id = 2;
  OrderStatus status = 3;
  // NEW: Added in v2 - old clients ignore, new clients use default
  optional string notes = 4;
  repeated string tags = 5;
}

// Version 3 - Deprecating fields
message OrderV3 {
  string id = 1;
  string customer_id = 2;
  OrderStatus status = 3;
  optional string notes = 4;
  repeated string tags = 5;
  // DEPRECATED: Use customer_id instead
  string customer_email = 6 [deprecated = true];
}
```

### Rules for Safe Evolution

| Action | Safe? | Notes |
|--------|-------|-------|
| Add field | ✅ | Use new field number |
| Remove field | ⚠️ | Use `reserved` to prevent reuse |
| Rename field | ✅ | Field number is what matters |
| Change field number | ❌ | Breaks wire compatibility |
| Change field type | ⚠️ | Some changes compatible |
| Reorder fields | ✅ | Order doesn't matter |

### Reserved Fields

```protobuf
message Order {
  reserved 6, 15, 100 to 200;
  reserved "old_field", "deprecated_field";

  string id = 1;
  // Field 6 was removed, reserved to prevent accidental reuse
}
```

## Buf CLI Integration

### buf.yaml

```yaml
version: v2
lint:
  use:
    - DEFAULT
  except:
    - PACKAGE_VERSION_SUFFIX
breaking:
  use:
    - FILE
```

### buf.gen.yaml

```yaml
version: v2
plugins:
  - remote: buf.build/grpc/csharp
    out: gen/csharp
  - remote: buf.build/protocolbuffers/csharp
    out: gen/csharp
```

### Commands

```bash
# Lint proto files
buf lint

# Check breaking changes
buf breaking --against '.git#branch=main'

# Generate code
buf generate

# Format proto files
buf format -w
```

## Best Practices

### Naming Conventions

```protobuf
// Package: lowercase with dots
package ecommerce.orders.v1;

// Service: PascalCase with "Service" suffix
service OrderService {}

// Method: PascalCase verb phrase
rpc CreateOrder(CreateOrderRequest) returns (CreateOrderResponse);

// Message: PascalCase
message OrderCreatedEvent {}

// Field: snake_case
string customer_id = 1;

// Enum: SCREAMING_SNAKE_CASE with prefix
enum OrderStatus {
  ORDER_STATUS_UNSPECIFIED = 0;
  ORDER_STATUS_DRAFT = 1;
}
```

### API Design Guidelines

1. **Use resource-oriented design**: `GetOrder`, `ListOrders`, `CreateOrder`
2. **Include unspecified enum value at 0**: Handles unknown values gracefully
3. **Use wrappers for optional primitives**: `google.protobuf.StringValue`
4. **Version your packages**: `v1`, `v1beta1`, `v2`
5. **Keep messages focused**: Single responsibility per message
6. **Document with comments**: Use `//` for documentation

## Workflow

When designing protobuf contracts:

1. **Identify Resources**: What entities does the service manage?
2. **Define Messages**: Data structures for each resource
3. **Design Service Methods**: CRUD operations, queries, commands
4. **Add Streaming**: Where real-time updates needed
5. **Document**: Comments for all messages and fields
6. **Lint**: Use Buf or protolint for consistency
7. **Version**: Plan for schema evolution
8. **Generate**: Create client/server code

## References

For detailed guidance:

- [Protocol Buffers Documentation](https://protobuf.dev/) - Official Google Protocol Buffers documentation
- [gRPC Documentation](https://grpc.io/docs/) - Official gRPC documentation and guides
- [Buf CLI](https://buf.build/docs/introduction) - Modern protobuf tooling (lint, breaking, generate)
- [Google API Design Guide](https://cloud.google.com/apis/design) - Resource-oriented API design patterns
- [gRPC for .NET](https://learn.microsoft.com/en-us/aspnet/core/grpc/) - ASP.NET Core gRPC documentation

---

**Last Updated:** 2025-12-26
