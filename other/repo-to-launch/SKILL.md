---
name: repo-to-launch
description: Turn a finished product or repository into a factual launch pack with screenshots/assets, an X post, LinkedIn copy, Product Hunt fields, Reddit/HN variants, and an OG image brief. Use when the user says launch this repo, make launch assets, or turn a shipped product into distribution.
---

# Repo to Launch

1. Run `scripts/inspect_repo.py` first. Use only facts found in the repo/product or supplied by the user.
2. Do not invent traction, customers, benchmarks, logos, or product capabilities.
3. Create `launch-pack/` with `facts.json`, `x.md`, `linkedin.md`, `product-hunt.md`, `reddit.md`, `hn.md`, `asset-brief.md`.
4. Prefer one concrete artifact/result over generic launch claims.
5. If screenshots/video are available, use the real product.
6. Run `scripts/validate_pack.py` before publishing.

