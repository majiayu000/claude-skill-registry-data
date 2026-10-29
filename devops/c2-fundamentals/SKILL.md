---
name: c2-fundamentals
description: Use when designing the command and control layer of an authorized red team or adversary emulation exercise. C2 concepts including beaconing, callbacks, and tasking, channel design over HTTPS, DNS, and SMB, malleable profiles that shape traffic, redirectors with nginx, jitter and sleep for OPSEC, and infrastructure hygiene for authorized operations. Covers what each component hides from defenders, how defenders detect it, and the logging you owe the client. Requires network-pivoting for the routing layer that C2 traffic often travels through.
version: 1.0.0
domain: c2
lifecycle: stable
last_verified: "2026-10-23"
requires:
  - network-pivoting
extends: []
relates: []
tools:
  - name: Metasploit Framework
    version: 6.4.x
  - name: nginx
    version: 1.26.x
  - name: OpenSSH
    version: 9.6
  - name: openssl
    version: 3.x
  - name: Python
    version: 3.12
---

Command and control is how an operator talks to implants during an authorized
adversary emulation: tasking goes out, results come back, on a schedule the
operator controls. This skill covers C2 fundamentals for red teams working
under a signed rules of engagement: beaconing concepts, channel choices,
malleable profiles, redirectors, OPSEC basics, and the audit trail you owe
the client. It is about infrastructure design and tradecraft, not about
building malware. Nothing here is deployed against infrastructure you do not
own or have explicit written permission to test.

## Quick Workflow

1. Define the emulation objective and the exact C2 rules in the rules of engagement (allowed channels, hours, targets).
2. Choose the channel: HTTPS for blending in, DNS for restrictive egress, SMB for internal hops.
3. Stand up the team server on infrastructure you own, with TLS and access controls from minute one.
4. Put a redirector in front of it so the team server address never appears in traffic.
5. Shape the traffic with a profile: realistic URIs, headers, jitter, and sleep.
6. Test the full loop in the lab before the engagement window opens.
7. Log every session and tear everything down when the engagement ends.

## 1. Core concepts

A C2 loop has four parts. The implant (agent) lives on the in-scope target.
The team server issues tasks and stores results. The channel carries both
directions. The operator drives it. Beaconing is the heartbeat: the implant
checks in on an interval, picks up tasks, and sends back output. Callbacks
are the reverse, the server pushing to the implant, which rarely survives
egress filtering. Everything in modern C2 is beaconing with variations.

Two numbers define your noise: sleep (seconds between check-ins) and jitter
(random percentage added to sleep). Short sleep with no jitter is a
metronome that network anomaly detection spots in minutes. Long sleep with
high jitter looks like a human browsing pattern but slows your operation.
Start with sleep 60 and jitter 30 for interactive work, and lengthen both
when you need to be quiet.

```bash
openssl req -x509 -newkey rsa:4096 -keyout c2.key -out c2.crt \
  -days 90 -nodes -subj "/CN=cdn-updates.example.net"
```

Generate a fresh certificate for every engagement, with a plausible name on
a domain you own. Never reuse certificates, domains, or infrastructure
between clients; cross-contamination is how one engagement's indicators
burn the next.

## 2. Channel design

HTTPS is the default channel because it blends into normal web traffic and
most networks allow it outbound. The implant POSTs to innocuous-looking
URIs and the server answers inside normal-looking responses. Terminate TLS
on your redirector, not on the team server, so the server's real address
and certificate never face the target network.

DNS is the fallback channel for networks that proxy or inspect HTTPS but
leave DNS open. It is slow (data hides in subdomain labels and TXT
records) and DNS logging makes it highly visible to defenders who look.
Use it for check-ins and short tasking, not bulk exfiltration.

SMB and named pipes carry C2 between internal hosts without touching the
network perimeter at all: one internet-facing implant relays for internal
ones over the same protocols Windows uses constantly. This is where
network-pivoting and C2 meet: the pivot host becomes the egress point and
internal implants never talk to the internet directly.

Match the channel to the egress you actually measured during recon, not to
what you hope is open. Test each channel from the target network position
before relying on it.

## 3. Profiles: shaping the traffic

A malleable profile defines what your C2 traffic looks like on the wire:
HTTP method, URIs, headers, user agents, and how data is encoded inside
requests and responses. The goal is to resemble ordinary traffic for the
environment you are emulating against, not to be invisible.

```python
# Minimal profile concept: what the wire sees per check-in
profile = {
    "method": "GET",
    "uris": ["/static/js/app.min.js", "/api/v2/config", "/assets/logo.png"],
    "headers": {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "Accept": "application/json"},
    "sleep": 60,
    "jitter": 30,
}
```

Rotate URIs and user agents across beacons so no single pattern repeats
every 60 seconds. Encode tasking inside plausible content (JSON config
blobs, image metadata) rather than raw base64 in a query string, which is
a signature every proxy flags. Keep total beacon size small and irregular;
identical byte counts on a fixed schedule are trivially detectable.

## 4. Redirectors

A redirector sits between the target and your team server and forwards only
traffic that matches your profile. Everything else gets a benign response.
This protects the team server's address and filters out scanners, sandboxes,
and curious analysts who hit your domain.

A minimal nginx redirector that forwards only your beacon URI and serves a
decoy site otherwise:

```nginx
server {
    listen 443 ssl;
    server_name cdn-updates.example.net;
    ssl_certificate /etc/nginx/c2.crt;
    ssl_certificate_key /etc/nginx/c2.key;

    location /api/v2/config {
        proxy_pass https://TEAMSERVER_IP:8443;
        proxy_set_header Host $host;
    }
    location / {
        root /var/www/decoy;
    }
}
```

```bash
sudo nginx -t && sudo systemctl reload nginx
curl -sk https://cdn-updates.example.net/api/v2/config -o /dev/null -w "%{http_code}\n"
curl -sk https://cdn-updates.example.net/ -o /dev/null -w "%{http_code}\n"
```

Host the redirector on short-lived infrastructure in the engagement's name,
harden it like any internet-facing server (updates, firewall, no extra
services), and log what it forwards. Domain fronting through major CDNs
used to hide the true destination, but providers have largely killed it;
do not design around a dead technique. What still works is boring and
effective: a clean domain, valid TLS, and traffic that matches the profile.

## 5. OPSEC basics for authorized operations

OPSEC in an authorized engagement means staying inside the rules and not
burning the client's environment or your own infrastructure. Keep beacons
inside the agreed hours unless 24/7 is explicitly allowed. Never let an
implant talk to infrastructure outside the engagement's domain list. Cap
exfiltration volumes in the rules of engagement and enforce the cap in the
team server config; "we took 40 GB to prove a point" is not a finding, it
is an incident. Separate infrastructure per client and per engagement, and
never reuse a domain that a previous engagement burned. If the blue team
detects you, that is data, not failure: record the detection time and
technique in your notes, because measuring detection is often the
engagement's actual objective.

## 6. Logging and teardown

You owe the client a complete record: when each session started, which
target it ran on, every task issued, and every byte exfiltrated with its
justification. Keep team server logs for the retention period in the
contract, then destroy them as agreed. Teardown is a checklist, not a hope:
kill every implant session, confirm no beacons remain (watch the redirector
logs go silent), delete the redirector and team server infrastructure,
revoke the certificates, and release the domains or park them. Verify
silence for at least one full beacon interval past the longest sleep you
configured before you declare the engagement closed.

## Edge cases

- Egress proxies that do TLS inspection break naive HTTPS C2 and also
  reveal it immediately. If the target inspects TLS, either the rules of
  engagement cover it or you switch channels; do not try to bypass the
  client's own security controls without written permission.
- DNS channel throughput collapses on networks with DNS rate limiting.
  Keep DNS tasking tiny and expect multi-minute round trips.
- Sleep and jitter apply per implant; fifty implants beaconing at once is
  still a flood. Stagger initial check-ins and cap concurrent sessions.
- Redirector misconfiguration that proxies everything (no filtering)
  exposes the team server to anyone who finds the domain. Test the decoy
  response from an unprofiled client before the engagement starts.
- Clock skew between implant and server breaks time-based profile logic.
  Use relative timing (sleep since last beacon), not absolute schedules.
- Losing the team server mid-engagement strands implants. Keep encrypted
  backups of the server state and document a recovery procedure before
  you need it.

## Escalation

When the primary channel is blocked or detected: fall back to the next
channel you tested during recon (HTTPS to DNS is the classic downgrade),
lengthen sleep and raise jitter, and reduce tasking to essentials. When a
redirector is burned (defenders blocklist the domain), cut it over to a
pre-staged spare domain rather than improvising new infrastructure
mid-engagement. When implants go silent, do not assume detection; check
redirector logs for connection attempts first, because network changes on
the client side cause most outages. If the blue team asks you to stop, you
stop immediately and start teardown; there is no escalation past that.

## Detection and defender view

Defenders detect C2 at several layers. Network: regular beacon intervals,
unusual user agents, JA3 TLS fingerprints that do not match real browsers,
DNS query volume and entropy anomalies, and connections to newly registered
or low-reputation domains. Endpoint: implant process behavior, injection
patterns, and persistence mechanisms. Proxy and TLS inspection: decoded
payloads that do not match the claimed content type. Your profile choices
decide which of these fire. Assume a competent blue team will find
long-running C2; the engagement measures how long it takes and what trips
first. Share your indicators with the defensive contact after the
engagement so they can build detections from real data.

## Key references

- MITRE ATT&CK T1071 Application Layer Protocol
- MITRE ATT&CK T1071.001 Web Protocols
- MITRE ATT&CK T1071.004 DNS
- MITRE ATT&CK T1090 Proxy
- MITRE ATT&CK T1132 Data Encoding
- MITRE ATT&CK T1008 Fallback Channels
- MITRE ATT&CK T1043 Commonly Used Port
- MITRE ATT&CK T1568 Dynamic Resolution
- MITRE ATT&CK T1573 Encrypted Channel
- CWE-200 Exposure of Sensitive Information to an Unauthorized Actor
- Metasploit Framework docs: https://docs.metasploit.com
- nginx docs: https://nginx.org/en/docs/
