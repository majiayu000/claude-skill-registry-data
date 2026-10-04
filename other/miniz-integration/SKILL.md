---
name: miniz-integration
description: Use when integrating, configuring, or debugging miniz compression, DEFLATE, zlib streams, gzip-compatible data, ZIP archives, or embedded decompression buffers
---

# miniz Integration

## Overview

Use this skill to integrate miniz by separating format choice, memory budget, streaming strategy, and integrity checks. Compression bugs on MCUs usually come from buffer ownership, incomplete streams, or confusing raw DEFLATE, zlib, gzip, and ZIP containers.

## When To Use

Use this skill when:

- The user wants miniz for firmware assets, logs, configuration packages, OTA payloads, filesystems, or embedded resources.
- The issue involves inflate errors, truncated output, high RAM use, ZIP archive handling, CRC mismatch, or streaming decompression.
- The project has constrained RAM/flash, external storage, OTA downloads, or filesystem integration.

Do not use this skill for very small streaming compression windows. Use `heatshrink-integration` when heatshrink is already selected for tiny MCU buffers.

## First Questions

Ask for:

- Data format: raw DEFLATE, zlib, gzip-like stream, or ZIP archive.
- Compression/decompression direction, max input size, max output size, and RAM budget.
- Storage/transport path, chunk size, and whether streaming is required.
- Integrity requirement: CRC, hash, signature, or container metadata.
- Current error code, input sample, and expected decompressed length.

## Integration Checklist

1. Pick the exact format.
   Do not mix raw DEFLATE streams, zlib headers, gzip files, and ZIP archives.

1. Budget memory before coding.
   Estimate output buffer, dictionary/window needs, file metadata, and stack usage.

1. Prefer streaming for large payloads.
   Feed bounded chunks and write output incrementally instead of allocating the whole image.

1. Validate sizes and integrity.
   Check compressed length, decompressed length, CRC/hash, and destination capacity.

1. Handle partial and corrupt data.
   Every read/write callback should report short I/O and decompressor errors distinctly.

1. Test worst-case input.
   Include incompressible data, empty streams, truncated streams, and oversized output.

## Common Failures

- Feeding gzip or ZIP data to a raw DEFLATE API.
- Allocating output by trusting unverified metadata.
- Treating decompression success as authenticity.
- Ignoring short writes to flash or filesystem.
- Running decompression on a task stack that is too small.
- Using archive filenames directly without path validation.

## Verification

Before claiming miniz works:

- State format, API path, chunk size, and max memory use.
- Confirm a known-good payload decompresses byte-for-byte.
- Confirm corrupt, truncated, and oversized payloads fail safely.
- Confirm integrity checks and destination bounds.

## Example

User:

```text
用 miniz 解 OTA 资源包偶尔失败。
```

Agent:

1. Confirms whether the package is ZIP, zlib, or raw DEFLATE.
1. Checks chunked read/write callbacks and decompressed length bounds.
1. Adds corrupt and truncated package tests before changing transport code.
