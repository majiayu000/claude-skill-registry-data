---
name: cloud-sql-psc-ports
description: Cloud SQL PSC port mapping — MySQL vs PostgreSQL, direct connection vs Auth Proxy. Captures that Auth Proxy for PostgreSQL uses port 3307, not 5432.
---

# Cloud SQL PSC Port Reference

## Overview

Domain knowledge about Cloud SQL Private Service Connect (PSC) port mapping for MySQL and PostgreSQL. Captures the non-obvious insight that Cloud SQL Auth Proxy uses different ports than the database default.

## MySQL PSC Ports

| Port | Purpose |
|------|---------|
| 3306 | Direct connection / Managed Connection Pooling |
| 3307 | Cloud SQL Auth Proxy |

## PostgreSQL PSC Ports

| Port | Purpose |
|------|---------|
| 5432 | Direct connection |
| 6432 | PgBouncer (Managed Connection Pooling) |
| 3307 | Cloud SQL Auth Proxy (NOT 5432) |

## Key Insight

**Auth Proxy for PostgreSQL uses port 3307 for outbound connections**, not PostgreSQL's default 5432.

Traffic path:
```
Pod → Auth Proxy (local:5432) → PSC Endpoint (:3307) → Cloud SQL (:5432)
```

If NetworkPolicy only allows 5432, Auth Proxy outbound connections will be blocked even though the local proxy listens on 5432.

## Sources

- https://cloud.google.com/sql/docs/postgres/about-private-service-connect
- https://cloud.google.com/sql/docs/mysql/about-private-service-connect

## Trigger

Use when:
- Designing PSC-based Cloud SQL connectivity from GKE
- Debugging NetworkPolicy issues with Cloud SQL connections
- Investigating why only opening the database port (e.g., 5432) doesn't work with Auth Proxy
