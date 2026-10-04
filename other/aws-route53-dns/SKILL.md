---
name: aws-route53-dns
description: >
  Full skill for AWS Route 53 DNS management for ndestates-io domains (hosted zones, nameserver delegation, record management). Specializes in email setup: domain verification TXT, DKIM CNAMEs, SPF, DMARC, MX for Amazon SES send + receive. Also handles general domain records (A, CNAME, etc.). Non-Microsoft (pure AWS). Complements /amazon-ses-email by automating DNS record application (no more manual DO DNS or registrar edits). Integrated with project-drift-guardian (DNS as code, pre/post checks), digitalocean (delegation or current registrar), security (least-privilege IAM), and evals. Use for initial domain bootstrap, SES email DNS, verification, ongoing mail-related records, and app subdomains. Enforces no-drift via cache + guardian. Always run from host with AWS CLI.
argument-hint: 'Task (e.g. "create hosted zone and apply full SES email records for ndestates-io.com", "upsert DKIM SPF DMARC MX verification records via Route53", "delegate nameservers to Route53", "verify propagation and SES domain status")'
user-invocable: true
disable-model-invocation: false
---

# AWS Route 53 DNS Setup for ndestates-io Domains (Domains + Email Records + Verification)

**Goal for ndestates-io:** Authoritative, reliable DNS via AWS Route 53 for the primary domain (e.g. ndestates-io.com or ndestates.com). Focus on email deliverability and authentication for Amazon SES (sending magic links/notifications to signers + receiving support/inbound). This skill provides the DNS half of SES setup — programmatic record management instead of manual edits in DO DNS or registrar. Non-Microsoft (AWS Route53 + SES only). Supports domain apex + subdomains, nameserver delegation, and verification.

**Core mandate:** DNS is critical infrastructure (Stage 6 agent slot). Cache-backed (current zone/records from prior scans), drift-gated (every change via /project-drift-guardian — DNS mismatches cause email blackholing or spoofing failures), security-first (IAM least-privilege, no broad zone access), observable (dig checks + propagation), repeatable via AWS CLI one-liners + JSON change batches. Never manual edits. Treat record sets as code. Use host for `aws route53`; cross with DDEV only for app-side verification.

This skill is self-contained, references ndestates-io skills (load-project-cache-first, cache-efficient, project-drift-guardian, amazon-ses-email, digitalocean-app-platform-docr-deploy, git-workflow-guardrails, security-audit-agent, eval/maintenance-task), and provides precise `aws route53` commands, change-batch examples for SES email records, delegation steps, verification, and integration points.

## Mandatory Start (cache + context — per all ndestates-io skills)
1. `/load-project-cache-first` (or /cache-efficient) — load INDEX, docs/codebase/ (INTEGRATIONS for current DNS state, ARCHITECTURE/STACK for email flows, CONCERNS for DNS drift risks), TODO-2026-06-14.md, prior evals.
2. `/project-drift-guardian` (or drift-check) — run with scope including "DNS" or "Route53 email records" or "domain delegation". Non-negotiable: DNS changes are high-risk for drift (propagation, NS delegation, record mismatches with SES).
3. Cross-load: amazon-ses-email (run SES verify first to obtain tokens, then this skill for DNS), branch-context-agent, github-expert, git-workflow-guardrails (before committing any JSON batches or notes), security-audit-agent (IAM), digitalocean-app-platform-docr-deploy (current domain registrar/DNS or delegation from DO), ai-engineering-maturity (Stage 6 for DNS infra).
4. Confirm current state: git status, current domain(s), existing hosted zone ID (if any), last known SES verification status, registrar (DO or other), AWS region (prefer us-east-1).

Never proceed without these. After changes: update docs/codebase/INTEGRATIONS.md, CONCERNS if new risks, drift requirements DB, and run /eval-maintenance-task.

**Non-Microsoft policy:** Pure AWS (Route 53 for all DNS + SES for email). No Microsoft DNS, Azure DNS, Office 365 DNS, or third-party like Cloudflare if it conflicts with "non-MS AWS" direction. Use Route 53 exclusively for ndestates-io domains.

## Route 53 Overview for ndestates-io + Email
- **Hosted Zone:** Public hosted zone for the domain (or subdomain). Route 53 becomes the authoritative nameserver.
- **Nameserver Delegation:** Get the 4 NS records from the zone and set them at the domain registrar (or DO nameservers panel if currently using DO DNS).
- **Email Records (tied to /amazon-ses-email):**
  - Domain verification TXT (from `aws ses verify-domain-identity`).
  - DKIM: 3 CNAME records (from `aws ses verify-domain-dkim`).
  - SPF: TXT at apex (or include in existing SPF).
  - DMARC: TXT at _dmarc.
  - MX: for inbound receiving (points to SES inbound-smtp).
- **Other common:** A/AAAA or CNAME for app (e.g. app.ndestates-io.com), CAA for security, custom MAIL FROM subdomain if used.
- **Verification:** After upsert, poll SES `get-identity-verification-attributes`, use `dig` +short to confirm propagation (can take minutes to hours for NS change).
- **Drift risks:** NS delegation at registrar, record values from SES tokens, TTLs, apex vs www handling. Guardian + record exports as code mitigate.
- **Costs:** Route 53 hosted zones + queries (low for ndestates-io transactional use). Monitor in AWS billing.

**References (load first):** docs/codebase/INTEGRATIONS.md (DNS/Email section), CONCERNS.md (SES DNS drift + new Route53 section), .grok/prompts/aws-route53-dns-setup.md (this prompt), amazon-ses-email skill (for token generation + Laravel side), digitalocean skill (registrar/NS steps), project-drift-guardian (DNS checks).

## Setup Procedures (one-liners + change batches + verification)
Always: Authenticate with limited AWS creds (`aws configure` or env). Prefer us-east-1. Run on host (not inside DDEV containers for AWS CLI). After SES commands produce tokens, immediately apply via this skill.

### 1. Create or Identify Hosted Zone
```bash
# List existing (note the Id, e.g. /hostedzone/Z0123456789ABC)
aws route53 list-hosted-zones --region us-east-1

# Create new public zone (caller-reference must be unique)
aws route53 create-hosted-zone \
  --name ndestates-io.com \
  --caller-reference "$(date +%s)-ndestates-io" \
  --region us-east-1
# Capture the Id (Z...) and the 4 NameServers from output.DelegationSet.NameServers
```

Store the HostedZoneId (e.g. ZXXXXXXXXXXXXX) for all future commands. Update cache/docs with it.

### 2. Delegate Nameservers (Critical for live domain)
- From the create output (or `aws route53 get-hosted-zone --id Z...`), copy the 4 NS values.
- At your registrar (DO Domains, or wherever ndestates-io.com is registered):
  - Change nameservers from current (DO or registrar defaults) to the four Route53 NS values.
  - Remove any old DNS records at the old provider after delegation succeeds (to avoid split-brain).
- Propagation for NS change can take 24-48h (usually faster). Monitor with:
```bash
dig NS ndestates-io.com +short
dig +trace ndestates-io.com   # to confirm authority
```

Use /digitalocean-app-platform-docr-deploy for DO-specific registrar instructions if applicable. Always run guardian before registrar changes.

### 3. Apply SES Email DNS Records (Verification, DKIM, SPF, DMARC, MX)
**Prerequisite:** Run the SES verification first (see /amazon-ses-email):
```bash
aws ses verify-domain-identity --domain ndestates-io.com --region us-east-1
aws ses verify-domain-dkim --domain ndestates-io.com --region us-east-1
# Note: VerificationToken and the three DkimTokens
```

Create a change batch JSON (store in repo under e.g. infra/dns/ or .grok/ for reference — treat as code):

Example `changes-ses-email.json` (adapt tokens):
```json
{
  "Comment": "ndestates-io SES email setup (verification + DKIM + SPF + DMARC + MX) - $(date)",
  "Changes": [
    {
      "Action": "UPSERT",
      "ResourceRecordSet": {
        "Name": "_amazonses.ndestates-io.com",
        "Type": "TXT",
        "TTL": 300,
        "ResourceRecords": [{"Value": "\"<VerificationToken-from-SES>\""}]
      }
    },
    {
      "Action": "UPSERT",
      "ResourceRecordSet": {
        "Name": "selector1._domainkey.ndestates-io.com",
        "Type": "CNAME",
        "TTL": 300,
        "ResourceRecords": [{"Value": "<token1>.dkim.amazonses.com"}]
      }
    },
    {
      "Action": "UPSERT",
      "ResourceRecordSet": {
        "Name": "selector2._domainkey.ndestates-io.com",
        "Type": "CNAME",
        "TTL": 300,
        "ResourceRecords": [{"Value": "<token2>.dkim.amazonses.com"}]
      }
    },
    {
      "Action": "UPSERT",
      "ResourceRecordSet": {
        "Name": "selector3._domainkey.ndestates-io.com",
        "Type": "CNAME",
        "TTL": 300,
        "ResourceRecords": [{"Value": "<token3>.dkim.amazonses.com"}]
      }
    },
    {
      "Action": "UPSERT",
      "ResourceRecordSet": {
        "Name": "ndestates-io.com",
        "Type": "TXT",
        "TTL": 300,
        "ResourceRecords": [{"Value": "\"v=spf1 include:amazonses.com ~all\""}]
      }
    },
    {
      "Action": "UPSERT",
      "ResourceRecordSet": {
        "Name": "_dmarc.ndestates-io.com",
        "Type": "TXT",
        "TTL": 300,
        "ResourceRecords": [{"Value": "\"v=DMARC1; p=quarantine; rua=mailto:dmarc@ndestates-io.com\""}]
      }
    },
    {
      "Action": "UPSERT",
      "ResourceRecordSet": {
        "Name": "ndestates-io.com",
        "Type": "MX",
        "TTL": 300,
        "ResourceRecords": [{"Value": "10 inbound-smtp.us-east-1.amazonaws.com"}]
      }
    }
  ]
}
```

Apply it:
```bash
aws route53 change-resource-record-sets \
  --hosted-zone-id Z0123456789ABC \
  --change-batch file://changes-ses-email.json \
  --region us-east-1
```

**Note on SPF:** If an apex TXT SPF already exists (from prior provider), merge the include:amazonses.com value instead of creating a second TXT at root (Route53 allows only one TXT per name for SPF best practice).

### 4. Verify Records + SES Status
```bash
# Local verification (after short propagation)
dig TXT _amazonses.ndestates-io.com +short
dig CNAME selector1._domainkey.ndestates-io.com +short
dig TXT _dmarc.ndestates-io.com +short
dig MX ndestates-io.com +short

# SES side
aws ses get-identity-verification-attributes --identities ndestates-io.com --region us-east-1
aws ses get-identity-dkim-attributes --identities ndestates-io.com --region us-east-1
```

Once SES shows "Success" for verification and DKIM, proceed to Laravel config and testing (see /amazon-ses-email).

### 5. IAM Least-Privilege for Route53 (DNS only)
```bash
aws iam create-user --user-name ndestates-io-route53
aws iam create-access-key --user-name ndestates-io-route53

# Minimal policy (attach via put-user-policy or console). Scope to specific zone when possible.
aws iam put-user-policy --user-name ndestates-io-route53 --policy-name Route53DnsManage --policy-document '{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "route53:ListHostedZones",
        "route53:GetHostedZone",
        "route53:ListResourceRecordSets",
        "route53:ChangeResourceRecordSets"
      ],
      "Resource": "arn:aws:route53:::hostedzone/Z0123456789ABC"
    }
  ]
}'
```

Store keys in DO secrets (never commit). Prefer IAM roles for EC2/App Platform where possible. Run security-audit-agent after.

### 6. Additional / Ongoing Records + Cleanup
- App subdomains, www redirect CNAMEs, etc.: similar UPSERT batches.
- Custom MAIL FROM (if used): additional MX + TXT for feedback.
- Cleanup old records (Action: DELETE) after successful delegation + verification.
- Export current zone for "as code" reference:
```bash
aws route53 list-resource-record-sets --hosted-zone-id Z... --region us-east-1 > infra/dns/ndestates-io.com-current.json
```

### 7. Monitoring, Drift & Production
- After any change: `/project-drift-guardian --scope "Route53 DNS + SES email records"` + `/eval-maintenance-task --task=route53-dns`.
- Update INTEGRATIONS.md with zone ID, record summary, NS values (sanitized).
- In CI/digitalocean flows: optional dry-run or validation step using the exported JSON.
- Propagation + email tests: send test, check DMARC reports, inbound to support@.

**One-liner full flow (cache-verified, after SES tokens obtained):**
```bash
# 1. Ensure zone + delegation (one-time)
aws route53 create-hosted-zone --name ndestates-io.com ...
# Set NS at registrar (manual or via registrar API)

# 2. Apply email records (idempotent UPSERT)
aws route53 change-resource-record-sets --hosted-zone-id Z... --change-batch file://changes-ses-email.json

# 3. Verify
dig ... && aws ses get-identity-verification-attributes ...
ddev exec php artisan config:clear   # once Laravel side updated
# Then full SES tests + guardian + eval
```

**Security & Governance (Stage 4 — mandatory):**
- IAM scoped to the exact hosted zone ARN (never *).
- Change batches reviewed (store JSON in repo).
- Registrar NS delegation is a high-privilege external change — double-check, use guardian, document.
- No PII or secrets in DNS records (DMARC rua is fine; avoid exposing internal hosts).
- Full checklist on new prompts/scripts or IAM changes.
- Cost + query logging via CloudWatch/Route53 resolver if expanded.

**Cross-references (max cache):**
- /load-project-cache-first + /project-drift-guardian (mandatory for every DNS op) + /amazon-ses-email (token source + Laravel + receiving).
- /digitalocean-app-platform-docr-deploy (registrar/NS delegation + DO secrets for Route53 keys).
- /security-audit-agent (IAM + delegation).
- /eval/maintenance-task (post DNS + email verification).
- docs/codebase/ (email + DNS in integrations/concerns).
- .grok/prompts/aws-route53-dns-setup.md
- copilot-instructions (DDEV local, branch rules, security on external changes).

**Advancement (AI Engineering Maturity):** Makes DNS a first-class, invocable, cache-backed, guardrailed part of the platform (Stage 6). Eliminates ad-hoc registrar edits. Future: scripted delegation (if registrar API), zone versioning in repo, automated drift detection on record sets vs expected JSON, or Route53 profiles.

Invoke for any DNS task: `/aws-route53-dns "apply full SES verification + DKIM + MX records for ndestates-io.com using Route53"`. After: update TODO + cache + drift DB. Re-run security checklist.

This completes reliable AWS-native (non-MS) domain + email DNS for ndestates-io when combined with /amazon-ses-email. Cite https://upsun.com/blog/8-stages-ai-engineering-maturity/ when using.

(Adapted from patterns in amazon-ses-email, project-drift-guardian, digitalocean skills; made specific to ndestates-io email flows + Route 53 automation.)
