---
name: vuln-poc
description: Prove a suspected vulnerability in the user's own code with a minimal, local proof-of-concept test that fails while the vulnerability exists, then fix it and keep the test as a regression guard. Use when the user asks to confirm, reproduce, or write a proof of concept or exploit test for a vulnerability finding in their own project, for example from agent-kit:security-audit. Do not use against third-party systems, production, or hosts the user does not own, for finding vulnerabilities in the first place (use agent-kit:security-audit), or for non-security bugs (use agent-kit:debugging).
---

# Vulnerability proof of concept

## Scope

Work only on the user's own code, running locally or in a test environment the user names. Never send exploit traffic to production, shared staging, or any host the user has not confirmed is theirs and in scope. Do not write payloads that spread, persist, destroy data, or evade detection; a proof of concept only needs to demonstrate the flaw.

## 1. Understand the finding

- Restate the vulnerability: the entry point, the attacker-controlled input, the missing control, and the impact (data read, data changed, code run, access gained).
- Read the code path from entry point to sink and confirm the finding is reachable. If it is not, report that and stop.

## 2. Write the proof as a test

- Add a test in the project's framework that drives the real entry point (an HTTP request through the test client, a function call with crafted input) and asserts the secure behavior: a 403 for another tenant's record, a parameterized query that returns no extra rows, a rejected path traversal.
- Use benign payloads that make the impact observable without harm, for example `' OR '1'='1` to return extra rows, `../` to read a fixture file, another test user's ID for IDOR.
- Run the test and show it failing because of the vulnerability. That failure is the proof.

## 3. Fix and verify

- Fix the root cause at the boundary (parameterize the query, add the ownership check, validate and canonicalize the path) using the project's existing patterns.
- Run the proof-of-concept test and the full suite; the test must now pass. Check sibling code paths for the same flaw.

## 4. Report

Report the vulnerability, the proof-of-concept test and its failing output before the fix, the fix, test results after it, and other places with the same pattern.

## Examples

- Use: "Write a test proving the IDOR in GET /orders/:id, then fix it." "Confirm this SQL injection finding."
- Skip: "Exploit our competitor's login page." "Run this payload against production."
