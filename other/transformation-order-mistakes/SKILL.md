---
name: transformation-order-mistakes
description: Detect and fix SE3 transform matrix multiplication order errors. Use when reviewing or writing code that chains coordinate frame transforms.
argument-hint: <file-or-function to review>
---

# Transformation Order Mistakes

## The Convention

When naming transforms `A2B`, the name describes the vector flow: it transforms a point **from frame A into frame B**.

To chain transforms, matrix multiplication must be ordered so a vector hits the transforms **right-to-left**, matching the flow through intermediate frames:

```
A2C = B2C @ A2B
```

Read right-to-left: a vector in A's frame first hits `A2B` (A -> B), then `B2C` (B -> C), arriving in C's frame.

## The Mistake Pattern

The most common error is writing the transforms in the **same order as the name reads left-to-right**:

```python
# WRONG: reads naturally but multiplies backwards
A2C = A2B @ B2C
```

This is wrong because a vector `v` would hit `B2C` first (expects B-frame input, but gets A-frame input).

## Real Examples

### Example 1: Three-frame chain (baseline -> left -> target)

```python
# WRONG
baseline2target = baseline2left @ left2target

# RIGHT: vector hits baseline2left first (rightmost), then left2target
baseline2target = left2target @ baseline2left
```

**What went wrong:** The author wrote the matrices in the same order as the English reading "baseline to left, left to target." But matrix multiplication applies right-to-left to vectors.

### Example 2: Computing target2base from known ee2target and ee2base

```python
# WRONG
target2base = inv(ee2target) @ ee2base

# RIGHT: vector in target frame hits target2ee first, then ee2base
target2base = ee2base @ inv(ee2target)
#           = ee2base @ target2ee
```

**What went wrong:** `inv(ee2target)` is `target2ee`. The author wrote `target2ee @ ee2base` which reads naturally as "target to ee, ee to base" — but that's the English reading order, not the multiplication order. A vector in target's frame must hit `target2ee` first (rightmost).

### Example 3: Composing desired pose into base frame

```python
# WRONG
ee2base = ee2target @ target2base

# RIGHT: vector in ee frame hits ee2target first (rightmost), then target2base
ee2base = target2base @ ee2target
```

## How to Verify

For any chain `result = M1 @ M2`:
1. A vector `v` is first multiplied by `M2` (rightmost)
2. That result is then multiplied by `M1` (leftmost)
3. So `M2` must accept vectors in the **source** frame
4. And `M1` must accept vectors in `M2`'s **output** frame

**Quick check:** The inner frame names must match. In `B2C @ A2B`, the output of `A2B` is B-frame, and the input of `B2C` is B-frame. The B's touch in the middle.

```
result = X2Z @ W2X
              ^  ^
              |  +-- input: W frame
              +-- output of right / input of left must match: X frame
```

If the inner names don't match, the order is wrong.
