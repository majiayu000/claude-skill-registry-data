---
name: vercel-infrastructure
description: Use when setting up Vercel projects, configuring blob storage, managing environment variables, or setting up custom domains with wildcard subdomains. Critical for avoiding env var loss and understanding wildcard routing requirements.
---

# Vercel Infrastructure Setup

## Overview

Guide for setting up Vercel infrastructure including blob storage, environment variables, custom domains, and wildcard subdomain routing. Contains critical warnings about common pitfalls that can cause data loss.

## Critical Warnings

### ⚠️ `vercel env pull` OVERWRITES .env.local

**This is the most dangerous pitfall.** Running `vercel env pull` completely replaces your local `.env.local` file. Any variables not stored in Vercel will be LOST.

```bash
# DANGER: This will DELETE any local-only variables
vercel env pull .env.local --yes
```

**What gets lost:**
- `DATABASE_URL` if you added it locally
- `AUTH_SECRET` if generated locally
- Any other vars not in Vercel

### Best Practice: Vercel as Source of Truth

**NEVER add variables only to `.env.local`.** Always:

1. Add to Vercel first: `echo "value" | vercel env add VAR_NAME production`
2. Then pull: `vercel env pull .env.local --yes`

This ensures `vercel env pull` never loses variables.

### Recovery if Variables Lost

If you accidentally overwrote `.env.local`:

```bash
# Recover DATABASE_URL from Neon
neonctl set-context --org-id <org-id>
neonctl projects list
neonctl connection-string --project-id <project-id>

# Generate new AUTH_SECRET
openssl rand -base64 32

# Add recovered values to Vercel, then pull
echo "<value>" | vercel env add DATABASE_URL production
vercel env pull .env.local --yes
```

### Fix Newline Escaping Issue

Vercel env pull sometimes adds `\n` at end of values:

```bash
sed -i '' 's/\\n"$/"/g' .env.local
```

## Project Setup

### Link Project

```bash
vercel link --yes
```

This creates `.vercel/project.json` with project and org IDs.

### Add .vercelignore

Prevent deployment errors from special files:

```
.beads/
.neon/
```

Socket files (like `.beads/bd.sock`) cause "Unknown system error -102" during deployment.

## Blob Storage

### Create Blob Store

```bash
vercel blob store add <store-name>
```

This automatically:
- Creates the blob store
- Adds `BLOB_READ_WRITE_TOKEN` to your Vercel project

### Pull Token Locally

```bash
vercel env pull .env.local --yes
```

### Usage in Code

```typescript
import { put, del } from "@vercel/blob";

// Upload file
const blob = await put(`${userId}/${versionId}/index.html`, content, {
  access: "public",
  addRandomSuffix: false,
});

// Delete file
await del(blob.url);
```

## Environment Variables

### Add Variable to All Environments

```bash
echo "value" | vercel env add VAR_NAME production
echo "value" | vercel env add VAR_NAME preview
echo "value" | vercel env add VAR_NAME development
```

### List Variables

```bash
vercel env ls
```

### Remove Variable

```bash
vercel env rm VAR_NAME production -y
```

### Required Variables for Typical App

| Variable | Source | Notes |
|----------|--------|-------|
| `DATABASE_URL` | Neon CLI or dashboard | `neonctl connection-string --project-id <id>` |
| `AUTH_SECRET` | Generate | `openssl rand -base64 32` |
| `BLOB_READ_WRITE_TOKEN` | Auto-added | Created with blob store |
| `NEXT_PUBLIC_*` | Manual | Client-visible vars need this prefix |

## Custom Domains

### Default Domain Limitation

**Vercel's `.vercel.app` domain does NOT support wildcard subdomains.**

- ✅ `project.vercel.app` works
- ❌ `subdomain.project.vercel.app` does NOT work

For wildcard subdomain routing, you MUST use a custom domain.

### Add Custom Domain

```bash
# Add root domain
vercel domains add yourdomain.com

# Add wildcard domain
vercel domains add "*.yourdomain.com"
```

### ⚠️ CRITICAL: Wildcard Domains Require Nameservers

**This is the most common wildcard setup failure.**

For **wildcard domains** (`*.yourdomain.com`), CNAME records are NOT sufficient. You MUST delegate your domain to Vercel's nameservers.

**Root domain only** (no wildcards):
| Type | Host | Value |
|------|------|-------|
| A | @ | `216.198.79.1` |

**Wildcard domains** - Change nameservers at your registrar to:
| Nameserver |
|------------|
| `ns1.vercel-dns.com` |
| `ns2.vercel-dns.com` |

**Why nameservers are required for wildcards:**
- CNAME records cannot be set on the root domain (DNS limitation)
- Wildcard SSL certificates require Vercel to control DNS
- Vercel dashboard will show "Invalid Configuration" until nameservers are updated

### DNS Configuration Options

**Option 1: Nameservers (Required for wildcards)**
- Go to your registrar (Namecheap, GoDaddy, etc.)
- Find "Nameservers" or "DNS" settings
- Change from default to "Custom DNS"
- Add `ns1.vercel-dns.com` and `ns2.vercel-dns.com`
- Vercel will manage all DNS records

**Option 2: A/CNAME Records (Root domain only, no wildcards)**
| Type | Host | Value |
|------|------|-------|
| A | @ | `216.198.79.1` |
| CNAME | www | `cname.vercel-dns.com` |

Note: Vercel's IP addresses are being updated. Old values (`76.76.21.21`, `cname.vercel-dns.com`) still work but new IPs are recommended.

### SSL Certificates

Vercel creates SSL certificates asynchronously. After adding domains:
- Root domain SSL: Usually immediate
- Wildcard SSL: May take several minutes after nameservers propagate

Check status:
```bash
curl -v https://test.yourdomain.com/ 2>&1 | grep -i ssl
```

### Domain Status in Dashboard

Check the Vercel dashboard for domain status:
- ✅ Green checkmark = Working
- ⚠️ "Invalid Configuration" = Nameservers not set (for wildcard)
- ⚠️ "DNS Change Recommended" = Working but could be optimized

### Nameserver Propagation

After changing nameservers:
- Can take 1-48 hours to fully propagate
- Check propagation: `dig NS yourdomain.com`
- Vercel dashboard will update when it detects the change

## Wildcard Subdomain Routing

### Make Domain Configurable

Store domain in environment variable for flexibility:

```typescript
// lib/routing.ts
export const APP_DOMAIN = process.env.NEXT_PUBLIC_APP_DOMAIN || "localhost";

export function extractSubdomain(hostname: string): string | null {
  const host = hostname.split(":")[0];

  // Local development
  if (host === "localhost" || host.endsWith(".localhost")) {
    const parts = host.split(".");
    if (parts.length === 2 && parts[1] === "localhost") {
      return parts[0];
    }
    return null;
  }

  // Production - works with any domain length
  const domainParts = APP_DOMAIN.split(".");

  if (host === APP_DOMAIN) return null;

  if (host.endsWith("." + APP_DOMAIN)) {
    const hostParts = host.split(".");
    const subdomainParts = hostParts.length - domainParts.length;

    if (subdomainParts === 1) {
      const subdomain = hostParts[0];
      return subdomain === "www" ? null : subdomain;
    }

    if (subdomainParts === 2 && hostParts[0] === "www") {
      return hostParts[1];
    }
  }

  return null;
}
```

This works with both 2-part (`canvas.site`) and 3-part (`project.vercel.app`) domains without code changes.

### Update Domain

When switching domains, only change the env var:

```bash
vercel env rm NEXT_PUBLIC_APP_DOMAIN production -y
echo "newdomain.com" | vercel env add NEXT_PUBLIC_APP_DOMAIN production
vercel deploy --prod
```

## Deployment

### Deploy to Production

```bash
vercel deploy --prod
```

### Common Deployment Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `Unknown system error -102` | Socket file in upload | Add to `.vercelignore` |
| `ENOENT` on env var | Variable not set | Add via `vercel env add` |
| Build fails | Missing env var at build | Ensure var exists for all environments |

## CLI Tools Reference

### Vercel CLI

```bash
vercel link                    # Link to project
vercel env ls                  # List env vars
vercel env add NAME ENV        # Add var (pipe value via stdin)
vercel env rm NAME ENV -y      # Remove var
vercel env pull .env.local     # Pull to local (OVERWRITES!)
vercel deploy --prod           # Deploy to production
vercel domains add DOMAIN      # Add domain
vercel domains ls              # List domains
vercel blob store add NAME     # Create blob store
```

### Neon CLI

```bash
neonctl set-context --org-id ID      # Set org context
neonctl projects list                 # List projects
neonctl connection-string --project-id ID  # Get DATABASE_URL
neonctl branches list --project-id ID      # List branches
```

## Checklist: New Vercel Project

- [ ] `vercel link --yes`
- [ ] Create `.vercelignore` with `.beads/`, `.neon/`
- [ ] Add all env vars to Vercel FIRST
- [ ] `vercel env pull .env.local --yes`
- [ ] Fix newlines: `sed -i '' 's/\\n"$/"/g' .env.local`
- [ ] `vercel blob store add <name>` (if needed)
- [ ] Pull again to get blob token
- [ ] `vercel deploy --prod`

### If Wildcard Subdomains Needed:

- [ ] `vercel domains add yourdomain.com`
- [ ] `vercel domains add "*.yourdomain.com"`
- [ ] **Change nameservers** at registrar to `ns1.vercel-dns.com` and `ns2.vercel-dns.com`
- [ ] Wait for nameserver propagation (1-48 hours)
- [ ] Check Vercel dashboard - wildcard should show ✅ not "Invalid Configuration"
- [ ] Wait for SSL certificate provisioning
- [ ] Test: `curl https://test.yourdomain.com/`
