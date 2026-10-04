---
name: anvil-node
description: Run local Ethereum nodes with Anvil. Use when setting up local development environments, forking mainnet for testing, or running integration tests against a local node.
---

# Anvil Local Node

Anvil is Foundry's fast local Ethereum node for development and testing.

## When to Use

- Local development and testing
- Forking mainnet or other networks
- Integration testing with frontend applications
- Testing transaction flows before mainnet
- Simulating complex scenarios

## Quick Start

```bash
# Start local node with 10 pre-funded accounts
anvil

# Start with custom port
anvil --port 8545

# Start with specific accounts
anvil --accounts 5 --balance 1000
```

## Default Configuration

When started without flags:

| Setting | Value |
|---------|-------|
| Port | 8545 |
| Accounts | 10 |
| Balance | 10000 ETH each |
| Chain ID | 31337 |
| Block time | Instant (mines on each tx) |

## Pre-Funded Accounts

Default test accounts (deterministic):

```
Account #0: 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266
Private Key: 0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80

Account #1: 0x70997970C51812dc3A010C7d01b50e0d17dc79C8
Private Key: 0x59c6995e998f97a5a0044966f0945389dc9e86dae88c7a8412f4603b6b78690d

Account #2: 0x3C44CdDdB6a900fa2b585dd299e03d12FA4293BC
Private Key: 0x5de4111afa1a4b94908f83103eb1f1706367c2e68ca870fc3fb9a804cdab365a
```

## Forking

### Fork Mainnet

```bash
# Fork at latest block
anvil --fork-url https://eth-mainnet.g.alchemy.com/v2/$API_KEY

# Fork at specific block (reproducible)
anvil --fork-url $MAINNET_RPC --fork-block-number 18000000
```

### Fork Other Networks

```bash
# Arbitrum
anvil --fork-url https://arb1.arbitrum.io/rpc

# Optimism
anvil --fork-url https://mainnet.optimism.io

# Base
anvil --fork-url https://mainnet.base.org

# Polygon
anvil --fork-url https://polygon-rpc.com
```

## Configuration Options

### Account Settings

```bash
# Custom number of accounts
anvil --accounts 20

# Custom balance (in ETH)
anvil --balance 100000

# Use specific mnemonic
anvil --mnemonic "test test test test test test test test test test test junk"

# Derivation path
anvil --derivation-path "m/44'/60'/0'/0/"
```

### Network Settings

```bash
# Custom chain ID
anvil --chain-id 1337

# Custom port
anvil --port 8546

# Listen on all interfaces
anvil --host 0.0.0.0

# Custom gas limit
anvil --gas-limit 30000000

# Custom gas price
anvil --gas-price 1000000000
```

### Mining Settings

```bash
# Auto-mine (default - instant blocks)
anvil

# Interval mining (block every N seconds)
anvil --block-time 12

# No mining (manual only)
anvil --no-mining
```

### State Management

```bash
# Load state from file
anvil --load-state state.json

# Dump state to file on exit
anvil --dump-state state.json

# State snapshot directory
anvil --state ./anvil-state
```

## Forking Features

See [forking.md](forking.md) for detailed patterns.

### Impersonating Accounts

```bash
# Start with unlocked accounts
anvil --fork-url $RPC --unlocked 0xWhaleAddress
```

Or via RPC:

```bash
# Unlock account
cast rpc anvil_impersonateAccount 0xWhaleAddress

# Send as whale
cast send 0xRecipient --value 100ether \
    --from 0xWhaleAddress \
    --unlocked

# Stop impersonating
cast rpc anvil_stopImpersonatingAccount 0xWhaleAddress
```

### Time Manipulation

```bash
# Increase time
cast rpc evm_increaseTime 86400  # 1 day

# Set timestamp
cast rpc evm_setNextBlockTimestamp 1700000000

# Mine block with new timestamp
cast rpc evm_mine
```

### Block Manipulation

```bash
# Mine N blocks
cast rpc anvil_mine 10

# Set block gas limit
cast rpc evm_setBlockGasLimit 50000000
```

## RPC Methods

### Standard Ethereum RPC

All standard Ethereum JSON-RPC methods are supported.

### Anvil-Specific Methods

```bash
# Mine blocks
cast rpc anvil_mine [numBlocks]

# Set balance
cast rpc anvil_setBalance 0xAddress 0x8ac7230489e80000  # 10 ETH in hex

# Set code
cast rpc anvil_setCode 0xAddress 0x608060...

# Set storage
cast rpc anvil_setStorageAt 0xContract 0x0 0x1

# Impersonate
cast rpc anvil_impersonateAccount 0xAddress

# Snapshot
SNAPSHOT_ID=$(cast rpc evm_snapshot)

# Revert to snapshot
cast rpc evm_revert $SNAPSHOT_ID

# Set nonce
cast rpc anvil_setNonce 0xAddress 100

# Set chain ID
cast rpc anvil_setChainId 1
```

## Integration with Forge

### Fork Testing

```solidity
contract ForkTest is Test {
    function setUp() public {
        // Fork mainnet at specific block
        vm.createSelectFork("mainnet", 18000000);
    }

    function test_ForkState() public {
        // Tests run against forked state
        IERC20 usdc = IERC20(0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48);
        assertGt(usdc.totalSupply(), 0);
    }
}
```

### Running Against Anvil

```bash
# Terminal 1: Start Anvil
anvil --fork-url $MAINNET_RPC

# Terminal 2: Run tests
forge test --rpc-url http://localhost:8545
```

## Common Use Cases

### Frontend Development

```bash
# Start persistent forked node
anvil --fork-url $MAINNET_RPC --dump-state ./state.json

# Connect frontend to http://localhost:8545
# Chain ID: 31337
```

### Integration Testing

```bash
# Start Anvil in background
anvil --fork-url $MAINNET_RPC &

# Deploy contracts
forge script script/Deploy.s.sol --rpc-url http://localhost:8545 --broadcast

# Run integration tests
forge test --rpc-url http://localhost:8545

# Stop Anvil
pkill anvil
```

### Debugging Transactions

```bash
# Fork at block before problematic tx
anvil --fork-url $RPC --fork-block-number 17999999

# Replay transaction
cast send --rpc-url http://localhost:8545 ...

# Debug with traces
cast run $TX_HASH --rpc-url http://localhost:8545
```

## Best Practices

1. **Use specific fork blocks** for reproducible tests
2. **Save state** for faster restarts during development
3. **Use unlocked accounts** for impersonation testing
4. **Set appropriate block time** for time-sensitive tests
5. **Monitor memory** usage when forking large state

## Troubleshooting

### Connection Issues

```bash
# Check if Anvil is running
curl http://localhost:8545 -X POST -H "Content-Type: application/json" \
    --data '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}'
```

### Memory Issues

```bash
# Limit cache size
anvil --fork-url $RPC --fork-retry-backoff 1000

# Use specific block to limit state
anvil --fork-url $RPC --fork-block-number 18000000
```

### RPC Rate Limits

```bash
# Add retry backoff
anvil --fork-url $RPC --fork-retry-backoff 1000

# Use multiple RPC endpoints (via load balancer)
```
