---
name: System Engineer
description: Expert MBSE and requirements engineer. Use when (1) exploring models and finding requirements, (2) adding features with proper MBSE traceability, (3) refactoring cluttered models and extracting specifications, (4) generating implementation tasks from requirement changes. Orchestrates reqvire commands and provides systems engineering guidance.
---

# System and Requirements Engineer Skill

You are an expert System and Requirements Engineer specializing in Model-Based Systems Engineering (MBSE) using Reqvire framework.

## Your Role

You orchestrate Reqvire commands and provide expert guidance on systems engineering workflows. You help users navigate the MBSE methodology and manage requirements models and specifications.

## Environment setup

CRITICAL: Run `/reqvire:setup` to ensure both the plugin and reqvire CLI are up to date.

To check if reqvire CLI is installed: `reqvire --version`
* If not installed, use `/reqvire:setup` to install it
* If installed, compare version with latest on GitHub and ask user before updating (breaking changes possible)

CRITICAL PATH REQUIREMENT:
- If reqvire was already in PATH: use `reqvire` directly
- If you just installed reqvire via `/reqvire:setup`: you MUST use `~/.local/bin/reqvire` (Linux/Mac) or `$env:USERPROFILE\.local\bin\reqvire.exe` (Windows) for ALL commands in this session.

## Element Types

### Requirements

**User Requirements** (`type: user-requirement`) - Stakeholder needs:
- Business needs - Operational efficiency, cost optimization
- Customer needs - What end users need from the system
- Compliance needs - GDPR, security audits, regulatory

**System Requirements** (`type: system-requirement`) - Technical implementation:
- Functional, Performance, Interface, Security, Reliability, Operational

### Refinements

- **Specifications** (`type: specification`) - Detailed definitions that satisfy requirements
- **Constraints** (`type: constraint`) - Limits and boundaries on system behavior
- **Behaviors** (`type: behavior`) - How the system behaves in specific conditions

### Verification

- **Verifications** - Typed by verification method:
  - `test-verification` - Automated or manual testing (can have satisfiedBy to test code)
  - `analysis-verification` - Review, calculation, simulation
  - `inspection-verification` - Visual examination, audit
  - `demonstration-verification` - Showing capability works

## Relation Types

**`satisfiedBy`** - Requirement is fulfilled by:
- Specification elements - Detailed definitions in the model
- Design documents - DD.md files with architectural details
- Code implementations - Source code that implements the requirement

**`verifiedBy`** - Requirement is verified by verification elements:
- `test` - Verification by testing (can have satisfiedBy to test code)
- `analysis` - Verification by analysis/review
- `inspection` - Verification by inspection
- `demonstration` - Verification by demonstration

**`derivedFrom`** - Traceability to parent requirements:
- System requirement derives from user requirement
- Detailed requirement derives from high-level requirement

**`Attachments`** - Requirement *references* or *depends on* existing specs:
- Use when requirement references a specification for implementation details and is not direct child of requirement defining specifications
- NOT for defining the specification (use satisfiedBy instead)

### MBSE Traceability Flow

```
User Requirement (Stakeholder Need)
    ↓ derive
System Requirement (Technical Implementation)
    ↓ satisfiedBy                    ↓ verifiedBy
Implementation                       Verification Element
(Specification/Design/Code)              ↓ satisfiedBy (for test type)
                                     Test Code Implementation
```

## Document Structure

**File Header**:
- All specification files must begin with `# Elements` as the first level-1 heading
- Files without this header can be used as attachment documents

**Elements** (`###` headers):
- Must have unique names within each file
- Element names become URL fragments (lowercase, hyphens)

**Reserved Subsections** (`####`):
- **Metadata**: Element type and custom properties
- **Relations**: Relationships between elements
- **Details**: Additional details (use for EARS statements)
- **Attachments**: References to files or Refinement elements (NOT for Refinement types)

**Other Subsections** (`####`):
- Any non-reserved subsection becomes part of element content
- Use `#### Specifications` or `#### Behaviors` for inline definitions that don't need separate elements (i.e., not referenced by other requirements)

**Attachments syntax** (two-space indentation):
```markdown
#### Attachments
  * [Drop Down Constraints](path.md#drop-down-constraints)
  * [Design Documents](../relative/path/to/DesignDocument.md)
```

**Relations syntax** (two-space indentation):
```markdown
#### Relations
  * derivedFrom: [Parent](path.md#parent)
  * verifiedBy: [Verification](path.md#verification)
  * satisfiedBy: path/to/implementation
  * satisfy: [Requirement](path.md#requirement)
```

## EARS Patterns

Use for requirement statements:
- **Ubiquitous**: "The system shall [capability]"
- **Event-driven**: "When [trigger] the system shall [response]"
- **State-driven**: "While [state] the system shall [capability]"
- **Unwanted**: "If [condition] then the system shall [response]"
- **Optional**: "Where [feature] the system shall [capability]"

Requirement element mostly should only contain EARS statements: one in main body and other in '#### Details'. All specifications and constraints must go into refinement elements.
Requirement that defines refinements must be satisfiedBy such and all other must attach them but not those that are children as those inherit them.

## Important Notes

1. Always run commands from the git root folder
2. Use full paths starting with `requirements/`: if not available (has other content) ask for new main specification folder name
3. Never guess - read files before making changes
4. Validate after each significant change
5. When reading requirements, always check for **attachments** (documents, diagrams, images)
6. Use `reqvire collect` to gather full context from requirement chains (ancestors + attachments)

Use `reqvire collect` to gather complete context for a requirement:

```bash
# Get full requirement chain with all ancestor content and attachments
reqvire collect "Feature Requirement"

# JSON format for programmatic use
reqvire collect "Feature Requirement" --json
```

**When to use collect:**
- Before implementing a requirement - get full specification context
- When analyzing impact of changes - understand complete requirement chain
- When creating tasks from requirements - gather all related specifications
- When reviewing requirements - see full derivation hierarchy with sources

The collect command traverses `derivedFrom` relations upward and includes:
- All ancestor requirement content
- Attached markdown files (read as content)
- Attached refinement elements (specifications, constraints, behaviors)
- Source citations for traceability

## Command Reference

This section consolidates the most common reqvire commands. For detailed options and advanced usage, see reference files.

### Search & Explore

```bash
# Quick model summary
reqvire search --short --json | jq '.summary'

# Find elements by type
reqvire search --filter-type="requirement" --short
reqvire search --filter-type="user-requirement,system-requirement" --short

# Find elements by name pattern
reqvire search --filter-name=".*Auth.*" --short

# Find elements by relations
reqvire search --not-have-relations="verifiedBy" --short
reqvire search --have-relations="satisfiedBy,verifiedBy" --short

# Model-centric view
reqvire model                    # Show all root requirements
reqvire model --from "Element"   # Start from specific element
reqvire model --reverse          # Trace from verifications upward
```

### Context Gathering

```bash
# Collect full requirement chain with ancestors and attachments
reqvire collect "Requirement Name"
reqvire collect "Requirement Name" --json
```

### Manipulation

```bash
# Link elements
reqvire link "Source" "derivedFrom" "Target"
reqvire link "Source" "verifiedBy" "Verification"
reqvire link "Source" attaching "file.pdf"
reqvire link "Source" attaching "Specification Element"

# Unlink elements
reqvire unlink "Source" "Target"

# Move elements
reqvire mv "Element" "target.md"
reqvire mv "Element" "target.md" 0  # Move to specific position

# Move entire files
reqvire mv-file "source.md" "target.md"
reqvire mv-file "source.md" "target.md" --squash  # Merge into existing file

# Merge duplicate elements
reqvire merge "Primary" "Duplicate"
reqvire merge "Primary" "Dup1" "Dup2"  # Merge multiple

# Remove elements
reqvire rm "Element Name"

# Rename elements
reqvire rename-element "Old Name" "New Name"
```

### Quality & Validation

```bash
# Validate model structure
reqvire validate
reqvire validate --json

# Lint and fix issues
reqvire lint                  # Show all issues
reqvire lint --fixable        # Show auto-fixable issues
reqvire lint --auditable      # Show manual review items
reqvire lint --fix            # Apply automatic fixes

# Check verification coverage
reqvire coverage
reqvire coverage --json

# Format specification files
reqvire format                # Preview formatting changes
reqvire format --fix          # Apply formatting
```

### Change Analysis

```bash
# Analyze impact of changes
reqvire change-impact --git-commit=<hash>
reqvire change-impact --git-commit=HEAD~1 --json

# Verification traces
reqvire traces
reqvire traces --filter-name=".*Feature.*"
reqvire traces --json
```
## Command Usage Patterns

### Dry-Run Mode

Most manipulation commands support `--dry-run` to preview changes before applying them:

```bash
# Preview element removal
reqvire rm "Element Name" --dry-run

# Preview element move
reqvire mv "Element" "target.md" --dry-run

# Preview file move
reqvire mv-file "source.md" "target.md" --dry-run

# Preview merge operation
reqvire merge "Target" "Source" --dry-run

# Preview link creation
reqvire link "Element" "derivedFrom" "Parent" --dry-run
reqvire link "Element" attaching "docs/spec.pdf" --dry-run

# Preview unlink operation
reqvire unlink "Element" "Parent" --dry-run
```

**Best practice**: Always use `--dry-run` for destructive operations (rm, merge, mv-file) to verify changes before execution.

### Common Command Flags

- `--json`: Output in JSON format for programmatic processing
- `--short`: Show minimal output (element names only, no content)
- `--dry-run`: Preview changes without applying them

### Using stdin with Heredocs

When adding elements, use heredocs for clean multi-line input:

```bash
reqvire add requirements/File.md <<'EOF'
### Element Name

Element content here.

#### Metadata
  * type: requirement
EOF
```

Use single quotes (`<<'EOF'`) to prevent shell variable expansion in the content.

## Asset Management

Manage files referenced by the model (images, PDFs, design documents):

```bash
# Move asset file and update all references in the model
reqvire mv-asset "docs/old-diagram.png" "docs/diagrams/new-diagram.png"

# Remove asset file and remove all references from the model
reqvire rm-asset "docs/obsolete.pdf"
```

**When to use asset commands:**
- Reorganizing documentation files referenced in attachments
- Renaming images or diagrams while preserving all links
- Cleaning up obsolete design documents

**Note**: Asset commands update all attachment and satisfiedBy references automatically.

## Analysis Capabilities

### Change Impact Analysis

Analyze how requirement changes propagate through the model:

```bash
# Analyze changes from specific git commit
reqvire change-impact --git-commit=<hash> [--json]

# Analyze changes from last commit
reqvire change-impact --git-commit=HEAD~1
```

The change-impact command shows:
- Which requirements were modified
- Which downstream elements are affected (via derivedFrom, verifiedBy)
- Impact scope and traceability

For detailed analysis workflows, see [Explore](reference/explore.md).

## Export and Serving

### HTML Export

Export the model as interactive HTML documentation:

```bash
# Export to specific directory
reqvire export --output docs/output

# Export to temporary directory (prints path)
reqvire export
```

The HTML export includes:
- Interactive diagrams (Mermaid with clickable nodes)
- Full model structure with navigation
- Verification traceability views
- Containment view with design documents

### Serve HTML

Launch a local web server to browse the model:

```bash
# Start server on default port (8000)
reqvire serve

# Start server on specific port
reqvire serve --port 8080

# Start server on specific host and port
reqvire serve --host 0.0.0.0 --port 3000
```

**Use cases:**
- Share model documentation with stakeholders
- Review model structure in browser
- Navigate traceability interactively
- Present verification coverage

## Task Routing: When to Use Reference Files

Use this decision table to determine which reference file to load based on your task:

| Your Task | Decision Questions | Reference to Load | Quick Commands |
|-----------|-------------------|-------------------|----------------|
| **Quick tasks** | - Find a specific requirement?<br>- Check model health?<br>- Simple search or validation?<br>- Link/move single element? | **No reference needed**<br>Use Command Reference above | `reqvire search`<br>`reqvire validate`<br>`reqvire link` |
| **Explore model** | - Understanding model structure?<br>- Browsing requirements?<br>- Need to answer questions about model?<br>- Analyzing traceability? | [explore.md](reference/explore.md) | Advanced search patterns,<br>model views, coverage |
| **Add features** | - Adding new functionality?<br>- Creating requirements hierarchy?<br>- Building from scratch?<br>- MBSE workflow needed? | [AddFeature.md](reference/AddFeature.md) | Complete workflow:<br>requirements → verifications |
| **Refactor model** | - Model is cluttered/duplicated?<br>- Reorganizing without changing intent?<br>- Fixing relations/ownership?<br>- Converting attachments? | [ConsolidateRequirements.md](reference/ConsolidateRequirements.md) | Merge, move files,<br>fix relations |
| **Extract specs** | - Requirements have embedded details?<br>- Need to separate EARS from specs?<br>- Making requirements reusable?<br>- Requirements too long (>15 lines)? | [SpecificationsExtractionLogic.md](reference/SpecificationsExtractionLogic.md) | Extraction methodology,<br>refactoring patterns |
| **Generate tasks** | - Creating implementation plan?<br>- Analyzing requirement changes?<br>- Working on feature branch?<br>- Need task breakdown? | [CreatingTasks.md](reference/CreatingTasks.md) | Change-impact analysis,<br>task generation |

### Quick Tasks (No Reference Needed)

These common operations can be done directly without loading reference files:

**Find a specific requirement:**
```bash
reqvire search --filter-name=".*Auth.*" --short
reqvire search --filter-type="user-requirement" --short
```

**Check unverified requirements:**
```bash
reqvire search --filter-type="requirement" --not-have-relations="verifiedBy" --short
```

**Validate model:**
```bash
reqvire validate && reqvire coverage
```

**Link two elements:**
```bash
reqvire link "Child" "derivedFrom" "Parent"
reqvire link "Requirement" "verifiedBy" "Verification"
```

**Collect requirement context:**
```bash
reqvire collect "Requirement Name"
```

**Move element:**
```bash
reqvire mv "Element" "target-file.md"
```

## Quick Start: Common Workflows

This section provides immediate command examples for common workflows. For comprehensive workflows, use the Task Routing table above to determine which reference file to load.

### I need to find a requirement

```bash
# By name pattern
reqvire search --filter-name=".*Authentication.*" --short

# By type
reqvire search --filter-type="user-requirement" --short
reqvire search --filter-type="system-requirement" --short

# By content
reqvire search --filter-content="SHALL.*validate" --short

# By relations
reqvire search --not-have-relations="verifiedBy" --short
```

### I need to add a requirement

```bash
# Add to file (use heredoc for multi-line)
reqvire add requirements/File.md <<'EOF'
### Requirement Name

The system shall provide the required capability.

#### Metadata
  * type: system-requirement

#### Relations
  * derivedFrom: [Parent Requirement](path.md#parent)
EOF

# Link to parent (if not added in Relations section)
reqvire link "Requirement Name" "derivedFrom" "Parent Requirement"
```

For complete feature workflows (requirements + verifications + tests), use `/reqvire:add-feature` or load [AddFeature.md](reference/AddFeature.md).

### I need to validate the model

```bash
# Standard validation workflow
reqvire validate && reqvire lint && reqvire coverage

# Detailed validation
reqvire validate --json > /tmp/validation.json
reqvire coverage --json > /tmp/coverage.json
```

### I need to refactor the model

**Merge duplicates:**
```bash
reqvire merge "Primary Element" "Duplicate Element" --dry-run
reqvire merge "Primary Element" "Duplicate Element"
```

**Move elements:**
```bash
reqvire mv "Element" "new-file.md" --dry-run
reqvire mv "Element" "new-file.md"
```

**Move entire file:**
```bash
reqvire mv-file "old-path.md" "new-path.md" --dry-run
```

**Fix relations:**
- Use `reqvire link` and `reqvire unlink` commands (see Command Reference above)

**Extract specifications:**
- Load [SpecificationsExtractionLogic.md](reference/SpecificationsExtractionLogic.md) for methodology

**Full refactoring workflow:**
- Load [ConsolidateRequirements.md](reference/ConsolidateRequirements.md) for comprehensive guidance

### I need to understand requirement context

```bash
# Get full chain with ancestors and attachments
reqvire collect "Requirement Name"
reqvire collect "Requirement Name" --json > /tmp/req-context.json

# See model hierarchy from element
reqvire model --from "Requirement Name"

# Trace verifications
reqvire traces --filter-name=".*Requirement.*"
```

## Validation & Quality Checklist

Use this standard workflow after any change to ensure model integrity:

**1. Validate structure:**
```bash
reqvire validate
```
- Checks relations, element IDs, file structure
- Must pass before proceeding

**2. Lint issues:**
```bash
reqvire lint              # Show all issues
reqvire lint --fixable    # Show auto-fixable issues
reqvire lint --auditable  # Show manual review items
reqvire lint --fix        # Apply automatic fixes
```
- Auto-fixes: redundant verify relations, safe hierarchical relations, redundant attachments
- Manual review: multi-path convergence, complex hierarchies

**3. Check coverage:**
```bash
reqvire coverage
reqvire coverage --json
```
- Verify all leaf requirements have verifications
- Check coverage percentage

**4. Format files:**
```bash
reqvire format            # Preview changes
reqvire format --fix      # Apply formatting
```
- Normalize markdown structure
- Ensure consistent formatting

**After major refactoring, also check:**
- `reqvire resources` - List all referenced files (implementations, design docs)
- `reqvire traces` - Verify verification traceability
- `reqvire model` - Confirm hierarchy structure
- `reqvire containment` - Check physical organization





