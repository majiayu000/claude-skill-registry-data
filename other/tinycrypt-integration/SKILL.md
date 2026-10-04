---
name: tinycrypt-integration
description: Use when integrating, porting, configuring, or debugging TinyCrypt cryptographic primitives, AES, SHA, HMAC, ECC, CTR/CCM, RNG, or embedded security code
---

# TinyCrypt Integration

## Overview

Use this skill to integrate TinyCrypt primitives safely. Cryptographic code needs test vectors, correct modes, nonce/IV discipline, key handling, and explicit threat boundaries before being used in products.

## When To Use

Use this skill when:

- The user wants lightweight crypto primitives on an MCU using TinyCrypt.
- The task involves AES, SHA, HMAC, CTR, CCM, ECC, RNG, key storage, message authentication, or encrypted firmware/data.
- Outputs do not match known vectors or peer devices.

Do not use this skill for TLS session integration. Use `mbedtls-integration` for full TLS. For standalone ECDH/ECDSA operations, use `micro-ecc-integration`.

## First Questions

Ask for:

- Primitive/mode: AES-CTR, AES-CCM, SHA, HMAC, ECC, or RNG.
- Protocol or data format consuming the primitive.
- Key, IV/nonce, tag length, AAD, and message framing policy without exposing secrets.
- Target MCU/compiler and hardware crypto availability.
- Known test vector or peer output.

## Integration Checklist

1. Use test vectors first.
   Validate primitive and mode with public vectors before product payloads.

1. Define nonce/IV rules.
   Nonce reuse can break security. Make generation and storage explicit.

1. Separate encryption and authentication.
   Know whether the mode authenticates data or only encrypts it.

1. Protect key material.
   Avoid logging keys, IV secrets, raw plaintext, or derived secrets.

1. Handle failures securely.
   Authentication failure must reject data, not fall back to plaintext.

## Common Failures

- AES mode mismatch with peer.
- Nonce/IV reused after reboot.
- Tag length or AAD differs from peer implementation.
- Hash/HMAC input framing differs.
- Test code logs secrets or accepts authentication failures.

## Verification

Before claiming TinyCrypt works:

- State primitive/mode, nonce policy, tag length, and framing.
- Confirm public test vectors pass.
- Confirm modified ciphertext/tag fails verification.
- Confirm secrets are not printed or stored insecurely.

## Example

User:

```text
TinyCrypt AES-CCM 加密后对端验签失败。
```

Agent:

1. Asks for mode parameters, nonce, tag length, AAD, framing, and test vector.
1. Checks nonce and AAD consistency before payload logic.
1. Verifies that modified tags are rejected.
