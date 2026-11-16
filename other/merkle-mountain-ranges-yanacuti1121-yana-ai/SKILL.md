---
name: merkle-mountain-ranges
description: Implement append-only cryptographic audit logs using Merkle Mountain Ranges (MMR). Any tampering with historical entries causes immediate root hash drift. Integrates with YAMTAM secure-logger.js for agent action immutability.
origin: MMR spec (Peter Todd), merkletreejs (MIT), YAMTAM Engine secure-logger design
license: Apache-2.0
version: 1.0.0
compatibility: claude-sonnet-4-6, claude-opus-4-7
---

# Merkle Mountain Ranges (Append-Only Audit Log)

Unlike flat log files, a Merkle Mountain Range lets you prove that any historical entry hasn't been modified — without scanning the entire log. Tampering changes the root hash instantly.

## When to Use

- Building tamper-evident audit logs for agent actions (who did what, when)
- Proving to an auditor that a log has not been modified since a given timestamp
- Implementing WORM (Write Once, Read Many) storage semantics in software
- Providing cryptographic chain of custody across 87 agent sessions

## Do NOT use for

- Real-time streaming logs where sub-millisecond latency is required (use structured logging + async flush)
- Secret data storage (MMR proves integrity, not confidentiality — encrypt first)

## How MMR Differs from a Simple Merkle Tree

```
Simple Merkle Tree — fixed, must rebuild entire tree to add leaf
MMR — grow by appending peaks, O(log n) update per new leaf

MMR structure for 7 leaves:
   Peak3
   /   \
 Pk2   Pk1  L7
 / \   / \
L1  L2 L3  L4  L5  L6
```

Adding leaf 8: merge L7+L8 → new peak, merge with Pk1 → new Pk2, etc.

## YAMTAM Usage

```js
import { SecureAuditLogger } from 'core/memory/secure-logger.js';

const logger = new SecureAuditLogger('releases/logs/audit.jsonl');

// Log an action — appends leaf to MMR, writes root hash
const { leaf, root } = logger.logAction('agent-42', 'bash:git-status', 'PASS');
console.log(`Leaf: ${leaf.slice(0,16)}… Root: ${root.slice(0,16)}…`);

// Verify entire log integrity
const result = logger.verify();
// throws SecureLogTamperError if any entry was modified
console.log(`Verified ${result.entryCount} entries. Root: ${result.root}`);
```

## Manual MMR (Pure Node.js)

```js
import { createHash } from 'crypto';

function sha256(data) {
  return createHash('sha256').update(data).digest('hex');
}

function merkleRoot(leaves) {
  if (leaves.length === 0) return sha256('EMPTY');
  let layer = [...leaves];
  while (layer.length > 1) {
    const next = [];
    for (let i = 0; i < layer.length; i += 2) {
      next.push(sha256(layer[i] + (layer[i+1] ?? layer[i])));
    }
    layer = next;
  }
  return layer[0];
}

// Add entries incrementally
const leaves = [];
function append(entry) {
  leaves.push(sha256(JSON.stringify(entry)));
  return merkleRoot(leaves);  // new root after append
}
```

## Tamper Detection

```js
// Simulate tampering: modify line 3 of log file
// → logger.verify() will throw:
// SecureLogTamperError: ROOT HASH DRIFT — stored: a3f8... computed: 7c21...

try {
  logger.verify();
} catch (e) {
  if (e.name === 'SecureLogTamperError') {
    // Freeze swarm, alert SIEM, begin forensic recovery
    swarmRouter.quarantine('all', 'LOG_TAMPER_DETECTED');
  }
}
```

## HMAC-Signed Entries

Each log entry includes an HMAC-SHA256 signature keyed by `YAMTAM_LOG_SECRET`:
```json
{
  "ts": "2026-05-23T10:00:00.000Z",
  "agentId": "agent-42",
  "command": "bash:ls",
  "status": "PASS",
  "leaf": "3f8a2b91...",
  "root": "7c21d4e9...",
  "hmac": "a1b2c3d4..."
}
```

## Anti-Fake-Pass Checklist

- [ ] `logger.verify()` called after every 100 entries minimum
- [ ] Root hash stored in a separate file (`audit.jsonl.root`) — not in the log itself
- [ ] HMAC secret is NOT the default (`yamtam-default-secret`) in production
- [ ] Tamper test: manually edit one log line → `verify()` should throw
- [ ] Log file opened with `flag: 'a'` (append) — never truncate or seek
