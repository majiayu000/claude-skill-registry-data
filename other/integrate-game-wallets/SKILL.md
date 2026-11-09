---
name: integrate-game-wallets
description: Integrate explicit player-wallet connection, scoped SIWE authentication, authority invalidation and reviewed target-specific handoff without application-held player keys.
engines: [AGNOSTIC]
---

# Integrate Game Wallets

## When to use

Connect or authenticate player-controlled EVM wallets, review account/chain/delegation lifecycle, inspect wallet batching capabilities, or prepare a narrow browser/native wallet handoff. A wallet login establishes account control; chain ownership and game access have separate owners.

## Workflow

1. Resolve the host engine and this skill with `commands/resolve-skill.sh integrate-game-wallets`; require `compatible: true`. Read the host WEB3.md, validated web3-game.json, architecture, selected chains and exact locked SDK/client identities. Preserve existing engine, style, media and Bubo authority. Unconfigured Web3 or missing compatible verification/transport ports remains unavailable. Selecting this skill imports/installs nothing and connects no account.
2. Read `references/INTEGRATION.md` and `.web3/CONTRACT.md` from the shared baseline. Use the framework-independent `.web3/runtime/wallet-session.mjs` or a reviewed host implementation. Supply the provider explicitly after the player's wallet selection; never discover/select an injected wallet silently or introduce a frontend framework solely for authentication. Keep key custody with the player and existing wallet.
3. Separate connected account, server authentication, canonical ownership and current game eligibility in APIs and UI. Obtain a server-issued canonical SIWE challenge bound to a strong one-use nonce, trusted browser session, exact HTTPS origin/URI, chain, address and short validity period. Have the server validate actual signature and all scope fields before issuing its session. The server's atomic durable nonce store and trusted chain-aware verifier are prerequisites, not JSON-configurable code.
4. Require an explicit account-kind/authority resolver and a tested verifier per selected profile. Handle undelegated EOA, ERC1271, ERC6492 and EIP7702 independently. Unknown or untested profiles return unavailable. Nonempty code cannot establish a conventional contract wallet, and an EOA key recovery alone cannot establish current delegation authority. Do not request raw delegation authorization, add a session key or enable sponsorship as part of login.
5. Invalidate pending requests and dependent authentication on account/chain/disconnect/delegation or relevant authority changes. Use finite deadlines, cancellation, identity checks before/after signing and teardown. Host watchers must report authority changes that EIP1193 does not standardize. Discard late results; local cancellation/disconnection cannot cancel an already displayed wallet prompt, revoke approvals or reverse chain effects.
6. Inspect selected-chain capabilities before planning wallet calls. EIP5792 `supported` means atomic batching is available; `ready` needs an upgrade and actual player approval; `unsupported` or unknown cannot promise atomic execution. Actual batching belongs to separately reviewed transaction integration and must require atomicity explicitly. Connection/login is no transaction, approval, listing, custody or delegation authorization.
7. For MAUI/native, preserve current WebView navigation/popup restrictions. An explicit native transport integration and real-device QA remain required. The optional native return guard only checks a fixed return URL, one-use state, S256 PKCE binding and expiry. It launches nothing and exposes no native methods. Verify OS app/universal links, backend code exchange, suspend/cold return, duplicates, account switching and identity on each selected target; in-memory callback fixtures establish none of these target claims.
8. Run the meaningful wallet tests with the explicitly provisioned pinned fixture. Preserve exact SDK/helper/policy/input identities and actual results. Require independent review and real browser/wallet/chain/native evidence for those deployment targets. Keep counterfactual/delegated wallets and unavailable services explicitly unsupported until their selected paths have matching evidence.

## Output

Deliver scoped challenge/session integration, the account-kind/capability matrix, invalidation/teardown behavior and evidence separated into actual SDK/local EVM, injected-port and real-target results. Never record player keys, signatures, nonce/session/PKCE material or wallet-linked personal data in public task artifacts. Delegate ownership and admission to `verify-onchain-game-assets`, trades to `integrate-game-asset-trading`, and independent lifecycle acceptance to `verify-web3-game-lifecycle`.
