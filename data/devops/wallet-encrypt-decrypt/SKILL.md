---
name: wallet-encrypt-decrypt
description: Encrypt and decrypt messages using BSV keys and ECDH. Uses @bsv/sdk for cryptographic operations.
allowed-tools: "Bash(bun:*)"
---

# Wallet Encrypt/Decrypt

Encrypt and decrypt messages using BSV keys (ECDH).

## When to Use

- Encrypt messages to a public key
- Decrypt messages with private key
- Secure communication between BSV addresses
- End-to-end encrypted messaging

## Usage

```bash
# Encrypt message to public key
bun run /path/to/skills/wallet-encrypt-decrypt/scripts/encrypt-message.ts <public-key> "message"

# Decrypt message with private key
bun run /path/to/skills/wallet-encrypt-decrypt/scripts/decrypt-message.ts <private-wif> <encrypted-hex>
```

## Encryption Method

Uses ECDH (Elliptic Curve Diffie-Hellman):
- Sender: Ephemeral key + recipient public key = shared secret
- Encrypt with AES using shared secret
- Send: ephemeral public key + encrypted data
- Recipient: private key + ephemeral public key = same shared secret
- Decrypt with AES

## Requirements

- `@bsv/sdk` package for ECDH and AES
- Valid BSV public/private keys
