---
name: amazon-ses-email
description: >
  Full skill for setting up Amazon SES email for the ndestates-io domain (sending + receiving). Non-Microsoft (AWS only). Integrated with Laravel mail config, DO hosting (droplet/App Platform), drift avoidance (project-drift-guardian + schema checks), security (least-privilege IAM, secrets), and billing flows. Use for initial domain setup, DNS records (DKIM/SPF/DMARC/MX), IAM user/keys or role, Laravel .env updates, testing send/receive, inbound processing (e.g. support emails or incoming signed docs), and troubleshooting. Enforces no-drift via cache + guardian. Always run from host for AWS CLI/doctl if needed.
argument-hint: 'Task (e.g. "setup SES for ndestates-io.com domain with inbound", "configure Laravel to send via SES", "add receipt rule for receiving", "verify DKIM and test email")'
user-invocable: true
disable-model-invocation: false
---

# Amazon SES Email Setup for ndestates-io Domain (Send + Receive)

**Goal for ndestates-io:** Reliable, non-Microsoft email (sending transactional + receiving at the domain) using Amazon SES. Tied to the ndestates-io domain (e.g. @ndestates-io.com or ndestates.com). Supports the platform's needs: admin notifications, signer emails (magic links), support tickets, and inbound processing. Billing docs via separate PayPal integration (see .github/skills/paypal-billing-integration/SKILL.md skill). Integrated with existing DO hosting, CI, drift prevention, and security.

**Core mandate:** Setup is infrastructure (Stage 6 agent slot): cache-backed spec (DNS records from cache, expected deliverability), drift-gated (project-drift-guardian before/after DNS/code changes), security-first (IAM least-privilege, no secrets in code), observable (tests + logs), and repeatable via one-liners + Laravel updates. Never ad-hoc. Use DDEV for local testing (mailpit), host for AWS CLI.

This skill is self-contained, references ndestates-io skills (load-project-cache-first, cache-efficient, project-drift-guardian, digitalocean-app-platform-docr-deploy, git-workflow-guardrails, security-audit-agent, eval/maintenance-task), and provides AWS CLI one-liners, DNS templates, Laravel config, inbound handling examples (SNS/S3 + webhook or Lambda to app), and verification steps.

## Mandatory Start (cache + context — per all ndestates-io skills)
1. `.github/prompts/load-project-cache-first.prompt.md` (or .github/skills/cache-efficient/SKILL.md) — load INDEX, docs/codebase/ (ARCHITECTURE for email flows, INTEGRATIONS/STACK for AWS/DO, CONCERNS for email risks), TODO-2026-06-14.md, prior evals.
2. `.github/skills/project-drift-guardian/SKILL.md` (or drift-check) — run scope/branch alignment on email config/DNS/code. Non-negotiable to avoid drift (e.g. DNS mismatches, config drift post-deploy).
3. Cross-load: branch-context-agent, github-expert (for workflows), git-workflow-guardrails (before DNS/code commits), security-audit-agent (IAM/secrets), digitalocean-... (update DO env/secrets), ai-engineering-maturity (track to Stage 6/8 for email infra as agent slot).
4. Confirm current state: git status --short, current DO target, last known email state (from cache/TODO), domain (e.g. ndestates-io.com from context/nick@ndestates.com).

Never proceed without these. Update shared assets (TODO, docs/codebase/INTEGRATIONS.md, drift DB) after.

**Non-Microsoft policy:** Pure AWS (SES, IAM, SNS/S3/Lambda if used). No Microsoft 365/Exchange/Outlook/SendGrid alternatives. Use AWS for everything.

## SES Overview for ndestates-io Domain
- **Sending:** Transactional emails (Laravel mailer: magic links, notifications, receipts via PayPal integration).
- **Receiving:** Domain emails (e.g. support@, inbound signed docs or forms) via SES inbound (MX to SES, receipt rules to S3 + SNS/Lambda that posts to Laravel webhook or queues for processing). Ties to ndestates-io flows (e.g. receive completed docs).
- Region: Prefer us-east-1 (or match DO region) for simplicity; sandbox first, then production request.
- Limits: Start in sandbox (send to verified emails), move to production (request review).
- Costs: Pay-per-use (low for transactional); monitor via AWS billing.
- Security: IAM user/role with ses:SendRawEmail etc. (least privilege). Secrets in DO App/Droplet env or Laravel .env (never commit). DKIM for auth. DMARC for anti-spoof.
- Drift avoidance: DNS records as code (docs or .env), config in repo, pre/post checks via guardian + tests. Post-deploy: send test + receive test + eval.

**References (load first):** docs/codebase/ARCHITECTURE.md (email in flows), INTEGRATIONS.md (AWS), CONCERNS.md (email deliverability risks), .github/prompts/amazon-ses-setup.md (detailed prompt), digitalocean skill (secrets/DNS in DO), prod-db-maintenance patterns (one-liner + eval).

## Setup Procedures (one-liners + Laravel + verification)
Always: Use AWS CLI (aws configure with limited creds). For prod: run on host with doctl/AWS creds. Local: DDEV + mailpit for testing (override .env to ses or log).

### 1. Verify Domain (Sending + Receiving)
```bash
# From host (with AWS creds; region us-east-1 example)
aws ses verify-domain-identity --domain ndestates-io.com --region us-east-1
aws ses verify-domain-dkim --domain ndestates-io.com --region us-east-1
# Note the VerificationToken and DKIM tokens (CNAMEs). Add to DNS (via DO or registrar).
# For receiving: also verify for inbound.
aws ses verify-domain-identity --domain ndestates-io.com --region us-east-1  # same for MX
```

**DNS Records:** Use the dedicated `.github/skills/aws-route53-dns/SKILL.md` skill (recommended) to create the hosted zone, delegate nameservers, and apply the records via Route 53 (programmatic UPSERT). This replaces manual adds via DO DNS or registrar.

Required records (tokens come from the SES verify steps above):
- Verification: TXT at _amazonses.ndestates-io.com with the VerificationToken value.
- DKIM: 3x CNAME (selector1/2/3._domainkey.ndestates-io.com -> the dkim.amazonses.com values).
- SPF: TXT at apex "v=spf1 include:amazonses.com ~all" (merge if existing SPF TXT present).
- DMARC: TXT at _dmarc.ndestates-io.com "v=DMARC1; p=quarantine; rua=mailto:dmarc@ndestates-io.com".
- MX (for receiving): 10 inbound-smtp.us-east-1.amazonaws.com (or your region).

See `.github/skills.github/skills/aws-route53-dns/SKILL.md/SKILL.md` and its prompt for exact `aws route53 change-resource-record-sets` batches (with JSON examples) + delegation + dig verification. Always run `.github/skills/project-drift-guardian/SKILL.md` before/after DNS operations.

### 2. IAM for SES (least privilege)
```bash
# Create user (or role for EC2/App)
aws iam create-user --user-name ndestates-io-ses
aws iam create-access-key --user-name ndestates-io-ses  # note ID/secret for .env or DO secrets
# Attach policy (minimal)
aws iam put-user-policy --user-name ndestates-io-ses --policy-name SESSendReceive --policy-document '{
  "Version": "2012-10-17",
  "Statement": [
    {"Effect": "Allow", "Action": ["ses:SendRawEmail", "ses:SendEmail"], "Resource": "*"},
    {"Effect": "Allow", "Action": ["ses:CreateReceiptRuleSet", "ses:DescribeReceiptRuleSet"], "Resource": "*"}
  ]
}'
```

Store keys in DO (App Platform env vars or droplet .env via secrets manager). Never in code/repo. Trigger security-audit-agent after.

### 3. Laravel Config (Sending + Receiving)
In .env (DDEV for local override; prod via DO secrets):
```
MAIL_MAILER=ses
MAIL_HOST=email-smtp.us-east-1.amazonaws.com
MAIL_PORT=587
MAIL_USERNAME=your-ses-smtp-user  # or use IAM role
MAIL_PASSWORD=...
MAIL_ENCRYPTION=tls
MAIL_FROM_ADDRESS=noreply@ndestates-io.com
MAIL_FROM_NAME="${APP_NAME}"

# SES specific (or rely on IAM)
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_DEFAULT_REGION=us-east-1
```

Update config/mail.php (ses driver) and config/services.php (ses).

For receiving: Add webhook or queue listener. E.g., SNS to S3, then Laravel job polls S3 or use SES inbound webhook (if set via receipt rule to HTTPS).

Example receipt rule (CLI):
```bash
aws ses create-receipt-rule-set --rule-set-name ndestates-io-inbound
aws ses create-receipt-rule --rule-set-name ndestates-io-inbound --rule '{
  "Name": "store-to-s3",
  "Enabled": true,
  "Recipients": ["@ndestates-io.com"],
  "Actions": [
    {"S3Action": {"BucketName": "ndestates-io-emails", "ObjectKeyPrefix": "inbound/"}}
  ]
}'
```
Then Laravel: Use AWS SDK to process S3 objects on webhook or cron (parse email, store in DB or trigger Filament notification).

Test send:
```bash
# Laravel
ddev exec php artisan tinker
Mail::raw('Test from ndestates-io', function($m){ $m->to('test@example.com')->subject('SES Test'); });
```

Test receive: Send email to user@ndestates-io.com (after MX), check S3 or app log.

### 4. Move out of Sandbox + Production
```bash
aws ses get-send-quota --region us-east-1  # check
# Request production access via AWS console (or CLI if available). Provide use case (ndestates-io transactional).
aws ses update-account-sending-enabled --enabled  # once approved
```

### 5. Monitoring & Drift
- CloudWatch for bounces/complaints.
- After setup: .github/skills/eval/maintenance-task/SKILL.md (define "clean" = successful test send/receive, no bounces in logs).
- Pre/post any DNS/deploy: .github/skills/project-drift-guardian/SKILL.md --scope "email domain + SES config".
- Update docs/codebase/INTEGRATIONS.md with records.
- In CI (via digitalocean skill): test email in staging.

**One-liner full setup (cache-verified):**
```bash
# Host with AWS creds
aws ses verify-domain-identity --domain YOURDOMAIN --region us-east-1
# ... add DNS from output ...
aws ses verify-domain-dkim ...
# Then Laravel .env + test
ddev exec php artisan config:clear
# Verify receive: check S3 or app endpoint
```

**Security & Governance (Stage 4 — mandatory):**
- IAM minimal (only SES actions). No root keys.
- Secrets: DO env or AWS Secrets Manager (inject at runtime). Full checklist on changes (MCP threats for new prompts/scripts).
- Receiving: Validate inbound (SPF/DKIM in app), rate limit, no PII in logs.
- Cost: Set CloudWatch alarms. Use in DO skill for env.

**Cross-references (max cache):**
- .github/prompts/load-project-cache-first.prompt.md + .github/skills/project-drift-guardian/SKILL.md + .github/skills/digitalocean-app-platform-docr-deploy/SKILL.md (hosting + secrets).
- .github/skills/aws-route53-dns/SKILL.md (preferred for all DNS record application + nameserver delegation — run after SES verify steps).
- /security-audit-agent (IAM/secrets).
- /eval/maintenance-task (post-setup verification).
- docs/codebase/ (email in e-sign flows).
- .github/prompts/amazon-ses-setup.md (for detailed AI-assisted setup).
- copilot-instructions (DDEV local, no destructive, auth).

**Advancement (AI Engineering Maturity):** Turns email into Stage 6 infra (agent slot for setup/verification, shared context in cache, evals as gates). Future: scheduled drift checks or Lambda for inbound processing.

Invoke for any email task: `.github/skills/amazon-ses-email/SKILL.md "setup receiving for support@ndestates-io.com"`. After: update TODO + cache. Re-run security checklist.

This makes SES native, drift-free, and integrated for ndestates-io (non-Microsoft, PayPal for billing separate). Cite https://upsun.com/blog/8-stages-ai-engineering-maturity/ when using.

(Adapted from patterns in digitalocean/prod-db-maintenance.github/skills/project-drift-guardian/SKILL.md skills across projects, made specific to ndestates-io + AWS SES + receiving.)