---
name: forge-deployment
description: Deploy and verify smart contracts with Foundry. Use when deploying contracts, writing deployment scripts, verifying on block explorers, or managing multi-chain deployments.
---

# Forge Deployment

Deploy and verify smart contracts using Foundry's deployment tools.

## Source verification preflight

For existing contracts, first read [source verification](references/source-verification.md): inherited credentials, exact build identity, Blockscout PRO authentication, standard JSON fallback, and independent Sourcify/Blockscout completion checks. Check the consumer’s configured `BLOCKSCOUT_API_KEY` in the inherited environment before looking in `.env` or asking for a key. Verification alone requires no signing key or onchain broadcast.

## When to Use

- Deploying contracts to testnets or mainnet
- Writing deployment scripts in Solidity
- Verifying contracts on Etherscan/Sourcify
- Managing multi-chain deployments
- Setting up deterministic deployments (CREATE2)

## Quick Deploy with forge create

```bash
# Basic deployment
forge create src/MyContract.sol:MyContract \
    --rpc-url $RPC_URL \
    --private-key $PRIVATE_KEY \
    --broadcast

# With constructor arguments
forge create src/MyContract.sol:MyContract \
    --rpc-url $RPC_URL \
    --private-key $PRIVATE_KEY \
    --constructor-args "arg1" 123 0xAddress \
    --broadcast

# Deploy and verify
forge create src/MyContract.sol:MyContract \
    --rpc-url $RPC_URL \
    --private-key $PRIVATE_KEY \
    --verify \
    --etherscan-api-key $ETHERSCAN_API_KEY \
    --broadcast
```

## Deployment Scripts

See [scripts.md](scripts.md) for comprehensive script patterns.

### Basic Script

```solidity
// script/Deploy.s.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import {Script, console} from "forge-std/Script.sol";
import {MyContract} from "../src/MyContract.sol";

contract DeployScript is Script {
    function run() public {
        uint256 deployerPrivateKey = vm.envUint("PRIVATE_KEY");

        vm.startBroadcast(deployerPrivateKey);

        MyContract myContract = new MyContract();
        console.log("MyContract deployed to:", address(myContract));

        vm.stopBroadcast();
    }
}
```

### Running Scripts

```bash
# Dry run (simulation)
forge script script/Deploy.s.sol

# Broadcast to network
forge script script/Deploy.s.sol \
    --rpc-url $RPC_URL \
    --broadcast

# Broadcast and verify
forge script script/Deploy.s.sol \
    --rpc-url $RPC_URL \
    --broadcast \
    --verify \
    --etherscan-api-key $ETHERSCAN_API_KEY

# Resume failed broadcast
forge script script/Deploy.s.sol \
    --rpc-url $RPC_URL \
    --resume
```

## Environment Configuration

### foundry.toml

```toml
[rpc_endpoints]
mainnet = "${MAINNET_RPC_URL}"
sepolia = "${SEPOLIA_RPC_URL}"
arbitrum = "${ARBITRUM_RPC_URL}"
base = "${BASE_RPC_URL}"

[etherscan]
mainnet = { key = "${ETHERSCAN_API_KEY}" }
sepolia = { key = "${ETHERSCAN_API_KEY}" }
arbitrum = { key = "${ARBISCAN_API_KEY}" }
base = { key = "${BASESCAN_API_KEY}" }
```

### .env File

```bash
PRIVATE_KEY=0x...
MAINNET_RPC_URL=https://eth-mainnet.g.alchemy.com/v2/...
SEPOLIA_RPC_URL=https://eth-sepolia.g.alchemy.com/v2/...
ETHERSCAN_API_KEY=...
```

## Contract Verification

### During Deployment

```bash
forge create src/MyContract.sol:MyContract \
    --rpc-url sepolia \
    --private-key $PRIVATE_KEY \
    --verify \
    --etherscan-api-key $ETHERSCAN_API_KEY \
    --broadcast
```

### After Deployment

```bash
# Basic verification
forge verify-contract \
    0xContractAddress \
    src/MyContract.sol:MyContract \
    --chain sepolia \
    --etherscan-api-key $ETHERSCAN_API_KEY

# With constructor args
forge verify-contract \
    0xContractAddress \
    src/MyContract.sol:MyContract \
    --chain sepolia \
    --constructor-args $(cast abi-encode "constructor(address,uint256)" 0xOwner 1000) \
    --etherscan-api-key $ETHERSCAN_API_KEY

# Watch for completion
forge verify-contract \
    0xContractAddress \
    src/MyContract.sol:MyContract \
    --chain sepolia \
    --watch
```

### Verify on Sourcify

```bash
forge verify-contract \
    0xContractAddress \
    src/MyContract.sol:MyContract \
    --chain sepolia \
    --verifier sourcify
```

## Deterministic Deployments (CREATE2)

### Using CREATE2

```solidity
contract DeployScript is Script {
    function run() public {
        bytes32 salt = keccak256("my-salt-v1");

        vm.startBroadcast();

        // CREATE2 deployment
        MyContract myContract = new MyContract{salt: salt}();

        vm.stopBroadcast();

        // Address is deterministic based on:
        // - deployer address
        // - salt
        // - contract bytecode
    }
}
```

### Pre-computing Address

```solidity
function computeCreate2Address(
    bytes32 salt,
    bytes32 initCodeHash,
    address deployer
) internal pure returns (address) {
    return address(uint160(uint256(keccak256(abi.encodePacked(
        bytes1(0xff),
        deployer,
        salt,
        initCodeHash
    )))));
}
```

## Multi-Chain Deployment

See [multichain.md](multichain.md) for patterns.

```solidity
contract MultiChainDeploy is Script {
    function run() public {
        // Deploy to multiple chains
        deployToChain("mainnet");
        deployToChain("arbitrum");
        deployToChain("base");
    }

    function deployToChain(string memory chain) internal {
        vm.createSelectFork(chain);
        vm.startBroadcast();

        new MyContract();

        vm.stopBroadcast();
    }
}
```

## Gas Estimation

```bash
# Estimate gas before deployment
forge script script/Deploy.s.sol --rpc-url $RPC_URL

# Output shows estimated gas for each transaction
```

## Transaction Management

### Pending Transactions

```bash
# List pending transactions
forge script script/Deploy.s.sol --rpc-url $RPC_URL --broadcast

# Resume after failure
forge script script/Deploy.s.sol --rpc-url $RPC_URL --resume

# Speed up pending tx
cast send --rpc-url $RPC_URL --gas-price 50gwei ...
```

### Transaction Files

Broadcasts are saved to:
```
broadcast/
└── Deploy.s.sol/
    └── 11155111/              # Chain ID (Sepolia)
        ├── run-latest.json    # Latest run
        └── run-1234567890.json
```

## Best Practices

1. **Always dry-run first**: Run without `--broadcast` to simulate
2. **Use environment variables**: Never commit private keys
3. **Verify contracts**: Always verify source code on explorers
4. **Save deployment addresses**: Log addresses for future reference
5. **Test on testnets first**: Deploy to Sepolia before mainnet
6. **Use deterministic deployments**: CREATE2 for consistent addresses
