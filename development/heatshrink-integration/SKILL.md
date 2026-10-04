---
name: heatshrink-integration
description: Use when integrating or debugging heatshrink embedded compression — encoder/decoder sink/poll/finish loops, window/lookahead sz2, HSER/HSDR codes, or static vs dynamic alloc
---

# heatshrink Integration

## Overview

Use this skill to integrate heatshrink (`github.com/atomicobject/heatshrink`) by fixing memory budget, `window_sz2`/`lookahead_sz2` sizes, the sink/poll/finish streaming loop, and decompression safety. Compression bugs usually come from mismatched encoder/decoder settings, an unfinished poll loop, or output buffers that are too small.

## When To Use

Use this skill when:

- The user wants heatshrink compression/decompression on an MCU.
- The task involves compressed logs, resources, firmware chunks, OTA payloads, or serial transfer compression.
- Decompression fails, output is truncated, memory is too high, or compressed data is incompatible.
- The project uses `heatshrink_encoder.h`, `heatshrink_decoder.h`, `heatshrink_config.h`, or the `heatshrink` command-line tool.

Do not use this skill for general archive formats like gzip/zip unless heatshrink is specifically involved.

## First Questions

Ask for:

- Use case: logs, UI assets, firmware chunks, telemetry, or storage.
- Encoder/decoder settings: `window_sz2` (4-15) and `lookahead_sz2` (3 to `window_sz2 - 1`). The CLI's compiled default is `-w 11 -l 4`; its help text recommends `-w 8 -l 4` for embedded systems.
- Allocation model: `HEATSHRINK_DYNAMIC_ALLOC` (heap via `HEATSHRINK_MALLOC`/`HEATSHRINK_FREE`) or static (`HEATSHRINK_STATIC_WINDOW_BITS`, `HEATSHRINK_STATIC_LOOKAHEAD_BITS`, `HEATSHRINK_STATIC_INPUT_BUFFER_SIZE`).
- Streaming or one-shot mode, and input/output chunk sizes plus decompressed size bound.
- Whether compressed data comes from host tools or target firmware.
- Current return code or mismatch symptom.

## Integration Checklist

1. Match settings across the boundary.
   Decoder `expansion_buffer_sz2` and `lookahead_sz2` must match the encoder's `window_sz2`/`lookahead_sz2`. Under static alloc, both sides must share the same `HEATSHRINK_STATIC_WINDOW_BITS`/`HEATSHRINK_STATIC_LOOKAHEAD_BITS`.

2. Choose the allocation model.
   Dynamic: `heatshrink_encoder_alloc(window_sz2, lookahead_sz2)` / `heatshrink_decoder_alloc(input_buffer_size, expansion_buffer_sz2, lookahead_sz2)`, freed with `*_free`. Static: set `HEATSHRINK_DYNAMIC_ALLOC 0` in `heatshrink_config.h` and use a stack/BSS instance, `*_reset` before reuse.

3. Drive the streaming loop correctly.
   Feed with `heatshrink_encoder_sink`/`heatshrink_decoder_sink` (check `*input_size` for bytes consumed; re-sink the remainder). Then loop `*_poll` until it returns `HSER_POLL_EMPTY`/`HSDR_POLL_EMPTY` before sinking more.

4. Flush at end of stream.
   After the last input, call `heatshrink_encoder_finish`/`heatshrink_decoder_finish`; while it returns `HSER_FINISH_MORE`/`HSDR_FINISH_MORE`, keep calling `*_poll` to drain output. Done is `HSER_FINISH_DONE`/`HSDR_FINISH_DONE`. Call `*_reset` before reusing the instance for a new stream.

5. Validate data integrity.
   Pair compression with CRC/hash when corruption matters. heatshrink carries no checksum or length header and does not reliably detect corrupt or truncated input, so integrity must be checked externally.

6. Test worst case.
   Some data expands; do not assume size savings. Size the output buffer/store for expansion, not just the compressed happy path.

## Common Failures

- Host encoder uses different `window_sz2`/`lookahead_sz2` than the MCU decoder (or mismatched `HEATSHRINK_STATIC_*`).
- Caller stops after one `*_poll` and treats partial output as complete, instead of looping until `HSER_POLL_EMPTY`/`HSDR_POLL_EMPTY`.
- `*_finish` never called (or its `HSER_FINISH_MORE`/`HSDR_FINISH_MORE` output not drained), so the tail of the stream is lost.
- Sinking more data on the encoder after `heatshrink_encoder_finish` without `heatshrink_encoder_reset` (returns `HSER_SINK_ERROR_MISUSE`).
- Ignoring `*input_size` from `*_sink` and dropping the unconsumed bytes.
- Truncated/corrupt compressed input produces silent garbage rather than an error, because heatshrink has no integrity check; `*_SINK_ERROR_NULL`/`*_POLL_ERROR_NULL` only guard null handles or buffers, and `HSDR_POLL_ERROR_UNKNOWN` is an internal-state guard, not a corruption detector.
- Compressed firmware lacks CRC before flash write; worst-case expansion exceeds allocated storage.

## Verification

Before claiming heatshrink works:

- State `window_sz2`/`lookahead_sz2`, allocation model (`HEATSHRINK_DYNAMIC_ALLOC`), decoder `input_buffer_size`, and buffer sizes.
- Confirm the poll loop drains to `*_POLL_EMPTY` and the finish loop drains `*_FINISH_MORE` to `*_FINISH_DONE`.
- Confirm a round-trip test for representative and worst-case (incompressible) data.
- Confirm that corrupt/truncated input is caught by an external integrity check, since heatshrink itself may emit silent garbage without an error code.
- Confirm the integrity check if used for firmware or persistent assets.

## Example

User:

```text
用 heatshrink 压缩资源，设备端解压出来缺尾巴。
```

Agent:

1. Asks for `window_sz2`/`lookahead_sz2`, decoder `input_buffer_size`/`expansion_buffer_sz2`, chunk sizes, and whether `heatshrink_decoder_finish` is called.
2. Checks that `*_poll` loops until `HSDR_POLL_EMPTY` and that `finish` is drained until `HSDR_FINISH_DONE` (the missing tail is almost always an undrained finish loop).
3. Verifies round-trip and truncated-input behavior, and that `heatshrink_decoder_reset` runs before reusing the instance.
