---
name: managing-bind9
description: |
  Use when working with Bind9 — bIND9 DNS server management covering zone files,
  named configuration, DNSSEC, RNDC controls, query logging, and server
  statistics. Use when managing BIND9 DNS servers, auditing zone configurations,
  troubleshooting DNS resolution, checking DNSSEC status, or monitoring BIND9
  performance and query patterns.
connection_type: bind9
preload: false
---

# BIND9 DNS Server Skill

Manage BIND9 DNS zones, configuration, DNSSEC, query logs, and server statistics.

## Core Helper Functions

```bash
#!/bin/bash

NAMED_CONF="${BIND9_CONF:-/etc/bind/named.conf}"
ZONES_DIR="${BIND9_ZONES_DIR:-/etc/bind/zones}"

# RNDC wrapper
bind_rndc() {
    rndc "$@" 2>/dev/null
}

# Query the local DNS server
bind_query() {
    local name="$1" type="${2:-A}"
    dig @localhost "$name" "$type" +short 2>/dev/null
}
```

## MANDATORY: Discovery-First Pattern

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== BIND9 Version ==="
named -v 2>/dev/null || dig @localhost version.bind txt chaos +short 2>/dev/null

echo ""
echo "=== Server Status ==="
rndc status 2>/dev/null | head -15

echo ""
echo "=== Configured Zones ==="
rndc zonestatus 2>/dev/null || named-checkconf -z "$NAMED_CONF" 2>/dev/null | head -25

echo ""
echo "=== Zone List ==="
rndc dumpdb -zones 2>/dev/null
grep -E "^zone " "$NAMED_CONF" /etc/bind/named.conf.local 2>/dev/null | head -20

echo ""
echo "=== DNSSEC Status ==="
for zone in $(grep -oP 'zone "\K[^"]+' "$NAMED_CONF" /etc/bind/named.conf.local 2>/dev/null | head -10); do
    DNSSEC=$(dig @localhost "$zone" DNSKEY +short 2>/dev/null | wc -l)
    echo "$zone: $DNSSEC DNSKEY records"
done | head -15

echo ""
echo "=== Server Statistics ==="
rndc stats 2>/dev/null
cat /var/cache/bind/named.stats 2>/dev/null | tail -20
```

### Phase 2: Analysis

```bash
#!/bin/bash
ZONE="${1:?Zone name required}"

echo "=== Zone Status ==="
rndc zonestatus "$ZONE" 2>/dev/null

echo ""
echo "=== Zone File Validation ==="
ZONE_FILE=$(grep -A5 "zone \"$ZONE\"" "$NAMED_CONF" /etc/bind/named.conf.local 2>/dev/null | grep -oP 'file "\K[^"]+')
if [ -n "$ZONE_FILE" ]; then
    named-checkzone "$ZONE" "$ZONE_FILE" 2>/dev/null
    echo ""
    echo "=== Zone Records ==="
    dig @localhost "$ZONE" AXFR +noall +answer 2>/dev/null | head -30
else
    echo "Zone file not found in config"
    echo ""
    echo "=== Zone Records via Query ==="
    for type in SOA NS A AAAA MX TXT CNAME SRV; do
        RESULT=$(dig @localhost "$ZONE" "$type" +short 2>/dev/null)
        [ -n "$RESULT" ] && echo "$type: $RESULT"
    done
fi

echo ""
echo "=== DNSSEC Validation ==="
dig @localhost "$ZONE" DNSKEY +dnssec +short 2>/dev/null | head -5
dig @localhost "$ZONE" SOA +dnssec +short 2>/dev/null

echo ""
echo "=== Query Log (recent) ==="
tail -50 /var/log/named/query.log 2>/dev/null | grep -i "$ZONE" | tail -10
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Use `dig` for DNS queries and `rndc` for server management
- Validate zone files with `named-checkzone` before reporting

## Safety Rules
- **Read-only by default**: Use `dig`, `rndc status`, and `named-checkconf` for inspection
- **Never edit zone files** directly without confirmation and backup
- **RNDC reload** affects live DNS resolution -- confirm before executing
- **DNSSEC key changes** require careful rollover procedures

## Output Format

Present results as a structured report:
```
Managing Bind9 Report
═════════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Anti-Hallucination Rules

1. **NEVER assume resource names** — always discover via CLI/API in Phase 1 before referencing in Phase 2.
2. **NEVER fabricate metric names or dimensions** — verify against the service documentation or `--help` output.
3. **NEVER mix CLI commands between service versions** — confirm which version/API you are targeting.
4. **ALWAYS use the discovery → verify → analyze chain** — every resource referenced must have been discovered first.
5. **ALWAYS handle empty results gracefully** — an empty response is valid data, not an error to retry.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

## Common Pitfalls
- **Serial number**: Must increment serial in SOA record for zone updates to propagate
- **File permissions**: BIND runs as `bind` or `named` user; zone files need correct ownership
- **AXFR restrictions**: Zone transfers should be restricted to authorized secondaries
- **Chroot**: Many installations run in chroot; paths may differ from expected
- **named-checkconf**: Always validate configuration before reloading
