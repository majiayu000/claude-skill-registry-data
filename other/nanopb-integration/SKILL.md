---
name: nanopb-integration
description: Use when integrating, porting, configuring, or debugging nanopb Protocol Buffers, .proto generation, pb_encode, pb_decode, callbacks, fixed sizes, or embedded serialization
---

# nanopb Integration

## Overview

Use this skill to integrate nanopb by controlling schema size, generated options, callbacks, and buffer ownership. Embedded protobuf failures usually come from mismatched generated files, unbounded fields, or callback misuse.

## When To Use

Use this skill when:

- The user wants Protocol Buffers on an MCU using nanopb.
- The task involves `.proto`, `.options`, `nanopb_generator.py`, `pb_encode`, `pb_decode`, repeated fields, strings, bytes, callbacks, or fixed-size arrays.
- Encoding/decoding fails, messages are truncated, memory usage is too high, or host and device schemas mismatch.

Do not use this skill for general JSON/INI parsing. Use `embedded-data-parsing-libs` instead.

## First Questions

Ask for:

- nanopb version and how code generation runs.
- `.proto`, `.options`, generated `.pb.c/.pb.h`, and host-side schema version.
- Transport/storage where messages are sent.
- Max message size, RAM budget, and whether streaming decode is needed.
- Current encode/decode error and sample payload if available.

## Integration Checklist

1. Lock schema and generated files together.
   Regenerate `.pb.c/.pb.h` whenever `.proto` or `.options` changes.

1. Bound variable fields.
   Use nanopb options for max string, bytes, repeated field, or callback-based streaming.

1. Size buffers explicitly.
   Know max encoded size and transport frame limits.

1. Check return values.
   Always inspect `pb_encode`/`pb_decode` failure and error text.

1. Validate compatibility.
   Test device-generated payload with host decoder and host-generated payload with device decoder.

## Common Failures

- Generated files are stale relative to `.proto`.
- Repeated/string fields need max sizes but default to callbacks.
- Decode fails because the transport strips length framing.
- Device and host use different schema versions.
- Stack buffers are too small for worst-case message size.
- Callback decode stores pointers into temporary buffers.

## Verification

Before claiming nanopb works:

- State schema version, generator path, max message size, and field-size policy.
- Confirm encode and decode of a golden message.
- Confirm malformed/truncated payload behavior.
- Confirm host-device compatibility.
- Confirm memory usage fits stack/heap/static budget.

## Example

User:

```text
nanopb 解码一直失败，但 PC 端 protobuf 能解析。
```

Agent:

1. Asks for `.proto`, `.options`, generated files, payload framing, and error string.
1. Checks stale generation and max field settings.
1. Tests a golden payload both directions.
