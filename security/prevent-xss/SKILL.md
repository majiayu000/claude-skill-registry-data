---
name: prevent-xss
description: Use when rendering user-supplied content in HTML, writing JavaScript that inserts data into the DOM, or building APIs whose responses are rendered in a browser.
source: 'OWASP XSS Prevention Cheat Sheet; OWASP DOM-based XSS Prevention Cheat Sheet (owasp.org/www-project-cheat-sheets); OWASP Top 10 2021 A03; CWE-79'
tags: [security, owasp, xss, cross-site-scripting, frontend, developer]
---

# Prevent XSS

Eliminate cross-site scripting by context-aware output encoding and a strict Content Security Policy — never trust user-supplied content as markup.

## Why This Is Best Practice

**Adopted by:** Mandated by PCI DSS v4.0 Requirement 6.2.4 and OWASP Top 10 2021 (A03:Injection). Google, Meta, and GitHub all use context-aware escaping combined with CSP. React, Vue, Angular, and Svelte escape by default for text content. OWASP lists XSS as one of the most prevalent web vulnerabilities with over 20,000 CVEs.
**Impact:** XSS enables session hijacking, credential theft, and full account takeover without any server-side vulnerability. Google's Bug Bounty program pays up to $31,337 for stored XSS. OWASP estimates XSS affects two-thirds of all web applications. Consistent output encoding reduces XSS to near-zero as a vulnerability class.
**Why best:** Input sanitization (stripping tags on input) is the alternative — it fails to handle all encoding variations and breaks legitimate content. Output encoding at render time is context-specific and structurally correct regardless of how data was stored.

Sources: OWASP XSS Prevention Cheat Sheet; CWE-79; Google Bug Bounty data; OWASP Top 10 2021

## Steps

1. **Use a framework that auto-escapes by default** — React (`{}` expressions), Vue (`{{ }}`), Angular (`{{ }}`), and Jinja2 (`{{ }}`) escape HTML entities automatically. Never use `dangerouslySetInnerHTML`, `v-html`, `[innerHTML]`, or `| safe` unless the content is provably safe.

2. **When rendering outside a framework, encode for context**:

   - **HTML body context** — encode `&`, `<`, `>`, `"`, `'` as HTML entities.
   - **HTML attribute context** — encode all non-alphanumeric characters as `&#xHH;`.
   - **JavaScript context** — encode data placed inside `<script>` tags using `\uXXXX` escaping; prefer `data-*` attributes over inline scripts.
   - **URL context** — percent-encode values placed in `href`, `src`, or query strings; validate that URLs start with `https://` not `javascript:`.
   - **CSS context** — avoid dynamic CSS values from user input entirely.

3. **Never trust `innerHTML`, `document.write`, or `eval` with user data** — use `textContent` for plain text, `createElement`/`setAttribute` for DOM construction.

   ```javascript
   // BAD
   element.innerHTML = userInput;

   // GOOD
   element.textContent = userInput;

   // GOOD — building elements safely
   const a = document.createElement('a');
   a.href = sanitizedUrl;   // validate URL scheme first
   a.textContent = userInput;
   ```

4. **Deploy a Content Security Policy** — see `apply-content-security-policy`. CSP is defense-in-depth: it limits the damage of any XSS that slips through by blocking script execution from unexpected origins.

5. **For rich-text user content (Markdown, HTML editors)** — use a dedicated sanitization library on the *output* side, not input side. Allowlist-based: DOMPurify (browser), bleach (Python), sanitize-html (Node). Never build your own HTML parser.

   ```javascript
   import DOMPurify from 'dompurify';
   element.innerHTML = DOMPurify.sanitize(userHtml, { ALLOWED_TAGS: ['b', 'i', 'a'] });
   ```

6. **Set `HttpOnly` and `Secure` flags on session cookies** — `HttpOnly` prevents JavaScript from reading the cookie even if XSS occurs, limiting the blast radius.

## Rules

- The six encoding contexts (HTML, attribute, JavaScript, URL, CSS, JSON) each require different encoding — one-size escaping is wrong.
- JSON responses served to browsers must set `Content-Type: application/json` (not `text/html`) to prevent MIME sniffing and JSON injection.
- DOM-based XSS occurs when JavaScript reads `location.hash`, `document.referrer`, or `postMessage` and injects it into the DOM — treat these as untrusted sources.

## Common Mistakes

- **Using HTML entity encoding inside a `<script>` block** — JavaScript context requires JavaScript string escaping, not HTML entity encoding.
- **Sanitizing on input** — strips content the user legitimately entered, fails to prevent stored-then-rendered XSS from bypassed filters.
- **Trusting `href` values** — `javascript:alert(1)` is a valid URL. Always validate URL scheme.
