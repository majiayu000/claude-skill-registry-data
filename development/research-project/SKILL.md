---
name: research-project
description: This skill should be used when initializing a new bioinformatics research project, checking project status, updating project phase, or getting research best practices guidance. Triggered by requests like "initialize project", "check status", "update phase", or "research best practices".
---

# Research Project Management

## Overview

Provides comprehensive project steering and management for bioinformatics research projects. Handles initialization, phase tracking, status monitoring, and best practices guidance.

## Core Capabilities

### 1. Project Initialization

Initialize a new research project structure using `scripts/init_project.py`.

**When to use**: When starting a new research project or setting up a standardized structure.

**Workflow**:
1. Confirm project location (current directory or specified path)
2. Run initialization script from the plugin directory:
   ```bash
   python "${CLAUDE_PLUGIN_ROOT}/scripts/init_project.py" --path /path/to/target/project
   ```
   **Important**: Use `${CLAUDE_PLUGIN_ROOT}` to reference the plugin's installation directory. The `--path` argument specifies where the project structure will be created.
3. Verify created structure
4. Guide user to next steps (edit STEERING.md, create first experiment)

**Created structure**:
```
project/
├── STEERING.md                             # Project progress tracker
├── notebook/
│   ├── tasks.md                            # Task management
│   ├── labnote/
│   │   ├── Exp00_TEMPLATE_labnote.ipynb    # Jupyter template
│   │   └── Exp00_TEMPLATE_labnote.md       # Markdown template
│   ├── report/
│   │   └── Exp00_TEMPLATE_report.md        # Report template
│   └── knowledge/                          # Reusable procedures
├── inbox/                                  # User input files
│   └── archive/                            # Processed files
├── data/raw/                               # Raw data (gitignored)
└── results/                                # Outputs (gitignored)
```

**Command**: `/research-init`

### 2. Status Checking

Check current project status, phase, and next actions.

**When to use**: When user asks "what's the status?", "where are we?", or "what should I do next?"

**Workflow**:
1. Read `STEERING.md` for current phase and priorities
2. Read `notebook/tasks.md` for experiment progress
3. Summarize:
   - Current phase
   - Active experiments
   - Completed milestones
   - Next recommended actions

**Command**: `/research-status`

### 3. Phase Management

Guide transitions between research phases using `references/phases.md`.

**Research phases**:
- **Planning**: Define research questions and hypotheses
- **Exploration**: Initial data analysis and hypothesis refinement
- **Execution**: Systematic experimentation
- **Integration**: Synthesize results into reports
- **Publication**: Prepare manuscripts and documentation

**When to use**: When project reaches a natural transition point or user requests phase update.

**Workflow**:
1. Review current phase from STEERING.md
2. Check phase completion criteria from `references/phases.md`
3. If criteria met, suggest phase transition
4. Update STEERING.md with new phase and priorities

### 4. Best Practices Guidance

Provide research best practices from `references/best-practices.md` and `references/quality-standards.md`.

**When to use**: When user needs guidance on:
- Hypothesis formulation
- Experimental design
- Scientific writing
- Data interpretation
- Quality standards

**Key principles**:
- **Hypothesis-driven**: Always start with testable hypotheses
- **Reproducibility**: Document everything for reproducibility
- **Fact/interpretation separation**: Keep observations separate from conclusions
- **Progressive disclosure**: Structure information hierarchically

### 5. Content Review

Proactively review user-created content against quality standards.

**When to use**: When user presents:
- Draft reports or conclusions
- Lab notebook entries
- Any scientific claims or findings

**Action**: Review content against `references/quality-standards.md` checklist:

1. **Fact vs. Interpretation Check**:
   - Are observations (facts) clearly separated from interpretation?
   - Are claims properly qualified with uncertainty level?
   - Are conclusions supported by cited evidence?

2. **Evidence Traceability Check**:
   - Does each claim link to a notebook/figure/table?
   - Are statistics complete (test name, n, effect size, p-value)?
   - Are figure references valid and accessible?

3. **Reproducibility Check**:
   - Are methods detailed enough for replication?
   - Are software/data versions specified?
   - Are random seeds documented?

**Output**: Provide constructive feedback with specific improvement suggestions.

**Example feedback**:
```markdown
### Review Feedback

**Fact/Interpretation Issues**:
- Line 23: "Gene X regulates pathway Y" - This is interpretation, not fact.
  Suggest: "Gene X expression correlated with pathway Y activity (r=0.85, p<0.01)"

**Missing Evidence Links**:
- Finding 2 has no figure reference. Add: "(Figure 2B, Exp03_analysis.ipynb)"

**Statistics Incomplete**:
- Effect size missing for differential expression claim. Add fold-change and CI.
```

## Resources

### scripts/

- `init_project.py`: Project initialization script (executable)

### commands/

- `research-init.md`: Project initialization command (`/research-init`)
- `research-status.md`: Status checking command (`/research-status`)

### references/

- `phases.md`: Detailed phase definitions and transition criteria
- `best-practices.md`: Hypothesis-driven research guidelines
- `quality-standards.md`: Scientific quality standards (fact/interpretation/conclusion separation)

## Usage Notes

- Always confirm project path before initialization
- Check for existing files to avoid overwriting
- Guide users through post-initialization steps
- Proactively suggest phase transitions when criteria are met
- Reference best practices when users show uncertainty
