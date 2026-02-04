---
name: multithreading
description: Multithreading and concurrency patterns for game servers including synchronization primitives
sasmp_version: "1.3.0"
version: "2.0.0"
bonded_agent: 01-game-server-architect
bond_type: SECONDARY_BOND

# Parameters
parameters:
  required:
    - threading_model
  optional:
    - thread_count
    - queue_size
  validation:
    threading_model:
      type: string
      enum: [single, thread_per_connection, thread_pool, actor]
    thread_count:
      type: integer
      min: 1
      max: 256
      default: 0  # 0 = auto (CPU cores)
    queue_size:
      type: integer
      min: 100
      max: 100000
      default: 10000

# Retry Configuration
retry_config:
  max_attempts: 1
  fallback: single_threaded

# Observability
observability:
  logging:
    level: debug
    fields: [thread_id, task_type, duration_us]
  metrics:
    - name: thread_pool_active_threads
      type: gauge
    - name: task_queue_size
      type: gauge
    - name: task_execution_duration_us
      type: histogram
    - name: lock_contention_count
      type: counter
---

# Multithreading for Game Servers

Implement **thread-safe game server architectures** with proper synchronization.

## Threading Models

| Model | Pros | Cons | Use Case |
|-------|------|------|----------|
| Single-threaded | Simple, predictable | Limited scale | Casual games |
| Thread-per-connection | Simple | High overhead | Small servers |
| Thread pool | Efficient | Complex | Most games |
| Actor model | No locks | Learning curve | Distributed |

## Synchronization Primitives

### Mutex (Mutual Exclusion)

```cpp
std::mutex game_state_mutex;

void updatePlayerPosition(int playerId, Vector3 pos) {
    std::lock_guard<std::mutex> lock(game_state_mutex);
    players[playerId].position = pos;
}
```

### Read-Write Lock

```cpp
std::shared_mutex players_rwlock;

// Multiple concurrent readers
Vector3 getPlayerPosition(int playerId) {
    std::shared_lock<std::shared_mutex> lock(players_rwlock);
    return players[playerId].position;
}

// Exclusive writer
void setPlayerPosition(int playerId, Vector3 pos) {
    std::unique_lock<std::shared_mutex> lock(players_rwlock);
    players[playerId].position = pos;
}
```

### Spinlock (Low Latency)

```cpp
std::atomic_flag spinlock = ATOMIC_FLAG_INIT;

void criticalSection() {
    while (spinlock.test_and_set(std::memory_order_acquire)) {
        // Spin - use for very short critical sections only
    }
    // Critical section
    spinlock.clear(std::memory_order_release);
}
```

## Lock-Free Patterns

```cpp
// Lock-free player state updates
struct PlayerState {
    std::atomic<float> x, y, z;
    std::atomic<int> health;
};

// Compare-and-swap for safe updates
bool tryDamagePlayer(std::atomic<int>& health, int damage) {
    int current = health.load();
    int newHealth = current - damage;
    return health.compare_exchange_strong(current, newHealth);
}

// SPSC Lock-free queue
template<typename T, size_t Size>
class SPSCQueue {
    std::array<T, Size> buffer;
    std::atomic<size_t> head{0};
    std::atomic<size_t> tail{0};

public:
    bool push(const T& item) {
        size_t current_tail = tail.load(std::memory_order_relaxed);
        size_t next = (current_tail + 1) % Size;
        if (next == head.load(std::memory_order_acquire)) return false;
        buffer[current_tail] = item;
        tail.store(next, std::memory_order_release);
        return true;
    }

    bool pop(T& item) {
        size_t current_head = head.load(std::memory_order_relaxed);
        if (current_head == tail.load(std::memory_order_acquire)) return false;
        item = buffer[current_head];
        head.store((current_head + 1) % Size, std::memory_order_release);
        return true;
    }
};
```

## Thread Pool Pattern

```cpp
class GameThreadPool {
    std::vector<std::thread> workers;
    std::queue<std::function<void()>> tasks;
    std::mutex queue_mutex;
    std::condition_variable condition;
    std::atomic<bool> stop{false};

public:
    explicit GameThreadPool(size_t threads = 0) {
        if (threads == 0) {
            threads = std::thread::hardware_concurrency();
        }

        for (size_t i = 0; i < threads; ++i) {
            workers.emplace_back([this] {
                while (true) {
                    std::function<void()> task;
                    {
                        std::unique_lock<std::mutex> lock(queue_mutex);
                        condition.wait(lock, [this] {
                            return stop || !tasks.empty();
                        });
                        if (stop && tasks.empty()) return;
                        task = std::move(tasks.front());
                        tasks.pop();
                    }
                    task();
                }
            });
        }
    }

    template<typename F>
    void enqueue(F&& task) {
        {
            std::unique_lock<std::mutex> lock(queue_mutex);
            tasks.push(std::forward<F>(task));
        }
        condition.notify_one();
    }

    ~GameThreadPool() {
        stop = true;
        condition.notify_all();
        for (auto& worker : workers) {
            worker.join();
        }
    }
};
```

## Game Server Architecture

```cpp
class ThreadedGameServer {
    GameThreadPool network_pool;  // Handle network I/O
    GameThreadPool game_pool;     // Game logic

    std::shared_mutex state_mutex;
    GameState state;

public:
    void onPacketReceived(Connection* conn, Packet& pkt) {
        // Network thread - parse and validate
        auto cmd = parseCommand(pkt);

        // Queue to game thread
        game_pool.enqueue([this, cmd] {
            std::unique_lock lock(state_mutex);
            state.applyCommand(cmd);
        });
    }

    void broadcastState() {
        std::shared_lock lock(state_mutex);
        auto snapshot = state.serialize();

        // Fan out on network threads
        for (auto& conn : connections) {
            network_pool.enqueue([conn, snapshot] {
                conn->send(snapshot);
            });
        }
    }
};
```

## Troubleshooting

### Common Failure Modes

| Problem | Root Cause | Solution |
|---------|------------|----------|
| Deadlock | Lock ordering violation | Consistent lock hierarchy |
| Priority inversion | Low priority holds lock | Priority inheritance mutex |
| False sharing | Adjacent atomics | Cache line padding |
| Race conditions | Missing synchronization | Atomic operations/locks |
| Thread starvation | Unfair scheduling | Fair lock or work stealing |
| Memory visibility | Missing barriers | Proper memory ordering |

### Debug Checklist

```bash
# Check thread count
ps -T -p $(pgrep game-server) | wc -l

# Thread CPU usage
top -H -p $(pgrep game-server)

# Detect deadlocks (Linux)
pstack $(pgrep game-server)

# Valgrind thread checker
valgrind --tool=helgrind ./game-server

# ThreadSanitizer
clang++ -fsanitize=thread -g game-server.cpp
```

```cpp
// Runtime deadlock detection
#include <mutex>
#include <thread>

class DeadlockDetector {
    std::unordered_map<std::thread::id, std::vector<void*>> held_locks;
    std::mutex detector_mutex;

public:
    void onLockAcquire(void* lock) {
        std::lock_guard<std::mutex> guard(detector_mutex);
        held_locks[std::this_thread::get_id()].push_back(lock);
        // Check for cycles in lock graph
    }
};
```

## Unit Test Template

```cpp
#include <gtest/gtest.h>
#include <thread>
#include <vector>

TEST(Threading, ThreadPoolExecutesTasks) {
    GameThreadPool pool(4);
    std::atomic<int> counter{0};

    for (int i = 0; i < 1000; ++i) {
        pool.enqueue([&counter] {
            counter++;
        });
    }

    std::this_thread::sleep_for(std::chrono::milliseconds(100));
    EXPECT_EQ(counter.load(), 1000);
}

TEST(Threading, RWLockAllowsConcurrentReads) {
    std::shared_mutex mutex;
    std::atomic<int> concurrent_readers{0};
    int max_concurrent = 0;

    std::vector<std::thread> threads;
    for (int i = 0; i < 10; ++i) {
        threads.emplace_back([&] {
            std::shared_lock lock(mutex);
            int current = ++concurrent_readers;
            max_concurrent = std::max(max_concurrent, current);
            std::this_thread::sleep_for(std::chrono::milliseconds(10));
            --concurrent_readers;
        });
    }

    for (auto& t : threads) t.join();
    EXPECT_GT(max_concurrent, 1);  // Multiple concurrent readers
}

TEST(Threading, AtomicCASWorks) {
    std::atomic<int> health{100};

    // Simulate concurrent damage
    std::vector<std::thread> threads;
    for (int i = 0; i < 10; ++i) {
        threads.emplace_back([&health] {
            int expected = health.load();
            while (!health.compare_exchange_weak(expected, expected - 10)) {
                // Retry
            }
        });
    }

    for (auto& t : threads) t.join();
    EXPECT_EQ(health.load(), 0);
}
```

## Resources

- `assets/` - Threading patterns
- `references/` - Concurrency guides
