---
name: embedded-data-parsing-libs
description: Use when integrating, porting, configuring, or debugging embedded C data parsers such as cJSON, jsmn, or inih on MCU projects
---

# Embedded Data Parsing Libs

## Overview

Use this skill for small embedded data parsers where the main risks are memory allocation, input bounds, encoding assumptions, recursion, and callback handling. Cover `cJSON`, `jsmn`, and `inih` without copying their full APIs.

## When To Use

Use this skill when:

- The user wants to parse JSON or INI on an MCU.
- The task mentions `cJSON`, `jsmn`, `inih`, config files, telemetry JSON, command payloads, or settings parsing.
- The issue involves parse failure, memory leak, heap exhaustion, malformed input, callback mapping, or stack/recursion limits.

Do not use this skill for binary protocols or large streaming parsers outside these small libraries.

## First Questions

Ask for:

- Parser library: `cJSON`, `jsmn`, `inih`, or another small C parser.
- Input source and maximum input size.
- Runtime: bare metal, RTOS, Linux, bootloader, or shell command.
- Whether dynamic allocation is allowed.
- Expected schema and how malformed input should behave.
- Current error, sample input, and memory budget.

## Library Checks

### cJSON

- Decide whether heap allocation is acceptable.
- Provide custom malloc/free hooks if the project uses a custom allocator.
- Always delete parsed trees after use.
- Bound input size before parsing.
- Validate type before reading values.

### jsmn

- Allocate enough tokens for the expected JSON shape.
- Handle `JSMN_ERROR_NOMEM`, `JSMN_ERROR_INVAL`, and `JSMN_ERROR_PART`.
- Remember that tokens reference the original input buffer.
- Validate string lengths and value types manually.

### inih

- Implement the handler callback with strict section/key matching.
- Decide whether duplicate keys overwrite, error, or merge.
- Bound line length and input source.
- Validate converted numeric values and ranges.

## Common Failures

- Heap fragmentation from repeated `cJSON_Parse` without hooks or cleanup.
- Token buffer too small for `jsmn`.
- Using JSON token pointers after the input buffer is freed.
- Accepting partial config and booting with unsafe defaults.
- Silent typo in INI key because handler ignores unknown fields.

## Verification

Before claiming parser integration works:

- State parser, allocation policy, max input size, and schema assumptions.
- Test valid input, missing fields, wrong types, malformed input, and oversize input.
- Confirm memory is released or static buffers are bounded.
- Confirm unknown fields and duplicate keys behavior.

## Example

User:

```text
想用 cJSON 解析串口发来的配置。
```

Agent:

1. Asks for max payload size, schema, allocator policy, and malformed-input behavior.
1. Uses custom hooks if needed and validates each field type.
1. Tests good JSON, missing keys, bad types, and oversized payloads.
