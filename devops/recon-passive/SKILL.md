---
name: recon-passive
description: Use when starting authorized reconnaissance on a target domain or organization while staying off the target's own infrastructure. Passive reconnaissance with whois, dig against public resolvers, crt.sh certificate transparency logs, Shodan, Censys, theHarvester, Sublist3r, and Amass in passive mode. Covers registrant and IP block data, DNS records from third party resolvers, subdomain discovery from public sources, exposed services and certificates in indexed databases, and clean OSINT consolidation. Teaches what is truly passive, what quietly touches the target, and how to build the baseline that active recon extends.
version: 1.0.0
domain: recon
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: []
tools:
  - name: whois
    version: 5.5
  - name: dig
    version: 9.18
  - name: theHarvester
    version: 4.6
  - name: Sublist3r
    version: "1.0"
  - name: Amass
    version: 4.2
  - name: crt.sh
    version: 2026.x
  - name: Shodan
    version: 2026.x
  - name: Censys
    version: 2026.x
---

Passive reconnaissance is intelligence gathering that never sends packets to the
target's own servers. You query registrars, public DNS resolvers, certificate
transparency logs, and indexed databases that other people built. This skill
covers the full passive workflow for an authorized engagement or bug bounty:
who owns what, which names exist, which services are already indexed, and how
to merge it all into a clean baseline. The baseline feeds the recon-active
skill, which picks up where passive work ends.

## Quick Workflow

1. Confirm written authorization and record the exact scope (domains, IPs, rules) before you collect anything.
2. Pull registration and IP block data with whois.
3. Query DNS records through public resolvers with dig, never against the target's authoritative servers.
4. Mine certificate transparency logs with crt.sh for subdomains and certificate metadata.
5. Search indexed infrastructure on Shodan and Censys for the target's IPs, domains, and certificates.
6. Harvest emails, names, and hosts with theHarvester from search engines and public sources.
7. Enumerate subdomains passively with Sublist3r and Amass in passive mode.
8. Deduplicate everything, resolve each name to an IP through a public resolver, and write one consolidated target list.

## 1. Confirm scope first

Passive does not mean permissionless. Write down the authorized domains, IP
ranges, and any off-limits assets before you run anything. Certificate
transparency logs and search engines already contain the data, but keeping a
scope file proves you stayed inside it if anyone asks.

```bash
mkdir -p recon/example.com
cd recon/example.com
cat > SCOPE.txt <<'EOF'
Client: Example Ltd
Authorized: example.com, *.example.com, 203.0.113.0/24
Off limits: partner.example.com (third party)
Authorization ref: SOW-2026-041
EOF
```

## 2. Registration and IP ownership with whois

whois tells you the registrar, name servers, creation dates, and sometimes
abuse contacts. It is a query to a registrar or regional internet registry,
not to the target, so it stays passive.

```bash
whois example.com
whois -h whois.arin.net 203.0.113.45
whois -h whois.ripe.net 203.0.113.45
```

What to record: registrar, name servers (they hint at the DNS provider and
possible DNS admin panels), creation and expiry dates (fresh domains in
phishing-themed engagements are a flag), and the netblock owner and abuse
contact. Registrant names are usually redacted under GDPR, so do not expect
much there. Record the registry output in your notes; it rarely changes during
an engagement.

## 3. DNS records through public resolvers

dig is passive only when the queries go to a resolver you do not own and the
target's authoritative server never sees your IP. Use a big public resolver and
ask for the standard record types.

```bash
dig +short example.com A @1.1.1.1
dig +short example.com AAAA @8.8.8.8
dig +short example.com MX @1.1.1.1
dig +short example.com TXT @1.1.1.1
dig +short example.com NS @8.8.8.8
dig +short example.com SOA @1.1.1.1
```

Read the SOA record for the admin mailbox and serial (format often reveals the
DNS software). Read TXT records for SPF and verification tokens; SPF lists the
mail providers the target trusts, and verification tokens name third party
services (Google, Microsoft, Zoom, and similar). MX records name the mail
provider, which matters for phishing-resistant assessments later. Never attempt
a zone transfer (AXFR) here; that query hits the authoritative server directly
and belongs in recon-active.

## 4. Certificate transparency with crt.sh

Every public TLS certificate is logged to certificate transparency. crt.sh
lets you search those logs, which is one of the richest passive subdomain
sources. You are querying crt.sh, not the target.

```bash
curl -s "https://crt.sh/?q=%25.example.com&output=json" \
  | jq -r '.[].name_value' \
  | sed 's/^\*\.//' \
  | sort -u > crt-subs.txt
wc -l crt-subs.txt
head -20 crt-subs.txt
```

The leading `%25` is a URL-encoded wildcard, so this catches
`mail.example.com` and deeper names. Strip the wildcard entries and dedupe.
Also read the issuer and validity dates: certificates issued yesterday for a
new subdomain can reveal infrastructure being staged. Check both the current
name and old names, because crt.sh keeps history and forgotten subdomains are
common findings.

## 5. Indexed infrastructure: Shodan and Censys

Shodan and Censys scan the whole internet continuously, so you can search their
indexes instead of touching the target. You need an account and an API key for
serious use; the free tiers are enough for small scopes.

```bash
shodan init YOUR_API_KEY
shodan host 203.0.113.45
shodan search "ssl:example.com" --fields ip_str,port,org --limit 50
shodan search "org:\"Example Ltd\" http.title:\"login\"" --limit 50
```

```bash
export CENSYS_API_ID="your-id"
export CENSYS_API_SECRET="your-secret"
censys search "example.com and services.service_name: HTTP" \
  --index hosts | jq -r '.result.hits[] | "\(.ip) \(.services[].port)"' | sort -u
```

What to record: open ports with banners, HTTP titles (admin panels, login
pages, and default pages stand out), TLS certificate subjects and SANs (more
subdomains), autonomous system and geolocation, and historical data showing
when a service appeared. Shodan's `host` view shows every open port on one IP
with banners, which is often enough to plan the active phase without scanning.

## 6. People and email harvesting with theHarvester

theHarvester pulls emails, names, and hostnames from search engines, PGP key
servers, and other public sources. It never touches the target directly.

```bash
theHarvester -d example.com -b all -f harvester
theHarvester -d example.com -b bing,duckduckgo,crtsh -l 500
```

Review the XML and JSON output in the `harvester` files. Emails give you the
naming convention (first.last@example.com versus flast@example.com), which
feeds username lists for authorized password work later. Hostnames found here
merge into your subdomain list. Treat every email as personal data: keep it in
the engagement folder, do not publish it, and delete it when the engagement
closes.

## 7. Passive subdomain enumeration: Sublist3r and Amass

Sublist3r queries search engines for subdomains. Amass in passive mode queries
dozens of data sources (certificate logs, DNS databases, archives) without
sending a single packet to the target. Never run Amass without `-passive` at
this stage; the default mode does active DNS resolution and brute forcing.

```bash
python3 sublist3r.py -d example.com -o sublist3r.txt -t 20
amass enum -passive -d example.com -o amass-passive.txt
```

Amass passive runs can take 10 to 30 minutes because they query many sources.
Let it finish. When done, merge all subdomain lists and resolve them once
through a public resolver to drop dead names:

```bash
cat crt-subs.txt sublist3r.txt amass-passive.txt | sort -u > all-subs.txt
while read -r s; do
  ip=$(dig +short "$s" A @1.1.1.1 | head -1)
  [ -n "$ip" ] && echo "$s $ip"
done < all-subs.txt > resolved.txt
```

`resolved.txt` is your consolidated baseline: every live name with its current
IP. Save it. This file is the input to recon-active.

## 8. Consolidation checklist

Before you declare passive recon done, verify each of these is recorded:
registration data, NS and MX and TXT findings, the full crt.sh subdomain list,
Shodan and Censys hits with ports and banners, harvested emails with the
naming convention noted, the merged subdomain list, and the resolved name to
IP map. If two sources disagree on an IP, trust the freshest DNS answer and
note the disagreement.

## Edge cases

- crt.sh returns thousands of junk entries for domains behind shared hosting
  or CDN certificates. Filter by checking which names actually resolve, and
  ignore names that belong to the CDN provider.
- Shodan and Censys data can be weeks old. A port shown as open may be closed
  now. Treat indexed data as a lead, not as ground truth.
- theHarvester with `-b all` can take a long time and some sources rate limit
  you. If it stalls, run sources one at a time (`-b bing`, then `-b crtsh`).
- Amass passive mode still needs API keys for the best sources. Without keys
  it returns fewer results; add keys for AlienVault OTX, VirusTotal, and
  Shodan in the Amass config to widen coverage.
- Wildcard DNS (`*.example.com` resolving to one IP) makes every guessed name
  appear live. Detect it by resolving a random string like
  `no-such-name-xyz123.example.com`; if it resolves, the domain uses a
  wildcard and passive lists need filtering against it.
- GDPR redaction means whois often shows "REDACTED FOR PRIVACY". That is
  normal; move on to the technical data instead of chasing the registrant.

## Escalation

When passive sources run dry: pivot on what you have. Search Shodan for the
target's TLS certificate hash to find IPs serving the same cert. Search for
the organization's ASN and enumerate its netblocks, then look at neighboring
hosts in the same ranges. Check web archives for old subdomains that no
longer resolve but hint at naming patterns. Search code repositories for the
domain string; developers leak staging hostnames in public code. Each new
name goes back through resolution and into the baseline. Only when the
passive list stops growing do you move to recon-active.

## Detection and defender view

True passive recon is nearly invisible to the target: your queries hit
registrars, resolvers, and databases, not the target's servers. What the
defender can see: certificate transparency logs are public, so a defender
monitoring crt.sh sees the same subdomain data you do (good defenders watch
for new certificates on lookalike domains). Shodan and Censys show the
target what is already indexed about them. Search engine queries leave no
trace on the target. TheHarvester's search engine scraping can trip
rate limits on the search provider, not the target. The main OPSEC risk is
your own API keys: Shodan and Censys log your queries, so use an
engagement-specific account, not a personal one.

## Key references

- MITRE ATT&CK T1590 Gather Victim Network Information
- MITRE ATT&CK T1590.001 Domain Properties
- MITRE ATT&CK T1590.002 DNS
- MITRE ATT&CK T1593 Search Open Technical Databases
- MITRE ATT&CK T1593.001 Databases
- MITRE ATT&CK T1593.002 WHOIS
- MITRE ATT&CK T1593.003 Digital Certificates
- MITRE ATT&CK T1596 Search Open Websites/Domains
- CWE-200 Exposure of Sensitive Information to an Unauthorized Actor
- crt.sh documentation: https://crt.sh
- Shodan documentation: https://developer.shodan.io
- Censys documentation: https://search.censys.io/api
- theHarvester docs: https://github.com/laramies/theHarvester
- OWASP Amass docs: https://github.com/owasp-amass/amass
