---
name: pricing-safety
description: Safely change TinyCart pricing calculations while preserving integer-cent arithmetic, discount bounds, and focused unit-test coverage.
---

# Pricing safety

Use this skill for changes to `src/tinycart/pricing.py`.

- Represent money only as integer cents.
- Reject invalid negative prices and quantities.
- Clamp discounts so a result cannot become negative.
- Run `python run_tests.py` after changes.
