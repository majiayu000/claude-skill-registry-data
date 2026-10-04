---
name: crypto-tool
description: Encrypt/decrypt strings with various algorithms
activation_keywords: [encrypt, decrypt, crypto, aes, rsa, hash, cipher, encode]
execution_mode: server
---

# Crypto Tool

Cryptographic operations:
- AES encrypt/decrypt
- RSA encrypt/decrypt
- Hash functions (MD5, SHA1, SHA256)
- Base64 encode/decode
- HMAC generation
- Random string generation

Use `builtin_crypto_tool` tool with fields:
- `operation`: one of "encrypt", "decrypt", "hash", "hmac", "random"
- `algorithm`: encryption algorithm (AES, RSA, MD5, SHA1, SHA256)
- `data`: data to process (required)
- `key`: (optional) encryption key or secret
- `mode`: (optional) for AES: ECB, CBC, GCM (default: CBC)

Returns processed result.
