---
name: cloudflare
description: Manage Cloudflare infrastructure including DNS records, zones, SSL/TLS, caching, firewall rules, Workers, Pages, and analytics. Use when working with Cloudflare APIs, creating or modifying DNS records, managing domain security, purging cache, deploying Workers/Pages, or analyzing traffic. Created by After Dark Systems, LLC.
---

# Cloudflare Management Skill

**Created by After Dark Systems, LLC**

## Overview

This skill provides comprehensive Cloudflare infrastructure management capabilities through the Cloudflare API v4. It enables full control over domains, DNS, security, performance, and serverless deployments.

## Authentication

API credentials are stored at `~/cloudflare_global_key` (or override via `CF_CREDS_FILE` environment variable). The file contains:
- Global API Key for legacy authentication
- API Token (Bearer token) for modern authentication

**Security Best Practices**:
- Ensure file permissions are restricted: `chmod 600 ~/cloudflare_global_key`
- Consider using environment variables or credential managers (e.g., `pass`, 1Password, system keychains) for production environments
- Rotate API tokens regularly (recommended: every 90 days)
- Use API tokens with minimal required permissions rather than Global API keys

**Recommended**: Use the Bearer token for API calls:
```bash
-H "Authorization: Bearer <token>"
```

To verify token validity:
```bash
./scripts/cf-api.sh verify-token
```

## Available Scripts

All scripts are located in the `scripts/` directory and use the credentials from `~/cloudflare_global_key`.

### Core API Client
- **cf-api.sh** - Base API client with authentication handling

### Zone Management
- **zones.sh** - List, get, create, and manage zones
- **zone-settings.sh** - Manage zone-level settings

### DNS Management
- **dns.sh** - Full DNS record CRUD operations
- **dns-import.sh** - Bulk import DNS records
- **dns-export.sh** - Export DNS records

### Security & Firewall
- **firewall.sh** - Firewall rules management
- **waf.sh** - Web Application Firewall rules
- **rate-limiting.sh** - Rate limiting rules
- **ip-access.sh** - IP access rules (block/allow)
- **ssl.sh** - SSL/TLS configuration

### Performance & Caching
- **cache.sh** - Cache purge and settings
- **page-rules.sh** - Page rules management
- **speed.sh** - Speed optimizations (minify, polish, etc.)

### Workers & Pages
- **workers.sh** - Cloudflare Workers management
- **pages.sh** - Cloudflare Pages projects

### Analytics & Logs
- **analytics.sh** - Traffic and security analytics
- **logs.sh** - Enterprise log access

## Quick Start Examples

### List All Zones
```bash
./scripts/zones.sh list
```

### Get Zone Details
```bash
./scripts/zones.sh get <zone_id>
# or by domain name
./scripts/zones.sh get-by-name example.com
```

### List DNS Records
```bash
./scripts/dns.sh list <zone_id>
# Filter by type
./scripts/dns.sh list <zone_id> --type A
```

### Create DNS Record
```bash
./scripts/dns.sh create <zone_id> \
  --type A \
  --name subdomain \
  --content 192.0.2.1 \
  --ttl 3600 \
  --proxied true
```

### Update DNS Record
```bash
./scripts/dns.sh update <zone_id> <record_id> \
  --content 192.0.2.2 \
  --ttl 1800
```

### Delete DNS Record
```bash
./scripts/dns.sh delete <zone_id> <record_id>
```

### Purge Cache
```bash
# Purge everything
./scripts/cache.sh purge-all <zone_id>

# Purge specific URLs
./scripts/cache.sh purge-urls <zone_id> "https://example.com/page1" "https://example.com/page2"

# Purge by cache tags
./scripts/cache.sh purge-tags <zone_id> tag1 tag2
```

### SSL/TLS Settings
```bash
# Get current SSL mode
./scripts/ssl.sh get-mode <zone_id>

# Set SSL mode (off, flexible, full, strict)
./scripts/ssl.sh set-mode <zone_id> strict
```

### Firewall Rules
```bash
# List firewall rules
./scripts/firewall.sh list <zone_id>

# Block an IP
./scripts/ip-access.sh block <zone_id> 192.0.2.100 "Suspicious activity"

# Allow an IP
./scripts/ip-access.sh allow <zone_id> 192.0.2.50 "Trusted server"
```

### Workers
```bash
# List workers
./scripts/workers.sh list

# Deploy a worker
./scripts/workers.sh deploy <script_name> <script_file>

# Delete a worker
./scripts/workers.sh delete <script_name>
```

## OpenNext Cloudflare (Next.js Deployments)

For deploying Next.js applications to Cloudflare Workers, use the `opennextjs-cloudflare` CLI instead of direct wrangler commands.

**Documentation**: https://opennext.js.org/cloudflare
**GitHub**: https://github.com/opennextjs/opennextjs-cloudflare
**Discord**: https://discord.gg/opennext

### CLI Commands

The `opennextjs-cloudflare` CLI supports the following commands:

#### build
Builds the Next.js application and runs Cloudflare-specific build steps:
```bash
pnpm opennextjs-cloudflare build
# With options
pnpm opennextjs-cloudflare build --skipNextBuild --noMinify
# With wrangler options
pnpm opennextjs-cloudflare build --config=/path/to/wrangler.jsonc --env=prod
```

#### populateCache
Populates the configured Open Next cache components:
```bash
# Populate local bindings (for local development)
pnpm opennextjs-cloudflare populateCache local

# Populate remote bindings (for deployed application)
pnpm opennextjs-cloudflare populateCache remote
```

**Note**: This command is implicitly called by `preview`, `deploy`, and `upload` commands.

**R2 Batch Uploads** (v1.13.0+): Supported out of the box for `preview` and `deploy`.

For versions before 1.13.0, R2 batching via rclone requires:
- `R2_ACCESS_KEY_ID`: Access key ID of the R2 API token
- `R2_SECRET_ACCESS_KEY`: Secret access key of the R2 API token
- `CLOUDFLARE_ACCOUNT_ID`: Account ID where the R2 bucket is located

#### preview
Populates local cache and launches a local development server:
```bash
pnpm opennextjs-cloudflare preview
```

#### deploy
Populates remote cache and deploys to Cloudflare (application serves immediately):
```bash
pnpm opennextjs-cloudflare deploy
```

#### upload
Populates remote cache and uploads a version without serving (for gradual deployments):
```bash
pnpm opennextjs-cloudflare upload
```

### Getting Help
```bash
# List all commands
pnpm opennextjs-cloudflare

# Get help for a specific command
pnpm opennextjs-cloudflare <command> --help
```

### Important Notes

- **Do NOT use wrangler commands directly** unless documented or you know what you're doing
- Most commands accept wrangler options (e.g., `--config`, `--env`)
- Compatibility date should be set to `2025-03-07` or later
- Set `compatibility_flags = ["nodejs_compat"]` in wrangler.jsonc

## Common Workflows

### Setting Up a New Domain

1. Add the zone:
```bash
./scripts/zones.sh create example.com
```

2. Get the zone ID:
```bash
ZONE_ID=$(./scripts/zones.sh get-by-name example.com --id-only)
```

3. Add required DNS records:
```bash
./scripts/dns.sh create $ZONE_ID --type A --name @ --content 192.0.2.1 --proxied true
./scripts/dns.sh create $ZONE_ID --type CNAME --name www --content example.com --proxied true
./scripts/dns.sh create $ZONE_ID --type MX --name @ --content mail.example.com --priority 10
```

4. Configure SSL:
```bash
./scripts/ssl.sh set-mode $ZONE_ID strict
```

### Migrating DNS from Another Provider

1. Export current records from the source provider
2. Import to Cloudflare:
```bash
./scripts/dns-import.sh <zone_id> records.txt
```

### Emergency: Block Attack Traffic

```bash
# Block specific IP
./scripts/ip-access.sh block <zone_id> <attacker_ip> "Attack mitigation"

# Enable Under Attack Mode
./scripts/zone-settings.sh set <zone_id> security_level under_attack

# Purge cache if compromised content was cached
./scripts/cache.sh purge-all <zone_id>
```

## API Reference

See `reference.md` for complete Cloudflare API v4 documentation including:
- All available endpoints
- Request/response formats
- Error codes and handling
- Rate limiting information

## Templates

The `templates/` directory contains JSON templates for common operations:
- `dns-records.json` - Common DNS record configurations
- `firewall-rules.json` - Firewall rule templates
- `page-rules.json` - Page rule templates
- `worker-config.json` - Worker configuration template

## Error Handling

All scripts follow a consistent error code convention:
- 0: Success
- 1: API error (check stderr for Cloudflare error code and message)
- 2: Invalid arguments (missing or malformed parameters)
- 3: Authentication error (invalid or missing credentials)
- 4: Resource not found (zone, record, or rule doesn't exist)

**Note**: This is the recommended error-handling standard that all scripts in this skill implement. Error responses include the Cloudflare error code and message for debugging.

## Best Practices

1. **Always use proxied records** when possible for DDoS protection
2. **Use strict SSL mode** for full end-to-end encryption
3. **Set appropriate TTLs** - shorter for dynamic content, longer for static
4. **Test firewall rules** in log mode before enforcing
5. **Use API tokens** with minimal required permissions
6. **Cache aggressively** but purge when content changes
7. **Monitor analytics** for unusual traffic patterns

## Support

For issues with this skill, contact After Dark Systems, LLC.

For Cloudflare API documentation: https://developers.cloudflare.com/api/
