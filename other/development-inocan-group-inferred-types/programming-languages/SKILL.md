---
name: programming-languages
description: Core programming languages for game server development including C++, C#, Go, Rust
sasmp_version: "1.3.0"
version: "2.0.0"
bonded_agent: 01-game-server-architect
bond_type: PRIMARY_BOND

# Parameters
parameters:
  required:
    - language
  optional:
    - runtime_version
    - optimization_level
  validation:
    language:
      type: string
      enum: [cpp, csharp, go, rust, java, nodejs]
    optimization_level:
      type: string
      enum: [debug, release, profile]
      default: release

# Retry Configuration
retry_config:
  max_attempts: 1
  fallback: none

# Observability
observability:
  logging:
    level: info
    fields: [language, compile_time_ms]
  metrics:
    - name: compilation_duration_seconds
      type: histogram
---

# Programming Languages for Game Servers

Master **high-performance languages** for real-time game server development.

## Language Comparison

| Language | Performance | Memory | Concurrency | Use Case |
|----------|-------------|--------|-------------|----------|
| C++ | Highest | Manual | Threads | AAA, FPS |
| Rust | High | Safe | Async | New projects |
| Go | High | GC | Goroutines | Microservices |
| C# | Medium | GC | Async | Unity, casual |
| Java | Medium | GC | Threads | MMO |

## C++ Game Server

```cpp
#include <boost/asio.hpp>

class GameServer {
public:
    GameServer(boost::asio::io_context& io, short port)
        : acceptor_(io, tcp::endpoint(tcp::v4(), port)) {
        start_accept();
    }

private:
    void start_accept() {
        auto socket = std::make_shared<tcp::socket>(acceptor_.get_executor());
        acceptor_.async_accept(*socket,
            [this, socket](boost::system::error_code ec) {
                if (!ec) handle_connection(socket);
                start_accept();
            });
    }

    tcp::acceptor acceptor_;
};
```

## Go Server

```go
type GameServer struct {
    players sync.Map
    tick    *time.Ticker
}

func (s *GameServer) handlePlayer(conn net.Conn) {
    defer conn.Close()
    for {
        msg := readMessage(conn)
        go s.processMessage(msg)
    }
}
```

## Rust Server

```rust
async fn handle_player(stream: TcpStream) -> Result<()> {
    let (reader, writer) = stream.split();
    loop {
        let msg = read_message(&mut reader).await?;
        let response = process_command(&msg).await;
        write_message(&mut writer, &response).await?;
    }
}
```

## Selection Criteria

| Factor | Best Choice |
|--------|-------------|
| Latency critical | C++, Rust |
| Rapid development | Go, C# |
| Team expertise | Match existing |
| Scalability | Go, Erlang |

## Troubleshooting

### Common Failure Modes

| Error | Root Cause | Solution |
|-------|------------|----------|
| Memory leak | Manual mgmt | Use RAII/smart ptrs |
| GC pauses | Allocation | Pool objects |
| Thread deadlock | Lock order | Lock hierarchy |
| Segfault | Pointer bug | Use Rust/sanitizers |

### Debug Checklist

```bash
# C++ memory check
valgrind --leak-check=full ./game-server

# Go profiling
go tool pprof http://localhost:6060/debug/pprof/heap

# Rust optimization
cargo build --release
```

## Unit Test Template

```cpp
TEST(GameServer, AcceptsConnections) {
    GameServer server(8080);
    TcpClient client;
    client.connect("localhost", 8080);
    EXPECT_TRUE(client.isConnected());
}
```

## Resources

- `assets/` - Language templates
- `references/` - Performance guides
