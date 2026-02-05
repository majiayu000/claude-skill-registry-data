---
name: side-channels
description: Timing attacks and other side-channel exploitation techniques
---

# Side-Channel Attacks

**Concept:** Extract secrets by observing indirect signals (timing, errors, etc.).

---

## Timing Side-Channel

**Signals:**
- Comparison that exits early on mismatch
- Observable response time differences
- Per-character validation

**Why it works:**
```c
// Vulnerable: early exit
for (int i = 0; i < len; i++) {
    if (input[i] != secret[i])
        return FAIL;  // Time varies by position
}
```

---

## Attack Recipe

**1. Establish baseline:**
```
Measure response time for known-wrong inputs
Calculate average/median for comparison
```

**2. Byte-by-byte oracle:**
```
For each position:
  For each candidate byte:
    Measure response time (multiple samples)
  Select byte with longest average time
```

**3. Noise reduction:**
- Multiple samples per candidate
- Use median (more robust than mean)
- Remove outliers
- Run from same network as target

---

## Strategies

**Local binary:**
- Minimal noise
- Direct timing measurement
- Few samples needed

**Remote server:**
- Network jitter requires many samples
- Statistical analysis helps
- Median over 20-100 samples

**Rate limited:**
- Add delays between attempts
- Prioritize likely characters
- Parallel connections if allowed

---

## Other Oracles

**Error-based:**
```
Different errors reveal different failure modes
- "Invalid length" vs "Bad character" vs "Wrong value"
Each error type leaks information
```

**Padding oracle:**
```
Decrypt ciphertext by observing padding errors
Valid vs invalid padding reveals information
```

---

## Pitfalls

| Issue | Solution |
|-------|----------|
| High jitter | More samples, statistical methods |
| Flat timing | Target uses constant-time comparison |
| Rate limits | Slow down, parallelize |
| Tiny differences | Higher precision timer, more samples |

---

## Detection

If all inputs produce same timing regardless of correctness:
- Target uses constant-time comparison
- Timing attack won't work
- Need different approach
