---
name: micro-ecc-integration
description: Use when integrating, porting, or debugging micro-ecc (uECC) ECDH, ECDSA, key generation, uECC_set_rng, signatures, curve selection, or key/signature byte formats on an MCU
---

# micro-ecc Integration

## Overview

Use this skill to integrate micro-ecc (kmackay/micro-ecc, header `uECC.h`) by treating randomness, key storage, curve choice, and test vectors as security-critical. ECC that compiles but never called `uECC_set_rng()` or uses mismatched key byte formats is not working. The core key generation, signing, verification, and ECDH functions return `1` on success and `0` on failure (`uECC_verify` returns `1` only for a valid signature); the size-query helpers instead return a byte count, and `uECC_compress`/`uECC_decompress` return `void`.

## When To Use

Use this skill when:

- The user wants ECDH (`uECC_shared_secret`), ECDSA (`uECC_sign`/`uECC_verify`), or key generation (`uECC_make_key`) on an MCU using micro-ecc.
- The issue involves `uECC_make_key`/`uECC_sign` returning `0`, bad signatures, key mismatch, RNG, curve selection, endian/format mismatch, or slow scalar multiplication.
- The project uses `uECC.h`, `uECC.c`, a `uECC_Curve`, or `uECC_set_rng`.

Do not use this skill for full TLS stacks. Use `mbedtls-integration` for TLS. For AES/SHA/HMAC primitives, use `tinycrypt-integration`.

## First Questions

Ask for:

- Curve and operation: `uECC_secp160r1`, `uECC_secp192r1`, `uECC_secp224r1`, `uECC_secp256r1`, or `uECC_secp256k1`; and ECDH vs ECDSA.
- Target MCU, compiler, and whether a hardware TRNG/crypto peripheral exists.
- The RNG source wired into `uECC_set_rng()` and the key storage policy.
- Public/private key byte format and endian expectations of the peer (`uECC_VLI_NATIVE_LITTLE_ENDIAN` setting, compressed vs uncompressed).
- Test vector, signature, or verification failure details, and the return code seen.

## Integration Checklist

1. Choose curve deliberately.
   Pick a `uECC_Curve` via `uECC_secp256r1()` (or the peer's curve) and enable it with the matching `uECC_SUPPORTS_secp256r1` macro. Disable unused curves to save flash.

1. Provide a real RNG first.
   Register `uECC_set_rng(uECC_RNG_Function fn)` where `fn` has signature `int fn(uint8_t *dest, unsigned size)` and returns `1` when `dest` is filled with good entropy, `0` otherwise. Without a valid RNG, both `uECC_make_key` and `uECC_sign` return `0`. Only `uECC_sign_deterministic` (RFC 6979-style deterministic nonce, needs a `uECC_HashContext`) works without an RNG.

1. Size every buffer from the curve.
   Always use `uECC_curve_private_key_size(curve)` and `uECC_curve_public_key_size(curve)` instead of hard-coded lengths or arithmetic on each other. The public key is `x||y` and equals `uECC_curve_public_key_size(curve)`; the private key equals `uECC_curve_private_key_size(curve)`. These are equal to 2x the field size and 1x the field size respectively for every curve EXCEPT `secp160r1`, where the private key is 21 bytes (the order needs an extra byte; the leading byte is often `0x00`) while the public key is 40 bytes. Never derive public-key or signature length from the private-key length.

1. Match key/signature byte format.
   Default is big-endian; public keys are raw `x||y` with NO `0x04` uncompressed prefix, so prepend `0x04` for SEC1/OpenSSL peers. If interop breaks, check `uECC_VLI_NATIVE_LITTLE_ENDIAN` matches both sides; keys/signatures across the two settings are incompatible. The signature is `r||s` and its length equals the public-key length (`uECC_curve_public_key_size(curve)`) -- for `secp160r1` that is 40 bytes, not `2 * private_key_size` (peers such as python-ecdsa may instead expect 42).

1. Sign the hash, not the message.
   `uECC_sign(private_key, hash, hash_size, signature, curve)` and `uECC_verify` take a message digest plus `hash_size`; hash the message yourself (e.g. SHA-256) and pass the digest. A hash longer than the curve order is truncated internally.

1. Handle compressed points if needed.
   With `uECC_SUPPORT_COMPRESSED_POINT`, use `uECC_compress`/`uECC_decompress`; a compressed point is one coordinate plus a leading parity byte, i.e. `(uECC_curve_public_key_size(curve) / 2) + 1` bytes. Validate imported keys with `uECC_valid_public_key`.

1. Protect secrets.
   Do not log private keys, the ECDSA nonce, or the shared secret from `uECC_shared_secret`.

## Common Failures

- `uECC_set_rng()` never called, so `uECC_make_key`/`uECC_sign` silently return `0`.
- RNG callback returns `0` (or returns success while producing weak/deterministic bytes) in production.
- Public key sent with or expecting a `0x04` prefix; micro-ecc uses raw `x||y` without it.
- `secp160r1` private key allocated as 20 bytes instead of 21, corrupting adjacent memory or the key.
- Deriving signature or public-key length from the private-key length; on `secp160r1` this over-allocates (42 vs 40) and breaks interop.
- `uECC_VLI_NATIVE_LITTLE_ENDIAN` mismatch between device and peer, so byte order flips and verify fails.
- Passing the raw message to `uECC_sign`/`uECC_verify` instead of the digest, or hashing inconsistently between the two sides.
- Curve mismatch: device built with `uECC_secp256r1` but server uses `secp256k1`.

## Verification

Before claiming micro-ecc works:

- State the `uECC_Curve`, operation, key/signature byte layout, and the RNG registered via `uECC_set_rng`.
- Confirm `uECC_make_key` returns `1` and buffers were sized with `uECC_curve_public_key_size`/`uECC_curve_private_key_size` (not derived from each other).
- Confirm known test vectors pass: `uECC_verify` returns `1` for a valid signature and `0` for tampered data/hash.
- For ECDH, confirm both peers derive the same `uECC_shared_secret`.
- Confirm secrets are not logged and storage policy is explicit.

## Example

User:

```text
micro-ecc 签名服务器验不过。
```

Agent:

1. Asks for the curve, whether the public key carries a `0x04` prefix, the hash input to `uECC_sign`, the RNG behind `uECC_set_rng`, and the `uECC_VLI_NATIVE_LITTLE_ENDIAN` setting on both sides.
1. Checks endian and that a digest (not the raw message) is passed, and reconstructs the peer's SEC1 format by prepending `0x04` to the `x||y` public key.
1. Verifies with a known vector via `uECC_verify` before changing protocol code.
