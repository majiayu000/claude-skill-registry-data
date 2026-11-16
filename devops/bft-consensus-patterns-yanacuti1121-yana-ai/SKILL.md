---
name: bft-consensus-patterns
description: Implement Byzantine Fault Tolerant voting for critical agent decisions. 3-of-N quorum for infrastructure writes, reputation-weighted voting, dual-verification pipelines, and automatic privilege demotion.
origin: PBFT (Castro & Liskov 1999), Raft (Ongaro & Ousterhout 2014), YAMTAM rule 54
license: Apache-2.0
version: 1.0.0
compatibility: claude-sonnet-4-6, claude-opus-4-7
---

# Byzantine Fault Tolerant Consensus

A swarm of 87 agents can tolerate up to 28 simultaneous compromised agents (f = ⌊(N-1)/3⌋) if decisions require 2f+1 votes.

## When to Use

- Critical operations that no single agent should decide unilaterally (rule changes, deploys, key rotation)
- Detecting when a minority of agents have been compromised or are producing incorrect output
- Dual-verification of important task results (two agents must agree before result is accepted)
- Enforcing quorum requirements before high-privilege Swarm Bus commands

## Do NOT use for

- Routine read-only operations (overhead not worth it for non-critical tasks)
- Single-agent systems or development environments

## BFT Voting via SwarmRouter

```js
import { SwarmRouter } from 'core/bus/swarm-router.js';

const router = new SwarmRouter();

// Register voters
['auditor-1', 'auditor-2', 'auditor-3', 'orch-1', 'orch-2'].forEach(id =>
  router.register(id, { role: 'auditor', trustScore: 90 })
);

// Propose a critical change
async function proposeChange(proposerId, change) {
  const QUORUM = 3;
  const votes = await Promise.allSettled(
    [...router.agents.keys()]
      .filter(id => id !== proposerId)
      .slice(0, 5)
      .map(id => router.route({
        from: proposerId, to: id,
        command: 'VOTE_REQUEST',
        payload: { change, fingerprint: router._fingerprint(change) }
      }))
  );

  const yesVotes = votes.filter(v => v.status === 'fulfilled' && v.value.delivered).length;
  if (yesVotes < QUORUM) throw new Error(`CONSENSUS_FAIL: ${yesVotes}/${QUORUM} votes`);
  return { approved: true, votes: yesVotes };
}
```

## Dual-Verification Pipeline (Lớp 79)

```js
// Run same task on two independent agents, compare results
async function dualVerify(task, agentA, agentB) {
  const [resultA, resultB] = await Promise.all([
    runAgent(agentA, task),
    runAgent(agentB, task),
  ]);

  const hashA = sha256(JSON.stringify(resultA));
  const hashB = sha256(JSON.stringify(resultB));

  if (hashA !== hashB) {
    // Results diverged — trigger investigation
    router.penalize(agentA, 10, 'DUAL_VERIFY_DIVERGENCE');
    router.penalize(agentB, 10, 'DUAL_VERIFY_DIVERGENCE');
    throw new Error('DUAL_VERIFY_FAIL: agent outputs diverged');
  }
  return resultA;
}
```

## Reputation-Weighted Voting

```js
function weightedQuorum(voters, minTrustScore = 60) {
  const eligible = voters.filter(a => a.trustScore >= minTrustScore && !a.quarantined);
  const totalWeight = eligible.reduce((sum, a) => sum + a.trustScore, 0);
  const threshold = totalWeight * 0.67;  // 67% weighted majority

  return { eligible: eligible.length, threshold, totalWeight };
}
```

## Automated Privilege Demotion (Lớp 80)

```js
// When task transitions to PENDING_APPROVAL state:
function demoteToMinPrivilege(agentId) {
  const agent = router.agents.get(agentId);
  // Restrict allowed commands to read-only subset
  agent.allowedCommands = new Set(['git status', 'ls', 'cat']);
  agent.role = 'observer';  // no write access
  router._log('PRIVILEGE_DEMOTE', agentId, { reason: 'PENDING_APPROVAL' });
}
```

## Agent Heartbeat Interrogation (Lớp 72)

```js
// Periodic challenge: agents must respond with correct HMAC
setInterval(() => {
  for (const [id, agent] of router.agents) {
    const challenge = randomBytes(16).toString('hex');
    const expectedResponse = hmac256(challenge, agent.sharedSecret);

    sendChallenge(id, challenge).then(response => {
      if (response !== expectedResponse) {
        router.quarantine(id, 'HEARTBEAT_FAIL');
      }
    }).catch(() => {
      router.quarantine(id, 'HEARTBEAT_TIMEOUT');
    });
  }
}, 30000);
```

## Anti-Fake-Pass Checklist

- [ ] QUORUM value ≥ 3 — never use `QUORUM = 1` even temporarily
- [ ] Quarantined agents excluded from voter pool
- [ ] Stale agents (heartbeat > TTL) excluded from voter pool
- [ ] Dual-verify divergence investigated — not silently retried
- [ ] Vote results logged to Merkle audit chain with fingerprints
