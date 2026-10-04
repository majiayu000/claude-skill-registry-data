---
name: aspire-hf-download
description: Stably download HuggingFace models or datasets on NSCC ASPIRE 2A using PBS compute jobs, Miniforge, huggingface_hub snapshot_download, hf_xet, and scratch storage; use when the user needs large HF repo downloads on aspire2a.nus.edu.sg or wants to diagnose stalled/partial model shard downloads.
---

# ASPIRE 2A HuggingFace Downloads

Use this skill when helping download large HuggingFace models or datasets on NSCC ASPIRE 2A.

The reliable pattern is:

1. Run the download inside a PBS compute job, not as a foreground login-node task.
2. Load `miniforge3/25.3.1`.
3. Install or refresh the user-local HuggingFace client with Xet support:
   `python -m pip install --user -U "huggingface_hub[hf_xet]"`.
4. Use `huggingface_hub.snapshot_download`, not `git clone` / `git lfs pull`, for large repos.
5. Put the final repo under `/scratch/users/nus/$USER/...`, not home.
6. Treat HuggingFace tokens explicitly, especially if `HF_HOME` is moved to scratch.
7. Monitor with `qstat`, PBS logs, `du`, and shard counts.

Do not recommend `ssh ... nohup git lfs pull` on the login node for big model/data downloads. It is fragile, can stall silently, and puts heavy I/O on the wrong node. `git-lfs` may exist on the login node, but it may be missing or unavailable in the compute/PBS environment, so the download workflow should not depend on it.

## PBS Template

Copy this as `hf_snapshot_download.pbs`, then edit the variables near the top.

```bash
#!/bin/bash
#PBS -N hf_snapshot_download
#PBS -q normal
#PBS -l select=1:ncpus=8:mem=64gb
#PBS -l walltime=24:00:00
#PBS -j oe
#PBS -o hf_snapshot_download.$PBS_JOBID.log

set -euo pipefail

module load miniforge3/25.3.1

python -m pip install --user -U "huggingface_hub[hf_xet]"

# Required: HuggingFace repo id, for example:
#   OpenOneRec/OneRec-8B-pro
#   facebook/opt-6.7b
#   HuggingFaceFW/fineweb
export HF_REPO_ID="${HF_REPO_ID:-OpenOneRec/OneRec-8B-pro}"

# Use "model" or "dataset".
export HF_REPO_TYPE="${HF_REPO_TYPE:-model}"

# Destination can be any scratch path the user owns.
# Example successful destination:
#   /scratch/users/nus/e1538xxx/models/OpenOneRec-OneRec-8B-pro-hf
export HF_LOCAL_DIR="${HF_LOCAL_DIR:-/scratch/users/nus/$USER/models/${HF_REPO_ID//\//-}}"

# Optional: set this before qsub if the repo is private or gated:
#   export HF_TOKEN=hf_...
# qsub -v HF_REPO_ID,HF_REPO_TYPE,HF_LOCAL_DIR,HF_TOKEN hf_snapshot_download.pbs
#
# Token pitfall:
# If you set HF_HOME=/scratch/users/nus/$USER/.cache/huggingface, huggingface_hub
# will look under that directory and may not read an existing login token from
# ~/.cache/huggingface/token. For gated/private repos, either pass HF_TOKEN with
# qsub, read ~/.cache/huggingface/token explicitly in Python, or copy the token to
# $HF_HOME/token before downloading. Never print the token in logs.

python - <<'PY'
import os
from pathlib import Path
from huggingface_hub import snapshot_download

repo_id = os.environ["HF_REPO_ID"]
repo_type = os.environ.get("HF_REPO_TYPE", "model")
local_dir = os.environ["HF_LOCAL_DIR"]
home_token_path = Path.home() / ".cache" / "huggingface" / "token"

token = os.environ.get("HF_TOKEN") or None
if token is None and home_token_path.exists():
    token = home_token_path.read_text().strip() or None

print(f"Downloading repo_id={repo_id}")
print(f"repo_type={repo_type}")
print(f"local_dir={local_dir}")
print(f"HF_HOME={os.environ.get('HF_HOME', '<unset>')}")
print(f"home_token_exists={home_token_path.exists()}")
print(f"token_length={len(token) if token else 0}")

path = snapshot_download(
    repo_id=repo_id,
    repo_type=repo_type,
    local_dir=local_dir,
    local_dir_use_symlinks=False,
    resume_download=True,
    token=token,
)

print(f"Done: {path}")
PY

echo "Disk usage:"
du -sh "$HF_LOCAL_DIR"

echo "Top-level files:"
find "$HF_LOCAL_DIR" -maxdepth 2 -type f | sed "s#^$HF_LOCAL_DIR/##" | sort | head -200
```

Submit examples:

```bash
# Public model
qsub -v HF_REPO_ID=OpenOneRec/OneRec-8B-pro,HF_REPO_TYPE=model,HF_LOCAL_DIR=/scratch/users/nus/$USER/models/OpenOneRec-OneRec-8B-pro-hf hf_snapshot_download.pbs

# Public dataset
qsub -v HF_REPO_ID=HuggingFaceFW/fineweb,HF_REPO_TYPE=dataset,HF_LOCAL_DIR=/scratch/users/nus/$USER/datasets/HuggingFaceFW-fineweb hf_snapshot_download.pbs

# Gated/private repo, assuming HF_TOKEN is already exported in the submitting shell
qsub -v HF_REPO_ID,HF_REPO_TYPE,HF_LOCAL_DIR,HF_TOKEN hf_snapshot_download.pbs
```

## Token Handling

On ASPIRE, the user may already be logged in under the default home token path:

```text
~/.cache/huggingface/token
```

If a PBS script sets `HF_HOME=/scratch/users/nus/$USER/.cache/huggingface`, `huggingface_hub` will use that scratch cache and may stop seeing the home token. Gated/private models or datasets can then fail with `401 Unauthorized` even though `huggingface-cli whoami` worked earlier on the login node.

Robust options:

- In the PBS Python block, explicitly read `Path.home() / ".cache/huggingface/token"` and pass `snapshot_download(token=token)`.
- Or export `HF_TOKEN` before submission and use `qsub -v HF_TOKEN,...`.
- Or, if using scratch `HF_HOME`, copy the token to `$HF_HOME/token` with permissions locked down. Do not echo or print the token.

Safe checks that do not leak the token:

```bash
python - <<'PY'
from pathlib import Path
p = Path.home() / ".cache" / "huggingface" / "token"
token = p.read_text().strip() if p.exists() else ""
print(f"home_token_exists={p.exists()}")
print(f"home_token_length={len(token)}")
PY

python - <<'PY'
from huggingface_hub import HfApi
try:
    info = HfApi().whoami()
    print("whoami_ok=True")
    print("name=" + str(info.get("name", "<unknown>")))
except Exception as exc:
    print("whoami_ok=False")
    print(type(exc).__name__ + ": " + str(exc)[:200])
PY
```

## Checks

Use these after submission:

```bash
qstat -u "$USER"
tail -f hf_snapshot_download.<jobid>.log
du -sh /scratch/users/nus/$USER/models/<repo-dir>
find /scratch/users/nus/$USER/models/<repo-dir> -maxdepth 1 -type f | sort
find /scratch/users/nus/$USER/models/<repo-dir> -name "*.safetensors" -o -name "*.bin" | wc -l
```

For sharded models, compare the shard count and names against HuggingFace's file list. Typical signals of a healthy model download include `config.json`, tokenizer files, index files such as `model.safetensors.index.json` when applicable, and all referenced shard files.

## Troubleshooting

- If `git lfs` works on the login node but fails inside PBS, switch to the `snapshot_download` template instead of trying to repair LFS in the job.
- If the job exits quickly, inspect the PBS log first; common causes are a missing or invalid `HF_TOKEN`, typo in `HF_REPO_ID`, unavailable queue/resources, or no scratch permission.
- If a gated/private repo returns `401 Unauthorized`, first check `HF_HOME`, the token path used inside PBS, and whether `HF_TOKEN` was exported through `qsub -v`.
- If the job appears stuck, check whether the log is still appending, whether `du -sh` on the target directory is growing, and whether new shard files are appearing.
- If home quota fills, verify `HF_LOCAL_DIR` points to `/scratch/users/nus/$USER/...`; avoid storing model shards in `$HOME`.
- If a partial directory exists, rerun the same PBS job with the same `HF_LOCAL_DIR`; `snapshot_download(..., resume_download=True)` should reuse completed files.

The known successful OneRec example path was:

```text
/scratch/users/nus/e1538xxx/models/OpenOneRec-OneRec-8B-pro-hf
```

Treat that as an example of the desired scratch layout, not as the only valid destination.
