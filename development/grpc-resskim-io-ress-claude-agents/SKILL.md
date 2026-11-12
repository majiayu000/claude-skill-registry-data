---
name: grpc
description: "gRPC 서비스 설계 — Protocol Buffers, buf 설정, Go·Spring 구현, 스트리밍, 에러 처리, 인터셉터, gRPC-Gateway. Use when 서비스 간 gRPC API 를 정의하거나 스트리밍·에러 코드·성능 문제를 다룰 때."
---

# gRPC Service Design

gRPC 서비스 설계, Protocol Buffers, 스트리밍, 에러 처리, 성능 최적화

## Quick Reference (결정 트리)

```
통신 방식 선택
    │
    ├─ 브라우저 직접 호출 필요 ──> REST 또는 gRPC-Web
    │
    ├─ 서비스 간 내부 통신 ────> gRPC (권장)
    │
    ├─ 실시간 양방향 통신 ────> gRPC Bidirectional Streaming
    │
    └─ 공개 API ──────────────> REST + gRPC Gateway

스트리밍 타입 선택
    │
    ├─ 요청 1 : 응답 1 ────────> Unary RPC
    │
    ├─ 요청 1 : 응답 N ────────> Server Streaming
    │
    ├─ 요청 N : 응답 1 ────────> Client Streaming
    │
    └─ 요청 N : 응답 M ────────> Bidirectional Streaming
```

---

## Protocol Buffers 기본

### 프로젝트 구조

```
proto/
├── buf.yaml              # buf 설정
├── buf.gen.yaml          # 코드 생성 설정
└── api/
    └── v1/
        ├── user.proto
        └── order.proto
```

### proto 파일 기본 구조

```protobuf
// api/v1/user.proto
syntax = "proto3";

package api.v1;

option go_package = "github.com/myorg/myapp/gen/go/api/v1;apiv1";
option java_package = "com.myorg.myapp.api.v1";
option java_multiple_files = true;

import "google/protobuf/timestamp.proto";
import "google/protobuf/empty.proto";

// 사용자 서비스
service UserService {
  // 사용자 조회
  rpc GetUser(GetUserRequest) returns (GetUserResponse);

  // 사용자 목록 (서버 스트리밍)
  rpc ListUsers(ListUsersRequest) returns (stream User);

  // 사용자 생성
  rpc CreateUser(CreateUserRequest) returns (User);

  // 사용자 삭제
  rpc DeleteUser(DeleteUserRequest) returns (google.protobuf.Empty);
}

message User {
  string id = 1;
  string email = 2;
  string name = 3;
  UserStatus status = 4;
  google.protobuf.Timestamp created_at = 5;
}

enum UserStatus {
  USER_STATUS_UNSPECIFIED = 0;
  USER_STATUS_ACTIVE = 1;
  USER_STATUS_INACTIVE = 2;
}

message GetUserRequest {
  string id = 1;
}

message GetUserResponse {
  User user = 1;
}

message ListUsersRequest {
  int32 page_size = 1;
  string page_token = 2;
}

message CreateUserRequest {
  string email = 1;
  string name = 2;
}

message DeleteUserRequest {
  string id = 1;
}
```

### 필드 번호 규칙

| 범위 | 용도 |
|------|------|
| 1-15 | 자주 사용하는 필드 (1바이트 인코딩) |
| 16-2047 | 일반 필드 (2바이트) |
| 19000-19999 | 예약됨 (사용 금지) |

**주의**: 필드 번호는 절대 재사용/변경 금지 (하위 호환성)

---

## buf 설정 (권장 도구)

### buf.yaml

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

### buf.gen.yaml

```yaml
version: v2
managed:
  enabled: true
  override:
    - file_option: go_package_prefix
      value: github.com/myorg/myapp/gen/go
plugins:
  # Go
  - remote: buf.build/protocolbuffers/go
    out: gen/go
    opt: paths=source_relative
  - remote: buf.build/grpc/go
    out: gen/go
    opt: paths=source_relative

  # Java
  - remote: buf.build/protocolbuffers/java
    out: gen/java
  - remote: buf.build/grpc/java
    out: gen/java
```

### 코드 생성

```bash
# Lint 검사
buf lint

# Breaking change 검사
buf breaking --against '.git#branch=main'

# 코드 생성
buf generate
```

---

## Go 구현

### 서버

```go
package main

import (
    "context"
    "log"
    "net"

    "google.golang.org/grpc"
    "google.golang.org/grpc/codes"
    "google.golang.org/grpc/status"

    pb "github.com/myorg/myapp/gen/go/api/v1"
)

type userServer struct {
    pb.UnimplementedUserServiceServer
    users map[string]*pb.User
}

func (s *userServer) GetUser(ctx context.Context, req *pb.GetUserRequest) (*pb.GetUserResponse, error) {
    if req.Id == "" {
        return nil, status.Error(codes.InvalidArgument, "id is required")
    }

    user, ok := s.users[req.Id]
    if !ok {
        return nil, status.Error(codes.NotFound, "user not found")
    }

    return &pb.GetUserResponse{User: user}, nil
}

func (s *userServer) ListUsers(req *pb.ListUsersRequest, stream pb.UserService_ListUsersServer) error {
    for _, user := range s.users {
        if err := stream.Send(user); err != nil {
            return err
        }
    }
    return nil
}

func main() {
    lis, _ := net.Listen("tcp", ":50051")

    server := grpc.NewServer(
        grpc.UnaryInterceptor(loggingInterceptor),
    )
    pb.RegisterUserServiceServer(server, &userServer{users: make(map[string]*pb.User)})

    log.Println("Server listening on :50051")
    server.Serve(lis)
}

func loggingInterceptor(ctx context.Context, req interface{}, info *grpc.UnaryServerInfo, handler grpc.UnaryHandler) (interface{}, error) {
    log.Printf("RPC: %s", info.FullMethod)
    return handler(ctx, req)
}
```

### 클라이언트

```go
package main

import (
    "context"
    "io"
    "log"
    "time"

    "google.golang.org/grpc"
    "google.golang.org/grpc/credentials/insecure"

    pb "github.com/myorg/myapp/gen/go/api/v1"
)

func main() {
    conn, _ := grpc.NewClient("localhost:50051",
        grpc.WithTransportCredentials(insecure.NewCredentials()),
    )
    defer conn.Close()

    client := pb.NewUserServiceClient(conn)

    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    defer cancel()

    // Unary RPC
    resp, err := client.GetUser(ctx, &pb.GetUserRequest{Id: "123"})
    if err != nil {
        log.Fatal(err)
    }
    log.Printf("User: %v", resp.User)

    // Server Streaming
    stream, _ := client.ListUsers(ctx, &pb.ListUsersRequest{PageSize: 10})
    for {
        user, err := stream.Recv()
        if err == io.EOF {
            break
        }
        log.Printf("User: %v", user)
    }
}
```

---

## Java/Spring 구현 (요약)

```kotlin
// build.gradle.kts
dependencies {
    implementation("net.devh:grpc-spring-boot-starter:3.0.0")
}
```

```java
// 서버: @GrpcService + UserServiceGrpc.UserServiceImplBase 상속
// 클라이언트: @GrpcClient("service-name") + BlockingStub 사용
```

---

## 에러 처리

### gRPC Status Codes

| Code | HTTP | 용도 |
|------|------|------|
| `OK` | 200 | 성공 |
| `INVALID_ARGUMENT` | 400 | 잘못된 요청 |
| `NOT_FOUND` | 404 | 리소스 없음 |
| `ALREADY_EXISTS` | 409 | 중복 |
| `PERMISSION_DENIED` | 403 | 권한 없음 |
| `UNAUTHENTICATED` | 401 | 인증 필요 |
| `INTERNAL` | 500 | 서버 에러 |
| `UNAVAILABLE` | 503 | 서비스 불가 |
| `DEADLINE_EXCEEDED` | 504 | 타임아웃 |

### 상세 에러 (google.rpc.Status)

```protobuf
import "google/rpc/error_details.proto";
```

```go
import (
    "google.golang.org/genproto/googleapis/rpc/errdetails"
    "google.golang.org/grpc/status"
)

func validateUser(req *pb.CreateUserRequest) error {
    var violations []*errdetails.BadRequest_FieldViolation

    if req.Email == "" {
        violations = append(violations, &errdetails.BadRequest_FieldViolation{
            Field:       "email",
            Description: "email is required",
        })
    }

    if len(violations) > 0 {
        st := status.New(codes.InvalidArgument, "validation failed")
        st, _ = st.WithDetails(&errdetails.BadRequest{FieldViolations: violations})
        return st.Err()
    }
    return nil
}
```

---

## 스트리밍 패턴

| 타입 | proto 정의 | 용도 |
|------|-----------|------|
| Server Streaming | `returns (stream T)` | 대량 데이터 내보내기 |
| Client Streaming | `rpc M(stream T)` | 파일 업로드 |
| Bidirectional | `(stream T) returns (stream T)` | 실시간 채팅 |

```go
// Server Streaming: stream.Send(&item) 반복 후 return nil
// Client Streaming: stream.Recv() 반복 후 stream.SendAndClose(&resp)
// Bidirectional: 양쪽 모두 Send/Recv, EOF로 종료 감지
```

---

## 인터셉터 (Middleware)

```go
// 인터셉터 체인 적용
server := grpc.NewServer(
    grpc.ChainUnaryInterceptor(loggingInterceptor, authInterceptor),
)

// 인터셉터 시그니처
func authInterceptor(ctx context.Context, req interface{},
    info *grpc.UnaryServerInfo, handler grpc.UnaryHandler) (interface{}, error) {
    md, _ := metadata.FromIncomingContext(ctx)
    // 토큰 검증 후 handler(ctx, req) 호출
}
```

---

## gRPC-Gateway (REST 변환)

### proto 어노테이션

```protobuf
import "google/api/annotations.proto";

service UserService {
  rpc GetUser(GetUserRequest) returns (User) {
    option (google.api.http) = {
      get: "/v1/users/{id}"
    };
  }

  rpc CreateUser(CreateUserRequest) returns (User) {
    option (google.api.http) = {
      post: "/v1/users"
      body: "*"
    };
  }
}
```

### 게이트웨이 서버

```go
func runGateway() {
    ctx := context.Background()
    mux := runtime.NewServeMux()

    opts := []grpc.DialOption{grpc.WithTransportCredentials(insecure.NewCredentials())}
    pb.RegisterUserServiceHandlerFromEndpoint(ctx, mux, "localhost:50051", opts)

    http.ListenAndServe(":8080", mux)
}
```

---

## 성능 최적화

### Connection Pooling

```go
// 클라이언트 연결 재사용
conn, _ := grpc.NewClient(address,
    grpc.WithTransportCredentials(insecure.NewCredentials()),
    grpc.WithDefaultServiceConfig(`{"loadBalancingConfig": [{"round_robin":{}}]}`),
)
// conn을 전역으로 재사용
```

### Keep-Alive

```go
server := grpc.NewServer(
    grpc.KeepaliveParams(keepalive.ServerParameters{
        MaxConnectionIdle: 5 * time.Minute,
        Time:              2 * time.Hour,
        Timeout:           20 * time.Second,
    }),
)
```

### 메시지 크기 제한

```go
server := grpc.NewServer(
    grpc.MaxRecvMsgSize(10 * 1024 * 1024), // 10MB
    grpc.MaxSendMsgSize(10 * 1024 * 1024),
)
```

---

## Anti-Patterns

| 실수 | 올바른 방법 |
|------|------------|
| 매 요청마다 연결 생성 | 연결 재사용 (Connection Pool) |
| 필드 번호 재사용 | 새 필드는 새 번호 할당 |
| 큰 메시지 한 번에 전송 | 스트리밍으로 분할 |
| 에러에 `UNKNOWN` 사용 | 적절한 Status Code 사용 |
| Deadline 미설정 | 항상 Context Deadline 설정 |

---

## 체크리스트

- [ ] Proto: 패키지 버저닝 (`api.v1`), Enum `UNSPECIFIED = 0`, buf lint 통과
- [ ] 구현: 적절한 Status Code, Context Deadline, 연결 재사용
- [ ] 운영: Health Check (`grpc.health.v1`), Reflection, Prometheus 메트릭

---

## 관련 Skills

- `/architecture:api-design` — REST API 설계 원칙
- `/observability:observability-otel` — gRPC 트레이싱
