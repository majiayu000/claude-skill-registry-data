---
name: recon-find-origin
description: "Origin IP discovery behind WAF/CDN via DNS history, subdomain leaks, certificate transparency, and misconfigurations"
category: "information-gathering"
version: "1.0"
author: "bountyreper-official"
tags:
  - recon
  - waf
  - origin-ip
  - cloudflare
  - dns
tech_stack:
  - web
cwe_ids:
  - CWE-200
chains_with:
  - recon-hunter
  - wstg-info-01
prerequisites: []
---

# Finding Origin IP Behind WAF

## Objective

Discover the origin IP behind Cloudflare/AWS WAF and other CDNs to bypass WAF protections and directly test the origin.

> **Attribution:** Methodology from [KathanP19/HowToHunt — FindOriginIP](https://github.com/KathanP19/HowToHunt/tree/master/FindOriginIP). Licensed GPL-3.0.

## Testing Methodology

### Phase 1: Confirm WAF

```bash
dig +short target.com
curl -s https://ipinfo.io/<IP> | jq -r '.org' # Cloudflare, Inc. = WAF
curl -s -D- https://target.com | grep -i "cf-ray\|x-amz\|aws"
```

### Phase 2: Historical DNS

```bash
# SecurityTrails
# https://securitytrails.com/domain/target.com/dns -> export A records
grep -E -o "([0-9]{1,3}\.){3}[0-9]{1,3}" dns_history.txt | sort -u > potential_ips.txt

# DNS Dumpster
# https://dnsdumpster.com -> network maps
```

### Phase 3: Subdomain Leaks

```bash
subfinder -silent -d target.com | dnsx -silent -a -resp | grep -v "104\.21\.\|172\.67\." | sort -u
# Dev/staging often bypass WAF
for sub in dev staging test beta admin origin direct; do
  dig +short $sub.target.com | grep -E "^[0-9]"
done
```

Focus subdomains: `dev`, `staging`, `test`, `beta`, `origin`, `direct`, `legacy`

### Phase 4: Certificate Transparency

```bash
# crt.sh
curl -s "https://crt.sh/?q=%25.target.com&output=json" | jq -r '.[].name_value' | sort -u
# Check cert SAN for origin IPs
```

### Phase 5: Misconfiguration Leaks

- Check `favicon` hash vs Shodan: `http.favicon.hash:123456`
- SPF records: `dig TXT target.com` may contain origin IP
- Email headers: Send mail to `noreply@target.com` auto-reply may leak origin
- GitHub search: `org:target "target.com" IP`

### Phase 6: Verification

```bash
for ip in $(cat potential_ips.txt); do
  echo "Testing $ip"
  curl -s --resolve target.com:443:$ip https://target.com -k -o /dev/null -w "%{http_code} $ip\n" | grep "200"
done
```

## What Constitutes a Finding

| Condition | Severity |
|-----------|----------|
| Origin IP found and directly accessible bypassing WAF | High (P2) |
| Historical IP still serves app (outdated WAF) | Medium (P3) |

## References

- [HowToHunt — FindOriginIP](https://github.com/KathanP19/HowToHunt/tree/master/FindOriginIP)
