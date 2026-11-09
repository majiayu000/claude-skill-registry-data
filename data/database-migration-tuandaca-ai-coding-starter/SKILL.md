---
name: database-migration
description: Safe database schema evolution, migration strategies, rollback procedures, and zero-downtime deployments
---

# Database Migration Skill

This skill provides guidance on safe database schema evolution.

## Migration Principles

- Always backward-compatible first
- Idempotent migration scripts
- Transactional DDL where supported
- Test migrations on production-scale data
- Clear rollback procedures

## Strategies

- Expand-contract pattern for zero-downtime
- Shadow tables for large migrations
- Online schema change tools (gh-ost, pt-osc)
- Migration versioning and tracking

## Safety

- Pre-deployment validation checks
- Automated rollback triggers
- Data integrity verification
- Point-in-time recovery readiness
