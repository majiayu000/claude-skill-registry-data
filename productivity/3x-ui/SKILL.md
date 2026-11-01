---
name: 3x-ui
description: Route operator requests to the correct 3x-ui skill for VPS deployment, installation, API automation, inbound design, routing, security hardening, or Cloudflare publishing.
---

# 3X-UI Repository Router

Use this skill when the task mentions `3x-ui` broadly but the correct operating surface is not yet chosen.

## Routing Rules

- Use `3x-ui-vps` for opinionated VPS deployment, nginx publishing, loopback-only panel exposure, and scripted maintenance.
- Use `3x-ui-install` for install, update, backup, restore, database migration, OpenAPI, and panel lifecycle workflows.
- Use `3x-ui-inbounds` for protocol, transport, REALITY, XHTTP, WebSocket, gRPC, Hysteria2, MTProto, and client compatibility.
- Use `3x-ui-routing` for Xray DNS, routing rules, direct/proxy/block policy, WARP rotation, subscription outbounds, and balancers.
- Use `3x-ui-security` for panel hardening, TLS, firewall, SSH, Fail2Ban, and backup protection.
- Use `3x-ui-cloudflare` for DNS, proxied publication, Tunnel, SSL modes, and edge-to-origin compatibility.

## Escalation Rules

- if the task mutates a live server, verify that the operator controls the host
- if the change involves current release-specific behavior, verify the official repository and wiki first
- for `v3.3.0+` API work, use `/panel/api` and the in-panel OpenAPI document
- if the task crosses multiple domains, start with the smallest safe change and then branch into the specialist skill

## Verified Baseline

Checked June 12, 2026 against 3X-UI `v3.3.0`, Xray-core `v26.6.1` as bundled by 3X-UI, sing-box `v1.13.13`, Hysteria `v2.9.2`, and current Cloudflare Developers documentation.
