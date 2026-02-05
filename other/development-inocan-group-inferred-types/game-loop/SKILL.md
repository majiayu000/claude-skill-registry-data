---
name: game-loop
description: Server-side game loop implementation with fixed timestep, physics simulation, and tick rate optimization
sasmp_version: "1.3.0"
version: "2.0.0"
bonded_agent: 05-game-loop-developer
bond_type: PRIMARY_BOND

# Parameters
parameters:
  required:
    - tick_rate
  optional:
    - physics_enabled
    - max_tick_catchup
  validation:
    tick_rate:
      type: integer
      min: 1
      max: 128
    physics_enabled:
      type: boolean
      default: true
    max_tick_catchup:
      type: integer
      min: 1
      max: 10
      default: 5

# Retry Configuration
retry_config:
  max_attempts: 1
  fallback: skip_frame

# Observability
observability:
  logging:
    level: info
    fields: [tick_number, tick_time_ms, entity_count]
  metrics:
    - name: game_tick_duration_seconds
      type: histogram
    - name: game_tick_count
      type: counter
    - name: game_entity_count
      type: gauge
---

# Server Game Loop

Implement **deterministic game loops** with fixed timestep for consistent gameplay.

## Fixed Timestep Loop

```javascript
class GameLoop {
  constructor(tickRate = 60) {
    this.tickRate = tickRate;
    this.tickMs = 1000 / tickRate;
    this.tick = 0;
    this.running = false;
  }

  start() {
    this.running = true;
    this.lastTime = process.hrtime.bigint();
    this.accumulator = 0n;
    this.loop();
  }

  loop() {
    if (!this.running) return;

    const now = process.hrtime.bigint();
    const deltaNs = now - this.lastTime;
    this.lastTime = now;
    this.accumulator += deltaNs;

    const tickNs = BigInt(Math.round(this.tickMs * 1_000_000));
    let ticksProcessed = 0;

    while (this.accumulator >= tickNs && ticksProcessed < 5) {
      this.update(this.tickMs);
      this.tick++;
      this.accumulator -= tickNs;
      ticksProcessed++;
    }

    // Prevent spiral of death
    if (ticksProcessed === 5) {
      this.accumulator = 0n;
      console.warn('Tick catchup limit reached');
    }

    const sleepMs = Math.max(1, this.tickMs - Number(this.accumulator) / 1_000_000);
    setTimeout(() => this.loop(), sleepMs);
  }

  update(dt) {
    this.processInputs();
    this.updatePhysics(dt);
    this.updateEntities(dt);
    this.checkGameState();
    this.broadcastState();
  }
}
```

## Tick Rate Guide

| Game Type | Rate | Budget | Rationale |
|-----------|------|--------|-----------|
| FPS | 60-128 Hz | 8-16ms | Hit precision |
| MOBA | 30-60 Hz | 16-33ms | Balance |
| BR | 20-30 Hz | 33-50ms | Scale |
| MMO | 10-20 Hz | 50-100ms | Massive |

## Performance Monitoring

```javascript
class TickMetrics {
  constructor(size = 100) {
    this.samples = [];
    this.size = size;
  }

  record(ms) {
    this.samples.push(ms);
    if (this.samples.length > this.size) this.samples.shift();
  }

  stats() {
    const sorted = [...this.samples].sort((a, b) => a - b);
    return {
      avg: this.samples.reduce((a, b) => a + b, 0) / this.samples.length,
      p50: sorted[Math.floor(sorted.length * 0.5)],
      p99: sorted[Math.floor(sorted.length * 0.99)]
    };
  }
}
```

## Troubleshooting

### Common Failure Modes

| Error | Root Cause | Solution |
|-------|------------|----------|
| Tick spikes | GC pauses | Object pooling |
| Drift | Float precision | Fixed-point math |
| Explosion | Large dt | Cap dt value |
| Stuttering | Variable tick | Fixed timestep |

### Debug Checklist

```javascript
const stats = metrics.stats();
console.log(`Avg: ${stats.avg.toFixed(2)}ms`);
console.log(`P99: ${stats.p99.toFixed(2)}ms`);
console.log(`Budget: ${(stats.avg / tickBudget * 100).toFixed(1)}%`);
```

## Unit Test Template

```javascript
describe('GameLoop', () => {
  test('maintains tick rate', async () => {
    const loop = new GameLoop(60);
    const ticks = [];

    loop.update = () => ticks.push(Date.now());
    loop.start();

    await new Promise(r => setTimeout(r, 100));
    loop.running = false;

    expect(ticks.length).toBeGreaterThan(4);
  });
});
```

## Resources

- `assets/` - Loop templates
- `references/` - Optimization guides
