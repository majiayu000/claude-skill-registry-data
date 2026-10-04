---
name: mend
description: "Expert agent for Mend (formerly WhiteSource) enterprise SCA platform. Covers dependency scanning, license compliance, vulnerability management, Renovate bot integration, SBOM export, and CI/CD integration. WHEN: \"Mend\", \"WhiteSource\", \"Mend SCA\", \"mend.io\", \"Renovate\", \"Renovate bot\", \"WhiteSource bolt\", \"Mend for Containers\"."
license: MIT
---

# Mend (WhiteSource)

This skill covers Mend (formerly WhiteSource), an enterprise-grade Software Composition Analysis platform. Mend provides vulnerability detection, license compliance management, and dependency update automation via the Renovate bot integration.

## How to Approach Tasks

1. **Clarify product naming:** Mend rebranded from WhiteSource in 2022. "WhiteSource" documentation still exists; features are equivalent.
2. **Identify the product tier:**
   - **Mend SCA** -- Core SCA for vulnerability and license management
   - **Mend for Containers** -- Container image SCA
   - **Mend Application Security** -- Unified SAST + SCA
   - **Renovate** -- Automated dependency update bot (open source, integrated with Mend)
3. **Identify the task:** Scan configuration, agent setup, policy definition, remediation, CI/CD integration, Renovate configuration.

## Mend Platform Overview

Mend provides enterprise SCA with:

- **Comprehensive vulnerability database:** Continuous monitoring, proactive alerts (alerts when new CVEs match your existing dependencies)
- **License compliance:** 300+ license types tracked, policy-based blocking
- **Effective usage analysis:** Similar to reachability — determines if vulnerable code is actually used
- **Remediation guidance:** Fix suggestions with upgrade paths and alternative libraries
- **SBOM export:** CycloneDX and SPDX formats
- **Consolidation:** Multi-language, multi-project management at enterprise scale

---

## Mend Agent (Unified Agent)

The Mend Unified Agent is a command-line tool that analyzes project dependencies and reports to the Mend cloud platform.

### Installation

```bash
# Download the unified agent
curl -LJO https://unified-agent.s3.amazonaws.com/wss-unified-agent.jar

# Verify download
sha512sum -c <(curl -s https://unified-agent.s3.amazonaws.com/wss-unified-agent.jar.sha512)
```

### Configuration (whitesource.config or mend.config)

```properties
# whitesource.config
apiKey=<YOUR_API_KEY>
productName=My Product
projectName=My Service

# Scan configuration
includes=**/*.jar **/*.war **/*.ear **/*.zip
excludes=**/*test* **/*spec*

# File system scanning
fileSystemScan=true

# Resolve dependencies from package manager
resolveAllDependencies=true

# Report paths
generateReport=true
reportType=json,html

# Policy check
checkPolicies=true
forceCheckAllDependencies=false

# Language-specific settings
npm.resolveLockFile=true
maven.resolveDependencies=true
gradle.resolveDependencies=true
python.resolveHierarchyTree=true
```

### Running the Agent

```bash
# Basic scan
java -jar wss-unified-agent.jar -c whitesource.config

# Override config properties on command line
java -jar wss-unified-agent.jar \
  -c whitesource.config \
  -d /path/to/project \
  -apiKey $MEND_API_KEY \
  -productName "My Product" \
  -projectName "My Service"

# Fail on policy violations
java -jar wss-unified-agent.jar -c whitesource.config -failOnError
```

---

## Policy Management

Mend policies define what constitutes a policy violation (license issues or vulnerabilities that should block a build or alert).

### Policy Types

**License policies:**
```
License Category: Copyleft Licenses
  Licenses: GPL-2.0, GPL-3.0, AGPL-3.0, LGPL-2.1, LGPL-3.0
  Action: Reject
  
License Category: Permissive Licenses
  Licenses: MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC
  Action: Approve
  
License Category: Review Required
  Licenses: MPL-2.0, EUPL-1.1
  Action: Reassign to: legal-team
```

**Vulnerability policies:**
```
Severity: Critical (CVSS 9.0+)
  Action: Reject

Severity: High (CVSS 7.0+)
  Action: Reject
  
CVSS Score >= 7.0 AND Has Fix
  Action: Reject (require upgrade)
  
CVSS Score >= 7.0 AND No Fix
  Action: Notify (can't force fix if no fix exists)
```

### Policy Evaluation in CI/CD

When `checkPolicies=true`:
- Agent evaluates all found components against configured policies
- Exit code 2: policy violation found → break the build
- Exit code 1: error in scan → break the build
- Exit code 0: success, no policy violations

---

## Vulnerability Management

### Alert Lifecycle

```
New CVE published → Mend matches to your inventory
  ↓
Alert created → Notification sent (email/Slack/Jira)
  ↓
Developer reviews alert
  ↓
Action: Fix (upgrade) | Waive (accept risk with expiry) | False Positive
  ↓
Status updated in Mend dashboard
```

### Effective Usage Analysis

Mend's effective usage analysis (comparable to reachability):

1. Analyzes your source code (Java, JavaScript, Python, .NET)
2. Determines if the vulnerable function/class in the dependency is actually called
3. Marks vulnerable components as "effective" or "not effective"

**Note:** "Not effective" doesn't mean zero risk (indirect usage patterns may not be detected), but significantly reduces remediation priority.

### Severity Scoring

Mend augments CVSS with:
- **Exploit maturity** -- PoC available / Functional exploit / Weaponized
- **EPSS (Exploit Prediction Scoring System)** -- Probability of exploitation in the wild
- **Mend CVSS adjustments** -- Temporal and environmental score factors

---

## Renovate Bot

Renovate is an open-source dependency update bot that Mend acquired and integrates with the Mend platform. It is also fully available standalone (open source, free).

### Key Renovate Advantages over Dependabot

- **Broader package manager support:** 100+ package managers vs. Dependabot's ~15
- **More flexible grouping:** Highly configurable update grouping
- **Self-hosted option:** Run in your own infrastructure
- **Config sharing:** `extends` base configs for organization-wide standards
- **Automerge granularity:** Fine-grained conditions for auto-merge
- **Changelog generation:** Aggregated changelogs for grouped PRs

### Renovate Configuration (renovate.json)

```json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": [
    "config:base",
    "security:openssf-scorecard"
  ],
  
  "schedule": ["after 9am and before 5pm on weekdays"],
  "timezone": "America/New_York",
  
  "prCreation": "not-pending",
  "prConcurrentLimit": 10,
  "prHourlyLimit": 2,
  
  "automerge": true,
  "automergeType": "pr",
  "automergeStrategy": "squash",
  
  "packageRules": [
    {
      "description": "Auto-merge minor and patch updates for dev dependencies",
      "matchDepTypes": ["devDependencies"],
      "matchUpdateTypes": ["minor", "patch"],
      "automerge": true
    },
    {
      "description": "Require review for major updates",
      "matchUpdateTypes": ["major"],
      "automerge": false,
      "reviewers": ["team:senior-developers"]
    },
    {
      "description": "Group AWS SDK updates",
      "matchPackagePrefixes": ["@aws-sdk/"],
      "groupName": "AWS SDK packages",
      "groupSlug": "aws-sdk"
    },
    {
      "description": "Disable updates for packages we manage manually",
      "matchPackageNames": ["react", "react-dom"],
      "enabled": false
    },
    {
      "description": "Security updates get priority label",
      "matchCategories": ["security"],
      "labels": ["security", "priority"],
      "minimumReleaseAge": "0 days"
    }
  ],
  
  "vulnerabilityAlerts": {
    "enabled": true,
    "labels": ["security"]
  },
  
  "commitMessagePrefix": "chore(deps): ",
  "commitMessageAction": "update",
  
  "labels": ["dependencies"],
  
  "ignoreDeps": [
    "node"
  ],
  
  "stabilityDays": 3
}
```

### Extends Configs

Renovate supports preset configs to share standards across repos:

```json
{
  "extends": [
    "config:base",          // Renovate's official base config
    "group:allNonMajor",    // Group all non-major updates
    ":automergeMinor",      // Auto-merge minor updates
    ":separatePatchReleases", // Separate PRs for patch updates
    "schedule:earlyMondays" // Only run on Monday mornings
  ]
}
```

**Org-wide preset:** Create a `renovate-config` repository in your GitHub org and reference it:
```json
{
  "extends": ["github>my-org/renovate-config"]
}
```

### Running Renovate Self-Hosted

```bash
# Docker
docker run --rm -it \
  -e RENOVATE_TOKEN=$GITHUB_TOKEN \
  -e LOG_LEVEL=debug \
  renovate/renovate:latest \
  my-org/my-repo

# Node.js
npx renovate --token=$GITHUB_TOKEN my-org/my-repo

# Kubernetes CronJob
# See https://docs.renovatebot.com/self-hosting/
```

---

## CI/CD Integration

### Jenkins

```groovy
stage('Mend SCA Scan') {
  steps {
    script {
      sh """
        java -jar wss-unified-agent.jar \
          -apiKey ${MEND_API_KEY} \
          -c whitesource.config \
          -d . \
          -productName "${env.JOB_NAME}" \
          -projectName "${env.BUILD_TAG}" \
          -failOnError
      """
    }
  }
}
```

### GitHub Actions

```yaml
- name: Mend SCA Scan
  run: |
    curl -LJO https://unified-agent.s3.amazonaws.com/wss-unified-agent.jar
    java -jar wss-unified-agent.jar \
      -apiKey $MEND_API_KEY \
      -d . \
      -productName "${{ github.repository }}" \
      -projectName "${{ github.ref_name }}" \
      -checkPolicies true \
      -failOnError
  env:
    MEND_API_KEY: ${{ secrets.MEND_API_KEY }}
```

### Azure DevOps

Mend has a native Azure DevOps extension (WhiteSource Bolt for Azure DevOps):
```yaml
- task: WhiteSource@21
  inputs:
    cwd: '$(Build.SourcesDirectory)'
    projectName: '$(Build.Repository.Name)'
```

---

## SBOM Export

```bash
# Via Mend CLI / API
# Generate CycloneDX SBOM for a project (via REST API)
curl -X POST https://saas.mend.io/api/v2.0/sbom \
  -H "Authorization: Bearer $MEND_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "projectToken": "YOUR_PROJECT_TOKEN",
    "format": "CycloneDX",
    "version": "1.4",
    "type": "json"
  }' \
  -o sbom.json
```

---

## Common Issues

**Agent fails to detect dependencies:**
- Verify `resolveAllDependencies=true` in config
- Check that language-specific resolvers are enabled (e.g., `npm.resolveLockFile=true`)
- Ensure the build has been run so lockfiles/dependency trees are present
- Check `fileSystemScan=false` is not set (which would skip dependency resolution)

**Policy violations not failing the build:**
- Ensure `checkPolicies=true` and `failOnError=true` are both set
- Verify policies are defined in the Mend organization matching the `apiKey`

**Renovate not creating PRs:**
- Check Renovate app is installed on the repository (for Mend-hosted) or bot has write access (self-hosted)
- Review Renovate logs: `npx renovate --token=$TOKEN --log-level=debug my-org/repo`
- Verify `renovate.json` is valid JSON (common issue: trailing commas)

**License false positives (package shows wrong license):**
- Mend detects licenses from multiple sources (npm metadata, file scanning, SPDX identifiers)
- Report false positive to Mend support for database correction
- Use `whitelist` (approval) override in policy for known-good packages
