---
name: midnight-developer
description: This skill should be used when Ethereum developers are building smart contracts on pod network. It explains pod's coordination-free, blockless execution model, teaches order-independent programming with CRDTs, identifies Ethereum patterns that break on pod, and shows when to use external sequencing for order-dependent applications.
---

# pod network Solidity Development

Guide Ethereum developers through pod network's coordination-free execution model and order-independent programming patterns.

## Critical: The Fundamental Paradigm Shift

**pod network has NO BLOCKS and NO GLOBAL ORDERING.**

This is not "Ethereum with faster blocks" - this is a **completely different execution model**:

| Ethereum                              | pod network                           |
| ------------------------------------- | ------------------------------------- |
| Global blockchain with ordered blocks | ❌ NO BLOCKS                          |
| All transactions globally ordered     | ❌ NO GLOBAL ORDERING                 |
| Single consensus state                | Each validator has local state        |
| Sequential execution                  | Parallel, order-independent execution |
| Block confirmations                   | Attestation-based finality (>2/3)     |

**Implication**: Smart contracts MUST be designed for **order-independent execution**, OR use external sequencing.

---

## When to Use This Skill

Trigger this skill when developers:

**Building on pod network:**

- "How do I deploy a contract on pod?"
- "I'm building an ERC20 token on pod network"
- "What's different about pod network for Solidity devs?"

**Migrating from Ethereum:**

- "Can I port my Ethereum contract to pod?"
- "Why doesn't my contract work on pod network?"
- "What breaks when moving from Ethereum to pod?"

**Encountering pod-specific concepts:**

- Questions about FastTypes (SharedCounter, Balance, OwnedCounter)
- Questions about `block.number` or `block.timestamp` on pod
- Questions about finality, attestations, or Past Perfection Time
- Questions about order-dependent logic

**Design decisions:**

- "Does pod network support order books?"
- "How do I handle race conditions on pod?"
- "When do I need external sequencing?"

---

## What Breaks from Ethereum

**80% of Ethereum contracts break on pod network without modification.**

### Block Fields (All Broken)

- ❌ `block.number` - Always **0** (no blocks exist)
- ❌ `block.timestamp` - **Validator-local**, not consensus
- ❌ `block.coinbase`, `block.difficulty`, `block.basefee` - Always **0**
- ❌ Block confirmations - No blocks = use attestations instead

### Order-Dependent Logic (Breaks)

- ❌ Traditional ERC20 `transfer()` - Race conditions on balance checks
- ❌ First-come-first-served (FCFS) - Different validators see different order
- ❌ DEX order books - Price-time priority requires ordering
- ❌ Increment-then-check patterns - Concurrent access breaks checks
- ❌ Non-commutative operations - `f(g(x)) ≠ g(f(x))` produces divergence

### What Works

- ✅ Pure functions
- ✅ View functions
- ✅ Event emissions
- ✅ Simple mappings (`someValue[key] = value`)
- ✅ FastTypes (SharedCounter, Balance, Owned Counter, sets)

**For detailed migration checklist**, load `references/ethereum-breaking-changes.md`.

---

## Core Development Workflow

### Step 1: Understand Coordination-Free Requirements

**For deep understanding**, load `references/coordination-free-primer.md`.

**Quick Summary**:

- Operations must be **commutative**: `f(g(state)) = g(f(state))`
- Or **idempotent**: `f(f(state)) = f(state)`
- Or **monotonic**: Only increases (or only decreases in isolated contexts)

### Step 2: Use FastTypes from pod SDK

**Always prefer FastTypes over custom implementations.**

Install pod SDK:

```bash
forge install podnetwork/pod-sdk
```

**For complete FastTypes API reference**, load `references/fasttypes-guide.md`.

**Quick Reference**:

```solidity
import { SharedCounter } from "pod-sdk/FastTypes.sol";
import { Balance } from "pod-sdk/FastTypes.sol";
import { OwnedCounter } from "pod-sdk/FastTypes.sol";
import { Uint256Set, AddressSet } from "pod-sdk/FastTypes.sol";

// SharedCounter: Monotonic increment-only counter
SharedCounter counter;
counter.increment();
uint256 value = counter.value();

// Balance: Token balance with safe spend/credit
Balance balance;
balance.credit(amount);    // Anyone can credit
balance.spend(amount);      // Only owner can spend (uses nonce)

// OwnedCounter: Per-address counters
OwnedCounter scores;
scores.increment(owner, key);
scores.decrement(owner, key);  // Only for own keys

// Sets: Add-only (no removal)
AddressSet voters;
voters.add(address);
bool exists = voters.contains(address);
```

**Reference templates** (available via pod-templating MCP):

- `token-simple` - ERC20-like token with Balance FastType
- `nft-simple` - ERC721-like NFT with SharedCounter
- `voting-simple` - Voting system with AddressSet and time utilities
- `auction` - Auction contract with Balance and time-based bidding
- `basic-contract` - Minimal starter template

**To scaffold contracts**, use the `pod-scaffold-contract` skill, which orchestrates the pod-templating MCP server.

### Step 3: Handle Time Correctly

**For detailed time handling**, load `references/time-based-logic.md`.

**Quick Summary**:

- `block.timestamp` is **validator-local** (each validator uses own clock)
- Use pod SDK time utilities for consensus

```solidity
import { requireTimeAfter, requireTimeBefore } from "pod-sdk/Time.sol";

function startEvent() public {
    requireTimeAfter(eventStart);  // Requires >2/3 validators agree
    // ... event logic
}

function participate() public {
    requireTimeBefore(eventEnd);  // Requires >2/3 validators agree
    // ... participation logic
}
```

**Add time buffers** (5-10 seconds) for edge cases:

```solidity
uint256 deadline = now + 1 hours + 5 seconds;  // 5s buffer
```

### Step 4: Deploy to pod network

**Deploy with Foundry**:

```bash
forge create MyContract \
    --rpc-url wss://rpc.testnet-02.midnight.network/ \
    --private-key $PRIVATE_KEY \
    --legacy  # pod uses legacy tx format
```

**Deploy with Hardhat** (configure in hardhat.config.js):

```javascript
networks: {
    pod: {
        url: "wss://rpc.testnet-02.midnight.network/",
        accounts: [process.env.PRIVATE_KEY],
        // Use legacy transactions
        hardfork: "london"
    }
}
```

### Step 5: Verify Finality

**Check transaction finality** via attestations (not block confirmations):

```bash
node scripts/check-attestations.js <txHash>
```

**Or via JSON-RPC**:

```javascript
const receipt = await provider.getTransactionReceipt(txHash);
const attestations = receipt.pod_metadata.attestations;
const committeeSize = receipt.pod_metadata.committee_size;
const byzantineThreshold = Math.ceil((committeeSize * 2) / 3);

if (attestations >= byzantineThreshold) {
  // Finalized! (~150ms on pod network)
}
```

**Use midnight-network MCP tools**:

- `verify_finality` - Check if transaction is finalized
- `network_health_dashboard` - Get network status
- `analyze_past_perfect_time` - Check finality lag

---

## When External Sequencing is Required

**If application inherently requires strict transaction ordering**, use external sequencing.

**Examples**:

- DEX order books (price-time priority)
- Auctions with MEV sensitivity
- FIFO job queues
- Priority-based allocation

**For implementation patterns**, load `references/external-sequencing-patterns.md`.

**Architecture**:

```
Users → Sequencer (off-protocol) → Ordered Batch → pod network
```

**Key Insight**: Sequencer provides ordering, pod network provides fast finality for the batch.

---

## Common Patterns and Solutions

### Pattern: Token Contract

```solidity
import { Balance } from "pod-sdk/FastTypes.sol";

mapping(address => Balance) public balances;

function transfer(address to, uint256 amount) public {
    balances[msg.sender].spend(amount);  // Safe: uses nonce
    balances[to].credit(amount);          // Safe: commutative
}
```

**Scaffold this pattern**: Use `pod-scaffold-contract` skill with `token-simple` template.

### Pattern: NFT Minting

```solidity
import { SharedCounter } from "pod-sdk/FastTypes.sol";

SharedCounter tokenIds;

function mint(address to) public {
    uint256 tokenId = tokenIds.value();
    tokenIds.increment();  // Safe: monotonic, commutative
    _mint(to, tokenId);
}
```

**Scaffold this pattern**: Use `pod-scaffold-contract` skill with `nft-simple` template.

### Pattern: Voting

```solidity
import { AddressSet, SharedCounter } from "pod-sdk/FastTypes.sol";

AddressSet voters;
SharedCounter yesVotes;
mapping(address => bool) hasVoted;

function vote(bool support) public {
    require(!hasVoted[msg.sender], "Already voted");  // Idempotent
    hasVoted[msg.sender] = true;
    voters.add(msg.sender);  // Safe: add-only
    if (support) yesVotes.increment();  // Safe: monotonic
}
```

**Scaffold this pattern**: Use `pod-scaffold-contract` skill with `voting-simple` template.

### Pattern: Time-Based Actions

```solidity
import { requireTimeAfter, requireTimeBefore } from "pod-sdk/Time.sol";

function claimReward() public {
    requireTimeAfter(claimStart);
    requireTimeBefore(claimEnd);
    // ... claim logic
}
```

**Scaffold this pattern**: Use `pod-scaffold-contract` skill with `auction` template.

---

## Reference Documents (Load as Needed)

### Progressive Loading Strategy

Load these references when developers need deeper understanding:

1. **coordination-free-primer.md** - **Most important**. Load when:
   - Developer new to pod network
   - Questions about "why doesn't this work?"
   - Need to understand the paradigm shift

2. **fasttypes-guide.md** - Load when:
   - Implementing contracts with FastTypes
   - Questions about specific FastType APIs
   - Need complete reference for SharedCounter, Balance, etc.

3. **ethereum-breaking-changes.md** - Load when:
   - Migrating existing Ethereum contract
   - Debugging "works on Ethereum, breaks on pod"
   - Need comprehensive migration checklist

4. **external-sequencing-patterns.md** - Load when:
   - Application requires strict ordering
   - Building DEX, auction, or FIFO queue
   - Questions about "when do I need a sequencer?"

5. **time-based-logic.md** - Load when:
   - Implementing deadlines, auctions, voting periods
   - Questions about `block.timestamp` behavior
   - Need detailed time handling patterns

---

## Scripts Reference

### check-attestations.js

Verify transaction finality via attestation count.

**Usage**:

```bash
node scripts/check-attestations.js <txHash> [rpcUrl]
```

**When to use**:

- After deploying contract (check deployment finalized)
- Monitoring critical transactions
- Debugging finality issues

---

## Development Checklist

**Before deploying to pod network**:

- [ ] Contract uses FastTypes (or external sequencing if order-dependent)
- [ ] No `block.number` usage
- [ ] No `block.timestamp` for consensus (use time utilities)
- [ ] No `block.coinbase`, `block.difficulty`, `block.basefee`
- [ ] No order-dependent logic (or external sequencing added)
- [ ] No race conditions on shared state
- [ ] No non-commutative operations
- [ ] Time-based logic uses `requireTimeAfter/Before`
- [ ] Tested commutativity (`test-commutativity.js`)
- [ ] Deploy command uses `--legacy` flag
- [ ] Finality verified via attestations (not block confirmations)

---

## pod network Resources

**Official Documentation**:

- pod Docs: https://docs.v1.pod.network/
- Solidity SDK: https://docs.v1.pod.network/solidity-sdk
- Architecture: https://docs.v1.pod.network/architecture/coordination-free
- Examples: https://docs.v1.pod.network/examples/

**Dev Network**:

- RPC Endpoint: wss://rpc.testnet-02.midnight.network/
- Chain ID: 0x50d (1293 decimal)
- Explorer: https://explorer.v1.pod.network/

**SDKs**:

- Solidity: `forge install podnetwork/pod-sdk`
- Rust: `pod-sdk` crate

**MCP Tools** (Available via midnight-network MCP server):

- `verify_finality` - Check transaction finality
- `network_health_dashboard` - Network status
- `analyze_address` - Address analysis
- `pod_getCommittee` - Validator committee info
- `pod_pastPerfectTime` - Last finalized timestamp

---

## Bottom Line

**pod network is fundamentally different from Ethereum**:

- NO BLOCKS, NO GLOBAL ORDER
- Requires order-independent design
- FastTypes guarantee correctness
- ~150ms finality via attestations

**When designing contracts**:

1. Start with FastTypes
2. Test commutativity
3. Use external sequencing only if truly needed

**When migrating from Ethereum**:

1. Load `ethereum-breaking-changes.md`
2. Replace block-dependent logic
3. Replace balances with FastTypes
4. Test on pod dev network

**This is a paradigm shift, not an incremental change.**
