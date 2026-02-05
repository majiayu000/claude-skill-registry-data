---
name: enterprise-security
description: Central authority for Claude Code enterprise security. Covers enterprise managed policies (managed-settings.json), settings precedence hierarchy, policy file locations (macOS, Linux, Windows), unoverridable organizational policies, cloud execution security (isolated VMs, network access controls, credential protection), IDE security (VS Code, JetBrains), devcontainer security, and security best practices for teams. Assists with configuring enterprise policies, understanding precedence, and implementing organizational security standards. Delegates 100% to docs-management skill for official documentation.
user-invocable: false
allowed-tools: Read, Glob, Grep, Skill
---

# Enterprise Security Skill

## MANDATORY: Invoke docs-management First

> **STOP - Before providing ANY response about Claude Code enterprise security:**
>
> 1. **INVOKE** `docs-management` skill
> 2. **QUERY** for the user's specific topic
> 3. **BASE** all responses EXCLUSIVELY on official documentation loaded
>
> **Skipping this step results in outdated or incorrect information.**

### Verification Checkpoint

Before responding, verify:

- [ ] Did I invoke docs-management skill?
- [ ] Did official documentation load?
- [ ] Is my response based EXCLUSIVELY on official docs?

If ANY checkbox is unchecked, STOP and invoke docs-management first.

---

## Overview

Central authority for Claude Code enterprise security. This skill uses **100% delegation to docs-management** - it contains NO duplicated official documentation.

**Architecture:** Pure delegation with keyword registry. All official documentation is accessed via docs-management skill queries.

## When to Use This Skill

**Keywords:** enterprise, managed-settings.json, enterprise managed policy, settings precedence, organizational policies, cloud execution security, IDE security, VS Code security, JetBrains security, devcontainer security, team security, audit logging, credential protection

**Use this skill when:**

- Configuring enterprise managed policies
- Understanding settings precedence
- Setting up organizational security standards
- Configuring cloud execution security
- Understanding IDE security considerations
- Setting up devcontainer security
- Implementing team security practices

## Keyword Registry for docs-management Queries

Use these keywords when querying docs-management skill for official documentation:

### Enterprise Managed Policies

| Topic | Keywords |
| --- | --- |
| Overview | "enterprise managed policy", "managed-settings.json" |
| File Locations | "enterprise policy paths", "policy file locations" |
| Precedence | "settings precedence", "enterprise policies precedence" |
| Unoverridable | "unoverridable policies", "organizational restrictions" |

### Cloud Execution Security

| Topic | Keywords |
| --- | --- |
| Overview | "cloud execution security", "isolated virtual machines" |
| Network Controls | "network access controls", "cloud network security" |
| Credentials | "credential protection", "cloud credential security" |
| Branch Restrictions | "branch restrictions", "protected branches" |
| Audit Logging | "audit logging", "security audit" |
| Cleanup | "automatic cleanup", "cloud session cleanup" |

### IDE Security

| Topic | Keywords |
| --- | --- |
| VS Code | "VS Code security", "IDE security VS Code" |
| JetBrains | "JetBrains security", "IDE security JetBrains" |
| IDE Context | "IDE-specific security", "extension security" |

### DevContainer Security

| Topic | Keywords |
| --- | --- |
| Container Isolation | "devcontainer security", "container isolation" |
| Security Features | "devcontainer security features", "container security" |
| Integration | "devcontainer sandboxing", "container integration" |

### Security Best Practices

| Topic | Keywords |
| --- | --- |
| Team Security | "team security", "organizational standards" |
| Sensitive Code | "working with sensitive code", "security best practices" |
| Reporting Issues | "reporting security issues", "HackerOne", "vulnerability disclosure" |

## Quick Decision Tree

**What do you want to do?**

1. **Set up managed policies** -> Query docs-management: "enterprise managed policy", "managed-settings.json"
2. **Understand precedence** -> Query docs-management: "settings precedence", "enterprise policies precedence"
3. **Find policy file locations** -> Query docs-management: "enterprise policy paths", "policy file locations"
4. **Configure cloud security** -> Query docs-management: "cloud execution security", "isolated virtual machines"
5. **Understand IDE security** -> Query docs-management: "VS Code security", "JetBrains security"
6. **Set up devcontainer** -> Query docs-management: "devcontainer security", "container isolation"
7. **Follow best practices** -> Query docs-management: "team security", "security best practices"

## Topic Coverage

### Managed Policies Topics

- managed-settings.json locations (macOS, Linux, Windows)
- Settings precedence hierarchy
- Unoverridable organizational policies
- Policy enforcement mechanisms

### Cloud Security Topics

- Isolated virtual machines
- Network access controls
- Credential protection
- Branch restrictions
- Audit logging
- Automatic cleanup

### IDE Security Topics

- VS Code extension security
- JetBrains plugin security
- IDE-specific security contexts

### DevContainer Topics

- Container isolation benefits
- Security features in devcontainer setup
- Integration with sandboxing

### Best Practices Topics

- Working with sensitive code
- Team security standards
- Reporting security issues (HackerOne)
- Vulnerability disclosure

## Troubleshooting Quick Reference

| Issue | Keywords for docs-management |
| --- | --- |
| Policy not applied | "enterprise managed policy", "settings precedence" |
| Wrong precedence | "settings precedence", "enterprise policies precedence" |
| Cloud security issues | "cloud execution security", "network access controls" |
| IDE security concerns | "VS Code security", "JetBrains security" |
| Container issues | "devcontainer security", "container isolation" |

## Related Skills

- **sandbox-configuration** - For sandboxing and isolation
- **permission-management** - For allow/deny/ask rules
- **settings-management** - For general configuration

## Version History

- **v1.0.0** (2025-11-30): Initial release (split from security-meta)
  - Focused on enterprise security only
  - Pure delegation architecture
  - Comprehensive keyword registry

---

## Last Updated

**Date:** 2025-11-30
**Model:** claude-opus-4-5-20251101
