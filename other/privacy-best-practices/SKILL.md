---
name: privacy-best-practices
description: Use as the cross-cutting checklist for any Avalanche privacy build — the do's and don'ts spanning eERC and private L1s (registration, auditor setup, amount/metadata leakage, key hygiene, defense in depth). Reference before shipping anything privacy-related.
category: Privacy Deep-Dive
difficulty: Intermediate
version: "0.2.0"
---

# Privacy Best Practices (eERC + Private L1s)

## Overview
Privacy fails at the seams. These rules apply across both Avalanche privacy models and catch the most common leaks. Pair with [[eerc-privacy-threat-model]] and [[private-l1-metadata-leakage]].

## Do
- **Always register recipients first.** Verify with `isAddressRegistered` before transferring; an unregistered recipient leaks intent (failed tx) and blocks the transfer ([[eerc-sdk-registration]]).
- **Set an auditor before going live** if you need compliance — operations encode an auditor PCT and expect a valid auditor key ([[eerc-auditor-compliance]]).
- **Keep decryption keys client-side only.** Derive from wallet signature; never log or transmit ([[eerc-key-management]]).
- **Use production verifiers** (`isProd=true`) off local ([[eerc-circuits-proofs]]).
- **Layer defenses.** Data privacy (eERC) + access privacy (private L1) cover different threats — combine for sensitive deployments ([[combining-eerc-with-private-l1]]).
- **Restrict reads and writes.** On a private L1, allowlists gate writes; you must separately restrict RPC for reads ([[restrict-rpc-access]]).
- **Use a multisig** for contract owner / AllowList Admin / ValidatorManager ([[poa-validator-manager]]).

## Don't
- **Don't assume a "private L1" encrypts data.** It doesn't — insiders see plaintext ([[private-l1-metadata-leakage]]).
- **Don't leak through amounts.** Round-number transfers, unique amounts, or "amount fingerprints" can deanonymize even when encrypted patterns correlate. Avoid amounts that act as identifiers.
- **Don't ignore metadata.** Sender/receiver addresses, timing, and frequency are visible on public chains even with eERC ([[anonymity-network-privacy]]).
- **Don't reuse addresses** across contexts you want unlinkable.
- **Don't expose a public RPC** for a chain you call "private."
- **Don't ship test verifiers** or single-EOA admins to production.

## Pre-ship checklist
- [ ] Recipients registered; auditor key set (if compliance).
- [ ] Production verifiers; correct `.ptau` per circuit.
- [ ] Keys client-side; rotation procedure documented.
- [ ] RPC restricted (if private L1); allowlists configured; admin = multisig.
- [ ] Threat model reviewed: what's hidden vs what leaks.

## AI Agent Prompt
> "Act as a privacy reviewer. Audit my Avalanche privacy build against the do/don't checklist and flag any leakage (amounts, metadata, key handling, RPC exposure, admin keys)."

## References
See `references/README.md` (synthesis of eERC + private-L1 skills).
