---
name: cloudflare-production
description: Production launch, DNS, SSL/TLS, Caching, WAF, Turnstile, and Edge configuration with Cloudflare for LKDV.
---

# Cloudflare Production Configuration & Launch

This skill provides procedures and standards for managing Cloudflare services (DNS, SSL/TLS, CDN, WAF, Workers, Turnstile) in production for Le Kit du Voyageur (LKDV).

## 1. Architecture & DNS Setup

- **Domain Apex & CNAME Flattening**:
  - Root domain `kitduvoyageur.com` and `www.kitduvoyageur.com` proxied through Cloudflare (Orange Cloud enabled).
  - Vercel origin configuration: CNAME `cname.vercel-dns.com` with proxy active or direct DNS based on SSL edge termination strategy.
- **SSL/TLS Encryption**:
  - Encryption mode: **Full (Strict)**. Never set to `Flexible` or `Off`.
  - Always Use HTTPS: **On**.
  - Minimum TLS Version: **TLS 1.3** (or 1.2 minimum fallback).
  - HTTP Strict Transport Security (HSTS): Enabled with `max-age=31536000; includeSubDomains; preload`.

## 2. Caching & Performance Rules

- **Static Assets (`/_next/static/*`, `/images/*`, `/fonts/*`)**:
  - Edge Cache TTL: 1 month (`cache-control: public, max-age=31536000, immutable`).
  - Cache Level: Cache Everything.
- **HTML & Dynamic Routes (`/compas`, `/compte`, `/api/*`)**:
  - Bypass cache (`Cache-Control: private, no-cache, no-store, must-revalidate`).
  - Never cache responses with `Set-Cookie` headers (especially Supabase auth session tokens).
- **Map & Geospatial Tiles (OSM / OpenFreeMap / Photon proxies)**:
  - Cache edge: 7 days for vector/raster tiles without personal data.

## 3. Security, WAF & Bot Protection

- **Turnstile Integration**:
  - Use Cloudflare Turnstile for user sign-in, sign-up, password reset, and public forms.
  - Server-side secret verification in API routes (`challenges.cloudflare.com/turnstile/v0/siteverify`).
- **WAF Rules (Web Application Firewall)**:
  - Block known malicious user agents and scrapers.
  - Rate limiting on `/api/auth/*` and AI endpoints (`/api/ai/*`): max 20 req/min per IP.
  - Geo-blocking / Managed challenge for high-risk autonomous ASN networks.
- **DDoS Mitigation**:
  - Cloudflare Under Attack Mode ready for emergency activation.

## 4. MCP & CLI Operations

- **Cloudflare MCP Server**:
  - Used to query DNS records, inspect worker scripts, verify cache status, and manage KV/R2 storage.
- **Wrangler CLI**:
  - Inspect deployments: `wrangler status`
  - Secrets management: `wrangler secret put <KEY>`
  - Tail logs: `wrangler tail`
