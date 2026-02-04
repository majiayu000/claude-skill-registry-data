---
skill: 'hardware-sizing'
version: '2.0.0'
updated: '2025-12-31'
category: 'local-ai-infrastructure'
complexity: 'advanced'
prerequisite_skills: []
composable_with:
  - 'local-ai-deployment'
  - 'mlops-operations'
  - 'financial-modeling'
  - 'production-readiness'
---

# Hardware Sizing Skill

## Overview
Expertise in calculating and specifying hardware requirements for local AI deployments, including GPU selection, server configuration, storage, and network planning based on workload characteristics and team size.

## Key Capabilities
- GPU selection and sizing for LLM inference
- Server configuration for AI workloads
- Storage planning for models and data
- Network bandwidth calculations
- TCO modeling for hardware investments
- Capacity planning and growth projections

## GPU Selection Guide

### NVIDIA GPU Comparison

| GPU | VRAM | FP16 TFLOPS | Bandwidth | TDP | Price (approx) | Best For |
|-----|------|-------------|-----------|-----|----------------|----------|
| RTX 4090 | 24GB | 82.6 | 1 TB/s | 450W | $1,600 | Small teams, dev |
| RTX A6000 | 48GB | 38.7 | 768 GB/s | 300W | $4,500 | Medium teams |
| A100 40GB | 40GB | 77.9 | 1.5 TB/s | 400W | $10,000 | Production |
| A100 80GB | 80GB | 77.9 | 2.0 TB/s | 400W | $15,000 | Large models |
| H100 80GB | 80GB | 267 | 3.35 TB/s | 700W | $30,000 | Maximum perf |
| L40S | 48GB | 91.6 | 864 GB/s | 350W | $8,000 | Balanced |

### Model VRAM Requirements

| Model Size | FP16 | INT8 | INT4/AWQ | Example Models |
|------------|------|------|----------|----------------|
| 7B | 14GB | 8GB | 4GB | Qwen-Next (small variant), GLM-4.6 (small variant) |
| 13B | 26GB | 14GB | 8GB | Qwen-Next (mid variant), MiniMax-M2 (mid variant) |
| 34B | 68GB | 36GB | 18GB | Qwen-Next / GLM-4.6 (large-ish variants) |
| 70B | 140GB | 75GB | 38GB | Qwen-Next / GLM-4.6 / MiniMax-M2 (largest variants) |
| 110B | 220GB | 115GB | 58GB | Frontier-scale variants (verify availability + license) |

**VRAM Formula:**
```
VRAM Required = (Parameters × Bytes per Parameter) + Context Window Overhead
- FP16: 2 bytes per parameter
- INT8: 1 byte per parameter
- INT4: 0.5 bytes per parameter
- Context overhead: ~2GB for 8K context, ~8GB for 32K context
```

### GPU Sizing by Team Size

| Team Size | Usage Level | Model Size | Recommended GPU | Quantity |
|-----------|-------------|------------|-----------------|----------|
| 1-5 | Dev/Test | 7B-13B | RTX 4090 | 1 |
| 5-15 | Production | 13B-34B | RTX 4090 or A6000 | 1-2 |
| 15-30 | Production | 34B-70B | A100 40GB | 2 |
| 30-75 | Production | 70B | A100 80GB | 2-4 |
| 75-150 | Enterprise | 70B+ | H100 or A100 | 4-8 |
| 150+ | Enterprise | 70B+ | H100 cluster | 8+ |

## Server Configuration Templates

### Small Team Server (5-15 developers)

```yaml
# Small team AI server specification
server:
  type: Tower or 2U Rack

cpu:
  model: AMD EPYC 7343 or Intel Xeon Gold 5315Y
  cores: 16
  threads: 32

memory:
  type: DDR4-3200 ECC
  capacity: 128GB
  channels: 8

gpu:
  model: NVIDIA RTX 4090
  count: 1-2
  vram_total: 24-48GB
  nvlink: false

storage:
  system:
    type: NVMe SSD
    capacity: 500GB
    raid: None
  models:
    type: NVMe SSD
    capacity: 2TB
    raid: None
  logs:
    type: SATA SSD
    capacity: 2TB
    raid: 1

network:
  type: 10GbE
  ports: 2
  bonding: Active/Standby

power:
  psu: 1200W
  redundancy: Single (N)
  ups: Recommended

estimated_cost:
  hardware: $10,000 - $15,000
  annual_power: $1,500
  annual_maintenance: $1,000
```

### Medium Team Server (15-50 developers)

```yaml
# Medium team AI server specification
server:
  type: 2U Rack Mount

cpu:
  model: AMD EPYC 7543 or Intel Xeon Platinum 8358
  cores: 32
  threads: 64

memory:
  type: DDR4-3200 ECC
  capacity: 256GB
  channels: 8

gpu:
  model: NVIDIA A6000 or RTX 4090
  count: 2-4
  vram_total: 96-192GB
  nvlink: Recommended for A6000

storage:
  system:
    type: NVMe SSD
    capacity: 1TB
    raid: 1
  models:
    type: NVMe SSD
    capacity: 4TB
    raid: 0
  logs:
    type: SAS SSD
    capacity: 4TB
    raid: 10

network:
  type: 25GbE
  ports: 2
  bonding: LACP

power:
  psu: 2000W
  redundancy: Redundant (N+1)
  ups: Required

estimated_cost:
  hardware: $35,000 - $60,000
  annual_power: $4,000
  annual_maintenance: $3,000
```

### Enterprise Server (50-200 developers)

```yaml
# Enterprise AI server specification
server:
  type: 4U Rack Mount or DGX-style

cpu:
  model: 2x AMD EPYC 9354 or Intel Xeon Platinum 8480+
  cores: 64 total
  threads: 128

memory:
  type: DDR5-4800 ECC
  capacity: 512GB - 1TB
  channels: 12-16

gpu:
  model: NVIDIA A100 80GB or H100
  count: 4-8
  vram_total: 320-640GB
  nvlink: Required (NVSwitch for 8+ GPUs)

storage:
  system:
    type: NVMe SSD
    capacity: 2TB
    raid: 1
  models:
    type: NVMe SSD
    capacity: 8TB
    raid: 0 or 10
  logs:
    type: NVMe SSD
    capacity: 8TB
    raid: 10
  backup:
    type: SAS HDD
    capacity: 32TB
    raid: 6

network:
  type: 100GbE or InfiniBand
  ports: 2-4
  bonding: LACP

power:
  psu: 3000W+
  redundancy: Redundant (N+N)
  ups: Required with generator backup

estimated_cost:
  hardware: $150,000 - $400,000
  annual_power: $15,000 - $30,000
  annual_maintenance: $10,000 - $20,000
```

## Capacity Planning

### Request Volume Estimation

| Developer Usage | Requests/Day | Tokens/Request | Daily Tokens |
|-----------------|--------------|----------------|--------------|
| Light (occasional) | 20-30 | 2,000 | 40K-60K |
| Medium (regular) | 50-100 | 3,000 | 150K-300K |
| Heavy (power user) | 150-250 | 4,000 | 600K-1M |
| Intensive (AI-first) | 300-500 | 5,000 | 1.5M-2.5M |

### Throughput Calculation

```
# Calculate required throughput

Daily Requests = Team Size × Requests per User per Day
Peak Factor = 0.1 (10% of daily load in peak hour)
Peak Requests per Minute = (Daily Requests × Peak Factor) / 60

Tokens per Request = Avg Input Tokens + Avg Output Tokens
Peak Tokens per Second = Peak Requests per Minute × Tokens per Request / 60

# Example: 50 medium-usage developers
Daily Requests = 50 × 100 = 5,000
Peak Requests/min = 5,000 × 0.1 / 60 = 8.3
Tokens/Request = 2,000 + 1,000 = 3,000
Peak Tokens/sec = 8.3 × 3,000 / 60 = 415 tok/s
```

### GPU Throughput Reference

| GPU | Model Size | Throughput (tok/s) | Concurrent Requests |
|-----|------------|-------------------|---------------------|
| RTX 4090 | 7B | 100-150 | 8-12 |
| RTX 4090 | 13B | 50-80 | 4-8 |
| A100 40GB | 13B | 120-180 | 16-24 |
| A100 40GB | 34B | 60-100 | 8-16 |
| A100 80GB | 70B | 40-70 | 4-8 |
| H100 80GB | 70B | 100-150 | 8-16 |
| 2x A100 80GB | 70B (TP=2) | 80-140 | 8-16 |

### Sizing Formula

```
Required GPUs = Peak Tokens/sec / Single GPU Throughput × Safety Factor

Safety Factor = 1.3 (30% headroom for spikes)

# Example: 415 tok/s needed for 70B model
Single A100 80GB throughput = 55 tok/s average
Required GPUs = 415 / 55 × 1.3 = 9.8 → 10 A100 80GB

# OR with 2-GPU tensor parallel:
TP=2 throughput = 110 tok/s
Required TP pairs = 415 / 110 × 1.3 = 4.9 → 5 pairs (10 GPUs)
```

## Storage Planning

### Model Storage Requirements

| Model Size | Weights (FP16) | Weights (INT4) | With Tokenizer |
|------------|----------------|----------------|----------------|
| 7B | 14GB | 4GB | +500MB |
| 13B | 26GB | 7GB | +500MB |
| 34B | 68GB | 18GB | +500MB |
| 70B | 140GB | 38GB | +500MB |
| 100B+ | 200GB+ | 50GB+ | +1GB |

### Storage Architecture

```yaml
storage_tiers:
  tier1_hot:  # Active models
    type: NVMe SSD
    iops: 500K+
    latency: <0.1ms
    purpose: Currently loaded models, active inference
    sizing: 2x largest model size

  tier2_warm:  # Standby models
    type: SATA SSD or NVMe
    iops: 50K+
    latency: <1ms
    purpose: Quick-loading alternate models
    sizing: 5-10x model sizes for model library

  tier3_cold:  # Archives
    type: HDD or object storage
    purpose: Model version history, backups
    sizing: 3x warm storage for versioning

log_storage:
  type: SSD (fast write)
  sizing: |
    Daily logs = Requests/day × 2KB average
    Monthly = Daily × 30
    Retention storage = Monthly × Retention months
```

## Network Planning

### Bandwidth Requirements

| Component | Traffic Type | Bandwidth Need |
|-----------|--------------|----------------|
| API Requests | Client → Server | 1-10 Mbps per concurrent user |
| Responses | Server → Client | 5-50 Mbps per concurrent user |
| Model Loading | Storage → GPU | 10+ Gbps (reduces load time) |
| Monitoring | Server → Collector | 10-100 Mbps |
| Replication | Server → Backup | Varies by backup frequency |

### Network Architecture

```
┌─────────────────────────────────────────────────────┐
│                  Corporate Network                   │
│                     (10 GbE)                         │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────┴──────────────────────────────┐
│                  Load Balancer                       │
│               (25-100 GbE uplink)                    │
└──────────────────────┬──────────────────────────────┘
                       │
         ┌─────────────┴─────────────┐
         │                           │
    ┌────┴────┐                 ┌────┴────┐
    │ AI Node │ ◄──(25 GbE)──► │ AI Node │
    │   #1    │                 │   #2    │
    └────┬────┘                 └────┬────┘
         │                           │
         └─────────────┬─────────────┘
                       │
              ┌────────┴────────┐
              │  Storage Array  │
              │   (100 GbE)     │
              └─────────────────┘
```

## TCO Calculation

### Hardware TCO Template

```markdown
## 3-Year Total Cost of Ownership

### Capital Expenditure (CapEx)
| Item | Unit Cost | Quantity | Total |
|------|-----------|----------|-------|
| Server (compute) | $15,000 | 2 | $30,000 |
| GPUs (A100 80GB) | $15,000 | 4 | $60,000 |
| Storage (NVMe) | $500/TB | 8TB | $4,000 |
| Network equipment | $5,000 | 1 | $5,000 |
| Installation | $2,000 | 1 | $2,000 |
| **CapEx Total** | | | **$101,000** |

### Operating Expenses (OpEx) - Annual
| Item | Monthly | Annual |
|------|---------|--------|
| Power (3kW average) | $400 | $4,800 |
| Cooling | $100 | $1,200 |
| Maintenance/support | $500 | $6,000 |
| Hosting/colocation | $1,000 | $12,000 |
| Admin labor (0.25 FTE) | $2,500 | $30,000 |
| **Annual OpEx** | **$4,500** | **$54,000** |

### 3-Year TCO
| Year | CapEx | OpEx | Cumulative |
|------|-------|------|------------|
| Year 1 | $101,000 | $54,000 | $155,000 |
| Year 2 | $0 | $54,000 | $209,000 |
| Year 3 | $0 | $54,000 | $263,000 |

### Per-Request Cost (at 500K requests/month)
Year 1: $155,000 / 6M requests = $0.026/request
Year 3: $263,000 / 18M requests = $0.015/request (amortized)
```

### Cloud API Cost Comparison

```markdown
## Local vs Cloud Cost Comparison

### Assumptions
- 50 developers, medium usage
- 100 requests/dev/day = 5,000 requests/day
- 3,000 tokens/request average
- 15M tokens/day = 450M tokens/month

### Cloud API Costs (GPT-4o-mini pricing)
- Input: $0.15/1M tokens × 150M = $22.50/month
- Output: $0.60/1M tokens × 300M = $180/month
- Total: ~$200/month = $2,400/year

### Cloud API Costs (GPT-4o pricing)
- Input: $2.50/1M tokens × 150M = $375/month
- Output: $10.00/1M tokens × 300M = $3,000/month
- Total: ~$3,375/month = $40,500/year

### Local Large Model (Qwen-Next / MiniMax-M2 / GLM-4.6)
- Year 1 TCO: $155,000
- Equivalent cloud cost: $40,500/year
- Breakeven: 3.8 years

### With Data Sovereignty Premium
If data can't go to cloud, local is only option.
Value of data sovereignty: Priceless / Required
```

## Scaling Strategy

### Horizontal Scaling Triggers

| Metric | Add Capacity When | Scale Strategy |
|--------|-------------------|----------------|
| GPU Utilization | >80% sustained | Add GPU or node |
| Queue Depth | >10 requests sustained | Add replica |
| P95 Latency | >5s sustained | Add GPU for parallelism |
| Memory Pressure | >90% VRAM | Larger GPU or quantization |

### Vertical Scaling Path

```
Stage 1: Single RTX 4090 (24GB)
   ↓ Need more VRAM
Stage 2: Single A6000 (48GB)
   ↓ Need more throughput
Stage 3: 2x A6000 with tensor parallel
   ↓ Need larger models
Stage 4: 2x A100 80GB
   ↓ Need more throughput
Stage 5: 4x A100 80GB with NVLink
   ↓ Need maximum performance
Stage 6: 8x H100 with NVSwitch
```

## Best Practices

### Procurement
1. **Budget 20% contingency** for unexpected needs
2. **Test before bulk purchase** with single unit
3. **Consider used enterprise GPUs** (A100s at 50% cost)
4. **Plan for 3-year lifecycle** (hardware depreciation)
5. **Include installation and training** in budget

### Deployment
1. **Start small, scale up** - validate before expanding
2. **Keep 30% headroom** for traffic spikes
3. **Plan upgrade path** before initial deployment
4. **Document all specifications** for future reference

### Monitoring
1. **Track utilization trends** weekly
2. **Plan capacity 3-6 months ahead**
3. **Review TCO quarterly** against cloud alternatives
4. **Update sizing models** with actual usage data

This skill ensures organizations size hardware appropriately for their AI workloads, optimizing for both performance and cost-effectiveness.
