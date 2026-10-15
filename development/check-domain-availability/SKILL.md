---
name: check-domain-availability
description: Check domain availability authoritatively via registry RDAP endpoints, bypassing registrars and third-party aggregators to avoid front-running. Use when screening domain candidates, verifying a name before purchase, or batch-checking many domains across TLDs.
---

# Check Domain Availability

Query the TLD registry's RDAP server directly. Never search names through registrar UIs, registrar APIs, or third-party domain-search SaaS — those are the documented front-running vectors (ICANN SSAC SAC-022; Network Solutions 2008).

## Protocol — RDAP only

WHOIS is being deprecated across the TLDs that matter:

- `.dev` `.app` and other Google TLDs — never had a WHOIS server, RDAP only
- `.io` — Identity Digital deprecated WHOIS on 2025-08-04, RDAP only
- `.com` `.net` — Verisign still runs WHOIS but recommends RDAP

Build for RDAP. Don't write `whois` parsers in 2026.

## Endpoints and rate limits

| TLD family                                                          | RDAP base                                     | Safe concurrency            |
| ------------------------------------------------------------------- | --------------------------------------------- | --------------------------- |
| `.com` `.net` (Verisign)                                            | `https://rdap.verisign.com/{tld}/v1/`         | parallel 3                  |
| Google gTLDs (`.dev` `.app` `.page` `.new` etc)                     | `https://pubapi.registry.google/rdap/`        | **sequential, ≤ 1 req/sec** |
| Identity Digital (`.io` `.ai` `.co` `.run` `.tools` `.tech` `.fyi`) | `https://rdap.identitydigital.services/rdap/` | parallel 5                  |
| Anything else                                                       | resolve via IANA bootstrap                    | per-registry                |

Parallelizing Google Registry above 1 req/sec returns HTTP 429 within ~10 requests. The other registries are generous.

## Endpoint resolution

IANA publishes the canonical RDAP endpoint per gTLD. Cache the bootstrap file locally:

```bash
IANA_CACHE="${TMPDIR:-/tmp}/iana-rdap.json"
[ -s "$IANA_CACHE" ] || curl -s https://data.iana.org/rdap/dns.json > "$IANA_CACHE"
```

ccTLDs (`.io` `.ai` `.co` `.tv` `.me` etc) are NOT in IANA bootstrap. Hardcode their RDAP servers from the registry's published documentation, or query the ccTLD's NIC.

## Status codes

| HTTP     | Meaning                                           |
| -------- | ------------------------------------------------- |
| 200      | Registered                                        |
| 404      | Not in registry — available to register           |
| 429      | Rate-limited — back off                           |
| 5xx, 000 | Transient (registry hiccup, TLS, network) — retry |

## Single-domain check

```bash
check_domain() {
  local domain="$1"
  local tld="${domain##*.}"
  local base
  case "$tld" in
    com|net)
      base="https://rdap.verisign.com/$tld/v1" ;;
    io|ai|co|tv)
      base="https://rdap.identitydigital.services/rdap" ;;
    *)
      # Resolve any other TLD via IANA bootstrap (covers Google, CentralNic, etc.)
      [ -s "$IANA_CACHE" ] || curl -s https://data.iana.org/rdap/dns.json > "$IANA_CACHE"
      base=$(jq -r --arg t "$tld" \
        '.services[] | select(.[0] | index($t)) | .[1][0]' "$IANA_CACHE" \
        | sed 's:/$::')
      [ -z "$base" ] && { printf "%-30s no-rdap-endpoint\n" "$domain"; return; }
      ;;
  esac
  local code
  code=$(curl -sk -o /dev/null -w "%{http_code}" -L --max-time 8 "$base/domain/$domain")
  case "$code" in
    200) printf "%-30s taken\n"      "$domain" ;;
    404) printf "%-30s AVAILABLE\n"  "$domain" ;;
    *)   printf "%-30s ?(%s)\n"      "$domain" "$code" ;;
  esac
}
export -f check_domain
```

## Batch check (correct concurrency per TLD)

Group by TLD family. Use the right concurrency for each:

```bash
NAMES=(kern foreword tenet herald vellum)

# Verisign — parallel 3
for n in "${NAMES[@]}"; do echo "$n.com"; done \
  | xargs -P 3 -I {} bash -c 'check_domain "$@"' _ {}

# Google Registry — MUST be sequential, ≤ 1 req/sec
for n in "${NAMES[@]}"; do check_domain "$n.dev"; sleep 1; done
for n in "${NAMES[@]}"; do check_domain "$n.app"; sleep 1; done

# Identity Digital — parallel 5
for n in "${NAMES[@]}"; do echo "$n.io"; done \
  | xargs -P 5 -I {} bash -c 'check_domain "$@"' _ {}
```

## Verify before purchase (high-stakes name)

Before paying for a name, cross-check three independent signals. Avoid every registrar search box.

```bash
name="example.com"
tld="${name##*.}"

# 1. RDAP — authoritative
case "$tld" in
  com|net) curl -s -o /dev/null -w "RDAP %{http_code}\n" \
             "https://rdap.verisign.com/$tld/v1/domain/$name" ;;
  io|ai|co|tv) curl -s -o /dev/null -w "RDAP %{http_code}\n" \
             "https://rdap.identitydigital.services/rdap/domain/$name" ;;
esac

# 2. WHOIS — only where the registry still runs one
case "$tld" in
  com|net) whois -h whois.verisign-grs.com "$name" \
             | grep -iE "Domain Status|No match" ;;
  # .dev / .app / .io: skip — no WHOIS server
esac

# 3. DNS NS — registered domains have NS records at the TLD level
dig +short NS "$name" @1.1.1.1 +tries=2 +time=2
```

All three saying "no record" → confidence near 100%. Any one returning data → already registered.

## Anti-patterns — never do these

- **Don't search names on registrar sites** (Namecheap, GoDaddy, Squarespace, Domain.com). Network Solutions did this in 2008 — registered every searched name themselves and forced users to buy from them. Documented in ICANN SSAC SAC-022.
- **Don't use third-party domain-search SaaS as the final check** (Domainr, instantdomainsearch, WhoisXMLAPI, DomainTools). They sell query data.
- **Don't use `rdap.org` as primary resolver** — it 429s easily and adds an unnecessary hop. It only issues 302 redirects (it doesn't proxy queries, so it's not a leak vector), but direct registry RDAP is faster and more accurate.
- **Don't check via Vercel / Cloudflare / Squarespace domain search** — these are registrars wearing a different shirt.
- **Don't waste time on Sysinternals WHOIS** — it's a Windows port of standard RFC 3912 with no special powers. macOS and Linux already have `whois` built in.

## ccTLD caveat

`.io` `.ai` `.co` `.tv` are ccTLDs — they sit OUTSIDE ICANN's registry/registrar separation regime. The registry operator (Identity Digital for these) has no formal contractual ban on logging or reusing query data. No documented incidents, but the structural guarantee is weaker than for `.com` `.dev` `.app`. For a high-value ccTLD name, register the moment your check returns 404; don't search repeatedly across days.

## Why registry-direct is safe

ICANN's 2024 `.com` Registry Agreement §5b prohibits Verisign from acting as a registrar or owning more than 15% of any registrar. Charleston Road Registry (Google's `.dev` `.app` registry) was incorporated specifically to maintain registry/registrar separation. SSAC SAC-022 reports zero documented registry-level front-running incidents.

The retail layer (registrars) is the documented threat. Avoid it for searches; use it only at the moment of purchase.

## References

- IANA RDAP bootstrap: `https://data.iana.org/rdap/dns.json`
- ICANN SSAC SAC-022 — domain name front-running threat report
- RFC 9082 / 9083 — RDAP query and response specs
- ICANN .com Registry Agreement (2024) §5b — registry/registrar separation
