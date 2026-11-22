---
name: "asnrecon"
description: "ASN and IPv4 range reconnaissance using bgp.he.net. USE WHEN user mentions ASN lookup, find IP ranges, company IP space, BGP reconnaissance, owned IP addresses, network footprint, OR wants to discover what IP ranges a company owns. Searches bgp.he.net free-form, extracts ASNs and IPv4 prefixes."
---

# Asnrecon

*Sourced from security-talent-bugskill-ai*

# AsnRecon

Discover a company's network footprint by finding their ASNs and owned IPv4 ranges using bgp.he.net.

**Why This Matters:** Companies often own IP space that isn't discoverable through DNS. Finding ASNs and IP ranges reveals infrastructure that subdomain enumeration misses - data centers, cloud deployments, legacy systems, and internal networks.

## Workflow Routing

**When executing a workflow, output this notification directly:**

```
Running the **WorkflowName** workflow from the **AsnRecon** skill...
```

| Workflow | Trigger | File |
|----------|---------|------|
| **FindAsn** | "find ASN", "ASN lookup", "company ASN" | `workflows/FindAsn.md` |
| **FindIpRanges** | "find IP ranges", "IPv4 prefixes", "owned IP space" | `workflows/FindIpRanges.md` |
| **FullAsnRecon** | "full ASN recon", "network footprint", "all IP ranges" | `workflows/FullAsnRecon.md` |

## Examples

**Example 1: Full ASN reconnaissance (RECOMMENDED)**
```
User: "Find the IP ranges owned by Acme Corp"
→ Invokes FullAsnRecon workflow
→ Searches bgp.he.net for "Acme Corp"
→ Identifies all ASNs associated with the company
→ Extracts IPv4 prefixes from each ASN's Prefixes V4 tab
→ Outputs {company}-asn-report.md with all ranges
→ User has complete network footprint for testing
```

**Example 2: Find company's ASN numbers**
```
User: "What ASNs does Netflix own?"
→ Invokes FindAsn workflow
→ Searches bgp.he.net free-form for "Netflix"
→ Lists all ASN numbers with organization names
→ Outputs ASN list for further investigation
```

**Example 3: Get IPv4 prefixes for known ASN**
```
User: "Show me the IPv4 ranges for AS2906"
→ Invokes FindIpRanges workflow
→ Fetches bgp.he.net/AS2906#_prefixes4
→ Extracts all IPv4 CIDR ranges
→ Outputs list of IP ranges for scanning
```

## Data Source

**bgp.he.net** - Hurricane Electric's BGP Toolkit

- Free to use, no authentication required
- Free-form search by company name, ASN, IP, or prefix
- Comprehensive BGP routing data
- Shows origin ASNs, prefixes, and relationships

**Key URLs:**
- Search: `https://bgp.he.net/search?search[search]={query}`
- ASN details: `https://bgp.he.net/AS{number}`
- IPv4 prefixes: `https://bgp.he.net/AS{number}#_prefixes4`

## Output Format

```
{company}-asn-report.md    # Full report with ASNs and all prefixes
{company}-asns.txt         # List of ASN numbers only
{company}-ipv4-ranges.txt  # All IPv4 CIDR ranges (one per line)
```

**Report format:**
```markdown
# ASN Reconnaissance: {Company}

## ASNs Found
| ASN | Organization | Country |
|-----|--------------|---------|
| AS12345 | Company Inc | US |

## IPv4 Prefixes
| Prefix | ASN | Description |
|--------|-----|-------------|
| 192.0.2.0/24 | AS12345 | Production |

## Summary
- Total ASNs: X
- Total IPv4 Prefixes: Y
- Estimated IPs: Z
```

## Integration with Recon Pipeline

ASN reconnaissance is typically done **before** subdomain enumeration:

```
1. AsnRecon → Find company's IP ranges
2. Reverse DNS on IP ranges → Discover additional domains
3. SubdomainEnum → Enumerate all discovered domains
4. Scan IP ranges directly → Find non-DNS infrastructure
```

**Combine with:**
- `masscan` / `nmap` for port scanning IP ranges
- Reverse DNS lookups to find hostnames
- `Recon` skill for subdomain enumeration on discovered domains

## Reference Documentation

- `workflows/FullAsnRecon.md` - Complete reconnaissance workflow
- `workflows/FindAsn.md` - ASN discovery workflow
- `workflows/FindIpRanges.md` - IPv4 prefix extraction workflow

