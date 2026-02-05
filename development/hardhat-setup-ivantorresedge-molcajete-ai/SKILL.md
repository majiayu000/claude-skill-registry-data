---
name: hardhat-setup
description: Templates and automation for initializing and configuring Hardhat projects. Use when setting up new Hardhat projects or adding Hardhat to existing codebases.
---

# Hardhat Setup Skill

This skill provides templates, scripts, and best practices for setting up Hardhat-based Solidity projects.

## When to Use

Use this skill when:
- Initializing a new Hardhat project
- Adding Hardhat to an existing Solidity codebase
- Configuring Hardhat settings (networks, plugins, etc.)
- Setting up Hardhat in a hybrid Foundry/Hardhat project
- Updating Hardhat configuration

**Prerequisites:** Node.js and npm/yarn/pnpm must be installed

## Integration with Framework Detection

Before using this skill, reference the `framework-detection` skill to:
- Check if Hardhat is already configured
- Determine if this is a hybrid setup
- Avoid overwriting existing configuration

## Quick Setup

### Basic Initialization

```bash
# Initialize new Hardhat project
npm init -y
npm install --save-dev hardhat
npx hardhat init

# Or with yarn
yarn init -y
yarn add --dev hardhat
npx hardhat init
```

### Project Structure

Hardhat creates this structure:

```
project/
├── hardhat.config.js     # Configuration
├── .env                  # Environment variables
├── package.json          # Dependencies
├── contracts/            # Contract source files
│   └── Lock.sol          # Example contract
├── test/                 # Test files
│   └── Lock.js           # Example test
├── scripts/              # Deployment scripts
│   └── deploy.js         # Example script
└── ignition/             # Hardhat Ignition (deployment modules)
```

## Configuration Templates

### hardhat.config.js

See `./templates/hardhat.config.js` for JavaScript configuration template.

**Key Configuration Sections:**

```javascript
require("@nomicfoundation/hardhat-toolbox");
require("dotenv").config();

module.exports = {
  solidity: {
    version: "0.8.30",
    settings: {
      optimizer: {
        enabled: true,
        runs: 200
      }
    }
  },
  networks: {
    hardhat: {},
    sepolia: {
      url: process.env.SEPOLIA_RPC_URL || "",
      accounts: process.env.PRIVATE_KEY ? [process.env.PRIVATE_KEY] : []
    }
  },
  etherscan: {
    apiKey: process.env.ETHERSCAN_API_KEY
  }
};
```

### hardhat.config.ts

See `./templates/hardhat.config.ts` for TypeScript configuration template.

**TypeScript Configuration:**

```typescript
import { HardhatUserConfig } from "hardhat/config";
import "@nomicfoundation/hardhat-toolbox";
import "dotenv/config";

const config: HardhatUserConfig = {
  solidity: "0.8.30",
  networks: {
    sepolia: {
      url: process.env.SEPOLIA_RPC_URL || "",
      accounts: process.env.PRIVATE_KEY ? [process.env.PRIVATE_KEY] : []
    }
  }
};

export default config;
```

### Environment Variables

See `./templates/.env.example` for complete environment variable template.

**Essential Variables:**

```bash
# RPC URLs
MAINNET_RPC_URL=
SEPOLIA_RPC_URL=

# Private Keys (NEVER commit actual keys)
PRIVATE_KEY=

# Etherscan API Keys
ETHERSCAN_API_KEY=

# Gas Settings
GAS_PRICE=
```

## Essential Plugins

### Hardhat Toolbox (Recommended)

Includes all essential plugins:

```bash
npm install --save-dev @nomicfoundation/hardhat-toolbox
```

**Includes:**
- `@nomicfoundation/hardhat-ethers` - Ethers.js integration
- `@nomicfoundation/hardhat-chai-matchers` - Chai matchers for testing
- `@nomicfoundation/hardhat-verify` - Contract verification
- `hardhat-gas-reporter` - Gas usage reporting
- `solidity-coverage` - Code coverage
- `@typechain/hardhat` - TypeScript types for contracts

### Individual Plugins

```bash
# Contract verification
npm install --save-dev @nomicfoundation/hardhat-verify

# Gas reporting
npm install --save-dev hardhat-gas-reporter

# Code coverage
npm install --save-dev solidity-coverage

# OpenZeppelin Upgrades
npm install --save-dev @openzeppelin/hardhat-upgrades
```

## Common Configurations

### 1. Multiple Networks

```javascript
networks: {
  mainnet: {
    url: process.env.MAINNET_RPC_URL,
    accounts: [process.env.PRIVATE_KEY],
    chainId: 1
  },
  sepolia: {
    url: process.env.SEPOLIA_RPC_URL,
    accounts: [process.env.PRIVATE_KEY],
    chainId: 11155111
  },
  arbitrum: {
    url: process.env.ARBITRUM_RPC_URL,
    accounts: [process.env.PRIVATE_KEY],
    chainId: 42161
  }
}
```

### 2. High Optimization for Production

```javascript
solidity: {
  version: "0.8.30",
  settings: {
    optimizer: {
      enabled: true,
      runs: 10000
    },
    viaIR: true
  }
}
```

### 3. Multiple Solidity Versions

```javascript
solidity: {
  compilers: [
    {
      version: "0.8.30",
      settings: {
        optimizer: { enabled: true, runs: 200 }
      }
    },
    {
      version: "0.8.20",
      settings: {
        optimizer: { enabled: true, runs: 200 }
      }
    }
  ]
}
```

### 4. Gas Reporter Configuration

```javascript
gasReporter: {
  enabled: process.env.REPORT_GAS === "true",
  currency: "USD",
  coinmarketcap: process.env.COINMARKETCAP_API_KEY,
  outputFile: "gas-report.txt",
  noColors: true
}
```

## Dependencies Management

### Installing OpenZeppelin

```bash
# OpenZeppelin Contracts
npm install @openzeppelin/contracts

# OpenZeppelin Upgrades Plugin
npm install --save-dev @openzeppelin/hardhat-upgrades
```

### Installing Common Libraries

```bash
# Ethers.js (usually included with hardhat-toolbox)
npm install ethers

# Chai for testing
npm install --save-dev chai

# Dotenv for environment variables
npm install --save-dev dotenv
```

## Initialization Script

See `./scripts/init-hardhat.sh` for automated setup.

**Usage:**

```bash
# Basic initialization
./scripts/init-hardhat.sh

# With project name
./scripts/init-hardhat.sh my-project

# With TypeScript
./scripts/init-hardhat.sh my-project --typescript
```

**What the script does:**
1. Checks if Node.js is installed
2. Initializes npm/yarn project
3. Installs Hardhat and essential plugins
4. Creates configuration files
5. Sets up .gitignore
6. Installs OpenZeppelin contracts
7. Creates example contract and test

## Hybrid Setup (Hardhat + Foundry)

When adding Hardhat to an existing Foundry project:

### 1. Initialize Hardhat Without Overwriting

```bash
# Initialize npm project
npm init -y

# Install Hardhat
npm install --save-dev hardhat
npx hardhat init  # Choose "Create an empty hardhat.config.js"
```

### 2. Configure Shared Directories

```javascript
// hardhat.config.js
module.exports = {
  paths: {
    sources: "./src",      // Use Foundry's src dir
    tests: "./test",       // Shared test dir
    cache: "./cache_hardhat",  // Separate cache
    artifacts: "./artifacts"
  },
  solidity: "0.8.30"
};
```

### 3. Update .gitignore

```gitignore
# Hardhat
artifacts/
cache/
cache_hardhat/
node_modules/
coverage/
coverage.json
typechain-types/

# Foundry
out/
lib/

# Environment
.env
.env.local
```

### 4. Shared Dependencies

```bash
# Install OpenZeppelin via npm (for Hardhat)
npm install @openzeppelin/contracts

# Foundry can reference node_modules
# Add to foundry.toml:
# libs = ["node_modules", "lib"]
```

## Testing Setup

### Basic Test Structure (JavaScript)

```javascript
const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("MyContract", function () {
  let myContract;
  let owner;

  beforeEach(async function () {
    [owner] = await ethers.getSigners();
    const MyContract = await ethers.getContractFactory("MyContract");
    myContract = await MyContract.deploy();
  });

  it("Should work correctly", async function () {
    // Test implementation
    expect(await myContract.someFunction()).to.equal(expectedValue);
  });
});
```

### Basic Test Structure (TypeScript)

```typescript
import { expect } from "chai";
import { ethers } from "hardhat";
import { MyContract } from "../typechain-types";

describe("MyContract", function () {
  let myContract: MyContract;

  beforeEach(async function () {
    const MyContract = await ethers.getContractFactory("MyContract");
    myContract = await MyContract.deploy();
  });

  it("Should work correctly", async function () {
    expect(await myContract.someFunction()).to.equal(expectedValue);
  });
});
```

### Running Tests

```bash
# Run all tests
npx hardhat test

# Run specific test
npx hardhat test test/MyContract.test.js

# With gas reporting
REPORT_GAS=true npx hardhat test

# With coverage
npx hardhat coverage
```

## Security Best Practices for Private Keys

⚠️ **CRITICAL: Never store production private keys in .env files!**

### Recommended Approaches (in order of preference)

#### 1. Hardware Wallets (Most Secure - Production)

Install the Ledger plugin:

```bash
npm install --save-dev @nomicfoundation/hardhat-ledger
```

Configure in `hardhat.config.js`:

```javascript
require("@nomicfoundation/hardhat-ledger");

module.exports = {
  networks: {
    mainnet: {
      url: process.env.MAINNET_RPC_URL,
      ledgerAccounts: [
        "0xYourLedgerAddress"
      ]
    }
  }
};
```

Deploy with Ledger:

```bash
npx hardhat run scripts/deploy.js --network mainnet
```

#### 2. Hardhat Configuration Variables (Recommended - Built-in)

Hardhat 2.x+ includes built-in support for secure configuration variables:

```bash
# Set a configuration variable (prompts for value, stores encrypted)
npx hardhat vars set PRIVATE_KEY

# List all configuration variables
npx hardhat vars list

# Delete a variable
npx hardhat vars delete PRIVATE_KEY
```

Use in `hardhat.config.js`:

```javascript
const { vars } = require("hardhat/config");

module.exports = {
  networks: {
    sepolia: {
      url: vars.get("SEPOLIA_RPC_URL"),
      accounts: [vars.get("PRIVATE_KEY")]
    }
  }
};
```

This stores encrypted values in your home directory and prompts for decryption when needed.

#### 3. hardhat-keystore Plugin (Encrypted Keystore)

Similar to Foundry's `cast wallet`, provides encrypted keystore management:

```bash
npm install --save-dev hardhat-keystore
```

Configure in `hardhat.config.js`:

```javascript
require("hardhat-keystore");

module.exports = {
  networks: {
    sepolia: {
      url: process.env.SEPOLIA_RPC_URL,
      accounts: {
        mnemonic: keystore.getMnemonic(),
        // or
        privateKey: keystore.getPrivateKey("deployer")
      }
    }
  }
};
```

#### 4. hardhat-secure-accounts Plugin (Third-Party Alternative)

```bash
npm install --save-dev hardhat-secure-accounts
```

Creates encrypted keystore files:

```bash
# Create new encrypted account
npx hardhat accounts:create

# Import existing private key
npx hardhat accounts:import --name deployer
```

Use in scripts:

```javascript
const { getSecureAccount } = require("hardhat-secure-accounts");

async function main() {
  const signer = await getSecureAccount("deployer");
  // Use signer for deployment
}
```

#### 5. Interactive Environment Variable (Development Only)

Prompt for private key at runtime (doesn't store on disk):

```javascript
const readline = require("readline");

async function getPrivateKey() {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  return new Promise((resolve) => {
    rl.question("Enter private key: ", (answer) => {
      rl.close();
      resolve(answer);
    });
  });
}

async function main() {
  const privateKey = await getPrivateKey();
  const wallet = new ethers.Wallet(privateKey, ethers.provider);
  // Use wallet for deployment
}
```

#### 6. .env Variables (Development/Testing ONLY)

⚠️ **Use ONLY for local development or testnet testing with non-production keys!**

```javascript
require("dotenv").config();

module.exports = {
  networks: {
    sepolia: {
      url: process.env.SEPOLIA_RPC_URL,
      accounts: process.env.PRIVATE_KEY ? [process.env.PRIVATE_KEY] : []
    }
  }
};
```

**If using .env:**
- ✅ Only use accounts created specifically for development/testing
- ✅ Never reuse production private keys
- ✅ Keep test funds minimal
- ✅ Add .env to .gitignore
- ❌ Never commit .env to version control
- ❌ Never use for mainnet deployments

## Deployment Setup

### Basic Deployment Script

```javascript
// scripts/deploy.js
const hre = require("hardhat");

async function main() {
  const MyContract = await hre.ethers.getContractFactory("MyContract");
  const myContract = await MyContract.deploy();
  await myContract.waitForDeployment();

  console.log("MyContract deployed to:", await myContract.getAddress());
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
```

### Deploy Commands

```bash
# Deploy to local network
npx hardhat run scripts/deploy.js

# Deploy to Sepolia with hardware wallet (RECOMMENDED for production)
npx hardhat run scripts/deploy.js --network sepolia
# (Ledger will prompt for approval)

# Deploy to Sepolia with Hardhat vars (RECOMMENDED for all deployments)
# First time: npx hardhat vars set PRIVATE_KEY
npx hardhat run scripts/deploy.js --network sepolia

# Development only: with .env private key
npx hardhat run scripts/deploy.js --network sepolia

# Verify contract
npx hardhat verify --network sepolia DEPLOYED_CONTRACT_ADDRESS
```

## Best Practices

1. **Secure private key management** - Use hardware wallets or Hardhat Configuration Variables for all deployments; never store production keys in .env
2. **Use hardhat-toolbox** - Includes all essential plugins
3. **TypeScript for large projects** - Better type safety and IDE support
4. **Comprehensive .env.example** - Document all required environment variables (but discourage private keys)
5. **Separate networks** - Configure all networks you'll deploy to
6. **Gas reporting** - Enable gas reports for optimization
7. **Code coverage** - Run coverage regularly
8. **Contract verification** - Always verify deployed contracts
9. **Version lock dependencies** - Use exact versions in package.json

## Troubleshooting

### Issue: "hardhat: command not found"

```bash
# Use npx
npx hardhat compile

# Or install globally (not recommended)
npm install -g hardhat
```

### Issue: Module not found errors

```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Issue: Compilation errors with OpenZeppelin

```bash
# Ensure correct import paths
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
```

### Issue: Network connection errors

```bash
# Check RPC URL in .env
# Test with curl
curl -X POST -H "Content-Type: application/json" \
  --data '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}' \
  $SEPOLIA_RPC_URL
```

## Quick Reference

| Task | Command | Notes |
|------|---------|-------|
| Init project | `npx hardhat init` | Creates new project |
| Add dependency | `npm install <package>` | Uses npm |
| Compile | `npx hardhat compile` | Compiles contracts |
| Test | `npx hardhat test` | Runs tests |
| Coverage | `npx hardhat coverage` | Test coverage |
| Gas report | `REPORT_GAS=true npx hardhat test` | Gas usage |
| Deploy | `npx hardhat run scripts/deploy.js` | Run deployment |
| Verify | `npx hardhat verify` | Verify on Etherscan |
| Clean | `npx hardhat clean` | Clean artifacts |

## Template Files

This skill provides the following templates:
- `./templates/hardhat.config.js` - JavaScript configuration
- `./templates/hardhat.config.ts` - TypeScript configuration
- `./templates/.env.example` - Environment variables template
- `./templates/deploy-script.js` - Deployment script template

## Scripts

This skill provides the following scripts:
- `./scripts/init-hardhat.sh` - Automated project initialization

---

**Next Steps After Setup:**
1. Configure `hardhat.config.js` for your networks
2. Copy `.env.example` to `.env` and fill in values
3. Install required dependencies with `npm install`
4. Write contracts in `contracts/`
5. Write tests in `test/`
6. Run `npx hardhat test` to verify setup
