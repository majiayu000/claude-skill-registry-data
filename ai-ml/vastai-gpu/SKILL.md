---
name: vastai-gpu
description: Rent a GPU on vast.ai, run experiments on it over SSH/rsync, pull artifacts back, and destroy it. Use when a task needs a GPU (training, CUDA, large-model inference).
---

# Run GPU experiments on vast.ai

You rent a GPU instance with the native `vastai` CLI, wait for it with `vastai-connect`
(which writes an SSH alias), then work with plain `ssh`/`rsync`. Money is spent per hour
from the moment an instance is created until it is **destroyed**. Never leave one behind.

## Prerequisites (check once)

```bash
vastai show instances --raw   # errors if vastai isn't installed or the API key isn't set
```

If missing: have the user register a public SSH key and create an API key at
https://cloud.vast.ai/manage-keys/, then:

```bash
uv tool install vastai && vastai set api-key <key>
uv tool install git+https://github.com/Yusuke710/vastai-skill.git
```

## 1. Find and rent

```bash
# Cheapest matching offers first. GPU names use underscores: RTX_3060, RTX_4090, A100_SXM4...
vastai search offers 'gpu_name=RTX_3060 num_gpus=1 reliability>0.98 dph<0.45' -o 'dph' --raw

vastai create instance <offer_id> --image vastai/pytorch:latest --disk 30 --ssh --raw
# → {"success": true, "new_contract": <instance_id>}
```

- Sanity-check the offer's `dph_total` ($/hr) against what the task deserves before renting.
- **Image:** default to `vastai/pytorch:latest` — its CUDA base layers are cached on most
  vast.ai hosts (boot-to-SSH ≈ 2–3 min). Other images usually download cold.
- `--disk` cannot be resized later; size it for datasets + checkpoints.
- The `new_contract` value is your instance id — the only instance you own.
- Running several instances? `vastai label instance <id> <name>` and use a distinct
  `--alias` for each.

## 2. Wait until reachable

```bash
vastai-connect <instance_id> --alias vast-gpu  # blocks until SSH works; then `ssh vast-gpu` / rsync work
```

Typical wait is 1–3 minutes. On timeout (5 min default) or any stall later (crawling
downloads, broken SSH auth): destroy and rent a different offer — re-renting beats
debugging. Cheap consumer hosts are a lottery; datacenter GPUs (A100/H100) are usually
more reliable.

## 3. Work over plain ssh/rsync

Normal remote-Linux workflow from here — nothing vast.ai-specific. Reminders, not recipes:

- rsync the project over gitignore-filtered so junk (.venv, data) doesn't cross the wire.
- Sanity-check that torch actually sees the GPU before paying for a long run.
- Detach long jobs so they survive SSH drops, and capture the exit code.
- **Before destroying**, pull back artifacts worth keeping (weights, logs, results) —
  they exist only on the instance. Check with the user if unsure what to keep.

## 4. Destroy the instance

```bash
vastai destroy instance <instance_id>
vastai show instances --raw              # verify it's gone; [] means nothing is billing
```

- **Destroy, never `stop`** — stopped instances still bill storage and may be unable to restart.
- **Only destroy instance ids you created in this session** (the `new_contract` values you
  received). Other instances — even ones with a familiar label or the same image — may
  belong to another job or agent running in parallel. Report unknown instances to the
  user; never "clean them up".
- If you intentionally leave an instance running (e.g. a long training job), tell the user
  explicitly: instance id, $/hr, and how to destroy it.
