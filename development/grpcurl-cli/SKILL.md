---
name: grpcurl-cli
description: "Wraps grpcurl, the curl-equivalent CLI for gRPC. Covers descriptor sources (server reflection default, --import-path + --proto for proto files, --protoset for compiled descriptor sets), service discovery (`list`, `describe`), invoking unary RPCs (`-d '{...}'`, `-d @file.json`, `-d @` for stdin), streaming RPCs (newline-delimited JSON via stdin), TLS configuration (--cacert, --cert, --key, --insecure, --plaintext), header injection (-H 'Authorization: Bearer ...'), and exit codes. Use for ad-hoc gRPC debugging, smoke testing, scriptable PR-time gates, and CLI-based interaction with reflective gRPC services."
---

# grpcurl-cli

## Overview

Per
[github.com/fullstorydev/grpcurl](https://github.com/fullstorydev/grpcurl/blob/master/README.md),
grpcurl can invoke any gRPC method using one of three descriptor
sources (server reflection, `.proto` source files, or compiled
`.protoset` files) and emits JSON responses. This skill wraps
grpcurl for: ad-hoc debugging, scriptable smoke tests, and
CI-based contract verification.

## When to use

- Manually exercising a gRPC server during development.
- Smoke test in CI: "can the deployed server respond to this RPC?"
- Reproducing a production bug locally before writing a test.
- Inspecting a third-party gRPC service that supports reflection.
- Verifying gRPC-to-HTTP gateway behaviour by comparing grpcurl
  + HTTP curl side by side.

## Authoring

### Install

Per [grpcurl README](https://github.com/fullstorydev/grpcurl/blob/master/README.md):

```bash
# Homebrew
brew install grpcurl

# Go install
go install github.com/fullstorydev/grpcurl/cmd/grpcurl@latest

# Docker
docker pull fullstorydev/grpcurl:latest
```

Verify:

```bash
grpcurl -version
```

### Choose a descriptor source

| Source | When |
|---|---|
| **Server reflection** (default) | Server implements the `grpc.reflection.v1` reflection service |
| **Proto source files** (`-import-path` + `-proto`) | Reflection disabled; you have the `.proto` files |
| **Protoset file** (`-protoset`) | Pre-compiled descriptor distributed alongside the binary |

Server reflection is the easiest but security-sensitive - many
production deployments disable it (`reflection.Register(s)` not
called). Plan accordingly.

Generate a protoset if neither reflection nor proto files are
available at call time:

```bash
protoc --proto_path=. \
       --descriptor_set_out=myservice.protoset \
       --include_imports \
       my/custom/server/service.proto
```

## Running

### Discover

Per [grpcurl README](https://github.com/fullstorydev/grpcurl/blob/master/README.md):

```bash
# List services
grpcurl -plaintext localhost:8787 list

# List methods in a service
grpcurl -plaintext localhost:8787 list my.custom.server.Service

# Describe a method (full schema)
grpcurl -plaintext localhost:8787 describe my.custom.server.Service.MethodOne

# Export proto schemas
grpcurl -plaintext -proto-out-dir "out_protos" localhost:8787 \
    describe my.custom.server.Service

# Export a protoset
grpcurl -plaintext -protoset-out "out.protoset" localhost:8787 \
    describe my.custom.server.Service
```

### Invoke unary RPCs

```bash
# Plaintext (no TLS)
grpcurl -plaintext \
    -d '{"id": 1234, "tags": ["foo","bar"]}' \
    localhost:8080 my.custom.server.Service/Method

# TLS with server-only cert
grpcurl -cacert ca.crt \
    -d '{"id": 1234}' \
    grpc.example.com:443 my.custom.server.Service/Method

# Mutual TLS
grpcurl -cacert ca.crt -cert client.crt -key client.key \
    -d '{"id": 1234}' \
    grpc.example.com:443 my.custom.server.Service/Method
```

| Flag | Use |
|---|---|
| `-plaintext` | No TLS (dev / internal) |
| `-insecure` | TLS, but skip verification |
| `-cacert` | CA certificate file |
| `-cert`, `-key` | Client certificate + private key (mTLS) |
| `-H` | Add header (repeat for multiple) |
| `-d` | Inline JSON request payload |
| `-d @<file>` | Read JSON from file |
| `-d @` | Read JSON from stdin |
| `-import-path` | Proto import path |
| `-proto` | Proto file path |
| `-protoset` | Compiled descriptor set |

### Auth headers

```bash
grpcurl -H "Authorization: Bearer ${TOKEN}" \
    -H "x-request-id: $(uuidgen)" \
    -d '{"id": 1234}' \
    grpc.example.com:443 my.custom.server.Service/Method
```

### Streaming RPCs

Per [grpcurl README](https://github.com/fullstorydev/grpcurl/blob/master/README.md):
for bidi or client-streaming, use newline-delimited JSON via
`-d @`:

```bash
grpcurl -plaintext \
    -d @ \
    localhost:8080 my.custom.server.Service/StreamMethod << EOM
{"request": 1}
{"request": 2}
{"request": 3}
EOM
```

Each line is one message to the server. Closing stdin signals
end-of-stream.

### Reproducing a production bug

```bash
# Capture failing request from logs / tracing
PAYLOAD=$(cat trace-payload.json)

# Reproduce against a staging instance
grpcurl -cacert ca.crt \
    -H "Authorization: Bearer ${TOKEN}" \
    -d "${PAYLOAD}" \
    staging.example.com:443 my.custom.server.Service/Method

# Compare status code per grpc-streaming-test-author references/status-codes.md
```

## Parsing results

### Successful response

```json
{
  "id": "1234",
  "name": "alice",
  "createdAt": "2026-05-01T10:30:00Z"
}
```

Exit code 0 → RPC succeeded (gRPC `OK`).

### Error response

```
ERROR:
  Code: NotFound
  Message: User 1234 does not exist
```

Per the status-code catalog in `grpc-streaming-test-author` (references/status-codes.md),
`NotFound` (code 5) maps to HTTP 404 and indicates the resource
isn't present. Exit code is non-zero.

### Exit codes

| Exit code | Meaning |
|---|---|
| 0 | RPC succeeded |
| non-zero | RPC failed (Code printed to stderr) |

For scripting:

```bash
if grpcurl -plaintext -d '{"id":"x"}' \
    localhost:8080 my.Service/GetUser > /tmp/out 2>&1; then
    echo "RPC ok"
else
    code=$(grep "Code:" /tmp/out | awk '{print $2}')
    echo "RPC failed: $code"
fi
```

For richer parsing in CI: `-format=json` and use `jq`:

```bash
grpcurl -plaintext -format=json -d '{"id":"x"}' \
    localhost:8080 my.Service/GetUser \
    | jq '.id'
```

## CI integration

### Smoke test on deploy

```yaml
# .github/workflows/grpc-smoke.yml
name: grpc-smoke
on:
  deployment_status:

jobs:
  smoke:
    if: github.event.deployment_status.state == 'success'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - name: Install grpcurl
        run: |
          # release assets are version-stamped; bump the tag on upgrade
          curl -L https://github.com/fullstorydev/grpcurl/releases/download/v1.9.3/grpcurl_1.9.3_linux_x86_64.tar.gz | tar xz
          # user-owned bin dir on PATH: no sudo, no write to /usr/local/bin
          mkdir -p "$HOME/.local/bin" && mv grpcurl "$HOME/.local/bin/"
          echo "$HOME/.local/bin" >> "$GITHUB_PATH"
      - name: Verify health endpoint
        run: |
          grpcurl -cacert ./certs/ca.crt \
              ${{ github.event.deployment.payload.host }}:443 \
              grpc.health.v1.Health/Check
      - name: Sample request
        env:
          TOKEN: ${{ secrets.SMOKE_TEST_TOKEN }}
        run: |
          grpcurl -cacert ./certs/ca.crt \
              -H "Authorization: Bearer ${TOKEN}" \
              -d '{"id":"smoke-test-1"}' \
              ${{ github.event.deployment.payload.host }}:443 \
              user.v1.UserService/GetUser
```

Exit code 0 → deploy is verified responsive. Non-zero → alert.

### Reflection-based smoke matrix

Where reflection is enabled, smoke-test every RPC:

```bash
SERVICES=$(grpcurl -plaintext localhost:8080 list | grep -v '^grpc')
for service in $SERVICES; do
  METHODS=$(grpcurl -plaintext localhost:8080 list "$service")
  for method in $METHODS; do
    # Skip unary methods that require payload
    grpcurl -plaintext "localhost:8080" "$method" 2>&1 \
      | grep -q "Code: \(Unimplemented\|InvalidArgument\)" || \
        echo "WARN: $method may be unreachable"
  done
done
```

This finds methods registered in reflection but returning
`Unimplemented` (per the status-code catalog in `grpc-streaming-test-author` (references/status-codes.md)).

## Anti-patterns

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| `-insecure` against production endpoints | MITM exposure; certificate validation bypass | Always provide `-cacert` |
| Reflection enabled in production | Schema disclosure; attack surface | Disable reflection in prod; use protoset distribution |
| Long-lived bearer tokens in CI scripts | Token leak via logs / artifacts | Short-lived tokens; mask in CI logs |
| Comparing stdout text across versions | grpcurl reformats; test brittleness | Compare JSON via `-format=json` + `jq` |
| Smoke-testing a write RPC | Side effects in prod / staging | Health-check + read-only smoke only |
| Stream RPC with `-d` inline (no `@`) | Only one message sent | Use `-d @` + stdin |
| No `-H "x-request-id"` | Hard to trace from server logs | Always inject a unique ID for traceability |
| `--proto` without `--import-path` for multi-file schemas | Import resolution fails | Set `--import-path` to project root |

## Limitations

- **Reflection-only is fragile.** Production-disabling reflection
  is standard; smoke matrices need protoset distribution.
- **JSON ↔ proto conversion has edge cases.** `int64` numbers
  large enough to lose precision in JSON become strings (per
  proto-JSON spec); be deliberate.
- **No replay mode.** Can't replay a captured trace; one
  invocation per call.
- **No throughput testing.** For load see
  `ghz-load`.
- **No mock server mode.** For mocking see
  `grpc-mock`.
- **Streaming feedback is line-buffered.** Server-streaming
  responses print as they arrive but stdin flushing can delay
  client-side messages.

## References

- grpcurl README:
  [github.com/fullstorydev/grpcurl](https://github.com/fullstorydev/grpcurl/blob/master/README.md).
- `$GITHUB_PATH` for a user-owned install dir in CI:
  [GitHub Actions: adding a system path](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-commands#adding-a-system-path).
- Companion catalogs:
  `buf-cli-lint-breaking-build` (references/versioning-strategy.md),
  `grpc-streaming-test-author` (references/status-codes.md).
- Sibling tools:
  `buf-cli-lint-breaking-build`,
  `ghz-load`,
  `grpc-mock`,
  `grpc-streaming-test-author`.
- Wire-level streaming semantics:
  `grpc-streaming-test-author` (references/wire-level-testing.md).
