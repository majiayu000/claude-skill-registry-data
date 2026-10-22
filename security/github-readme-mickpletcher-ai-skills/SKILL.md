---
name: github-readme
description: Write or repair an accurate, repository-specific README based on verified project files and requirements.
---
<!-- GENERATED CANDIDATE: edit master-skills or adapters, not this file -->
# Repository README Writer

## Purpose
Create or update README documentation that accurately describes a repository, its installation, configuration, use, testing, and limitations. Prefer verified evidence over plausible-looking instructions.

## Triggers
Use when asked to write, rewrite, repair, or document a repository README. Recognize the shortcuts `readme` and `gr` followed by repository details.

## Do not use
- For designing a new repository from scratch: use a repository architecture workflow.
- For implementing code, reviewing a pull request, or auditing unrelated documentation.
- When the user has provided too little information to identify the repository: ask for a repository link, path, or description.

## Inputs and evidence
Obtain the repository name, purpose, audience, language, files, entry points, dependencies, configuration, license, and existing README when available. Prefer inspected repository files over an old README, and an old README over unsupported guesses. If repository access is unavailable, label any unverifiable commands, paths, and claims explicitly.

## Workflow
1. Classify the repository (single script, CLI, API, MCP server, automation, multi-module toolkit, skills library, website, or template).
2. Inspect available source files and existing documentation. Verify names, paths, command flags, environment variables, dependencies, and license text.
3. Determine whether to repair existing sections or create a new README. Preserve useful existing structure and voice; avoid unnecessary rewrites.
4. Draft only applicable sections: overview, capabilities, component inventory, structure, prerequisites, installation, configuration, usage, tests, troubleshooting, security, related projects, and license.
5. Provide runnable examples only when grounded in inspected files or explicit user input. Mark unverified examples clearly.
6. Cross-check all links, filenames, commands, and configuration names against evidence. Identify unresolved assumptions.
7. Deliver the requested README text or, when repository write access is available and authorized, propose or apply the file change and report what was actually committed.

## Writing requirements
Use plain, direct technical language and short paragraphs. Avoid promotional adjectives, emojis, empty headings, invented testimonials, and generic setup commands. Use tables for modules, environment variables, and parameters when useful. Keep the license section accurate and last. Respect the user's preferred voice without hardcoding an individual author.

## Repair mode
Compare the current README to verified repository contents; identify stale sections, broken paths, and missing features. Prefer targeted updates when the document remains substantially correct. Explain any major omissions or changes.

## Validation
- All documented paths and case-sensitive filenames exist or are marked unverified.
- Setup and usage commands match real entry points or are explicitly hypothetical.
- Dependencies, configuration, and license claims are supported by evidence.
- Security notes appear when credentials or sensitive data are involved.
- The result has no placeholders disguised as finished documentation.
- The README matches the repository's actual scope, not a generic template.

## Examples
- "readme for this Python CLI, using the actual pyproject.toml and commands"
- "gr owner/repository: repair outdated installation and usage instructions"
- "Draft a README for this PowerShell module based on the supplied files"
