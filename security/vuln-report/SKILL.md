---
name: vuln-report
description: >
  Write a vulnerability report. Use when the user says "vulnerability report",
  "vuln report", "security finding", "write up this finding", "pentest finding",
  "bug bounty report", "security disclosure", "CVE writeup", "document this vulnerability",
  "how to report a security issue", or needs to formally document a security vulnerability
  with evidence, impact, and remediation guidance - even if they don't explicitly say "report".
---

## Overview

Based on **Penetration Testing** (Georgia Weidman) and industry bug bounty standards (HackerOne, Bugcrowd). A vulnerability report is the primary deliverable of security testing. Its job is to make the reader understand the risk, believe it is real (evidence), and know exactly how to fix it. Reports that lack clear reproduction steps are ignored. Reports that lack business impact framing are deprioritized.

Weidman's rule: a finding no one acts on is a finding that didn't matter. Write for the engineer who needs to fix it AND the manager who needs to prioritize it.

## Workflow

### Step 1: Write the finding header

```
Finding title: [Concise, specific title that names the vulnerability and affected component]
  Good: "SQL Injection in /api/search allows unauthenticated data exfiltration"
  Bad: "SQL Injection Found"

Finding ID: [VULN-001 / internal reference]
Severity: [Critical / High / Medium / Low / Informational]
CVSS Score: [e.g. 9.8 (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H)]
CWE: [e.g. CWE-89: SQL Injection]
Affected component: [URL, endpoint, function, or system]
Discovered: [date]
Reported by: [tester name or handle]
Status: [Open / Remediated / Accepted Risk]
```

### Step 2: Write the executive summary

2-3 sentences for a non-technical reader. No jargon. Lead with impact, not with the technical detail.

```
[What is at risk, who is at risk, and what an attacker can do.]

Example: "The search endpoint is vulnerable to SQL injection. An unauthenticated
attacker can extract all user records from the database, including email addresses
and hashed passwords for [N] users. No special tools or skills are required."
```

### Step 3: Write the technical description

Explain the vulnerability mechanically: what it is, why it exists, and what makes it exploitable.

```
Vulnerability class: [SQL Injection / XSS / IDOR / etc.]

Description:
[Explain the root cause. What input is unsanitized? What query is constructed? What check
is missing? Why is this exploitable in this specific context?]

Example: "The /api/search endpoint concatenates the `q` parameter directly into a SQL
query without parameterization:

  query = "SELECT * FROM products WHERE name LIKE '%" + request.q + "%'"

The query is executed with a DB user that has SELECT access across all tables. This allows
an attacker to inject SQL that reads from arbitrary tables including the users table."
```

### Step 4: Write reproduction steps

Numbered, exact, copy-pasteable. Another engineer should be able to reproduce without asking questions.

```
Prerequisites: [unauthenticated / authenticated as standard user / etc.]
Environment: [production URL / staging / specific version]

Steps:
1. Navigate to: https://[target]/api/search
2. Send the following request:
   GET /api/search?q=test' UNION SELECT username,password,email,NULL FROM users--
   Host: [target]
3. Observe the response contains user records from the `users` table:
   [paste example response showing PII]

Time to reproduce: [2 minutes]
Tools required: [Browser / Burp Suite / curl]
```

### Step 5: Document evidence

Attach or reference:
- Screenshots with annotations showing the vulnerable request and response
- Curl commands or Burp request/response pairs
- Any data accessed (use redacted samples - do not include real PII in the report)

```
Evidence:
- Screenshot 1: [vuln-001-request.png] - HTTP request with injection payload
- Screenshot 2: [vuln-001-response.png] - Response showing extracted user records (redacted)
- Burp file: [vuln-001.burp] - Full request/response session

Note: Real user data was not retained. Screenshots show [first name] field populated
with test values to confirm extraction was possible.
```

### Step 6: Document impact

Describe the realistic worst-case scenario. Quantify where possible.

```
Confidentiality impact: [data exposed, e.g. all user emails and hashed passwords]
Integrity impact: [can attacker modify data? e.g. none / could update records]
Availability impact: [can attacker disrupt service? e.g. none]
Scope: [who is affected - all users / specific role / all customers]
Exploitability: [unauthenticated, no special tools required, exploitable remotely]
Business impact: [regulatory exposure, breach notification obligation, reputational risk]

Example: "An attacker can extract the full users table containing ~50,000 records.
Each record includes email, hashed password (bcrypt), and last login date.
This constitutes a notifiable breach under GDPR Article 33 if exploited."
```

### Step 7: Write remediation guidance

Specific, actionable, prioritized. Include a code example where applicable.

```
Remediation:

Primary fix (required):
Use parameterized queries for all database operations. Replace string concatenation
with prepared statements:

  # Vulnerable (current):
  query = "SELECT * FROM products WHERE name LIKE '%" + request.q + "%'"

  # Fixed:
  query = "SELECT * FROM products WHERE name LIKE ?"
  cursor.execute(query, ('%' + request.q + '%',))

Secondary controls (defense in depth):
- Restrict the DB user to the minimum required tables (principle of least privilege)
- Add input validation to reject SQL metacharacters in the search field
- Enable a WAF rule to detect SQL injection patterns in query parameters

Verification: After fix, retest with payload:
  ?q=test' UNION SELECT 1,2,3--
  Expected: 400 error or no results. No SQL structure in response.

Remediation effort estimate: [Low / Medium / High - e.g. 2-4 hours for a developer familiar with the codebase]
```

## Anti-Patterns

**1. No reproduction steps**
Bad: "SQL injection was found in the search endpoint."
Good: Exact URL, exact payload, expected response. Reproducible in under 5 minutes.

**2. Technical description without business impact**
Bad: "This is a reflected XSS."
Good: "This allows an attacker to inject scripts that run in a victim's browser, steal session cookies, and take over their account. Delivered via a crafted link sent over email."

**3. Remediation is generic**
Bad: "Use parameterized queries."
Good: Show the vulnerable code pattern, the fixed code pattern, and what to test after the fix.

**4. Evidence includes real PII**
Bad: Screenshot shows real user emails from extracted database.
Good: Real PII redacted or replaced with test markers. Report proves exploitability without retaining actual customer data.

## Quality Checklist

- [ ] Title is specific - names the vulnerability type and affected component
- [ ] CVSS score and CWE referenced
- [ ] Executive summary leads with business impact (no jargon)
- [ ] Technical description explains root cause, not just symptoms
- [ ] Reproduction steps are numbered, exact, and testable by another engineer
- [ ] Evidence attached with real PII redacted
- [ ] Impact quantified - who is affected, what data, regulatory exposure
- [ ] Remediation includes: primary fix with code example, secondary controls, and verification test
- [ ] Remediation effort estimated
