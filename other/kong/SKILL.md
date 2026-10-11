---
name: kong
description: Kong API Gateway — routes, services, plugins, Admin API.
---

# Kong API Gateway

Kong is an open-source API gateway and platform built on Nginx/OpenResty. In Supabase, Kong routes all traffic to internal services (PostgREST, GoTrue, Realtime, Storage, Edge Functions).

## Detection Signals

| Signal | Meaning |
|---|---|
| `kong` service in `docker-compose.yml` | Self-hosted Kong |
| `volumes/api/kong.yml` in Supabase project | Supabase-embedded Kong config |
| `KONG_*` env vars | Kong configuration |
| `8000` / `8443` ports exposed | Kong proxy ports |
| `8001` / `8444` ports exposed | Kong Admin API ports |

## Core Concepts

| Concept | Description |
|---|---|
| **Service** | An upstream backend (e.g., PostgREST at `http://rest:3000`) |
| **Route** | A matching rule (host, path, method) that forwards to a Service |
| **Plugin** | Middleware attached to a Route, Service, or globally |
| **Upstream** | Load balancer target with health checks and multiple targets |
| **Consumer** | A user or application that calls your API (used for auth plugins) |

## Supabase-Specific Notes

**Declarative config only**: Supabase does not use the Kong Admin API — all config is declarative in `kong.yml`. In self-hosted setups, always edit `kong.yml` rather than calling the Admin API, or changes will be lost on restart.

**`strip_path` on prefix routes**: always set `strip_path: true` on a route matched by a path prefix — otherwise Kong forwards the prefix to the upstream and the upstream returns 404 for every request.

**`apikey` header**: Supabase uses a custom `apikey` header (the anon or service-role key). The Supabase Kong config validates this via the JWT plugin — the `apikey` is a valid JWT signed with your `JWT_SECRET`. Always include `apikey` in the CORS plugin `headers` list.

## Load on Demand

| When | Load |
|------|------|
| Configuring plugins (JWT, CORS, rate-limiting, caching) | `references/plugins.md` |
| Setting up routes, services, Admin API, upstreams | `references/routes-services.md` |
| Rate limiting strategies or consumer management | `references/consumers.md` |
