---
name: osint-recon
description: >
  OSINT investigation and reconnaissance workflows. Username enumeration, domain intelligence,
  dark web monitoring, social media analysis, and structured investigation methodology.
  Use for authorized OSINT research, threat intelligence, and security investigations.
---

# OSINT Recon

Open Source Intelligence investigation and reconnaissance workflows.

## how to use

- `/osint-recon`
  Apply OSINT methodology to the current investigation.

- `/osint-recon <target-type>`
  Plan an OSINT investigation for username, domain, email, or organization.

## when to apply

Reference these guidelines when:
- investigating usernames or email addresses
- performing domain intelligence gathering
- conducting threat intelligence research
- analyzing social media footprints
- mapping organizational structure
- participating in OSINT CTF challenges

## investigation methodology

### OSINT Cycle
1. **Planning**: Define objectives, scope, legal constraints
2. **Collection**: Gather raw data from open sources
3. **Processing**: Clean, normalize, deduplicate data
4. **Analysis**: Correlate findings, identify patterns
5. **Dissemination**: Report findings with confidence levels
6. **Feedback**: Refine collection based on gaps

### Evidence Classification
| Level | Description | Example |
|-------|-------------|---------|
| Confirmed | Multiple independent sources | Username + email + profile photo match |
| Probable | Strong single source or partial corroboration | Username match + similar bio |
| Possible | Single weak source | Username exists on platform |
| Doubtful | Contradictory or unreliable | Common username, no distinguishing info |

## username enumeration

### Sherlock-Style Patterns
```python
# Pattern: Multi-platform username check
import asyncio
import aiohttp
from typing import TypedDict

class UsernameResult(TypedDict):
    platform: str
    url: str
    status: str  # "found", "not_found", "error"
    response_time_ms: float

PLATFORMS = {
    "github": "https://github.com/{username}",
    "twitter": "https://x.com/{username}",
    "instagram": "https://instagram.com/{username}",
    "reddit": "https://reddit.com/user/{username}",
    "linkedin": "https://linkedin.com/in/{username}",
    "medium": "https://medium.com/@{username}",
    "dev.to": "https://dev.to/{username}",
    "hackernews": "https://news.ycombinator.com/user?id={username}",
}

async def check_username(
    session: aiohttp.ClientSession,
    platform: str,
    url: str,
) -> UsernameResult:
    """Check if username exists on a platform."""
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
            return {
                "platform": platform,
                "url": url,
                "status": "found" if resp.status == 200 else "not_found",
                "response_time_ms": 0,
            }
    except Exception:
        return {"platform": platform, "url": url, "status": "error", "response_time_ms": 0}
```

### Key Tools
- **Sherlock**: Username enumeration across 400+ sites
- **WhatsMyName**: Web-based username search
- **Namechk**: Domain + username availability

## domain intelligence

### DNS & WHOIS
```bash
# DNS enumeration
dig +short A example.com
dig +short MX example.com
dig +short TXT example.com
dig +short NS example.com

# WHOIS
whois example.com

# Subdomain enumeration
# Tools: subfinder, amass, sublist3r
subfinder -d example.com -silent

# Certificate transparency
curl -s "https://crt.sh/?q=%25.example.com&output=json" | jq '.[].name_value'
```

### Technology Fingerprinting
- **Wappalyzer**: Browser extension for tech stack detection
- **BuiltWith**: Historical technology data
- **Shodan**: Internet-connected device search
- **Censys**: Certificate and host search

## email intelligence

### Email Verification Patterns
```python
# Pattern: Email OSINT workflow
def email_osint(email: str) -> dict:
    """Gather intelligence from an email address."""
    local_part, domain = email.split("@")
    return {
        "email": email,
        "domain_info": {
            "mx_records": dns_lookup(domain, "MX"),
            "spf_record": dns_lookup(domain, "TXT", filter="spf"),
            "dmarc_record": dns_lookup(f"_dmarc.{domain}", "TXT"),
        },
        "breach_check": "Use HaveIBeenPwned API",
        "social_profiles": "Cross-reference with username enumeration",
        "domain_age": "WHOIS creation date",
    }
```

### Tools
- **theHarvester**: Email, subdomain, name harvesting
- **Hunter.io**: Email pattern discovery
- **HaveIBeenPwned**: Breach exposure check

## dark web intelligence

### CTI Feed Sources (from DeepDarkCTI)
| Source Type | Examples | Use Case |
|-------------|----------|----------|
| Paste sites | Pastebin, GhostBin | Credential leaks, data dumps |
| Forums | Monitored via threat intel platforms | Threat actor discussion |
| Marketplaces | Tracked by law enforcement | Compromised data sales |
| Telegram | Public channels | Real-time threat chatter |
| Discord | Public servers | Community threat intel |

### CTI Integration Pattern
```python
# Pattern: CTI feed aggregation
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class ThreatLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class ThreatIndicator:
    ioc_type: str  # ip, domain, hash, email, url
    ioc_value: str
    source: str
    threat_level: ThreatLevel
    first_seen: datetime
    context: str
    confidence: float  # 0.0 - 1.0
```

## social media analysis

### Profile Analysis Framework
1. **Account metadata**: Creation date, follower/following ratio, posting frequency
2. **Content analysis**: Topics, sentiment, language patterns
3. **Network analysis**: Connections, group memberships, interactions
4. **Temporal analysis**: Activity patterns, time zones, posting schedules
5. **Cross-platform correlation**: Matching profiles across platforms

### OSINT Workflow Template (from Obsidian OSINT Templates)

```markdown
## Investigation: {{target}}
**Date**: {{date}}
**Objective**: {{objective}}
**Scope**: {{scope}}

### Findings
| Source | Data Point | Confidence | Notes |
|--------|-----------|------------|-------|

### Timeline
| Date | Event | Source |

### Connections Map
[Graph of relationships between entities]

### Assessment
**Confidence Level**: Confirmed / Probable / Possible / Doubtful
**Summary**:
**Recommendations**:
```

## data correlation techniques

### Entity Resolution
```python
# Pattern: Cross-source entity matching
def correlate_entities(sources: list[dict]) -> list[dict]:
    """Match entities across different OSINT sources."""
    # Exact matches: email, phone, unique IDs
    # Fuzzy matches: names (Levenshtein), usernames (substring)
    # Behavioral matches: writing style, posting times
    # Visual matches: profile photo reverse image search
    ...
```

### Pivot Points
- Username → email → real name → address
- Domain → IP → other domains (reverse DNS)
- Phone → social media → real identity
- Image → EXIF data → GPS coordinates → other photos

## integration with the operator's environment

| Component | Integration |
|-----------|------------|
| `memory` MCP server | Store entities, relations, observations as investigation graph |
| `security-auditor` agent | Automate reconnaissance for security assessments |
| `PostToolUse` hook | All OSINT commands logged in audit.log |
| `sequential` MCP | Step-by-step reasoning for complex correlations |
| `CoreMind` security layer | Hash chain audit trail for investigation activities |

### Using Memory MCP for Investigations
```
# Store investigation entities
mcp__memory__create_entities: [{name: "target_user", entityType: "person", observations: ["..."]}]
mcp__memory__create_relations: [{from: "target_user", to: "target_domain", relationType: "owns"}]
mcp__memory__search_nodes: {query: "target investigation"}
```

## legal and ethical guidelines

1. **Only use publicly available information**
2. **Never access private accounts or systems without authorization**
3. **Respect robots.txt and rate limits** (see `browser-automation-safety` skill)
4. **Document your methodology for reproducibility**
5. **Report findings responsibly** (coordinated disclosure)
6. **Comply with local privacy laws** (GDPR, CCPA, etc.)
7. **Never harass or stalk individuals**

## cross-references

- **offensive-security** skill: Full penetration testing methodology
- **security-review** skill: Code-level security analysis
- **browser-automation-safety** skill: Rate limiting, robots.txt compliance
- **research-methodology** skill: Source credibility assessment
- **SECURITY_ARSENAL.md**: Complete tool inventory
