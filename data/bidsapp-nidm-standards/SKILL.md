---
name: bidsapp-nidm-standards
description: Standards and tools for creating, maintaining, and refactoring NIDM-integrated BIDSapps that run through BABS. Use when working with sensein BIDSapp repositories (freesurfer_bidsapp, mriqc-nidm_bidsapp, ants_bidsapp) or creating new BIDSapps. Helps with repository structure consistency, NIDM integration patterns, CLI argument standardization, BIDS-compliant output structures, and BABS configuration.
compatibility: "Designed for code editing and development tasks. Works with Python, Docker, Singularity/Apptainer, and neuroimaging pipeline development. Suitable for both claude.ai and Claude Code environments."
---

# BIDSapp NIDM Standards

Standardize BIDSapp repositories with NIDM integration for consistent structure, output formats, and BABS compatibility.

## Overview

This skill defines standards for BIDSapp repositories that:
1. Process neuroimaging data (FreeSurfer, MRIQC, ANTs, etc.)
2. Integrate NIDM (Neuroimaging Data Model) outputs
3. Run through BABS (BIDS App Bootstrap) on HPC clusters
4. Maintain consistent structure across multiple analysis tools

## Core Standards

### Repository Structure

All BIDSapp repos follow this structure:

```
<bidsapp_name>/
├── src/
│   ├── <analysis_name>/          # Main analysis code
│   │   ├── __init__.py
│   │   ├── run.py               # Entry point
│   │   └── <analysis>_runner.py
│   └── nidm/                     # NIDM conversion (analysis-specific)
│       ├── __init__.py
│       ├── nidm_converter.py
│       └── data/
├── tests/
│   ├── test_<analysis>.py
│   └── test_nidm.py
├── examples/
├── Dockerfile
├── Singularity
├── setup.py
├── requirements.txt
├── VERSION
└── README.md
```

### CLI Arguments

**Standard BIDS arguments** (required):
- `bids_dir` - Input BIDS dataset path
- `output_dir` - Output directory path  
- `analysis_level` - Must be "participant"
- `--participant-label` - Subject ID(s) without "sub-" prefix
- `--session-label` - Session ID(s) without "ses-" prefix (optional)

**Standard NIDM arguments** (required):
- `--nidm-input-dir` - Path to existing NIDM files directory
- `--skip-nidm` - Skip NIDM conversion
- `--skip-<analysis>` - Skip analysis if already run (e.g., `--skip-freesurfer`, `--skip-mriqc`, `--skip-ants`)

**Analysis-specific arguments** (optional):
- Add as needed for specific analysis tools (e.g., `--fs-license` for FreeSurfer, `--nprocs` for MRIQC)

See `references/cli_arguments.md` for complete specifications.

### Output Structure

**BIDS-compliant derivatives structure**:

```
<output_dir>/
└── <bidsapp_name>/              # e.g., freesurfer_nidm, mriqc_nidm, ants_nidm
    ├── dataset_description.json
    ├── <analysis>/              # e.g., freesurfer, mriqc, ants
    │   ├── dataset_description.json
    │   └── sub-{id}/
    │       └── ses-{session}/   # Optional
    │           └── [analysis outputs]
    └── nidm/
        ├── dataset_description.json
        └── sub-{id}/
            └── ses-{session}/   # Optional
                └── sub-{id}_ses-{session}.ttl
```

### NIDM Integration Workflow

The standard NIDM workflow:

1. **Copy existing NIDM file** from `--nidm-input-dir` to output NIDM folder
2. **Run analysis** (unless `--skip-<analysis>`)
3. **Extract metrics** from analysis outputs
4. **Integrate into NIDM file** (overwrite the copied file)

The NIDM input directory should contain:
- Single `nidm.ttl` file at root, OR
- Per-subject files: `sub-{id}/ses-{session}/sub-{id}_ses-{session}.ttl`

For complete NIDM integration specifications, see `references/nidm_integration.md`.

## Common Workflows

### Check Repository Compliance

Verify a repo follows standards:

1. **Directory structure**: Compare against `references/repo_structure.md`
2. **CLI arguments**: Check `src/<analysis>/run.py` for standard args
3. **Output structure**: Verify code creates `<bidsapp_name>/{<analysis>, nidm}/` pattern
4. **NIDM integration**: Ensure copy→run→integrate workflow exists
5. **Containers**: Check Dockerfile/Singularity follow `references/container_patterns.md`

### Refactor Existing Repository

To update a repo to match standards:

1. **Review**: Compare current structure against `references/repo_structure.md`
2. **Reorganize**: Move files to match standard layout
3. **Update CLI**: Add missing standard arguments
   - Ensure `--participant-label`, `--session-label`
   - Add `--nidm-input-dir`, `--skip-nidm`, `--skip-<analysis>`
4. **Fix output structure**: Update code to create proper BIDS derivatives
5. **Update NIDM workflow**: Implement copy→run→integrate pattern
6. **Align containers**: Update Dockerfile/Singularity
7. **Standardize setup.py**: Match template configuration
8. **Update tests**: Ensure test coverage for all components

### Create New BIDSapp

To create a new NIDM-integrated BIDSapp from scratch:

1. **Initialize structure**: Copy `assets/template/` directory
2. **Rename components**: Replace `<analysis>` placeholders throughout
3. **Implement analysis**: Code `src/<analysis>/<analysis>_runner.py`
4. **Implement NIDM**: Code `src/nidm/nidm_converter.py` for this analysis
5. **Build containers**: 
   - Create Dockerfile following `references/container_patterns.md`
   - Create Singularity file for HPC deployment
6. **Add tests**: Follow standard test patterns
7. **Generate BABS config**: Use `references/babs_config.md` template
8. **Document**: Update README with usage examples

### Update Standards Across All Repos

When changing standards that affect all BIDSapps:

1. **Update this skill**: Modify reference documentation first
2. **Identify affected repos**: List all BIDSapps needing updates
3. **Update each repo**:
   - NIDM converter pattern changes → `src/nidm/nidm_converter.py`
   - CLI changes → `src/<analysis>/run.py`
   - Output structure changes → Runner and output code
   - Container changes → Dockerfile, Singularity
4. **Test with BABS**: Ensure all repos work with BABS workflow
5. **Update BABS configs**: Regenerate YAML files if needed

## Reference Documentation

All reference files provide detailed specifications:

- `references/repo_structure.md` - Complete repository structure template with explanations
- `references/nidm_integration.md` - Full NIDM workflow, file formats, integration patterns
- `references/babs_config.md` - BABS YAML configuration template with examples
- `references/cli_arguments.md` - Complete CLI argument specifications and validation
- `references/container_patterns.md` - Docker and Singularity build patterns
- `references/testing_patterns.md` - Test structure and coverage requirements

## Container Standards

Both Dockerfile and Singularity should:
- Use analysis tool base images where available (e.g., `vnmd/freesurfer_8.0.0`)
- Install Python package via setup.py
- Set appropriate entry points
- Support both Docker and Apptainer/Singularity execution
- Follow BIDS App containerization best practices

See `references/container_patterns.md` for complete specifications.

## Testing Standards

Standard test coverage:
- CLI argument parsing and validation
- BIDS input dataset validation
- Analysis execution (with mock or example data)
- NIDM conversion correctness
- Output structure validation
- Container build and execution

Use pytest with fixtures for test data. See `references/testing_patterns.md`.

## BABS Integration

All BIDSapps must work with BABS for HPC deployment. Key requirements:

- Accept standard BIDS App CLI arguments
- Output to BIDS derivatives structure
- Support DataLad input datasets
- Work with Singularity/Apptainer containers
- Include proper resource requirements

Generate BABS YAML configs using `references/babs_config.md` template.
