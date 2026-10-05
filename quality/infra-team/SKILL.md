---
name: infra-team
description: Spawn an infrastructure team for Homebrew packages, system setup, and security hardening. Use when modifying Brewfile, adding system-level packages, or reviewing infrastructure security.
user-invocable: true
argument-hint: <infrastructure-change-description>
context: fork
agent: brew-specialist
---

# Infrastructure Team Spawn Recipe

## Team Composition

| Role | Model | Tools | Purpose |
|------|-------|-------|---------|
| **Lead/Coordinator** (you) | inherit | All | Coordinate infrastructure changes |
| **Brew Specialist** | Haiku | Read, Glob, Grep, Bash | Brewfile, cask management |
| **Security Auditor** | Sonnet | Read, Glob, Grep | Review security implications |
| **Reviewer** | Sonnet | Read, Glob, Grep, Bash | Documentation and review |

## Spawn Protocol

1. **Analyze** the infrastructure change requirements
2. **Spawn brew-specialist**:
   - Modify Brewfile as needed
   - Handle cask installations
   - Resolve conflicts with mise (prefer mise for CLI tools)
3. **Spawn security-auditor** (in parallel):
   - Review all changes for security implications
   - Check for known vulnerabilities in new packages
   - Verify secrets management compliance
4. **Spawn reviewer** after both complete:
   - Review documentation updates
   - Verify Brewfile is sorted and clean
5. **Validate**: `brew bundle check` and `uv run mde-py validate --all`

## File Ownership (No Conflicts)

| Owner | Owns | Cannot Touch |
|-------|------|-------------|
| Brew Specialist | `Brewfile`, `Brewfile.lock.json` | mise config, src/ |
| Security Auditor | Nothing (read-only) | Everything |
| Reviewer | Nothing (read-only) | Everything |
| Lead | `docs/`, integration | Delegates Brewfile |

## Conflict Resolution
- Tool in both Brewfile AND mise? Remove from Brewfile (mise wins)
- Tool is brew-only (GUI apps, system libs)? Keep in Brewfile
- Tool has mise registry entry? Use mise instead

## Quality Gate
```bash
brew bundle check
brew doctor
uv run mde-py validate --all
```
