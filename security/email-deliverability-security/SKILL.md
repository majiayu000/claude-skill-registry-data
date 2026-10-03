---
name: email-deliverability-security
description: Configure email authentication so legitimate mail lands and spoofed mail is blocked. Covers SPF, DKIM, DMARC (with the p=none → p=quarantine → p=reject migration path), MTA-STS, TLS-RPT, ARC, and BIMI. Invoke when launching a new sending domain, when domains are being spoofed, or when transactional email is landing in spam.
---

# Email Authentication & Deliverability Security

Email security has two faces — inbound (don't get phished) and outbound (don't get spoofed, don't land in spam). This skill is about the **outbound** posture: configuring SPF, DKIM, DMARC, and friends so your real mail authenticates and impostors are rejected.

Done right, this is a one-evening project per domain that pays off forever. Done wrong, your password reset emails land in junk and attackers send invoices to your customers from `accounting@yourdomain.com`.

## When to invoke

- Launching a new sending domain
- Your domain is being spoofed (you see bounce reports for mail you didn't send)
- Transactional mail (password reset, receipts) consistently lands in spam
- Consolidating from multiple ESPs to one
- An auditor asks about your DMARC posture
- After a phishing wave that abused your domain

## The pieces — what each record does

| Record | Purpose | Required? |
|---|---|---|
| **SPF** | Lists which servers are *allowed* to send for the domain | Yes |
| **DKIM** | Signs each message with a key in DNS; receiver verifies signature | Yes |
| **DMARC** | Tells receivers what to do when SPF or DKIM fails, and where to send reports | Yes |
| **MTA-STS** | Forces TLS between sending and receiving MTAs | Recommended |
| **TLS-RPT** | Receives reports of TLS failures | Recommended |
| **BIMI** | Shows your brand logo in supporting mail clients | Optional, requires DMARC enforcement + VMC |
| **ARC** | Preserves auth state when mail passes through forwarders (mailing lists) | Receiver-side mostly, set up if you forward |

A "fully authenticated" sending posture needs at least SPF + DKIM + DMARC with a real policy.

## Step 1 — SPF

SPF lists every IP / hostname / third-party allowed to send from your domain.

```
v=spf1 mx include:_spf.google.com include:mailgun.org include:sendgrid.net -all
```

Key rules:

- **`-all` (hard fail)** is the goal. `~all` (soft fail) is acceptable as a stepping stone but eventually move to `-all`.
- **10 DNS lookup limit.** Every `include:` and `a` and `mx` mechanism counts. Many ESPs publish records that chain dozens of `include:` and silently push you over the limit. Use [dmarcian's SPF surveyor](https://dmarcian.com/spf-survey/) to count.
- **Flatten if needed**: services like [mxtoolbox](https://mxtoolbox.com), [spfwizard](https://spf-record.com), or your own automation can resolve the chain to IPs once and produce a flat record. Refresh periodically — the providers change theirs.
- **One SPF record per domain.** Multiple TXT records starting with `v=spf1` is a permanent fail.

### Verify

```bash
dig +short TXT example.com | grep -i 'v=spf1'

# Send a test mail to a Gmail address you own, view "Show original" — SPF: PASS
```

## Step 2 — DKIM

DKIM is per-ESP. Each sending service gives you a public key to put in DNS; the ESP signs outgoing mail with the private key.

Add the records the ESP gives you, exactly. Common selectors: `default._domainkey`, `mailgun._domainkey`, `s1._domainkey`, etc.

```
mailgun._domainkey.example.com.   TXT  "v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQ..."
```

Rules:

- **2048-bit RSA preferred.** Some providers still default to 1024 — 2048 is the standard for new deployments.
- **One selector per ESP**, never reuse keys across providers.
- **Rotate periodically** (annual is fine for low-stakes; quarterly for high-stakes). Providers usually have a rotation flow.
- **Drop unused selectors** when you decommission an ESP — otherwise an attacker who somehow got the old key can keep signing.

### Verify

```bash
dig +short TXT mailgun._domainkey.example.com

# Test mail to Gmail → Show original → DKIM: PASS, domain alignment OK
```

## Step 3 — DMARC

DMARC ties SPF + DKIM together and tells receivers what to do on failure. It also gives you reports about who is sending mail as you (legitimate or otherwise).

**Start in monitoring mode** (`p=none`) — don't break your own mail by going straight to `reject`:

```
_dmarc.example.com.   TXT   "v=DMARC1; p=none; rua=mailto:dmarc-reports@example.com; ruf=mailto:dmarc-forensic@example.com; fo=1; adkim=s; aspf=s"
```

Fields:

- **`p=none|quarantine|reject`** — action when both SPF and DKIM fail to align. Start at `none`, watch reports for 2–4 weeks.
- **`rua=`** — daily aggregate reports. Receive these; they tell you who is sending as you.
- **`ruf=`** — per-failure forensic reports (often disabled by receivers due to privacy concerns).
- **`adkim=s|r`** — strict or relaxed DKIM alignment. `s` is stricter; most ESPs work with `r`.
- **`aspf=s|r`** — same for SPF.
- **`pct=`** — percent of mail to apply the policy to (used during migration; default 100).

### Migration path

```
Week 1–2:   p=none, pct=100     — collect reports, identify all legitimate senders
Week 3–4:   p=quarantine, pct=25 — 25% of failing mail goes to spam
Week 5–6:   p=quarantine, pct=100
Week 7–8:   p=reject, pct=25
Week 9+:    p=reject, pct=100    — fully enforced
```

If at any step the reports show a legitimate sender failing, pause and fix (add to SPF, get DKIM set up for that path) before advancing.

### Reading aggregate reports

DMARC reports are XML. Use a parser — handling them by hand does not scale.

Free / cheap options:

- [Postmark DMARC Monitoring](https://dmarc.postmarkapp.com) — free for personal domains
- [dmarcian](https://dmarcian.com) — free tier
- [Valimail Monitor](https://www.valimail.com/dmarc-monitor) — free
- Self-hosted: [parsedmarc](https://github.com/domainaware/parsedmarc) → Elasticsearch / OpenSearch / Loki

Look in reports for:

- **All your real ESPs passing** → good
- **Random IPs passing SPF/DKIM** → potentially a misconfigured legitimate forwarder, or a sender you forgot about, or your domain is leaked via an ESP that shouldn't have it
- **Random IPs failing** → spoofing attempts. Once `p=reject` is live, these get bounced.

## Step 4 — MTA-STS

MTA-STS forces TLS between mail servers. Without it, an attacker on the path between sending and receiving MTAs can downgrade to plaintext.

Two pieces:

1. **DNS TXT record**:

   ```
   _mta-sts.example.com.   TXT   "v=STSv1; id=20260512000000;"
   ```

2. **Policy file** at `https://mta-sts.example.com/.well-known/mta-sts.txt`:

   ```
   version: STSv1
   mode: enforce
   mx: *.example.com
   max_age: 86400
   ```

`mode: testing` first if you're cautious; `mode: enforce` once you're sure your MX is reachable over TLS.

## Step 5 — TLS-RPT

Pair with MTA-STS to get reports on TLS failures.

```
_smtp._tls.example.com.   TXT   "v=TLSRPTv1; rua=mailto:tls-reports@example.com"
```

## Step 6 — BIMI (optional, brand polish)

BIMI shows your brand logo in supporting mail clients (Gmail, Yahoo, Apple Mail). Requires:

- DMARC at `p=quarantine` or `p=reject` (so not on day one)
- SVG logo at a public URL (specific spec — square aspect, basic profile)
- Verified Mark Certificate (VMC, ~$1500/year from DigiCert or Entrust) for Gmail / Apple Mail to display

```
default._bimi.example.com.   TXT   "v=BIMI1; l=https://example.com/logo.svg; a=https://example.com/vmc.pem"
```

Skip until everything else is enforced. Marketing rather than security.

## Common patterns and pitfalls

**Subdomains.** Receivers don't apply your apex DMARC policy to subdomains automatically. Either:

- Set `sp=` in DMARC (subdomain policy) to specify
- Set explicit DMARC records on `mail.example.com`, `notifications.example.com`, etc.

For subdomains you never send from, `v=DMARC1; p=reject;` keeps attackers from spoofing them.

**Apex CNAME problem.** Some DNS hosts allow CNAME at the apex (`example.com`) via flattening. Most don't. If you can't put TXT at the apex, your DNS host is wrong for email.

**Forwarders break SPF.** When your user has set up auto-forward in their inbox, the forwarded mail comes from a different IP — your SPF won't authorize it. DKIM still passes because the signature travels with the message. This is why DKIM is more reliable than SPF for delivery-quality scoring.

**Mailing lists break DKIM.** Lists often rewrite the From header or modify the body, breaking the signature. ARC was designed to preserve auth state across hops; receivers that honor ARC can still trust the original auth result. If you operate or rely on mailing lists, look into ARC.

**Cold-start a new ESP.** New IP / domain pairs have no reputation. Warm up by ramping volume gradually over 2–4 weeks. Sudden bulk from a new domain → straight to spam.

**Multiple SPF records.** Two `v=spf1` records is the most common configuration error in the wild. Merge into one.

**Forgotten test/staging subdomains.** A forgotten record for `staging.example.com` pointing to an old IP, with no DMARC, is a beautiful spoofing target. Audit all sending subdomains.

## Verification commands

```bash
DOMAIN=example.com

dig +short TXT $DOMAIN | grep 'v=spf1'
dig +short TXT _dmarc.$DOMAIN
dig +short TXT default._domainkey.$DOMAIN    # adjust selector
dig +short TXT mailgun._domainkey.$DOMAIN
dig +short TXT _mta-sts.$DOMAIN
dig +short TXT _smtp._tls.$DOMAIN

# End-to-end test — send mail to your-test@gmail.com, then in Gmail → Show original
# Check "Authentication-Results" header for:
#   spf=pass, dkim=pass, dmarc=pass
```

## Inbound — accept what you should, reject what you should

Most of this skill is about outbound, but a quick note on inbound:

- **Set up DMARC reporting on inbound too** — if you receive mail at `dmarc-reports@example.com`, the reports themselves are inbound mail and need a place to land
- **Reject mail with failing DKIM/SPF/DMARC at your own MX** — most receivers (Gmail, Outlook, hosted ESPs) do this for you
- **Phishing of your own staff** — separate skill / training; the technical layer here just makes it harder for attackers to spoof your domain

## Checklist

For a fully-authenticated sending domain:

- [ ] One SPF record at apex, all senders enumerated, `-all` (or `~all` as interim)
- [ ] SPF DNS lookup count under 10
- [ ] DKIM key per ESP, 2048-bit, correct selector in DNS
- [ ] DMARC record exists with `rua=` for aggregate reports
- [ ] DMARC reports are flowing into a parser (Postmark, dmarcian, parsedmarc)
- [ ] DMARC policy at `p=quarantine` or `p=reject` (not stuck at `p=none` forever)
- [ ] Subdomains have explicit DMARC (or `sp=` on apex)
- [ ] Non-sending domains have `v=DMARC1; p=reject; sp=reject;` to prevent spoofing
- [ ] MTA-STS configured, mode enforce
- [ ] TLS-RPT pointed at a real mailbox
- [ ] Test mail to Gmail shows `dkim=pass spf=pass dmarc=pass`
- [ ] Unused old DKIM selectors removed
- [ ] Audit of all sending subdomains, including forgotten staging/test

## What this skill will not do

- Help send spam, phishing, or mail from domains you do not own
- Recommend staying at `p=none` indefinitely once monitoring is established
- Replace ESP-specific deliverability guidance (Mailgun / SendGrid / Postmark have product-specific advice on top of this)
