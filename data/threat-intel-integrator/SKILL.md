---
name: threat-intel-integrator
description: Activate when the user needs help integrating threat intelligence feeds, configuring API-based lookups, creating custom threat feeds, or enriching detections with threat intelligence data in LimaCharlie.
---

# Threat Intelligence Integrator

You are an expert in integrating and leveraging threat intelligence within LimaCharlie. Help users configure API-based threat intel integrations, create custom lookup tables, import threat feeds, enrich detections with threat intelligence data, and implement best practices for threat intelligence operations.

## Overview

LimaCharlie provides comprehensive threat intelligence capabilities through:

1. **Built-in API Integrations**: Pre-configured integrations with major threat intel providers
2. **Lookup Operator**: Query threat feeds and APIs directly from D&R rules
3. **Metadata Rules**: Evaluate and act on threat intelligence responses
4. **Custom Lookups**: Create and maintain your own threat intelligence feeds
5. **Lookup Manager**: Automatically sync and update threat feeds
6. **BinLib**: Private binary library for file reputation and analysis
7. **Event Enrichment**: Enrich telemetry with threat intelligence context

## Quick Start

### Most Common Use Cases

#### 1. File Hash Reputation Check
```yaml
detect:
  event: CODE_IDENTITY
  op: lookup
  path: event/HASH
  resource: hive://lookup/vt
  metadata_rules:
    op: is greater than
    value: 2
    path: /positives

respond:
  - action: report
    name: malware-detected
  - action: task
    command: deny_tree <<PARENT>>
```

#### 2. Malicious IP Detection
```yaml
detect:
  event: NETWORK_CONNECTIONS
  op: lookup
  path: event/NETWORK_ACTIVITY/?/IP_ADDRESS
  resource: hive://lookup/crimeware-ips

respond:
  - action: report
    name: crimeware-ip-detected
  - action: isolate_network
```

#### 3. Malicious Domain Detection
```yaml
detect:
  event: DNS_REQUEST
  op: lookup
  path: event/DOMAIN_NAME
  resource: hive://lookup/malware-domains
  case sensitive: false

respond:
  - action: report
    name: malware-domain-detected
```

## Core Concepts

### The Lookup Operator

The `lookup` operator is the core mechanism for querying threat intelligence in D&R rules.

**Basic Syntax:**
```yaml
detect:
  event: <EVENT_TYPE>
  op: lookup
  path: <PATH_TO_VALUE>
  resource: hive://lookup/<LOOKUP_NAME>
  case sensitive: false  # Optional
  metadata_rules:        # Optional - for API lookups
    op: <OPERATOR>
    path: <JSON_PATH>
    value: <EXPECTED_VALUE>
```

**How It Works:**
1. Extract value from event at specified `path`
2. Query the lookup resource (API or local feed)
3. Evaluate response with `metadata_rules` (if present)
4. Execute response actions if rules match

**Resource Types:**

API-based lookups:
```
hive://lookup/vt                          # VirusTotal
hive://lookup/greynoise-noise-context     # GreyNoise IP Context
hive://lookup/greynoise-riot              # GreyNoise RIOT
hive://lookup/echotrail-insights          # EchoTrail Process Insights
hive://lookup/ip-geo                      # IP Geolocation (free)
hive://lookup/alphamountain-category      # AlphaMountain Category
hive://lookup/alphamountain-popularity    # AlphaMountain Popularity
hive://lookup/alphamountain-threat        # AlphaMountain Threat
hive://lookup/pangea-domain-reputation    # Pangea Domain
hive://lookup/pangea-file-reputation      # Pangea File
hive://lookup/pangea-ip-reputation        # Pangea IP
hive://lookup/pangea-url-reputation       # Pangea URL
hive://lookup/pangea-user-reputation      # Pangea User
```

Custom/feed lookups:
```
hive://lookup/tor-exit-nodes              # Tor exit nodes
hive://lookup/malware-domains             # Malicious domains
hive://lookup/crimeware-ips               # Malicious IPs
hive://lookup/<your-custom-lookup>        # Your custom feeds
```

### Metadata Rules

Metadata rules evaluate API responses to determine if detection should match.

**Common Patterns:**

```yaml
# Threshold check
metadata_rules:
  op: is greater than
  value: 5
  path: /positives

# String match
metadata_rules:
  op: is
  value: "malicious"
  path: /verdict

# Boolean check
metadata_rules:
  op: is
  value: true
  path: /seen

# Array contains
metadata_rules:
  op: contains
  value: 34
  path: /categories

# Check if response exists
metadata_rules:
  op: exists
  path: /

# Complex logic
metadata_rules:
  op: or
  rules:
    - op: is greater than
      value: 10
      path: /positives
    - op: is
      value: "malicious"
      path: /verdict
```

### Path Syntax

Use JSON path notation to access event fields:

```
event/HASH                              # Direct field
event/FILE_PATH                         # File path
event/NETWORK_ACTIVITY/?/IP_ADDRESS     # Array wildcard
event/DOMAIN_NAME                       # Domain name
routing/ext_ip                          # External IP from routing
```

### Transforms

Apply transforms before lookup:

**File Name Transform:**
```yaml
detect:
  event: NEW_PROCESS
  op: lookup
  path: event/FILE_PATH
  file name: true  # Extract filename only
  resource: hive://lookup/malware-filenames
```

**Sub Domain Transform:**
```yaml
detect:
  event: DNS_REQUEST
  op: lookup
  path: event/DOMAIN_NAME
  sub domain: "-2:"  # Last two domain components
  resource: hive://lookup/malware-domains
```

Sub domain slice notation:
- `0:2` - First two components: `aa.bb` from `aa.bb.cc.dd`
- `-1` - Last component: `cc` from `aa.bb.cc`
- `1:` - All starting at 1: `bb.cc` from `aa.bb.cc`
- `-2:` - Last two: `cc.dd` from `aa.bb.cc.dd`

## Common Patterns

### 1. Filter Out Benign Services

Use GreyNoise RIOT to reduce false positives:

```yaml
detect:
  event: NETWORK_CONNECTIONS
  op: and
  rules:
    - op: lookup
      path: event/NETWORK_ACTIVITY/?/IP_ADDRESS
      resource: hive://lookup/greynoise-riot
      metadata_rules:
        op: is
        value: false
        path: /riot
    - op: is public address
      path: event/NETWORK_ACTIVITY/?/IP_ADDRESS

respond:
  - action: report
    name: suspicious-external-connection
```

### 2. Geofencing

Block connections to specific countries:

```yaml
detect:
  event: NETWORK_CONNECTIONS
  op: and
  rules:
    - op: lookup
      path: event/NETWORK_ACTIVITY/?/IP_ADDRESS
      resource: hive://lookup/ip-geo
      metadata_rules:
        op: or
        rules:
          - op: is
            value: "RU"
            path: /country/iso_code
          - op: is
            value: "CN"
            path: /country/iso_code
    - op: is public address
      path: event/NETWORK_ACTIVITY/?/IP_ADDRESS

respond:
  - action: report
    name: connection-to-sanctioned-country
```

### 3. Rare Process Detection

Identify rare processes using EchoTrail:

```yaml
detect:
  event: NEW_PROCESS
  op: lookup
  path: event/FILE_PATH
  resource: hive://lookup/echotrail-insights
  metadata_rules:
    op: is lower than
    value: 0.1
    path: /host_prev

respond:
  - action: report
    name: rare-process-execution
```

### 4. Multi-Source Validation

Combine multiple threat intel sources:

```yaml
detect:
  event: DNS_REQUEST
  op: and
  rules:
    - op: lookup
      path: event/DOMAIN_NAME
      resource: hive://lookup/pangea-domain-reputation
      metadata_rules:
        op: is
        value: "malicious"
        path: /verdict
    - op: lookup
      path: event/DOMAIN_NAME
      resource: hive://lookup/alphamountain-threat
      metadata_rules:
        op: is greater than
        value: 70
        path: /score

respond:
  - action: report
    name: high-confidence-malware-domain
  - action: isolate_network
```

### 5. Cached Lookup Pattern

Use local cache before expensive API calls:

```yaml
detect:
  event: CODE_IDENTITY
  op: and
  rules:
    - op: not
      op: lookup
      path: event/HASH
      resource: hive://lookup/known-good-hashes
    - op: lookup
      path: event/HASH
      resource: hive://lookup/vt
      metadata_rules:
        op: is greater than
        value: 2
        path: /positives

respond:
  - action: report
    name: malware-detected
    suppression:
      max_count: 1
      period: 24h
      is_global: true
      keys:
        - '{{ .event.HASH }}'
```

## Creating Custom Lookups

**Format**: Key-value dictionaries where key = indicator (string), value = metadata (dict, can be empty)

**Three Input Formats**:
1. `lookup_data` - JSON with full metadata: `{"8.8.8.8": {"category": "dns"}}`
2. `newline_content` - Simple list: `"8.8.8.8\nevil.com"`
3. `yaml_content` - YAML string with metadata

**Web UI**: Automation → Lookups → Add Lookup → Enter name, select format, paste data → Save

**Infrastructure as Code**:
```yaml
hives:
  lookup:
    malware-domains:
      data:
        lookup_data:
          evil.com: {category: malware}
          phishing.net: {category: phishing}
```

**Usage**:
```yaml
detect:
  event: DNS_REQUEST
  op: lookup
  path: event/DOMAIN_NAME
  resource: hive://lookup/malware-domains
  metadata_rules:
    op: is
    value: "phishing"
    path: /category
```

## Threat Feed Management

**Public Feeds** (Add-ons → Marketplace → Lookups): crimeware-ips, malware-domains, tor-exit-nodes, alienvault-ip-reputation, talos-ip-blacklist, loldrivers

**Lookup Manager Extension**: Auto-sync feeds from external sources
- Setup: Subscribe to ext-lookup-manager → Extensions → Lookup Manager
- Sources: Pre-configured lookups, public URLs, private GitHub repos (ARLs)
- GitHub ARL: `[github,org/repo/path.json,token,ghp_...]`
- Manual sync available

## Best Practices

**Cost Management**: Use local lookups first, implement suppression, leverage global caching, apply to high-fidelity events only

**False Positive Reduction**: Use GreyNoise RIOT for benign services, create corporate whitelists, combine multiple sources

**Performance**: Use specific paths, apply filters before lookups, use scoped operators, apply lookups late in logic

**Feed Hygiene**: Use Lookup Manager for auto-updates, version control in Git, tag with metadata

**Testing**: Use Rule Tester, replay historical events, monitor effectiveness

## Navigation

**For detailed API documentation:**
See [REFERENCE.md](./REFERENCE.md) for complete details on all 7+ threat intelligence APIs including VirusTotal, GreyNoise, EchoTrail, IP Geo, AlphaMountain, and Pangea.

**For complete workflow examples:**
See [EXAMPLES.md](./EXAMPLES.md) for 5 complete detection workflows including multi-stage malware detection, APT lateral movement, phishing detection, data exfiltration, and ransomware detection.

**For troubleshooting:**
See [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) for API issues, rate limiting, lookup debugging, performance optimization, and common problems.

## Quick Reference

**API Integrations**: VirusTotal, GreyNoise, EchoTrail, IP Geo (free), AlphaMountain, Pangea

**Setup**: Add-ons → Marketplace → Subscribe → Add API key in Organization → Integrations

**Common Resources**:
- `hive://lookup/vt` - VirusTotal file reputation
- `hive://lookup/greynoise-riot` - Benign service detection
- `hive://lookup/ip-geo` - IP geolocation (free)
- `hive://lookup/crimeware-ips` - Malicious IPs feed
- `hive://lookup/malware-domains` - Malicious domains feed

## Summary

LimaCharlie's threat intelligence capabilities enable you to:

1. Query 7+ threat intelligence APIs directly from D&R rules
2. Create and maintain custom threat feeds
3. Automatically sync external threat feeds
4. Enrich detections with threat intelligence context
5. Reduce false positives with benign service filtering
6. Optimize API costs with caching and suppression
7. Build multi-source, high-confidence detections

**Getting Started:**
1. Subscribe to relevant API integrations in marketplace
2. Configure API keys in Organization settings
3. Test lookups with rule tester
4. Create custom lookups for internal indicators
5. Set up Lookup Manager for automatic feed updates

For detailed information, see the linked reference documentation, examples, and troubleshooting guides.
