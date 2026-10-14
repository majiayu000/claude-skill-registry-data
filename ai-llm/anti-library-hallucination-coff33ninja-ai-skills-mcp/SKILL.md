---
name: anti-library-hallucination
description: Prevents suggesting non-existent packages, fabricated library names, and invalid version pins. Also guards against typosquatting and slopsquatting risks.
---

# Anti-Library Hallucination Skill

## Problem

LLMs invent non-existent packages at alarming rates:
- 99% of fake library names are accepted without question
- 1-character typos in library names trigger hallucinations in up to 26% of tasks
- Year-based prompts ("a library from 2025") produce hallucinations up to 84% of the time
- 91.96% of hallucinated version strings follow real versioning conventions but were never released
- 27.76% of LLM-suggested dependency upgrades point to non-existent versions
- Some hallucinated names get registered by attackers (slopsquatting)

## Detection triggers

Activate when:
- Suggesting a pip/npm/cargo/maven package to install
- Writing `import` or `from ... import` for an unfamiliar library
- Pinning a specific version number
- The user asks for a library "for X task" without naming one
- The project needs a dependency added

## Protocol

### 1. Never invent a package name
If you don't know a package exists, do NOT guess. Say: "I'm not sure which package to recommend for that. Check PyPI/npm/crates.io or tell me what you've used before."

### 2. Verify before importing
Before writing an import for a library not already in the project:
- Check if it's already in requirements.txt, pyproject.toml, Cargo.toml, package.json
- Look at existing imports in the project for the same library
- If the library is unfamiliar, state the uncertainty

### 3. Version pinning rules
When pinning a version:
- Verify the version actually exists in the registry
- Do not invent patch versions — stick to major.minor or "latest"
- Prefer range specifiers over exact pins unless the project convention requires exact pins
- Check if the pinned version has known CVEs

### 4. Typos and misspellings
If the user types a library name with a possible typo:
- Do NOT assume they meant a valid library and use it
- Ask: "Did you mean `correct-name`? The name you wrote doesn't match any package I'm sure about."

### 5. Year-based and adjective-based requests
When asked for a "library from 2025" or a "fast XML parser":
- Do NOT invent a package that fits the description
- Suggest well-known packages in the space
- If none come to mind, say so

## When NOT to use
- Standard library modules (os, sys, json, etc.)
- Packages already in the project's dependencies
- Well-known packages you've verified exist recently

## Bundled Script

Copy `verify-package.ps1` to your project's `.ai_scripts/` directory:

```powershell
cp <skill-path>/anti-library-hallucination/scripts/verify-package.ps1 .ai_scripts/
```

Checks if a package name exists on npm/PyPI/Cargo/nuget/Go proxy before suggesting it:

```powershell
.ai_scripts\verify-package.ps1 -PackageName requests -Registry pypi
.ai_scripts\verify-package.ps1 -PackageName zod -Registry npm
```

## Cross-references

- **verify-and-cite** — Both require verification before suggesting a library/fact.

- **anti-phantom-symbols** — Both prevent invented APIs. This one covers package names; anti-phantom-symbols covers symbols within them.

- **anti-rogue-actions** — Suggesting a real but wrong package can cause destructive side effects.
- **skill-loader** — Apply the capped selection policy when deciding which verification skills should also be active during library suggestion tasks.
