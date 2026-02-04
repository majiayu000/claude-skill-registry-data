---
name: Cloudflare DNS Analytics
description: This skill should be used when the user asks about "DNS performance", "zone settings", "DNS analytics", "domain configuration", "DNS report", "zone list", "DNS troubleshooting", "DNSSEC", "DNS latency", or needs to monitor and optimize Cloudflare DNS.
version: 1.0.0
---

# Cloudflare DNS Analytics

Monitor DNS performance and configuration using the DNS Analytics MCP server.

## Available Tools

| Tool | Purpose |
|------|---------|
| `zones_list` | List all zones under the active account |
| `dns_report` | Get DNS performance report for a zone over a time period |
| `show_account_dns_settings` | View DNS settings at the account level |
| `show_zone_dns_settings` | View DNS settings for a specific zone |

## Common Workflows

### DNS Health Check
1. Use `zones_list` to identify zones
2. Use `dns_report` for each zone to check performance
3. Review metrics for latency, query volume, errors

### Configuration Audit
1. Use `show_account_dns_settings` for account-level settings
2. Use `show_zone_dns_settings` for zone-specific settings
3. Compare settings across zones for consistency

### Performance Investigation
1. Identify the zone with `zones_list`
2. Pull `dns_report` for the relevant time frame
3. Analyze query patterns and response times

## DNS Report Metrics

The DNS report typically includes:
- Query volume over time
- Response time distribution
- Query types (A, AAAA, CNAME, etc.)
- Response codes (NOERROR, NXDOMAIN, etc.)
- Geographic distribution

## Integration with Workers

For Workers using custom domains:
1. Verify zone configuration with `show_zone_dns_settings`
2. Check DNS report for the zone
3. Correlate with Workers observability data

## Troubleshooting

| Issue | Investigation Steps |
|-------|---------------------|
| Slow DNS resolution | Check `dns_report` for latency metrics |
| Missing records | Verify `show_zone_dns_settings` |
| High error rates | Review response codes in `dns_report` |
| Zone not found | List zones with `zones_list` |

## Tips

- Zone IDs from `zones_list` are needed for other operations
- DNS reports can span custom time ranges
- Account settings may override zone settings
- Use with observability tools for full-stack debugging
