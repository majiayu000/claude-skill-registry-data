---
name: snyk
description: "Run Snyk dependency, container, and infrastructure scans; review findings, ignore policies, and CI gates."
category: devops
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["snyk", "sca", "vulnerabilities", "containers", "security", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Snyk Security Scanning AI Skill Guide

## Overview & Engine Architecture

Snyk scans applications for vulnerable dependencies (Open Source), container images, IaC misconfigs, and optionally code issues. Results flow to the Snyk UI and CI. Agents prioritize reachable/high-severity issues, prefer upgrade paths over endless ignores, and wire gates that match the team's risk appetite.

```
Manifests / lockfiles / Dockerfiles / IaC
   -> snyk test | monitor | container test | iac test
       -> Vulnerability DB + policy
           -> Fix PRs / ignores / CI fail
```

## When to use this skill

- Adding dependency scanning to repos and pipelines
- Triaging CVEs in npm/pip/maven lockfiles
- Scanning container images before deploy
- Setting org ignore policies with expiry

## Operational directives

1. Commit lockfiles; Snyk accuracy depends on resolved trees.
2. Fix by upgrading or replacing packages before ignoring.
3. Ignores need reason + expiry; permanent ignores for highs are exceptional.
4. Use `snyk monitor` for continuous tracking; `snyk test` for PR gates.
5. Never paste Snyk tokens into source; use CI secrets.

## CLI sketches

```bash
snyk auth
snyk test --severity=package-lock.json
snyk test --severity=high --json-file-output=snyk.json
snyk container test myimage:tag
snyk iac test terraform/
snyk ignore --id=SNYK-JS-LODASH-123 --expiry=2026-12-01 --reason="Mitigated by input validation; upgrade blocked"
```

## Triage matrix

| Finding | Prefer |
| --- | --- |
| Patch version available | Bump lockfile ASAP |
| Major upgrade breaking | Schedule upgrade epic; temporary ignore with expiry |
| Dev-only dependency, not shipped | Still fix; lower gate severity if policy allows |
| False positive / unreachable | Document ignore; link to analysis |

## Best practices

- Separate app SCA gates from container/IaC projects for clearer ownership.
- Fail PRs on new highs/criticals introduced by the change; baseline debt via backlog.
- Pair with `@semgrep`/`@codeql` for first-party code bugs SCA cannot see.
- Rebuild images after base-image fixes; rescanning an old tag is not remediation.

## Limitations

- Reachability analysis quality varies by ecosystem and plan features.
- Private registry auth must be configured or scans miss/partial trees.
- License scanning policies are org-specific and may block otherwise "safe" packages.

## Related skills

- `@dependabot-config` - automated dependency PR companion
- `@semgrep` / `@codeql` - SAST companions
- `@docker` - image rebuild and minimal base practices
- `@owasp-asvs` - map dependency risk into verification evidence
