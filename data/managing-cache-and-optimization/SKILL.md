---
name: managing-cache-and-optimization
description: Use when managing Shannon CLI performance and costs - check cache statistics, clear stale entries, set budgets, understand automatic model selection and cost optimization
---

# Managing Cache and Optimization

## Overview

Shannon CLI provides automatic caching and cost optimization across all operations.

## Cache Management

**Check statistics**:
```bash
shannon cache stats
```
Shows: Hit rate, size, savings (USD and time)

**Clear cache**:
```bash
shannon cache clear         # All caches
shannon cache clear --type analysis  # Just analysis cache
```

**Cache layers** (3 tiers):
- Analysis: 7-day TTL
- Command: 30-day TTL
- MCP: Indefinite

**Performance targets**:
- Hit rate: >60% (good), >80% (excellent)
- Cache speed: <500ms
- Size: <500MB total

## Cost Optimization

**Set budget**:
```bash
shannon budget set 10.00  # $10 limit
shannon budget status     # Check spending
```

**Automatic model selection**:
- Simple tasks → haiku (cheapest)
- Complex tasks → sonnet (balanced)
- Auto-selected per complexity

**View optimization**:
```bash
shannon optimize
```
Shows: Potential savings, model recommendations

## Quick Reference

| Command | Purpose |
|---------|---------|
| cache stats | View hit rates and savings |
| cache clear | Clear stale entries |
| budget set N | Set spending limit |
| budget status | Check remaining budget |
| optimize | View cost-saving suggestions |

## When to Clear Cache

- After Shannon Framework updates
- Cache size >400MB
- Hit rate <40% (stale entries)
- Debugging cache-related issues
