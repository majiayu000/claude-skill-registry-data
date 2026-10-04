---
name: circle-dev
description: >
  Comprehensive development support for Circle's stablecoin ecosystem including USDC/EURC integration,
  wallet solutions (Developer-Controlled, User-Controlled, Modular), cross-chain transfers (CCTP,
  Bridge Kit, Gateway), smart contracts, and payment APIs. Use when building applications with Circle
  for - (1) Stablecoin payments and transfers, (2) Wallet creation and management, (3) Cross-chain
  USDC/EURC transfers, (4) Smart contract deployment and management, (5) Gas fee sponsorship and
  optimization, (6) Circle Mint integration, (7) Global payment settlement, (8) FX operations with
  stablecoins. Covers SDK usage (TypeScript/JavaScript), API integration (REST), smart contract
  development (Solidity), and Circle-specific features like programmable wallets, native cross-chain
  transfers, and gasless transactions.
---

# Circle Development Support

Comprehensive toolkit for building stablecoin-powered applications with Circle's ecosystem including USDC, EURC, wallets, cross-chain transfers, and payment infrastructure.

## Quick Start

### Product Selection

Always start by choosing the right Circle product for your use case. See [product-guide.md](references/product-guide.md) for detailed comparison.

**Quick decision**:
- Accept/send stablecoin payments → **USDC/EURC** (stablecoins)
- Build wallet into app → **Developer-Controlled Wallets** (programmable wallets)
- Give users custody → **User-Controlled Wallets** (social login, PIN)
- Transfer USDC across chains → **CCTP or Bridge Kit** (cross-chain)
- Unified balance across chains → **Gateway** (chain abstraction)
- Deploy smart contracts → **Circle Contracts** (no-code + API)
- Sponsor user gas fees → **Gas Station** (developer-paid)
- Let users pay gas in USDC → **Circle Paymaster** (user-paid)
- Institutional liquidity → **Circle Mint** (fiat ↔ USDC/EURC)

### Common Tasks

**1. Create a wallet and send USDC**:
- Review [wallet_creation_example.ts](scripts/wallet_creation_example.ts) for wallet setup
- Key points: API key management, blockchain selection, transaction signing
- See [security.md](references/security.md) for security patterns

**2. Transfer USDC across chains**:
- Use [cctp_transfer_example.ts](scripts/cctp_transfer_example.ts) for native cross-chain transfers
- Alternative: [bridge_kit_example.ts](scripts/bridge_kit_example.ts) for simplified integration
- See [crosschain-guide.md](references/crosschain-guide.md) for comparison

**3. Enable gasless transactions**:
- Use [paymaster_example.ts](scripts/paymaster_example.ts) for USDC gas payments
- Or implement Gas Station for developer-sponsored fees
- See [gas-optimization.md](references/gas-optimization.md) for best practices

**4. Deploy smart contracts**:
- Start with Circle Contracts Console or API
- See [contracts-guide.md](references/contracts-guide.md) for deployment patterns
- Integrate with CCTP for cross-chain contract interactions

## Core Workflows

### Wallet Creation & Management

**Developer-Controlled Wallets** (backend-managed):
```typescript
import { initiateDeveloperControlledWalletsClient } from '@circle-fin/developer-controlled-wallets';

// 1. Initialize SDK
const client = initiateDeveloperControlledWalletsClient({
  apiKey: process.env.CIRCLE_API_KEY,
  entitySecret: process.env.ENTITY_SECRET
});

// 2. Create wallet
const wallet = await client.createWallet({
  accountType: 'SCA', // Smart Contract Account for ERC-4337
  blockchains: ['ETH-SEPOLIA', 'POLY-AMOY'],
  metadata: [{ name: 'user_id', value: 'user123' }]
});

// 3. Send USDC
const transfer = await client.createTransaction({
  walletId: wallet.data.walletId,
  blockchain: 'ETH-SEPOLIA',
  tokenAddress: '0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238', // USDC
  destinationAddress: '0x...',
  amount: ['10.00']
});
```

**User-Controlled Wallets** (user-custodied with social login):
```typescript
import { W3SSdk } from '@circle-fin/w3s-pw-web-sdk';

// 1. Initialize SDK
const sdk = new W3SSdk({
  appId: process.env.APP_ID,
  authentication: {
    userToken: userToken,
    encryptionKey: encryptionKey
  }
});

// 2. Create wallet with social login
await sdk.execute(challengeId, (error, result) => {
  if (result) {
    console.log('Wallet created:', result.data.wallets);
  }
});
```

See [wallet_creation_example.ts](scripts/wallet_creation_example.ts) for complete implementation.

### Cross-Chain USDC Transfers

**CCTP (Native Cross-Chain Transfer Protocol)**:
```typescript
import { CircleClient } from '@circle-fin/circle-sdk';

// 1. Initialize SDK
const circle = new CircleClient({ apiKey: process.env.CIRCLE_API_KEY });

// 2. Burn USDC on source chain (e.g., Ethereum)
const burnTx = await sourceChainUSDC.burn(amount);
const messageHash = await waitForAttestation(burnTx.hash);

// 3. Get attestation from Circle
const attestation = await circle.getAttestation(messageHash);

// 4. Mint USDC on destination chain (e.g., Arbitrum)
const mintTx = await destChainReceiver.receiveMessage(
  attestation.message,
  attestation.signature
);
```

**Bridge Kit (Simplified SDK)**:
```typescript
import { createBridgeKit } from '@circle-fin/bridge-kit';

// 1. Initialize Bridge Kit
const kit = createBridgeKit({ apiKey: process.env.BRIDGE_API_KEY });

// 2. Execute transfer (handles CCTP under the hood)
const result = await kit.bridge({
  from: { adapter: viemAdapter, chain: 'Ethereum' },
  to: { adapter: solanaAdapter, chain: 'Solana' },
  amount: '100.00'
});

console.log('Transfer status:', result.status);
```

See [cctp_transfer_example.ts](scripts/cctp_transfer_example.ts) and [bridge_kit_example.ts](scripts/bridge_kit_example.ts).

### Gas Fee Management

**Circle Paymaster (Users Pay in USDC)**:
```typescript
import { PaymasterClient } from '@circle-fin/paymaster-sdk';

// 1. Initialize Paymaster client
const paymaster = new PaymasterClient({
  chain: 'ethereum',
  paymasterAddress: '0x...' // Circle Paymaster contract
});

// 2. Get UserOperation with Paymaster fields
const userOp = await paymaster.sponsorUserOperation({
  sender: wallet.address,
  callData: encodedCallData,
  // Paymaster will be paid in USDC
});

// 3. Submit to bundler
const txHash = await bundler.sendUserOperation(userOp);
```

**Gas Station (Developer Sponsors Fees)**:
```typescript
// 1. Create SCA wallet with Gas Station enabled
const wallet = await client.createWallet({
  accountType: 'SCA',
  blockchains: ['ETH-SEPOLIA']
});

// 2. Configure Gas Station policy in Circle Console
// Set spending limits, allowed contracts, etc.

// 3. Transactions automatically use Gas Station
const tx = await client.createTransaction({
  walletId: wallet.data.walletId,
  // Gas fees automatically sponsored
});
```

See [gas-optimization.md](references/gas-optimization.md) for detailed patterns.

### Smart Contract Deployment

**Via Console (No-Code)**:
1. Navigate to Circle Developer Console → Contracts
2. Select template (ERC-20, ERC-721, ERC-1155, or custom)
3. Configure parameters and deploy

**Via API (Programmatic)**:
```typescript
import { CircleContracts } from '@circle-fin/contracts-sdk';

// 1. Initialize SDK
const contracts = new CircleContracts({
  apiKey: process.env.CIRCLE_API_KEY
});

// 2. Deploy contract
const deployment = await contracts.deployContract({
  walletId: wallet.data.walletId,
  blockchain: 'ETH-SEPOLIA',
  templateId: 'erc20', // or custom bytecode
  parameters: {
    name: 'MyToken',
    symbol: 'MTK',
    totalSupply: '1000000'
  }
});

// 3. Monitor deployment
const status = await contracts.getDeploymentStatus(deployment.id);
```

See [contracts-guide.md](references/contracts-guide.md) for advanced patterns.

## Critical Security Requirements

**Never deploy without**:

1. **API Key Protection**: Store API keys in environment variables, never commit to code
2. **Entity Secret Encryption**: Use secure key management for wallet entity secrets
3. **Transaction Validation**: Always verify recipient addresses and amounts
4. **Rate Limiting**: Implement request throttling for API calls
5. **Webhook Verification**: Validate webhook signatures from Circle
6. **Smart Contract Audits**: Audit custom contracts before mainnet deployment
7. **Testnet Testing**: Test all flows on testnet (Sepolia, Amoy, etc.) first

See [security.md](references/security.md) for complete checklist and examples.

## Architecture Patterns

### Programmable Wallets Architecture

Circle offers three wallet types optimized for different use cases:

**Developer-Controlled**:
- Backend manages private keys
- Ideal for custodial applications
- Supports batch operations
- Gas Station compatible

**User-Controlled**:
- User owns keys (MPC-based)
- Social login (Google, Apple, Email)
- PIN recovery mechanism
- Best for consumer apps

**Modular (MSCA)**:
- Flexible smart contract accounts
- Custom business logic via modules
- ERC-4337 compatible
- Advanced use cases

See [wallets-guide.md](references/wallets-guide.md) for detailed comparison.

### Cross-Chain Architecture

**CCTP (Point-to-Point)**:
```
Source Chain (Ethereum)
  ↓ Burn USDC
Circle Attestation Service
  ↓ Sign burn event
Destination Chain (Arbitrum)
  ↓ Mint USDC
```

**Gateway (Unified Balance)**:
```
Deposit to Gateway Wallet (any chain)
  ↓ Balance pooled
Gateway API Attestation
  ↓ Instant transfer (<500ms)
Withdraw on any chain
```

See [crosschain-guide.md](references/crosschain-guide.md) for architecture details.

## Development Setup

### Dependencies

**Wallet SDKs**:
```bash
# Developer-Controlled Wallets
npm install @circle-fin/developer-controlled-wallets

# User-Controlled Wallets (Web)
npm install @circle-fin/w3s-pw-web-sdk

# User-Controlled Wallets (React Native)
npm install @circle-fin/w3s-pw-react-native-sdk
```

**Cross-Chain SDKs**:
```bash
# Bridge Kit
npm install @circle-fin/bridge-kit

# CCTP contracts (Solidity)
npm install @circle-fin/evm-cctp-contracts
```

**Smart Contract Tools**:
```bash
# Circle Contracts SDK
npm install @circle-fin/contracts-sdk

# Standard tools
npm install ethers viem
```

### Contract Addresses

**USDC Token Addresses**:
- Ethereum Mainnet: `0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48`
- Arbitrum: `0xaf88d065e77c8cC2239327C5EDb3A432268e5831`
- Optimism: `0x0b2C639c533813f4Aa9D7837CAf62653d097Ff85`
- Polygon: `0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359`
- Base: `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`
- Solana: `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v`
- Sepolia (Testnet): `0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238`

**CCTP Contracts (Mainnet)**:
- Ethereum TokenMessenger: `0xBd3fa81B58Ba92a82136038B25aDec7066af3155`
- Arbitrum TokenMessenger: `0x19330d10D9Cc8751218eaf51E8885D058642E08A`

**Circle Paymaster (Mainnet)**:
- Ethereum: `0x...` (Check latest deployment)
- Arbitrum: `0x...`
- Base: `0x...`

See [api-reference.md](references/api-reference.md) for complete address list.

## Supported Blockchains

### USDC/EURC Support
- **EVM Chains**: Ethereum, Arbitrum, Optimism, Base, Polygon, Avalanche, BSC
- **Non-EVM**: Solana, Sui, Algorand, Stellar, NEAR, Polkadot, Hedera
- **Total**: 20+ blockchains

### Wallet Support (Programmable Wallets)
- **Dev & User-Controlled**: Ethereum, Arbitrum, Optimism, Base, Polygon, Avalanche
- **Modular Wallets**: Select EVM chains with ERC-4337 support

### Cross-Chain Support
- **CCTP**: Ethereum, Arbitrum, Optimism, Base, Polygon, Avalanche, Solana, Sui
- **Bridge Kit**: 200+ routes across dozens of blockchains
- **Gateway**: All major EVM chains + Solana

## Testing

### SDK Testing (TypeScript)

```typescript
import { expect } from 'chai';
import { initiateDeveloperControlledWalletsClient } from '@circle-fin/developer-controlled-wallets';

describe('Wallet Integration', () => {
  it('should create wallet successfully', async () => {
    const client = initiateDeveloperControlledWalletsClient({
      apiKey: process.env.TEST_API_KEY,
      entitySecret: process.env.TEST_ENTITY_SECRET
    });

    const wallet = await client.createWallet({
      accountType: 'EOA',
      blockchains: ['ETH-SEPOLIA']
    });

    expect(wallet.data.walletId).to.be.a('string');
    expect(wallet.data.state).to.equal('LIVE');
  });
});
```

### Smart Contract Testing (Foundry)

```solidity
import {Test} from "forge-std/Test.sol";
import {ITokenMessenger} from "@circle-fin/evm-cctp-contracts/interfaces/ITokenMessenger.sol";

contract CCTPTest is Test {
    ITokenMessenger tokenMessenger;
    address usdc;

    function setUp() public {
        // Fork mainnet
        vm.createSelectFork(vm.envString("ETH_RPC_URL"));

        tokenMessenger = ITokenMessenger(0xBd3fa81B58Ba92a82136038B25aDec7066af3155);
        usdc = 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48;
    }

    function testBurnUSDC() public {
        // Test CCTP burn functionality
        uint256 amount = 100e6; // 100 USDC

        vm.startPrank(user);
        IERC20(usdc).approve(address(tokenMessenger), amount);

        uint64 nonce = tokenMessenger.depositForBurn(
            amount,
            4, // Arbitrum domain
            bytes32(uint256(uint160(recipient))),
            usdc
        );

        assertTrue(nonce > 0);
        vm.stopPrank();
    }
}
```

## Common Pitfalls

1. **Testnet vs Mainnet confusion**: Always verify blockchain parameter (e.g., 'ETH-SEPOLIA' vs 'ETH')
2. **Missing API key**: Ensure API keys are properly configured for each environment
3. **Insufficient USDC approval**: Always approve sufficient amount before transfers
4. **Wrong token address**: USDC addresses differ across chains - verify before each transaction
5. **Gas Station wallet type**: Must use SCA (Smart Contract Account) for Gas Station
6. **CCTP attestation timeout**: Attestations can take up to 20 minutes on mainnet
7. **Webhook signature validation**: Always verify Circle webhook signatures
8. **Entity secret management**: Never expose entity secrets in frontend code

## MCP Server Integration

Circle provides an MCP server for AI-assisted development:

```bash
# Claude Code
claude mcp add --transport http circle https://api.circle.com/v1/codegen/mcp --scope user

# Cursor (1-click)
# Visit Circle MCP documentation for auto-install

# Windsurf / Kiro
# Add to mcp_config.json
```

The MCP server helps generate code for:
- Wallet creation and management
- CCTP cross-chain transfers
- Bridge Kit integration
- Smart contract deployment
- Payment flows

## Resources

### Documentation
- **Main Docs**: https://developers.circle.com/
- **USDC Guide**: https://developers.circle.com/stablecoins/what-is-usdc
- **Wallets**: https://developers.circle.com/wallets/
- **CCTP**: https://developers.circle.com/cctp
- **API Reference**: https://developers.circle.com/api-reference

### Code Examples
- **Sample Projects**: https://developers.circle.com/sample-projects
- **GitHub**: https://github.com/circlefin
- **CCTP Contracts**: https://github.com/circlefin/evm-cctp-contracts

### Support
- **Documentation**: https://developers.circle.com/
- **GitHub Issues**: https://github.com/circlefin
- **Status Page**: https://status.circle.com/

## Bundled Resources

### Scripts
- **[wallet_creation_example.ts](scripts/wallet_creation_example.ts)**: Complete wallet creation with security
- **[cctp_transfer_example.ts](scripts/cctp_transfer_example.ts)**: Native cross-chain USDC transfer
- **[bridge_kit_example.ts](scripts/bridge_kit_example.ts)**: Simplified cross-chain transfer with Bridge Kit
- **[paymaster_example.ts](scripts/paymaster_example.ts)**: USDC gas payment implementation

### References
- **[product-guide.md](references/product-guide.md)**: Circle product comparison and selection
- **[wallets-guide.md](references/wallets-guide.md)**: Deep dive into wallet types and architecture
- **[crosschain-guide.md](references/crosschain-guide.md)**: CCTP, Bridge Kit, and Gateway comparison
- **[security.md](references/security.md)**: Security best practices and checklist
- **[gas-optimization.md](references/gas-optimization.md)**: Gas fee optimization strategies
- **[contracts-guide.md](references/contracts-guide.md)**: Smart contract deployment and management
- **[api-reference.md](references/api-reference.md)**: Complete API reference with addresses

### Assets
- **[wallet-integration-template.ts](assets/wallet-integration-template.ts)**: Production-ready wallet integration
- **[cctp-contract-template.sol](assets/cctp-contract-template.sol)**: CCTP smart contract template

## Support Context7 Integration

When the user needs up-to-date documentation or specific implementation details not covered in this skill:

1. Identify the library needed (e.g., "@circle-fin/developer-controlled-wallets", "@circle-fin/bridge-kit")
2. Use Context7 MCP tools to query latest documentation
3. Combine Context7 results with this skill's guidance

Example:
```
User: "How do I use the new Modular Wallets features?"
→ Use Context7: resolve-library-id("@circle-fin/modular-wallets")
→ Then query-docs with specific module questions
→ Apply security patterns from security.md
```

## Circle Mint & Payments

### Circle Mint (Institutional Fiat ↔ USDC/EURC)

Circle Mint is for institutional customers to mint/redeem USDC and EURC:

**Access Requirements**:
- Business entity (exchanges, wallets, banks, etc.)
- Contact Circle for account setup
- Bank account in supported country (200+ countries)

**Features**:
- Zero-fee fiat ↔ USDC/EURC conversion
- Near-instant settlement with partner banks
- Global transfers across 20+ blockchains
- API access for programmatic operations

**Use Cases**:
- Exchange liquidity management
- Institutional treasury operations
- Payment processor integration
- Global remittances

### Circle Payments Network (CPN)

Real-time global settlement network for financial institutions:

**Key Features**:
- Real-time FX quoting and locking
- Smart routing across beneficiary institutions
- USDC-powered cross-border transfers
- End-to-end encryption for compliance
- Webhook-based payment monitoring

**Target Users**: Originating Financial Institutions (OFIs)

**Workflow**:
1. Generate FX quote
2. Create payment with beneficiary details
3. Transfer USDC on-chain
4. Circle handles settlement with beneficiary

See API documentation for integration details.

## StableFX

Foreign exchange operations using stablecoins:

**Capabilities**:
- Integrate FX functionality into applications
- Support multi-currency operations with stablecoins
- Real-time exchange rate updates

Contact Circle for access to StableFX APIs.
