---
name: api-grpc
description: >
  Test gRPC / Protocol Buffers APIs — reflection, method enumeration, authz, and injection. Load
  on gRPC services (HTTP/2, content-type application/grpc, .proto files, ports like 50051),
  grpc-web, or "protobuf". Signals: grpc, protobuf, reflection service, ServerReflection.
domain: api
type: technique
stability: learning
modes: [bugbounty, pentest]
severity: high
owasp_api: [API1:2023-BOLA, API5:2023-BFLA]
cwe: [CWE-284]
tools: [grpcurl, grpcui, buf, burp]
schema_version: 1
---

# gRPC / Protobuf API attacks

## When it applies
The target exposes gRPC (or grpc-web). Binary framing over HTTP/2 makes it feel opaque, but the
same authz/injection bugs apply — and server reflection often hands you the whole API.

## Why it works
gRPC methods are RPCs with typed messages; security still lives per-method. Reflection (if on)
exposes every service/method, and teams frequently skip auth on internal-looking RPCs or trust
the client-generated stubs to enforce access.

## Method
1. **Enumerate via reflection**: `grpcurl -plaintext host:50051 list` then `list <service>` and
   `describe <method>`; `grpcui` for an interactive UI. No reflection? Recover `.proto` from the
   client/mobile app or JS (grpc-web).
2. **Call methods directly**: `grpcurl -d '{"id":123}' host:port pkg.Service/Method` — test
   BOLA/BFLA by calling privileged methods or swapping object ids with a low-priv token.
3. **Auth testing**: replay with/without metadata (the gRPC equivalent of headers/tokens); many
   servers authenticate the connection but not each method.
4. **Injection**: message fields feed backends — test SQLi/NoSQLi/command injection in string fields.
5. **grpc-web**: it rides HTTP/1.1+base64 — proxy through Burp, decode frames, tamper.

## Gotchas
- Reflection off ≠ safe — extract the schema from clients; then `grpcurl` with a local `.proto`.
- Binary framing hides bugs from scanners; manual method-by-method testing is the win.
- HTTP/2 + TLS: use `-plaintext` only when the service is plaintext; otherwise pass certs.

## Verify success
Call a method your role shouldn't reach, read/modify another object, or land an injection —
proving per-method authz or input handling is broken.

## References
grpcurl/grpcui docs; OWASP API Security (2023); "hacking gRPC" write-ups.
