---
name: project-migrate
description: Use this skill to migrate existing projects to the SynthesisFlow structure. It uses an AI-powered analysis to intelligently discover, categorize, and migrate documentation, generate rich frontmatter, and preserve git history.
---

# Project Migrate Skill

## Purpose

To intelligently migrate existing projects (brownfield) to the SynthesisFlow directory structure using a powerful, AI-assisted workflow. This skill goes beyond simple file moving by leveraging the **Gemini CLI** to analyze document content, ensuring accurate categorization and the generation of rich, meaningful metadata. It provides a safe, guided migration with discovery, analysis, backup, and validation phases to ensure zero data loss and high-quality results.

## When to Use

Use this skill in the following situations:

- Adding SynthesisFlow to an existing project with established documentation.
- Migrating docs from an ad-hoc structure to SynthesisFlow conventions.
- When you want to automatically and intelligently categorize and add metadata to existing documents.
- To ensure a safe migration with backups and rollback capabilities.

## Prerequisites

- Project with existing documentation (`docs/`, `documentation/`, `wiki/`, or markdown files).
- Git repository initialized.
- Write permissions to the project directory.
- `gemini` CLI tool installed and authenticated.
- `doc-indexer` skill available for final compliance checking.

## Workflow

The skill guides you through a series of phases with interactive approval.

### Step 1: Run the Migration Script

Execute with one of three modes:

**Interactive (default)** - Review and approve each phase:
```bash
bash scripts/project-migrate.sh
```

**Dry-run** - Preview the plan without making any changes:
```bash
bash scripts/project-migrate.sh --dry-run
```

**Auto-approve** - Skip prompts for automation (useful for CI/CD):
```bash
bash scripts/project-migrate.sh --auto-approve
```

### Step 2: Review Each Phase

**Phase 1 & 2 - AI-Powered Discovery and Analysis**:
The script scans for all markdown files. For each file, it calls the **Gemini CLI** to analyze the document's *content*, not just its filename. This results in a much more accurate categorization of files into types like `spec`, `proposal`, `adr`, etc. The output is a detailed plan mapping each file to its new, correct location in the SynthesisFlow structure.

**Phase 3 - Planning**:
Shows you the complete, AI-driven migration plan for your approval. You can review source and target mappings before any files are moved.

**Phase 4 - Backup**:
Creates a timestamped backup directory of your entire `docs/` folder and includes a `rollback.sh` script before any changes are made.

**Phase 5 - Migration**:
Executes the plan, moving files using `git mv` to preserve history and creating the necessary directory structure.

**Phase 6 - LLM-Based Link Updates**:
Uses the Gemini CLI to intelligently identify and correct broken or outdated relative links within migrated files. This LLM-based approach is more robust than simple path recalculation, as it understands document context and can handle edge cases that pattern matching might miss.

**Phase 7 - Validation**:
Verifies that all files were migrated correctly, checks link integrity, and validates the new directory structure.

**Phase 8 - AI-Powered Frontmatter Generation (Optional)**:
For files that lack YAML frontmatter, the script uses the **Gemini CLI** to read the file content and generate rich, `doc-indexer` compliant frontmatter. This includes a suggested `title`, the `type` determined during the analysis phase, and a concise `description` summarizing the document's purpose.

### Step 3: Post-Migration

After successful completion:
- Review the validation report for any warnings.
- Run the `doc-indexer` skill to verify full documentation compliance.
- Commit the migration changes to git.

## Error Handling

### Gemini CLI Issues

**Symptom**: The script fails during the "Analysis" or "Frontmatter Generation" phase with an error related to the `gemini` command.

**Solution**:
- Ensure the `gemini` CLI is installed and in your system's PATH.
- Verify you are authenticated by running `gemini auth`.
- Check for Gemini API outages or network connectivity issues.
- The script has basic fallbacks, but for best results, ensure the Gemini CLI is functional.

### Other Issues

For issues related to permissions, conflicts, or broken links, the script provides detailed error messages and resolution suggestions during its interactive execution. The backup and rollback script is always available for a safe exit.

## Notes

- **AI-Enhanced**: Uses Gemini for intelligent content analysis, not just simple pattern matching.
- **Safe by default**: Creates a full backup with a rollback script before making any changes.
- **Git-aware**: Preserves file history using `git mv`.
- **Interactive**: You review and approve the AI-generated plan before execution.
- **Rich Metadata**: Generates high-quality frontmatter, including titles and descriptions.
- **LLM-Powered Link Correction**: Uses Gemini to intelligently update relative links with context awareness.