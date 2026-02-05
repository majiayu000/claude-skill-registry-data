---
name: deploy-vps
description: Deploy a new image to a VPS Ubuntu host using GHCR and a deploy script.
---

## Intent
Use for GitOps-style deploys to a VPS when a new image is pushed.

## Steps
1. Confirm target env (dev|stage|prd|custom) and image tag.
2. Verify no secrets are exposed; use placeholders.
3. Use a deploy script or image updater on the VPS to pull and restart.
4. Verify health checks and metrics (Prometheus/Grafana) if available.

## Safety
- Require explicit confirmation before touching production.
- Provide rollback steps (previous tag) before execution.
