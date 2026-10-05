---
name: grpc
description: Use when gRPC development — Protocol Buffers, service definitions, streaming,
  interceptors, load balancing. Use when working with grpc.
domain: development
author: oyi77
license: Apache-2.0
subdomain: software-development
tags:
- coding
- grpc
- software-engineering
- testing
version: 1.0.0
category: development
---



## Overview

gRPC is a high-performance RPC framework using Protocol Buffers for serialization and HTTP/2 for transport. This skill covers service definition, unary and streaming RPCs, error handling, interceptors, and production deployment patterns.

## Capabilities

- Define services and messages with Protocol Buffers (proto3)
- Implement unary, server-streaming, client-streaming, and bidirectional RPCs
- Handle errors with gRPC status codes
- Build interceptors for auth, logging, and metrics
- Implement health checks and graceful shutdown
- Configure load balancing and service discovery
- Generate client/server code for Go, Python, Node.js, Java

## When to Use
**Trigger phrases:**
- "grpc"
- "gRPC development — Protocol Buffers, service definitions, streaming, interceptor"


- Microservice-to-microservice communication requiring low latency
- Real-time streaming (chat, live data, IoT)
- Polyglot services (multiple languages)
- High-throughput internal APIs
- Mobile-to-backend communication (efficient binary serialization)

## When NOT to Use

- Task is about deployment, not development (use deploy skills)
- Task is about code review, not writing (use review skills)
- You need to understand existing code first (use research skills)
- Task is about testing only (use test skills)
- Requirements are unclear (clarify first)
- Task is trivially simple (single line fix)


## Pseudo Code

The grpc workflow follows a standard pipeline pattern.

Core flow:
```
# grpc primary flow
input = prepare(raw_data)
result = process(input, config={balancing, buffers, definitions, development, grpc})
validate(result)
deliver(result)
```

Error handling:
```
on error:
  log(error_details)
  retry_with_backoff(max=3)
  if still_failing: alert_and_escalate()
```


### Proto Definition
```protobuf
// user.proto
syntax = "proto3";
package user;

service UserService {
  // Unary RPC
  rpc GetUser(GetUserRequest) returns (User);
  // Server streaming
  rpc ListUsers(ListUsersRequest) returns (stream User);
  // Client streaming
  rpc CreateUsers(stream CreateUserRequest) returns (CreateUsersResponse);
  // Bidirectional streaming
  rpc Chat(stream ChatMessage) returns (stream ChatMessage);
}

message GetUserRequest {
  string id = 1;
}

message User {
  string id = 1;
  string name = 2;
  string email = 3;
  int64 created_at = 4;
}

message ListUsersRequest {
  int32 page_size = 1;
  string page_token = 2;
}

message CreateUserRequest {
  string name = 1;
  string email = 2;
}

message CreateUsersResponse {
  int32 count = 1;
}

message ChatMessage {
  string user_id = 1;
  string text = 2;
  int64 timestamp = 3;
}
```

### Server (Node.js)
```javascript
// server.js
const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');

const packageDef = protoLoader.loadSync('user.proto', {
  keepCase: true,
  longs: String,
  enums: String,
  defaults: true,
  oneofs: true,
});

const proto = grpc.loadPackageDefinition(packageDef).user;

const server = new grpc.Server();

server.addService(proto.UserService.service, {
  // Unary RPC
  GetUser: async (call, callback) => {
    const user = await db.users.findById(call.request.id);
    if (!user) {
      return callback({
        code: grpc.status.NOT_FOUND,
        message: 'User not found',
      });
    }
    callback(null, user);
  },

  // Server streaming
  ListUsers: (call) => {
    const stream = db.users.createCursor();
    stream.on('data', (user) => call.write(user));
    stream.on('end', () => call.end());
  },

  // Client streaming
  CreateUsers: (call, callback) => {
    let count = 0;
    call.on('data', async (req) => {
      await db.users.create(req);
      count++;
    });
    call.on('end', () => callback(null, { count }));
  },

  // Bidirectional streaming
  Chat: (call) => {
    call.on('data', (msg) => {
      // Broadcast to all connected clients
      chatClients.forEach(client => client.write(msg));
    });
    chatClients.add(call);
    call.on('end', () => chatClients.delete(call));
  },
});

server.bindAsync('0.0.0.0:50051', grpc.ServerCredentials.createInsecure(), () => {
  console.log('gRPC server running on port 50051');
  server.start();
});
```

### Client (Node.js)
```javascript
// client.js
const client = new proto.UserService('localhost:50051',
  grpc.credentials.createInsecure()
);

// Unary call
client.GetUser({ id: '123' }, (err, response) => {
  if (err) console.error(err);
  else console.log(response);
});

// Server streaming
const stream = client.ListUsers({ pageSize: 100 });
stream.on('data', (user) => console.log(user));
stream.on('end', () => console.log('Done'));

// Bidirectional streaming
const chat = client.Chat();
chat.on('data', (msg) => console.log('Received:', msg));
chat.write({ userId: 'me', text: 'Hello!' });
chat.end();
```

### Interceptor (Auth + Logging)
```javascript
// interceptor.js
const authInterceptor = (options, nextCall) => {
  return new grpc.InterceptingCall(nextCall(options), {
    start: (metadata, listener, next) => {
      metadata.add('authorization', `Bearer ${getToken()}`);
      next(metadata, listener);
    },
  });
};

const loggingInterceptor = (options, nextCall) => {
  return new grpc.InterceptingCall(nextCall(options), {
    start: (metadata, listener, next) => {
      const start = Date.now();
      next(metadata, {
        onReceiveMessage: (message, next) => {
          console.log(`RPC took ${Date.now() - start}ms`);
          next(message);
        },
        ...listener,
      });
    },
  });
};

// Use on client
const client = new proto.UserService('localhost:50051',
  grpc.credentials.createInsecure(),
  { interceptors: [authInterceptor, loggingInterceptor] }
);
```

## Common Patterns

Proven patterns for grpc usage.

- **Batch processing**: Process multiple items in parallel for throughput
- **Retry with backoff**: Handle transient failures gracefully
- **Rate limiting**: Respect API limits with configurable delays
- **Logging**: Structured logging for debugging and audit trails


### Health Check
```protobuf
// health.proto (standard gRPC health check)
service Health {
  rpc Check(HealthCheckRequest) returns (HealthCheckResponse);
}

message HealthCheckRequest { string service = 1; }
message HealthCheckResponse {
  enum ServingStatus { UNKNOWN = 0; SERVING = 1; NOT_SERVING = 2; }
  ServingStatus status = 1;
}
```

### Graceful Shutdown
```javascript
process.on('SIGTERM', () => {
  server.tryShutdown(() => {
    console.log('Server shut down gracefully');
    process.exit(0);
  });
  // Force shutdown after 10s
  setTimeout(() => server.forceShutdown(), 10000);
});
```

### Deadlines
```javascript
// Client sets deadline (5 second timeout)
const deadline = new Date();
deadline.setSeconds(deadline.getSeconds() + 5);
client.GetUser({ id: '123' }, { deadline }, callback);
```

## How to Use

1. Understand the requirement and existing codebase patterns
2. Design the solution with error handling and testability in mind
3. Implement incrementally with tests for each change
4. Verify against expected outcomes (manual and automated)
5. Document usage, edge cases, and integration points
6. Review with team before merging to shared branches

## Red Flags

- **Skipping tests to ship faster**: Untested code breaks in production when you least expect it
- **No error handling in production code**: Unhandled errors crash services and lose user data
- **Hardcoded configuration values**: Hardcoded values prevent environment switching and leak secrets
- **Ignoring security implications**: Missing input validation, auth bypasses, and injection vulnerabilities
- **Over-engineering simple solutions**: Premature abstraction adds complexity without proportional benefit

## Verification

- [ ] Skill output matches expected behavior

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Tests slow me down" | Bugs slow you down 10x more. Tests are speed, not overhead. |
| "I will refactor later" | Technical debt compounds. Refactor as you go. |
| "It works on my machine" | If it is not in CI, it does not work. Ship proof, not claims. |