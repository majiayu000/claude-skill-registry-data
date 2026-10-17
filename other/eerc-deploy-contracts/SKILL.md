---
name: eerc-deploy-contracts
description: Use when the agent needs to deploy the eERC contracts with Hardhat — compiling, building circuits, and deploying the verifiers, BabyJubJub library, Registrar, and EncryptedERC in the correct order, for standalone or converter mode.
category: eERC
difficulty: Advanced
version: "0.1.0"
---

# eERC — Deploy the Contracts (Hardhat)

## Overview
Deploying eERC means: build the circuits/verifiers, deploy the `BabyJubJub` library, deploy the `Registrar`, then deploy `EncryptedERC` with the verifier addresses linked to the library. The repo ships ready scripts: `scripts/deploy-standalone.ts` and `scripts/deploy-converter.ts`.

## Prerequisites
- Node `>= v22.x`, `Circom >= 2.1.9`.
```sh
git clone https://github.com/ava-labs/EncryptedERC.git && cd EncryptedERC
npm install
npx hardhat compile
npx hardhat zkit make --force   # compile circuits
npx hardhat zkit verifiers      # generate Solidity verifiers
```

## Deploy order (what the scripts do)
1. **Deploy 5 verifiers** — `registration`, `mint`, `withdraw`, `transfer`, `burn` (via `deployVerifiers`). Set `isProd = true` for production/mainnet trusted-setup verifiers.
2. **Deploy `BabyJubJub`** library (linked into EncryptedERC).
3. **Deploy `Registrar(registrationVerifier)`**.
4. **Deploy `EncryptedERC`** linking BabyJubJub:

```ts
const encryptedERCFactory = new EncryptedERC__factory({
  "contracts/libraries/BabyJubJub.sol:BabyJubJub": babyJubJub,
});
const eerc = await encryptedERCFactory.connect(deployer).deploy({
  registrar: registrar.target,
  isConverter: false,        // false = standalone, true = converter
  name: "Test", symbol: "TEST",
  mintVerifier, withdrawVerifier, transferVerifier, burnVerifier,
  decimals: DECIMALS,
});
await eerc.waitForDeployment();
```

## Run it
```sh
# Local
npx hardhat node
npx hardhat run scripts/deploy-standalone.ts --network localhost
# or converter (also deploys a SimpleERC20 + mints test tokens):
npx hardhat run scripts/deploy-converter.ts --network localhost
```
For Fuji, configure the network + key and use `--network fuji` — see [[eerc-deploy-fuji]].

## Output addresses you must keep
`registrar`, `encryptedERC`, and the verifier + `babyJubJub` addresses (the scripts `console.table` them). The frontend needs the `encryptedERC` address; the SDK reads `registrar` from it.

## Common Pitfalls
- **Not building circuits first.** `zkit make` + `zkit verifiers` must run before deploy or verifier artifacts are missing.
- **Test verifiers on mainnet.** Always `isProd = true` for non-local — see [[eerc-circuits-proofs]].
- **Forgetting the library link.** The `BabyJubJub` link key string must match exactly: `contracts/libraries/BabyJubJub.sol:BabyJubJub`.

## AI Agent Prompt
> "Act as a deployment engineer. Deploy eERC in <standalone|converter> mode to <network>: build circuits, deploy the verifiers, BabyJubJub, Registrar, and EncryptedERC, and print the resulting addresses."

## References
See `references/README.md` — includes copies of `deploy-standalone.ts` / `deploy-converter.ts`.
