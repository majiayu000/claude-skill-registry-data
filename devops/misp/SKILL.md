---
name: misp
description: "Expert agent for MISP (Malware Information Sharing Platform). Covers events, attributes, objects, galaxies, taxonomies, correlation engine, sharing groups, feeds, PyMISP, STIX/TAXII export, warninglists, and misp-modules enrichment. WHEN: \"MISP\", \"Malware Information Sharing Platform\", \"MISP event\", \"MISP feed\", \"PyMISP\", \"MISP galaxy\", \"MISP taxonomy\", \"MISP object\", \"sharing group\", \"misp-modules\"."
license: MIT
---

# MISP

This skill covers MISP (Malware Information Sharing Platform). It has deep expertise in MISP's data model, configuration, automation via PyMISP, and deployment for both internal intelligence management and community sharing.

## How to Approach Tasks

1. **Classify the request type:**
   - **Data model** -- Events, attributes, objects, galaxies, taxonomies
   - **Sharing / federation** -- Sharing groups, synchronization, feeds
   - **Automation** -- PyMISP, REST API, automation scripts
   - **Integration** -- SIEM/SOAR integration, STIX/TAXII export
   - **Administration** -- Server setup, user management, performance tuning

2. **Identify deployment context:**
   - **Single instance** (internal TIP only)
   - **Federated** (sync with other MISP instances -- ISAC, trusted partners)
   - **Feed consumer** (importing external OSINT and commercial feeds)

3. **Load context** -- Read `references/architecture.md` for data model and infrastructure details.

## Platform Overview

MISP is an open-source threat intelligence platform licensed under AGPL. Originally developed by CIRCL (Computer Incident Response Center Luxembourg) and now maintained by a global community.

**Key strengths:**
- Community-driven: Large ecosystem of feeds, galaxies, and modules maintained by the security community
- Flexible sharing: Granular control over who sees what
- Open standards: Native STIX 2.1 and TAXII 2.1 support
- Extensibility: Python ecosystem via PyMISP and misp-modules

## MISP Data Model

### Events

Events are the top-level container in MISP. An event represents a piece of intelligence -- an incident, malware analysis, threat report, or IOC collection.

**Event fields:**
- `info`: Short description (title)
- `date`: Date of the event/intelligence
- `threat_level_id`: 1-High, 2-Medium, 3-Low, 4-Undefined
- `analysis`: 0-Initial, 1-Ongoing, 2-Completed
- `distribution`: Who can see this event (see sharing below)
- `sharing_group_id`: If distribution=4 (Sharing Group), which group

**Best practice:** One event per incident/campaign/malware sample. Don't combine unrelated intelligence in one event.

### Attributes

Attributes are atomic indicators or observables attached to an event.

**Attribute types (common):**

| Category | Type | Example |
|---|---|---|
| Network activity | ip-src | Source IP of attack |
| Network activity | ip-dst | C2 destination IP |
| Network activity | domain | Malicious domain |
| Network activity | url | Full malicious URL |
| Network activity | hostname | Resolved hostname |
| Payload delivery | md5 | File hash (MD5) |
| Payload delivery | sha256 | File hash (SHA-256) |
| Payload delivery | filename | Malware filename |
| Payload delivery | email-src | Phishing sender |
| Payload delivery | email-subject | Phishing subject line |
| External analysis | link | Link to external report |
| Antivirus detection | text | AV detection name |
| Persistence mechanism | regkey | Registry key for persistence |
| Financial fraud | btc | Bitcoin address |

**Attribute flags:**
- `to_ids`: Boolean -- should this attribute be exported to IDS/blocking systems? Set false for informational attributes (not IOCs).
- `comment`: Free-text analyst annotation
- `tags`: Apply taxonomy tags or galaxy clusters (see below)

### Objects

Objects are structured groups of attributes representing a complex entity.

**Why objects?** A single file is better described by multiple related attributes: filename, MD5, SHA-256, file size, mimetype, file path. An MISP object groups these into a cohesive unit.

**Common MISP objects:**

| Object Template | Use Case | Key Attributes |
|---|---|---|
| `file` | Malware file | filename, md5, sha256, size, filetype |
| `email` | Phishing email | from, to, subject, body, attachment refs |
| `network-connection` | Network flow | src-ip, src-port, dst-ip, dst-port, protocol |
| `url` | Web resource | url, domain, ip, first-seen, last-seen |
| `domain-ip` | Domain + resolution | domain, ip (passive DNS record) |
| `person` | Threat actor individual | name, email, username |
| `vulnerability` | CVE details | id (CVE), cvss-score, description |
| `course-of-action` | Defensive recommendation | name, description, cost, efficacy |
| `yara` | YARA rule | yara (rule text), context |
| `pe` | Windows PE file | type, compilation-timestamp, sections, imports |

**Creating an object:**
`Events > [Event] > Add Object > [Object Template]`

Objects are linked to other objects and attributes via references (relationships).

### Galaxies

Galaxies are structured knowledge bases attached to events or attributes.

**Galaxy structure:**
- **Galaxy**: Knowledge domain (e.g., MITRE ATT&CK Enterprise, Threat Actors, Malware)
- **Cluster**: A specific entry within the galaxy (e.g., APT29, LockBit, T1566.001)
- **Elements**: Sub-properties of the cluster (synonyms, description, links)

**Key galaxy collections:**

| Galaxy | Content |
|---|---|
| MITRE ATT&CK Enterprise | All ATT&CK techniques (T-numbers) |
| MITRE ATT&CK Mobile | Mobile ATT&CK techniques |
| MITRE ATT&CK ICS | ICS/SCADA ATT&CK techniques |
| Threat Actor | Named threat actor groups (APT29, Lazarus, etc.) |
| Malware | Malware families (LockBit, Emotet, Cobalt Strike, etc.) |
| Ransomware | Ransomware groups and TTPs |
| Tool | Legitimate + offensive tools (Metasploit, Mimikatz, etc.) |
| Country | Nation-state associations |
| Sector | Industry verticals (targeting context) |

**Using galaxies in practice:**
- Tag an event with the Threat Actor galaxy cluster for APT29 → Event is linked to the full APT29 knowledge base
- Tag an attribute with ATT&CK technique T1566.001 → Spearphishing Attachment technique context added
- Galaxies are automatically included in STIX export as attack-pattern and threat-actor objects

### Taxonomies

Taxonomies are controlled vocabulary tagging systems. Applied as tags to events, attributes, or objects.

**Built-in taxonomies:**

| Taxonomy | Purpose | Example Tags |
|---|---|---|
| `tlp` | Traffic Light Protocol | tlp:red, tlp:amber, tlp:green, tlp:clear |
| `admiralty-scale` | Source reliability/info credibility | admiralty-scale:source-reliability="a", admiralty-scale:information-credibility="1" |
| `PAP` | Permissible Actions Protocol | PAP:RED, PAP:AMBER, PAP:GREEN, PAP:WHITE |
| `kill-chain` | Lockheed Martin Kill Chain | kill-chain:reconnaissance, kill-chain:command-and-control |
| `malware_classification` | Malware types | malware_classification:ransomware, malware_classification:rat |
| `workflow` | Internal workflow state | workflow:state="incomplete", workflow:state="complete" |
| `type` | Intel type | type:OSINT, type:SIGINT, type:HUMINT |
| `circl` | CIRCL internal | circl:incident-classification="vulnerability" |

**Enabling taxonomies:**
`Administration > Taxonomies > Enable [taxonomy]`
Most common: Enable TLP immediately on all fresh MISP deployments.

## Correlation Engine

MISP automatically correlates attributes across events.

### How Correlation Works

When a new attribute is added:
1. MISP checks if the same value exists in any other event
2. If yes: A correlation link is created between the two events
3. Correlation links are visible on event pages and in the correlation graph

**Correlation types:**
- Direct: Same exact value (same IP in two events)
- Fuzzy: Similar patterns (overlapping CIDR ranges -- disabled by default; high false positive risk)

### Using Correlations

**Correlation graph (visual):**
`Events > [Event] > Correlation Graph`
Shows all events connected to this event via shared indicators; pivot across campaigns.

**Correlation via API:**
```python
# Get all events correlated with a specific attribute value
results = misp.search(value="198.51.100.42", type_attribute="ip-dst", include_correlations=True)
```

### Performance Tuning

Correlation is computationally expensive at scale. Tuning options:
- **Warninglists**: Suppress correlation for benign values (see Warninglists section)
- **Correlation threshold**: Skip correlation for attributes below a confidence threshold
- **Exclude types**: Disable correlation for certain attribute types that produce high noise (e.g., `text`, `comment`)

## Sharing and Distribution

### Distribution Levels

Every event and attribute has a distribution setting:

| Level | Who can see | Use case |
|---|---|---|
| 0 - Your Organisation Only | Local org only | Draft intelligence; sensitive unvetted data |
| 1 - This Community Only | All users on this MISP instance | Internal community sharing |
| 2 - Connected Communities | This instance + synced instances (1 hop) | Trusted partner network |
| 3 - All Communities | All MISP instances reachable (unlimited hops) | Public/community intelligence |
| 4 - Sharing Group | Only members of specified sharing group | Controlled sharing with named orgs |

**Recommendation:** Default to level 0 for new events; promote to higher distribution after review.

### Sharing Groups

Sharing groups define a specific list of MISP instances or organizations that can access intelligence.

**Creating a sharing group:**
`Sharing Groups > Add Sharing Group`
- Name and description
- Add organizations (by MISP UUID or manual search)
- Add MISP instances (synchronization endpoints)
- Set roaming (can members re-share with their own sharing groups?)

**Use case:** Multi-sector ISAC participation
- Create sharing group "FS-ISAC Financial Sector"
- Add all member MISP instances
- Events tagged with this group shared only with financial sector ISAC members
- No accidental sharing to unrelated communities

### Instance Synchronization

MISP can synchronize events between instances (federated model).

**Sync modes:**
- **Push**: Local instance pushes events to remote (must have write access on remote)
- **Pull**: Local instance pulls events from remote (must have read access on remote)
- **Full mirror**: Push + pull (bidirectional sync)

**Sync filters:**
- Tag whitelist/blacklist: Sync only events with specific tags
- Event filter: Sync only events above a certain threat level
- Org filter: Sync events from specific organizations only

**Configuration:**
`Administration > Servers > Add Server`
- Remote URL, API key
- Push/pull settings
- Sync filters

## Feeds

Feeds allow MISP to import intelligence from external sources automatically.

### Configuring Feeds

`Sync Actions > Feeds > Add Feed`

**Feed types:**
- **MISP feed**: Remote MISP instance export (JSON format)
- **CSV feed**: Simple CSV with attribute values
- **FreeTaxii feed**: TAXII 2.1 source
- **OTX feed**: AlienVault OTX (built-in connector)

**Recommended free feeds:**

| Feed Name | URL | Content |
|---|---|---|
| CIRCL OSINT Feed | https://www.circl.lu/doc/misp/feed-osint/ | OSINT IOCs from CIRCL |
| Botvrij.eu | https://www.botvrij.eu/data/feed-osint/ | OSINT malware IOCs |
| Abuse.ch MalwareBazaar | Via MISP connector | Malware hashes |
| Abuse.ch URLhaus | Via MISP connector | Malware distribution URLs |
| Abuse.ch ThreatFox | Via MISP connector | IOCs from ThreatFox community |
| ESET MISP feed | Via MISP connector | ESET threat research |

**Feed caching:**
Enable feed caching so MISP checks new attributes against all feeds locally (fast lookups without external API calls).

`Sync Actions > Feeds > Cache all feeds`
Schedule daily recaching via cron.

### Checking Attributes Against Feeds

With caching enabled, MISP shows feed hits on attribute view:
- Blue feed icon next to an attribute = this value was seen in a configured feed
- Click to see which feeds contain this value and with what context

## Warninglists

Warninglists suppress false positives by marking known-benign values as "known safe."

### Purpose

When importing feeds or correlating, you'll see IPs like `8.8.8.8` (Google DNS) or `192.168.1.1` (RFC1918). These should not be flagged as malicious.

Warninglists tell MISP: "This value is on a known-good list; don't flag it as suspicious."

### Built-in Warninglists

- Alexa Top 1 Million domains
- RFC 1918 private IP ranges
- RFC 5735 special-purpose IPv4 addresses
- Common public DNS resolvers (8.8.8.8, 1.1.1.1, etc.)
- Microsoft Office 365 IP ranges
- Major CDN IP ranges (Cloudflare, Akamai, Fastly)
- Government website domains

**Enabling warninglists:**
`Warning Lists > Enable All` (or selectively enable relevant ones)

### Effect

- Attributes on warninglists display a warning triangle icon
- `to_ids` is automatically set to false for warnlisted values
- Correlation is suppressed (prevents spurious correlations from common infrastructure)

## PyMISP (Python Library)

PyMISP is the official Python library for interacting with the MISP REST API.

### Installation

```bash
pip install pymisp
```

### Authentication

```python
from pymisp import PyMISP

misp = PyMISP(
    url="https://your-misp-instance.example.com",
    key="your-api-key",
    ssl=True
)
```

### Common Operations

Covers creating events and attributes, searching by value/tag/timestamp, exporting STIX bundles, and adding objects (e.g. `FileObject`) to events. See `references/pymisp-examples.md` for full code examples of each.

## REST API Reference

### Authentication

All requests require:
```
Authorization: {your_api_key}
Accept: application/json
Content-Type: application/json
```

Covers CRUD endpoints for events and attributes, advanced `restSearch` endpoints, sharing group/feed/warninglist endpoints, and the `restSearch` JSON body format. See `references/rest-api.md` for the full endpoint list and an example search body.

## STIX/TAXII Integration

### Exporting as STIX 2.1

**Single event:**
`Events > [Event] > Download > STIX 2.1 JSON`

**Via API:**
```
GET /events/restSearch/stix2?type=ip-dst&to_ids=1&last=7d
```

**Via MISP TAXII server** (misp-stix module required):
MISP can expose a TAXII 2.1 server to allow external consumers to pull STIX bundles.

### Importing STIX

**From TAXII:**
`Sync Actions > Feeds > Add Feed > TAXII` 
Enter TAXII server URL and credentials.

**Manual STIX import:**
`Events > Import Events > STIX 2.x`
Upload a STIX JSON bundle; MISP creates events from the STIX objects.

**Via API:**
```
POST /events/upload_stix
Content: STIX JSON bundle
```

### MISP ↔ OpenCTI Integration

MISP and OpenCTI integrate bidirectionally:
- OpenCTI can consume MISP events via MISP connector
- MISP can receive intelligence from OpenCTI via TAXII
- Organizations use MISP for sharing and OpenCTI for analysis/graph visualization

## misp-modules (Enrichment)

misp-modules is a separate service providing enrichment, import, and export modules for MISP.

### Architecture

- Separate Python service (`python3 -m misp_modules`)
- MISP calls misp-modules via REST
- Each module: Takes an attribute value as input, returns enriched data

### Common Modules

**Enrichment modules:**
- `ipasn`: Resolve IP to ASN and organization
- `whois`: WHOIS lookup for domain/IP
- `virustotal`: VirusTotal lookup (API key required)
- `shodan_internetdb`: Shodan Internet DB lookup (no API key needed)
- `urlscan`: URLScan.io submission and result
- `hashlookup`: CIRCL Hashlookup for known file hashes (returns if hash is known good/malicious)
- `greynoise`: GreyNoise IP classification
- `emailheader`: Parse email headers into attributes
- `cve_advanced`: CVE details from NVD
- `yara_syntax_validator`: Validate YARA rules

**Import modules:**
- `pdf_enrich`: Extract IOCs from PDF reports
- `csvimport`: Flexible CSV import with field mapping
- `goamlimport`: GoAML financial intelligence format

**Using enrichment:**
1. On any attribute: Click `Enrich Attribute`
2. Select module(s) to run
3. Results added as new attributes (with parent relationship)

### Installation

```bash
git clone https://github.com/MISP/misp-modules.git
cd misp-modules
pip install -e ".[all]"
python3 -m misp_modules -l 0.0.0.0 -s
```

Configure in MISP: `Administration > Server Settings > MISP > Plugin` → set misp-modules URL

## Reference Files

- `references/architecture.md` -- MISP server architecture, database model, correlation engine internals, feed caching mechanism, synchronization protocol, user role model, REST API structure, STIX export pipeline, misp-modules service architecture, and performance tuning guidance.
- `references/pymisp-examples.md` -- Full PyMISP code examples: creating events/attributes, searching, STIX export, and adding objects.
- `references/rest-api.md` -- Full MISP REST API endpoint list and an example `restSearch` JSON body.
