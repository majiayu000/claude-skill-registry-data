---
name: ls-skill-importer
description: Import external skills from a URL (GitHub or other) or local path; discover, validate, security-screen, and summarize each skill so the user can choose which to import. Use when the user wants to add skills from a repo/URL or local folder, or when screening and selecting skills to add to the framework.
metadata:
  version: "1.5"
---

# Skill importer

**Purpose:** Let the user point at a **URL** or **local path** containing skills; stage, discover, and screen them without executing candidate code during intake; let the user choose candidates and resolve collisions; then coordinate mandatory vetting, normalization, and isolated sandbox validation before any canonical import.

## When to use this skill

- User wants to "import skills from this URL" or "add skills from GitHub/anthropics/skills."
- User has a local folder or markdown and wants to screen/import skills.
- User asks to "parse a repo and add the skills" or "validate and import skills."

## Workflow (agent steps)

1. **Stage the source**  - For a repository or archive URL, fetch it into a temporary directory. For a local path, use that path as the scan root without changing it. For pasted content or a single-document URL, write the exact bytes to a temporary candidate directory. All review and normalization work stays outside `ls/skills/` until every gate below passes.
2. **Scan**  - Run `ls/tools/skill_importer_scan <path>` from the repo root. The current importer scanner takes a directory path only and writes a human-readable summary to stdout.
3. **Summarize and choose**  - Present each candidate's purpose, included files, code types, heuristic security result, and any content-safety review instructions emitted by validation tooling. Do not execute candidate code. Ask which candidates to import.
4. **Check duplicates and overlap**  - Compare selected candidates with `ls/skills/` by directory name, frontmatter `name`, description, purpose, and triggers. On collision or high overlap, offer **Ignore new**, **Replace existing**, **Merge**, or **Create as new**; get explicit user choice. If the selected source is a local directory, make a temporary staged copy before any gate may edit it; leave the source unchanged.
5. **Pass full vetting**  - Load `ls-skill-vetter` and complete its source, specification, metadata, all-files code, permission, and risk review against the staged candidate. The heuristic importer scan is evidence for this review, not a substitute for it. Continue only with a recorded passing verdict; a warning is not passed until its required user approval is recorded, and `DO NOT INSTALL` never passes.
6. **Normalize in staging**  - Load `ls-skill-normalizer` as the normative normalization contract and use [SKILL_NORMALIZATION.md](../../docs/SKILL_NORMALIZATION.md) as its synchronized public checklist and examples. Apply it to the staged candidate, documents first and tooling second. Resolve the final directory/frontmatter name and add `metadata.version: "1.0"` if missing as part of these staged edits. Present the normalization summary and key edits, obtain the required approval, then freeze the normalized candidate without copying it to the canonical tree.
7. **Validate the frozen bytes**  - Record a deterministic content digest covering every relative path and file byte in the frozen normalized candidate. If normalization changed bytes covered by the vetting report, rerun `ls-skill-vetter` on the frozen candidate. Then load `ls-skill-sandbox-tester`, copy those exact normalized bytes into its isolated sandbox, verify the sandbox copy has the same digest, run the selected smoke command, and require a pass. Record the frozen digest, final vetting verdict, normalization approval, sandbox command, and sandbox result. Any later candidate change makes the affected evidence stale and requires the corresponding gates again.
8. **Copy, register, and confirm**  - Only while all three gate records are passing, current, and bound to the frozen normalized bytes, copy those bytes to `ls/skills/<name>/` and verify the canonical copy matches. Register it per [PLATFORM_REGISTRY.md](../../docs/PLATFORM_REGISTRY.md). Deployment remains a separate explicitly authorized action and may not bypass the same evidence boundary. Confirm success only after canonical copy and registration succeed; otherwise report the blocking gate and stop.

## Rule ownership

This skill owns the operational import flow. `SKILL_IMPORTING.md` is a public reference for the same rules, but agents should load this skill for execution.

- Candidate content is never executed during import screening.
- Pasted content and single-document URLs are staged in a temporary directory, scanned, and presented before any final write.
- Duplicate/overlap choices require explicit user selection; do not auto-replace or auto-merge.
- Heuristic scan results are advisory intake evidence; they never authorize canonical mutation by themselves.
- A successful import requires current vetting, normalization, and sandbox evidence bound to the same frozen normalized bytes before canonical copy or registration.
- Missing, failed, rejected, unresolved, untested, stale, or byte-mismatched gate evidence blocks canonical copy, registration, deployment, and success confirmation.

## Security and content safety screening (heuristic only)

- Tool does **not** execute any skill code. It only scans file contents.
- **Security:** Flags risky execution patterns in scripts/assets, including dynamic evaluation, remote installer pipelines, PowerShell expression execution, sensitive file access, and privilege escalation markers. Results are advisory inputs to the mandatory `ls-skill-vetter` review; the scan alone neither accepts nor rejects a candidate.
- **Content safety:** Use [SKILL_VALIDATION_PATTERNS.md](../../docs/SKILL_VALIDATION_PATTERNS.md) for the pattern file and review flow. For pattern hits, show references only: file, line, column, pattern id, and the pattern description. Do not display the matched candidate content.

## Sources

- **URL**  - GitHub repo, archive link, or any fetchable URL. Agent fetches; then runs scan on the resulting path.
- **Local path**  - Directory on disk with skill subdirs.
- **Single markdown**  - Use the skill-creator workflow to create a new skill from a doc; that skill is then framework-compatible and can be used with this importer flow for batch consistency.
- **Pasted content or URL to a single document**  - Follow [SKILL_IMPORTING.md](../../docs/SKILL_IMPORTING.md#adding-a-skill-from-paste-or-url). Validation is always path-based; never pass skill content through the shell.

## Compatibility

- Only directories that contain a valid SKILL.md (Agent Skills spec: `name`, `description`) are considered skills. Imported skills remain spec-compliant and interchangeable (see [SKILL_INTEROPERABILITY.md](../../docs/SKILL_INTEROPERABILITY.md)).

## Reference

- [SKILL_IMPORTING.md](../../docs/SKILL_IMPORTING.md)  - Full workflow, duplicate/overlap checks, normalization, tool usage, security notes.
- [SKILL_NORMALIZATION.md](../../docs/SKILL_NORMALIZATION.md)  - Synchronized public checklist and examples for the normative `ls-skill-normalizer` workflow.
- [SKILL_VALIDATION_PATTERNS.md](../../docs/SKILL_VALIDATION_PATTERNS.md)  - Pattern file location, refresh behavior, content-safety review flow.
- [SKILL_DISCOVERY.md](../../docs/SKILL_DISCOVERY.md)  - Public registry discovery when importing.
- [PLATFORM_REGISTRY.md](../../docs/PLATFORM_REGISTRY.md)  - Registration file list after import.
- [SKILL_INTEROPERABILITY.md](../../docs/SKILL_INTEROPERABILITY.md)  - Import/export and spec alignment.
- `ls-skill-vetter`  - Mandatory full source, metadata, code, permission, and risk review before normalization or canonical mutation.
- `ls-skill-sandbox-tester`  - Mandatory isolated smoke validation of the frozen normalized bytes before canonical mutation.
