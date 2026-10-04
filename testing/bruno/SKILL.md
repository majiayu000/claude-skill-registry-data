---
name: bruno
description: "Create version-controlled Bruno API collections, write Bru request files, and run API checks through the Bruno CLI in CI."
category: cross-platform
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["bruno", "bru-markup", "api-testing", "bru-cli", "rest-api", "graphql", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Bruno API Client AI Skill Guide (Claude)

## Overview & Engine Architecture
Bruno is an offline-first, Git-native open-source API client and testing platform. Unlike Postman or Insomnia, Bruno stores API collections directly as plain-text **Bru markup files (`.bru`)** within your repository, enabling seamless version control, zero cloud vendor lock-in, and automated CI/CD execution via the **Bruno CLI (`@usebruno/cli`)**. Claude operates as an API Architecture Specialist and QA Automation Lead, specializing in **declarative `.bru` file authoring**, **JavaScript pre-request and post-response scripting (`bru.*`, `req.*`, `res.*`)**, **OAuth2/JWT token lifecycle management**, and **automated headless CI test runners**.

### Bruno File Architecture & Execution Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                 Bruno System Architecture                   │
│                                                             │
│  Git-Native Collection Hierarchy                            │
│  ├── `bruno.json` (Collection root descriptor & settings)   │
│  ├── `environments/*.bru` (Plaintext & Secret Variables)    │
│  └── `folder/request.bru` (Declarative Bru Markup DSL)      │
│                                                             │
│  Runtime & Execution Engine                                 │
│  ├── Node.js / Electron Sandboxed V8 JavaScript Runtime     │
│  ├── Axios HTTP Transport Engine                            │
│  └── `@usebruno/cli` (Headless CI/CD Test Suite Runner)     │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **Bru Markup DSL Authoring**: Write clean, valid `.bru` request definitions including `meta`, `get`/`post`/`put`/`delete`, `headers`, `auth`, `body:json`, `vars:pre-request`, `script:pre-request`, and `assert` blocks.
2. **Automated Token Chaining & Scripting**: Author JavaScript post-response scripts to extract JWT bearer tokens from authentication responses and store them dynamically in collection variables (`bru.setVar()`).
3. **Environment & Secret Isolation**: Manage environment-specific configs (`dev.bru`, `staging.bru`, `prod.bru`), ensuring secrets are tagged with `secret` keywords and added to `.gitignore`.
4. **CI/CD Test Runner Integration**: Generate robust command-line invocation scripts using `bru run` with JUnit/JSON report outputs and strict failure threshold exit codes.

---

## Production Bru File Recipe: Authenticated POST with Assertion & Token Extraction

Save this file as `users/create-user.bru` inside a Bruno collection:

```bru
meta {
  name: Create Customer Profile
  type: http
  seq: 2
}

post {
  url: {{baseUrl}}/api/v1/customers
  body: json
  auth: bearer
}

auth:bearer {
  token: {{bearerToken}}
}

headers {
  Content-Type: application/json
  X-Request-ID: {{requestId}}
}

body:json {
  {
    "email": "developer@enterprise.io",
    "name": "Jane Doe",
    "tier": "enterprise",
    "metadata": {
      "region": "us-east-1"
    }
  }
}

vars:pre-request {
  requestId: req.getUuid()
}

assert {
  res.status: eq 201
  res.body.data.id: isDefined
  res.body.data.email: eq "developer@enterprise.io"
  res.responseTime: lt 500
}

script:post-response {
  // Extract generated user ID for downstream request chaining
  if (res.getStatus() === 201) {
    const customerId = res.getBody().data.id;
    bru.setVar("createdCustomerId", customerId);
    console.log(`[BRUNO] Stored customerId: ${customerId}`);
  }
}
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **`Error: {{variable}} not resolving` in Request URL** | Active environment is not selected, or variable is defined in a different environment scope. | 1. In GUI, select active environment from dropdown.<br>2. In CLI, specify explicit environment flag: `bru run --env Local`.<br>3. Verify variable exists in `environments/<env>.bru` or was set via `bru.setVar()`. |
| **`UNABLE_TO_VERIFY_LEAF_SIGNATURE` on Local HTTPS** | Node.js TLS rejection triggered by self-signed local development certificates (e.g. `localhost`). | 1. In Bruno Preferences $\rightarrow$ *General*, disable **SSL Certificate Verification**.<br>2. In CLI execution, pass `NODE_TLS_REJECT_UNAUTHORIZED=0 bru run --env Local`. |
| **Assertion Fails on JSON Path: `Cannot read property of undefined`** | API response was not JSON formatted (e.g. HTML 500 error page) or response structure changed. | 1. Add guard assertion: `res.status: eq 200`.<br>2. In post-response script, check `typeof res.getBody() === 'object'`.<br>3. Inspect raw response headers to verify `Content-Type: application/json`. |
| **`bru run` Fails in GitHub Actions CI with Exit Code 1** | One or more assertions in the collection failed, or tests timed out waiting for backend services. | 1. Inspect JUnit/HTML report generated via `bru run --output report.html --format html`.<br>2. Increase request timeout via `--timeout 10000`.<br>3. Verify CI secrets match environment variable keys. |

---

## Command Line Syntax & CI/CD Pipelines

```bash
# Run Entire Bruno Collection Against Staging Environment
npx @usebruno/cli run --env Staging

# Run Specific Folder and Export JUnit XML for CI Pipelines
npx @usebruno/cli run tests/billing/ --env Production --output results.xml --format junit

# Run Collection Recursively with Variable Overrides
npx @usebruno/cli run --env Local --env-var baseUrl=http://127.0.0.1:8080 --bail

# Lint Collection for Broken .bru Syntax
npx @usebruno/cli lint
```

### Essential File & Directory Paths
- **Collection Descriptor**: `<collection_root>/bruno.json`
- **Environment Definitions**: `<collection_root>/environments/*.bru`
- **Global App Preferences**: `~/.config/bruno/` (Linux) / `%APPDATA%\bruno` (Windows) / `~/Library/Application Support/bruno` (macOS)
- **Sensitive Secrets File**: `<collection_root>/environments/*.secret.bru` (Must be added to `.gitignore`)

---

## Agent Operational Directive
> **MANDATORY**: Always store API requests in clean `.bru` format rather than monolithic JSON exports. In CI/CD pipelines, execute tests with `npx @usebruno/cli run --env <ENV>` and never commit secret variables to public source control.
