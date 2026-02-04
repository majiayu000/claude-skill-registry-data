---
name: cost-calculator
description: Cost estimation scripts and tools for calculating GPU hours, training costs, and inference pricing across Modal, Lambda Labs, and RunPod platforms. Use when estimating ML training costs, comparing platform pricing, calculating GPU hours, budgeting for ML projects, or when user mentions cost estimation, pricing comparison, GPU budgeting, training cost analysis, or inference cost optimization.
allowed-tools: Read, Write, Bash, Glob, Grep, Edit
---

# ML Training Cost Calculator

**Purpose:** Provide production-ready cost estimation tools for ML training and inference across cloud GPU platforms (Modal, Lambda Labs, RunPod).

**Activation Triggers:**
- Estimating training costs for ML models
- Comparing GPU platform pricing
- Calculating GPU hours for training jobs
- Budgeting for ML projects
- Optimizing inference costs
- Evaluating cost-effectiveness of different GPU types
- Planning resource allocation

**Key Resources:**
- `scripts/estimate-training-cost.sh` - Calculate training costs based on model size, data, GPU type
- `scripts/estimate-inference-cost.sh` - Estimate inference costs for production workloads
- `scripts/calculate-gpu-hours.sh` - Convert training parameters to GPU hours
- `scripts/compare-platforms.sh` - Compare costs across Modal, Lambda, RunPod
- `templates/cost-breakdown.json` - Structured cost breakdown template
- `templates/platform-pricing.yaml` - Up-to-date platform pricing data
- `examples/training-cost-estimate.md` - Example training cost calculation
- `examples/inference-cost-estimate.md` - Example inference cost analysis

## Platform Pricing Overview

### Modal (Serverless - Pay Per Second)

**GPU Options:**
- **T4**: $0.000164/sec ($0.59/hr) - Development, small models
- **L4**: $0.000222/sec ($0.80/hr) - Cost-effective training
- **A10**: $0.000306/sec ($1.10/hr) - Mid-range training
- **A100 40GB**: $0.000583/sec ($2.10/hr) - Large model training
- **A100 80GB**: $0.000694/sec ($2.50/hr) - Very large models
- **H100**: $0.001097/sec ($3.95/hr) - Cutting-edge training
- **H200**: $0.001261/sec ($4.54/hr) - Latest generation
- **B200**: $0.001736/sec ($6.25/hr) - Maximum performance

**Free Credits:**
- Starter: $30/month free
- Startup credits: Up to $50,000 FREE

### Lambda Labs (On-Demand Hourly)

**Single GPU:**
- **1x A10**: $0.31/hr - Cheapest single GPU option
- **1x V100 16GB**: $0.55/hr - Most affordable multi-GPU base

**8x GPU Clusters:**
- **8x V100**: $4.40/hr ($0.55/GPU) - Most affordable multi-GPU
- **8x A100 40GB**: $10.32/hr ($1.29/GPU)
- **8x A100 80GB**: $14.32/hr ($1.79/GPU)
- **8x H100**: $23.92/hr ($2.99/GPU)

### RunPod (Serverless - Pay Per Minute)

**Key Features:**
- Pay-per-minute billing
- FlashBoot <200ms cold-starts
- Zero egress fees on storage
- 30+ GPU SKUs available

## Cost Estimation Scripts

### 1. Estimate Training Cost

**Script:** `scripts/estimate-training-cost.sh`

**Usage:**
```bash
bash scripts/estimate-training-cost.sh \
  --model-size 7B \
  --dataset-size 10000 \
  --epochs 3 \
  --gpu t4 \
  --platform modal
```

**Parameters:**
- `--model-size`: Model size (125M, 350M, 1B, 3B, 7B, 13B, 70B)
- `--dataset-size`: Number of training samples
- `--epochs`: Number of training epochs
- `--batch-size`: Training batch size (default: auto-calculated)
- `--gpu`: GPU type (t4, a10, a100-40gb, a100-80gb, h100)
- `--platform`: Cloud platform (modal, lambda, runpod)
- `--peft`: Use PEFT/LoRA (yes/no, default: no)
- `--mixed-precision`: Use FP16/BF16 (yes/no, default: yes)

**Output:**
```json
{
  "model": "7B",
  "dataset_size": 10000,
  "epochs": 3,
  "gpu": "T4",
  "platform": "Modal",
  "estimated_hours": 4.2,
  "cost_breakdown": {
    "compute_cost": 2.48,
    "storage_cost": 0.05,
    "total_cost": 2.53
  },
  "cost_optimizations": {
    "with_peft": 1.26,
    "savings_percentage": 50
  },
  "alternative_platforms": {
    "lambda_a10": 1.30,
    "runpod_t4": 2.40
  }
}
```

**Calculation Methodology:**
- Estimates tokens per sample (avg 500 tokens)
- Calculates total training tokens
- Applies throughput rates per GPU type
- Accounts for PEFT (90% memory reduction)
- Accounts for mixed precision (2x speedup)

### 2. Estimate Inference Cost

**Script:** `scripts/estimate-inference-cost.sh`

**Usage:**
```bash
bash scripts/estimate-inference-cost.sh \
  --requests-per-day 1000 \
  --avg-latency 2 \
  --gpu t4 \
  --platform modal \
  --deployment serverless
```

**Parameters:**
- `--requests-per-day`: Expected daily requests
- `--avg-latency`: Average inference time (seconds)
- `--gpu`: GPU type
- `--platform`: Cloud platform
- `--deployment`: Deployment type (serverless, dedicated)
- `--batch-inference`: Batch requests (yes/no, default: no)

**Output:**
```json
{
  "requests_per_day": 1000,
  "requests_per_month": 30000,
  "avg_latency_sec": 2,
  "gpu": "T4",
  "platform": "Modal Serverless",
  "cost_breakdown": {
    "daily_compute_seconds": 2000,
    "daily_cost": 0.33,
    "monthly_cost": 9.90,
    "cost_per_request": 0.00033
  },
  "scaling_analysis": {
    "requests_10k_day": 99.00,
    "requests_100k_day": 990.00
  },
  "dedicated_alternative": {
    "monthly_cost": 442.50,
    "break_even_requests_day": 4500
  }
}
```

### 3. Calculate GPU Hours

**Script:** `scripts/calculate-gpu-hours.sh`

**Usage:**
```bash
bash scripts/calculate-gpu-hours.sh \
  --model-params 7B \
  --tokens-total 30M \
  --gpu a100-40gb
```

**Parameters:**
- `--model-params`: Model parameters (125M, 350M, 1B, 3B, 7B, 13B, 70B)
- `--tokens-total`: Total training tokens
- `--gpu`: GPU type
- `--peft`: Use PEFT (yes/no)
- `--multi-gpu`: Number of GPUs (default: 1)

**GPU Throughput Benchmarks:**
```
T4 (16GB):
  - 7B full fine-tune: 150 tokens/sec
  - 7B with PEFT: 600 tokens/sec

A100 40GB:
  - 7B full fine-tune: 800 tokens/sec
  - 7B with PEFT: 3200 tokens/sec
  - 13B with PEFT: 1600 tokens/sec

A100 80GB:
  - 13B full fine-tune: 600 tokens/sec
  - 70B with PEFT: 400 tokens/sec

H100:
  - 70B with PEFT: 1200 tokens/sec
```

### 4. Compare Platforms

**Script:** `scripts/compare-platforms.sh`

**Usage:**
```bash
bash scripts/compare-platforms.sh \
  --training-hours 4 \
  --gpu-type a100-40gb
```

**Output:**
```markdown
# Platform Cost Comparison

## Training Job: 4 hours on A100 40GB

| Platform | GPU Cost | Egress Fees | Total | Notes |
|----------|----------|-------------|-------|-------|
| Modal | $8.40 | $0.00 | $8.40 | Serverless, pay-per-second |
| Lambda | $5.16 | $0.00 | $5.16 | Cheapest for dedicated |
| RunPod | $8.00 | $0.00 | $8.00 | Pay-per-minute |

## Winner: Lambda Labs ($5.16)

Savings: $3.24 (38.6% vs Modal)

Recommendation: Use Lambda for long-running dedicated training, Modal for
serverless/bursty workloads.
```

## Cost Templates

### Cost Breakdown Template

**Template:** `templates/cost-breakdown.json`

```json
{
  "project_name": "ML Training Project",
  "cost_estimate": {
    "training": {
      "model_size": "7B",
      "training_runs": 4,
      "hours_per_run": 4.2,
      "gpu_type": "T4",
      "platform": "Modal",
      "cost_per_run": 2.48,
      "total_training_cost": 9.92
    },
    "inference": {
      "deployment_type": "serverless",
      "expected_requests_month": 30000,
      "gpu_type": "T4",
      "platform": "Modal",
      "monthly_cost": 9.90
    },
    "storage": {
      "model_artifacts_gb": 14,
      "dataset_storage_gb": 5,
      "monthly_storage_cost": 0.50
    },
    "total_monthly_cost": 20.32,
    "breakdown_percentage": {
      "training": 48.8,
      "inference": 48.7,
      "storage": 2.5
    }
  },
  "cost_optimizations_applied": {
    "peft_lora": "50% training cost reduction",
    "mixed_precision": "2x faster training",
    "serverless_inference": "Pay only for actual usage",
    "batch_inference": "Up to 10x reduction in inference cost"
  },
  "potential_savings": {
    "without_optimizations": 45.00,
    "with_optimizations": 20.32,
    "total_savings": 24.68,
    "savings_percentage": 54.8
  }
}
```

### Platform Pricing Data

**Template:** `templates/platform-pricing.yaml`

```yaml
platforms:
  modal:
    billing: per-second
    free_credits: 30  # USD per month
    startup_credits: 50000  # USD for eligible startups
    gpus:
      t4:
        price_per_sec: 0.000164
        price_per_hour: 0.59
        vram_gb: 16
      a100_40gb:
        price_per_sec: 0.000583
        price_per_hour: 2.10
        vram_gb: 40
      h100:
        price_per_sec: 0.001097
        price_per_hour: 3.95
        vram_gb: 80

  lambda:
    billing: per-hour
    free_credits: 0
    minimum_billing: 1-hour
    gpus:
      a10_1x:
        price_per_hour: 0.31
        vram_gb: 24
      a100_40gb_1x:
        price_per_hour: 1.29
        vram_gb: 40
      a100_40gb_8x:
        price_per_hour: 10.32
        total_vram_gb: 320

  runpod:
    billing: per-minute
    free_credits: 0
    features:
      - zero_egress_fees
      - flashboot_200ms
    gpus:
      t4:
        price_per_hour: 0.60  # Approximate
        vram_gb: 16
```

## Cost Estimation Examples

### Example 1: Training 7B Model

**File:** `examples/training-cost-estimate.md`

**Scenario:**
- Model: Llama 2 7B fine-tuning
- Dataset: 10,000 samples (5M tokens)
- Epochs: 3
- Total tokens: 15M
- Method: LoRA/PEFT

**Cost Calculation:**

```bash
bash scripts/estimate-training-cost.sh \
  --model-size 7B \
  --dataset-size 10000 \
  --epochs 3 \
  --gpu t4 \
  --platform modal \
  --peft yes
```

**Results:**
```
Training Time: 4.2 hours
Modal T4 Cost: $2.48
Alternative (Lambda A10): $1.30 (47% cheaper)

Optimization Impact:
- Without PEFT: $12.40 (5x more expensive)
- With PEFT: $2.48
- Savings: $9.92 (80%)
```

**Recommendation:** Use Lambda A10 for cheapest option, or Modal T4 for
serverless convenience.

### Example 2: Production Inference

**File:** `examples/inference-cost-estimate.md`

**Scenario:**
- Model: Custom 7B classifier
- Expected traffic: 1,000 requests/day
- Avg latency: 2 seconds per request
- Growth: 10x in 6 months

**Cost Calculation:**

```bash
bash scripts/estimate-inference-cost.sh \
  --requests-per-day 1000 \
  --avg-latency 2 \
  --gpu t4 \
  --platform modal \
  --deployment serverless
```

**Current (1K requests/day):**
```
Serverless Modal T4:
- Daily cost: $0.33
- Monthly cost: $9.90
- Cost per request: $0.00033

Dedicated Lambda A10:
- Monthly cost: $223 (24/7 instance)
- Break-even: 2,250 requests/day
- Not recommended for current traffic
```

**After Growth (10K requests/day):**
```
Serverless Modal T4:
- Monthly cost: $99.00
- Still cost-effective

Dedicated Lambda A10:
- Monthly cost: $223
- Break-even reached at 2,250 requests/day
- Recommendation: Stay serverless until 10K+ daily
```

## Cost Optimization Strategies

### 1. Use PEFT/LoRA

**Savings:** 50-90% training cost reduction

```bash
# Calculate savings
bash scripts/estimate-training-cost.sh --model-size 7B --peft no
# Cost: $12.40

bash scripts/estimate-training-cost.sh --model-size 7B --peft yes
# Cost: $2.48
# Savings: $9.92 (80%)
```

### 2. Mixed Precision Training

**Savings:** 2x faster training, 50% cost reduction

Automatically enabled in cost estimations with `--mixed-precision yes`

### 3. Platform Selection

**Use Case Guidelines:**

```bash
# Short jobs (<1 hour): Modal serverless
bash scripts/compare-platforms.sh --training-hours 0.5 --gpu-type t4
# Winner: Modal ($0.30 vs Lambda $0.31 minimum)

# Long jobs (4+ hours): Lambda dedicated
bash scripts/compare-platforms.sh --training-hours 4 --gpu-type a100-40gb
# Winner: Lambda ($5.16 vs Modal $8.40)

# Variable workloads: Modal serverless
# Pay only for actual usage, no idle cost
```

### 4. Batch Inference

**Savings:** Up to 10x reduction in inference cost

```bash
# Single inference
bash scripts/estimate-inference-cost.sh \
  --requests-per-day 1000 \
  --avg-latency 2 \
  --batch-inference no
# Cost: $9.90/month

# Batch inference (10 requests per batch)
bash scripts/estimate-inference-cost.sh \
  --requests-per-day 1000 \
  --avg-latency 0.3 \
  --batch-inference yes
# Cost: $1.49/month
# Savings: $8.41 (85%)
```

## Quick Reference: Cost Per Use Case

### Small Model Training (< 1B params)
- **Best GPU:** T4
- **Best Platform:** Modal (serverless)
- **Typical Cost:** $0.50-$2.00 per run
- **Time:** 30 min - 2 hours

### Medium Model Training (1B-7B params)
- **Best GPU:** T4 (with PEFT) or A100 40GB
- **Best Platform:** Lambda A10 (cheapest) or Modal T4 (convenience)
- **Typical Cost:** $1.00-$8.00 per run
- **Time:** 2-8 hours

### Large Model Training (7B-70B params)
- **Best GPU:** A100 80GB or H100 (with PEFT)
- **Best Platform:** Lambda (dedicated) or Modal (serverless)
- **Typical Cost:** $10-$100 per run
- **Time:** 8-48 hours

### Low-Traffic Inference (<1K requests/day)
- **Best Deployment:** Modal serverless
- **Best GPU:** T4
- **Typical Cost:** $5-$15/month

### High-Traffic Inference (>10K requests/day)
- **Best Deployment:** Dedicated or batch serverless
- **Best GPU:** A10 or A100
- **Typical Cost:** $100-$500/month

## Dependencies

**Required for scripts:**
```bash
# Bash 4.0+ (for associative arrays)
bash --version

# jq (for JSON processing)
sudo apt-get install jq

# bc (for floating-point calculations)
sudo apt-get install bc

# yq (for YAML processing)
pip install yq
```

## Best Practices Summary

1. **Always estimate before training** - Use cost scripts to avoid surprises
2. **Use PEFT for large models** - 50-90% cost savings
3. **Enable mixed precision** - 2x speedup with no quality loss
4. **Choose platform based on workload:**
   - Modal: Serverless, short jobs, variable workloads
   - Lambda: Long-running, dedicated, multi-GPU
   - RunPod: Per-minute billing flexibility
5. **Batch inference when possible** - Up to 10x cost reduction
6. **Apply for startup credits** - Modal offers $50K free
7. **Monitor actual costs** - Compare estimates to actuals, optimize
8. **Use smallest viable GPU** - T4 often sufficient with PEFT

---

**Supported Platforms:** Modal, Lambda Labs, RunPod
**GPU Types:** T4, L4, A10, A100 (40GB/80GB), H100, H200, B200
**Output Format:** JSON cost breakdowns and markdown reports
**Version:** 1.0.0
