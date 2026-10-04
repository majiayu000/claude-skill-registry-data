---
name: foundry-project
description: Set up and configure Foundry projects. Use when initializing new projects, configuring foundry.toml, managing dependencies, or structuring Solidity codebases.
---

# Foundry Project Setup

Initialize, configure, and manage Foundry projects.

## When to Use

- Creating new Foundry projects
- Configuring foundry.toml settings
- Managing dependencies (forge-std, OpenZeppelin, etc.)
- Setting up remappings
- Optimizing build and test settings

## Quick Start

### New Project

```bash
# Create new project
forge init my-project
cd my-project

# Create from template
forge init my-project --template https://github.com/foundry-rs/forge-template
```

### Existing Project

```bash
# Initialize in existing directory
forge init --force

# Clone and build
git clone https://github.com/some/project
cd project
forge build
```

## Project Structure

```
my-project/
├── foundry.toml          # Configuration
├── .env                  # Environment variables (gitignored)
├── .gitignore
├── README.md
├── lib/                  # Dependencies
│   └── forge-std/        # Standard library
├── script/               # Deployment scripts
│   └── Deploy.s.sol
├── src/                  # Source contracts
│   └── MyContract.sol
└── test/                 # Tests
    └── MyContract.t.sol
```

## foundry.toml Configuration

See [config.md](config.md) for all options.

### Basic Configuration

```toml
[profile.default]
src = "src"
out = "out"
libs = ["lib"]
solc = "0.8.24"
optimizer = true
optimizer_runs = 200

[profile.default.fuzz]
runs = 256

[profile.default.invariant]
runs = 256
depth = 15
```

### With RPC Endpoints

```toml
[rpc_endpoints]
mainnet = "${MAINNET_RPC_URL}"
sepolia = "${SEPOLIA_RPC_URL}"
arbitrum = "${ARBITRUM_RPC_URL}"

[etherscan]
mainnet = { key = "${ETHERSCAN_API_KEY}" }
sepolia = { key = "${ETHERSCAN_API_KEY}" }
arbitrum = { key = "${ARBISCAN_API_KEY}" }
```

### With Remappings

```toml
[profile.default]
remappings = [
    "@openzeppelin/=lib/openzeppelin-contracts/",
    "@uniswap/=lib/v3-periphery/contracts/",
    "solmate/=lib/solmate/src/"
]
```

## Dependency Management

### Install Dependencies

```bash
# Install forge-std (usually included by default)
forge install foundry-rs/forge-std

# Install OpenZeppelin
forge install OpenZeppelin/openzeppelin-contracts

# Install specific version
forge install OpenZeppelin/openzeppelin-contracts@v4.9.0

# Install without commit
forge install OpenZeppelin/openzeppelin-contracts --no-commit
```

### Update Dependencies

```bash
# Update all
forge update

# Update specific
forge update lib/openzeppelin-contracts
```

### Remove Dependencies

```bash
forge remove openzeppelin-contracts
```

### Common Dependencies

```bash
# OpenZeppelin contracts
forge install OpenZeppelin/openzeppelin-contracts

# OpenZeppelin upgradeable
forge install OpenZeppelin/openzeppelin-contracts-upgradeable

# Solmate (gas-optimized)
forge install transmissions11/solmate

# Solady (ultra-optimized)
forge install Vectorized/solady

# PRB Math (fixed-point math)
forge install PaulRBerg/prb-math

# Uniswap V3
forge install Uniswap/v3-core
forge install Uniswap/v3-periphery
```

## Remappings

### Auto-generate

```bash
# Generate remappings from lib/
forge remappings > remappings.txt
```

### Manual remappings.txt

```
forge-std/=lib/forge-std/src/
@openzeppelin/contracts/=lib/openzeppelin-contracts/contracts/
@openzeppelin/contracts-upgradeable/=lib/openzeppelin-contracts-upgradeable/contracts/
solmate/=lib/solmate/src/
```

### In foundry.toml

```toml
[profile.default]
remappings = [
    "forge-std/=lib/forge-std/src/",
    "@openzeppelin/contracts/=lib/openzeppelin-contracts/contracts/"
]
```

## Build Commands

```bash
# Build all contracts
forge build

# Build with sizes
forge build --sizes

# Clean and rebuild
forge clean && forge build

# Build specific contract
forge build --contracts src/MyContract.sol
```

## Profile Management

### Multiple Profiles

```toml
[profile.default]
optimizer = true
optimizer_runs = 200

[profile.ci]
optimizer = true
optimizer_runs = 200
fuzz = { runs = 1000 }

[profile.lite]
optimizer = false

[profile.production]
optimizer = true
optimizer_runs = 10000
via_ir = true
```

### Using Profiles

```bash
# Use CI profile
FOUNDRY_PROFILE=ci forge test

# Use production profile for deployment
FOUNDRY_PROFILE=production forge script script/Deploy.s.sol --broadcast
```

## Environment Variables

### .env File

```bash
# .env
MAINNET_RPC_URL=https://eth-mainnet.g.alchemy.com/v2/your-key
SEPOLIA_RPC_URL=https://eth-sepolia.g.alchemy.com/v2/your-key
ETHERSCAN_API_KEY=your-etherscan-key
PRIVATE_KEY=0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80
```

### Loading .env

```bash
# Load before commands
source .env && forge script script/Deploy.s.sol

# Or use dotenv in scripts
export $(cat .env | xargs) && forge test
```

### In Scripts

```solidity
contract DeployScript is Script {
    function run() public {
        uint256 deployerKey = vm.envUint("PRIVATE_KEY");
        address owner = vm.envAddress("OWNER_ADDRESS");
        string memory rpcUrl = vm.envString("RPC_URL");

        vm.startBroadcast(deployerKey);
        // ...
    }
}
```

## Common Tasks

### Run Tests

```bash
forge test                    # All tests
forge test -vvv               # With traces
forge test --match-test test_Deposit  # Specific test
forge test --watch            # Watch mode
forge test --gas-report       # Gas report
```

### Run Scripts

```bash
forge script script/Deploy.s.sol              # Dry run
forge script script/Deploy.s.sol --broadcast  # Execute
forge script script/Deploy.s.sol --verify     # Verify contracts
```

### Generate Documentation

```bash
forge doc                     # Generate docs
forge doc --serve             # Serve locally
forge doc --out docs          # Output to docs/
```

### Check Code

```bash
forge fmt                     # Format code
forge fmt --check             # Check formatting
forge snapshot                # Gas snapshot
forge snapshot --diff         # Compare with previous
```

## .gitignore

```gitignore
# Foundry
/out
/cache
/broadcast

# Environment
.env
.env.*
!.env.example

# Dependencies (if not using git submodules)
# /lib

# Coverage
lcov.info
coverage/
```

## Best Practices

1. **Pin Solidity version** in foundry.toml
2. **Use remappings** for cleaner imports
3. **Separate profiles** for CI, development, production
4. **Never commit** .env files with real keys
5. **Use forge-std** Test contract for all tests
6. **Organize tests** by contract (MyContract.t.sol)
7. **Document** with NatSpec comments
