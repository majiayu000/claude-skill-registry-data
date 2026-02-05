---
name: TanStack Start
description: |
  Build full-stack React applications with TanStack Start on Cloudflare Workers. Type-safe routing, server functions, SSR/streaming, and seamless D1/KV/R2 integration.

  Use when: building full-stack React apps, need SSR with Cloudflare Workers, want type-safe server functions, or migrating from Next.js.

  RC status - v1.0 stable pending. Monitor tanstack/router#5734 (memory leak) before production use.
allowed-tools: [Bash, Read, Write, Edit]
---

# TanStack Start Skill [DRAFT - NOT READY]

⚠️ **Status: Release Candidate - Monitoring for Stability**

This skill is prepared but NOT published. Waiting for:
- ⏸️ v1.0 stable release (currently RC v1.145.3 as of 2026-01-03)
- ❌ GitHub #5734 resolved (memory leak with TanStack Form - **STILL OPEN**, last activity Nov 20, 2025, related PR tanstack/form#1866)
- ⏸️ Critical bugs stabilization period
- ⏸️ Template/reference content creation

**Current Package:** `@tanstack/react-start@1.145.3` (Jan 2026)

**DO NOT USE IN PRODUCTION YET** - RC status, active memory leak issue

**Issue #5734 Summary**: Memory leak when using TanStack Form with TanStack Start. Pages with forms leak memory on repeated loads, causing server crashes (~30 min). Heap snapshots show retained object references preventing GC.

---

## Skill Overview

TanStack Start is a full-stack React framework with:
- Client-first architecture with opt-in SSR
- Built on TanStack Router (type-safe routing)
- Server functions for API logic
- Official Cloudflare Workers support
- Integrates with TanStack Query

---

## When v1.0 Stable

This skill will provide:
- Cloudflare Workers + D1/KV/R2 setup
- Server function patterns
- SSR vs CSR strategies
- Migration guide from Next.js
- Known issues and solutions

---

## Monitoring

Track stability at: `planning/stability-tracker.md`

**Check weekly:**
- Package: `npm view @tanstack/react-start version`
- [TanStack Start Releases](https://github.com/TanStack/router/releases)
- [Issue #5734](https://github.com/TanStack/router/issues/5734) - Memory leak blocker

---

## Installation (When Ready)

```bash
npm create cloudflare@latest -- --framework=tanstack-start
```

---

**Last Updated:** 2026-01-03
**RC Announced:** September 22, 2025
**Expected Stable:** Pending issue #5734 resolution + final RC feedback
**Monitoring:** Issue #5734 still open (last activity Nov 20, 2025). Related PR #1866 in TanStack Form repo.
