---
name: cast-commands
description: Interact with EVM chains using Cast CLI. Use when querying blockchain data, sending transactions, calling contracts, or converting between formats. Cast is the Swiss Army knife for chain interaction.
---

# Cast Commands

Cast is Foundry's command-line tool for interacting with EVM-compatible blockchains.

## When to Use

- Querying contract state (balances, storage, call results)
- Sending transactions
- Calling contract functions
- Converting between data formats
- Debugging transactions
- ENS resolution
- ABI encoding/decoding

## Reading Contract State

### call - Read-Only Function Calls

```bash
# Call a view function
cast call 0xContract "balanceOf(address)(uint256)" 0xAddress

# Call with RPC URL
cast call 0xContract "totalSupply()(uint256)" --rpc-url mainnet

# Call function with multiple return values
cast call 0xContract "getReserves()(uint112,uint112,uint32)"
```

### balance - Get ETH Balance

```bash
# Get balance in wei
cast balance 0xAddress --rpc-url mainnet

# Get balance in ether
cast balance 0xAddress --rpc-url mainnet -e
```

### storage - Read Storage Slots

```bash
# Read slot 0
cast storage 0xContract 0 --rpc-url mainnet

# Read specific slot
cast storage 0xContract 0x2 --rpc-url mainnet
```

### code - Get Contract Bytecode

```bash
# Get deployed bytecode
cast code 0xContract --rpc-url mainnet
```

## Sending Transactions

### send - Write Transactions

```bash
# Send transaction
cast send 0xContract "transfer(address,uint256)" \
    0xRecipient 1000000000000000000 \
    --rpc-url mainnet \
    --private-key $PRIVATE_KEY

# Send with value (ETH)
cast send 0xContract "deposit()" \
    --value 1ether \
    --rpc-url mainnet \
    --private-key $PRIVATE_KEY

# Send raw ETH transfer
cast send 0xRecipient --value 1ether \
    --rpc-url mainnet \
    --private-key $PRIVATE_KEY
```

### Gas Configuration

```bash
# Specify gas limit
cast send 0xContract "mint()" --gas 500000

# Specify gas price (legacy)
cast send 0xContract "mint()" --gas-price 50gwei

# Specify EIP-1559 fees
cast send 0xContract "mint()" \
    --priority-gas-price 2gwei \
    --gas-price 100gwei
```

## ABI Encoding/Decoding

### abi-encode - Encode Function Arguments

```bash
# Encode function call data
cast abi-encode "transfer(address,uint256)" 0xRecipient 1000

# Encode constructor arguments
cast abi-encode "constructor(string,string,uint8)" "Token" "TKN" 18
```

### abi-decode - Decode Data

```bash
# Decode function output
cast abi-decode "balanceOf(address)(uint256)" 0x000...0001

# Decode with multiple outputs
cast abi-decode "getReserves()(uint112,uint112,uint32)" 0x...
```

### calldata - Encode Full Calldata

```bash
# Encode function selector + arguments
cast calldata "transfer(address,uint256)" 0xRecipient 1000
# Output: 0xa9059cbb...

# Decode calldata
cast calldata-decode "transfer(address,uint256)" 0xa9059cbb...
```

### sig - Get Function Selector

```bash
# Get 4-byte selector
cast sig "transfer(address,uint256)"
# Output: 0xa9059cbb

# Get event signature
cast sig-event "Transfer(address,address,uint256)"
```

## Data Conversion

### Numbers

```bash
# Hex to decimal
cast to-dec 0xff
# Output: 255

# Decimal to hex
cast to-hex 255
# Output: 0xff

# Convert to wei
cast to-wei 1.5 ether
# Output: 1500000000000000000

# Convert from wei
cast from-wei 1500000000000000000
# Output: 1.5
```

### Units

```bash
# Parse units
cast to-unit 1000000000000000000 ether
# Output: 1

# Format units
cast to-wei 100 gwei
# Output: 100000000000
```

### Strings and Bytes

```bash
# String to bytes32
cast format-bytes32-string "hello"

# Bytes32 to string
cast parse-bytes32-string 0x68656c6c6f...

# ASCII to hex
cast from-utf8 "hello"

# Hex to ASCII
cast to-ascii 0x68656c6c6f
```

### Addresses

```bash
# Checksum address
cast to-checksum-address 0xaddress

# Compute CREATE address
cast compute-address 0xDeployer --nonce 5

# Compute CREATE2 address
cast create2 --starts-with 0000 \
    --deployer 0xDeployer \
    --init-code-hash 0x...
```

## Block & Transaction Info

### block - Get Block Data

```bash
# Get latest block
cast block latest --rpc-url mainnet

# Get specific block
cast block 18000000 --rpc-url mainnet

# Get block field
cast block latest --field timestamp --rpc-url mainnet
```

### tx - Get Transaction Data

```bash
# Get transaction by hash
cast tx 0xTxHash --rpc-url mainnet

# Get specific field
cast tx 0xTxHash --field gasPrice --rpc-url mainnet
```

### receipt - Get Transaction Receipt

```bash
# Get receipt
cast receipt 0xTxHash --rpc-url mainnet

# Get logs
cast receipt 0xTxHash --field logs --rpc-url mainnet
```

### logs - Get Event Logs

```bash
# Get logs by event signature
cast logs "Transfer(address,address,uint256)" \
    --from-block 18000000 \
    --to-block latest \
    --address 0xTokenContract \
    --rpc-url mainnet
```

## Chain Info

```bash
# Get chain ID
cast chain-id --rpc-url mainnet

# Get gas price
cast gas-price --rpc-url mainnet

# Get base fee
cast base-fee --rpc-url mainnet

# Get nonce
cast nonce 0xAddress --rpc-url mainnet
```

## ENS

```bash
# Resolve ENS name
cast resolve-name vitalik.eth --rpc-url mainnet

# Lookup address
cast lookup-address 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045 --rpc-url mainnet
```

## Wallet Operations

### wallet - Manage Keys

```bash
# Generate new wallet
cast wallet new

# Get address from private key
cast wallet address --private-key $PRIVATE_KEY

# Sign message
cast wallet sign "message" --private-key $PRIVATE_KEY

# Verify signature
cast wallet verify --address 0xAddress "message" 0xSignature
```

## Debugging

### run - Trace Transaction

```bash
# Run transaction trace
cast run 0xTxHash --rpc-url mainnet

# Quick trace
cast run 0xTxHash --quick --rpc-url mainnet
```

### 4byte - Decode Function Signature

```bash
# Lookup function signature
cast 4byte 0xa9059cbb
# Output: transfer(address,uint256)

# Lookup event signature
cast 4byte-event 0xddf252ad...
```

## Utility Commands

### keccak - Hash Data

```bash
# Keccak256 hash
cast keccak "hello"

# Hash function signature (for selector)
cast keccak "transfer(address,uint256)" | cut -c1-10
```

### concat-hex - Concatenate Hex

```bash
cast concat-hex 0x1234 0x5678
# Output: 0x12345678
```

### access-list - Generate Access List

```bash
# Generate access list for transaction
cast access-list 0xContract "swap(uint256)" 1000 \
    --rpc-url mainnet
```

## RPC Configuration

### Using foundry.toml

```toml
[rpc_endpoints]
mainnet = "${MAINNET_RPC_URL}"
sepolia = "${SEPOLIA_RPC_URL}"
```

```bash
# Use named endpoint
cast call 0xContract "totalSupply()(uint256)" --rpc-url mainnet
```

### Environment Variable

```bash
export ETH_RPC_URL=https://eth-mainnet.g.alchemy.com/v2/...
cast call 0xContract "totalSupply()(uint256)"
```

## Common Patterns

See [patterns.md](patterns.md) for more examples.

### Check Token Balance

```bash
cast call $TOKEN "balanceOf(address)(uint256)" $ADDRESS --rpc-url mainnet | cast to-dec
```

### Approve and Transfer

```bash
# Approve
cast send $TOKEN "approve(address,uint256)" $SPENDER $AMOUNT \
    --rpc-url mainnet --private-key $PK

# Transfer
cast send $TOKEN "transferFrom(address,address,uint256)" $FROM $TO $AMOUNT \
    --rpc-url mainnet --private-key $PK
```

### Interact with Uniswap

```bash
# Get reserves
cast call $PAIR "getReserves()(uint112,uint112,uint32)" --rpc-url mainnet

# Get price
cast call $ROUTER "getAmountsOut(uint256,address[])(uint256[])" \
    1000000000000000000 "[$WETH,$USDC]" --rpc-url mainnet
```
