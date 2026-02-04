---
name: probitas-info
description: Information about Probitas framework. Use when asked "what is Probitas", explaining its purpose, features, or comparing with other test frameworks.
---

## What is Probitas?

Scenario-based E2E testing framework for backend services (APIs, databases,
message queues).

## Key Features

| Feature           | Description                              |
| ----------------- | ---------------------------------------- |
| Scenario-Based    | Tests as readable scenarios with steps   |
| Built-in Clients  | HTTP, gRPC, GraphQL, SQL, Redis, MongoDB |
| Fluent Assertions | Unified `expect()` with chainable checks |
| Auto Cleanup      | Resources with automatic cleanup         |
| Batteries         | faker, FakeTime, spy, stub included      |

## Quick Example

```typescript
import { client, expect, scenario } from "jsr:@probitas/probitas";

export default scenario("API Test", { tags: ["http"] })
  .resource("http", () =>
    client.http.createHttpClient({
      url: Deno.env.get("API_URL") ?? "http://localhost:8080",
    }))
  .step("GET /users", async (ctx) => {
    const res = await ctx.resources.http.get("/users");
    expect(res).toBeOk().toHaveStatus(200);
  })
  .build();
```

## Available Clients

| Client     | Factory Function                             | Use Case             |
| ---------- | -------------------------------------------- | -------------------- |
| HTTP       | `client.http.createHttpClient()`             | REST APIs, webhooks  |
| HTTP OIDC  | `client.http.oidc.createOidcHttpClient()`    | OAuth 2.0/OIDC APIs  |
| PostgreSQL | `client.sql.postgres.createPostgresClient()` | PostgreSQL databases |
| MySQL      | `client.sql.mysql.createMySqlClient()`       | MySQL databases      |
| SQLite     | `client.sql.sqlite.createSqliteClient()`     | Embedded databases   |
| DuckDB     | `client.sql.duckdb.createDuckDbClient()`     | Analytics databases  |
| gRPC       | `client.grpc.createGrpcClient()`             | gRPC services        |
| ConnectRPC | `client.connectrpc.createConnectRpcClient()` | Connect/gRPC-Web     |
| GraphQL    | `client.graphql.createGraphqlClient()`       | GraphQL APIs         |
| Redis      | `client.redis.createRedisClient()`           | Cache, pub/sub       |
| MongoDB    | `client.mongodb.createMongoClient()`         | Document databases   |
| Deno KV    | `client.deno_kv.createDenoKvClient()`        | Deno KV store        |
| RabbitMQ   | `client.rabbitmq.createRabbitMqClient()`     | AMQP message queues  |
| SQS        | `client.sqs.createSqsClient()`               | AWS message queues   |

## API Reference

Use `deno doc` to look up API:

```bash
# Core module
deno doc jsr:@probitas/probitas

# Client modules (use pattern: jsr:@probitas/probitas/client/<name>)
deno doc jsr:@probitas/probitas/client/http
deno doc jsr:@probitas/probitas/client/http/oidc
deno doc jsr:@probitas/probitas/client/grpc
deno doc jsr:@probitas/probitas/client/connectrpc
deno doc jsr:@probitas/probitas/client/graphql
deno doc jsr:@probitas/probitas/client/redis
deno doc jsr:@probitas/probitas/client/mongodb
deno doc jsr:@probitas/probitas/client/rabbitmq
deno doc jsr:@probitas/probitas/client/sqs
deno doc jsr:@probitas/probitas/client/deno_kv
deno doc jsr:@probitas/probitas/client/sql        # Common SQL types
deno doc jsr:@probitas/probitas/client/sql/postgres
deno doc jsr:@probitas/probitas/client/sql/mysql
deno doc jsr:@probitas/probitas/client/sql/sqlite
deno doc jsr:@probitas/probitas/client/sql/duckdb
```

## Documentation

- LLM sitemap: https://probitas-test.github.io/llms.txt
