---
name: dorado-bench-v2
description: Oxford Nanopore basecalling with Dorado on University of Michigan HPC clusters (ARMIS2 and Great Lakes). Use when running dorado basecalling, generating SLURM jobs for basecalling, benchmarking models, optimizing GPU resources, or processing POD5 data. Captures model paths, GPU allocations, and job metadata. Integrates with ont-experiments for provenance tracking. Supports fast/hac/sup models, methylation calling, and automatic resource calculation.
---

# Dorado-Bench v2 - ONT Basecalling

Basecalling toolkit for UM HPC clusters with provenance tracking.

## Integration

Run through ont-experiments for provenance tracking:

```bash
ont_experiments.py run basecalling exp-abc123 --model sup --output calls.bam --json stats.json
```

Or standalone:

```bash
python3 dorado_basecall.py /path/to/pod5 --model sup --cluster armis2 --output calls.bam
```

## Cluster Configurations

### ARMIS2 (sigbio-a40)

```yaml
partition: sigbio-a40
account: bleu1
gres: gpu:a40:1
dorado: /nfs/turbo/umms-bleu-secure/programs/dorado-1.1.1-linux-x64/bin/dorado
models: /nfs/turbo/umms-bleu-secure/programs/dorado_models
```

### Great Lakes (gpu_mig40)

```yaml
partition: gpu_mig40
account: bleu99
gres: gpu:nvidia_a100_80gb_pcie_3g.40gb:1
```

## Model Tiers

| Tier | Accuracy | ARMIS2 Resources |
|------|----------|------------------|
| fast | ~95% | batch=4096, mem=50G, 24h |
| hac | ~98% | batch=2048, mem=75G, 72h |
| sup | ~99% | batch=1024, mem=100G, 144h |

## Options

| Option | Description |
|--------|-------------|
| `--model TIER` | fast, hac, sup (default: hac) |
| `--version VER` | Model version (default: v5.0.0) |
| `--cluster` | armis2 or greatlakes |
| `--output FILE` | Output BAM file |
| `--json FILE` | Output JSON statistics |
| `--slurm FILE` | Generate SLURM script |
| `--emit-moves` | Include move table |
| `--modifications MOD` | Enable 5mCG_5hmCG methylation |

## SLURM Generation

```bash
python3 dorado_basecall.py /path/to/pod5 \
  --model sup@v5.0.0 \
  --cluster armis2 \
  --slurm job.sbatch

sbatch job.sbatch
```

## Event Tracking

When run through ont-experiments, captures:
- Model name and full path
- Model tier/version/chemistry
- Batch size and device
- BAM statistics (reads, qscore, N50)
- SLURM job ID, nodes, GPUs

## Methylation Calling

```bash
ont_experiments.py run basecalling exp-abc123 \
  --model sup \
  --modifications 5mCG_5hmCG \
  --output calls_5mc.bam
```

Resources adjusted: memory +50%, batch size -30%
