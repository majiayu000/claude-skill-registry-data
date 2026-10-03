---
name: codebase-audit
description: Audit an inherited or unfamiliar codebase systematically rather than ad-hoc. Covers scope discipline, day-0 triage, SAST and SCA tool recipes (semgrep, CodeQL, gitleaks, trivy), OWASP Top 10 mapped to grep patterns, auth-surface walkthrough, and writing reports that drive remediation. Invoke when inheriting a codebase, accepting an audit engagement, or reviewing AI-generated code before shipping.
---

# Codebase Audit — the Inherited-Code Playbook

This is the skill that **binds the others together**. Most engagement value from a security review comes from the auditor's process, not from any single check. A junior auditor with a great tool produces a noisy report; a senior auditor with `grep` and a methodology finds the things that matter.

This skill is the methodology. It walks the audit from "I just got SSH access / a repo URL" through to "here's the prioritized report with owners and deadlines." It cross-links into every hardening skill in this repo as the deep-dive material per finding class.

## When to invoke

- **Inheriting a codebase** — new job, new client, open-source fork, acquisition target
- **"Audit my app"** engagement — freelancer / consultancy work
- **Onboarding to a project** — you'll touch the code soon and need to know what's safe to assume
- **AI-generated codebase review** — before shipping a Claude/Copilot/Cursor-written app
- **Periodic re-audit** — annual review of a system you already know

## Step 0 — Scope before substance

The most common reason audits fail is the auditor trying to look at everything. Scope discipline is the difference between a useful report and a 300-page document nobody reads.

Before starting, write down:

- **Why this audit exists** — diligence? incident? compliance? onboarding?
- **Who reads the report** — engineers? CTO? legal? buyer?
- **Time budget** — 4 hours? 4 days? 4 weeks? This determines depth.
- **What's in scope** — which repos / services / domains / accounts. Get it confirmed in writing.
- **What's explicitly out of scope** — third-party SaaS, customer data, anything the client did not authorize. Get this confirmed too.
- **Deliverable shape** — report? findings spreadsheet? remediation PRs? presentation?

Without these five answers, do not start. Time spent here saves three times that later.

## Step 1 — Day-0 triage (the first 30 minutes)

The goal of the first 30 minutes is **orientation, not findings**. Build a mental model of the system. Findings come later.

```bash
# What language(s), what framework(s)?
cd <repo>
ls -la
cat README.md
find . -name 'package.json' -not -path '*/node_modules/*' | head -5
find . -name 'requirements*.txt' -o -name 'pyproject.toml' -o -name 'Gemfile' -o -name 'go.mod' -o -name 'Cargo.toml' 2>/dev/null
```

Answer in writing (in your notes, not yet the report):

1. **Stack** — language, framework, DB, cache, queue, deploy target
2. **Entry points** — what URLs / endpoints does this expose? Background workers? CLIs?
3. **Auth story** — how do users log in, what session mechanism, are admins separate?
4. **Data** — what's stored, where (Postgres, Mongo, S3, files on disk, third parties)?
5. **Secrets** — where are they (env, vault, hardcoded — yes, look)?
6. **Deploy** — how does code get to production? Who can deploy? CI/CD or manual?
7. **Blast radius** — if this whole system were compromised tomorrow, what's the worst that happens? Customer data leak? Money lost? Operations halted? Reputation only?

If you cannot answer one of these from a 30-minute look, that's already a finding.

## Step 2 — Inventory the surface

Now enumerate everything that matters.

### Repositories and branches

```bash
git log --oneline | head -20
git log --all --format='%aN' | sort -u           # who has committed
git tag                                          # release cadence
git remote -v                                    # where is it published
ls -la .github/                                  # workflows, codeowners
```

### Routes / endpoints

```bash
# Next.js — App Router routes
find app -name 'route.ts' -o -name 'route.js' -o -name 'page.tsx' 2>/dev/null

# Next.js — Pages Router API routes
find pages/api 2>/dev/null

# Express
grep -rE "app\.(get|post|put|delete|patch|use)\(" src 2>/dev/null
grep -rE "router\.(get|post|put|delete|patch)\(" src 2>/dev/null

# Server Actions (Next.js)
grep -rln "'use server'" app 2>/dev/null

# WordPress — REST endpoints
grep -rE "register_rest_route" wp-content/ 2>/dev/null

# OpenAPI / Swagger if present
find . \( -name 'openapi.yaml' -o -name 'openapi.json' -o -name 'swagger.*' \) 2>/dev/null
```

Build a list of every entry point. For each, you'll later answer "is auth checked? is input validated?"

### Dependencies

```bash
cat package.json | jq '.dependencies, .devDependencies'
wc -l package-lock.json                          # rough sense of transitive surface
find . -name 'node_modules' -prune -o -name 'package.json' -print | wc -l
```

### Infrastructure-as-code

```bash
find . \( -name '*.tf' -o -name 'Dockerfile*' -o -name 'docker-compose*' -o -name 'k8s*.yaml' \) -not -path '*/node_modules/*' 2>/dev/null
ls .github/workflows/ 2>/dev/null
```

### Where data lives

```bash
# Database connection strings — environment variables only, never hardcoded
grep -rE 'DATABASE_URL|MONGO_URL|REDIS_URL|postgres://|mongodb://' --include='*.{js,ts,py,rb,go,env,yml,yaml}' . 2>/dev/null | grep -v node_modules

# File storage paths
grep -rE 'multer|formidable|busboy|fs\.write|writeFile|S3|R2|Bucket' --include='*.{js,ts}' . 2>/dev/null | grep -v node_modules | head -20
```

## Step 3 — Tool-assisted scanning

Run automated tools early, parse their output later. The tools give you a haystack of candidates; the manual review (Step 4–6) figures out which are real.

### SAST — static code analysis

```bash
# Semgrep — fast, language-aware, good default rules
brew install semgrep
semgrep --config=auto --json -o /tmp/semgrep.json . 2>/dev/null
semgrep --config=auto . 2>&1 | grep -E '(WARNING|ERROR|^Findings:|^\s*severity:)' | head -30

# More targeted — security-focused rules only
semgrep --config=p/security-audit --config=p/owasp-top-ten .

# For JavaScript/TypeScript specifically
semgrep --config=p/javascript --config=p/typescript .

# Language-specific
semgrep --config=p/python   # Python — bandit-equivalent rules
semgrep --config=p/php      # PHP including WordPress patterns
```

### Secret scanning

```bash
# gitleaks — across history too
brew install gitleaks
gitleaks detect --source . --report-format json --report-path /tmp/gitleaks.json
gitleaks detect --source . --log-opts="--all"   # scan all branches + history

# trufflehog — different ruleset, often catches things gitleaks misses
trufflehog git file://. --json --only-verified > /tmp/trufflehog.json
```

### Dependency / SCA

```bash
# npm
npm audit --omit=dev --audit-level=high

# Better — Socket for behavior-level signals
# (https://socket.dev — runs in CI on PRs)

# OSV-Scanner — broader than npm audit
osv-scanner --recursive .

# pip-audit for Python
pip-audit --strict -r requirements.txt
```

### Container scanning

```bash
# Trivy — image scanning, IaC scanning, secret scanning
trivy fs --severity HIGH,CRITICAL .
trivy image myapp:latest --severity HIGH,CRITICAL
trivy config .   # Dockerfile + k8s + terraform misconfigs
```

### GitHub CodeQL (if hosted on GitHub)

Enable in repo Settings → Code security → CodeQL analysis. It's free for public repos and worth its quotas for private. The results land in the Security tab; treat them as candidates, not verdicts.

### What each tool catches, what it misses

| Tool | Catches | Misses |
|---|---|---|
| Semgrep | Pattern-shaped vulns (SQL string-concat, unsafe deserialization, missing CSRF) | Logic bugs, broken access control, business-logic issues |
| Gitleaks | Token-shape secrets in code/history | Custom secret formats, encrypted-at-rest values |
| npm audit | Known CVEs against pinned versions | Malicious-by-design packages, unreported issues |
| Socket | Behavior changes (sudden network calls, install scripts) | Pre-existing issues in established packages |
| Trivy | Image CVEs, misconfigured IaC, secrets in images | Application logic, runtime behavior |
| CodeQL | Dataflow-level vulns (taint analysis) | Issues outside its rule set, recent CVEs not yet ruled |

**No tool finds broken access control.** That is the single most common high-severity finding in real audits, and it requires manual review. Plan time accordingly.

## Step 4 — Manual review — Auth surface

Auth surface is where the highest-impact findings cluster. Walk every entry point and answer:

1. **Is auth checked?** Server-side, in the handler itself — not just at middleware.
2. **Is authorization checked?** Auth says "you are X"; authz says "X may do this." They are not the same check.
3. **Are object IDs resolved against the requester?** `GET /invoices/:id` must verify the invoice belongs to the requesting user.
4. **What happens on auth failure?** Generic error (good) or detailed enumeration ("user not found" vs "wrong password" — bad)?
5. **Where are session cookies issued?** `HttpOnly`, `Secure`, `SameSite=Lax`?
6. **Password reset and email change flows?** Single-use token, expiring, invalidates sessions on success?

```bash
# Find every route + look for the auth check
grep -rEn "app\.(get|post|put|delete|patch)\(['\"]" src | head -40
# Then for each, check the handler for: session lookup, role check, owner check
```

See [`auth-hardening`](../auth-hardening/SKILL.md) for the deep dive and the checklist.

## Step 5 — Manual review — Input handling

Every place untrusted input enters the system:

```bash
# SQL — anything that concatenates user input
grep -rEn "(\\.query\\(|\\.execute\\(|raw\\().*\\+.*req\\." --include='*.{js,ts,py}' . | head
grep -rEn 'f"SELECT.*\\{|f"INSERT.*\\{' --include='*.py' .

# HTML rendering — anything that dangerouslySetInnerHTML, v-html, .innerHTML
grep -rEn 'dangerouslySetInnerHTML|v-html|\\.innerHTML\\s*=' --include='*.{tsx,jsx,vue,ts,js}' .

# Shell execution
grep -rEn 'child_process|execSync|spawn|popen|os\\.system|subprocess\\.(run|call|Popen)' --include='*.{js,ts,py}' . | head

# Eval and friends
grep -rEn '\\beval\\(|new Function\\(|exec\\(' --include='*.{js,ts,py}' . | head

# File path joining with user input
grep -rEn 'path\\.join.*req\\.|os\\.path\\.join.*request' --include='*.{js,ts,py}' . | head
```

Every hit is a candidate. Read the surrounding code. Most are fine; some are critical.

## Step 6 — OWASP Top 10 mapped to grep recipes

A quick checklist with concrete searches for each Top-10 category (Web Apps, 2021 edition):

**A01 — Broken Access Control** (most common, hardest to grep)

- Read every handler. Does it check the user owns the resource?
- `grep -rEn ":id|:slug" src/routes` — every parameterized route is a candidate

**A02 — Cryptographic Failures**

```bash
grep -rEn 'md5|sha1|DES|crypto\.createCipher\b' --include='*.{js,ts,py}' .   # deprecated/weak
grep -rEn 'http://' --include='*.{js,ts,py,html}' . | grep -v 'w3.org\|example\.com\|localhost'
```

**A03 — Injection**

- See SQL / shell / HTML grep above
- Plus: `grep -rEn 'LDAP|ldap_search' .` if LDAP is in scope
- Plus: NoSQL injection patterns — `grep -rEn '\$where|\$regex' --include='*.{js,ts}' .`

**A04 — Insecure Design** — by inspection, not grep

**A05 — Security Misconfiguration**

```bash
grep -rEn 'NODE_ENV.*development|DEBUG\s*=\s*True|app\.debug\s*=\s*True' --include='*.{js,ts,py}' .
grep -rE 'cors.*\*|Access-Control-Allow-Origin.*\*' --include='*.{js,ts,py}' .
```

**A06 — Vulnerable and Outdated Components** — `npm audit`, `osv-scanner` (Step 3)

**A07 — Identification and Authentication Failures** — auth surface walkthrough (Step 4)

**A08 — Software and Data Integrity Failures**

- Lockfile present?
- Third-party dependencies pinned?
- Deserialization of untrusted data — `grep -rE 'pickle\\.loads|yaml\\.load(\\(|\\s)' .`

**A09 — Security Logging and Monitoring Failures**

- Is there logging at all? See [`log-strategy`](../log-strategy/SKILL.md).
- Are failures logged? Auth events?

**A10 — Server-Side Request Forgery (SSRF)**

```bash
grep -rEn 'fetch\\(.*req\\.|axios.*req\\.|requests\\.(get|post)\\(.*request' --include='*.{js,ts,py}' . | head
```

## Step 7 — Dependency-surface review

See [`dependency-supply-chain`](../dependency-supply-chain/SKILL.md) for the deep workflow. Specifically for audit:

- Is there a lockfile? Is it committed?
- Are direct deps tightly pinned (no caret on critical libs)?
- Any deps with single-digit weekly downloads? Investigate each.
- Any deps with maintainer transferred in the last 90 days?
- Install scripts on transitive deps — enumerate them.
- Has `npm audit --audit-level=high` been run recently? What does it say?

## Step 8 — Infra & deploy review

- Where does code run? VPS, container platform, serverless, Kubernetes?
- Who can deploy? CI service account? Multiple humans?
- Where are production secrets? Env vars at the platform? A secret manager? `.env` on disk?
- Is there a way for an attacker to influence the build? (Pull-request runs that get prod secrets, etc.)
- Are images / artifacts pinned by SHA?
- What's the rollback story?

See [`vps-hardening`](../vps-hardening/SKILL.md), [`docker-container-security`](../docker-container-security/SKILL.md), [`github-actions-security`](../github-actions-security/SKILL.md), [`cloudflare-hardening`](../cloudflare-hardening/SKILL.md), [`backend-architecture`](../backend-architecture/SKILL.md).

## Step 9 — Write the report

The report exists to drive action. Optimize for "can a different engineer fix this in a sprint?"

### Per finding

```
## [CRITICAL] Broken access control on /api/invoices/:id

### Summary
Any authenticated user can read any invoice by ID. No owner check.

### Evidence
- File: src/api/invoices/[id]/route.ts:12
- Reproduction: as user A, fetch /api/invoices/<an id belonging to user B>
  $ curl -H "Cookie: $A_SESSION" https://app.example.com/api/invoices/$B_INVOICE_ID
  → 200 OK with B's data

### Impact
Cross-tenant data exposure. Any logged-in user reads every invoice.

### Remediation
Add owner check in the handler:
  const invoice = await db.invoices.findFirst({ where: { id, userId: session.userId }});
  if (!invoice) return NextResponse.json({ error: 'not found' }, { status: 404 });

### Severity reasoning
CRITICAL — affects all customer data, exploitable by any logged-in user, no
detection in current monitoring.

### Suggested owner: <name>
### Suggested deadline: <date — typically 7 days for critical>
```

### Severity classes

Use a small scale, consistently applied:

- **CRITICAL** — exploitable without auth, or with low-effort auth, affects all users or money / data integrity
- **HIGH** — exploitable with some pre-condition (specific user role, specific data), affects sensitive data
- **MEDIUM** — exploitable but limited blast radius, or requires significant attacker effort
- **LOW** — defense-in-depth, hygiene improvement, not directly exploitable
- **INFO** — observation, no action required

Aggressive severity inflation kills the report's usefulness. If everything is HIGH, nothing is HIGH.

### Group by severity, then by area

A reader skims for CRITICALs and HIGHs first. Make that easy. Within severity, group by area (auth, data handling, infra) so an owner can take their slice.

### Include a one-page summary

Decision-makers read the summary, not the report. Cover:

- How many findings, by severity
- The top 3 to fix this week
- The systemic patterns (e.g. "auth checks are inconsistent across handlers — not a finding-per-handler problem")
- Suggested timeline / sprint allocation

## Step 10 — Anti-patterns junior auditors fall into

- **Boil the ocean** — trying to audit everything in scope to the same depth. Time-box per area; go deep where impact is highest.
- **Tool output is the report** — pasting `npm audit` output without synthesis or prioritization. Tool output is candidates, not findings.
- **No reproduction steps** — "I think this might be vulnerable" is not a finding. Either prove it or downgrade to INFO.
- **Severity inflation** — calling everything CRITICAL because the auditor wants attention. Kills credibility.
- **Wrong audience** — writing for engineers when the buyer is the CTO, or vice versa. Match the language.
- **No remediation** — listing problems without "do this to fix" leaves the recipient stuck.
- **Adversarial tone** — "the developers clearly did not understand security" is unproductive. Frame as observations + fixes.
- **Missing the systemic** — listing 30 instances of the same pattern, instead of "this pattern occurs throughout the codebase; fix here is to introduce a shared helper / linter rule."
- **Auditing without authorization** — never audit a system you do not have written permission for, even if you think you're being helpful.

## Step 11 — After delivery

- **Walk through the report with the team** if possible. A 30-minute call beats a 50-page document for getting buy-in.
- **Offer to retest** specific findings after fixes — closes the loop.
- **Document what's been fixed** in the report itself, or in a follow-up appendix.
- **Note what's deferred** with the reasoning. "Accepted risk: X, until Y date, owner Z" is fine; "ignored" is not.

## When you find a critical mid-audit

Stop. Notify the client / stakeholder same-day if the finding affects customer data, money, or trust. Holding a CRITICAL for a final report on Friday when you found it on Monday is itself a finding.

## Quick checklist — am I done?

- [ ] Scope was agreed in writing
- [ ] Day-0 triage notes exist (stack, auth, secrets, data, deploy, blast radius)
- [ ] Surface inventory exists (routes, deps, infra)
- [ ] SAST/SCA/secret/container scans ran; output triaged
- [ ] Auth surface walked manually
- [ ] OWASP Top 10 grep recipes run
- [ ] Each finding has reproduction, impact, remediation, owner, deadline, severity
- [ ] Severity scale was applied consistently
- [ ] One-page summary written for decision-makers
- [ ] Critical findings communicated to client same-day they were discovered

## What this skill will not do

- Help audit a system you do not have written authorization for
- Provide exploitation techniques for findings — the report describes the issue and the fix, not the attack
- Replace a full penetration test for systems where regulatory or contractual obligations require one
- Generate a "your app is secure" certificate — audits find issues; they do not prove absence
