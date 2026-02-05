---
name: design-patterns
description: Game server design patterns including ECS, command pattern, and event sourcing
sasmp_version: "1.3.0"
version: "2.0.0"
bonded_agent: 01-game-server-architect
bond_type: SECONDARY_BOND

# Parameters
parameters:
  required:
    - pattern_type
  optional:
    - storage_backend
  validation:
    pattern_type:
      type: string
      enum: [ecs, command, observer, state_machine, object_pool, event_sourcing]
    storage_backend:
      type: string
      enum: [memory, redis, postgresql]
      default: memory

# Retry Configuration
retry_config:
  max_attempts: 1
  fallback: none

# Observability
observability:
  logging:
    level: debug
    fields: [pattern, entity_count, event_type]
  metrics:
    - name: ecs_entities_total
      type: gauge
    - name: command_execution_duration_us
      type: histogram
    - name: event_sourcing_replay_duration_ms
      type: histogram
    - name: object_pool_utilization
      type: gauge
---

# Design Patterns for Game Servers

Apply **proven design patterns** for scalable, maintainable game server architecture.

## Pattern Selection Guide

| Pattern | Purpose | Use Case |
|---------|---------|----------|
| ECS | Data-oriented design | Entity management |
| Command | Action encapsulation | Input replay, undo |
| Observer | Event notification | State changes |
| State Machine | State transitions | Player states |
| Object Pool | Memory efficiency | Bullets, particles |
| Event Sourcing | Audit trail | Match replay |

## Entity Component System (ECS)

```cpp
// Components - pure data, no logic
struct Position { float x, y, z; };
struct Velocity { float dx, dy, dz; };
struct Health { int current, max; };
struct NetworkSync { uint32_t last_sync_tick; };

// Entity is just an ID
using Entity = uint32_t;

// Component storage
template<typename T>
class ComponentArray {
    std::unordered_map<Entity, T> components;

public:
    void add(Entity e, T component) {
        components[e] = component;
    }

    T* get(Entity e) {
        auto it = components.find(e);
        return it != components.end() ? &it->second : nullptr;
    }

    void remove(Entity e) {
        components.erase(e);
    }
};

// System - logic that operates on components
class MovementSystem {
public:
    void update(float dt, World& world) {
        for (auto& [entity, pos] : world.query<Position, Velocity>()) {
            auto& vel = world.get<Velocity>(entity);
            pos.x += vel.dx * dt;
            pos.y += vel.dy * dt;
            pos.z += vel.dz * dt;
        }
    }
};

class DamageSystem {
public:
    void applyDamage(Entity target, int amount, World& world) {
        if (auto* health = world.get<Health>(target)) {
            health->current -= amount;
            if (health->current <= 0) {
                world.emit<EntityDied>(target);
            }
        }
    }
};
```

## Command Pattern

```cpp
struct GameCommand {
    uint64_t tick;
    uint32_t playerId;

    virtual ~GameCommand() = default;
    virtual void execute(GameState& state) = 0;
    virtual void undo(GameState& state) = 0;
    virtual std::unique_ptr<GameCommand> clone() const = 0;
};

struct MoveCommand : GameCommand {
    Vector3 direction;
    Vector3 previousPosition;  // For undo

    void execute(GameState& state) override {
        auto& player = state.players[playerId];
        previousPosition = player.position;
        player.velocity = direction * player.speed;
    }

    void undo(GameState& state) override {
        state.players[playerId].position = previousPosition;
    }

    std::unique_ptr<GameCommand> clone() const override {
        return std::make_unique<MoveCommand>(*this);
    }
};

// Command history for replay
class CommandHistory {
    std::vector<std::unique_ptr<GameCommand>> history;

public:
    void record(std::unique_ptr<GameCommand> cmd) {
        history.push_back(std::move(cmd));
    }

    GameState replay(const GameState& initial) {
        GameState state = initial;
        for (const auto& cmd : history) {
            cmd->execute(state);
        }
        return state;
    }

    void undoLast(GameState& state) {
        if (!history.empty()) {
            history.back()->undo(state);
            history.pop_back();
        }
    }
};
```

## Event Sourcing

```cpp
// Events are immutable facts
struct GameEvent {
    uint64_t timestamp;
    uint64_t sequence;

    virtual ~GameEvent() = default;
    virtual void apply(GameState& state) const = 0;
    virtual std::string serialize() const = 0;
};

struct PlayerDamaged : GameEvent {
    uint32_t playerId;
    uint32_t sourceId;
    int damage;
    DamageType type;

    void apply(GameState& state) const override {
        auto& player = state.players[playerId];
        player.health -= damage;
        player.lastDamageSource = sourceId;
    }

    std::string serialize() const override {
        return fmt::format("{{\"type\":\"damage\",\"player\":{},\"damage\":{}}}",
                          playerId, damage);
    }
};

class EventStore {
    std::vector<std::unique_ptr<GameEvent>> events;

public:
    void append(std::unique_ptr<GameEvent> event) {
        event->sequence = events.size();
        events.push_back(std::move(event));
    }

    GameState rebuildState() const {
        GameState state;
        for (const auto& event : events) {
            event->apply(state);
        }
        return state;
    }

    GameState rebuildAtTime(uint64_t timestamp) const {
        GameState state;
        for (const auto& event : events) {
            if (event->timestamp > timestamp) break;
            event->apply(state);
        }
        return state;
    }
};
```

## Object Pool

```cpp
template<typename T, size_t N>
class ObjectPool {
    struct PoolEntry {
        T object;
        bool in_use = false;
    };

    std::array<PoolEntry, N> pool;
    std::stack<size_t> free_indices;
    std::mutex mutex;

public:
    ObjectPool() {
        for (size_t i = 0; i < N; ++i) {
            free_indices.push(i);
        }
    }

    T* acquire() {
        std::lock_guard<std::mutex> lock(mutex);
        if (free_indices.empty()) return nullptr;

        size_t idx = free_indices.top();
        free_indices.pop();
        pool[idx].in_use = true;
        return &pool[idx].object;
    }

    void release(T* obj) {
        std::lock_guard<std::mutex> lock(mutex);
        size_t idx = obj - &pool[0].object;
        pool[idx].object.reset();
        pool[idx].in_use = false;
        free_indices.push(idx);
    }

    size_t available() const {
        return free_indices.size();
    }
};

// Usage
ObjectPool<Bullet, 1000> bulletPool;

void fireBullet(Player& player) {
    Bullet* bullet = bulletPool.acquire();
    if (bullet) {
        bullet->init(player.position, player.aimDirection);
        activeBullets.push_back(bullet);
    }
}

void onBulletHit(Bullet* bullet) {
    activeBullets.remove(bullet);
    bulletPool.release(bullet);
}
```

## State Machine

```cpp
enum class PlayerState {
    Idle, Running, Jumping, Attacking, Dead
};

class PlayerStateMachine {
    PlayerState current = PlayerState::Idle;
    std::unordered_map<PlayerState,
        std::unordered_set<PlayerState>> transitions;

public:
    PlayerStateMachine() {
        // Define valid transitions
        transitions[PlayerState::Idle] = {
            PlayerState::Running,
            PlayerState::Jumping,
            PlayerState::Attacking,
            PlayerState::Dead
        };
        transitions[PlayerState::Running] = {
            PlayerState::Idle,
            PlayerState::Jumping,
            PlayerState::Dead
        };
        transitions[PlayerState::Jumping] = {
            PlayerState::Idle,
            PlayerState::Dead
        };
        transitions[PlayerState::Attacking] = {
            PlayerState::Idle,
            PlayerState::Dead
        };
        // Dead is terminal - no transitions out
        transitions[PlayerState::Dead] = {};
    }

    bool canTransition(PlayerState newState) const {
        auto it = transitions.find(current);
        return it != transitions.end() &&
               it->second.count(newState) > 0;
    }

    bool transition(PlayerState newState) {
        if (!canTransition(newState)) return false;

        onExit(current);
        current = newState;
        onEnter(current);
        return true;
    }

private:
    void onEnter(PlayerState state) {
        switch (state) {
            case PlayerState::Jumping:
                player->velocity.y = JUMP_FORCE;
                break;
            case PlayerState::Dead:
                player->onDeath();
                break;
        }
    }

    void onExit(PlayerState state) {
        // Cleanup for previous state
    }
};
```

## Troubleshooting

### Common Failure Modes

| Pattern | Problem | Root Cause | Solution |
|---------|---------|------------|----------|
| ECS | Component fragmentation | Sparse storage | Archetype-based storage |
| Command | Memory bloat | Unbounded history | Limit history size |
| Event Sourcing | Slow replay | Too many events | Periodic snapshots |
| Object Pool | Exhaustion | Leaks | Track allocations |
| State Machine | Invalid state | Missing transition | Validate all paths |

### Debug Checklist

```cpp
// ECS diagnostics
void debugECS(World& world) {
    std::cout << "Entities: " << world.entityCount() << std::endl;
    std::cout << "Components per type:\n";
    world.forEachArchetype([](const Archetype& a) {
        std::cout << "  " << a.signature() << ": " << a.size() << "\n";
    });
}

// Object pool health
void debugPool(ObjectPool& pool) {
    std::cout << "Pool utilization: "
              << (pool.capacity() - pool.available())
              << "/" << pool.capacity() << std::endl;
}

// Event store stats
void debugEventStore(EventStore& store) {
    std::cout << "Events: " << store.size() << std::endl;
    std::cout << "Rebuild time: " << measureRebuildTime(store) << "ms\n";
}
```

## Unit Test Template

```cpp
#include <gtest/gtest.h>

TEST(ECS, CreatesAndQueriesEntities) {
    World world;

    Entity player = world.createEntity();
    world.add<Position>(player, {0, 0, 0});
    world.add<Velocity>(player, {1, 0, 0});

    auto entities = world.query<Position, Velocity>();
    EXPECT_EQ(entities.size(), 1);
}

TEST(Command, UndoRestoresState) {
    GameState state;
    state.players[1].position = {0, 0, 0};

    auto cmd = std::make_unique<MoveCommand>();
    cmd->playerId = 1;
    cmd->direction = {1, 0, 0};

    cmd->execute(state);
    EXPECT_NE(state.players[1].velocity.x, 0);

    cmd->undo(state);
    EXPECT_EQ(state.players[1].position.x, 0);
}

TEST(EventSourcing, RebuildMatchesLive) {
    EventStore store;
    GameState liveState;

    for (int i = 0; i < 100; ++i) {
        auto event = std::make_unique<PlayerDamaged>();
        event->playerId = 1;
        event->damage = 1;
        event->apply(liveState);
        store.append(std::move(event));
    }

    auto rebuiltState = store.rebuildState();
    EXPECT_EQ(rebuiltState.players[1].health, liveState.players[1].health);
}

TEST(ObjectPool, AcquireAndRelease) {
    ObjectPool<Bullet, 10> pool;

    std::vector<Bullet*> acquired;
    for (int i = 0; i < 10; ++i) {
        acquired.push_back(pool.acquire());
        EXPECT_NE(acquired.back(), nullptr);
    }

    // Pool exhausted
    EXPECT_EQ(pool.acquire(), nullptr);

    // Release one
    pool.release(acquired.back());
    acquired.pop_back();

    // Can acquire again
    EXPECT_NE(pool.acquire(), nullptr);
}
```

## Resources

- `assets/` - Pattern implementations
- `references/` - Design pattern catalogs
