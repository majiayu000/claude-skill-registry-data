---
name: state-sync
description: Game state synchronization, snapshot systems, and conflict resolution for consistent multiplayer experience
sasmp_version: "1.3.0"
version: "2.0.0"
bonded_agent: 04-state-sync-expert
bond_type: PRIMARY_BOND

# Parameters
parameters:
  required:
    - sync_model
    - update_rate_hz
  optional:
    - buffer_size
    - interpolation_delay_ms
  validation:
    sync_model:
      type: string
      enum: [snapshot, delta, lockstep, interest_management]
    update_rate_hz:
      type: integer
      min: 1
      max: 128
    buffer_size:
      type: integer
      min: 2
      max: 10
      default: 3
    interpolation_delay_ms:
      type: integer
      min: 50
      max: 200
      default: 100

# Retry Configuration
retry_config:
  max_attempts: 3
  backoff: exponential
  initial_delay_ms: 50

# Observability
observability:
  logging:
    level: debug
    fields: [entity_count, delta_size, checksum]
  metrics:
    - name: sync_delta_bytes
      type: histogram
    - name: sync_entities_updated
      type: counter
    - name: sync_desync_detected
      type: counter
---

# State Synchronization

Ensure **consistent game state** across all connected players.

## Snapshot Interpolation

```javascript
class SnapshotBuffer {
  constructor(size = 3, delay = 100) {
    this.buffer = [];
    this.size = size;
    this.delay = delay;
  }

  add(snapshot) {
    this.buffer.push({
      time: snapshot.serverTime,
      entities: new Map(snapshot.entities)
    });
    while (this.buffer.length > this.size) {
      this.buffer.shift();
    }
  }

  interpolate(renderTime) {
    const targetTime = renderTime - this.delay;
    const [before, after] = this.findBrackets(targetTime);

    if (!before || !after) return this.extrapolate();

    const t = (targetTime - before.time) / (after.time - before.time);
    return this.lerp(before, after, t);
  }

  lerp(before, after, t) {
    const result = new Map();
    for (const [id, a] of before.entities) {
      const b = after.entities.get(id);
      if (b) {
        result.set(id, {
          x: a.x + (b.x - a.x) * t,
          y: a.y + (b.y - a.y) * t,
          z: a.z + (b.z - a.z) * t
        });
      }
    }
    return result;
  }
}
```

## Delta Compression

```javascript
class DeltaCompressor {
  createDelta(baseline, current) {
    const delta = { created: [], updated: [], deleted: [] };

    for (const [id, entity] of current) {
      const prev = baseline.get(id);
      if (!prev) {
        delta.created.push({ id, ...entity });
      } else if (this.changed(prev, entity)) {
        delta.updated.push({ id, ...this.diff(prev, entity) });
      }
    }

    for (const [id] of baseline) {
      if (!current.has(id)) delta.deleted.push(id);
    }

    return delta;
  }

  changed(a, b) {
    return a.x !== b.x || a.y !== b.y || a.z !== b.z;
  }

  diff(prev, curr) {
    const d = {};
    if (prev.x !== curr.x) d.x = curr.x;
    if (prev.y !== curr.y) d.y = curr.y;
    if (prev.z !== curr.z) d.z = curr.z;
    return d;
  }
}
```

## Sync Model Comparison

| Model | Latency | Bandwidth | Best For |
|-------|---------|-----------|----------|
| Snapshot | Medium | High | Simple games |
| Delta | Medium | Low | Most games |
| Lockstep | High | Low | RTS, Fighting |
| Interest Mgmt | Low | Low | MMO |

## Troubleshooting

### Common Failure Modes

| Error | Root Cause | Solution |
|-------|------------|----------|
| Teleporting | Empty buffer | Increase buffer size |
| Desync | Non-determinism | Add checksums |
| Rubber-banding | Bad reconciliation | Fix prediction |
| Invisible entities | AoI bug | Check interest radius |

### Debug Checklist

```javascript
// Check buffer state
console.log(`Buffer: ${buffer.length}/${buffer.size}`);
console.log(`Time span: ${buffer.getTimeSpan()}ms`);

// Verify checksums
const cs1 = computeChecksum(clientState);
const cs2 = computeChecksum(serverState);
console.log(`Match: ${cs1 === cs2}`);
```

## Unit Test Template

```javascript
describe('DeltaCompressor', () => {
  test('detects changes', () => {
    const compressor = new DeltaCompressor();
    const baseline = new Map([['e1', { x: 0, y: 0 }]]);
    const current = new Map([['e1', { x: 1, y: 0 }]]);

    const delta = compressor.createDelta(baseline, current);
    expect(delta.updated).toHaveLength(1);
    expect(delta.updated[0].x).toBe(1);
  });
});
```

## Resources

- `assets/` - Sync templates
- `references/` - Best practices
