---
name: data-classification-scanner
displayName: Data Classification Scanner
tagline: Scan repos and storage for PII, PHI, and sensitive data exposure, then generate a classification report.
description: |
  Scans GitHub repositories, S3 buckets, and Google Drive for personally identifiable
  information (PII), protected health information (PHI), financial data, and other
  sensitive content. Classifies findings by data type and sensitivity level, maps
  data flows, and generates a comprehensive data classification report with remediation
  recommendations.
department:
  - Security & Compliance
  - Cloud Security
use_cases:
  - Compliance Audit
  - Documentation
tools_required:
  - GitHub MCP
  - AWS MCP
  - Google Drive MCP
agents_compatible:
  - Claude / Claude Code
  - Cursor
  - Windsurf
  - ChatGPT
  - GitHub Copilot
  - Any MCP-compatible agent
author: Webrix
verified: true
updatedAt: 2026-02-24
version: 1.0.0
exampleInput: |
  We're a healthcare company subject to HIPAA and need to know where sensitive data
  lives before our annual compliance audit. Can you scan our 60 GitHub repos and 15
  S3 buckets for PII and PHI? We also have a shared Google Drive with patient-facing
  documents. Need a classification report showing what we found, where it is, and
  what we should do about it.
exampleOutput: |
  Data Classification Report — Healthcare Corp (HIPAA Scope)

  EXECUTIVE SUMMARY
  Total Findings:     47 across 3 data sources
  Critical (PHI):     12 — SSN, medical record IDs, patient names in code/config
  High (PII):         18 — Email, phone, addresses in repos and S3
  Medium:             11 — Financial data, internal IDs
  Low (metadata):     6  — Sample data, test fixtures

  FINDINGS BY SOURCE
  | Source        | Critical | High | Medium | Low | Total |
  |---------------|----------|------|--------|-----|-------|
  | GitHub (60)   | 8        | 14   | 7      | 4   | 33    |
  | S3 (15)       | 3        | 3    | 2      | 1   | 9     |
  | Google Drive  | 1        | 1    | 2      | 1   | 5     |

  TOP FINDINGS (Critical)
  - patient-service/config: sample SSN in config template
  - analytics-export bucket: CSV with MRN + diagnosis codes
  - patient-portal repo: hardcoded test patient name in seed data

  REMEDIATION PRIORITIES
  1. Remove PHI from patient-service config, use env vars
  2. Encrypt S3 analytics-export bucket, enable access logging
  3. Replace seed data with synthetic PHI in patient-portal

  Generated: Data flow map, sensitivity matrix, remediation checklist
---

# Data Classification Scanner

Scan repos and storage for PII, PHI, and sensitive data exposure, then generate a classification report.

**Integrations:** GitHub, AWS, Google Drive

## When to Use

- The user needs to identify where sensitive data (PII, PHI, financial) is stored before a compliance audit
- A new regulation (HIPAA, GDPR, PCI-DSS) requires a data inventory and classification
- The user mentions "data classification", "PII scan", "PHI inventory", "sensitive data discovery", or "compliance data map"
- Teams want to document data flows and sensitivity for security reviews or due diligence

## Steps

### Step 1: Define Classification Taxonomy

Establish data categories and sensitivity levels:

| Data Type | Examples | Sensitivity Level | Compliance Relevance |
|-----------|----------|-------------------|---------------------|
| **PHI** | SSN, medical record IDs, diagnoses, treatment codes | Critical | HIPAA |
| **PII** | Name, email, phone, address, DOB, driver's license | High | GDPR, CCPA |
| **Financial** | Credit card, bank account, tax ID | High | PCI-DSS |
| **Credentials** | Passwords, API keys, tokens | Critical | Various |
| **Internal IDs** | Employee ID, customer ID (non-PII) | Medium | Internal policy |
| **Public / Non-sensitive** | Marketing content, product docs | Low | N/A |

Define scope with the user: Which regulations apply? Which data types are in scope? Which repositories, buckets, or drives should be included?

### Step 2: Scan Code Repositories

Use GitHub MCP to search across repositories for sensitive patterns:

| Pattern Category | Examples | Detection Approach |
|------------------|----------|-------------------|
| SSN | `xxx-xx-xxxx`, `\d{3}-\d{2}-\d{4}` | Regex, format validation |
| Email | `user@domain.com` | Regex (exclude generic samples) |
| Phone | E.164, US format | Regex, country-specific patterns |
| Medical IDs | MRN, NPI, ICD codes | Domain-specific patterns |
| Credit card | `4xxx`, `5xxx` (Luhn check) | Format + checksum |
| API keys / secrets | `api_key=`, `password=`, token prefixes | Config patterns |
| Addresses | Street, city, postal code | Structured pattern matching |

| Scope Option | Description |
|--------------|-------------|
| **Repos** | Org-wide, team-owned, or user-provided list |
| **Paths** | Include/exclude (e.g., skip `node_modules/`, `vendor/`, tests) |
| **File types** | Config, env samples, seed data, SQL migrations |
| **History** | Head only vs. full git history |

Record: repo, file path, line number, data type, sample (redacted), and whether it's production config vs. test/sample.

### Step 3: Scan Cloud Storage

Use AWS MCP and Google Drive MCP to inventory and sample storage:

| Storage Type | What to Check | Tools / Approach |
|--------------|---------------|------------------|
| **S3 buckets** | Bucket listing, object metadata, sample object contents | List buckets, list objects, GetObject (sample) |
| **S3 policy** | Public access, encryption, logging | GetBucketPolicy, GetBucketEncryption |
| **Google Drive** | Shared drives, folder structure, file contents | List files, read document text |
| **Object naming** | File names suggesting PII (e.g., `patient_123.csv`) | Metadata and path analysis |

| Finding Field | Description |
|---------------|-------------|
| Bucket / Drive path | Full path or key |
| Object count / size | Approximate scope |
| Data type detected | PHI, PII, financial, etc. |
| Encryption status | Encrypted at rest? |
| Access controls | Public, shared, private |
| Sample finding | Redacted excerpt |

### Step 4: Map Data Flows

Document how sensitive data moves through systems:

| Flow Element | Description |
|--------------|-------------|
| **Source** | Repo, bucket, database, API |
| **Sink** | Where data is sent (e.g., analytics, third-party) |
| **Processing** | Transformations, aggregations |
| **Retention** | How long data is kept |
| **Access** | Who can read/write (roles, teams) |

Infer flows from: import statements, API calls, config references, and documented integrations. Note any cross-boundary transfers (e.g., repo → S3, S3 → external vendor).

### Step 5: Generate Classification Report

Produce a structured report with:

| Section | Content |
|---------|---------|
| **Executive Summary** | Total findings, breakdown by severity and source |
| **Findings by Source** | Table: GitHub / S3 / Drive → Critical / High / Medium / Low |
| **Findings Detail** | Per finding: location, data type, sample (redacted), sensitivity |
| **Data Flow Map** | Diagram or table of sources → processing → sinks |
| **Sensitivity Matrix** | Data type × storage location × access controls |
| **Remediation Priorities** | Ranked by risk: remove, encrypt, restrict access, document |

For each finding, recommend: remove (if sample/test), encrypt, move to secure storage, or formally document as acceptable residual risk.

## Output

Deliver:
- Data classification report (markdown or document) with executive summary
- Findings table by source (GitHub, S3, Google Drive) and sensitivity level
- Detailed findings list with location, data type, redacted sample, and remediation action
- Data flow map showing sources, processing, and sinks
- Remediation checklist with prioritized actions (remove PHI, enable encryption, restrict access)
- Optional: Compliance mapping (e.g., HIPAA requirements → findings → controls)
