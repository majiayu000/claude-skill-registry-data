---
name: io-multiplexing
description: High-performance I/O multiplexing including epoll, IOCP, kqueue, and io_uring
sasmp_version: "1.3.0"
version: "2.0.0"
bonded_agent: 02-networking-specialist
bond_type: PRIMARY_BOND

# Parameters
parameters:
  required:
    - io_model
  optional:
    - max_events
    - timeout_ms
  validation:
    io_model:
      type: string
      enum: [epoll, iocp, kqueue, io_uring, select]
    max_events:
      type: integer
      min: 64
      max: 10000
      default: 1024
    timeout_ms:
      type: integer
      min: 0
      max: 1000
      default: 16

# Retry Configuration
retry_config:
  max_attempts: 1
  fallback: blocking_io

# Observability
observability:
  logging:
    level: debug
    fields: [events_count, wait_time_ms]
  metrics:
    - name: io_events_processed
      type: counter
    - name: io_wait_duration_ms
      type: histogram
---

# I/O Multiplexing for Game Servers

Implement **high-performance I/O handling** for thousands of concurrent connections.

## I/O Model Comparison

| Model | Platform | Connections | Latency |
|-------|----------|-------------|---------|
| epoll | Linux | 100K+ | Low |
| kqueue | BSD/macOS | 100K+ | Low |
| IOCP | Windows | 100K+ | Low |
| io_uring | Linux 5.1+ | 1M+ | Lowest |
| select | All | ~1000 | Medium |

## Linux epoll

```c
#include <sys/epoll.h>

int epollfd = epoll_create1(0);

// Add socket
struct epoll_event ev;
ev.events = EPOLLIN | EPOLLET;  // Edge-triggered
ev.data.fd = client_socket;
epoll_ctl(epollfd, EPOLL_CTL_ADD, client_socket, &ev);

// Event loop
struct epoll_event events[MAX_EVENTS];
while (running) {
    int nfds = epoll_wait(epollfd, events, MAX_EVENTS, timeout_ms);
    for (int i = 0; i < nfds; i++) {
        if (events[i].events & EPOLLIN) handleRead(events[i].data.fd);
        if (events[i].events & EPOLLOUT) handleWrite(events[i].data.fd);
    }
}
```

## Linux io_uring

```c
#include <liburing.h>

struct io_uring ring;
io_uring_queue_init(256, &ring, 0);

// Submit read
struct io_uring_sqe *sqe = io_uring_get_sqe(&ring);
io_uring_prep_recv(sqe, socket_fd, buffer, BUFFER_SIZE, 0);
io_uring_sqe_set_data(sqe, &connection);
io_uring_submit(&ring);

// Reap completions
struct io_uring_cqe *cqe;
io_uring_wait_cqe(&ring, &cqe);
Connection* conn = io_uring_cqe_get_data(cqe);
handleCompletion(conn, cqe->res);
io_uring_cqe_seen(&ring, cqe);
```

## Game Server Pattern

```cpp
class GameServer {
    int epollfd;

    void run() {
        while (running) {
            pollEvents(16);  // 16ms = 60 FPS budget
            gameTick();
            broadcastState();
        }
    }

    void pollEvents(int timeout_ms) {
        struct epoll_event events[1024];
        int n = epoll_wait(epollfd, events, 1024, timeout_ms);
        for (int i = 0; i < n; i++) {
            handleEvent(events[i]);
        }
    }
};
```

## Troubleshooting

### Common Failure Modes

| Error | Root Cause | Solution |
|-------|------------|----------|
| EMFILE | Too many fds | Increase ulimit |
| Missed events | Level-triggered bug | Use edge-triggered |
| Starvation | Unbalanced load | Round-robin |
| High latency | Blocking call | Async everything |

### Debug Checklist

```bash
# Check fd limits
ulimit -n

# Monitor fd usage
ls /proc/$(pgrep game-server)/fd | wc -l

# Check epoll stats
cat /proc/$(pgrep game-server)/fdinfo/3
```

## Unit Test Template

```cpp
TEST(EpollServer, HandlesMultipleConnections) {
    EpollServer server(8080);
    vector<TcpClient> clients(100);

    for (auto& client : clients) {
        client.connect("localhost", 8080);
    }

    EXPECT_EQ(server.connectionCount(), 100);
}
```

## Resources

- `assets/` - I/O benchmarks
- `references/` - Platform guides
