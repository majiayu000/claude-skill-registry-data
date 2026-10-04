---
name: mbedtls-integration
description: Use when integrating, porting, configuring, or debugging mbedTLS on MCU projects, TLS handshakes, certificates, entropy, RNG, memory, or secure embedded transports
---

# mbedTLS Integration

## Overview

Use this skill to integrate mbedTLS on embedded targets by proving entropy/RNG, time, certificate storage, transport I/O, and memory configuration before debugging application protocols. TLS failures often come from platform hooks rather than cryptography logic.

## When To Use

Use this skill when:

- The user wants TLS, HTTPS, MQTT over TLS, DTLS, X.509, crypto, or secure boot-related primitives using mbedTLS.
- The issue involves handshake failure, certificate validation, entropy source, RNG, memory allocation, time validity, or socket callbacks.
- The target is resource-constrained or has hardware crypto/TRNG.

Do not use this skill for generic networking before TCP/IP works. Use `lwip-integration` first when connectivity is unproven. For lightweight ECC-only operations, use `micro-ecc-integration` or `tinycrypt-integration`.

## First Questions

Ask for:

- mbedTLS version, target MCU/RTOS, compiler, and network stack.
- Use case: TLS client, TLS server, DTLS, crypto only, MQTT TLS, HTTPS, or certificate parsing.
- `mbedtls_config.h`, enabled features, heap/static allocation policy, and hardware crypto use.
- Entropy/RNG source and time source.
- Certificate chain model, CA storage, SNI/hostname verification, and current error code.

## Integration Checklist

1. Prove entropy and RNG.
   TLS requires a real entropy source. Do not ship deterministic test entropy.

1. Configure time.
   Certificate validation needs valid time or an explicit product policy for time-less validation.

1. Bound memory.
   Configure record size, heap, I/O buffers, certificate features, and algorithms for MCU limits.

1. Connect transport callbacks.
   Network send/recv callbacks must handle non-blocking, timeout, and partial I/O correctly.

1. Validate certificates.
   Use CA chain, hostname/SNI, and expected verification policy. Do not disable verification silently.

1. Decode error codes.
   Convert negative mbedTLS errors to readable names before guessing.

## Common Failures

- Handshake fails because time is unset.
- Certificate verification is disabled to "make it work".
- Entropy source is weak or not initialized.
- Heap is too small for certificate chain or record buffers.
- Socket callbacks treat timeout as fatal or ignore partial writes.
- SNI hostname does not match broker/server certificate.

## Verification

Before claiming mbedTLS works:

- State use case, mbedTLS version, entropy source, time source, and memory policy.
- Confirm a handshake to the target server with certificate verification enabled, unless explicitly out of scope.
- Report decoded error codes for failures.
- Confirm secrets, private keys, and certificates are not logged.
- Confirm memory usage fits the target.

## Example

User:

```text
MQTT 加 mbedTLS 后握手失败。
```

Agent:

1. Asks for mbedTLS error code, config, entropy/time source, broker certificate, SNI, and heap size.
1. Decodes the error and checks time/certificate verification before MQTT logic.
1. Verifies TLS connect before MQTT connect.
