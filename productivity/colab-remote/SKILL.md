---
name: colab-remote
category: compute
description: >
  Orchestrate Google Colab Pro/Pro+ GPU instances as remote training backends via SSH.
  Compounds /agent-browser (to launch Colab sessions and install colab-ssh) with SSH
  (to operate the runtime remotely). Use when: (1) launching a Colab notebook for GPU
  training, (2) running training jobs on Colab from the local terminal, (3) transferring
  datasets/checkpoints to/from Colab, (4) monitoring GPU utilization on a Colab instance,
  (5) integrating Colab GPU compute with /autoany EGRI optimization loops, (6) reconnecting
  to a Colab session after timeout. Triggers on: "colab", "colab-remote", "colab ssh",
  "colab training", "remote GPU", "colab pro", "train on colab", "google colab".
---

# Colab Remote — SSH-Operated GPU Training

Operate Google Colab Pro/Pro+ instances as headless GPU backends from the local terminal.

## Architecture

```
Local Mac (Claude Code)
  ├── agent-browser → Chrome → colab.research.google.com
  │   └── Opens notebook, runs colab-ssh setup cell
  ├── SSH tunnel → Colab runtime (via ngrok or cloudflared)
  │   └── Run training, monitor GPU, transfer files
  └── /autoany EGRI loop (local)
      └── Proposes mutations → SSH executes on Colab → evaluates results
```

## Phase 1: Launch Colab Session (Browser Automation)

Use `/agent-browser` to open Colab and set up SSH access.

### Step 1: Open Colab and create notebook

```bash
agent-browser open "https://colab.research.google.com/#create=true"
agent-browser wait --load networkidle
agent-browser snapshot -i
```

If login is required, prompt the user to authenticate manually, then re-snapshot.

### Step 2: Select GPU runtime

Navigate Runtime > Change runtime type, select GPU (T4/V100/A100 depending on plan), and save.

### Step 3: Install colab-ssh and get connection details

Type the SSH setup code into a cell. Two methods supported:

**Method A: ngrok (recommended)**

```python
!pip install colab-ssh --upgrade
from colab_ssh import launch_ssh
launch_ssh("YOUR_NGROK_TOKEN")
```

User must provide ngrok authtoken from https://ngrok.com.

**Method B: cloudflared (no account needed)**

```python
!pip install colab-ssh --upgrade
from colab_ssh import launch_ssh_cloudflared
launch_ssh_cloudflared(password="your-password-here")
```

### Step 4: Extract and save connection details

After the cell runs, snapshot output to extract hostname/port. Save for reuse:

```bash
mkdir -p ~/.colab-remote
cat > ~/.colab-remote/session.env << 'EOF'
COLAB_HOST=0.tcp.ngrok.io
COLAB_PORT=12345
COLAB_USER=root
COLAB_METHOD=ngrok
EOF
```

Load in subsequent commands: `source ~/.colab-remote/session.env`

## Phase 2: SSH Operations

### Connect

```bash
# ngrok
ssh -o StrictHostKeyChecking=no -p $COLAB_PORT root@$COLAB_HOST
# cloudflared
ssh -o StrictHostKeyChecking=no -o ProxyCommand="cloudflared access ssh --hostname %h" root@$COLAB_HOST
```

### Verify GPU

```bash
ssh -p $COLAB_PORT root@$COLAB_HOST "nvidia-smi"
```

### Transfer files

```bash
# Upload
scp -P $COLAB_PORT -r ./data root@$COLAB_HOST:/content/data
# Download
scp -P $COLAB_PORT -r root@$COLAB_HOST:/content/checkpoints ./checkpoints
```

### Run training

```bash
# Foreground
ssh -p $COLAB_PORT root@$COLAB_HOST "cd /content && python train.py --epochs 10"
# Background (survives SSH disconnect)
ssh -p $COLAB_PORT root@$COLAB_HOST "cd /content && nohup python train.py > train.log 2>&1 &"
# Monitor
ssh -p $COLAB_PORT root@$COLAB_HOST "tail -f /content/train.log"
```

### Monitor GPU

```bash
ssh -p $COLAB_PORT root@$COLAB_HOST "nvidia-smi --query-gpu=utilization.gpu,utilization.memory,memory.used,memory.total,temperature.gpu --format=csv"
```

### Install dependencies

```bash
ssh -p $COLAB_PORT root@$COLAB_HOST "pip install torch transformers peft bitsandbytes accelerate datasets"
```

## Phase 3: EGRI Integration (/autoany)

Wire Colab as the execution backend for an EGRI optimization loop. See `references/egri-colab.md` for the full problem-spec template and harness patterns.

### Execution loop (summary)

```
for each trial:
  1. Upload mutated artifact → scp to Colab
  2. Execute on Colab GPU → ssh python train.py
  3. Evaluate results → ssh python evaluate.py
  4. Download metrics → scp results.json
  5. Score locally (immutable evaluator)
  6. Promote or discard based on policy
```

## Phase 4: Session Lifecycle

| Tier | Max runtime | Idle timeout | GPU |
|------|-------------|--------------|-----|
| Free | 12h | 90min | T4, limited |
| Pro | 24h | 90min | T4, V100, priority |
| Pro+ | 24h | 90min | T4, V100, A100 |

### Keep-alive

```bash
ssh -p $COLAB_PORT root@$COLAB_HOST "while true; do sleep 300; echo keepalive; done &"
```

### Reconnect after timeout

1. Check: `ssh -p $COLAB_PORT root@$COLAB_HOST "echo ok" 2>/dev/null && echo "UP" || echo "DOWN"`
2. If dead, re-launch via Phase 1 (browser automation)
3. Resume from last checkpoint

### Google Drive persistence

Mount Drive to persist across sessions:

```bash
ssh -p $COLAB_PORT root@$COLAB_HOST "python -c 'from google.colab import drive; drive.mount(\"/content/drive\")'"
# Checkpoints survive in /content/drive/MyDrive/
```

## Quick Reference

| Task | Command |
|------|---------|
| Check GPU | `ssh -p $COLAB_PORT root@$COLAB_HOST "nvidia-smi"` |
| Upload | `scp -P $COLAB_PORT ./file root@$COLAB_HOST:/content/` |
| Download | `scp -P $COLAB_PORT root@$COLAB_HOST:/content/file ./` |
| Run script | `ssh -p $COLAB_PORT root@$COLAB_HOST "python /content/script.py"` |
| Background job | `ssh -p $COLAB_PORT root@$COLAB_HOST "nohup python train.py > log 2>&1 &"` |
| Tail log | `ssh -p $COLAB_PORT root@$COLAB_HOST "tail -20 /content/log"` |
| Disk space | `ssh -p $COLAB_PORT root@$COLAB_HOST "df -h /content"` |
| Kill job | `ssh -p $COLAB_PORT root@$COLAB_HOST "pkill -f train.py"` |
| Session alive? | `ssh -p $COLAB_PORT root@$COLAB_HOST "echo ok" 2>/dev/null` |

## Prerequisites

- **ngrok account** (free): https://ngrok.com — or `cloudflared`: `brew install cloudflared`
- **Colab Pro/Pro+** for GPU priority and longer runtimes
- **agent-browser** installed and working
- **Google account** signed into Chrome
