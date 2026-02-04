---
name: check_physics
description: 実装内容が数学的・物理学的に妥当か検証する
---

# Verify Physics

This skill performs a review of the code specifically focusing on physics and math correctness.

## Instructions

1.  **Dimensional Analysis**:
    *   Check if unit handling (e.g., `astropy.units`, `quantities`) is used correctly.
    *   Ensure operations are physically valid (e.g., not adding Length to Time).

2.  **Mathematical Inspection**:
    *   Verify equations against known reference papers or standard textbooks.
    *   Check for numerical stability issues (e.g., division by zero, floating point precision loss).
    *   Check edge cases (e.g., $f=0$, infinite limits).

3.  **Sanity Checks**:
    *   Create a small script to test conservation laws (e.g., Parseval's theorem for FFT).
    *   Verify that reasonable inputs produce physically reasonable outputs.

4.  **Report**:
    *   Provide a summary of the analysis, pointing out any suspect logic or confirming validity.
