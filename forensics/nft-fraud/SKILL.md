---
name: nft-fraud
description: Use when assessing NFT projects, marketplaces, or fraud
  patterns on an authorized engagement. Covers wash trading detection,
  metadata and minting flaws, phishing against collectors, and
  marketplace logic review. Also use when investigating suspicious NFT
  activity for a client.
version: 1.0.0
domain: blockchain
lifecycle: stable
last_verified: '2026-10-23'
requires: []
extends: []
relates: [smart-contract-audit, blockchain-forensics, phishing-defense]
tools:
  - name: Python
    version: '3.12'
---

NFT fraud is mostly market manipulation and theft, not chain breaks:
wash trading to fake volume, phishing to steal tokens, and minting
bugs that let insiders grab rare items. This skill covers authorized
assessment and investigation: detecting wash trading, reviewing mint
and metadata logic, and mapping the phishing patterns that target
collectors.

## Quick Workflow

1. Define the scope: the collection, the marketplace, or the fraud
   pattern under investigation.
2. Pull on chain data: transfers, sales, and mints for the collection.
3. Detect wash trading: circular sales, self dealing, and volume
   without economic substance.
4. Review the minting logic: randomness, allowlists, and insider
   advantage.
5. Check metadata: is it on chain, on IPFS pinned, or on a server
   that can rug.
6. Map phishing patterns: fake mints, malicious approvals, and
   signature scams targeting holders.
7. Review marketplace logic: order matching, royalties, and delisting.
8. Report with transaction hashes as evidence.

## 1. Wash trading detection

```python
#!/usr/bin/env python3
"""Wash trade heuristics on NFT transfer data (public chain data)."""
import json, collections

# transfers: list of dicts with token_id, seller, buyer, price, tx
transfers = [json.loads(l) for l in open("/tmp/nft/transfers.jsonl")]

# Heuristic 1: buyer == seller (self dealing)
self_deals = [t for t in transfers if t["buyer"] == t["seller"]]
print("self deals:", len(self_deals))

# Heuristic 2: circular trading rings (A->B->C->A on same token)
by_token = collections.defaultdict(list)
for t in transfers:
    by_token[t["token_id"]].append(t)
rings = 0
for tid, ts in by_token.items():
    addrs = [t["seller"] for t in ts] + [ts[-1]["buyer"]]
    if len(set(addrs)) < len(addrs):
        rings += 1
print("tokens with repeated traders (possible rings):", rings)

# Heuristic 3: volume concentration in few wallets
vol = collections.Counter()
for t in transfers:
    vol[t["buyer"]] += t["price"]
print("top 5 buyers by volume:", vol.most_common(5))
```

## 2. Mint and metadata review

```bash
# Minting logic: check randomness source and allowlist enforcement
grep -rn "random\|block.timestamp\|allowlist\|merkleProof" nft-contracts/contracts --include="*.sol" | head -20
# block.timestamp randomness is predictable; merkle proofs must verify
```

```bash
# Metadata: where does tokenURI point, and can it change?
grep -rn "tokenURI\|setBaseURI\|_baseURI" nft-contracts/contracts --include="*.sol" | head -10
# Findings: mutable base URI with EOA owner (rug risk), unpinned IPFS,
# reveal mechanics that insiders can game
curl -s "$(cast call $CONTRACT 'tokenURI(uint256)' 1 --rpc-url $RPC_URL)" | head -c 300
```

## 3. Collector phishing patterns

```bash
# Patterns to brief and to check in marketplace UX:
# - malicious setApprovalForAll requests (drain entire collections)
# - fake mint sites promoted on compromised social accounts
# - signature phishing (EIP-712 signatures that list NFTs for sale)
echo "defense: hardware wallet, revoke approvals, verify domains, simulate transactions"
```

```bash
# Check a wallet's approvals as part of an incident review (public data)
# list ERC721 approvals to unknown operators for the victim address
python3 - << 'PY'
print("query: ApprovalForAll events where owner=victim, operator not in allowlist")
print("any unknown operator with approval = immediate revoke")
PY
```

## Edge cases

- Wash trading vs legitimate market making. Require multiple
  heuristics to agree before calling it fraud.
- The collection is on a chain with cheap gas. Wash trading is
  cheaper there; adjust thresholds.
- Metadata is fully on chain. Rug risk drops, but mint fairness
  still needs review.
- Investigation involves real victims. Handle personal data
  carefully and coordinate with the client's legal team.

## Escalation

- Active phishing site found: report to the registrar and hosting
  provider, and warn the community through official channels.
- Marketplace vulnerability found: disclose to the marketplace
  security contact with a testnet proof of concept.
- Large scale fraud with identified victims: involve law enforcement
  per the client's counsel.

## Detection and defender view

Marketplaces detect wash trading with the same heuristics above,
plus fee analysis (wash traders pay fees, so fee revenue spikes).
They defend with verified collections, transaction simulation, and
approval warnings. Collectors defend with hardware wallets, minimal
approvals, and skepticism toward DMs offering mints. The durable fix
for projects is fair mint mechanics and immutable metadata.

## Key references

- CWE-862 (Missing Authorization): approval phishing surface.
- CWE-330 (Use of Insufficiently Random Values): mint randomness.
- Chain analysis methodology for NFT transfers.
