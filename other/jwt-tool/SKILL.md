---
name: jwt-tool
description: Parse, decode, and verify JWT tokens
activation_keywords: [jwt, token, decode, verify, parse, oauth, bearer]
execution_mode: server
---

# JWT Tool

JWT (JSON Web Token) operations:
- Decode JWT token (header and payload)
- Verify JWT signature (HS256, RS256, ES256)
- Check token expiration
- Extract claims
- Encode new JWT token

Use `builtin_jwt_tool` tool with fields:
- `operation`: one of "decode", "verify", "encode"
- `token`: JWT token string (required for decode/verify)
- `secret`: (optional) secret key for verification
- `payload`: (optional) payload for encode
- `algorithm`: (optional) algorithm (default: HS256)

Returns decoded payload and verification result.
