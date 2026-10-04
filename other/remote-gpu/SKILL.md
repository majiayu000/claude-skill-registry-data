---
name: remote-gpu
category: compute
description: >
  Orchestrate a headless GPU server (NUC, cloud VM, or any SSH-accessible machine) from a local
  Mac or workstation. Use when: (1) Running GPU workloads remotely (training, inference, video
  generation), (2) Triggering Claude Code sessions on a remote machine, (3) Launching autoany
  EGRI loops, symphony orchestrations, or training scripts on remote hardware, (4) Managing jobs
  on a headless GPU server (submit, monitor, cancel, download results), (5) Setting up SSH
  tunnels or API bridges to a GPU machine, (6) Orchestrating multi-machine agent workflows.
  Triggers on: remote gpu, headless server, gpu server, remote training, remote inference,
  ssh gpu, nuc server, remote claude code, remote agent, gpu orchestration.
---

# Remote GPU Orchestrator

Operate a headless GPU server from your Mac. Submit jobs (training, inference, agents),
monitor progress, and retrieve results — all over SSH or HTTP API.

## Architecture

```
┌─────────────────┐         SSH / HTTP API        ┌──────────────────────┐
│  Mac (Control)   │ ──────────────────────────▶  │  NUC / GPU Server    │
│                  │                               │                      │
│  - Claude Code   │  Commands:                    │  - RTX 4090 (12GB)   │
│  - This skill    │    submit_job                  │  - gpu-server.py     │
│  - gpu-remote.sh │    check_status               │  - Job queue         │
│                  │    stream_logs                 │  - Claude Code       │
│                  │    download_results            │  - autoany / symphony│
│                  │    run_claude_session          │  - LTX-2 / training  │
└─────────────────┘                               └──────────────────────┘
```

## Quick Setup

### 1. Configure SSH Access

```bash
# On Mac — set up passwordless SSH to NUC
ssh-keygen -t ed25519 -f ~/.ssh/nuc_gpu
ssh-copy-id -i ~/.ssh/nuc_gpu.pub user@NUC_IP

# Add to ~/.ssh/config
cat >> ~/.ssh/config << 'EOF'
Host nuc-gpu
  HostName NUC_IP_ADDRESS
  User YOUR_USER
  IdentityFile ~/.ssh/nuc_gpu
  Port 22
  ServerAliveInterval 60
EOF

# Test
ssh nuc-gpu "nvidia-smi"
```

### 2. Install Server on NUC

```bash
# SSH into NUC
ssh nuc-gpu

# Copy and start the server
pip install fastapi uvicorn psutil
python gpu-server.py --port 8420 --workdir ~/gpu-jobs
```

Or run `scripts/setup-nuc.sh nuc-gpu` from Mac to automate.

### 3. Use from Mac

```bash
# Via SSH (simplest)
source scripts/gpu-remote.sh
gpu-submit "python train.py --epochs 10" --workdir ~/project
gpu-status
gpu-logs job-abc123
gpu-download job-abc123

# Via HTTP API (if gpu-server.py running)
curl http://nuc-gpu:8420/submit -d '{"command":"python train.py"}'
curl http://nuc-gpu:8420/jobs
```

## Job Types

### Training Runs

```bash
# Submit a training job
gpu-submit "cd ~/project && python train.py --config config.yaml" \
  --name "lora-training-v2" \
  --workdir ~/project

# Monitor GPU usage during training
gpu-watch  # streams nvidia-smi every 5s
```

### Video Generation (LTX-2)

```bash
gpu-submit "cd ~/LTX-2 && source .venv/bin/activate && \
  python -m ltx_pipelines.run \
    --config configs/ltx-2.3-22b-distilled-2stage.yaml \
    --quantization fp8-cast \
    --prompt 'A drone shot over mountains at dawn' \
    --height 704 --width 1216 --num_frames 97 \
    --output /tmp/output.mp4" \
  --name "ltx-mountains" \
  --download /tmp/output.mp4
```

### Claude Code Sessions

```bash
# Start a Claude Code session on the NUC
gpu-claude "Fix the failing tests in ~/project" --workdir ~/project

# Start with a specific branch
gpu-claude "Implement the feature described in PLAN.md" \
  --workdir ~/project --branch feature/new-api
```

### Autoany EGRI Loops

```bash
# Run an EGRI optimization loop on GPU
gpu-submit "cd ~/autoany && cargo run -- \
  --config egri.toml \
  --max-iterations 50 \
  --target-metric accuracy" \
  --name "egri-optimization"
```

### Symphony Orchestrations

```bash
# Launch a symphony workflow on GPU
gpu-submit "cd ~/symphony && cargo run -- \
  orchestrate workflow.toml" \
  --name "symphony-pipeline"
```

## Commands Reference

All commands work via the `gpu-remote.sh` shell functions:

| Command | Description |
|---------|-------------|
| `gpu-submit CMD` | Submit a job, returns job ID |
| `gpu-status` | Show all jobs and GPU state |
| `gpu-logs JOB_ID` | Stream logs from a job |
| `gpu-cancel JOB_ID` | Cancel a running job |
| `gpu-download JOB_ID [FILE]` | Download job output files |
| `gpu-watch` | Live GPU monitoring (nvidia-smi) |
| `gpu-claude PROMPT` | Start Claude Code session on NUC |
| `gpu-ssh` | Interactive SSH to NUC |
| `gpu-sync DIR` | rsync a directory to/from NUC |
| `gpu-tunnel PORT` | SSH tunnel a port from NUC to localhost |

### Options

```
--name NAME        Human-readable job name
--workdir DIR      Working directory on NUC
--branch BRANCH    Git branch to checkout before running
--download FILE    Auto-download this file when job completes
--gpu GPU_ID       Target GPU index (default: 0)
--timeout SECS     Job timeout (default: 3600)
```

## HTTP API (gpu-server.py)

If running the Python API server on the NUC:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/submit` | POST | Submit job `{command, name, workdir, timeout}` |
| `/jobs` | GET | List all jobs with status |
| `/jobs/{id}` | GET | Job detail (status, logs, files) |
| `/jobs/{id}/logs` | GET | Stream job logs (SSE) |
| `/jobs/{id}/cancel` | POST | Cancel running job |
| `/jobs/{id}/files` | GET | List output files |
| `/jobs/{id}/files/{name}` | GET | Download a file |
| `/status` | GET | GPU info, disk, memory |

See `references/api-reference.md` for full API documentation.

## Configuration

Create `~/.config/gpu-remote/config.toml` on Mac:

```toml
[server]
host = "nuc-gpu"          # SSH host alias or IP
port = 8420               # API server port (if using HTTP)
user = "your-user"        # SSH user
mode = "ssh"              # "ssh" or "api"

[defaults]
workdir = "~/gpu-jobs"
timeout = 3600
gpu_id = 0

[sync]
exclude = [".git", "node_modules", "__pycache__", ".venv"]
```

## Troubleshooting

- **SSH timeout:** Add `ServerAliveInterval 60` to SSH config
- **CUDA OOM:** Check `gpu-status` for other jobs using VRAM, cancel or wait
- **Job stuck:** Use `gpu-logs JOB_ID` to check output, `gpu-cancel JOB_ID` to kill
- **Server down:** SSH in and restart: `ssh nuc-gpu "python gpu-server.py &"`
- **File transfer slow:** Use `gpu-sync` (rsync) instead of individual downloads
