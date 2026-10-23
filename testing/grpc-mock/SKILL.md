---
name: grpc-mock
description: "Wraps gRPC server-mocking patterns for client-side tests: Go bufconn (in-memory net.Listener via google.golang.org/grpc/test/bufconn) + mockgen-generated interface mocks, Python pytest-grpc fixtures + unittest.mock patching of stubs, JVM grpc-mock library / in-process gRPC server (InProcessServerBuilder), Node @grpc/grpc-js fake server with NewServer-on-port-0. Also carries the interceptor-layer test patterns (Go / Java / grpc-js auth, retry, logging, error-mapping, chained ordering via a spy handler) in references/interceptors.md. Use when writing client-side tests that need a controllable gRPC server response (success cases, error cases, timeouts, single-response error injection) without spinning up a real backend, or when testing a gRPC interceptor. For multi-message streaming-sequence tests (server-streaming, bidi), use grpc-streaming-test-author instead. Distinct from grpcurl-cli (ad-hoc CLI invocation against a real server) and ghz-load (perf against a real server)."
---

# grpc-mock

## Overview

Mocking a gRPC server lets client-side tests exercise success
paths, every `grpc.StatusCode` (per the status-code catalog in
`grpc-streaming-test-author`, references/status-codes.md),
timeouts, and streaming sequences without a real backend. The
in-process harness is also the substrate for interceptor tests -
see [references/interceptors.md](references/interceptors.md).

Three approaches dominate, picked by language:

| Approach | Mechanism |
|---|---|
| **In-process gRPC server** | A real `grpc.Server` listens on an in-memory transport (`bufconn` in Go, `InProcessServerBuilder` in JVM). Tests exercise the full client stack. |
| **Interface mock** | `mockgen` / `gomock` (Go) / Mockito (JVM) / `unittest.mock` (Python) replace the generated client stub with a programmable mock. Faster but skips marshalling. |
| **Standalone mock server** | Run a tool like `grpcmock` / `dishwasher` as a subprocess. Cross-language client testing. |

## When to use

- Client-side tests need controllable gRPC responses (success +
  error matrix).
- Streaming-RPC tests need a server that sends a deterministic
  sequence.
- Mid-test failure injection (deadline / cancellation / status
  code).
- Tests must not depend on a running backend (offline CI).
- Cross-service contract testing: want the client to see what
  the contract says, not what the current server happens to do.

## Authoring

### Go: bufconn + in-process server

Per
[pkg.go.dev/google.golang.org/grpc/test/bufconn](https://pkg.go.dev/google.golang.org/grpc/test/bufconn),
`bufconn.Listener` is the canonical in-memory transport:

```go
package myservice_test

import (
    "context"
    "net"
    "testing"

    "google.golang.org/grpc"
    "google.golang.org/grpc/codes"
    "google.golang.org/grpc/credentials/insecure"
    "google.golang.org/grpc/status"
    "google.golang.org/grpc/test/bufconn"
    pb "example.com/proto"
)

const bufSize = 1024 * 1024

type fakeServer struct {
    pb.UnimplementedUserServiceServer
    nextResponse *pb.User
    nextErr      error
}

func (f *fakeServer) GetUser(ctx context.Context, req *pb.GetUserRequest) (*pb.User, error) {
    if f.nextErr != nil {
        return nil, f.nextErr
    }
    return f.nextResponse, nil
}

func setupClient(t *testing.T, fake *fakeServer) pb.UserServiceClient {
    lis := bufconn.Listen(bufSize)
    s := grpc.NewServer()
    pb.RegisterUserServiceServer(s, fake)
    go func() { _ = s.Serve(lis) }()
    t.Cleanup(func() { s.Stop() })

    conn, err := grpc.DialContext(context.Background(), "bufnet",
        grpc.WithContextDialer(func(context.Context, string) (net.Conn, error) {
            return lis.Dial()
        }),
        grpc.WithTransportCredentials(insecure.NewCredentials()),
    )
    if err != nil { t.Fatal(err) }
    t.Cleanup(func() { conn.Close() })

    return pb.NewUserServiceClient(conn)
}

func TestGetUser_NotFound(t *testing.T) {
    fake := &fakeServer{
        nextErr: status.Error(codes.NotFound, "user does not exist"),
    }
    client := setupClient(t, fake)

    _, err := client.GetUser(context.Background(), &pb.GetUserRequest{Id: "missing"})

    st, _ := status.FromError(err)
    if st.Code() != codes.NotFound {
        t.Fatalf("got %v, want NotFound", st.Code())
    }
}
```

Per the status-code catalog in `grpc-streaming-test-author`
(references/status-codes.md):
assert on `status.Code()`, not on error message strings.

### Go: gomock / mockgen (interface mock)

For tests that don't need the marshalling/transport stack:

```bash
go install go.uber.org/mock/mockgen@latest
mockgen -source=gen/user_grpc.pb.go -destination=mocks/user_mock.go
```

```go
import (
    "testing"
    "go.uber.org/mock/gomock"
    pb "example.com/proto"
    mocks "example.com/mocks"
)

func TestServiceWithMockClient(t *testing.T) {
    ctrl := gomock.NewController(t)
    mockClient := mocks.NewMockUserServiceClient(ctrl)

    mockClient.EXPECT().
        GetUser(gomock.Any(), gomock.Eq(&pb.GetUserRequest{Id: "u1"})).
        Return(&pb.User{Id: "u1", Name: "Alice"}, nil)

    // Test the code that uses mockClient ...
}
```

Tradeoff: doesn't exercise serialisation; faster, less fidelity.

### Python: in-process server + pytest fixture

```python
import grpc
import pytest
from concurrent import futures
from user_pb2 import User, GetUserRequest
from user_pb2_grpc import UserServiceServicer, add_UserServiceServicer_to_server, UserServiceStub


class FakeUserService(UserServiceServicer):
    next_response = None
    next_status = None

    def GetUser(self, request, context):
        if self.next_status is not None:
            context.abort(self.next_status, "fake error")
        return self.next_response


@pytest.fixture
def fake_service():
    return FakeUserService()


@pytest.fixture
def grpc_channel(fake_service):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    add_UserServiceServicer_to_server(fake_service, server)
    port = server.add_insecure_port("[::]:0")
    server.start()
    channel = grpc.insecure_channel(f"localhost:{port}")
    yield channel
    server.stop(grace=0)


def test_get_user_not_found(fake_service, grpc_channel):
    fake_service.next_status = grpc.StatusCode.NOT_FOUND
    stub = UserServiceStub(grpc_channel)
    with pytest.raises(grpc.RpcError) as exc:
        stub.GetUser(GetUserRequest(id="missing"))
    assert exc.value.code() == grpc.StatusCode.NOT_FOUND
```

`server.add_insecure_port("[::]:0")` lets the OS pick a free
port - important for parallel test execution.

### Python: unittest.mock patching of stub

```python
from unittest.mock import patch, MagicMock
import grpc

def test_service_with_mock_stub():
    with patch("myapp.user_pb2_grpc.UserServiceStub") as MockStub:
        instance = MockStub.return_value
        instance.GetUser.return_value = User(id="u1", name="Alice")

        # Test the code that uses UserServiceStub ...
```

### JVM: InProcessServerBuilder

```java
import io.grpc.inprocess.InProcessChannelBuilder;
import io.grpc.inprocess.InProcessServerBuilder;
import io.grpc.testing.GrpcCleanupRule;

@Rule public final GrpcCleanupRule grpcCleanup = new GrpcCleanupRule();

@Test
public void getUser_notFound() throws Exception {
    String serverName = InProcessServerBuilder.generateName();
    grpcCleanup.register(InProcessServerBuilder
        .forName(serverName)
        .directExecutor()
        .addService(new UserServiceGrpc.UserServiceImplBase() {
            @Override
            public void getUser(GetUserRequest req, StreamObserver<User> obs) {
                obs.onError(Status.NOT_FOUND
                    .withDescription("user does not exist")
                    .asRuntimeException());
            }
        })
        .build()
        .start());

    UserServiceGrpc.UserServiceBlockingStub stub = UserServiceGrpc.newBlockingStub(
        grpcCleanup.register(InProcessChannelBuilder
            .forName(serverName)
            .directExecutor()
            .build()));

    StatusRuntimeException e = assertThrows(StatusRuntimeException.class,
        () -> stub.getUser(GetUserRequest.newBuilder().setId("missing").build()));
    assertEquals(Status.Code.NOT_FOUND, e.getStatus().getCode());
}
```

### Node / TypeScript: @grpc/grpc-js + port 0

```typescript
import * as grpc from "@grpc/grpc-js";
import { UserServiceService } from "./generated/user_grpc_pb";

function createServer(handlers: Partial<UserServiceServer>) {
  const server = new grpc.Server();
  server.addService(UserServiceService, handlers);
  return new Promise<{ port: number; server: grpc.Server }>((resolve, reject) => {
    server.bindAsync("127.0.0.1:0", grpc.ServerCredentials.createInsecure(), (err, port) => {
      if (err) return reject(err);
      server.start();
      resolve({ port, server });
    });
  });
}

test("GetUser returns NOT_FOUND", async () => {
  const { port, server } = await createServer({
    getUser: (_call, callback) => {
      callback({ code: grpc.status.NOT_FOUND, details: "user does not exist" });
    },
  });
  const client = new UserServiceClient(`localhost:${port}`, grpc.credentials.createInsecure());
  await expect(() => promisify(client.getUser.bind(client))({ id: "missing" }))
    .rejects.toMatchObject({ code: grpc.status.NOT_FOUND });
  server.forceShutdown();
});
```

## Running

These tests run as ordinary unit tests:

```bash
go test ./...                 # Go
pytest tests/                 # Python
mvn test                      # JVM
npm test                      # Node
```

Per-language test runners; no separate harness needed.

## Parsing results

Test failures point to:

- **Wrong status code** - fix server-side error mapping or
  test expectation per the status-code catalog in
  `grpc-streaming-test-author` (references/status-codes.md).
- **Marshalling errors** - proto definition / generated code
  drift; regenerate via `buf-cli-lint-breaking-build`.
- **Timeout** - server not responding; fake handler hung;
  check `context.WithTimeout` usage.

## CI integration

```yaml
jobs:
  unit-tests-with-grpc-mocks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-go@v5
      - run: go test ./... -race -timeout=60s
```

`-race` is critical for mock-server tests - concurrent client +
server goroutines often surface races.

## Anti-patterns

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| Asserting on error message strings | Brittle to i18n / wording | Assert on `status.Code()` |
| Hard-coded ports (`8080`) in tests | Port conflicts in parallel CI | Use bufconn (Go), `[::]:0` (Python), InProcessChannel (JVM), port 0 (Node) |
| Sharing one mock server across tests | Test order matters; flaky | Per-test setup; `t.Cleanup` / fixture teardown |
| Mocking gRPC stub without server registration | Tests skip codec, marshalling, error mapping | In-process server preferred over interface mock for service-level tests |
| Returning a Go error directly (not `status.Error`) | Client sees `Code: Unknown` | Always wrap with `status.Errorf(codes.X, "...")` |
| Mocking streaming methods with one response | Tests don't exercise multi-message logic | Use a real stream + `Send` multiple times |
| Forgetting `server.Stop()` in teardown | Goroutine leaks; future tests pollute | `t.Cleanup` / pytest fixture yield |
| No `-race` flag in Go tests | Concurrent races slip through | Always `go test -race` in CI |

## Limitations

- **No wire-level fault injection** in-process. For partial-byte
  cutoffs or middlebox-induced errors, use a real network +
  toxiproxy / tc.
- **bufconn / InProcessServer skip TLS.** Tests that exercise
  TLS-specific code paths need a real server.
- **Streaming-test ergonomics differ per language.** Bidi
  streaming with deterministic interleavings is fiddly
  everywhere; see
  `grpc-streaming-test-author`.
- **Mock-stub approach loses error-mapping fidelity.** A real
  `status.Errorf` wraps differently than a hand-constructed
  Go error.
- **Doesn't replace contract tests.** Mocks reflect what *this
  test* expects; they don't enforce that the real server actually
  produces those responses. Pair with
  `protobuf-compat-checking` (in the qa-contract-testing plugin).

## References

- bufconn Go package:
  [pkg.go.dev/google.golang.org/grpc/test/bufconn](https://pkg.go.dev/google.golang.org/grpc/test/bufconn).
- grpcio Python testing:
  [grpc.io/docs/languages/python/quickstart/](https://grpc.io/docs/languages/python/quickstart/).
- gRPC JVM in-process:
  [grpc.io/docs/languages/java/basics/](https://grpc.io/docs/languages/java/basics/).
- @grpc/grpc-js:
  [github.com/grpc/grpc-node/tree/master/packages/grpc-js](https://github.com/grpc/grpc-node/tree/master/packages/grpc-js).
- Interceptor test patterns (Go / Java / grpc-js playbooks):
  [references/interceptors.md](references/interceptors.md)
  (+ [references/go-interceptors.md](references/go-interceptors.md),
  [references/java-interceptors.md](references/java-interceptors.md),
  [references/grpc-js-interceptors.md](references/grpc-js-interceptors.md)).
- Status-code assertions:
  `grpc-streaming-test-author` (references/status-codes.md).
- Sibling tools:
  `grpcurl-cli`,
  `ghz-load`,
  `grpc-streaming-test-author`.
