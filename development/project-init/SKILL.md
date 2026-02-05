---
name: project-init
description: Use this skill when starting a new project or adding SynthesisFlow to an existing project. Scaffolds the directory structure (docs/specs, docs/changes) and configuration files needed for the spec-driven development workflow.
---

# Project Init Skill

## Purpose

Initialize a new project with the SynthesisFlow directory structure and configuration files. This skill sets up the foundational folders needed for the spec-driven development workflow, creating a standard structure for specifications, change proposals, and documentation.

## When to Use

Use this skill in the following situations:

- Starting a completely new project that will use SynthesisFlow
- Adding SynthesisFlow methodology to an existing project **with no existing documentation**
- Setting up a consistent structure for spec-driven development
- Ensuring project follows SynthesisFlow conventions from the beginning

**Important**: If the project already has documentation in a `docs/` directory, use the **project-migrate** skill instead. It will properly catalog, categorize, and migrate existing documentation into the SynthesisFlow structure while preserving git history and updating links.

## Prerequisites

- Write permissions to the target directory
- Git repository already initialized (recommended but not required)

## Workflow

### Step 1: Assess the Current Project State

Before initializing, determine:
- Is this a brand new project or an existing codebase?
- Does a `docs/` directory already exist?
- If `docs/` exists, does it contain markdown files?
- Where should the SynthesisFlow structure be created?

**Decision Tree**:
- **No docs/ directory**: Proceed with project-init (this skill)
- **Empty docs/ directory**: Proceed with project-init (this skill)
- **docs/ with existing markdown files**: Use **project-migrate** skill instead

The init-project.sh script will automatically detect existing documentation and suggest using project-migrate if appropriate.

### Step 2: Run the Initialization Script

Execute the helper script to create the directory structure:

**For current directory:**
```bash
bash scripts/init-project.sh
```

**For a specific directory:**
```bash
bash scripts/init-project.sh -d /path/to/project
```

The script will create:
- `docs/specs/` - Source-of-truth for approved specifications
- `docs/changes/` - Staging area for proposed changes (Spec PRs)

### Step 3: Verify Structure Creation

Check that the directories were created successfully:
```bash
ls -la docs/
```

Expected output:
```
docs/
├── specs/
└── changes/
```

### Step 4: Initialize Supporting Files (Manual)

After the directory structure is created, consider adding these files:

**Create RETROSPECTIVE.md** (in project root):
```bash
cat > RETROSPECTIVE.md << 'EOF'
# Development Retrospective

This file captures learnings from completed tasks to inform and improve future development work.

## Active Improvements
EOF
```

**Create AGENTS.md** (using agent-integrator skill):
```bash
# Use the agent-integrator skill to create AGENTS.md
bash skills/agent-integrator/scripts/update-agents-file.sh
```

### Step 5: Next Steps

After initialization, guide the user on getting started:

1. **Create first specification**: Use the `spec-authoring` skill to propose the first feature
2. **Set up GitHub integration**: Create GitHub repository if not exists, set up project board
3. **Document the system**: Add initial specs to `docs/specs/` directory
4. **Initialize git tracking**: Ensure new directories are committed to version control

## Error Handling

### Directory Already Exists

**Symptom**: Script reports that directories already exist or initialization appears to do nothing

**Solution**:
- Check if `docs/specs/` and `docs/changes/` already exist
- If they exist, the project is already initialized
- No action needed - the script is idempotent

### Permission Denied

**Symptom**: "Permission denied" when creating directories

**Solution**:
- Verify write permissions to the target directory
- Check if parent directory exists
- Try with appropriate permissions: `sudo` if necessary (rare)

### Wrong Directory Initialized

**Symptom**: Directories created in unexpected location

**Solution**:
- Remove incorrect directories: `rm -rf docs/`
- Re-run with explicit path: `bash scripts/init-project.sh -d /correct/path`
- Always verify current working directory before running

## Directory Structure Explained

### docs/specs/

**Purpose**: Source-of-truth for all approved specifications

**Contents**:
- Approved specification files
- Design documents
- Architecture decisions
- System requirements

**Example structure**:
```
docs/specs/
├── 001-initial-system.md
├── 002-authentication.md
└── feature-name/
    ├── spec.md
    └── design.md
```

### docs/changes/

**Purpose**: Staging area for proposed changes before approval

**Contents**:
- Change proposals in review
- Spec deltas for new features
- Task breakdowns
- Planning documents

**Example structure**:
```
docs/changes/
├── my-feature/
│   ├── proposal.md
│   ├── spec-delta.md
│   └── tasks.md
└── another-feature/
    └── proposal.md
```

**Workflow**: Changes start in `docs/changes/`, get approved via Spec PR, then move to `docs/specs/`

## project-init vs project-migrate

Understanding when to use each skill:

### Use project-init when:
- Starting a **brand new project** from scratch
- Project has **no existing documentation**
- docs/ directory is **empty** or doesn't exist
- You just need the basic SynthesisFlow directory structure

### Use project-migrate when:
- Project has **existing documentation** in docs/ or other locations
- You want to **migrate legacy docs** into SynthesisFlow structure
- You need to **preserve git history** during migration
- Documentation has **relative links** that need updating
- You want **doc-indexer compliant frontmatter** added automatically

### Smooth Handoff

The init-project.sh script automatically detects existing documentation and will:
1. Count markdown files in docs/ (excluding docs/specs/ and docs/changes/)
2. If found, display a recommendation to use project-migrate
3. Show the benefits of using project-migrate over basic initialization
4. Give you the option to continue with project-init or cancel

This ensures you always use the right skill for your situation.

## Notes

- The script is **idempotent** - safe to run multiple times
- Existing directories won't be overwritten or deleted
- The script only creates directories, no files are created automatically
- Consider adding `.gitkeep` files to track empty directories in git
- This is just the directory scaffold - content comes from using other skills
- The structure is intentionally minimal - projects add what they need
- **Detection logic**: The script checks for markdown files in docs/, excluding those already in specs/ or changes/ subdirectories
