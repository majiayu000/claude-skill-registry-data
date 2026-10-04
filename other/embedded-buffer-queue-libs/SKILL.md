---
name: embedded-buffer-queue-libs
description: Use when integrating, porting, configuring, or debugging embedded ring buffers, circular buffers, FIFO queues, Ring-Buffer, or QueueForMcu libraries
---

# Embedded Buffer Queue Libs

## Overview

Use this skill for embedded ring buffers and lightweight queues. The core decision is ownership and concurrency: single producer/consumer, ISR-to-task, task-to-task, DMA-to-task, or multi-producer use.

## When To Use

Use this skill when:

- The user wants to integrate or debug Ring-Buffer, QueueForMcu, circular buffers, FIFOs, UART RX buffers, log queues, or event queues.
- The issue involves overflow, data loss, race conditions, wraparound, off-by-one capacity, ISR safety, or DMA buffer handoff.

Do not use this skill for RTOS-native queues unless the issue is about wrapping a custom buffer around them.

## First Questions

Ask for:

- Buffer/queue library and intended data type.
- Producer and consumer contexts: ISR, DMA, task, main loop, shell, or logger.
- Required behavior on full/empty: drop, overwrite oldest, block, error, or backpressure.
- Element size, capacity, maximum burst, and latency budget.
- Whether operations must be lock-free or protected by critical sections.

## Integration Checklist

1. Define ownership.
   Specify exactly who writes, who reads, and whether there can be multiple producers or consumers.

1. Define full/empty semantics.
   Do not leave overwrite/drop/block behavior implicit.

1. Check capacity math.
   Many ring buffers hold `N-1` items to distinguish full from empty.

1. Protect concurrent access.
   Use interrupt masking, atomics, mutexes, or single-producer/single-consumer rules as appropriate.

1. Verify wraparound.
   Test writes and reads across the end of the buffer.

1. Add telemetry.
   Track high-water mark, overflow count, drop count, or queue full events.

## Common Failures

- Race between ISR producer and task consumer.
- Off-by-one capacity causes one byte or one element to disappear.
- DMA writes into a buffer while CPU reads stale cached data.
- Full buffer silently overwrites critical data.
- Queue stores pointers to stack objects that go out of scope.

## Verification

Before claiming buffer/queue works:

- State producer/consumer contexts and protection strategy.
- Confirm full, empty, wraparound, and overflow behavior.
- Confirm maximum burst fits capacity or drops are counted intentionally.
- For DMA/cache systems, state cache maintenance or memory placement.

## Example

User:

```text
UART 中断收数据用 ring buffer，偶尔丢字节。
```

Agent:

1. Asks for producer/consumer contexts, baud, buffer size, overflow policy, and critical sections.
1. Checks N versus N-1 capacity and ISR/task race.
1. Adds overflow counters and tests burst input across wraparound.
