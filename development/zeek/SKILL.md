---
name: zeek
description: "Expert agent for Zeek network analysis framework. Covers event-driven scripting, structured log analysis (conn.log, dns.log, http.log, ssl.log, files.log), protocol analysis, Intelligence Framework, cluster deployment, Spicy parsers, and Zeek packages. WHEN: \"Zeek\", \"Zeek script\", \"Zeek log\", \"conn.log\", \"zeekctl\", \"Bro\", \"network forensics\", \"Zeek Intelligence Framework\", \"Spicy parser\", \"Zeek cluster\"."
license: MIT
---

# Zeek

This skill covers Zeek (formerly Bro), the open-source network analysis framework. It has deep knowledge of Zeek's event-driven scripting language, structured log formats, protocol analysis capabilities, cluster deployment, and integration with security analytics platforms.

**Important distinction:** Zeek is NOT a traditional IDS. It does not use alert rules like Suricata/Snort. It is a passive network analysis framework that generates rich structured metadata about all network activity. Pair Zeek with Suricata for both metadata and signature-based detection.

## How to Approach Tasks

When you receive a request:

1. **Classify** the request:
   - **Log analysis** -- Apply structured log knowledge; reference log schema
   - **Script writing** -- Apply Zeek scripting language guidance
   - **Cluster deployment** -- Load `references/architecture.md`
   - **Threat hunting** -- Apply log correlation methodology
   - **SIEM integration** -- Apply integration patterns for Elastic/Splunk/Kafka
   - **Protocol parsing** -- Reference Spicy and built-in protocol support

2. **Clarify use case** -- Zeek is used for forensics/hunting, not real-time blocking. If the user needs active prevention, recommend adding Suricata alongside Zeek.

3. **Gather context** -- Throughput, deployment mode (standalone vs. cluster), SIEM platform, log retention requirements, programming experience with Zeek scripts.

4. **Recommend** -- Provide specific Zeek script code, log analysis queries, or configuration snippets.

## Core Expertise

### Zeek Log Reference

Zeek generates structured tab-separated logs (or JSON) for each protocol and event type.

**Core logs:**

**conn.log** -- The foundation log. Every network connection generates one record at connection close:
```
ts          uid                id.orig_h    id.orig_p  id.resp_h    id.resp_p  proto  service  duration  orig_bytes  resp_bytes  conn_state  history
1705330425  CXfbCm1ABCDEF123   10.1.2.3     54321      192.168.1.1  80         tcp    http      0.234     1234        5678        SF          ShADadfFRR
```
Key fields: `uid` (unique connection ID, links all logs for same session), `conn_state` (SF=normal close, S0=no response, REJ=rejected, RSTO=RST by originator, RSTR=RST by responder), `history` (packet-level state machine trace)

**dns.log** -- All DNS queries and responses:
```
ts          uid       id.orig_h  id.orig_p  id.resp_h  id.resp_p  proto  query                 qtype  qtype_name  rcode  answers
1705330425  CXFBCM1A  10.1.2.3   54321      8.8.8.8    53         udp    evil.example.com      1      A           0      1.2.3.4
```

**http.log** -- All HTTP transactions:
```
ts          uid       id.orig_h  id.orig_p  id.resp_h    id.resp_p  method  host             uri              referrer  user_agent         status_code  resp_body_len
1705330425  CXFBCM1A  10.1.2.3   54321      192.168.1.1  80         GET     evil.example.com /payload/mal.exe  -         python-requests/2  200          102400
```

**ssl.log** -- TLS/SSL handshakes:
```
ts          uid       id.orig_h  id.orig_p  id.resp_h    id.resp_p  version  cipher               curve    server_name      established  cert_chain_fuids  subject              issuer               validation_status
1705330425  CXFBCM1A  10.1.2.3   54321      1.2.3.4      443        TLSv12   TLS_AES_256_GCM_SHA  x25519   evil.example.com  T            FuniqID1         CN=evil.example.com  CN=Let's Encrypt     ok
```

**files.log** -- Files observed traversing the network:
```
ts          fuid      tx_hosts   rx_hosts  source  depth  analyzers  mime_type                  filename       duration  md5                               sha1
1705330425  FuniqID1  1.2.3.4   10.1.2.3  HTTP    0      MD5,SHA1   application/x-dosexec      malware.exe    0.1       d41d8cd98f00b204e9800998ecf8427e
```

**x509.log** -- TLS certificate details:
```
ts          id        certificate.subject      certificate.issuer  certificate.not_valid_before  certificate.not_valid_after  san.dns
1705330425  FcertID   CN=evil.example.com      CN=Let's Encrypt    2024-01-01                   2024-04-01                   evil.example.com,*.evil.example.com
```

**notice.log** -- Zeek notice framework output (from scripts that generate notices):
```
ts          uid       note              msg                                  src         dst         sub
1705330425  CXFBCM1A  HTTP::SQL_Injection  SQL injection attempt detected   10.1.2.3    1.2.3.4     /search?q=1'%20OR%201=1
```

**Other important logs:**
| Log | Content |
|---|---|
| `weird.log` | Protocol anomalies and unexpected behavior |
| `smb_files.log` | SMB file operations |
| `smb_mapping.log` | SMB share mapping events |
| `ntlm.log` | NTLM authentication exchanges |
| `kerberos.log` | Kerberos authentication events |
| `ftp.log` | FTP sessions |
| `ssh.log` | SSH connections (includes hassh fingerprints) |
| `smtp.log` | Email transactions |
| `tunnel.log` | Tunneled traffic detection |
| `dpd.log` | Dynamic Protocol Detection failures |
| `capture_loss.log` | Packet loss indicators |
| `reporter.log` | Zeek internal messages |
| `pe.log` | Portable Executable (Windows binary) metadata |

### Log Correlation Using uid

The `uid` field is critical -- it uniquely identifies each connection and links across all log types:

```bash
# Find all log entries for a specific connection
UID="CXfbCm1ABCDEF123"

# In all logs simultaneously
grep $UID conn.log http.log ssl.log files.log dns.log

# With zcat for compressed logs
zcat /path/to/logs/2024-01-15/*.log.gz | grep $UID

# Using zeek-cut for structured output
cat conn.log | zeek-cut uid id.orig_h id.resp_h service duration | grep $UID
```

### zeek-cut Utility

`zeek-cut` extracts specific fields from Zeek tab-separated logs:

```bash
# Extract specific fields from conn.log
cat conn.log | zeek-cut ts id.orig_h id.resp_h id.resp_p proto service duration

# Filter with awk
cat conn.log | zeek-cut id.orig_h id.resp_h id.resp_p bytes | awk '$4 > 1000000'

# Count connections by destination
cat conn.log | zeek-cut id.resp_h id.resp_p | sort | uniq -c | sort -rn | head 20

# Convert epoch timestamps to human-readable
cat conn.log | zeek-cut -d ts id.orig_h id.resp_h
```

### Zeek Scripting Language

Zeek's scripting language is event-driven. Scripts subscribe to events generated by the protocol analyzers and network framework.

**Script structure:**
```zeek
##! Script description using ##! for doc comments

module MyModule;

# Global variables and state
global suspicious_hosts: set[addr] = {};

# Export definitions (accessible from other scripts)
export {
    ## Redef logging stream to add custom fields
    redef enum Log::ID += { LOG };
    
    type Info: record {
        ts:   time    &log;
        host: addr    &log;
        note: string  &log;
    };
}

# Event handler: called when Zeek sees an HTTP request
event http_request(c: connection, method: string, original_URI: string,
                   unescaped_URI: string, version: string)
{
    if ( /\.exe$/ in unescaped_URI ) {
        # Generate a notice
        NOTICE([$note=Notice::Policy,
                $msg=fmt("EXE download: %s", unescaped_URI),
                $conn=c,
                $identifier=cat(c$id$orig_h, unescaped_URI)]);
    }
}

# Event handler: called at script initialization
event zeek_init()
{
    Log::create_stream(MyModule::LOG, [$columns=Info, $path="my_custom"]);
    print "MyModule initialized";
}

# Event handler: called on connection close
event connection_state_remove(c: connection)
{
    if ( c$id$resp_h in suspicious_hosts ) {
        Log::write(MyModule::LOG, [$ts=network_time(),
                                   $host=c$id$resp_h,
                                   $note="Connection to suspicious host"]);
    }
}
```

**Common events to handle:**
| Event | When |
|---|---|
| `zeek_init()` | Script loaded |
| `zeek_done()` | Zeek shutting down |
| `new_connection(c)` | New connection started |
| `connection_state_remove(c)` | Connection closed |
| `http_request(c, method, uri, ...)` | HTTP request observed |
| `http_reply(c, version, code, reason)` | HTTP response observed |
| `dns_request(c, msg, query)` | DNS query |
| `dns_A_reply(c, msg, ans, TTL)` | DNS A record response |
| `ssl_client_hello(c, version, ...)` | TLS client hello |
| `ssl_server_hello(c, version, ...)` | TLS server hello |
| `file_new(f)` | New file observed |
| `file_hash(f, kind, hash)` | File hash computed |
| `smb1_tree_connect_andx_request(c, ...)` | SMB tree connect |
| `ssh_auth_result(c, result, ...)` | SSH auth result |

**Data types:**
```zeek
# Basic types
local s: string = "hello";
local i: int = 42;
local c: count = 0;
local r: double = 3.14;
local b: bool = T;
local t: time = current_time();
local a: addr = 10.0.0.1;
local p: port = 80/tcp;
local sub: subnet = 10.0.0.0/8;

# Compound types
local s_set: set[addr] = {};
local s_vec: vector of string = vector();
local s_table: table[addr] of count = {};

# Connection record (the most important type)
local conn: connection;  # Has c$id, c$orig, c$resp, c$service, c$uid, etc.
```

**Pattern matching:**
```zeek
# Check if string matches regex
if ( /malware/ in some_string ) { ... }

# Check subnet membership
if ( some_addr in 10.0.0.0/8 ) { ... }

# Check set membership
if ( some_addr in suspicious_hosts ) { ... }
```

### Intelligence Framework

The Zeek Intelligence Framework allows feeding IOC feeds into Zeek for real-time matching:

**Intel feed format (tab-separated):**
```
#fields indicator	indicator_type	meta.source	meta.desc	meta.url
1.2.3.4	Intel::ADDR	my_feed	Known C2 IP	https://source.example.com
evil.example.com	Intel::DOMAIN	my_feed	Malware domain	https://source.example.com
d41d8cd98f00b204e9800998ecf8427e	Intel::FILE_HASH	my_feed	Malware MD5
```

**Loading intel:**
```zeek
# /etc/zeek/site/intel.zeek
@load frameworks/intel/seen
@load frameworks/intel/do_notice

redef Intel::read_files += {
    "/etc/zeek/intel/malicious-ips.intel",
    "/etc/zeek/intel/malicious-domains.intel",
    "/etc/zeek/intel/malware-hashes.intel"
};
```

**Intel types:**
- `Intel::ADDR` -- IP address
- `Intel::SUBNET` -- IP subnet
- `Intel::URL` -- URL
- `Intel::SOFTWARE` -- Software version string
- `Intel::EMAIL` -- Email address
- `Intel::DOMAIN` -- Domain name
- `Intel::USER_NAME` -- Username
- `Intel::FILE_HASH` -- File hash (MD5/SHA1/SHA256)
- `Intel::FILE_NAME` -- File name
- `Intel::CERT_HASH` -- Certificate hash

### Zeek Packages (ZKG)

The Zeek Package Manager (`zkg`) installs community packages:

```bash
# Install package manager (usually bundled with Zeek)
pip3 install zkg

# Refresh package list
zkg refresh

# Search for packages
zkg search zeek-long-connections
zkg search dns-tunneling

# Install packages
zkg install zeek-long-connections
zkg install corelight/bro-sysmon
zkg install zeek/packages/ja3

# List installed
zkg list installed

# Enable installed packages (add to site/packages.zeek)
echo "@load packages" >> /etc/zeek/site/local.zeek
```

**Essential packages:**
- `zeek/zeek-ja3` -- JA3 TLS fingerprinting (adds ja3 hash to ssl.log)
- `corelight/zeek-community-id` -- Community ID flow hashing (links Zeek, Suricata, Elastic)
- `zeek/zeek-long-connections` -- Detects unusually long connections (beaconing)
- `corelight/bro-simple-scan` -- Port scan detection
- `zeek/zeek-EternalSafety` -- EternalBlue/MS17-010 detection
- `mitre-attack/bzar` -- MITRE ATT&CK-based detection scripts

## Threat Hunting with Zeek Logs

### Common Hunt Queries

**Beaconing detection (regular interval connections):**
```bash
# Find hosts making many small connections to the same destination
cat conn.log | zeek-cut id.orig_h id.resp_h id.resp_p duration orig_bytes \
  | awk '$4 < 5 && $5 < 1000' \
  | awk '{print $1, $2, $3}' \
  | sort | uniq -c | sort -rn \
  | awk '$1 > 100'  # More than 100 short connections = potential beacon
```

**DNS with high NX domain rate (potential DGA):**
```bash
cat dns.log | zeek-cut id.orig_h query rcode \
  | awk '$3 == 3' \  # NXDOMAIN = rcode 3
  | awk '{print $1}' \
  | sort | uniq -c | sort -rn \
  | awk '$1 > 50'    # More than 50 NX domains from single host
```

**Large outbound file transfers:**
```bash
cat conn.log | zeek-cut ts id.orig_h id.resp_h service orig_bytes resp_bytes \
  | awk '$5 > 10000000' \  # Originator sent > 10MB (potential exfil)
  | awk '!($4 == "http" || $4 == "ssl")' \ # Exclude normal web traffic
  | sort -k5 -rn
```

**New external connections from internal hosts:**
```bash
# Connections to IPs not seen in previous 7 days (requires log comparison)
# Practical approach: look for connections to IPs with low history
cat conn.log | zeek-cut ts id.orig_h id.resp_h id.resp_p service \
  | awk '!/^(10\.|172\.(1[6-9]|2[0-9]|3[01])\.|192\.168\.)/' \
  | awk '{print $3}' | sort -u  # Unique external IPs contacted
```

**SMB lateral movement:**
```bash
cat smb_mapping.log | zeek-cut ts id.orig_h id.resp_h share path \
  | grep -E "\\\\(C|ADMIN|IPC)\$" \  # Admin share access
  | sort
```

**Kerberoasting detection:**
```bash
cat kerberos.log | zeek-cut ts id.orig_h request_type service cipher error_msg \
  | awk '$2 == "TGS" && $4 == "rc4-hmac"' \  # RC4 encryption for service tickets = Kerberoasting
  | sort | uniq -c | sort -rn
```

## Common Pitfalls

1. **Expecting Zeek to block traffic** -- Zeek is passive/read-only. To block, you need Suricata IPS, firewall, or NAC integration.

2. **Not understanding uid correlation** -- Each connection has a unique `uid`. All logs for the same connection share this uid. Always use uid to pivot between log types during investigation.

3. **Ignoring `conn_state`** -- `S0` (connection attempt, no response) and `REJ` (rejected) are as forensically important as `SF` (successful). A mass of S0 events = port scan.

4. **Missing the `weird.log`** -- `weird.log` contains protocol anomalies that often indicate exploitation or evasion. It is underused but high signal.

5. **Writing Zeek scripts that aren't event-driven** -- Don't try to write procedural Zeek scripts. Structure everything as event handlers. State persistence happens through global tables and sets.

6. **Not using `zeek-cut` for field extraction** -- Parsing Zeek TSV logs with raw `awk`/`cut` is error-prone because field positions change when fields are added. Use `zeek-cut` which handles headers.

## Reference Files

Load these when you need deep knowledge for a specific area:

- `references/architecture.md` -- Zeek internals (event engine, script execution, cluster deployment with manager/logger/proxy/workers, log rotation, Spicy custom parsers, performance tuning). Read for architecture, cluster design, and advanced scripting questions.
