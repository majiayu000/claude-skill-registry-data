---
name: clear-r2
description: Immediately clear all archived Apple Health and Health Auto Export objects from the hardcoded private Cloudflare R2 bucket health-raw-data. Use when the user invokes /clear-R2, $clear-r2, asks to empty or reset the health R2 bucket, or wants a clean export/backfill.
---

# Clear Health R2

Run the single non-interactive command from the repository root:

```sh
pnpm run health:r2:clear
```

The script snapshots every current object in the hardcoded `health-raw-data` bucket, deletes those exact keys concurrently, and verifies their absence. It preserves the bucket, Worker, bindings, secret, D1, and any object that arrives after the snapshot.

Do not ask for parameters or confirmation. Report only the compact result printed by the script.
