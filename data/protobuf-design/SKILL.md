---
name: protobuf-design
description: Protocol Buffers and Interface Definition Languages for service contracts
allowed-tools: Read, Glob, Grep, Write, Edit, mcp__perplexity__search, mcp__context7__resolve-library-id, mcp__context7__query-docs
---

# Protocol Buffers Design Skill

## When to Use This Skill

Use this skill when:

- **Designing gRPC services** - Protocol Buffers (proto3) for typed service contracts
- **Schema definition** - Messages, enums, services, streaming patterns
- **Implementing in C#** - gRPC with ASP.NET Core
- **Schema evolution** - Backward/forward compatibility, versioning

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

## Proto3 Structure Overview

```protobuf
syntax = "proto3";

package ecommerce.orders.v1;

option csharp_namespace = "ECommerce.Orders.V1";

import "google/protobuf/timestamp.proto";

service OrderService {
  rpc GetOrder(GetOrderRequest) returns (Order);
  rpc ListOrders(ListOrdersRequest) returns (ListOrdersResponse);
  rpc WatchStatus(WatchRequest) returns (stream StatusUpdate);
}

enum OrderStatus {
  ORDER_STATUS_UNSPECIFIED = 0;
  ORDER_STATUS_DRAFT = 1;
  ORDER_STATUS_SUBMITTED = 2;
}

message Order {
  string id = 1;
  string customer_id = 2;
  OrderStatus status = 3;
  google.protobuf.Timestamp created_at = 4;
}
```

**For complete template**: See [proto-syntax.md](references/proto-syntax.md)

## Quick Reference

### gRPC RPC Types

| Pattern | Syntax | Use Case |
|---------|--------|----------|
| Unary | `rpc Get(Req) returns (Resp)` | Simple CRUD |
| Server Stream | `rpc List(Req) returns (stream Resp)` | Large results, updates |
| Client Stream | `rpc Upload(stream Req) returns (Resp)` | Batch uploads |
| Bidirectional | `rpc Chat(stream Req) returns (stream Resp)` | Real-time sync |

**For streaming patterns**: See [grpc-patterns.md](references/grpc-patterns.md)

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Package | lowercase.dots.version | `ecommerce.orders.v1` |
| Service | PascalCase + Service | `OrderService` |
| RPC | PascalCase verb | `CreateOrder` |
| Message | PascalCase | `OrderCreatedEvent` |
| Field | snake_case | `customer_id` |
| Enum | SCREAMING_PREFIX_VALUE | `ORDER_STATUS_DRAFT` |

## Workflow

1. **Identify Resources**: What entities does the service manage?
2. **Define Messages**: Data structures for each resource
3. **Design Service Methods**: CRUD operations, queries, commands
4. **Add Streaming**: Where real-time updates needed
5. **Document**: Comments for all messages and fields
6. **Lint**: Use Buf or protolint for consistency
7. **Version**: Plan for schema evolution
8. **Generate**: Create client/server code

## References

Load on-demand based on need:

| Reference | Load When |
|-----------|-----------|
| [proto-syntax.md](references/proto-syntax.md) | Creating proto definitions, well-known types, advanced patterns |
| [grpc-patterns.md](references/grpc-patterns.md) | Designing streaming services (server, client, bidirectional) |
| [csharp-implementation.md](references/csharp-implementation.md) | Implementing gRPC in .NET/C# with ASP.NET Core |
| [schema-evolution.md](references/schema-evolution.md) | Planning schema changes, Buf CLI, versioning |

## Related Skills (Cross-Plugin)

| Phase | Skill | Plugin | Purpose |
| ----- | ----- | ------ | ------- |
| DESIGN | `protobuf-design` (this skill) | formal-specification | Architecture research, pattern selection |
| AUTHORING | *N/A* | spec-driven-development | **Gap:** `protobuf-authoring` not yet created |

**Workflow:** Design (research gRPC patterns) → Author (create .proto files) → Generate (code generation)

> **Note:** Unlike OpenAPI and AsyncAPI, protobuf authoring is typically straightforward enough that the design skill's C# implementation reference covers concrete creation. A dedicated `protobuf-authoring` skill may be added if demand warrants.

## External References

- [Protocol Buffers Documentation](https://protobuf.dev/) - Official Google documentation
- [gRPC Documentation](https://grpc.io/docs/) - Official gRPC guides
- [Buf CLI](https://buf.build/docs/introduction) - Modern protobuf tooling
- [Google API Design Guide](https://cloud.google.com/apis/design) - Resource-oriented API patterns
- [gRPC for .NET](https://learn.microsoft.com/en-us/aspnet/core/grpc/) - ASP.NET Core gRPC docs

## MCP Research

For current protobuf patterns and tools:

```text
perplexity: "Protocol Buffers proto3" "gRPC service design patterns"
context7: "grpc" (for official documentation)
microsoft-learn: "gRPC ASP.NET Core" (for .NET implementation)
```

## Version History

- **v2.0.0** (2026-01-17): Refactored to progressive disclosure pattern
  - Extracted 4 reference files (~550 lines)
  - Hub reduced from 700 to ~130 lines
  - Updated NuGet package versions (Grpc.AspNetCore 2.71.0)
- **v1.0.0** (2025-12-26): Initial release

---

**Last Updated:** 2026-01-17
