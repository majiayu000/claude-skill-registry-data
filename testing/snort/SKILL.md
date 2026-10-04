---
name: snort
description: "Expert agent for Snort 3 IDS/IPS. Covers Snort 3 architecture (inspectors, codecs, DAQ), rule syntax with sticky buffers and service keyword, OpenAppID, hyperscan, Talos rule updates, and migration from Snort 2. WHEN: \"Snort\", \"Snort 3\", \"Snort rule\", \"Talos rules\", \"OpenAppID\", \"DAQ\", \"Snort inspector\", \"snort.lua\", \"Snort 2 migration\", \"hyperscan\"."
license: MIT
---

# Snort 3

This skill covers Snort 3, the rewritten IDS/IPS engine from Cisco Talos. It has deep knowledge of Snort 3's architecture, Lua-based configuration, rule language with sticky buffers, OpenAppID application identification, DAQ (Data Acquisition) layer, and the differences from Snort 2.

**Important:** Snort 2 reached end-of-life January 2026. All new deployments and migrations should use Snort 3. When users reference Snort 2 configuration, assist with migration to Snort 3.

## How to Approach Tasks

When you receive a request:

1. **Classify** the request:
   - **Rule writing** -- Apply Snort 3 rule syntax with sticky buffers
   - **Configuration** -- Apply Lua-based snort.lua configuration guidance
   - **Snort 2 migration** -- Load `references/architecture.md` for migration differences
   - **Architecture/internals** -- Load `references/architecture.md`
   - **Troubleshooting** -- Apply diagnostic methodology below

2. **Clarify Snort 2 vs. Snort 3** -- If the user mentions preprocessors, snort.conf, or other Snort 2 concepts, confirm they are migrating to Snort 3 and adjust guidance accordingly.

3. **Gather context** -- Deployment mode (IDS/IPS), throughput, OS, integration with Cisco ecosystem (FMC, FTD), existing rulesets.

4. **Recommend** -- Provide specific Lua configuration, rule syntax, or operational commands.

## Core Expertise

### Snort 3 vs. Snort 2 Key Differences

| Feature | Snort 2 | Snort 3 |
|---|---|---|
| Configuration | snort.conf (custom language) | snort.lua (Lua scripting) |
| Threading | Single-threaded | Multi-threaded (configurable) |
| Preprocessors | Preprocessors (fixed API) | Inspectors (modular, new API) |
| Rules | Classic rule syntax | Extended with sticky buffers, service keyword |
| Pattern matching | PCRE, AC-split | Hyperscan (Intel) for performance |
| Protocol decoders | Built-in codecs | Separate codec layer (extensible) |
| App identification | Limited | OpenAppID (full application fingerprinting) |
| Lua scripting | Not native | Lua rules and configuration |
| DAQ | Limited | DAQ v3 (pluggable capture modules) |

### Lua Configuration (snort.lua)

Snort 3 uses Lua for configuration, enabling programmatic configuration:

```lua
-- snort.lua

-- Network variables
HOME_NET = '10.0.0.0/8,172.16.0.0/12,192.168.0.0/16'
EXTERNAL_NET = '!$HOME_NET'
DNS_SERVERS = '$HOME_NET'
HTTP_SERVERS = '$HOME_NET'
HTTP_PORTS = '80,8080,8000,8008,443,8443'

-- Include default variables
include 'snort_defaults.lua'

-- Packet handling
daq = {
    module_dirs = { '/usr/lib/daq' },
    modules = {
        {
            name = 'afpacket',
            mode = 'passive'  -- or 'inline'
        }
    },
    inputs = { 'eth0' },
    snaplen = 65535
}

-- Network inspection configuration
normalizer = { tcp = { ips = true } }

-- Stream tracking
stream = {}
stream_tcp = {
    policy = 'windows',
    session_timeout = 180,
    max_pdu = 16384
}
stream_udp = { session_timeout = 30 }

-- Application layer inspectors
http_inspect = {
    request_depth = 1460,
    response_depth = 65535,
    normalize_utf = true,
    decompress_pdf = false
}

dns = { max_rdata_len = 255 }
ftp_server = { def_max_param_len = 100 }
smtp = { max_header_line_len = 1000 }
ssh = { max_client_bytes = 19600 }
ssl = {}
dce_tcp = {}
dce_udp = {}

-- Detection engine
detection = {
    hyperscan_literals = true,  -- Enable hyperscan for performance
    pcre_to_regex = true
}

-- Rule files
ips = {
    mode = ips.INLINE_TEST,  -- TEST mode first; switch to INLINE for blocking
    rules = [[
        include $RULE_PATH/snort3-community.rules
        include $RULE_PATH/snort3-registered.rules
        include $RULE_PATH/local.rules
    ]],
    variables = default_variables
}

-- Output (Unified2 for compatibility, or JSON)
alert_fast = { file = true, packet = false }
alert_json = {
    file = true,
    fields = 'timestamp pkt_num proto pkt_gen pkt_len dir src_ap dst_ap rule action'
}
log_pcap = { limit = 100 }

-- Performance statistics
perf_monitor = {
    modules = { flow = {} },
    format = 'text',
    output = 'stdout'
}
```

### Rule Syntax

Snort 3 rules maintain backward compatibility with Snort 2 rules but introduce several improvements.

**Classic rule format (still valid in Snort 3):**
```
alert tcp $HOME_NET any -> $EXTERNAL_NET $HTTP_PORTS (
    msg:"Custom HTTP Suspicious URI";
    content:"/malware.exe"; http_uri;
    nocase;
    sid:1000001; rev:1;
)
```

**Snort 3 sticky buffer style (preferred):**
```
alert http $HOME_NET any -> $EXTERNAL_NET any (
    msg:"Custom HTTP Malicious Download";
    http_uri;
    content:"/payload.exe";
    nocase;
    service:http;
    sid:1000001; rev:1;
)
```

**`service` keyword (Snort 3 key feature):**
The `service` keyword binds the rule to an application protocol detected by OpenAppID, independent of port:
```
# Detects HTTP regardless of port (detected by OpenAppID)
alert http any any -> any any (
    msg:"HTTP on Non-Standard Port";
    service:http;
    http_method;
    content:"POST";
    http_uri;
    content:"/c2/beacon";
    sid:1000002; rev:1;
)
```

**Sticky buffers in Snort 3:**
```
alert http any any -> any any (
    msg:"Suspicious Download User-Agent";
    http_header:"User-Agent";      # Sticky buffer for User-Agent header
    content:"python-requests";
    nocase;
    http_uri;
    content:"/download/";
    sid:1000003; rev:1;
)
```

**Snort 3 HTTP sticky buffers:**
| Buffer | Description |
|---|---|
| `http_uri` | Normalized URI path |
| `http_raw_uri` | Raw URI |
| `http_method` | HTTP method |
| `http_header` | Specific header value |
| `http_request_body` | Request body |
| `http_response_body` | Response body |
| `http_cookie` | Cookie header |
| `http_client_body` | Alias for request body |

**Lua-based rules (Snort 3 only):**
```lua
-- local.lua -- Can contain Lua rule functions
local function detect_custom(pkt)
    local payload = pkt:get_payload()
    if payload and payload:find("BEACON") then
        return true
    end
    return false
end
```

```
alert tcp any any -> any any (
    msg:"Lua Custom Detection";
    luajit:detect_custom.lua, detect_custom;
    sid:1000004; rev:1;
)
```

### OpenAppID

OpenAppID enables application-aware detection independent of port. Snort 3 can identify 3000+ applications.

**Enable OpenAppID:**
```lua
-- snort.lua
appid = {
    app_detector_dir = '/usr/lib/snort/appid',
    log_stats = true
}
```

**Use in rules:**
```
# Detect any BitTorrent traffic regardless of port
alert tcp any any -> any any (
    msg:"BitTorrent Application Detected";
    appid:BitTorrent;
    sid:1000005; rev:1;
)

# Detect Dropbox file sync
alert tcp $HOME_NET any -> $EXTERNAL_NET any (
    msg:"Dropbox Sync Detected";
    appid:Dropbox;
    sid:1000006; rev:1;
)
```

**List available app detectors:**
```bash
# List all included app detectors
ls /usr/lib/snort/appid/odp/lua/
```

### Talos Rule Updates

Snort 3 uses the same Talos ruleset infrastructure as Snort 2, with Snort 3-specific rule packages.

**Rule packages:**
- **Community rules** -- Free, basic coverage. Download from snort.org.
- **Registered rules** -- Free with registration. Delayed from subscriber rules.
- **Subscriber/Talos Intelligence** -- Paid subscription. Real-time rules with Talos threat intel.

**Manual update process:**
```bash
# Download community rules
wget https://www.snort.org/downloads/community/snort3-community-rules.tar.gz
tar -xzf snort3-community-rules.tar.gz -C /etc/snort/rules/

# Download registered/subscriber rules (requires oinkcode)
OINKCODE="your_oinkcode_here"
wget "https://www.snort.org/rules/snortrules-snapshot-3000.tar.gz?oinkcode=$OINKCODE" \
  -O snort3-rules.tar.gz
tar -xzf snort3-rules.tar.gz -C /etc/snort/rules/
```

**pulledpork3 automation:**
```bash
# Install pulledpork3
git clone https://github.com/shirkdog/pulledpork3.git
cd pulledpork3
pip3 install -r requirements.txt

# Configure /etc/pulledpork3/pulledpork.conf
# Set oinkcode, rule paths, enable/disable preferences

# Run update
python3 pulledpork.py -c /etc/pulledpork3/pulledpork.conf

# Reload Snort after rule update
kill -SIGHUP $(pidof snort)
```

### Inline IPS Mode

**AF_PACKET inline mode:**
```lua
daq = {
    modules = {
        {
            name = 'afpacket',
            mode = 'inline'
        }
    },
    inputs = { 'eth0:eth1' }  -- Colon separates inline pair
}

ips = {
    mode = ips.INLINE  -- Enable active blocking
}
```

**NFQ inline mode:**
```lua
daq = {
    modules = {
        {
            name = 'nfq',
            variables = {
                queue = '0'
            }
        }
    }
}
```

```bash
# iptables for NFQ
iptables -I FORWARD -j NFQUEUE --queue-num 0
snort -c /etc/snort/snort.lua --daq nfq --daq-var queue=0
```

### Hyperscan Integration

Hyperscan is Intel's high-performance regular expression library. Snort 3 uses it for fast pattern matching when available.

**Enable in configuration:**
```lua
detection = {
    hyperscan_literals = true,  -- Use hyperscan for literal (content) matching
    pcre_to_regex = true        -- Convert PCRE to hyperscan regex where possible
}
```

**Verify hyperscan is active:**
```bash
snort --version | grep -i hyperscan
snort --help-modules | grep hyperscan
```

**Performance impact:** Hyperscan can provide 2-5x improvement in pattern matching throughput for content-heavy rulesets.

## Troubleshooting

### Performance Diagnostics

```bash
# Check Snort performance statistics
snort -c /etc/snort/snort.lua --lua 'perf_monitor = { format="text", output="stdout" }' -i eth0

# Verify DAQ is working correctly
snort --daq-list
snort -c /etc/snort/snort.lua --daq afpacket --daq-var fanout_type=hash -i eth0 --pcap-show

# Test configuration without starting
snort -c /etc/snort/snort.lua -T
```

### Rule Testing

```bash
# Test rules against PCAP
snort -c /etc/snort/snort.lua -r /path/to/capture.pcap -A alert_fast

# Test single rule file
snort -c /etc/snort/snort.lua -r capture.pcap --rule 'alert tcp any any -> any any (msg:"Test"; sid:1;)'

# Verbose output for debugging
snort -c /etc/snort/snort.lua -r capture.pcap -v -d -e
```

### Common Issues

**Rules from Snort 2 not loading in Snort 3:**
- Snort 3 removed `flags:S+` syntax -- replace with `flags:S`
- `http_header;` in Snort 2 is different from `http_header` sticky buffer in Snort 3
- Some `urilen` syntax changed
- Run `snort -c snort.lua -T` to identify specific parse errors

**Application protocol not detected (service keyword not matching):**
- Verify OpenAppID is enabled and app detector directory is correct
- Check that the protocol is in the OpenAppID library: `ls /usr/lib/snort/appid/odp/`
- Application identification requires enough packets for handshake; won't trigger on first packet

**High CPU with hyperscan:**
- If hyperscan is not compiled in, Snort falls back to PCRE which is slower
- Verify: `snort --version` should show hyperscan version if compiled

## Common Pitfalls

1. **Using Snort 2 rule syntax directly** -- Most Snort 2 rules work, but `preprocessors`, `portvar`, and some keyword syntax differ. Test all imported rules with `snort -T`.

2. **Not using the `service` keyword** -- Rules without `service:` rely on port-based detection. Modern applications use non-standard ports. Add `service:http` to HTTP rules for port-independent detection.

3. **Missing OpenAppID detectors** -- The base Snort 3 package may not include all app detectors. Download the OpenAppID package from snort.org separately.

4. **Running inline mode without testing** -- Always run in `INLINE_TEST` mode first. This mode evaluates rules but does not drop packets, allowing you to identify false positives before enabling blocking.

5. **Ignoring Lua configuration errors** -- Lua syntax errors in snort.lua fail silently in some versions. Always run `snort -T -c snort.lua` after configuration changes.

## Reference Files

Load these when you need deep knowledge for a specific area:

- `references/architecture.md` -- Snort 3 internals (inspectors, codecs, DAQ layer, OpenAppID engine, Lua scripting API, comparison with Snort 2 for migration). Read for architecture, migration, and internals questions.
