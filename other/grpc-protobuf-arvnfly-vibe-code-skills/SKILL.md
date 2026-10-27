---
name: grpc-protobuf
description: "gRPC services, Protocol Buffers schema contracts, streaming RPCs, and backward-compatible message evolution."
---

# gRPC & Protocol Buffers Protocol

Build high-performance binary inter-service RPCs.

---

## 1. Protobuf Backward Compatibility

1. Never change field tag numbers once assigned.
2. Use `reserved` tags when deprecating fields.
3. Treat all fields as optional to facilitate rolling upgrades.

---

## 2. Streaming & Interceptors

Implement logging, authentication, and distributed tracing via gRPC interceptors.
