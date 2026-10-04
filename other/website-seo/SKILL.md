---
name: website-seo
description: Domain binding, SSL setup, Cloudflare DNS, search engine submission, sitemap management, and Windows shared hosting FTP workflows
triggers:
  - bind domain to github pages
  - cloudflare ssl 525 error
  - cloudflare origin server a record proxy
  - submit sitemap to google
  - baidu verification
  - yandex verification
  - nginx 403 directory index forbidden
  - nginx url rewrite query string
  - mysql root password ubuntu 8.0
  - install mysql on ubuntu
  - classic asp iis to linux migration
  - admin_v19 asp backend not running
  - sync static files between servers
  - create index.html for directory listing
  - biweekly cron sync script
  - canonical points to github io instead of production domain
  - github pages seo custom domain
  - sitemap still has github io url after domain change
  - cloudflare overrides robots txt
  - git rebase conflict sitemap xml
---

# Website SEO & Administration

## Domain Binding (GitHub Pages → Custom Domain)

### GitHub Settings
1. Repository → Settings → Pages → Custom domain: `www.example.com`
2. Do NOT check "Enforce HTTPS" until after DNS verification completes

### Cloudflare DNS
| Type | Name | Target | Proxy |
|------|------|--------|-------|
| CNAME | www | `githubtalk.github.io` | DNS only (gray) during verification |

**Critical**: Keep DNS-only (gray cloud) while GitHub validates domain ownership. After GitHub issues HTTPS cert, re-enable proxy (orange cloud).

### Why Enforce HTTPS Is Optional with Cloudflare
Cloudflare Flexible/Full SSL already handles HTTP→HTTPS redirect at CDN level. GitHub's "Enforce HTTPS" does the same. If `https://www.example.com` works in browser, the checkbox is cosmetic.

---

## Cloudflare SSL 525 Error

**Symptom**: `HTTP 525 - SSL handshake failed`

**Root cause**: Origin server has no valid SSL certificate for the domain

**Quick fix**:
- Cloudflare → SSL/TLS → Mode: **Flexible**
- Visitor → Cloudflare: HTTPS ✅
- Cloudflare → Origin: HTTP (no cert needed) ✅

**Permanent fix**: Install Let's Encrypt on origin server (requires RDP/SSH access)

---

## Cloudflare Proxy → Origin Server Setup

When your origin is a VPS/root server (not GitHub Pages), Cloudflare proxies traffic to your server's IP.

### Step 1: Start web server on origin FIRST
```bash
# On origin server
sudo systemctl start nginx
sudo systemctl enable nginx
sudo ss -tlnp | grep -E ':80|:443'  # verify listening
curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1  # should NOT be 000
```

### Step 2: Check PHP-FPM if site returns 502 Bad Gateway
```bash
# If nginx serves 502, PHP-FPM is usually the cause
sudo systemctl status php8.3-fpm | grep "Active:"
# Check socket permissions
ls -la /run/php/php*-fpm.sock
# If permission denied in error log, fix:
sudo chmod 660 /run/php/php8.3-fpm.sock
sudo usermod -a -G www-data nginx
sudo systemctl restart nginx php8.3-fpm
```

**Step 2: Cloudflare DNS record**
| Type | Name | Target | Proxy |
|------|------|--------|-------|
| A | sub | `YOUR_SERVER_IP` | Proxied (☁️ orange) |

**Step 3: Verify**
```bash
# Test through Cloudflare (not direct IP)
curl -sI https://your-domain.com/ | grep cf-ray
```

Full reference: `references/cloudflare-origin-server.md`

---

## Nginx sites-enabled Gotcha (Ubuntu)

On Ubuntu, nginx configs go in `/etc/nginx/sites-enabled/` but **nginx.conf does not include it by default**. If nginx starts but serves nothing on port 80:

1. Check: `grep sites-enabled /etc/nginx/nginx.conf`
2. If missing, add inside `http {}` block: `include /etc/nginx/sites-enabled/*;`
3. Test: `sudo nginx -t`
4. Reload: `sudo systemctl reload nginx`

Note: The `include` line must be INSIDE the `http {}` block, not after the closing `}`. If you see `"server" directive is not allowed here`, the include is outside the http block.

## Creating Directory Index Pages

When migrating from ASP/PHP sites that generate listing pages dynamically, you may need to create static `index.html` for directories:

```bash
# Generate product list from existing HTML files
for f in /home/ubuntu/wwwroot/products/*.html; do
  id=$(basename "$f" .html)
  title=$(grep -oP '(?<=<title>)[^<]+' "$f" 2>/dev/null | head -1)
  echo "<li><a href=\"/products/$id.html\">$title</a></li>"
done > /tmp/product_list.txt

# Combine with HTML template
cat > /home/ubuntu/wwwroot/products/index.html << HTMLEOF
<!DOCTYPE html>
<html><head><title>Product Center</title></head>
<body>
<ul>
$(cat /tmp/product_list.txt)
</ul>
</body></html>
HTMLEOF
```

Key patterns:
- Extract title from each HTML file: `grep -oP '(?<=<title>)[^<]+' "$f"`
- Include navigation from main site
- Match the visual style of source site

See `references/website-sync-workflow.md` for full sync script template.

---

## Classic ASP (VBScript) Cannot Run on Linux

**Symptom**: ASP files in `/admin_v19/` return as plain text download or show directory listing instead of executing

**Root Cause**: Classic ASP (VBScript/Jet OLEDB, `.asp` files using `Server.CreateObject("ADODB.Connection")`) is **Windows IIS only**. Mono does not support Classic ASP — only ASP.NET (C#/VB.NET).

**Verification**:
```bash
# Check if file is being served as text (not executed)
curl -s "https://domain.com/admin_v19/login.asp" | head -5
# If you see VBScript code like <% ... %> returned as text, it's not executing

# Check server type
curl -sI "https://original-site.com/" | grep -i server
# IIS = Windows, nginx/apache = Linux
```

**Implications for Migration**:
| Original Stack | Target Stack | Classic ASP Backend |
|---------------|--------------|---------------------|
| Windows + IIS | Linux + Nginx | ❌ **Cannot migrate** — rewrite backend or keep Windows server |
| Windows + IIS | Windows + IIS | ✅ Works as-is |
| Linux + Apache | Linux + Nginx | ✅ Works (if ASP.NET, not Classic) |

**Migration Options**:
1. **Keep original server for admin** — Use `www.shengtuo-tractor.com/admin_v19/` for backend updates, sync static files to new server
2. **Rebuild backend** — Rewrite ASP admin in PHP/Laravel, point to MySQL database
3. **Use Windows VPS** — Keep IIS + Classic ASP, add Cloudflare in front

**Key files to check**:
- `Conn.asp` — Database connection string: `"Provider = Microsoft.Jet.OLEDB.4.0;Data Source="&server.mapPath(...)`
- This uses Microsoft Access-style Jet OLEDB, which is Windows-only

**Reference**: `references/classic-asp-iis-migration.md`

---

## Sitemap After Domain Change

**Problem**: Switched custom domain but sitemap.xml still has old URLs like `githubtalk.github.io/shengtuo-tractor/`

**Fix**:
1. Update `sitemap.xml` in the GitHub repository with new domain URLs
2. Also update `canonical`, JSON-LD `@id`/`url`, `og:url`, `og:image`, `twitter:image` — all must reference production domain
3. GitHub Pages automatically redirects `/sitemap.xml` from parked URL to custom domain
4. Search Console "Couldn't fetch" = CDN cache delay, refreshes in 2-5 min

> ⚠️ **Cloudflare can override robots.txt**: Cloudflare Dashboard Rules can control robots.txt at CDN level, ignoring your origin file. If changes don't appear, check Cloudflare Dashboard → Rules. See `references/github-pages-seo.md`.

---

## Baidu Verification

- Baidu web interface rejects `.html` file upload via browser (UI bug: "Unsupported document type")
- **Solution**: Upload verification file via FTP client to web root, then trigger file verification in Baidu console
- FTP upload to Windows shared hosting works where browser UI fails

---

## Yandex Verification

**File method**:
- Filename must be: `yandex_<code>.html` (underscore in middle, not underscore at start)
- Content must be full HTML wrapper, not plain text

**Example**:
```html
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
</head>
<body>Verification: 3fdba79f71c66d1b</body>
</html>
```

Upload via FTP, then trigger verification in Yandex Webmaster.

---

## Search Engine Submission Priority

| Engine | Priority | Tools |
|--------|----------|-------|
| Google | Must-do | search.google.com/search-console |
| Bing | High (Yahoo shared) | bing.com/webmasters |
| Yandex | Medium (Russia) | webmaster.yandex.com |
| Baidu | If China market | zhanzhang.baidu.com |

### Submission Checklist
1. Verify ownership (HTML tag / file / CNAME)
2. Submit sitemap URL: `https://www.example.com/sitemap.xml`
3. Ensure HTTPS works and canonical URLs are correct
4. Check coverage/index status after 1-3 days

---

## Verification Methods

### Choosing a Method

| Method | Best For | Limitations |
|--------|----------|-------------|
| **HTML tag** | Any site | Must be able to edit `<head>` |
| **Cloudflare授权** | Cloudflare-proxied sites | Only works for Google |
| **File upload** | FTP-accessible sites | Baidu only accepts .txt/.html |
| **CNAME** | Sites with Cloudflare blocking bots | Most reliable for Baidu |

### Google Verification

**HTML tag method** (most universal):
```bash
# Find the <head> tag in index.html, insert meta tag right after <title>
sed -i 's|<title>|<meta name="google-site-verification" content="XXXXX" />\n<title>|' index.html
git add index.html && git commit -m "Add Google verification" && git push
```

**Confirm tag is live** (allow 2-3 min for GitHub Pages rebuild):
```bash
curl -s "https://example.com/" | grep "verification_code"
```

### Baidu Verification (FTP)

Baidu file verification requires **raw text file** (no HTML wrapper):
```bash
# Create file with ONLY the verification code string
echo -n "codeva-XXXXX" > baidu_verify_codeva-XXXXX.html
curl -u "USER:PASS" -T baidu_verify_codeva-XXXXX.html "ftp://HOST/wwwroot/"
```

Verify:
```bash
curl -s "https://example.com/baidu_verify_codeva-XXXXX.html"
# Should return: codeva-XXXXX (plain text, no HTML)
```

### Yandex Verification

Filename must be `yandex_<code>.html` (underscore in middle, not at start):
```html
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
</head>
<body>Verification: 3fdba79f71c66d1b</body>
</html>
```

### Bing Verification

Use HTML tag method (same as Google):
```html
<meta name="msvalidate.01" content="YOUR_BING_CODE">
```

---

## References
- `references/cloudflare-ssl-modes.md`
- `references/cloudflare-origin-server.md`
- `references/seo-submission-checklist.md`
- `references/baidu-verify-ftp.md` — Baidu verification on Windows shared hosting (FTP upload, raw text file)
- `references/sitemap-template.md` — Optimized sitemap template with priorities
- `references/nginx-url-rewrite-static.md` — Rewriting query params (?id=X) to static HTML files
- `references/mysql-ubuntu-setup.md` — MySQL 8.0 on Ubuntu, root password reset via debian-sys-maint
- `references/classic-asp-iis-migration.md` — Classic ASP on Windows IIS, cannot run on Linux/Mono
- `references/website-sync-workflow.md` — Sync script for migrating static content between domains, creating directory index pages
- `references/github-pages-seo.md` — GitHub Pages custom domain SEO: canonical/sitemap/OG tags must point to production domain, Cloudflare overrides, git rebase conflicts