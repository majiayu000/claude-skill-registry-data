---
name: devtool
description: Development utilities - datetime, hash, uuid, encoding/decoding, password generator, regex validation
activation_keywords: [datetime, hash, uuid, base64, base58, encode, decode, password, regex, time, now]
execution_mode: server
---

# DevTool Skill

All-in-one development utilities tool. Use `builtin_devtool` tool with the following operations:

## Operations

### 1. datetime
- `now`: Get current time in various formats
- `convert`: Convert time between timezones
- `parse`: Parse a timestamp string
- `relative`: Calculate relative time

### 2. hash
Calculate hash values:
- `sha1`, `sha256`, `sha512`
- `bcrypt`: Hash password with bcrypt

### 3. uuid
Generate UUIDs:
- `v4`: Random UUID v4

### 4. encode/decode
- `base64_encode`, `base64_decode`
- `base58_encode`, `base58_decode`
- `url_encode`, `url_decode`
- `hex_encode`, `hex_decode`

### 5. password
Generate secure passwords. Parameters:
- `length`: Password length (default 16)
- `use_uppercase`: Include uppercase letters (default true)
- `use_lowercase`: Include lowercase letters (default true)
- `use_numbers`: Include numbers (default true)
- `use_special`: Include special chars (default true)

### 6. regex
- `validate`: Validate string against regex pattern
- `match`: Find matches in text

### 7. aes
- `aes_encrypt`: AES encryption
- `aes_decrypt`: AES decryption

## Parameters

- `operation`: The operation to perform
- `input`: Input string (for hash, encode, decode, regex)
- `param`: Additional parameter (timezone, length, etc.)
- `length`: Password length
- `use_uppercase`: Include uppercase (true/false)
- `use_lowercase`: Include lowercase (true/false)
- `use_numbers`: Include numbers (true/false)
- `use_special`: Include special chars (true/false)
