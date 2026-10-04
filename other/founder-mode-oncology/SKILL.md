---
name: founder-mode-oncology
category: healthcare
description: >
  Personalized cancer treatment navigation — maximal diagnostics, parallel therapy, therapeutic development, structure-based protein design. Use when (1) researching cancer treatments or combinations, (2) designing diagnostic strategies, (3) evaluating neoantigen vaccines or radioligand therapies, (4) navigating FDA expanded access or IRB processes, (5) interpreting ctDNA/MRD data, (6) building bioinformatics pipelines, (7) scRNA-seq target discovery, (8) AlphaFold/RFdiffusion/ProteinMPNN for neoantigen validation or de novo binder design, (9) patient advocacy. Keywords — cancer, oncology, neoantigen, vaccine, immunotherapy, radioligand, ctDNA, scRNA-seq, FAP, AlphaFold, RFdiffusion, ProteinMPNN, personalized medicine.
---

# Founder Mode Oncology

Systematic framework for navigating personalized cancer treatment, generalized from Sid Sijbrandij's osteosarcoma case (2022-2026). Transforms the ad-hoc "billionaire with a team" approach into a reproducible methodology using open-source tools and structured decision-making.

## The Three-Pillar Framework

### Pillar 1: Maximal Diagnostics

Run every available diagnostic modality to build a complete molecular picture. Standard clinical panels miss non-obvious targets.

**Minimum diagnostic stack (in priority order):**

1. **Genomics**: WGS + WES (tumor/normal paired) — somatic mutations, CNV, structural variants
2. **Transcriptomics**: Bulk RNA-seq + scRNA-seq (tumor + PBMCs) — gene expression, immune landscape, non-obvious targets
3. **Liquid biopsy**: ctDNA (tumor-informed, e.g. Signatera) + methylation-based (e.g. Northstar) — real-time monitoring
4. **Functional testing**: Organoid drug testing + mass response assays — empirical drug sensitivity
5. **Imaging**: Standard (CT/MRI) + novel PET tracers (68Ga-FAP, 68Ga-B7H3) — target validation
6. **Flow cytometry**: B/T cell subsets — immune status tracking

**Critical insight**: scRNA-seq reveals targets that standard panels miss. In the reference case, scRNA-seq identified FAP overexpression in osteosarcoma — invisible to gene panels and WES — enabling the breakthrough radioligand therapy.

**Tissue handling**: Always request cryopreserved (flash-frozen) samples alongside FFPE. FFPE destroys RNA quality needed for transcriptomics.

See [references/diagnostics-pipeline.md](references/diagnostics-pipeline.md) for the complete open-source bioinformatics pipeline.

### Pillar 2: Personalized Therapeutic Development

Use diagnostic findings to design patient-specific treatments. Access experimental drugs via FDA expanded access.

**Treatment categories (layer compatible modalities):**

| Category | Mechanism | Examples |
|----------|-----------|---------|
| Checkpoint inhibitors | Remove immune brakes | Dostarlimab (PD-1), Ipilimumab (CTLA-4) |
| Neoantigen vaccines | Train immune recognition | Peptide vaccines (pVACtools), mRNA vaccines |
| Oncolytic viruses | Kill tumor + release antigens | AdaPT-001 (TGF-beta trap) |
| Cell therapies | Direct immune killing | NK cells (SNK-01), CAR-T, MSCs |
| Radioligand therapy | Targeted radiation | 177Lu/225Ac conjugated to tumor-targeting ligand |
| Immune modulators | Amplify response | GM-CSF, Anktiva (IL-15) |
| Targeted therapy | Block specific pathways | XGeva (RANKL), mTOR inhibitors |

**Regulatory pathway**: FDA Form 3926 (Individual Patient Expanded Access IND) — typically approved within 48 hours. The FDA is faster than hospital IRBs.

See [references/treatment-categories.md](references/treatment-categories.md) for detailed treatment logic.
See [references/regulatory-access.md](references/regulatory-access.md) for expanded access navigation.

### Pillar 3: Parallel Treatment

Run compatible therapies simultaneously. Monitor with ctDNA and serial scRNA-seq to measure what works.

**Combination logic:**
```
Checkpoint inhibitors  → Remove immune brakes (foundation layer)
  + Neoantigen vaccines → Train recognition (synergizes with checkpoint)
  + Oncolytic virus     → Kill + release antigens (synergizes with vaccines)
  + Cell therapy        → Innate killing (independent mechanism)
  + Radioligand         → Targeted kill to specific marker (independent)
  + Immune modulators   → Amplify all of the above
```

**Monitoring cadence:**
- ctDNA: every 2-4 weeks (real-time response measurement)
- scRNA-seq PBMCs: monthly (immune evolution tracking)
- Imaging (PET/CT/MRI): every 2-3 months
- Flow cytometry: monthly

**Success metric**: Immune infiltration shift (cold → hot tumor). Reference case: 19% → 89% T cells in tumor microenvironment.

See [references/mrd-monitoring.md](references/mrd-monitoring.md) for liquid biopsy interpretation.

## Decision Workflow

```
1. DIAGNOSE COMPREHENSIVELY
   ├── Order WGS + WES + RNA-seq + scRNA-seq
   ├── Establish ctDNA baseline (multiple platforms)
   ├── Request cryopreserved tissue (not just FFPE)
   └── Run functional drug testing (organoids if available)

2. IDENTIFY TARGETS
   ├── Standard: Known driver mutations → approved targeted therapies
   ├── Non-obvious: scRNA-seq → overexpressed surface proteins (FAP, B7H3, EphA2)
   ├── Validate: PET imaging with target-specific tracers (theranostic confirmation)
   └── Predict: Neoantigen candidates via pVACseq + MHCflurry

3. DESIGN TREATMENT COMBINATION
   ├── Foundation: Checkpoint inhibitor (if not contraindicated)
   ├── Layer: Neoantigen vaccine (peptide or mRNA)
   ├── Layer: One or more of: oncolytic virus, cell therapy, radioligand
   ├── Support: Immune modulators, bone protection, etc.
   └── Access: FDA Form 3926 for experimental agents

4. MONITOR AND ADAPT
   ├── ctDNA every 2-4 weeks → detect response or progression early
   ├── Serial scRNA-seq → track immune landscape evolution
   ├── Imaging every 2-3 months → structural assessment
   └── Adjust: Add/remove therapies based on molecular response

5. MAINTAIN REMISSION
   ├── Preventive vaccines (mRNA neoantigen, ongoing)
   ├── Continued monitoring (ctDNA, imaging)
   └── Backup: Engineered cell therapies with logic gates (if needed)
```

## Team Structure

| Role | Function | Scaling Alternative |
|------|----------|-------------------|
| Care CEO | Orchestrate diagnostics, coordinate institutions | AI agent + case manager |
| Clinical advisory board | Treatment decisions, drug interactions | Tumor board + AI decision support |
| Scientific advisory board | Interpret genomics, design experiments | Bioinformatics platforms |
| Concierge medical service | Logistics, scheduling, access | Patient navigator programs |

## Cost Reality

| Approach | Estimated Cost |
|----------|---------------|
| Sid's full approach (2022-2026) | $1M+ |
| Future platform-based personalized oncology | ~$175K (Hershberg projection) |
| Standard pancreatic cancer treatment | $250K+ |
| OpenVaxx DIY mRNA vaccine (materials only) | $4.2K-$13.4K per patient |
| Drug approval (population medicine) | $4.4B |

## Structural Biology Layer (AlphaFold + Protein Design)

Structure prediction adds 3D validation on top of the sequence-based pipeline. Four integration points:

### 1. Neoantigen Vaccine Validation
After pVACseq + MHCflurry rank candidates by sequence, validate top 20-50 with **AlphaFold Multimer** (peptide + HLA chain). Filter by ipTM >0.5, PAE_interface <10. Re-rank. This catches peptides that score well in 1D but don't physically fit the MHC groove.

### 2. Radioligand Target Modeling
Retrieve target structure from **AlphaFold DB** (FAP: AF-Q12884-F1, B7H3: AF-Q5ZPR3-F1). Model ligand binding with **Chai/Boltz**. Validate that diagnostic (68Ga) and therapeutic (177Lu/225Ac) versions maintain equivalent binding.

### 3. De Novo Therapeutic Binder Design
When no existing drug fits the target: **RFdiffusion** (2.8K stars) generates backbone geometries → **ProteinMPNN** (1.7K stars) designs sequences → **ESMFold/AlphaFold2** validates structures. Tier 1 candidates: pLDDT >85, pTM >0.8.

### 4. Mutation Impact Analysis
For each somatic mutation: predict wildtype vs mutant structures. Surface-altering mutations on expressed proteins → neoantigen candidates. Destabilizing mutations → misfolded protein → immune recognition. **ESM-2** embeddings for fast batch screening.

See [references/structural-biology.md](references/structural-biology.md) for the complete pipeline, tool stack, quality thresholds, and key target UniProt IDs.

---

## Key Reference Case Data

- **Source**: [osteosarc.com](https://osteosarc.com) — 25TB open data (Google Cloud)
- **Article**: [centuryofbio.com/p/sid](https://centuryofbio.com/p/sid) — "Going Founder Mode on Cancer" by Elliot Hershberg
- **Venture fund**: [evenone.ventures](https://evenone.ventures) — scaling personalized oncology
- **Research repo**: `~/broomva/research/founder-mode-cancer/` — complete local analysis

## References

- [Diagnostics Pipeline](references/diagnostics-pipeline.md) — Open-source bioinformatics toolchain (BWA → GATK → ASCAT → Scanpy → pVACtools)
- [Treatment Categories](references/treatment-categories.md) — Detailed treatment modalities, mechanisms, and combination rationale
- [Regulatory Access](references/regulatory-access.md) — FDA expanded access, IRB navigation, tissue access strategies
- [MRD Monitoring](references/mrd-monitoring.md) — Liquid biopsy platforms, interpretation, and cross-platform comparison
- [Structural Biology](references/structural-biology.md) — AlphaFold, RFdiffusion, ProteinMPNN for neoantigen validation and de novo binder design
- [Open-Source Tools](references/open-source-tools.md) — GitHub repos, neoantigen vaccine pipelines, analysis tools
