---
name: kurrentdb
description: Provides KurrentDB (EventStoreDB) client code for event sourcing and CQRS. Generates correct package names, connection strings, and API patterns for Python, Node.js, .NET, F#, Go, Java, Rust. Triggers on "kurrentdb", "eventstore", "event sourcing", "append events", "read stream", "subscription", "aggregate", "CQRS".
---

# KurrentDB Development Skill

Provides working code for KurrentDB (formerly EventStoreDB) - the event-native database.

## When to Read Additional Files

| Need | Read |
|------|------|
| Full API reference for any language | `reference.md` |
| Ready-to-run project templates | `templates/{language}/` |

## Quick Reference

### Docker Setup (Insecure Single Node)

```bash
docker run --name kurrentdb-node -it -p 2113:2113 \
    docker.kurrent.io/kurrent-latest/kurrentdb:latest \
    --insecure --run-projections=All --enable-atom-pub-over-http
```

Or use docker-compose - see `templates/docker-compose.yaml`

**Connection String:** `kurrentdb://localhost:2113?tls=false`
**Web UI:** http://localhost:2113

### Client Installation Quick Reference

| Language | Install Command |
|----------|-----------------|
| .NET/C# | `dotnet add package KurrentDB.Client` |
| F# | `dotnet add package KurrentDB.Client` |
| Java | Add `com.eventstore:db-client-java:5.3.2` to pom.xml |
| Python | `pip install kurrentdbclient` |
| Node.js | `npm install @kurrent/kurrentdb-client` |
| Go | `go get github.com/kurrent-io/KurrentDB-Client-Go/kurrentdb` |
| Rust | Add `kurrentdb = "1.0"` to Cargo.toml |

## Key API Patterns

### Optimistic Concurrency (CRITICAL)
ALWAYS use expected revision for aggregates:
- `NO_STREAM` - Creating new aggregate (stream must not exist)
- `StreamExists` - Appending to existing stream
- Specific revision number - Prevent concurrent modifications

### Subscriptions
- **Catch-up**: Read history + live events. Use for projections.
- **Persistent**: Server-managed with ACK/NACK. Use for reliable processing.

### System Streams
- `$ce-{category}` - All events from streams matching pattern (e.g., `$ce-order` for `order-*`)
- `$et-{eventType}` - All events of a type (e.g., `$et-OrderCreated`)

## Official Documentation

- https://docs.kurrent.io/server/
- https://docs.kurrent.io/clients/
