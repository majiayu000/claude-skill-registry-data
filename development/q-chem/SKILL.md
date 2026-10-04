---
name: q-chem
description: Build, review, debug, and automate Q-Chem quantum chemistry workflows. Use when working with Q-Chem input files, $rem section, job types, basis sets, SCF convergence, geometry optimization, frequency calculations, solvent models, or Q-Chem execution and restart issues.
metadata:
  skill-author: MindSpore Science Team
---

# HPC Q-Chem Skill

Treat Q-Chem as a staged quantum-chemistry workflow built around a valid input deck with modular section structure.

## Quick Start

### Typical Workflow
1. Write input file ($rem, $molecule sections) —see [references/01-input-file-structure.md](references/01-input-file-structure.md)
2. Select method and basis set —see [references/02-method-selection.md](references/02-method-selection.md)
3. Choose job type (SP, Opt, Freq) —see [references/03-job-types.md](references/03-job-types.md)
4. Handle SCF convergence if needed —see [references/04-scf-convergence.md](references/04-scf-convergence.md)
5. Set up geometry, charge, and multiplicity —see [references/05-geometries-charges.md](references/05-geometries-charges.md)
6. Configure restart for multi-step workflows —see [references/06-restart-workflows.md](references/06-restart-workflows.md)
7. Add solvent model if needed —see [references/07-solvent-models.md](references/07-solvent-models.md)
8. Submit to HPC cluster —see [references/08-cluster-execution.md](references/08-cluster-execution.md)
9. Handle errors —see [references/error-recovery.md](references/error-recovery.md)

## Skill Map

```
User Requirements
├─ Input Deck Authoring
│ ├─ $rem section (job control keywords) →01-input-file-structure.md
│ ├─ $molecule section (charge/mult/geometry) →01-input-file-structure.md
│ ├─ $basis section (custom basis) →01-input-file-structure.md
│ └─ Method selection (HF, DFT, MP2, CCSD(T)) →02-method-selection.md
├─ Job Types
│ ├─ Single Point (SP) →03-job-types.md
│ ├─ Geometry Optimization (Opt) →03-job-types.md
│ ├─ Frequency (Freq) →03-job-types.md
│ ├─ Excited States (TDDFT, CIS) →03-job-types.md
│ └─ Properties (NMR, dipole) →03-job-types.md
├─ SCF & Convergence
│ ├─ SCF convergence strategies →04-scf-convergence.md
│ └─ Guess methods (SAD, Core, Read) →04-scf-convergence.md
├─ Solvent Effects
│ └─ PCM, SM8, SMD models →07-solvent-models.md
├─ Restart & Workflows
│ ├─ Reading previous job →06-restart-workflows.md
│ └─ Multi-job batch files →06-restart-workflows.md
│ └─ Plot files and Fchk →06-restart-workflows.md
└─ HPC Cluster Execution
   ├─ SLURM/PBS job scripts →08-cluster-execution.md
   ├─ MPI and OpenMP parallelization →08-cluster-execution.md
   └─ Scratch directory management →08-cluster-execution.md
```

## Reference Documents

| Document | Content |
|----------|---------|
| [references/01-input-file-structure.md](references/01-input-file-structure.md) | Input file anatomy: $comment, $molecule, $rem, $basis sections |
| [references/02-method-selection.md](references/02-method-selection.md) | HF, DFT functionals (B3LYP, ωB97X-D, M06-2X), basis sets, MP2, CCSD(T) |
| [references/03-job-types.md](references/03-job-types.md) | SP, Opt, Freq, TDDFT, CIS, property calculations |
| [references/04-scf-convergence.md](references/04-scf-convergence.md) | SCF guess methods, DIIS, GDM, level-shifting, stability checks |
| [references/05-geometries-charges.md](references/05-geometries-charges.md) | Charge/mult format, Cartesian/Z-matrix, symmetry |
| [references/06-restart-workflows.md](references/06-restart-workflows.md) | Reading MOs, batch jobs, plot files |
| [references/07-solvent-models.md](references/07-solvent-models.md) | PCM, SM8, SMD; solvent selection |
| [references/08-cluster-execution.md](references/08-cluster-execution.md) | SLURM/PBS scripts, MPI/OpenMP, scratch directory |
| [references/error-recovery.md](references/error-recovery.md) | Input, SCF, optimization, frequency, runtime errors; recovery workflow |

## Key Decision Points

| Question | Guide | Summary |
|----------|-------|---------|
| Single point, opt, or freq? | [03-job-types.md](references/03-job-types.md) | SP, Opt, Freq job types |
| Which method and basis? | [02-method-selection.md](references/02-method-selection.md) | HF, DFT, MP2, CCSD(T) with appropriate basis |
| SCF convergence issues? | [04-scf-convergence.md](references/04-scf-convergence.md) | SCF_GUESS, MAX_SCF_CYCLES, or GDM |
| Solvent effects needed? | [07-solvent-models.md](references/07-solvent-models.md) | SOLVENT_MODEL = PCM or SMD |
| Need to restart? | [06-restart-workflows.md](references/06-restart-workflows.md) | Read MOs or batch jobs |

## Guardrails

- Do not invent Q-Chem $rem keywords —consult [01-input-file-structure.md](references/01-input-file-structure.md)
- Do not treat charge and multiplicity as cosmetic metadata —they must match the electron count.
- Do not run restart-sensitive workflows without proper file handling —see [06-restart-workflows.md](references/06-restart-workflows.md)
- Do not copy $rem sections from unrelated systems without checking method, basis, and job intent.
- Do not run Freq on a non-optimized geometry.
- Do not mix incompatible job types (e.g., Opt with TDDFT requires specific settings).

## Outputs

Always report:

- job type (SP, Opt, Freq, TDDFT, etc.)
- method and basis selection
- charge and multiplicity
- restart policy if applicable
- expected key outputs (.out, .fchk, plot files) and next stage

## Template Files

Template files in `assets/templates/` are ready-to-use starting scaffolds that can be copied and modified:

| Template | Type | Use Case | Reference |
|----------|------|---------|-----------|
| [assets/templates/sp_water.in](assets/templates/sp_water.in) | Input (.in) | Single point energy of water | [01-input-file-structure.md](references/01-input-file-structure.md), [02-method-selection.md](references/02-method-selection.md) |
| [assets/templates/opt_freq_water.in](assets/templates/opt_freq_water.in) | Input (.in) | Geometry optimization + frequency | [03-job-types.md](references/03-job-types.md), [06-restart-workflows.md](references/06-restart-workflows.md) |
| [assets/templates/qchem-slurm.sh](assets/templates/qchem-slurm.sh) | Batch script | SLURM submission for Q-Chem | [08-cluster-execution.md](references/08-cluster-execution.md) |

## Error Recovery

Consult [references/error-recovery.md](references/error-recovery.md) for structured diagnosis of:

- Input file errors ($rem, $molecule, $basis)
- SCF convergence failures
- Optimization failures
- Frequency calculation errors
- Restart and file issues
- Runtime errors (memory, scratch, segmentation)