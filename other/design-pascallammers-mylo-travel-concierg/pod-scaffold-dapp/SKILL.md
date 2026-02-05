---
name: pod-scaffold-dapp
description: This skill should be used when developers need to scaffold complete decentralized applications on pod network, including smart contracts, Rust CLI tools, web frontends (React + Vite + viem), and testing infrastructure. Use when starting new DApps, building full-stack applications, or needing end-to-end project setup. Orchestrates pod-templating MCP server, frontend templates, and development tools for comprehensive DApp creation.
---

# pod Scaffold DApp

Orchestrate complete decentralized application scaffolding for pod network, from smart contracts to web frontends.

## Overview

This skill guides developers through creating production-ready pod network DApps with all necessary layers:

- **Smart contracts** (Solidity + FastTypes)
- **CLI tools** (Rust + pod SDK)
- **Web frontend** (React + Vite + viem)
- **Testing infrastructure** (Foundry + Vitest)
- **Deployment configuration**

Use the pod-templating MCP server for backend scaffolding and built-in frontend templates for complete DApp creation.

## When to Use This Skill

Trigger this skill when developers need:

**Full-stack DApp creation:**

- "Create a complete token DApp with frontend"
- "Build an NFT marketplace on pod network"
- "I need a voting platform with web UI"
- "Scaffold a complete DApp for pod network"

**Adding frontend to existing contracts:**

- "Add a web frontend to my pod contract"
- "Create a React UI for my deployed token"
- "I need a user interface for my NFT contract"

**Full project setup:**

- "Set up a new pod network project with everything"
- "Initialize a DApp with contract, CLI, and frontend"
- "Start a full-stack pod application"

## Scaffolding Workflow

### Step 1: Choose DApp Template

First, identify the appropriate full project template from pod-templating MCP server.

**Available full project templates** (Solidity + Rust CLI + Foundry):

| Template          | Description                | Includes                      |
| ----------------- | -------------------------- | ----------------------------- |
| `token-contract`  | ERC20-style token DApp     | Token contract + CLI + tests  |
| `nft-contract`    | ERC721-style NFT DApp      | NFT contract + CLI + tests    |
| `voting-contract` | Governance/voting DApp     | Voting contract + CLI + tests |
| `notary-contract` | Document notarization DApp | Notary contract + CLI + tests |

**For simple/custom contracts**, use simple templates and add structure manually:

| Template         | Description          | Use Case                  |
| ---------------- | -------------------- | ------------------------- |
| `basic-contract` | Minimal starter      | Custom logic, learning    |
| `token-simple`   | Token only (no CLI)  | Need custom CLI structure |
| `nft-simple`     | NFT only (no CLI)    | Need custom CLI structure |
| `voting-simple`  | Voting only (no CLI) | Need custom CLI structure |
| `auction`        | Auction contract     | Time-based bidding DApp   |

**Recommendation**: Start with full project templates (`token-contract`, `nft-contract`, `voting-contract`, `notary-contract`) for fastest setup.

### Step 2: Discover Template Details

Use `get_template_details` to understand template structure and required variables:

```javascript
// Get details for full project template
get_template_details({
  templateName: 'token-contract'
});
```

**Returns:**

- Template metadata
- Required variables (contract name, token parameters, etc.)
- Project structure overview
- Next steps

### Step 3: Scaffold Backend (Contract + CLI + Tests)

Use `render_template` to generate the complete backend:

```javascript
// Scaffold full project (contract + CLI + tests)
render_template({
  templateName: 'token-contract',
  targetPath: '/path/to/my-token-dapp',
  variables: {
    contract_name: 'GameToken',
    token_name: 'Game Coin',
    token_symbol: 'GAME',
    decimals: '18',
    max_supply: '1000000',
    license: 'MIT'
  }
});
```

**Result:**

```
my-token-dapp/
├── contract/           # Solidity contracts + Foundry
│   ├── src/
│   │   └── GameToken.sol
│   ├── test/
│   │   └── GameToken.t.sol
│   ├── script/
│   │   └── Deploy.s.sol
│   ├── foundry.toml
│   └── out/          # Compiled artifacts (after forge build)
├── cli/              # Rust CLI
│   ├── src/
│   │   ├── main.rs
│   │   └── bindings.rs
│   ├── Cargo.toml
│   └── target/       # Built CLI (after cargo build)
└── README.md
```

### Step 4: Add Frontend Layer

Copy the frontend template from `assets/frontend-template/` to the project:

```bash
# Copy frontend template to project
cp -r assets/frontend-template/ my-token-dapp/frontend/

# Navigate to frontend
cd my-token-dapp/frontend
```

**Result:**

```
my-token-dapp/
├── contract/         # (from Step 3)
├── cli/             # (from Step 3)
└── frontend/        # NEW: React + Vite + viem
    ├── src/
    │   ├── components/
    │   │   ├── WalletConnect.tsx
    │   │   └── NetworkInfo.tsx
    │   ├── contracts/
    │   │   └── config.ts    # Configure contract here
    │   ├── lib/
    │   │   ├── chains.ts    # pod network config
    │   │   └── wagmi-config.ts
    │   ├── App.tsx
    │   └── main.tsx
    ├── package.json
    ├── vite.config.ts
    └── .env.example
```

### Step 5: Configure Frontend Integration

**5a. Install Frontend Dependencies**

```bash
cd frontend
npm install
```

**5b. Configure Environment**

```bash
cp .env.example .env
```

Update `.env`:

```env
VITE_MIDNIGHT_RPC_URL=wss://rpc.testnet-02.midnight.network
VITE_POD_CHAIN_ID=54321
VITE_CONTRACT_ADDRESS=0x...  # After deployment
VITE_WALLETCONNECT_PROJECT_ID=your-project-id
```

**5c. Add Contract ABI**

After compiling contract (`cd ../contract && forge build`):

```typescript
// frontend/src/contracts/config.ts
import contractAbi from '../../../contract/out/GameToken.sol/GameToken.json';

export const CONTRACT_ADDRESS = import.meta.env.VITE_CONTRACT_ADDRESS as `0x${string}`;
export const CONTRACT_ABI = contractAbi.abi;
```

**5d. Update Chain Configuration (if needed)**

Edit `frontend/src/lib/chains.ts` to match actual pod network chain IDs.

### Step 6: Build and Test Locally

**6a. Compile Contract**

```bash
cd contract
forge build
```

**6b. Test Contract**

```bash
forge test
```

**6c. Start Frontend Dev Server**

```bash
cd ../frontend
npm run dev
```

Open http://localhost:3000

### Step 7: Add DApp-Specific Components

Based on the contract type, add custom components to `frontend/src/components/`:

**For Token DApp:**

```typescript
// frontend/src/components/TokenBalance.tsx
import { useReadContract, useAccount } from 'wagmi';
import { CONTRACT_ADDRESS, CONTRACT_ABI } from '../contracts/config';

export function TokenBalance() {
  const { address } = useAccount();
  const { data: balance } = useReadContract({
    address: CONTRACT_ADDRESS,
    abi: CONTRACT_ABI,
    functionName: 'balanceOf',
    args: address ? [address] : undefined,
  });

  return <div>Your balance: {balance?.toString() || '0'}</div>;
}
```

```typescript
// frontend/src/components/TransferForm.tsx
import { useWriteContract } from 'wagmi';
import { useState } from 'react';
import { parseUnits } from 'viem';
import { CONTRACT_ADDRESS, CONTRACT_ABI } from '../contracts/config';

export function TransferForm() {
  const [to, setTo] = useState('');
  const [amount, setAmount] = useState('');
  const { writeContract, isPending } = useWriteContract();

  const handleTransfer = () => {
    writeContract({
      address: CONTRACT_ADDRESS,
      abi: CONTRACT_ABI,
      functionName: 'transfer',
      args: [to as `0x${string}`, parseUnits(amount, 18)],
    });
  };

  return (
    <form onSubmit={(e) => { e.preventDefault(); handleTransfer(); }}>
      <input
        placeholder="Recipient address"
        value={to}
        onChange={(e) => setTo(e.target.value)}
      />
      <input
        placeholder="Amount"
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
      />
      <button type="submit" disabled={isPending}>
        {isPending ? 'Transferring...' : 'Transfer'}
      </button>
    </form>
  );
}
```

**For NFT DApp:**

- `NFTGallery.tsx` - Display owned NFTs
- `MintForm.tsx` - Mint new NFTs
- `NFTCard.tsx` - Individual NFT display

**For Voting DApp:**

- `ProposalList.tsx` - Show all proposals
- `VoteButton.tsx` - Cast vote
- `Results.tsx` - Display voting results

**For Auction DApp:**

- `AuctionTimer.tsx` - Display time remaining
- `BidForm.tsx` - Place bid
- `BidHistory.tsx` - Show bid history

### Step 8: Deploy and Verify

**8a. Deploy Contract**

Use `midnight-deployment-engineer` agent for production deployment:

```
"Deploy my GameToken contract to pod devnet"
```

**Agent will:**

- Generate deployment script
- Validate deployment readiness
- Provide deployment instructions
- Verify contract on pod explorer
- Output contract address

**8b. Update Frontend Configuration**

After deployment, update `frontend/.env`:

```env
VITE_CONTRACT_ADDRESS=0xDeployedContractAddress
```

**8c. Build and Deploy Frontend**

```bash
cd frontend
npm run build
```

Deploy `dist/` to Vercel, Netlify, or other hosting.

## Progressive Reference Loading

Load reference documents as needed for detailed guidance:

### references/frontend-integration.md

**Load when:**

- Need to integrate frontend with contracts
- Want to understand viem/wagmi patterns
- Adding custom contract interactions
- Implementing event listening
- Optimizing frontend performance

**Contains:**

- Complete viem + wagmi setup guide
- Contract interaction patterns (read/write)
- pod network-specific frontend patterns (finality, time-based logic)
- Event listening examples
- Common DApp components (wallet connect, network switcher)
- Testing frontend integration
- Performance optimization techniques

### references/dapp-architecture.md

**Load when:**

- Need to understand full DApp architecture
- Planning component interactions
- Designing data flow
- Structuring large DApps
- Making architectural decisions

**Contains:**

- Complete DApp layer breakdown
- Data flow patterns
- Component integration strategies
- File system organization
- Deployment strategies
- Full-stack testing approaches
- pod network-specific architectural considerations
- MCP server integration patterns

## Template Selection Guide

### Choose Based on Complexity

| Need                | Recommended Template  | Reason                             |
| ------------------- | --------------------- | ---------------------------------- |
| Quick start         | Full project template | Everything pre-configured          |
| Standard use cases  | Full project template | Production-ready, best practices   |
| Custom requirements | Simple template       | More flexibility, manual CLI setup |
| Learning            | Simple template       | Understand each component          |

### Full Project Templates (Recommended)

**Advantages:**

- ✅ Complete project structure
- ✅ CLI tools included
- ✅ Foundry tests ready
- ✅ Deployment scripts
- ✅ Best practices enforced

**Use for:**

- Production DApps
- Rapid prototyping
- Standard use cases (tokens, NFTs, voting)

### Simple Templates

**Advantages:**

- ✅ More customization flexibility
- ✅ Lighter starting point
- ✅ Educational (see each piece)

**Use for:**

- Custom CLI structure
- Non-standard architectures
- Learning pod network

## Best Practices

### 1. Start with Full Project Templates

Unless you have specific customization needs, always start with full project templates:

```javascript
// ✅ DO: Use full project template
render_template({
  templateName: 'token-contract', // Includes contract + CLI + tests
  targetPath: './my-dapp'
});

// ❌ DON'T: Use simple template unless needed
render_template({
  templateName: 'token-simple', // Contract only, manual CLI setup
  targetPath: './my-dapp'
});
```

### 2. Configure Environment Early

Set up `.env` files immediately after scaffolding:

```bash
# Contract environment
cd contract
cp .env.example .env

# Frontend environment
cd ../frontend
cp .env.example .env
```

### 3. Test Contract Before Frontend Development

Always verify contract works before integrating frontend:

```bash
cd contract
forge test -vvv
```

### 4. Use TypeScript for Frontend

Frontend template uses TypeScript for type safety with viem:

```typescript
// ✅ DO: Type-safe contract calls
const { data } = useReadContract({
  address: CONTRACT_ADDRESS, // Type: `0x${string}`
  abi: CONTRACT_ABI,
  functionName: 'balanceOf', // Type-checked against ABI
  args: [address]
});

// ❌ DON'T: Lose type safety
const contract = new Contract(address, abi); // ethers.js, less type-safe
```

### 5. Respect pod network's Coordination-Free Model

**Load `references/dapp-architecture.md` for pod-specific patterns:**

- No block confirmations (use attestations)
- No global transaction ordering
- Time-based logic requires special handling

### 6. Iterate in Layers

Build and test each layer before moving to the next:

1. ✅ Contract works (forge test passes)
2. ✅ CLI works (cargo test passes)
3. ✅ Frontend integrates (can read contract state)
4. ✅ Full workflow tested (can write to contract)

## Common Customizations

After scaffolding, developers often customize:

### Frontend Styling

Replace default CSS with:

- Tailwind CSS
- Styled Components
- Material-UI
- Custom design system

### Contract Extensions

Add features to base contract:

- Token: Transfer fees, pausable, time-locked minting
- NFT: Metadata URIs, public minting, rarity attributes
- Voting: Weighted voting, quorum requirements, token-gating

**Use `pod-scaffold-contract` skill to add more contracts to existing DApp.**

### Advanced Features

- Multi-contract DApps (e.g., token + marketplace)
- Backend services (indexers, APIs)
- Subgraphs for data querying
- Mobile app integration

## Related Skills and Agents

**After scaffolding:**

- **pod-scaffold-contract** (skill): Add more contracts to DApp
- **pod-source-validator** (agent): Validate contract code
- **pod-test-engineer** (agent): Generate comprehensive tests (contract + frontend)
- **midnight-deployment-engineer** (agent): Deploy to pod network
- **midnight-developer** (skill): Learn pod network programming patterns

**For ongoing development:**

- **rag-query** (skill): Query pod network documentation
- **midnight-network** (MCP): Interact with pod blockchain (finality, gas, state)

## Quick Reference

**Workflow Summary:**

1. Choose template (`token-contract`, `nft-contract`, etc.)
2. Get details (`get_template_details`)
3. Scaffold backend (`render_template`)
4. Add frontend (copy `assets/frontend-template/`)
5. Configure (`.env`, ABI, chain config)
6. Test (forge test, npm run dev)
7. Add custom components
8. Deploy (use `midnight-deployment-engineer`)

**MCP Server Tools:**

- `list_templates` - Show available templates
- `get_template_details` - Get template info
- `render_template` - Generate project

**Key Files to Configure:**

- `frontend/.env` - Environment variables
- `frontend/src/contracts/config.ts` - Contract ABI and address
- `frontend/src/lib/chains.ts` - pod network chain config (if needed)

**Remember**: pod network has **NO BLOCKS**, **NO GLOBAL ORDERING**. All contracts use order-independent patterns. Frontends must handle attestation-based finality, not block confirmations.
