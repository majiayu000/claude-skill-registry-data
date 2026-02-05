---
name: GithubPages
description: Complete GitHub Pages deployment and management system. Static site hosting with Jekyll, custom domains, and GitHub Actions. USE WHEN user mentions 'github pages', 'deploy static site', 'host website on github', 'jekyll site', 'custom domain for github', OR wants to publish a website from a repository.
---

# GitHub Pages Skill

Complete guide for deploying, configuring, and managing GitHub Pages sites.

## Quick Reference

| Site Type | Repository Name | URL Pattern |
|-----------|----------------|-------------|
| User/Org Site | `<username>.github.io` | `https://<username>.github.io` |
| Project Site | Any repository name | `https://<username>.github.io/<repo>` |

**Availability:**
- Public repos: GitHub Free (all plans)
- Private repos: GitHub Pro, Team, Enterprise

---

## Workflow Routing

**When executing a workflow, output this notification directly:**

```
Running the **WorkflowName** workflow from the **GithubPages** skill...
```

| Workflow | Trigger | File |
|----------|---------|------|
| **QuickStart** | "setup github pages", "create pages site" | `workflows/QuickStart.md` |
| **CustomDomain** | "add custom domain", "configure domain" | `workflows/CustomDomain.md` |
| **JekyllSetup** | "setup jekyll", "add jekyll theme" | `workflows/JekyllSetup.md` |
| **ActionsWorkflow** | "custom build", "github actions for pages" | `workflows/ActionsWorkflow.md` |
| **Troubleshoot** | "pages not working", "fix github pages" | `workflows/Troubleshoot.md` |
| **Deploy** | "deploy to github pages", "publish site" | `workflows/Deploy.md` |

---

## Examples

**Example 1: Create a new GitHub Pages site**
```
User: "Setup GitHub Pages for my project"
→ Invokes QuickStart workflow
→ Checks if user/org or project site
→ Configures publishing source (branch or Actions)
→ Creates initial content structure
→ Verifies deployment
```

**Example 2: Add custom domain**
```
User: "Add my domain example.com to GitHub Pages"
→ Invokes CustomDomain workflow
→ Determines domain type (apex vs subdomain)
→ Provides DNS configuration instructions
→ Adds CNAME file or configures via Settings
→ Enables HTTPS enforcement
```

**Example 3: Setup Jekyll theme**
```
User: "Add a theme to my GitHub Pages site"
→ Invokes JekyllSetup workflow
→ Lists available supported themes
→ Configures _config.yml
→ Sets up custom CSS/layouts if needed
```

**Example 4: Deploy with custom build**
```
User: "Deploy my Next.js site to GitHub Pages"
→ Invokes ActionsWorkflow workflow
→ Creates custom GitHub Actions workflow
→ Configures build process
→ Sets up artifact deployment
```

---

## Site Types

### User/Organization Site

**Requirements:**
- Repository name MUST be `<username>.github.io`
- Only ONE per account
- Publishes from default branch

**Setup:**
```bash
# Create repository named exactly: username.github.io
# Enable Pages in Settings > Pages
# Select source branch
```

### Project Site

**Requirements:**
- Can use any repository
- Multiple project sites allowed
- URL includes repository name

**Setup:**
```bash
# Any repository works
# Enable Pages in Settings > Pages
# Choose: branch (root or /docs) OR GitHub Actions
```

---

## Publishing Sources

### Option 1: Deploy from Branch

**Best for:** Jekyll sites, simple static sites

**Configuration:**
1. Go to Settings > Pages
2. Select "Deploy from a branch"
3. Choose branch (main, gh-pages, etc.)
4. Choose folder: `/` (root) or `/docs`

**Behavior:**
- Pushes to branch trigger automatic builds
- Jekyll processes Markdown by default
- CNAME file auto-created for custom domains

### Option 2: GitHub Actions Workflow

**Best for:** Custom builds, non-Jekyll generators

**Configuration:**
1. Go to Settings > Pages
2. Select "GitHub Actions"
3. Create workflow file in `.github/workflows/`

**Behavior:**
- Full control over build process
- Works with Hugo, Gatsby, Next.js, etc.
- Artifacts uploaded and deployed

---

## Jekyll Integration

### Auto-Enabled Plugins

These plugins work automatically on GitHub Pages:

| Plugin | Purpose |
|--------|---------|
| jekyll-coffeescript | CoffeeScript support |
| jekyll-default-layout | Automatic layouts |
| jekyll-gist | GitHub Gist embedding |
| jekyll-github-metadata | Repository metadata |
| jekyll-optional-front-matter | Optional YAML front matter |
| jekyll-paginate | Pagination |
| jekyll-readme-index | README as index |
| jekyll-titles-from-headings | Auto-generate titles |
| jekyll-relative-links | Convert relative links |

### Supported Themes

Available without additional configuration:

- Architect
- Cayman
- Dinky
- Hacker
- Leap day
- Merlot
- Midnight
- Minima
- Minimal
- Modernist
- Slate
- Tactile
- Time machine

**Usage in `_config.yml`:**
```yaml
theme: jekyll-theme-minimal
title: My Site
description: Site description
```

### Remote Themes

Use any Jekyll theme from GitHub:

```yaml
remote_theme: owner/repo-name
```

---

## Custom Domains

### Domain Types

| Type | Example | DNS Record |
|------|---------|------------|
| Apex | `example.com` | A or ALIAS |
| WWW Subdomain | `www.example.com` | CNAME |
| Custom Subdomain | `blog.example.com` | CNAME |

### DNS Configuration

**For Apex Domains (A Records):**
```
185.199.108.153
185.199.109.153
185.199.110.153
185.199.111.153
```

**For Apex Domains (AAAA Records - IPv6):**
```
2606:50c0:8000::153
2606:50c0:8001::153
2606:50c0:8002::153
2606:50c0:8003::153
```

**For Subdomains (CNAME Record):**
```
www.example.com → username.github.io
blog.example.com → username.github.io
```

### Verification Commands

```bash
# Check A records
dig example.com +noall +answer -t A

# Check AAAA records
dig example.com +noall +answer -t AAAA

# Check CNAME records
dig www.example.com +nostats +nocomments +nocmd
```

---

## Usage Limits

| Resource | Limit |
|----------|-------|
| Repository size | 1 GB (recommended) |
| Published site size | 1 GB (maximum) |
| Bandwidth | 100 GB/month (soft) |
| Builds | 10/hour (soft, branch only) |
| Deployment timeout | 10 minutes |

**Restrictions:**
- No server-side languages (PHP, Python, Ruby)
- No commercial transactions or e-commerce
- Must comply with GitHub Terms of Service

---

## Security Best Practices

1. **Verify custom domains** - Prevents domain takeover attacks
2. **Avoid wildcard DNS** - `*.example.com` creates security risks
3. **Enable HTTPS** - Always enforce HTTPS after certificate provisioning
4. **Don't expose secrets** - Public sites accessible even from private repos
5. **Update DNS promptly** - If disabling site, update/remove DNS records

---

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Site not publishing | Check branch/folder settings, verify entry file exists |
| 404 errors | Ensure `index.html`, `index.md`, or `README.md` at root |
| Custom domain not working | Wait 24h for DNS propagation, verify records with `dig` |
| HTTPS not available | Wait up to 1 hour after DNS verification |
| Mixed content warnings | Change `http://` to `https://` in all assets |
| Build failures | Check Actions tab for error logs |

---

## File References

| Topic | Reference File |
|-------|----------------|
| DNS Configuration | `references/DnsConfiguration.md` |
| Jekyll Configuration | `references/JekyllConfiguration.md` |
| Actions Workflows | `references/ActionsWorkflows.md` |
| Troubleshooting Guide | `references/Troubleshooting.md` |
| Best Practices | `references/BestPractices.md` |

---

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/verify-dns.sh` | Verify DNS configuration for custom domains |
| `scripts/check-site-status.sh` | Check if GitHub Pages site is live |

---

## External Documentation

- [GitHub Pages Quickstart](https://docs.github.com/en/pages/quickstart)
- [Custom Domain Configuration](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site)
- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [GitHub Actions for Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
