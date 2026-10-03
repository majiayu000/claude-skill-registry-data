---
name: dns-domain-security
description: Secure the DNS and domain layer below TLS — the records, registrar, and provider access everyone forgets. Covers dangling records and subdomain takeover, registrar hardening and transfer locks, CAA, DNSSEC trade-offs, zone hygiene, split-horizon leakage, scoped DNS API tokens, and CT-log monitoring. Invoke when auditing a zone, when a domain or registrar account changes hands, or after decommissioning a SaaS service a CNAME pointed at.
---

# DNS & Domain Security

Everything above DNS assumes DNS is telling the truth. TLS certificates are issued based on DNS-validated control, email authentication lives in TXT records, and your entire brand hangs off a registrar login. Yet the DNS layer usually gets one setup session at launch and then years of unreviewed drift: records pointing at services that no longer exist, a registrar account with a password from 2019, and API tokens with zone-wide write access baked into three CI pipelines.

This skill audits and hardens that layer. The recurring theme is **lifecycle**: DNS records outlive the things they point to, and every orphaned pointer is a liability someone else can pick up.

## When to invoke

- Periodic audit of a zone you operate (quarterly is a good cadence)
- A SaaS service, PaaS app, or static-hosting project was decommissioned — did its DNS records go with it?
- Domain or registrar account is changing hands (team member left, agency handover, acquisition)
- A certificate appeared in CT logs that nobody requested
- Setting up DNS automation (CI, ACME DNS-01, dynamic records) and deciding token scope
- A domain in the portfolio is approaching expiry

## The threat map

| Layer | Attack | Primary control |
|---|---|---|
| Registrar account | Credential stuffing, social-engineered transfer | MFA (hardware key), transfer lock, registry lock |
| Domain lifecycle | Expiry → re-registration by attacker | Auto-renew, expiry monitoring, long registration |
| Zone content | Dangling CNAME → subdomain takeover | Stale-record audits, deprovision checklist |
| Certificate issuance | Unauthorized cert from any public CA | CAA records, CT-log monitoring |
| Resolution integrity | Cache poisoning, spoofed responses | DNSSEC (with operational care) |
| Provider API | Leaked token rewrites the zone | Per-zone scoped tokens, rotation |

Registrar compromise sits above everything: an attacker who controls the registrar account controls NS delegation, and from there every record, every cert, every mailbox. Harden top-down.

## Dangling records and subdomain takeover

A dangling record points at a resource you no longer control. The classic case: `app.example.com` is a CNAME to a PaaS or SaaS endpoint, the project gets deleted, the CNAME stays. On many providers, anyone can then claim that endpoint name and serve content — with a valid certificate — on **your** subdomain. That is a phishing page, cookie-scoped script host, or OAuth redirect target wearing your domain.

The same applies to A/AAAA records pointing at released cloud IPs, NS records delegating to a decommissioned nameserver, and MX records at a cancelled mail provider.

### Audit the zone for danglers

Export the zone from your provider (API or panel), then walk every CNAME target:

```bash
# zone.txt: one "name type target" per line, exported from your DNS provider
awk '$2 == "CNAME" {print $1, $3}' zone.txt | while read -r name target; do
  status=$(dig +short "$target" A | head -1)
  if [ -z "$status" ]; then
    echo "DANGLING? $name -> $target (no A record for target)"
  fi
done
```

A CNAME whose target does not resolve (`NXDOMAIN`) is the loudest signal — on several SaaS platforms that exact state means "claimable". But **resolving is not proof of safety**: a target that resolves to the provider's shared ingress while returning the provider's "no such app / unknown domain" error page is often claimable too. Follow up on every CNAME to a third-party platform:

```bash
awk '$2 == "CNAME" {print $1}' zone.txt | while read -r name; do
  code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 10 "https://$name/")
  echo "$name -> HTTP $code"
done
# 404 / 502 / provider error page on a name you "own" = investigate immediately
```

And check A/AAAA records against infrastructure you still hold:

```bash
awk '$2 == "A" {print $1, $3}' zone.txt | while read -r name ip; do
  # Compare against your current inventory of owned IPs
  grep -q "^$ip$" owned-ips.txt || echo "ORPHAN IP: $name -> $ip"
done
```

**Remediation is deletion.** If a record's target is gone, the record goes too — same change window, ideally the same deprovisioning checklist. Make "remove DNS records" a mandatory step in every service-teardown runbook; that is the systemic fix.

## Registrar account hardening

The registrar account is the root of trust for the whole domain. Treat it like a production root credential.

- **MFA with a hardware key or TOTP** — never SMS; SIM-swap against a registrar account is a well-worn path
- **Unique, vaulted password** — this account must not share credentials with anything
- **Transfer lock (`clientTransferProhibited`)** on every domain — verify with `whois`, don't trust the panel:

```bash
whois example.com | grep -i 'status'
# want: clientTransferProhibited (and clientDeleteProhibited / clientUpdateProhibited where offered)
```

- **Registry lock** for high-value domains — a paid, manual-verification lock at the registry itself; changes require an out-of-band ceremony. Worth it for the domain your business runs on.
- **Expiry is an account-takeover path.** A lapsed domain gets re-registered by drop-catchers within minutes; the new owner receives your password resets, your mail, your OAuth callbacks. Auto-renew on, payment method current, **and** independent expiry monitoring:

```bash
whois example.com | grep -i 'expiry\|expiration'
# Alert at 60 and 30 days out — do not rely on registrar reminder emails alone
```

- **Registrant contact email must not be on the domain itself** — if `example.com` breaks, the reset email for its own registrar account must still arrive
- **WHOIS privacy** on, unless a compliance regime requires published contacts

## CAA — restrict who may issue certificates

CAA records tell certificate authorities which of them may issue for your domain. Without CAA, **any** publicly trusted CA will issue to anyone who can pass domain validation — which, combined with a dangling record or DNS hijack, becomes a valid cert on your name.

```
example.com.   CAA   0 issue "letsencrypt.org"
example.com.   CAA   0 issue "pki.goog"
example.com.   CAA   0 issuewild ";"
example.com.   CAA   0 iodef "mailto:security@example.com"
```

- `issue` — enumerate exactly the CAs you actually use (check your CDN/proxy's docs; they often issue via their own CA partners)
- `issuewild ";"` — forbid wildcard issuance entirely unless you deliberately use wildcards
- `iodef` — some CAs will report refused issuance attempts here

```bash
dig +short CAA example.com
```

CAA is checked at issuance time only — it does not revoke existing certs, and a CA that ignores the spec is a CA-compromise scenario, not something CAA solves. It is cheap, standard, and closes the "any CA, any attacker with DV" gap. Set it on every zone.

## DNSSEC — what it buys and what it costs

DNSSEC cryptographically signs your zone so resolvers can verify responses were not forged in transit. It protects against cache poisoning and off-path spoofing of **your zone's data**.

What it does **not** do: encrypt queries (that's DoH/DoT, a resolver-side concern), protect against a compromised registrar or DNS provider (they hold the keys), or help clients whose resolvers don't validate.

The operational risk is real: a botched key rollover or a DS record left at the registrar after switching DNS providers makes your zone **hard-fail** for every validating resolver — a self-inflicted outage that plain DNS cannot have.

- Prefer providers with **fully managed DNSSEC** (automatic rollovers, one-click DS via registrar integration)
- **When migrating DNS providers, remove the DS record at the registrar first**, wait out the TTL, then move — the top DNSSEC outage cause is a stale DS pointing at the old provider's keys
- Verify after any change:

```bash
dig +dnssec example.com A | grep -E 'RRSIG|flags'   # want RRSIG present, ad flag from a validating resolver
dig +short DS example.com @198.51.100.1              # DS at the parent must match current keys
```

If your provider only offers manual DNSSEC and you have no monitoring for it, enabling it can be a net risk increase. Decide deliberately; don't cargo-cult it on.

## Zone hygiene

- **Wildcards (`*.example.com`)** — a wildcard A/CNAME makes *every* nonexistent subdomain resolve. That widens cookie scope abuse, makes takeover-style phishing names (`login-secure.example.com`) resolve without the attacker touching your zone, and defeats dangling-record auditing because nothing ever NXDOMAINs. Enumerate real hostnames explicitly; reserve wildcards for platforms that genuinely need them, on a dedicated subdomain tier.
- **Stale-record inventory** — every record should have a known owner and purpose. If nobody can say what `legacy-api.example.com` is for, resolve that before an attacker does.
- **TXT sprawl** — TXT records accumulate: site-verification tokens for tools abandoned years ago, SPF includes for departed ESPs, ad-hoc key material. Each one leaks which vendors you use (recon gold) and some (stale verification tokens, stale SPF includes) grant standing capability to whoever controls the referenced service. Dump and prune:

```bash
dig +short TXT example.com
dig +short TXT _dmarc.example.com
# For each verification token: is the tool still in use? If not, delete.
```

- **Comment/tag records at the provider** if supported — `owner=platform-team, reason=acme-dns01, added=2026-08` turns future audits from archaeology into a diff.

## Split-horizon and internal hostname leakage

Internal infrastructure names do not belong in public zones. `vpn.example.com`, `jenkins.example.com`, `db-primary.example.com` resolving publicly — even to RFC 1918 addresses — hands attackers a labeled network map for free.

- Keep internal names in a **separate internal zone** (`internal.example.com` served only by internal resolvers, or a distinct private domain) — true split-horizon, not public records with private IPs
- Remember that **certificates leak names too**: a cert requested for an internal hostname via a public CA lands in CT logs forever. Use a wildcard cert at a boundary name, or an internal CA, for hosts that should stay unlisted.
- Audit what's already public: your zone export *is* the attacker's enumeration result. Read it with that lens — every name that surprises you would delight them.

## DNS provider access control

The DNS provider account and its API tokens can rewrite reality for your domain. Common failure: one account-wide "DNS edit everything" token pasted into CI for a single ACME DNS-01 challenge.

- **One token per automation, scoped to one zone**, minimum permissions (edit TXT only, if the provider supports record-type scoping)
- For ACME specifically, prefer **CNAME-delegated challenges** (`_acme-challenge.example.com` CNAME to a dedicated throwaway zone) so the token only touches that zone
- **Rotate tokens** on a schedule and immediately on any pipeline compromise; keep an inventory of which token lives where
- Provider account itself: MFA, audit log reviewed, humans and automation as separate members — the same discipline as the registrar
- Zone changes belong in **change control**: provider audit log at minimum, zone-as-code (Terraform/OctoDNS) with review if the zone is large enough to drift

## Monitoring

DNS problems are silent until exploited. Two external signals cover most of it:

- **Certificate Transparency logs** — every publicly trusted cert is logged. Watch your domains for issuance you didn't initiate; an unexpected cert is the earliest visible sign of a takeover or hijack in progress. Free watchers exist (e.g. crt.sh-based alerting, CA-provided CT monitors); spot-check manually:

```bash
curl -s "https://crt.sh/?q=%25.example.com&output=json" \
  | python3 -c 'import json,sys; [print(e["name_value"], e["not_before"]) for e in json.load(sys.stdin)]' \
  | sort -u | tail -30
```

- **Passive DNS** — services that record what names resolved to over time. Useful for spotting a subdomain of yours suddenly resolving somewhere new (takeover detection) and for reconstructing what a deleted record used to point at during incident response.
- **Scheduled self-checks** — cron the dangling-CNAME loop, the `whois` expiry/lock check, and a diff of the zone export against the last known-good copy. A zone diff landing in a chat channel weekly costs nothing and catches both drift and tampering.

## TTL strategy

TTLs are an incident-response parameter disguised as a performance knob.

- **Low TTL (60–300 s) on records you may need to move fast** — app endpoints, anything with a failover story. During an incident, a 24 h TTL means a full day of clients still resolving the compromised or dead target.
- **Higher TTL (1–24 h) is fine for stable plumbing** — MX, TXT/SPF, NS glue that changes rarely.
- The "low TTL helps attackers" worry is mostly misplaced: an attacker who can change your records can also change your TTLs. Low TTL on the *legitimate* record mainly determines how fast **you** can recover — a hijacked record with a long TTL keeps poisoning caches long after you fix the zone. Bias toward agility on anything user-facing.
- Before planned migrations, **drop the TTL one full old-TTL period in advance**, migrate, then raise it back.

## Quick checklist

- [ ] Registrar: MFA (non-SMS), unique vaulted password, reset email off-domain
- [ ] `whois` shows `clientTransferProhibited` on every domain; registry lock on crown-jewel domains
- [ ] Auto-renew on + independent expiry alerts at 60/30 days
- [ ] Zone exported; every record has a known owner and purpose
- [ ] Dangling-CNAME audit run; all CNAMEs to third-party platforms verified claimed-by-us
- [ ] A/AAAA records cross-checked against currently-owned IP inventory
- [ ] No wildcard records without a deliberate reason
- [ ] TXT records pruned; stale verification tokens and SPF includes removed
- [ ] CAA present: `issue` for actual CAs only, `issuewild ";"` if no wildcards, `iodef` set
- [ ] DNSSEC decision made deliberately; if on, managed rollovers + DS verified; if migrating providers, DS removal sequenced first
- [ ] No internal hostnames in public zones; internal names on internal resolvers; no internal names in CT via public CAs
- [ ] DNS API tokens: per-zone, minimal permissions, inventoried, rotation schedule
- [ ] CT-log monitoring active for all domains
- [ ] Dangling-record and zone-diff checks scheduled, not one-off
- [ ] TTLs: low on movable endpoints, deliberate everywhere else
- [ ] Service-teardown runbooks include "delete the DNS records"

## What this skill will not do

- Help claim, probe, or "test" a dangling subdomain on a domain you do not own — takeover checks are for your own zones only
- Assist with domain transfer, WHOIS manipulation, or registrar access for domains you do not control
- Recommend disabling DNSSEC purely to avoid operational effort where managed tooling exists — the trade-off must be argued, not defaulted
- Enumerate or fingerprint third-party zones beyond what auditing your own delegations requires
