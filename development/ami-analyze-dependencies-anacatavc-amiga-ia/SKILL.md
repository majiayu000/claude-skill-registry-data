---
name: ami-analyze-dependencies
description: Analyzes the project's libraries and dependencies. It checks for unused dependencies, outdated versions, security vulnerabilities, and generates a structured report of the project's dependency health.
allowed-tools: Bash, Read, Grep, Write
---

# Skill: Dependency Analyzer

When invoked, act as a **Dependency Health Analyst**.

## Workflow

### 1. Identify the Project Ecosystem
- Scan the repository for package manager files (e.g., `package.json`, `requirements.txt`, `pom.xml`, `build.gradle`, `go.mod`, etc.).
- Identify the languages and package managers in use.

### 2. Dependency Audit
- **Outdated Dependencies:** Check which dependencies are severely outdated and should be updated.
- **Unused Dependencies:** Identify dependencies that are declared but do not appear to be imported or used in the codebase.
- **Undeclared Dependencies (Phantom):** Detect libraries that are being imported or used in the code but are missing from the ecosystem's package file (e.g., missing from `package.json`).
- **Security Vulnerabilities:** Note any dependencies that have known security vulnerabilities if the ecosystem provides this (e.g., via `npm audit` or equivalent commands).
- **Duplication/Overlap:** Identify if multiple libraries are being used for the same purpose (e.g., using both `axios` and `fetch`, or `lodash` and native array methods).

### 3. Execution of Automated Tools
- Run appropriate terminal commands to aid in your analysis (e.g., `npm outdated`, `npm audit` for Node.js, `pip-audit`, `pip check` for Python, or equivalent) based on the ecosystem.

### 4. Classify and Report Findings
- Compile a detailed report of your findings.
- Group the findings logically (e.g., "Critical Vulnerabilities", "Outdated Packages", "Unused Packages", "Undeclared Packages", "Architecture/Overlap Issues").
- For each finding, provide a clear recommendation (update, remove, or replace).
- **CRITICAL:** Output this complete structured list of findings directly to the user in the chat interface before taking any further action.

### 5. Action Plan (Optional)
- Ask the user if they would like you to automatically apply any of the recommended fixes (such as updating specific packages, removing unused ones, or fixing vulnerabilities).
- If the user approves, proceed to make the requested changes and update the package files accordingly.

---
**Language Rule:** Although your code and commits MUST be in English, you MUST communicate and interact in the chat using the same language the user is speaking (e.g., Spanish, French, etc.).
