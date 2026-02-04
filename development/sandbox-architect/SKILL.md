---
name: sandbox-architect
description: Analyze codebases to generate optimal Claude Code Sandbox configurations. Use this skill when users need to set up sandbox security settings for their projects. This skill should be triggered when users ask about sandbox configuration, security settings, or when setting up Claude Code for a new project. It analyzes the codebase stack (Node.js, Python, Rust, Go, PHP, etc.), detects dependencies, and generates appropriate sandbox and permission settings through an interactive Q&A process.
---

# Sandbox Architect

## Overview

This skill analyzes a codebase to understand its technology stack, architecture, and dependencies, then generates tailored Claude Code Sandbox configurations. The skill uses an interactive question-and-answer approach to achieve 95% confidence before generating the final configuration.

## Workflow

### Phase 1: Automatic Codebase Analysis

Before asking questions, analyze the codebase automatically:

1. **Run the analysis script** to detect the stack:
   ```bash
   python3 scripts/analyze_codebase.py
   ```

2. **If the script is unavailable**, manually check for:
   - `package.json` → Node.js/JavaScript
   - `requirements.txt`, `pyproject.toml`, `setup.py` → Python
   - `Cargo.toml` → Rust
   - `go.mod` → Go
   - `composer.json` → PHP
   - `Gemfile` → Ruby
   - `pom.xml`, `build.gradle` → Java
   - `*.csproj` → .NET
   - `Dockerfile`, `docker-compose.yml` → Container-based

3. **Identify key patterns**:
   - Web frameworks (Next.js, Django, FastAPI, etc.)
   - Dev servers (Vite, webpack-dev-server, etc.)
   - Testing frameworks (Jest, pytest, etc.)
   - Docker/container usage
   - Database connections
   - External API integrations

### Phase 2: Interactive Clarification Questions

Ask clarifying questions until 95% confident. Number each question and provide labeled options.

#### Question Template Format

```
**[N]/ [Question Title]**

[Brief context about why this matters]

Options:
- **a)** [Option description]
- **b)** [Option description]
- **c)** [Custom input option if applicable]

**Recommendation**: [Your recommended choice] - [Reason why]
```

#### Core Questions to Ask

**1/ Security Posture**

Different projects require different security levels based on their context.

Options:
- **a)** Learning/Exploration - I'm experimenting and want minimal friction
- **b)** Standard Development - Balance between security and productivity
- **c)** High Security - Working with sensitive code, untrusted dependencies, or production systems
- **d)** CI/CD Pipeline - Automated environment with strict controls

**Recommendation**: b) Standard Development - Provides good security while maintaining productivity. Switch to c) if handling credentials or untrusted code.

---

**2/ Development Server Usage**

Dev servers need to bind to localhost ports (especially on macOS).

Options:
- **a)** Yes - I run dev servers (npm run dev, python manage.py runserver, etc.)
- **b)** No - This is a library, CLI tool, or backend-only project
- **c)** Sometimes - I occasionally test with local servers

**Recommendation**: Based on detected framework. If web framework detected, recommend a).

---

**3/ Container/Docker Usage**

Docker commands are incompatible with sandbox and need special handling.

Options:
- **a)** Yes - I use docker, docker-compose, or similar container tools
- **b)** No - No containerization in this project
- **c)** Sometimes - Docker is optional for this project

**Recommendation**: If Dockerfile detected, recommend a) and add to excludedCommands.

---

**4/ Git Operations Preference**

Git push/commit can be sensitive operations.

Options:
- **a)** Auto-allow all git operations (sandboxed)
- **b)** Ask before push/commit (recommended for team projects)
- **c)** Ask before all git operations (maximum caution)

**Recommendation**: b) - Allows routine git status/diff/log but prompts before changing history.

---

**5/ SSH Agent Access** (Linux/macOS)

Required for SSH-based git authentication.

Options:
- **a)** Yes - I use SSH keys for GitHub/GitLab
- **b)** No - I use HTTPS with credential helper
- **c)** Not sure - Check my setup

**Recommendation**: If .git/config shows SSH remote URLs, recommend a).

---

**6/ Sensitive Files to Protect**

Beyond the defaults (.env, secrets), identify project-specific sensitive files.

Options:
- **a)** Default protection only (.env, .env.*, secrets/)
- **b)** Add custom paths (please specify)
- **c)** I have credentials in non-standard locations

If b) or c) selected, ask: "Please list the file patterns to protect (e.g., `config/production.yml`, `*.key`)"

**Recommendation**: a) unless detected files like `credentials.py`, `*.pem`, `*.key`.

---

**7/ Package Registry Access**

Network access needed for installing dependencies.

Options:
- **a)** Public registries only (npmjs.org, pypi.org, crates.io, etc.)
- **b)** Private/internal registry (please specify domain)
- **c)** Air-gapped - No network access needed
- **d)** Mixed - Both public and private registries

**Recommendation**: Based on detected package manager and any .npmrc/.pypirc files.

---

**8/ Escape Hatch Behavior**

When a command fails in sandbox, should Claude retry outside sandbox?

Options:
- **a)** Yes - Allow unsandboxed retries with prompt (good for discovering requirements)
- **b)** No - Fail closed, I'll update config manually (maximum security)

**Recommendation**: a) for new projects (learning phase), b) for established configs.

---

**9/ Auto-Allow Sandboxed Commands**

Should sandboxed bash commands run without prompting?

Options:
- **a)** Yes - Auto-allow (recommended for trusted projects)
- **b)** No - Still prompt for approval (useful for learning what Claude runs)

**Recommendation**: a) for productivity, b) when learning Claude Code or auditing behavior.

---

**10/ Additional Tools/Commands** (if applicable)

Based on codebase analysis, ask about specific tools detected:

- Kubernetes (kubectl, helm)
- Database CLIs (psql, mysql, mongosh)
- Cloud CLIs (aws, gcloud, az)
- Build tools (make, gradle, maven)

### Phase 3: Configuration Generation

After collecting answers, generate the configuration by:

1. Reading `references/stack-templates.md` for the base template
2. Customizing based on user answers
3. Adding detected dependencies and domains
4. Presenting the final configuration with explanations

#### Output Format

```json
// .claude/settings.json
// Generated by Sandbox Architect for [detected stack]
{
    "sandbox": {
        // [Comment explaining each setting]
    },
    "permissions": {
        // [Comment explaining each rule]
    }
}
```

### Phase 4: Verification

After generating the config:

1. Summarize what the configuration does
2. List any trade-offs or limitations
3. Provide next steps for testing
4. Offer to adjust if needed

## Key Principles

### Ask Questions Progressively

- Start with high-impact questions (security posture, dev server)
- Skip questions that analysis already answered
- Group related questions when possible
- Explain WHY each question matters

### Provide Clear Recommendations

Every question must include:
- Numbered options (a, b, c, etc.)
- A clear recommendation with reasoning
- Context-specific advice based on codebase analysis

### Reference the Documentation

For complex scenarios, reference `references/sandbox-guide.md` which contains:
- Complete setting descriptions
- Platform-specific notes (Linux vs macOS)
- Security threat model
- Troubleshooting guidance

## Resources

### scripts/

- `analyze_codebase.py` - Automatic stack and dependency detection

### references/

- `sandbox-guide.md` - Complete Claude Code Sandbox documentation
- `stack-templates.md` - Pre-built configurations for common stacks

### Confidence Threshold

Reach 95% confidence before generating configuration. Factors that increase confidence:

- Clear stack identification (+20%)
- Dev server needs known (+15%)
- Docker usage clarified (+10%)
- Git auth method confirmed (+10%)
- Sensitive file paths identified (+15%)
- Network requirements known (+15%)
- Security posture selected (+15%)

If confidence is below 95%, continue asking clarifying questions about uncertain areas.
