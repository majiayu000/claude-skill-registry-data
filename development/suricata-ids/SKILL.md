---
name: suricata-ids
description: Use when deploying, tuning, or troubleshooting Suricata as a
  network intrusion detection sensor on a network you are authorized to
  monitor. Covers sensor placement and capture setup, rule syntax and
  Emerging Threats rulesets, EVE JSON logging, TLS and JA3 fingerprinting,
  performance tuning for high throughput, suppressing false positives, and
  feeding alerts into the SIEM. Use when the SOC needs network visibility,
  when tuning noisy NIDS alerts, or when validating a sensor deployment.
version: 1.0.0
domain: soc
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [incident-response]
tools:
  - name: Suricata
    version: "7.0"
  - name: tcpdump
    version: "4.99.5"
  - name: Python
    version: "3.12"
---

Suricata is an open source network IDS/IPS that inspects traffic against
signature rules and logs rich metadata (EVE JSON) for hunting. This skill
covers deploying a Suricata 7 sensor defensively: where to place it, how
to write and tune rules, how to read EVE logs, and how to keep it fast
enough to see everything. Only run sensors on networks you own or are
authorized to monitor.

## Quick Workflow

1. Place the sensor where it sees the traffic you care about (SPAN port,
   TAP, or inline) and verify it captures with tcpdump first.
2. Install Suricata 7, enable the Emerging Threats Open ruleset, and
   confirm rules load without errors.
3. Configure EVE JSON output with alert, dns, tls, http, and flow
   logging enabled.
4. Baseline for one week: record alert volume per rule and signature.
5. Tune: disable or threshold noisy rules, add suppressions for known-
   good traffic with ticket references.
6. Ship EVE logs to the SIEM and build dashboards for top alerts,
   top source IPs, and rule hit rates.
7. Review rule updates weekly and re-baseline after each update.
8. Test detection with a safe, local simulation (a lab attack host) and
   confirm the expected alerts fire.

## 1. Placement and capture

A sensor that does not see the traffic cannot detect anything. Options:

- SPAN/mirror port: easiest, no inline risk, but drops packets under
  load and misses traffic if the switch is oversubscribed.
- Network TAP: sees everything, no packet loss from mirroring, costs
  hardware.
- Inline (IPS mode): can block, but a sensor failure can break traffic
  unless you use a bypass TAP.

Verify capture before touching Suricata:

```bash
# Confirm the interface sees traffic (replace eth1 with your monitor iface)
sudo tcpdump -i eth1 -c 20 -nn

# Check for packet loss on the capture interface
cat /proc/net/dev | grep eth1

# Large receive offload can hide packets from the IDS; disable on monitor ifaces
sudo ethtool -K eth1 gro off lro off
```

For a lab, mirror a port on your switch or use a virtual SPAN in your
hypervisor. Document which network segments the sensor covers and,
critically, which it does not.

## 2. Installation and ruleset

```bash
# Ubuntu: install Suricata 7 from the official PPA
sudo add-apt-repository ppa:oisf/suricata-7.0
sudo apt update && sudo apt install -y suricata

# Update the Emerging Threats Open ruleset
sudo suricata-update

# Verify the rules load cleanly (do this after every rule change)
sudo suricata -T -c /etc/suricata/suricata.yaml

# Check the version and build features
suricata --build-info | head -30
```

Key paths: `/etc/suricata/suricata.yaml` (config),
`/var/lib/suricata/rules/suricata.rules` (downloaded rules),
`/var/log/suricata/eve.json` (alerts and metadata).

Enable the rulesets you need in `/etc/suricata/suricata.yaml` and use
`suricata-update` with a configuration that disables categories you do
not want (for example `emerging-games` on a corporate network).

## 3. Rule syntax

A Suricata rule has a header (action, protocol, addresses, ports) and
options in parentheses.

```text
alert http $HOME_NET any -> $EXTERNAL_NET any \
  (msg:"SUSP PowerShell download cradle pattern";
   flow:established,to_server;
   http.uri; content:"/powershell"; nocase;
   http.user_agent; content:"Mozilla"; nocase;
   classtype:trojan-activity; sid:9000001; rev:1;)
```

Important keywords:

```text
# Match a DNS query for a suspicious domain
alert dns $HOME_NET any -> any any \
  (msg:"SUSP DNS query to known bad TLD";
   dns.query; content:".xyz"; endswith;
   classtype:trojan-activity; sid:9000002; rev:1;)

# Match TLS SNI to a suspicious domain
alert tls $HOME_NET any -> $EXTERNAL_NET any \
  (msg:"SUSP TLS SNI to dynamic DNS host";
   tls.sni; content:".duckdns.org"; endswith;
   classtype:trojan-activity; sid:9000003; rev:1;)

# Threshold: only alert after 10 hits from one source in 60 seconds
alert http $HOME_NET any -> $EXTERNAL_NET any \
  (msg:"POSSIBLE brute force login attempts";
   flow:established,to_server; http.uri; content:"/login";
   threshold:type threshold, track by_src, count 10, seconds 60;
   classtype:attempted-recon; sid:9000004; rev:1;)
```

Rule hygiene: every local rule gets a `sid` above 9000000 (your private
range), a `rev` you bump on change, a `msg` that says what fired, and a
reference (URL or ticket) in a comment above it.

## 4. EVE JSON logging

EVE JSON is the main output you will hunt in. Enable the log types you
need in `suricata.yaml`:

```yaml
outputs:
  - eve-log:
      enabled: yes
      filetype: regular
      filename: eve.json
      types:
        - alert
        - dns:
            query: yes
            answers: yes
        - tls:
            extended: yes
        - http:
            extended: yes
        - flow
        - fileinfo
```

Read alerts with jq during tuning:

```bash
# Top alert signatures in the last hour
jq -r 'select(.event_type=="alert") | .alert.signature' /var/log/suricata/eve.json \
  | sort | uniq -c | sort -rn | head -20

# All alerts for one suspicious IP
jq -r 'select(.event_type=="alert" and .src_ip=="192.0.2.44")
  | "\(.timestamp) \(.alert.signature) \(.dest_ip):\(.dest_port)"' \
  /var/log/suricata/eve.json

# TLS handshakes with JA3 fingerprints (great for hunting malware C2)
jq -r 'select(.event_type=="tls") | "\(.src_ip) \(.tls.ja3.hash) \(.tls.sni)"' \
  /var/log/suricata/eve.json | sort | uniq -c | sort -rn | head -20
```

## 5. JA3 and protocol fingerprinting

JA3 fingerprints the TLS client handshake, which identifies malware
families even when the domain changes. Suricata logs it in EVE TLS
events.

```bash
# Find rare JA3 hashes (first step of a C2 hunt)
jq -r 'select(.event_type=="tls" and .tls.ja3.hash != null)
  | .tls.ja3.hash' /var/log/suricata/eve.json \
  | sort | uniq -c | sort -n | head -20

# Correlate a rare JA3 with its destinations
jq -r 'select(.event_type=="tls" and .tls.ja3.hash=="e7d705a3286e0e892b58c3f0a1d3cb7e")
  | "\(.src_ip) -> \(.dest_ip):\(.dest_port) sni=\(.tls.sni)"' \
  /var/log/suricata/eve.json | sort -u
```

Also useful: JA3S (server fingerprint), HASSH for SSH, and DHCP
fingerprints. Compare observed hashes against public JA3 feeds and your
own baseline of normal clients.

## 6. Performance tuning

A sensor that drops packets misses attacks. Watch the stats:

```bash
# Check capture drops (should stay near zero)
jq -r 'select(.event_type=="stats")
  | "\(.timestamp) capture.kernel_drops=\(.stats.capture.kernel_drops)"' \
  /var/log/suricata/stats.log | tail -5

# Or from the stats log directly
grep -a "capture.kernel_drops" /var/log/suricata/stats.log | tail -3
```

Tuning levers in `suricata.yaml`:

- Increase `runmode` workers: use `workers` mode on multi-queue NICs.
- Raise `stream.memcap` and `flow.memcap` if you see stream depth
  warnings, but watch total RAM.
- Disable protocol parsers you do not need (for example SMB parsing on
  a sensor that only watches DMZ web traffic).
- Use `bpf-filter` to skip trusted bulk traffic (backups, monitoring)
  at capture time.
- Pin Suricata to dedicated CPU cores and keep the management traffic
  off the monitor interface.

Rule of thumb: if `kernel_drops` grows during business hours, you need
more cores, fewer rules, or a BPF filter. Never ignore drops; they are
blind spots.

## 7. Tuning and suppression

Weekly tuning keeps the SOC from drowning:

```bash
# Find the noisiest rules over the last 7 days
jq -r 'select(.event_type=="alert") | "\(.alert.signature_id) \(.alert.signature)"' \
  /var/log/suricata/eve.json | sort | uniq -c | sort -rn | head -15
```

In `threshold.config`:

```text
# Suppress a noisy rule for the vulnerability scanner (ticket SOC-5200)
suppress gen_id 1, sig_id 2010935, track by_src, ip 198.51.100.10

# Rate-limit a chatty informational rule
threshold gen_id 1, sig_id 2013028, type limit, track by_src, count 1, seconds 3600
```

Process: for each top noisy rule, decide disable, threshold, or
suppress, record the ticket, and re-check after the next rule update.
Never suppress by destination IP of an external host; suppress the
known-good internal source instead.

## 8. Shipping to the SIEM

```bash
# Example: Filebeat shipping EVE JSON to Elastic
# /etc/filebeat/filebeat.yml snippet
filebeat.inputs:
  - type: log
    paths: [/var/log/suricata/eve.json]
    json.keys_under_root: true
    json.add_error_key: true
output.elasticsearch:
  hosts: ["https://elastic.internal:9200"]
```

Build SIEM content on top: a dashboard of alert volume by signature, a
watchlist of JA3 hashes seen in threat intel, and a correlation that
joins Suricata alerts with EDR process data on internal IP and time.

## Edge cases

- Encrypted traffic: Suricata sees metadata (SNI, JA3, cert fields),
  not payloads. Do not expect HTTP content rules to fire on HTTPS.
- Asymmetric routing: if the sensor sees only one direction, stream
  reassembly fails and many rules never fire. Fix the mirror, not the
  rules.
- VLAN tags: if the mirror port sends tagged frames and Suricata is
  not configured for VLANs, it may ignore the traffic. Test with
  tcpdump first.
- ET rules update weekly and can change alert volume overnight. Diff
  the ruleset on update and re-baseline noisy new rules.
- Large file transfers trigger file extraction rules. Exclude backup
  windows and known-good file servers with BPF or suppression.
- IPv6: rules written with `$HOME_NET` as IPv4-only miss IPv6
  traffic. Define both, or attackers will walk through the gap.

## Escalation

- Suricata fails to start after a rule change: run `suricata -T` to
  find the broken rule, fix or disable it, and restart. Keep the last
  known-good ruleset as a backup.
- Drops persist after tuning: reduce the active ruleset to
  `emerging-malware`, `emerging-exploit`, and `emerging-trojan` only,
  then add categories back one at a time while watching drops.
- Alerts point to an internal host: pivot to EDR and DHCP logs to
  identify the host, then follow the incident-response skill.
- You need full packet capture for forensics: add `pcap-log` or a
  dedicated full-packet recorder (Suricata is an alerting engine, not
  a packet archive).
- Sensor is blind to a segment: document the gap, propose TAP or SPAN
  placement, and note compensating controls (EDR, proxy logs) in the
  risk register.

## Detection and defender view

Suricata is a defender tool, so the attacker view is evasion:

- Attackers fragment packets and use overlapping segments to confuse
  reassembly. Keep `stream` reassembly at OS-policy defaults and
  updated; test with a lab IDS evasion tool to confirm.
- Attackers tunnel C2 over DNS, ICMP, or HTTPS to blend in. Write
  rules on anomaly metadata (long DNS labels, rare JA3, beaconing
  intervals) rather than only on known-bad domains.
- Attackers use valid certificates and CDNs, so SNI and cert rules
  miss them. Correlate network alerts with endpoint process data.
- Attackers slow scans to stay under thresholds. Keep a second,
  longer-window threshold rule for scan detection.
- Tune so the SOC trusts the sensor: a Suricata that pages on every
  scan gets ignored, and then the real alert gets missed too.

## Key references

- MITRE ATT&CK T1071.001 (Web Protocols), T1048 (Exfiltration Over
  Alternative Protocol), T1595 (Active Scanning), T1105 (Ingress Tool
  Transfer).
- Suricata 7 user guide: https://docs.suricata.io/en/suricata-7.0.0/
- Emerging Threats rules documentation:
  https://doc.emergingthreats.net/
- JA3 fingerprinting: https://github.com/salesforce/ja3
- EVE JSON schema: Suricata docs, "Eve JSON Output" chapter.
