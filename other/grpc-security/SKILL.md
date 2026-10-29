---
name: grpc-security
description: Use when assessing gRPC services on an authorized
  engagement. Covers service enumeration via reflection, auth review,
  message validation, and intercepting gRPC traffic. Also use when a
  microservice backend speaks gRPC behind the REST gateway.
version: 1.0.0
domain: api
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [api-security-testing, api-versioning]
tools:
  - name: Python
    version: "3.12"
  - name: Burp Suite
    version: "2026.2"
---

gRPC services hide behind binary protobuf: harder to see than REST,
but the same flaws live inside. This skill covers authorized
assessment: enumerating services, reviewing auth, and testing message
handling. Test only services you are authorized to assess.

## Quick Workflow

1. Find the gRPC endpoints: ports, gateways, and documentation.
2. Enumerate services: reflection first, then protos from the client
   or repo.
3. Review authentication: per method, not just at the gateway.
4. Test authorization: can a low privilege caller reach admin
   methods.
5. Fuzz messages: malformed protobuf, huge fields, and type
   confusion.
6. Check metadata handling: tokens and keys in headers.
7. Intercept traffic: proxy the HTTP/2 with the right tooling.
8. Report per method with the auth verdict.

## 1. Enumeration via reflection

```bash
# If reflection is enabled, list services (authorized target)
# grpcurl as tooling:
# grpcurl -plaintext target.example:50051 list
# grpcurl -plaintext target.example:50051 list package.Service
echo "reflection enabled in production = information disclosure; note it"
```

```bash
# Without reflection: get the protos from the web client, mobile app,
# or the repo you are authorized to review, then:
# grpcurl -plaintext -proto service.proto target.example:50051 list
```

## 2. Auth testing per method

```python
#!/usr/bin/env python3
"""gRPC method auth matrix (fill from enumeration, test each)."""
methods = [
    ("UserService/GetUser", "user", "pass"),
    ("UserService/ListUsers", "user", "FAIL?"),
    ("AdminService/Shutdown", "user", "must fail"),
]
for method, role, want in methods:
    print(f"[ ] {method} as {role}: expect {want}")
print("test: no token, user token, admin token per method")
print("gateway auth is not enough; check the service too")
```

```bash
# Intercept: Burp supports HTTP/2; point the gRPC client at it
# Look for: tokens in metadata, PII in messages, verbose errors
# Fuzz: send oversized strings, negative ints, and unknown fields;
# watch for 500s and panics (unhandled = DoS or info leak)
echo "malformed protobuf often crashes naive handlers"
```

## Edge cases

- The service uses custom auth metadata. Review the interceptor
  code; custom auth is where the bugs are.
- Reflection disabled and no protos available. Then the assessment
  is traffic analysis plus the methods you can guess; note the
  coverage limit.
- gRPC web in the browser. Test through the browser like a web
  app, with the binary encoding noted.

## Escalation

- Auth missing on a sensitive method: prove with a test account
  call, then report as the top finding.
- Panic on malformed input: report the DoS with the exact bytes.

## Detection and defender view

Defenders see gRPC attacks as unusual method calls, auth failures
per method, and malformed protobuf errors. They defend with
per method auth interceptors, schema validation, and reflection
disabled in production. The durable practice is treating gRPC like
any API: authenticated, authorized, validated, and logged.

## Key references

- CWE-862 (Missing Authorization): per method gaps.
- CWE-20 (Improper Input Validation): message handling.
- gRPC authentication documentation.
