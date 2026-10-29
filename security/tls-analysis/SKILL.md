---
name: tls-analysis
description: Use when assessing the TLS configuration of a service you own
  or are authorized to test, or when decrypting your own captured traffic
  for troubleshooting. Covers certificate chain validation with openssl,
  protocol and cipher enumeration, testssl.sh comprehensive scans, TLS
  keylog decryption in Wireshark, and JA3/JA4 fingerprinting for detection.
  Use when a scanner flags weak ciphers, when you need to prove a
  misconfiguration, or when encrypted traffic must be inspected
  defensively.
version: 1.0.0
domain: crypto
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [crypto-fundamentals]
tools:
  - name: OpenSSL
    version: 3.x
  - name: testssl.sh
    version: 3.2.3
  - name: Wireshark
    version: 4.4
---

TLS analysis verifies that encrypted connections are actually secure:
valid certificates, modern protocol versions, strong cipher suites, and
correct server configuration. It also covers the defensive side of
decrypting traffic you are entitled to inspect, using key material from
your own clients. This skill gives you the openssl-first workflow for quick
checks, testssl.sh for comprehensive audits, and Wireshark keylog decryption
for troubleshooting your own captures. Scope: test only endpoints you own or
are authorized to assess, and decrypt only traffic you have the right to
inspect (your own systems, with the client's keylog or consent). Never
intercept or decrypt third-party traffic.

## Quick Workflow

1. Check the certificate chain, expiry, and hostname matching with
   `openssl s_client`.
2. Enumerate supported protocol versions and cipher suites.
3. Run testssl.sh for the full audit: vulnerabilities, headers, and
   misconfigurations.
4. Grade the findings by exploitability: protocol downgrade and weak
   ciphers first, informational items last.
5. For traffic inspection, capture with a keylog from your own client and
   decrypt in Wireshark.
6. Fingerprint TLS clients and servers (JA3/JA4) for detection baselines.
7. Write remediation: exact config changes, not vague advice.
8. Re-test after the fix to confirm the grade changed.

## 1. Certificate checks with openssl

The certificate is the first thing to verify and the most common thing to be
wrong: expired, wrong hostname, or an incomplete chain.

```bash
# Full handshake view: chain, cipher, protocol
openssl s_client -connect example.com:443 -servername example.com -showcerts < /dev/null 2>/dev/null | head -60

# Certificate dates and subject/issuer, one-liners
echo | openssl s_client -connect example.com:443 -servername example.com 2>/dev/null \
  | openssl x509 -noout -dates -subject -issuer

# Subject Alternative Names (the hostnames this cert is valid for)
echo | openssl s_client -connect example.com:443 -servername example.com 2>/dev/null \
  | openssl x509 -noout -ext subjectAltName

# Days until expiry (alert under 30)
echo | openssl s_client -connect example.com:443 -servername example.com 2>/dev/null \
  | openssl x509 -noout -checkend 2592000 && echo "OK: more than 30 days" || echo "RENEW SOON"

# Verify the full chain against system trust store
openssl s_client -connect example.com:443 -servername example.com -verify_return_error < /dev/null 2>&1 | grep -E 'Verify return code'
```

Always pass `-servername` (SNI); without it you may get the default vhost's
certificate and misdiagnose a healthy server. A `Verify return code: 21`
means an incomplete chain (missing intermediate), which is a server config
bug, not a CA problem.

## 2. Protocol and cipher enumeration

Find out what the server actually negotiates, including the legacy protocols
it should have disabled years ago.

```bash
# Which protocol versions are accepted? (try each explicitly)
for proto in tls1 tls1_1 tls1_2 tls1_3; do
  printf "%-8s: " "$proto"
  echo | timeout 5 openssl s_client -connect example.com:443 -servername example.com -$proto < /dev/null 2>&1 \
    | grep -E 'Protocol  :' | head -1
done

# Cipher suites offered (openssl lists what IT offers; testssl.sh enumerates the server)
nmap --script ssl-enum-ciphers -p 443 example.com 2>/dev/null | head -40

# Check one specific weak cipher directly
echo | timeout 5 openssl s_client -connect example.com:443 -cipher 'DES-CBC3-SHA' < /dev/null 2>&1 | grep -E 'Cipher    :'
```

Anything below TLS 1.2 in 2026 is a finding. 3DES, RC4, export ciphers, and
anonymous (ADH/AECDH) suites are findings. TLS 1.3-only is the ideal; TLS
1.2 with a tight cipher list is acceptable.

## 3. Comprehensive audit with testssl.sh

testssl.sh runs hundreds of checks in one go: protocols, ciphers, known
vulnerabilities (Heartbleed, POODLE, ROBOT, and friends), certificate
issues, and HTTP security headers.

```bash
# Full audit, HTML + JSON output for the report
./testssl.sh --htmlfile audit.html --jsonfile audit.json example.com

# Faster pass: vulnerabilities and protocols only
./testssl.sh -U -p example.com

# Cipher-focused pass
./testssl.sh -E -e example.com

# STARTTLS services (SMTP, IMAP, FTP): test the upgrade path too
./testssl.sh -t smtp mail.example.com:25
```

Read the output by severity: red items are exploitable now (SWEET32 with
3DES, LOGJAM with export DH), yellow items are hardening opportunities
(missing HSTS, TLS 1.0 still on). Quote the exact finding lines in your
report; "testssl.sh says BAD" is not evidence, the cipher string is.

## 4. Decrypting your own traffic in Wireshark

When you need to see inside TLS for troubleshooting your own systems, have
the client log session keys and point Wireshark at the log. This only works
with key material you legitimately hold.

```bash
# Have YOUR client log keys (example: curl or a browser you control)
export SSLKEYLOGFILE=/tmp/keys.log
curl --tlsv1.3 https://example.com/ -o /dev/null

# Capture the traffic at the same time
dumpcap -i eth0 -w tls_capture.pcap host example.com &

# In Wireshark: Preferences -> Protocols -> TLS -> (Pre)-Master-Secret log
# filename -> /tmp/keys.log, then reload the capture.
# tshark equivalent:
tshark -r tls_capture.pcap -o tls.keylog_file:/tmp/keys.log -Y http -T fields -e http.host -e http.request.uri | head -20
```

Limits to know: keylogging does not work for all clients, TLS 1.3 with
certain configurations resists it, and you must delete the keylog file when
done because it decrypts everything captured during the session. Never ask
a user for their keylog; generate it from systems you administer.

## 5. JA3 and JA4 fingerprinting

TLS handshakes fingerprint clients and servers. Defenders use these
fingerprints to spot malware C2 (which often uses unusual TLS libraries)
hiding in HTTPS noise.

```bash
# JA3 from a capture (tshark with ja3 fields, or a dedicated tool)
tshark -r tls_capture.pcap -Y tls.handshake.type==1 -T fields -e tls.handshake.ja3 2>/dev/null | sort -u | head

# JA4 is the modern successor (check your tshark/dissector version for support)
tshark -r tls_capture.pcap -Y tls.handshake.type==1 -T fields -e tls.handshake.ja4 2>/dev/null | sort -u | head

# Baseline your environment: collect fingerprints of known-good clients first,
# then alert on never-before-seen fingerprints talking to rare destinations
```

Build the baseline before the incident: record the JA3/JA4 of your standard
browsers, updaters, and agents. During triage, a Python-based C2 client or a
Go implant has a distinctive handshake that stands out against that
baseline immediately.

## 6. Remediation write-up

Vague advice ("use strong ciphers") gets ignored. Write the exact config.

```bash
# Example: nginx hardening snippet for the report
cat <<'EOF'
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers 'TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
ssl_prefer_server_ciphers on;
add_header Strict-Transport-Security "max-age=63072000" always;
EOF

# Verify the fix with a retest, same commands as the audit
./testssl.sh -p -e example.com | grep -E 'offered|OK|NOT ok' | head -20
```

## Edge cases

- SNI required but you forgot `-servername`: you audited the wrong vhost.
  Re-run with SNI for every hostname on the server.
- Server behind a CDN or WAF: you tested the edge, not the origin. Note
  which one in the report; both matter, but they are different findings.
- Client certificate required (mTLS): openssl needs `-cert` and `-key`;
  without them the handshake fails and the audit is incomplete.
- testssl.sh is slow on some hosts: use targeted flags (`-p`, `-U`, `-E`)
  instead of the full run, and raise timeouts for high-latency targets.
- Keylog decryption shows nothing: the session used a cipher or extension
  your Wireshark build cannot handle, or the keylog did not cover that
  session. Verify keylog timestamps overlap the capture.

## Escalation

- Findings disputed by the server team ("the scanner is wrong"): reproduce
  with raw openssl commands from section 2 and show the exact handshake;
  openssl output ends arguments.
- Need to prove exploitability, not just presence: demonstrate with a
  controlled downgrade or a decrypt of a captured session using a weak
  cipher, only within the authorized scope, and stop at proof of concept.
- Internal PKI issues (private CA, short-lived certs): audit the CA
  practices themselves (key storage, issuance policy, revocation), not just
  the leaf certificates.
- Encrypted traffic you cannot decrypt but must analyze: fall back to
  metadata analysis (JA3/JA4, SNI, flow sizes and timing) which needs no
  keys.

## Detection and defender view

TLS is both a shield and a hiding place: it protects your users and it
protects attacker C2 equally. Defenders should inventory TLS everywhere
(expire certs before they expire you, via monitoring), enforce TLS 1.2+
with a managed cipher policy, and deploy JA3/JA4 baselining on egress to
catch non-browser TLS clients beaconing out. Watch for the defensive
failure modes: expired certificates breaking monitoring, overly broad
cipher lists kept for "compatibility", and TLS inspection middleboxes with
weak configurations of their own. The misuse case is intercepting traffic
you have no right to see; certificate checks and audits are authorized
assessment work, while decrypting third-party traffic is interception, and
the line between them is consent and scope.

## Key references

- MITRE ATT&CK T1040 (Network Sniffing): the traffic this analysis
  protects.
- MITRE ATT&CK T1573 (Encrypted Channel) and T1071.001 (Web Protocols):
  attacker use of TLS this analysis helps detect.
- MITRE ATT&CK T1557 (Adversary-in-the-Middle): the attack weak TLS
  enables.
- CWE-327 (Use of a Broken or Risky Cryptographic Algorithm): weak
  ciphers and protocols.
- CWE-295 (Improper Certificate Validation): chain and hostname failures.
- CWE-311 (Missing Encryption of Sensitive Data): the gap TLS fills.
- OpenSSL documentation: https://www.openssl.org/docs/
- testssl.sh: https://github.com/testssl/testssl.sh
- Wireshark TLS preferences: https://www.wireshark.org/docs/
