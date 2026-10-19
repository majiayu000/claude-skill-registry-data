---
name: footprinting
description: Fingerprint a web target's technology stack and immediately pivot into the tech-specific bug hunt — WordPress (wpscan/user-enum/xmlrpc/plugin CVEs), IIS (shortscan shortname 8.3, WebDAV, ViewState), SharePoint, Tomcat/Spring/Jenkins/GitLab/Jira, Laravel/ThinkPHP/Drupal/Joomla, Elasticsearch/Kibana, framework tells, git/env exposure — matched to CVE families and the right tools per stack. Use whenever a domain/subdomain/host is found during recon and you need to know what it runs and which known bugs to attack, when the user says "footprint", "what tech is this", "it's WordPress/IIS — go at it", "find CVEs for this stack", or hands over any URL to classify before testing.
---

# Footprinting — Tech Fingerprint → Known-Bug Attack Plan

The moment a domain resolves, classify it and pivot to the stack's known bug surface. One script + one matrix.

## Run the fingerprinter

```bash
python scripts/footprint.py https://target.com [--probe] [--out plan.md]
```
- Passive-ish pass (default): homepage + robots + one 404-shape probe, header/cookie/body signature matching against 23 tech rules, then cheap generic exposure checks (`/.git/HEAD`, `/.env`, `/backup.zip`, `composer.json`, …) with INTERESTING / blocked / clean labels.
- `--probe` adds paced confirmation probes per detected tech (wp-login, actuator, manager/html, `_layouts`, shortname `~a`, …) — ~1.3s apart.
- Output: a markdown plan — detected stack, per-tech bug families, confirm probes, and ready-to-run tool commands (wpscan/shortscan/nuclei/droopescan/joomscan/nikto with the target formatted in).

## Then read the matrix
Open `references/tech-matrix.md` and execute the section for every detected tech. The matrix is the aggressive layer the script can't be: **version pinning first, CVE matching second, tool ladder third, manual checks fourth.** Highlights:

- **WordPress**: wpscan full enum (users/plugins/themes/db-exports), REST author enumeration, xmlrpc pingback SSRF + system.multicall, debug.log/wp-config backups, staging twins via wayback.
- **IIS**: **shortscan** for 8.3 shortname disclosure (reconstruct config/backup filenames), WebDAV PROPFIND/PUT, trace.axd/elmah.axd, ViewState MAC check → ysoserial.net.
- **Spring**: actuator env/heapdump; **Tomcat**: manager, PUT JSP; **Jenkins**: CVE-2024-23897 CLI read; **Jira/Confluence**: OGNL/template CVE families by version.
- **Laravel**: `.env` + Ignition; **ThinkPHP**: invokefunction; **Elasticsearch/Kibana/Argo**: anon-API checks (this exact method found a live anon ES 2.4.4 cluster on a real hunt).
- **Any stack**: git/svn/env/backup/composer exposure ladder; Cloudflare in front → curl_cffi or CDP browser-pass.

## Workflow position
Run this on every alive host from recon (bb-pipeline Phase 1 output), and again whenever a new subdomain surfaces from wayback/VT pivots. Feed discovered JS bundles onward to js-recon/js-audit; feed CMS/plugin versions to CVE matching + the bb-disclosures corpus (`query.py --q "<tech>"`) to see what that stack actually paid for.

## Rules
- This is active testing: scope-check each host first, respect program rate limits and required headers.
- Version disclosure alone is usually a pre-declared dupe — chain to a working exploit before reporting (bb-chains).
- Deserialization/RCE proofs need explicit program permission; marker payloads only.
