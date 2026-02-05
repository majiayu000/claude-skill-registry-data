---
name: jpyc-dev-toolkit
description: Comprehensive toolkit for building applications with JPYC (Japanese Yen Pegged Coin). Use this skill when developing with JPYC token, implementing payment features, integrating JPYC SDK, deploying JPYC contracts to Base Sepolia, or building DApps with JPYC. Supports both JPYC SDK v1 usage and direct Solidity smart contract development with Hardhat, ethers.js, viem, Next.js, and React.
---

# JPYC Development Toolkit

## Overview

This skill provides comprehensive support for building applications with JPYC (Japanese Yen Pegged Coin), a stablecoin pegged to the Japanese Yen. It covers three main development approaches:

1. **JPYC SDK v1** - Using the official SDK for standard operations
2. **Smart Contract Development** - Building custom contracts that integrate with JPYC
3. **Frontend Integration** - Implementing JPYC features in web applications

The skill includes ready-to-use templates, deployment scripts, integration patterns, and best practices specifically tailored for JPYC development on Base Sepolia and other supported networks.

## When to Use This Skill

Trigger this skill when users request:

- "Implement JPYC payment functionality"
- "Deploy JPYC to Base Sepolia"
- "Set up JPYC SDK in my project"
- "Create a JPYC transfer component"
- "Build a donation system with JPYC"
- "Integrate JPYC into my DApp"
- "How do I use transferWithAuthorization with JPYC?"

## Quick Start Guide

### For SDK Users

If using the JPYC SDK v1:

1. **Setup**: Run the setup script
   ```bash
   bash scripts/setup_jpyc_sdk.sh
   ```

2. **Configure**: Edit `.env` with contract address and keys
   ```env
   JPYC_CONTRACT_ADDRESS=0x431D5dfF03120AFA4bDf332c61A6e1766eF37BDB
   PRIVATE_KEY=0x...
   RPC_URL=https://sepolia.base.org
   ```

3. **Use SDK functions**: See `references/sdk-features.md` for all available operations

### For Smart Contract Developers

If building custom contracts:

1. **Copy template**: Use `assets/contract-templates/JPYCIntegration.sol` as starting point

2. **Configure Hardhat**: Copy `assets/hardhat-config/hardhat.config.example.ts` to your project

3. **Deploy to Base Sepolia**: Use `scripts/deploy_jpyc_base.ts`

4. **Choose integration pattern**: See `references/integration-patterns.md` for recommended approaches

### For Frontend Developers

If building web interfaces:

1. **Copy components**: Use templates from `assets/frontend-examples/`
   - `JPYCBalance.tsx` - Display JPYC balance
   - `JPYCTransfer.tsx` - Transfer JPYC tokens

2. **Configure network**: Set up wagmi/viem with Base Sepolia (see `references/network-config.md`)

3. **Implement pattern**: Follow integration patterns in `references/integration-patterns.md`

## Core Development Tasks

### Task 1: Setting Up JPYC SDK

**When to use**: Need to interact with JPYC using the official SDK

**Steps**:

1. Add SDK as Git Submodule:
   ```bash
   git submodule add -b develop https://github.com/jcam1/sdks.git external/jpyc-sdk
   ```

2. Run automated setup:
   ```bash
   bash scripts/setup_jpyc_sdk.sh
   ```

3. Configure environment variables in `external/jpyc-sdk/packages/v1/.env`

**Available SDK operations**:
- Mint new tokens
- Get total supply
- Transfer tokens
- Approve spender
- Transfer from
- Permit allowance (EIP-2612)
- Transfer with Authorization (EIP-3009)
- Receive with Authorization (EIP-3009)
- Cancel Authorization (EIP-3009)

**Detailed reference**: See `references/sdk-features.md`

### Task 2: Deploying JPYC to Base Sepolia

**When to use**: Base Sepolia doesn't have official JPYC deployment, need custom deployment

**Prerequisites**:
- Base Sepolia ETH in your wallet
- JPYCv2 contract source code

**Steps**:

1. Add JPYCv2 as submodule:
   ```bash
   git submodule add https://github.com/jcam1/JPYCv2.git external/jpyc-contract
   ```

2. Configure Hardhat with Base Sepolia (copy from `assets/hardhat-config/hardhat.config.example.ts`)

3. Set environment variables:
   ```env
   PRIVATE_KEY=0x...
   BASE_SEPOLIA_RPC_URL=https://sepolia.base.org
   BASESCAN_API_KEY=your_api_key
   ```

4. Deploy using the script:
   ```bash
   npx hardhat run scripts/deploy_jpyc_base.ts --network baseSepolia
   ```

5. Verify contract on Basescan:
   ```bash
   npx hardhat verify --network baseSepolia <CONTRACT_ADDRESS>
   ```

**Detailed guide**: See `references/network-config.md`

### Task 3: Implementing Payment Features

**When to use**: Need to add JPYC payment functionality to your application

**Choose the right pattern** based on use case:

| Use Case | Pattern | Key Benefits |
|----------|---------|--------------|
| P2P transfers | `transfer` | Simple, low gas |
| E-commerce | `transferWithAuthorization` | Payment ID tracking, gasless |
| Subscriptions | `permit + transferFrom` | Flexible, recurring possible |
| B2B invoices | `receiveWithAuthorization` | Receiver controls execution |

**Implementation approaches**:

#### A. Using Smart Contracts

Start with the template contract:

```solidity
// Copy from assets/contract-templates/JPYCIntegration.sol
contract JPYCIntegration {
    function processPayment(
        address from,
        address to,
        uint256 amount,
        string calldata paymentId
    ) external {
        // Payment processing with ID tracking
    }
}
```

**Pros**: Maximum flexibility, custom business logic
**Cons**: Requires contract deployment and audit

#### B. Using EIP-3009 (Recommended)

Leverage JPYC's built-in `transferWithAuthorization`:

```typescript
// Hash payment ID to use as nonce
const paymentId = "order_12345";
const nonce = ethers.keccak256(ethers.toUtf8Bytes(paymentId));

// User signs authorization (gasless)
const signature = await signer.signTypedData(domain, types, {
  from: userAddress,
  to: merchantAddress,
  value: amount,
  validAfter: 0,
  validBefore: deadline,
  nonce: nonce
});

// Backend executes transfer (pays gas)
await jpycContract.transferWithAuthorization(
  userAddress, merchantAddress, amount,
  0, deadline, nonce, v, r, s
);
```

**Pros**: No custom contract needed, secure, low cost
**Cons**: Requires event monitoring and DB management

**Detailed patterns**: See `references/integration-patterns.md`

### Task 4: Building Frontend Components

**When to use**: Need UI components for JPYC interactions

**Available templates**:

#### Balance Display Component

Copy `assets/frontend-examples/JPYCBalance.tsx`:

```typescript
import { JPYCBalance } from './JPYCBalance';

<JPYCBalance jpycAddress="0x431D..." />
```

Features:
- Auto-refresh every 10 seconds
- Formatted display with decimals
- Loading and error states
- Customizable styling

#### Transfer Form Component

Copy `assets/frontend-examples/JPYCTransfer.tsx`:

```typescript
import { JPYCTransfer } from './JPYCTransfer';

<JPYCTransfer
  jpycAddress="0x431D..."
  onSuccess={(txHash) => console.log('Success:', txHash)}
  onError={(error) => console.error('Error:', error)}
/>
```

Features:
- Input validation
- Transaction status tracking
- Error handling
- Explorer link generation

**Setup requirements**:
1. Install dependencies: `wagmi`, `viem`
2. Configure network (see `references/network-config.md`)
3. Wrap app with WagmiProvider

### Task 5: Implementing Gasless Transactions

**When to use**: Want users to interact without paying gas fees

**Options**:

#### Option 1: EIP-2612 Permit

Best for: Approval without gas

```typescript
// User signs permit (no gas)
const signature = await signer.signTypedData(domain, permitTypes, {
  owner: userAddress,
  spender: contractAddress,
  value: amount,
  nonce: nonce,
  deadline: deadline
});

// Backend executes permit + transferFrom (pays gas)
await jpycContract.permit(userAddress, contractAddress, amount, deadline, v, r, s);
await contractAddress.transferFrom(userAddress, recipient, amount);
```

#### Option 2: EIP-3009 Transfer with Authorization

Best for: Direct transfers with payment ID

```typescript
// User signs authorization (no gas)
const signature = await signer.signTypedData(domain, transferTypes, {
  from: userAddress,
  to: merchantAddress,
  value: amount,
  validAfter: 0,
  validBefore: deadline,
  nonce: nonce
});

// Backend executes (pays gas)
await jpycContract.transferWithAuthorization(
  userAddress, merchantAddress, amount, 0, deadline, nonce, v, r, s
);
```

**Implementation details**: See `references/integration-patterns.md` Pattern 4

## Best Practices

### Security

1. **Approve Safety**: Always reset to zero before changing allowance
   ```solidity
   jpyc.approve(spender, 0);
   jpyc.approve(spender, newAmount);
   ```
   Or use `increaseAllowance` / `decreaseAllowance`

2. **Signature Validation**: Verify domain separator matches
   ```typescript
   const domain = {
     name: 'JPYCv2',
     version: '2',
     chainId: targetChainId,
     verifyingContract: jpycAddress
   };
   ```

3. **Nonce Management**: Ensure uniqueness to prevent replay
   ```typescript
   const paymentId = `order_${orderId}_${Date.now()}`;
   const nonce = ethers.keccak256(ethers.toUtf8Bytes(paymentId));
   ```

4. **Deadline Setting**: Set appropriate expiration times
   ```typescript
   const deadline = Math.floor(Date.now() / 1000) + 3600; // 1 hour
   ```

### Performance

1. **Use L2 Networks**: Deploy on Base Sepolia for lower gas costs

2. **Batch Operations**: Combine multiple operations when possible

3. **Event Monitoring**: Use WebSocket for real-time updates
   ```typescript
   jpycContract.on("Transfer", (from, to, amount) => {
     // Handle transfer event
   });
   ```

### Development Workflow

1. **Test Locally First**: Use Hardhat network for development
   ```bash
   npx hardhat node
   npx hardhat run scripts/deploy.ts --network localhost
   ```

2. **Use Testnets**: Deploy to Base Sepolia before mainnet

3. **Verify Contracts**: Always verify on block explorers
   ```bash
   npx hardhat verify --network baseSepolia <ADDRESS>
   ```

## Troubleshooting

### Common Issues

**"Insufficient funds" error**
- **Cause**: Not enough Base Sepolia ETH
- **Solution**: Get from faucet (see `references/resources.md`)

**"Network mismatch" error**
- **Cause**: Wallet connected to wrong network
- **Solution**: Switch to Base Sepolia (Chain ID: 84532)

**"Nonce already used" error**
- **Cause**: EIP-3009 nonce collision
- **Solution**: Ensure unique payment IDs, check DB for duplicates

**Signature verification fails**
- **Cause**: Incorrect domain separator or expired deadline
- **Solution**: Verify chainId, contract address, and deadline

## Resources

This skill includes comprehensive resources organized by type:

### scripts/

**`setup_jpyc_sdk.sh`** - Automated SDK setup
- Adds Git Submodule
- Installs dependencies
- Compiles SDK
- Generates .env template

**`deploy_jpyc_base.ts`** - Base Sepolia deployment
- Pre-flight checks (balance, network)
- Deploys JPYCv2 contract
- Configures roles (MINTER, etc.)
- Generates verification command

### references/

**`sdk-features.md`** - Complete SDK v1 reference
- All 9 available operations
- Setup instructions
- Code examples
- Security considerations

**`integration-patterns.md`** - Payment implementation patterns
- Pattern selection guide
- Code examples for each pattern
- Security best practices
- Trade-off analysis

**`network-config.md`** - Network configuration guide
- Base Sepolia setup
- Hardhat configuration
- Frontend setup (ethers.js, viem, wagmi)
- Troubleshooting

**`resources.md`** - External resources
- Official JPYC links
- GitHub repositories
- Technical articles
- Tools and explorers
- Faucets and RPC providers

### assets/

**`contract-templates/JPYCIntegration.sol`** - Smart contract template
- Payment processing with ID tracking
- Event emission
- Security features (ReentrancyGuard)
- Refund functionality

**`frontend-examples/`** - React components
- `JPYCBalance.tsx` - Balance display component
- `JPYCTransfer.tsx` - Transfer form component
- Uses wagmi + viem
- Production-ready with error handling

**`hardhat-config/hardhat.config.example.ts`** - Hardhat configuration
- Base Sepolia + other networks
- Etherscan/Basescan verification
- Gas reporter
- TypeChain support

## Additional Notes

- **Target Network**: Base Sepolia recommended for development (Chain ID: 84532)
- **JPYC Decimals**: 18 (same as ETH)
- **Contract Standard**: ERC20 with EIP-2612 and EIP-3009 extensions
- **Recommended Pattern**: EIP-3009 `transferWithAuthorization` for most use cases

For detailed information on any topic, refer to the corresponding file in `references/`.
