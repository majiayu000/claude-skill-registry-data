---
name: ens-dev
description: >
  Comprehensive development support for ENS (Ethereum Name Service) including name registration,
  resolution, subdomains, smart contracts, and multichain integration. Use when building applications
  with ENS for - (1) Domain name registration and management (.eth names), (2) Name resolution (ENS
  to address, address to ENS), (3) Subdomain creation and management, (4) Avatar and profile records,
  (5) Smart contract integration with ENS, (6) Multichain resolution (L2s, sidechains), (7) Name
  Wrapper and permission management (fuses), (8) DNS integration (traditional domains on ENS), (9)
  Reverse resolution (address to name). Covers library usage (viem, ethers, wagmi), smart contract
  development (Solidity), ENS protocol architecture (Registry, Resolver, Registrar), and ENS-specific
  features like wrapped names, CCIP Read, and programmable fuses.
---

# ENS Development Support

Comprehensive toolkit for building applications with Ethereum Name Service (ENS) - the decentralized naming protocol that converts addresses into human-readable names like "vitalik.eth".

## Quick Start

### Core Concepts

ENS converts complex addresses into memorable names across the entire Web3 ecosystem. Understanding the key components is essential:

**Name Resolution Flow**:
```
ENS Name (vitalik.eth)
  ↓ Registry lookup
ENS Registry (finds resolver)
  ↓ Resolver query
Resolver Contract (returns address)
  ↓ Result
Ethereum Address (0xd8dA...)
```

**Key decision points**:
- Register .eth names → **ETH Registrar Controller** (annual registration)
- Resolve names to addresses → **Universal Resolver** (supports all resolution types)
- Create subdomains → **Registry + Resolver** (owner can create infinite subdomains)
- Add profile data → **Public Resolver** (avatars, URLs, social handles)
- Manage permissions → **Name Wrapper** (programmable ownership with fuses)
- Integrate DNS domains → **DNSSEC Oracle** (import traditional domains)
- Support L2/multichain → **CCIP Read** (ERC-3668 for offchain resolution)
- Address to name lookup → **Reverse Resolver** (.addr.reverse)

### Common Tasks

**1. Resolve ENS name to address**:
- Review [basic_resolution.ts](scripts/basic_resolution.ts) for simple name resolution
- Key points: Universal Resolver usage, normalization, error handling
- See [resolution-guide.md](references/resolution-guide.md) for advanced patterns

**2. Register .eth domain**:
- Use [registration_example.ts](scripts/registration_example.ts) for commit-reveal flow
- Alternative: Use ENS Manager App at https://ens.app for UI-based registration
- See [registration-guide.md](references/registration-guide.md) for pricing and flow details

**3. Create and manage subdomains**:
- Use [subdomain_creation.ts](scripts/subdomain_creation.ts) for programmatic subdomain creation
- Configure permissions with Name Wrapper for granular control
- See [subdomains-guide.md](references/subdomains-guide.md) for architecture patterns

**4. Set avatar and profile records**:
- Start with [profile_records.ts](scripts/profile_records.ts) for avatar, URL, social records
- Supports NFT avatars via EIP-634 format
- See [records-guide.md](references/records-guide.md) for all record types

**5. Integrate with smart contracts**:
- Use [contract_integration.sol](assets/contract-integration-template.sol) for Solidity integration
- Key pattern: Query resolver for specific record types
- See [contracts-guide.md](references/contracts-guide.md) for gas optimization

**6. Enable multichain resolution**:
- Implement [ccip_read_example.ts](scripts/ccip_read_example.ts) for L2/offchain resolution
- Test with "test.offchaindemo.eth" (resolves to 0x779981590E7Ccc0CFAe8040Ce7151324747cDb97)
- See [multichain-guide.md](references/multichain-guide.md) for CCIP Read implementation

## Core Workflows

### Name Resolution

**Basic Resolution (viem v2.35.0+)**:
```typescript
import { createPublicClient, http } from 'viem';
import { mainnet } from 'viem/chains';
import { normalize } from 'viem/ens';

// 1. Initialize client
const client = createPublicClient({
  chain: mainnet,
  transport: http()
});

// 2. Resolve name to address
const address = await client.getEnsAddress({
  name: normalize('vitalik.eth')
});
// Returns: 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045

// 3. Reverse resolution (address to name)
const name = await client.getEnsName({
  address: '0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045'
});
// Returns: vitalik.eth
```

**Advanced Resolution with Universal Resolver**:
```typescript
import { createPublicClient, http, namehash } from 'viem';
import { mainnet } from 'viem/chains';

const client = createPublicClient({
  chain: mainnet,
  transport: http()
});

// Universal Resolver address (automatically used by viem)
const UNIVERSAL_RESOLVER = '0xeEeEEEeE14D718C2B47D9923Deab1335E144EeEe';

// Resolve multiple record types
const avatar = await client.getEnsAvatar({ name: normalize('vitalik.eth') });
const text = await client.getEnsText({
  name: normalize('vitalik.eth'),
  key: 'com.twitter'
});
const contentHash = await client.getEnsText({
  name: normalize('vitalik.eth'),
  key: 'contentHash'
});
```

**With ethers.js**:
```typescript
import { ethers } from 'ethers';

const provider = new ethers.JsonRpcProvider('https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY');

// Forward resolution
const address = await provider.resolveName('vitalik.eth');

// Reverse resolution
const name = await provider.lookupAddress('0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045');

// Get resolver for advanced queries
const resolver = await provider.getResolver('vitalik.eth');
const avatar = await resolver.getAvatar();
const twitter = await resolver.getText('com.twitter');
```

See [basic_resolution.ts](scripts/basic_resolution.ts) for complete implementation.

### .eth Domain Registration

**.eth registration uses a commit-reveal pattern to prevent front-running**:

```typescript
import { createWalletClient, http, namehash } from 'viem';
import { mainnet } from 'viem/chains';
import { privateKeyToAccount } from 'viem/accounts';

const account = privateKeyToAccount('0x...');
const client = createWalletClient({
  account,
  chain: mainnet,
  transport: http()
});

// Contract addresses
const ETH_REGISTRAR_CONTROLLER = '0x59E16fcCd424Cc24e280Be16E11Bcd56fb0CE547';

// 1. Check name availability
const name = 'myname';
const available = await publicClient.readContract({
  address: ETH_REGISTRAR_CONTROLLER,
  abi: registrarAbi,
  functionName: 'available',
  args: [name]
});

if (!available) throw new Error('Name not available');

// 2. Make commitment
const commitment = await publicClient.readContract({
  address: ETH_REGISTRAR_CONTROLLER,
  abi: registrarAbi,
  functionName: 'makeCommitment',
  args: [name, account.address, duration, secret, resolver, [], false, 0]
});

const commitTx = await client.writeContract({
  address: ETH_REGISTRAR_CONTROLLER,
  abi: registrarAbi,
  functionName: 'commit',
  args: [commitment]
});

// 3. Wait minimum 60 seconds (anti-front-running)
await new Promise(resolve => setTimeout(resolve, 60000));

// 4. Register name (requires ETH payment)
const price = await publicClient.readContract({
  address: ETH_REGISTRAR_CONTROLLER,
  abi: registrarAbi,
  functionName: 'rentPrice',
  args: [name, duration]
});

const registerTx = await client.writeContract({
  address: ETH_REGISTRAR_CONTROLLER,
  abi: registrarAbi,
  functionName: 'register',
  args: [name, account.address, duration, secret, resolver, [], false, 0],
  value: price.base + price.premium
});
```

**Pricing (as of ENSv2)**:
- 5+ characters: $5/year
- 4 characters: $160/year
- 3 characters: $640/year

**Grace Period**: 90 days after expiration with 21-day declining premium

See [registration_example.ts](scripts/registration_example.ts) for complete flow.

### Subdomain Creation & Management

**Creating Subdomains (Domain Owner)**:
```typescript
import { createWalletClient, http, namehash } from 'viem';
import { mainnet } from 'viem/chains';

const client = createWalletClient({
  account,
  chain: mainnet,
  transport: http()
});

const ENS_REGISTRY = '0x00000000000C2E074eC69A0dFb2997BA6C7d2e1e';
const PUBLIC_RESOLVER = '0xF29100983E058B709F3D539b0c765937B804AC15';

// 1. Create subdomain (you must own parent domain)
const parentNode = namehash('mydomain.eth');
const label = 'sub'; // Creates sub.mydomain.eth
const labelHash = keccak256(toBytes(label));

// Set subdomain owner in registry
await client.writeContract({
  address: ENS_REGISTRY,
  abi: registryAbi,
  functionName: 'setSubnodeOwner',
  args: [parentNode, labelHash, newOwnerAddress]
});

// 2. Configure resolver for subdomain
const subdomainNode = namehash('sub.mydomain.eth');

await client.writeContract({
  address: ENS_REGISTRY,
  abi: registryAbi,
  functionName: 'setResolver',
  args: [subdomainNode, PUBLIC_RESOLVER]
});

// 3. Set address record in resolver
await client.writeContract({
  address: PUBLIC_RESOLVER,
  abi: resolverAbi,
  functionName: 'setAddr',
  args: [subdomainNode, targetAddress]
});
```

**Using Name Wrapper for Permission Control**:
```typescript
const NAME_WRAPPER = '0xD4416b13d2b3a9aBae7AcD5D6C2BbDBE25686401';

// Wrap name to enable fuses
await client.writeContract({
  address: NAME_WRAPPER,
  abi: wrapperAbi,
  functionName: 'wrapETH2LD',
  args: ['mydomain', account.address, 0, ethers.ZeroAddress]
});

// Create subdomain with custom permissions
const PARENT_CANNOT_CONTROL = 1 << 16; // Parent can't modify
const CANNOT_TRANSFER = 1 << 1; // Name can't be transferred

await client.writeContract({
  address: NAME_WRAPPER,
  abi: wrapperAbi,
  functionName: 'setSubnodeOwner',
  args: [
    parentNode,
    'sub',
    newOwner,
    PARENT_CANNOT_CONTROL | CANNOT_TRANSFER,
    expiry
  ]
});
```

See [subdomain_creation.ts](scripts/subdomain_creation.ts) for production patterns.

### Avatar & Profile Records

**Setting Profile Records**:
```typescript
import { createWalletClient, http, namehash } from 'viem';

const PUBLIC_RESOLVER = '0xF29100983E058B709F3D539b0c765937B804AC15';

const node = namehash('myname.eth');

// 1. Set avatar (supports multiple formats)
// NFT avatar: eip155:1/erc721:0x... or eip155:1/erc1155:0x.../1
await client.writeContract({
  address: PUBLIC_RESOLVER,
  abi: resolverAbi,
  functionName: 'setText',
  args: [node, 'avatar', 'eip155:1/erc721:0xb7F7F6C52F2e2fdb1963Eab30438024864c313F6/2430']
});

// IPFS avatar: ipfs://...
await client.writeContract({
  address: PUBLIC_RESOLVER,
  abi: resolverAbi,
  functionName: 'setText',
  args: [node, 'avatar', 'ipfs://QmY...']
});

// 2. Set social records
const records = {
  'com.twitter': 'vitalikbuterin',
  'com.github': 'vbuterin',
  'url': 'https://vitalik.eth.limo',
  'email': 'vitalik@ethereum.org',
  'description': 'Ethereum co-founder'
};

for (const [key, value] of Object.entries(records)) {
  await client.writeContract({
    address: PUBLIC_RESOLVER,
    abi: resolverAbi,
    functionName: 'setText',
    args: [node, key, value]
  });
}

// 3. Set content hash (for decentralized websites)
await client.writeContract({
  address: PUBLIC_RESOLVER,
  abi: resolverAbi,
  functionName: 'setContenthash',
  args: [node, contentHash] // IPFS or Swarm hash
});

// 4. Set multiple coin addresses (multichain)
// Ethereum (coinType: 60)
await client.writeContract({
  address: PUBLIC_RESOLVER,
  abi: resolverAbi,
  functionName: 'setAddr',
  args: [node, 60, ethAddressBytes]
});

// Bitcoin (coinType: 0)
await client.writeContract({
  address: PUBLIC_RESOLVER,
  abi: resolverAbi,
  functionName: 'setAddr',
  args: [node, 0, btcAddressBytes]
});
```

See [profile_records.ts](scripts/profile_records.ts) for all record types.

### Smart Contract Integration

**Query ENS in Solidity**:
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

interface IENSRegistry {
    function resolver(bytes32 node) external view returns (address);
}

interface IResolver {
    function addr(bytes32 node) external view returns (address);
}

contract ENSIntegration {
    IENSRegistry public immutable ens;

    constructor(address _ens) {
        ens = IENSRegistry(_ens);
    }

    function resolve(bytes32 node) public view returns (address) {
        address resolver = ens.resolver(node);
        if (resolver == address(0)) return address(0);

        return IResolver(resolver).addr(node);
    }

    function sendToENSName(bytes32 node) external payable {
        address recipient = resolve(node);
        require(recipient != address(0), "ENS name not found");

        (bool success, ) = recipient.call{value: msg.value}("");
        require(success, "Transfer failed");
    }
}
```

**Using @ensdomains/ens-contracts package**:
```solidity
pragma solidity ^0.8.19;

import "@ensdomains/ens-contracts/contracts/registry/ENS.sol";
import "@ensdomains/ens-contracts/contracts/resolvers/PublicResolver.sol";

contract MyContract {
    ENS public ens;

    constructor(ENS _ens) {
        ens = _ens;
    }

    function getAddress(bytes32 node) public view returns (address) {
        address resolverAddr = ens.resolver(node);
        if (resolverAddr == address(0)) return address(0);

        PublicResolver resolver = PublicResolver(resolverAddr);
        return resolver.addr(node);
    }
}
```

See [contract_integration.sol](assets/contract-integration-template.sol) for production template.

### Multichain Resolution (CCIP Read)

**CCIP Read (ERC-3668) for L2 and Offchain Resolution**:

```typescript
import { createPublicClient, http } from 'viem';
import { mainnet } from 'viem/chains';

const client = createPublicClient({
  chain: mainnet,
  transport: http(),
  // CCIP Read is automatically supported in viem 2.35.0+
});

// Resolve L2/offchain ENS name
const address = await client.getEnsAddress({
  name: normalize('test.offchaindemo.eth')
});
// Should resolve to: 0x779981590E7Ccc0CFAe8040Ce7151324747cDb97
// even though data is stored on L2 or offchain

// Query offchain text records
const twitter = await client.getEnsText({
  name: normalize('l2name.eth'),
  key: 'com.twitter'
});
```

**Implementing Custom CCIP Read Resolver**:
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

interface IOffchainResolver {
    error OffchainLookup(
        address sender,
        string[] urls,
        bytes callData,
        bytes4 callbackFunction,
        bytes extraData
    );

    function resolve(bytes calldata name, bytes calldata data)
        external
        view
        returns (bytes memory);
}

contract CCIPReadResolver is IOffchainResolver {
    string[] public urls;

    constructor(string[] memory _urls) {
        urls = _urls;
    }

    function resolve(bytes calldata name, bytes calldata data)
        external
        view
        returns (bytes memory)
    {
        revert OffchainLookup(
            address(this),
            urls,
            data,
            this.resolveWithProof.selector,
            abi.encode(name, data)
        );
    }

    function resolveWithProof(bytes calldata response, bytes calldata extraData)
        external
        view
        returns (bytes memory)
    {
        // Verify offchain data and return result
        // Implementation depends on your L2/offchain storage
    }
}
```

See [ccip_read_example.ts](scripts/ccip_read_example.ts) for complete implementation.

## Critical Security Requirements

**Never deploy without**:

1. **Name Normalization**: Always use UTS-46 normalization before processing names
2. **Input Validation**: Validate ENS names match expected format (no homograph attacks)
3. **Address Verification**: Display both name AND address in transaction UIs
4. **Resolver Verification**: Check resolver is trusted before using its data
5. **Expiry Checks**: Verify name hasn't expired before critical operations
6. **Reverse Record Validation**: Confirm reverse record matches forward resolution
7. **CCIP Read Security**: Validate offchain data signatures and sources
8. **Private Key Protection**: Never expose private keys when setting records

**UI Best Practices**:
- Show both "vitalik.eth" AND "0xd8d..." in transaction confirmations
- Implement debouncing for ENS input fields (300-500ms)
- Display warning if name will expire soon (<30 days)
- Check reverse record is set before displaying name in place of address

See [security.md](references/security.md) for complete checklist.

## Architecture Patterns

### ENS Protocol Architecture

```
┌─────────────────────────────────────────────┐
│           Application Layer                  │
│  (Your dApp, Wallet, Smart Contract)        │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│        Universal Resolver (v2)              │
│  (Handles all resolution, CCIP Read)        │
└─────────────────┬───────────────────────────┘
                  │
      ┌───────────┴───────────┐
      │                       │
┌─────▼─────────┐    ┌────────▼────────┐
│  ENS Registry │    │   Resolvers     │
│  (Ownership)  │    │  (Data Storage) │
└─────┬─────────┘    └────────┬────────┘
      │                       │
┌─────▼─────────────────────┬─▼────────┐
│  Registrars               │  Records │
│  (.eth, DNS, etc.)       │  (Addr,   │
│                           │   Text,   │
│  Name Wrapper             │   Content)│
│  (Permissions/Fuses)      │           │
└───────────────────────────┴───────────┘
```

### Name States & Wrapped Names

**Unwrapped → Wrapped → Emancipated → Locked**:

1. **Unwrapped**: Traditional ENS ownership (mutable, no fuses)
2. **Wrapped**: Converted to ERC-1155 NFT (fuses can be set)
3. **Emancipated**: Parent cannot control (PARENT_CANNOT_CONTROL burned)
4. **Locked**: Name locked permanently (CANNOT_UNWRAP burned)

**Fuse Types**:
- **Parent-Controlled**: Grant "perks" (e.g., CAN_EXTEND_EXPIRY)
- **Owner-Controlled**: Restrict "permissions" (e.g., CANNOT_TRANSFER)

See [name-wrapper-guide.md](references/name-wrapper-guide.md) for complete fuse reference.

### Resolution Flow

```typescript
// Modern approach with Universal Resolver (automatically handles all cases)
const address = await client.getEnsAddress({ name: normalize('name.eth') });

// Traditional approach (manual registry + resolver lookup)
const registry = getContract({ address: ENS_REGISTRY, abi: registryAbi, client });
const resolverAddress = await registry.read.resolver([namehash('name.eth')]);
const resolver = getContract({ address: resolverAddress, abi: resolverAbi, client });
const address = await resolver.read.addr([namehash('name.eth')]);
```

## Development Setup

### Dependencies

**For TypeScript/JavaScript**:
```bash
# viem (recommended for ENSv2)
npm install viem

# ethers.js (v6+)
npm install ethers

# wagmi (for React)
npm install wagmi viem

# ENS contracts (for Solidity integration)
npm install @ensdomains/ens-contracts

# ENS utilities
npm install @ensdomains/ensjs
```

**For Solidity**:
```bash
# Foundry
forge install ensdomains/ens-contracts

# Hardhat
npm install @ensdomains/ens-contracts
```

### Contract Addresses

**Mainnet**:
- ENS Registry: `0x00000000000C2E074eC69A0dFb2997BA6C7d2e1e`
- Base Registrar (.eth): `0x57f1887a8BF19b14fC0dF6Fd9B2acc9Af147eA85`
- ETH Registrar Controller: `0x59E16fcCd424Cc24e280Be16E11Bcd56fb0CE547`
- Public Resolver: `0xF29100983E058B709F3D539b0c765937B804AC15`
- Universal Resolver: `0xeEeEEEeE14D718C2B47D9923Deab1335E144EeEe`
- Name Wrapper: `0xD4416b13d2b3a9aBae7AcD5D6C2BbDBE25686401`
- Reverse Registrar: `0xa58E81fe9b61B5c3fE2AFD33CF304c454AbFc7Cb`

**Sepolia Testnet**:
- ENS Registry: `0x00000000000C2E074eC69A0dFb2997BA6C7d2e1e`
- ETH Registrar Controller: `0xfb3cE5D01e0f33f41DbB39035dB9745962F1f968`
- Public Resolver: `0xE99638b40E4Fff0129D56f03b55b6bbC4BBE49b5`

See [deployments.md](references/deployments.md) for complete list.

### React Integration (wagmi)

```typescript
import { useEnsAddress, useEnsAvatar, useEnsName } from 'wagmi';
import { normalize } from 'viem/ens';

function ENSProfile({ name }: { name: string }) {
  const { data: address } = useEnsAddress({ name: normalize(name) });
  const { data: avatar } = useEnsAvatar({ name: normalize(name) });
  const { data: ensName } = useEnsName({ address });

  return (
    <div>
      <img src={avatar} alt={name} />
      <p>{name} → {address}</p>
      <p>Reverse: {ensName}</p>
    </div>
  );
}
```

## Testing

### Library Testing (TypeScript)

```typescript
import { expect } from 'chai';
import { createPublicClient, http } from 'viem';
import { mainnet } from 'viem/chains';
import { normalize } from 'viem/ens';

describe('ENS Resolution', () => {
  const client = createPublicClient({
    chain: mainnet,
    transport: http()
  });

  it('should resolve vitalik.eth correctly', async () => {
    const address = await client.getEnsAddress({
      name: normalize('vitalik.eth')
    });

    expect(address).to.equal('0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045');
  });

  it('should handle reverse resolution', async () => {
    const name = await client.getEnsName({
      address: '0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045'
    });

    expect(name).to.equal('vitalik.eth');
  });
});
```

### Smart Contract Testing (Foundry)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "forge-std/Test.sol";
import "@ensdomains/ens-contracts/contracts/registry/ENS.sol";
import "@ensdomains/ens-contracts/contracts/resolvers/PublicResolver.sol";

contract ENSIntegrationTest is Test {
    ENS ens;
    PublicResolver resolver;

    function setUp() public {
        // Fork mainnet
        vm.createSelectFork(vm.envString("ETH_RPC_URL"));

        ens = ENS(0x00000000000C2E074eC69A0dFb2997BA6C7d2e1e);
        resolver = PublicResolver(0xF29100983E058B709F3D539b0c765937B804AC15);
    }

    function testResolveVitalik() public view {
        bytes32 node = 0xee6c4522aab0003e8d14cd40a6af439055fd2577951148c14b6cea9a53475835;

        address resolverAddr = ens.resolver(node);
        assertEq(resolverAddr, address(resolver));

        address addr = PublicResolver(resolverAddr).addr(node);
        assertEq(addr, 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045);
    }
}
```

## Common Pitfalls

1. **Missing Normalization**: Always normalize names with UTS-46 before hashing
2. **Direct Registry Queries**: Use Universal Resolver instead of manual registry lookups
3. **Hardcoded Resolver**: Don't assume Public Resolver - always query from registry
4. **Namehash Errors**: Use library functions for namehash - manual implementation is error-prone
5. **Reverse Record Assumptions**: Not all addresses have reverse records set
6. **Expiry Ignorance**: Check expiry before trusting resolution in critical paths
7. **CCIP Read Timeout**: Offchain resolution can be slow - implement proper timeout handling
8. **Homograph Attacks**: Validate input to prevent look-alike character exploitation
9. **Missing ENSv2 Support**: Update to viem 2.35.0+ or ethers v6+ for Universal Resolver
10. **Gas Optimization**: Batch resolver queries when fetching multiple records

## ENSv2 Migration Checklist

**For App Developers**:
- ✅ Update viem to v2.35.0+ or ethers to v6+
- ✅ Use Universal Resolver (automatic with updated libraries)
- ✅ Test with "test.offchaindemo.eth" for CCIP Read support
- ✅ Handle CCIP Read timeouts gracefully
- ✅ Display both name and address in UIs

**For Resolver Developers**:
- ✅ Implement ERC-3668 (CCIP Read) for offchain data
- ✅ Support wildcard resolution if needed
- ✅ Add proper signature verification for offchain responses
- ✅ Test with Universal Resolver

**For Subname Operators**:
- ✅ Consider wrapping names for permission management
- ✅ Set appropriate fuses for subdomain distribution
- ✅ Document subdomain expiry policies
- ✅ Implement subdomain marketplace if needed

## Resources

### Official Documentation
- **Main Docs**: https://docs.ens.domains/
- **Protocol Overview**: https://docs.ens.domains/learn/protocol
- **Deployments**: https://docs.ens.domains/learn/deployments
- **FAQ**: https://docs.ens.domains/faq
- **LLM Context**: https://docs.ens.domains/llms-full.txt

### Code Repositories
- **ENS Contracts**: https://github.com/ensdomains/ens-contracts
- **ENS App v3**: https://github.com/ensdomains/ens-app-v3
- **ENS Docs**: https://github.com/ensdomains/docs
- **Main GitHub**: https://github.com/ensdomains

### Tools & Services
- **ENS Manager**: https://ens.app (register and manage names)
- **ENSv2 Info**: https://ens.domains/ensv2
- **Main Site**: https://ens.domains/

### Support
- **Bug Bounty**: Immunefi - up to $250K for critical bugs
- **GitHub Issues**: https://github.com/ensdomains/ens-contracts/issues
- **Documentation Issues**: https://github.com/ensdomains/docs/issues

## Bundled Resources

### Scripts
- **[basic_resolution.ts](scripts/basic_resolution.ts)**: Complete name resolution examples
- **[registration_example.ts](scripts/registration_example.ts)**: .eth domain registration flow
- **[subdomain_creation.ts](scripts/subdomain_creation.ts)**: Subdomain creation and management
- **[profile_records.ts](scripts/profile_records.ts)**: Avatar and profile record management
- **[ccip_read_example.ts](scripts/ccip_read_example.ts)**: Multichain/L2 resolution implementation

### References
- **[resolution-guide.md](references/resolution-guide.md)**: Complete resolution patterns
- **[registration-guide.md](references/registration-guide.md)**: Registration pricing and process
- **[subdomains-guide.md](references/subdomains-guide.md)**: Subdomain architecture patterns
- **[records-guide.md](references/records-guide.md)**: All record types and formats
- **[contracts-guide.md](references/contracts-guide.md)**: Smart contract integration patterns
- **[multichain-guide.md](references/multichain-guide.md)**: CCIP Read and L2 resolution
- **[name-wrapper-guide.md](references/name-wrapper-guide.md)**: Name Wrapper and fuse reference
- **[security.md](references/security.md)**: Security best practices
- **[deployments.md](references/deployments.md)**: All contract addresses

### Assets
- **[contract-integration-template.sol](assets/contract-integration-template.sol)**: Production Solidity template
- **[resolver-implementation.sol](assets/resolver-implementation.sol)**: Custom resolver template

## Support Context7 Integration

When the user needs up-to-date documentation or specific implementation details:

1. Use ENS official docs as primary source: https://docs.ens.domains/
2. For smart contract details: @ensdomains/ens-contracts on GitHub
3. For library-specific questions: Use Context7 with viem or ethers.js
4. Combine Context7 results with this skill's security guidelines

Example:
```
User: "How do I implement wildcard resolution?"
→ Check ENS docs for EIP-2544 (wildcard resolution)
→ Use Context7: query-docs with "@ensdomains/ens-contracts" for contract examples
→ Apply security patterns from security.md
```

## Name Wrapper Fuse Reference

### Owner-Controlled Fuses (Restrict Permissions)

- `CANNOT_UNWRAP` (0x01): Prevent unwrapping to traditional ENS
- `CANNOT_BURN_FUSES` (0x02): No more fuses can be burned
- `CANNOT_TRANSFER` (0x04): Name cannot be transferred
- `CANNOT_SET_RESOLVER` (0x08): Resolver cannot be changed
- `CANNOT_SET_TTL` (0x10): TTL cannot be modified
- `CANNOT_CREATE_SUBDOMAIN` (0x20): Cannot create new subdomains
- `CANNOT_APPROVE` (0x40): Cannot approve name transfers

### Parent-Controlled Fuses (Grant Perks)

- `PARENT_CANNOT_CONTROL` (0x10000): Parent loses control (emancipation)
- `CAN_EXTEND_EXPIRY` (0x40000): Subdomain owner can extend expiry

### Common Fuse Patterns

**Locked Forever**:
```typescript
const LOCKED = CANNOT_UNWRAP | CANNOT_BURN_FUSES | PARENT_CANNOT_CONTROL;
```

**Transferable but Locked**:
```typescript
const TRANSFERABLE_LOCKED = CANNOT_UNWRAP | CANNOT_BURN_FUSES;
```

**Fully Controlled Subdomain**:
```typescript
const EMANCIPATED = PARENT_CANNOT_CONTROL | CAN_EXTEND_EXPIRY;
```

## DNS Integration

ENS supports importing traditional DNS domains via DNSSEC:

**Supported TLDs**: .com, .org, .net, .io, .app, and 200+ more

**Integration Flow**:
1. Add DNSSEC to your DNS domain
2. Create TXT record: `_ens.yourdomain.com` → `a=0xYourAddress`
3. Import to ENS via Manager App or contract call
4. Manage DNS domain like native .eth name

**Benefits**:
- Use existing domain on ENS
- Full ENS feature support (records, subdomains, etc.)
- Bridge Web2 and Web3 identity

See ENS documentation for complete DNSSEC setup guide.
