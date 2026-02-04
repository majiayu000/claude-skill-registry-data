---
name: socket-programming
description: Low-level socket programming including BSD sockets, Winsock, and network byte manipulation
sasmp_version: "1.3.0"
version: "2.0.0"
bonded_agent: 02-networking-specialist
bond_type: SECONDARY_BOND

# Parameters
parameters:
  required:
    - socket_type
  optional:
    - buffer_size
    - non_blocking
  validation:
    socket_type:
      type: string
      enum: [tcp, udp, raw]
    buffer_size:
      type: integer
      min: 1024
      max: 65536
      default: 8192
    non_blocking:
      type: boolean
      default: true

# Retry Configuration
retry_config:
  max_attempts: 3
  backoff: exponential
  initial_delay_ms: 100
  retryable_errors:
    - ECONNREFUSED
    - ETIMEDOUT

# Observability
observability:
  logging:
    level: debug
    fields: [socket_fd, bytes_transferred]
  metrics:
    - name: socket_bytes_sent
      type: counter
    - name: socket_bytes_received
      type: counter
---

# Socket Programming for Games

Master **low-level socket programming** for custom game networking.

## Socket Types

| Type | Protocol | Use Case |
|------|----------|----------|
| SOCK_STREAM | TCP | Reliable data |
| SOCK_DGRAM | UDP | Real-time |
| SOCK_RAW | Raw IP | Custom protocols |

## BSD Socket (C)

```c
#include <sys/socket.h>
#include <netinet/in.h>

int create_game_server(int port) {
    int sockfd = socket(AF_INET, SOCK_DGRAM, 0);

    struct sockaddr_in addr = {
        .sin_family = AF_INET,
        .sin_port = htons(port),
        .sin_addr.s_addr = INADDR_ANY
    };

    bind(sockfd, (struct sockaddr*)&addr, sizeof(addr));
    fcntl(sockfd, F_SETFL, O_NONBLOCK);

    return sockfd;
}
```

## Socket Options

```c
// Disable Nagle (reduce latency)
int flag = 1;
setsockopt(sockfd, IPPROTO_TCP, TCP_NODELAY, &flag, sizeof(flag));

// Enable address reuse
setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &flag, sizeof(flag));

// Set buffer size
int bufsize = 65536;
setsockopt(sockfd, SOL_SOCKET, SO_RCVBUF, &bufsize, sizeof(bufsize));
```

## Byte Order

```c
// Network byte order
uint16_t port_net = htons(8080);
uint32_t ip_net = htonl(ip_host);

// Host byte order
uint16_t port_host = ntohs(port_net);
```

## Platform Differences

| Feature | BSD | Winsock |
|---------|-----|---------|
| Init | None | WSAStartup() |
| Close | close() | closesocket() |
| Error | errno | WSAGetLastError() |
| Non-block | fcntl() | ioctlsocket() |

## Troubleshooting

### Common Failure Modes

| Error | Root Cause | Solution |
|-------|------------|----------|
| EADDRINUSE | Port in use | SO_REUSEADDR |
| ECONNRESET | Peer closed | Handle gracefully |
| EMFILE | Too many fds | Increase ulimit |
| High latency | Nagle | TCP_NODELAY |

### Debug Checklist

```bash
# Check listening sockets
netstat -tlnp | grep game-server

# Trace syscalls
strace -e socket,bind,connect ./game-server

# Monitor traffic
tcpdump -i lo port 8080
```

## Unit Test Template

```c
void test_socket_creation() {
    int fd = create_game_server(8080);
    assert(fd >= 0);

    struct sockaddr_in addr;
    socklen_t len = sizeof(addr);
    getsockname(fd, (struct sockaddr*)&addr, &len);
    assert(ntohs(addr.sin_port) == 8080);

    close(fd);
}
```

## Resources

- `assets/` - Socket templates
- `references/` - Platform guides
