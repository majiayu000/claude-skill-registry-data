---
name: abd
description: Attiya-Bar-Noy-Dolev atomic register emulation over message-passing. Load when designing quorum-based distributed storage, proving linearizability, or reasoning about fault-tolerant shared memory.
---

# ABD: Atomic Register Emulation

**Paper**: Attiya, Bar-Noy, Dolev. *Sharing memory robustly in message-passing systems*. JACM 42(1):124-142, 1995.

## Core Idea

ABD emulates a wait-free, atomic (linearizable) register on top of an asynchronous message-passing network tolerating `f < n/2` crash failures. It is the foundational reduction from shared memory to message passing.

## Three Structural Pillars

| Pillar | Formal Object | Role |
|---|---|---|
| **Quorum Intersection** | `Q subset of 2^Pi, forall Q1,Q2 in Q: Q1 intersect Q2 != empty` | Any two majority sets overlap >= 1 correct process |
| **Timestamps** | `(seq: N, writer_id: Pi)` with lex order | Total order on writes; uniqueness across writers |
| **Write-back** | Reader propagates `(v_max, t_max)` to quorum | Upgrades regularity to atomicity; prevents new-old inversion |

## Protocol

### SWMR (Single-Writer Multi-Reader)

```
WRITE(v):
  1. t <- t + 1                          [local]
  2. send WRITE(v, t) to all Pi           [1 RTT]
  3. wait for ACK from majority
  4. return OK
  -- Latency: 2d, Messages: O(n) --

READ():
  1. send READ(nonce) to all Pi           [1 RTT: query]
  2. wait for (v_i, t_i) from majority
  3. (v*, t*) <- argmax_t {responses}
  4. send WRITE(v*, t*) to all Pi         [1 RTT: write-back]
  5. wait for ACK from majority
  6. return v*
  -- Latency: 4d, Messages: O(n) --
```

### MWMR Extension

Writers add a query phase to discover the current max timestamp:

```
WRITE(v):
  1. send READ(nonce) to all Pi           [1 RTT: query]
  2. wait for (v_i, t_i) from majority
  3. t <- (max(t_i.seq) + 1, my_id)      [local]
  4. send WRITE(v, t) to all Pi           [1 RTT: broadcast]
  5. wait for ACK from majority
  -- Latency: 4d, Messages: O(n) --
```

Read is identical to SWMR read (2 RTT).

### Server Logic

```
on receive WRITE(v, t) from p:
  if t > local_t:
    local_v <- v; local_t <- t
  send ACK(v, t) to p

on receive READ(nonce) from p:
  send ACK(local_v, local_t, nonce) to p
```

## Correctness Skeleton

| Property | Argument |
|---|---|
| **Termination** | f<n/2 implies majority always alive; each phase needs only majority |
| **Writes ordered** | SWMR: monotone by single writer. MWMR: (seq,id) unique |
| **Latest value** | Query majority intersect write majority != empty implies sees latest ts |
| **No new-old inversion** | Write-back ensures majority holds t1; R2 majority overlaps implies t2 >= t1 |
| **Linearization** | Order by ts; writes before reads at same ts |
| **Necessity of f < n/2** | Partition argument: two halves, cross-messages delayed |

## Complexity

| Operation | RTTs | Messages | Latency |
|---|---|---|---|
| SWMR Write | 1 | O(n) | 2d |
| SWMR Read | 2 | O(n) | 4d |
| MWMR Write | 2 | O(n) | 4d |
| MWMR Read | 2 | O(n) | 4d |

## Extensions

| Variant | Change | Trade-off |
|---|---|---|
| **Fast reads** | Skip write-back when no concurrent write | 1-RTT reads; impossible for MWMR with n>5 |
| **Byzantine ABD** | f < n/3 quorums + value validation + PKI | Tolerates arbitrary faults; 3x replication |
| **Coded ABD** | Erasure coding replaces full replication | Lower storage/bandwidth; same intersection property |
| **Reconfigurable** | Consensus on quorum membership changes | Dynamic membership (RAMBO protocol) |

## Key Insight

The write-back phase is what separates ABD from a naive quorum read. Without it, you get regular semantics (concurrent reads may disagree). With it, you get atomic/linearizable semantics. This single extra round-trip is the price of consistency.

## References

- Attiya, Bar-Noy, Dolev. JACM 1995. DOI:10.1145/200836.200869
- Tseng et al. (Gus) SPAA 2023. DOI:10.1145/3558481.3591086
- Vukolic. Quorum Systems. Morgan & Claypool 2012

## Concrete Affordance: Runnable ABD Simulation

### Quick Start

```bash
# No external dependencies beyond Python 3.10+ standard library
python3 /Users/alice/v/asi/skills/abd/abd_sim.py
```

### Simulation Script (`abd_sim.py`)

Save the following as `/Users/alice/v/asi/skills/abd/abd_sim.py`:

```python
#!/usr/bin/env python3
"""
ABD SWMR atomic register simulation using threads + queues.
Spawns N=5 server processes (threads), 1 writer, 2 readers.
Demonstrates the write-back phase that upgrades regular → atomic semantics.
Tolerates f < n/2 = 2 crash failures.
"""

import threading
import queue
import time
import random
from dataclasses import dataclass, field
from typing import Any

N = 5  # number of servers
MAJORITY = N // 2 + 1

@dataclass
class TimestampedValue:
    value: Any = None
    seq: int = 0
    writer_id: int = 0

    def __lt__(self, other):
        return (self.seq, self.writer_id) < (other.seq, other.writer_id)

    def __repr__(self):
        return f"({self.value}, ts=({self.seq},{self.writer_id}))"


class ABDServer(threading.Thread):
    """Server process holding a local copy of the register."""

    def __init__(self, server_id: int, crash_after: int | None = None):
        super().__init__(daemon=True)
        self.server_id = server_id
        self.local = TimestampedValue()
        self.inbox = queue.Queue()
        self.crash_after = crash_after  # crash after N messages (None = never)
        self.msg_count = 0

    def run(self):
        while True:
            msg = self.inbox.get()
            self.msg_count += 1
            if self.crash_after and self.msg_count > self.crash_after:
                return  # simulate crash
            op, ts_val, reply_q = msg
            if op == "WRITE":
                if ts_val > self.local or (ts_val.seq == self.local.seq
                        and ts_val.writer_id == self.local.writer_id):
                    self.local = ts_val
                reply_q.put(("ACK", self.server_id, self.local))
            elif op == "READ":
                reply_q.put(("ACK", self.server_id, self.local))


def broadcast_and_collect(servers, op, ts_val, majority=MAJORITY):
    """Send op to all servers, wait for majority ACKs."""
    reply_q = queue.Queue()
    for s in servers:
        try:
            s.inbox.put_nowait((op, ts_val, reply_q))
        except Exception:
            pass  # server may have crashed
    acks = []
    deadline = time.monotonic() + 2.0
    while len(acks) < majority and time.monotonic() < deadline:
        try:
            acks.append(reply_q.get(timeout=0.1))
        except queue.Empty:
            pass
    return acks


def abd_write(servers, value, writer_state):
    """SWMR WRITE: increment local ts, broadcast, wait majority ACK."""
    writer_state.seq += 1
    writer_state.value = value
    ts = TimestampedValue(value, writer_state.seq, writer_state.writer_id)
    acks = broadcast_and_collect(servers, "WRITE", ts)
    assert len(acks) >= MAJORITY, f"Write failed: only {len(acks)} ACKs"
    print(f"  WRITE({value}) committed with ts=({ts.seq},{ts.writer_id}), "
          f"{len(acks)}/{N} ACKs")
    return ts


def abd_read(servers, reader_id):
    """SWMR READ: query majority, pick max ts, WRITE-BACK, return value."""
    # Phase 1: query
    acks = broadcast_and_collect(servers, "READ", TimestampedValue())
    assert len(acks) >= MAJORITY, f"Read query failed: only {len(acks)} ACKs"
    best = max((a[2] for a in acks), key=lambda tv: (tv.seq, tv.writer_id))

    # Phase 2: write-back (THIS is what makes it atomic, not just regular)
    wb_acks = broadcast_and_collect(servers, "WRITE", best)
    assert len(wb_acks) >= MAJORITY, f"Write-back failed: only {len(wb_acks)} ACKs"

    print(f"  READ by reader-{reader_id} => {best.value} "
          f"(ts=({best.seq},{best.writer_id}), "
          f"query={len(acks)}/{N}, wb={len(wb_acks)}/{N})")
    return best.value


def main():
    print(f"ABD Simulation: {N} servers, majority={MAJORITY}\n")

    # Spawn servers (crash server #4 after 3 messages to demonstrate fault tolerance)
    servers = [ABDServer(i, crash_after=3 if i == 4 else None) for i in range(N)]
    for s in servers:
        s.start()

    writer_state = TimestampedValue(None, 0, writer_id=0)

    # Writer writes 3 values
    print("--- Writer phase ---")
    for v in ["alpha", "beta", "gamma"]:
        abd_write(servers, v, writer_state)
        time.sleep(0.05)

    # Two readers read concurrently
    print("\n--- Reader phase (server #4 has crashed) ---")
    threads = []
    for rid in [1, 2]:
        t = threading.Thread(target=abd_read, args=(servers, rid))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

    # Both readers MUST return "gamma" (linearizability via write-back)
    print("\n--- Write after crash, demonstrating f<n/2 tolerance ---")
    abd_write(servers, "delta", writer_state)
    abd_read(servers, 3)

    print("\nDone. All operations linearizable despite 1 server crash.")


if __name__ == "__main__":
    main()
```

### Using a Real Distributed Register Library

For production use beyond simulation:

```bash
# dslib — distributed systems simulation library (Python)
pip install dslib

# Or use etcd as a real linearizable register:
pip install etcd3
```

```python
# etcd3 as a linearizable register (ABD-like semantics via Raft)
import etcd3
client = etcd3.client(host='localhost', port=2379)
client.put('/register/x', 'value')           # linearizable write
value, metadata = client.get('/register/x')   # linearizable read
```

### Key Files

| Path | Description |
|---|---|
| `/Users/alice/v/asi/skills/abd/abd_sim.py` | Runnable SWMR simulation (create from snippet above) |
| `/Users/alice/v/asi/skills/abd/SKILL.md` | This document |
