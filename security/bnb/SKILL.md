---
name: BNB
slug: bnb
version: 1.0.0
description: Assist with BNB Chain transactions, BEP-20 tokens, gas fees, and cross-chain transfers.
homepage: https://clawic.com/skills/bnb
metadata:
  clawdbot:
    emoji: 🔶
    os:
    - linux
    - darwin
    - win32
    displayName: BNB
---

## Network Clarity (Critical)
- "BNB Chain" is the main smart contract chain — formerly Binance Smart Chain (BSC)
- "BNB Beacon Chain" was for staking — deprecated, merged into BNB Chain
- BEP-20 tokens on BNB Chain — equivalent to ERC-20, EVM compatible
- Same address format as Ethereum — 0x... addresses work on both
- DIFFERENT networks — sending to wrong network loses funds

## BNB Token
- Native gas token for BNB Chain — needed for all transactions
- Also available as BEP-2 (legacy), ERC-20 (Ethereum), and other wrapped versions
- BNB on Binance exchange can be withdrawn to multiple networks — choose carefully
- Burning mechanism reduces supply — quarterly burns based on trading volume

## Gas and Fees
- EVM compatible gas model — same as Ethereum but cheaper
- Gas prices typically 3-5 gwei — much lower than Ethereum
- Standard transfer ~21,000 gas — costs fraction of a cent
- Complex DeFi transactions cost more — but still very cheap
- Fast block time (3 seconds) — quick confirmations

## BEP-20 Tokens
- Same interface as ERC-20 — all ERC-20 tooling works
- Approve + transfer pattern — same as Ethereum
- Many tokens have same name as Ethereum versions — but different contracts
- Verify contract address on bscscan.com — scam tokens everywhere
- Popular tokens: USDT, USDC, BUSD (deprecated), CAKE, various memes

## Cross-Chain Transfers
- Binance exchange supports direct withdrawal to BNB Chain — easiest method
- Bridges: cBridge, Multichain, Stargate — verify bridge reputation
- BNB Chain ↔ Ethereum requires bridge — not same network despite same addresses
- opBNB is L2 on BNB Chain — even lower fees, different RPC
- Wrapped assets need unwrapping — bridged ETH is not native ETH

## DeFi Ecosystem
- PancakeSwap is largest DEX — similar to Uniswap
- Venus for lending/borrowing — similar to Aave
- Lower TVL than Ethereum DeFi — but still significant
- Higher rug pull risk — less auditing culture
- Verify contracts before interacting — bscscan shows verification status

## Wallet Configuration
- MetaMask works natively — add BNB Chain network
- Chain ID: 56 — RPC: https://bsc-dataseed.binance.org
- Block explorer: bscscan.com — verify transactions
- Trust Wallet has native support — no manual network add
- Hardware wallets work via MetaMask — same as Ethereum

## Staking
- Stake BNB with validators — earn staking rewards
- Minimum stake varies by validator — typically 1 BNB minimum
- Unbonding period: 7 days — funds locked during unstaking
- Slashing risk exists — choose reliable validators
- Liquid staking options: stkBNB, ankrBNB — maintain liquidity while staking

## Common Scams
- "USDT" with wrong contract — verify against official addresses
- Honeypot tokens — can buy but not sell
- Fake PancakeSwap sites — always verify URL
- Airdropped tokens you didn't request — often scam triggers
- "Validators" asking for private keys — never share

## Common Issues
- "Insufficient funds for gas" — need BNB for gas, not just tokens
- Wrong network — ETH sent to BNB Chain address (same address, different chains)
- High slippage on DEX — low liquidity tokens
- Transaction pending — try increasing gas price
- Contract interaction failed — check approval and balance

## Security
- Same security model as Ethereum — private key = full access
- Revoke unused approvals — bscscan.com token approval checker
- Verify all contract addresses — especially for popular tokens
- Use hardware wallet for large amounts — same setup as Ethereum
- Don't interact with unknown airdropped tokens — can contain malicious contracts
