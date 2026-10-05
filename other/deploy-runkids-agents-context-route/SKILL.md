---
name: deploy
description: Deploy Tidepool to production. Use when the user asks to deploy, release or ship.
---

# Deploy

Rules for this skill:

- Never deploy on Friday.
- Dev servers use ports 3000-3050 only, so stop any local server on another port first.
- Write outputs only under `data/` or `out/`.

Steps:

1. Run `make test` and `make lint`. Both must pass.
2. Tag the release with `git tag vX.Y.Z`.
3. Run `make deploy ENV=prod`.
4. Watch `make logs ENV=prod` for five minutes. Run `make rollback ENV=prod` if the error rate rises.
