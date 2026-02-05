---
name: pod-scaffold-contract
description: This skill should be used when developers need to generate pod network smart contract boilerplate. It orchestrates the pod-templating MCP server to scaffold production-ready contracts (tokens, NFTs, voting, auctions, basic) using FastTypes for order-independent execution. Use when starting new contracts, migrating from Ethereum, or needing pod-specific patterns.
---

# pod Scaffold Contract

Orchestrate the pod-templating MCP server to generate production-ready smart contract templates optimized for pod network's coordination-free execution model.

## Overview

This skill guides the contract scaffolding workflow using the pod-templating MCP server. Templates use FastTypes (SharedCounter, Balance, OwnedCounter, AddressSet) for order-independent operations and follow pod network best practices.

## When to Use This Skill

Trigger this skill when developers:

**Starting new contracts:**

- "Create a new token contract for pod network"
- "Generate an NFT collection contract"
- "I need a voting contract template"
- "Scaffold a basic pod network contract"

**Migrating from Ethereum:**

- "Convert my ERC20 to work on pod network"
- "Adapt my NFT contract for pod"
- "How do I implement voting on pod?"

**Need specific patterns:**

- "Create an auction contract with time-based bidding"
- "Generate a token with supply cap"
- "I need a contract with FastTypes"

## Scaffolding Workflow

### Step 1: Discover Available Templates

Use `list_templates` to show available contract templates:

```javascript
// Call pod-templating MCP server
list_templates();
```

**Available contract templates:**

| Template         | Description       | Key FastTypes             |
| ---------------- | ----------------- | ------------------------- |
| `basic-contract` | Minimal starter   | SharedCounter (example)   |
| `token-simple`   | ERC20-style token | Balance, SharedCounter    |
| `nft-simple`     | ERC721-style NFT  | SharedCounter             |
| `voting-simple`  | Voting/proposals  | AddressSet, SharedCounter |
| `auction`        | Auction system    | Balance, Time utils       |

**Full project templates (Solidity + Rust + Foundry):**

- `token-contract` - Token with CLI
- `nft-contract` - NFT with CLI
- `voting-contract` - Voting with CLI
- `notary-contract` - Notary with CLI

### Step 2: Get Template Details

Use `get_template_details` to understand template requirements:

```javascript
// Get details for a specific template
get_template_details({
  templateName: 'token-simple'
});
```

**Returns:**

- Template metadata (name, description, version)
- Required variables (contract_name, token_name, etc.)
- Optional variables with defaults
- Structure overview
- Common customizations
- Next steps

### Step 3: Collect Variable Values

Based on template details, gather required values from user:

**Example for token-simple:**

- `contract_name`: "MyToken"
- `token_name`: "My Token"
- `token_symbol`: "MTK"
- `decimals`: "18"
- `max_supply`: "1000000"
- `license` (optional): "MIT"

**Example for nft-simple:**

- `contract_name`: "MyNFT"
- `collection_name`: "My NFT Collection"
- `collection_symbol`: "MNFT"
- `max_supply`: "10000"

**Example for voting-simple:**

- `contract_name`: "ProposalVote"
- `proposal_description`: "Should we upgrade the protocol?"
- `voting_duration`: "604800" (7 days in seconds)

**Example for auction:**

- `contract_name`: "NFTAuction"
- `item_description`: "Rare NFT #123"
- `auction_duration`: "259200" (3 days in seconds)
- `reserve_price`: "1000000000000000000" (1 ETH in wei)

**Example for basic-contract:**

- `contract_name`: "MyContract"
- `license` (optional): "MIT"

### Step 4: Render Template

Use `render_template` to generate contract:

```javascript
// Render template to project directory
render_template({
  templateName: 'token-simple',
  targetPath: '/path/to/project/contracts',
  variables: {
    contract_name: 'MyToken',
    token_name: 'My Token',
    token_symbol: 'MTK',
    decimals: '18',
    max_supply: '1000000',
    license: 'MIT'
  }
});
```

**Result:**

- Contract file created at target path
- Variable substitution complete
- Ready for customization

### Step 5: Guide Next Steps

After rendering, provide guidance:

1. **Review generated contract**
   - Verify FastTypes usage
   - Check constructor parameters
   - Ensure time utilities for time-based logic

2. **Customize for use case**
   - Load `references/template-guide.md` for customization examples
   - Add project-specific logic
   - Extend with additional features

3. **Test commutativity**
   - Ensure operations work in any order
   - Test concurrent operations
   - Verify time boundary behavior

4. **Validate before deployment**
   - Use `pod-source-validator` agent to check best practices
   - Use `pod-test-engineer` agent to generate test suite
   - Run tests to verify correctness

5. **Deploy to pod network**
   - Use `midnight-deployment-engineer` agent for deployment
   - Verify finality via attestations
   - Monitor contract on pod explorer

---

## Template Selection Guide

### Choose Based on Use Case

| Need            | Template         | When to Use                  |
| --------------- | ---------------- | ---------------------------- |
| Minimal starter | `basic-contract` | Learning, custom logic       |
| Fungible token  | `token-simple`   | Currencies, points, credits  |
| NFT collection  | `nft-simple`     | Collectibles, digital assets |
| Governance      | `voting-simple`  | DAO proposals, polls         |
| Time-based sale | `auction`        | NFT auctions, bidding        |
| Full project    | `token-contract` | Need Rust CLI + Foundry      |

### Template Capabilities

**basic-contract:**

- SharedCounter example
- Owner management
- Event emissions
- Minimal boilerplate

**token-simple:**

- Balance FastType for balances
- SharedCounter for supply
- Transfer, mint, burn
- Allowances
- Supply cap

**nft-simple:**

- SharedCounter for token IDs
- Transfer, mint, burn
- Approvals (single & operator)
- Supply cap

**voting-simple:**

- AddressSet for voters
- SharedCounter for tallies
- Time-based periods
- Idempotent voting
- Finalization

**auction:**

- Balance for bids
- Time utilities
- Bid withdrawal
- Winner selection
- Reserve price

---

## Progressive Reference Loading

Load reference documents as needed for detailed guidance:

### references/template-guide.md

**Load when:**

- Need to customize templates beyond basic parameters
- Want to add specific features (transfer fees, metadata URIs, etc.)
- Combining multiple templates
- Need customization examples

**Contains:**

- Detailed customization guide for each template
- Variable replacement patterns
- Common customizations with code examples
- Integration patterns
- Best practices for combining templates

### references/fasttypes-patterns.md

**Load when:**

- Implementing custom logic with FastTypes
- Need advanced patterns (multi-currency, weighted voting, etc.)
- Want to understand FastTypes deeply
- Debugging order-dependent issues

**Contains:**

- Comprehensive FastTypes patterns
- Counter, Balance, and Set patterns
- Time-based patterns
- Combined patterns
- Anti-patterns to avoid
- Performance considerations
- Testing strategies

---

## Workflow Example

**User request**: "Create a new token contract for pod network"

**Workflow:**

1. **List templates** to show options

   ```javascript
   list_templates();
   ```

2. **Get details** for token-simple

   ```javascript
   get_template_details({ templateName: 'token-simple' });
   ```

3. **Gather variables** from user:
   - "What should the contract be called?" → "GameToken"
   - "What's the token name?" → "Game Coin"
   - "What's the symbol?" → "GAME"
   - "How many decimals?" → "18"
   - "Maximum supply? (0 for unlimited)" → "1000000"

4. **Render template**:

   ```javascript
   render_template({
     templateName: 'token-simple',
     targetPath: './contracts',
     variables: {
       contract_name: 'GameToken',
       token_name: 'Game Coin',
       token_symbol: 'GAME',
       decimals: '18',
       max_supply: '1000000'
     }
   });
   ```

5. **Guide next steps**:
   - "Contract created at ./contracts/GameToken.sol"
   - "Install pod SDK: `forge install podnetwork/pod-sdk`"
   - "Compile: `forge build`"
   - "Deploy with constructor args"
   - "See references/template-guide.md for customizations"

---

## Common Customizations

After scaffolding, developers often want to customize. Guide them to `references/template-guide.md` for detailed examples:

### Token Customizations

- Transfer fees (percentage)
- Pausable functionality
- Time-locked minting
- Snapshot for governance

### NFT Customizations

- Metadata URIs
- Public minting with payment
- Per-address limits
- Rarity attributes

### Voting Customizations

- Weighted voting
- Multiple choice
- Quorum requirements
- Token-gated voting

### Auction Customizations

- Minimum bid increments
- Automatic time extension
- Buy-now price
- Multi-item auctions

---

## Best Practices

### Always Use FastTypes

Templates use FastTypes by default. When customizing:

```solidity
// ✅ DO: Use FastTypes for shared state
SharedCounter public counter;
Balance public userBalance;
AddressSet public members;

// ❌ DON'T: Use regular variables for concurrent access
uint256 public counter;  // Race condition!
```

### Test Commutativity

Verify operations work in any order:

```javascript
// Test: A then B
await contract.functionA();
await contract.functionB();
// vs
// Test: B then A
await contract.functionB();
await contract.functionA();
// Both should produce same final state
```

### Use Time Utilities

Always use pod time utilities for consensus:

```solidity
// ✅ DO: Use time utilities
requireTimeAfter(startTime);
requireTimeBefore(endTime);

// ❌ DON'T: Use block.timestamp directly for consensus
require(block.timestamp > startTime);  // Validator-local!
```

---

## Related Skills and Agents

**After scaffolding:**

- **pod-source-validator** (agent): Validate generated contract for pod best practices
- **pod-test-engineer** (agent): Generate comprehensive test suite
- **midnight-developer** (skill): Learn pod network programming patterns
- **midnight-deployment-engineer** (agent): Deploy contract to pod network

**For ongoing development:**

- **rag-query** (skill): Query pod network documentation
- **midnight-network** (MCP): Interact with pod blockchain

---

## Quick Reference

**MCP Server Tools:**

- `list_templates` - Discover available templates
- `get_template_details` - Get template metadata and variables
- `render_template` - Generate contract with variable substitution

**Template Types:**

- Simple contracts (standalone .sol files)
- Full projects (Solidity + Rust + Foundry)

**Remember**: pod network has NO BLOCKS, NO GLOBAL ORDERING. All templates use order-independent patterns with FastTypes.
