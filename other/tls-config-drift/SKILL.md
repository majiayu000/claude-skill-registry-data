---
name: tls-config-drift
description: "TLS config drift scanner: harvests every TLS-version constant, cipher-suite array, cert-pinning call, mTLS flag, cert-validation callback, and FIPS-mode setting. LLM analyses each statement as acceptable, misconfigured, or downgrade-prone when an element is missing. Read-only. Audience: Senior. Trigger: /ssl-drift"
trigger: /ssl-drift
---

## What this is for

TLS configuration drifts silently: a developer adds TLS_RSA_WITH_RC4_128_SHA to
a cipher array, pins the wrong public-key fingerprint, or forgets `rejectUnauthorized`
in an mTLS setup. `security-smell-scanner` flags generic "use TLS 1.2+" - no tool
reads the actual cipher suites and cert-pin values and classifies each as acceptable
vs downgrade-risk. This skill catalogs every TLS-relevant statement, and the LLM
classifies each by drift-type.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## ## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

### Step 1

1. If `-help` is passed, print the `## Usage` block below and stop.

### Step 2

2. Confirm `-ProjectDir` is provided and the path exists.

### Step 3

3. Run: `scripts/tls-config-scan.ps1 -ProjectDir "<path>"`

### Step 4

4. LLM reads the JSON output. For each finding:

### Step 5

- **TLS version**: is it TLSv1.2+ (acceptable) or TLSv1/TLSv1.1 (deprecated)?

### Step 6

- **Cipher suite array**: any NULL-cipher, RC4, CBC-SHA, or export-grade suite? Is the array restrictive or overly permissive?

### Step 7

- **Cert pinning**: is the fingerprint correct for the current certificate? Is HPKP used (deprecated/dangerous)?

### Step 8

- **mTLS**: is `rejectUnauthorized` set to `true`? Is `requestCert` paired with `ca`?

### Step 9

- **Cert validation**: does `checkServerIdentity` bypass checks? Is a custom validator weakening security?

### Step 10

- **FIPS mode**: is it explicitly enabled? Is it consistent across the project?

### Step 11

- **Downgrade risk**: if a config element is missing (e.g., no `minVersion`), what is the implicit default?

### Step 12

- Severity scale: FIPS-disabled > weak pin > TLSv1.1 > TLSv1.2 with wide cipher > missing mTLS flag.

### Step 13

5. Write `tls-config-drift-report.md` to the working directory.

## Usage

```
/ssl-drift                              # interactive
/ssl-drift <dir>                        # scan project
/ssl-drift -help                        # show usage
```

Returns JSON with `findings[]`:
`{file, line, findingType, lineContent}` plus summary counts.
