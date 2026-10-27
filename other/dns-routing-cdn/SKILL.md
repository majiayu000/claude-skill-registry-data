---
name: dns-routing-cdn
description: "DNS architecture, latency-based routing, CDN caching hierarchies, and apex domain configuration."
---

# DNS & CDN Routing Protocol

1. Set appropriate TTL values (short during migrations, long for stable records).
2. Serve apex and subdomain traffic through an authoritative CDN.
3. Configure Cache-Control headers to maximize edge cache hit ratios.
