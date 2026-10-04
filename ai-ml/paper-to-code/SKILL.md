---
name: paper-to-code
description: Read an ML/robotics research paper PDF, extract its key concepts, contributions, algorithms, losses, training tricks, architectures, and pipeline stages, then index a target codebase and map each paper item to its implementation — noting what is actually used vs. dead, partial, or missing. Use when the user wants to understand how a paper is implemented in a repo, audit a release against its paper, or onboard onto a research codebase.
argument-hint: <path/to/paper.pdf> <path/to/repo>
---

# Paper → Code Mapping

Inputs: `$1` = path to the research paper PDF, `$2` = path to the repository on disk.
If either is missing from `$ARGUMENTS`, ask the user for it before doing anything else.
Verify both paths exist (and that `$2` is a directory) before starting.

This skill is for **machine learning and robotics** papers. Work in four phases. Do not skip the checkpoint after Phase 1.

## Phase 1 — Extract the paper's claims

Read the **entire** paper with the Read tool, including appendices and supplementary material — algorithms, hyperparameter tables, and implementation details are usually in the appendix. PDFs over 10 pages require the `pages` parameter (max 20 pages per request); get the page count first (`pdfinfo` if available, otherwise probe with Read) and read in chunks until you've covered every page.

Build an inventory with stable IDs so the mapping table can reference them:

| Prefix | Category | What to capture |
|--------|----------|-----------------|
| C# | Concepts | Core ideas/definitions the paper introduces or relies on |
| N# | Contributions | The explicitly claimed contributions (usually bulleted in the intro) |
| A# | Algorithms | Named algorithms / pseudocode blocks, with their Algorithm numbers |
| L# | Losses & objectives | Every loss term and objective, with equation numbers and weighting coefficients; for RL: reward functions, advantage estimators, value targets |
| T# | Training tricks | Warmup, LR schedules, freezing/unfreezing schedules, curriculum, EMA, gradient clipping, augmentations, initialization tricks, mixed precision, replay buffers, exploration schedules, domain randomization, sim-to-real transfer tricks |
| M# | Architectures | Model components: backbones, attention variants, adapters, policy/value/critic networks, encoders/decoders, perception modules, controllers (MPC, PID, impedance), state estimators |
| S# | Stages | Pipeline stages: data collection/teleoperation, preprocessing, pretraining → finetuning → distillation, sim training → real deployment, inference-time procedures (beam search, action chunking, test-time adaptation) |
| E# | Environment & I/O | (Robotics/RL) Simulators, benchmarks, datasets, observation spaces, action spaces and their parameterization (delta EEF, joint pos, etc.), control frequencies, hardware interfaces |

For each item record:
- **Name** and a 1–2 sentence description
- **Paper location** — section, equation, algorithm, figure, or table number
- **Key hyperparameters/symbols** (e.g., τ = 0.07, λ_KL = 0.1, horizon H = 16)
- **Code-search keywords** — names you'd grep for, including both the math name and common implementation names (e.g., "contrastive loss" ↔ `info_nce`, `clip_loss`; "temperature" ↔ `tau`, `temp`; "action chunking" ↔ `chunk_size`, `horizon`)

**Checkpoint:** present the inventory as a compact table before touching the code, so the user can correct or prioritize items.

## Phase 2 — Index the codebase (subagent fan-out)

Do the recon yourself, then **divide the indexing across parallel subagents** rather than reading every module in the main context.

1. **Recon (main context):** directory tree (2–3 levels), package config (`setup.py`/`pyproject.toml`/`package.xml` for ROS), README, config files (YAML/Hydra/gin/argparse defaults), and launch files. Use this to choose the partition for step 2.
2. **Fan out Explore agents** — launch them in a single message so they run concurrently. Partition by responsibility (typical: one agent per top-level package, e.g. model/architecture code, training pipeline + data loading, eval/inference/deployment, scripts/configs). Each agent's prompt must include:
   - its assigned directories,
   - the relevant inventory items (IDs, descriptions, and code-search keywords from Phase 1) it should look for,
   - instructions to return: entry points it found, a module index (path → purpose → key classes/functions), a mechanism catalog (model classes, losses, reward/cost functions, optimizers/schedulers, data pipeline ops, environment wrappers, controllers, config flags with defaults), and candidate `file:line` locations for each assigned inventory item.
   For small repos (≲20 source files), 1–2 agents or direct reading is fine — don't over-shard.
3. **Merge (main context):** combine the agents' summaries into one entry-point list, module index, and mechanism catalog. Entry points are the ground truth for "used" in Phase 3.

## Phase 3 — Map paper → code

For each inventory item, search for its implementation (symbol names, equation variable names, comments citing the paper or equation numbers, config keys) and assign a status:

- ✅ **Implemented & used** — wired into an executed path. Cite the definition (`file:line`) AND where it's invoked from an entry point.
- ⚠️ **Implemented but NOT used** — defined but never called/instantiated, behind a default-off flag, commented out, or in an unreachable branch. State the evidence for why you concluded it's unused.
- 🔶 **Partial / divergent** — exists but differs from the paper: simplified variant, missing term, different hyperparameter or default. Describe the difference precisely.
- ❌ **Not found** — no implementation located (note: may live in a separate/private repo; say so if the README hints at it).

The subagents' candidate locations from Phase 2 are leads, not conclusions — verify usage tracing in the main context (or with follow-up agents for large repos).

Rules for this phase:
- **Symbol presence is not usage.** Verify "used" by tracing from entry points: is the flag on by default in the shipped configs? Is the loss term actually added to the total loss? Is the module in `forward()`? Is the stage invoked by the launch/train scripts?
- **Compare hyperparameters:** paper values vs. config defaults. Collect divergences.
- **Don't trust the README** — verify claims in code.
- **Reverse pass:** list significant mechanisms in the code that the paper never mentions (engineering extras, extra losses, stability hacks). These are often the most interesting findings.

## Phase 4 — Report

Produce a markdown report with these sections:

1. **Paper summary** — 3–5 bullets.
2. **Paper inventory** — the Phase 1 table (final, corrected version).
3. **Codebase index** — compact annotated tree with one-line purposes per module.
4. **Mapping table** — `ID | Paper item | Paper loc | Implementation (file:line) | Status | Notes`.
5. **Unused / dead implementations** — each with the evidence trail.
6. **Code-only mechanisms** — things in the code the paper doesn't mention.
7. **Divergences** — paper vs. code differences worth flagging (hyperparameters, simplified algorithms, missing loss terms).
8. **Open questions** — anything you couldn't resolve.

Use clickable `file:line` references throughout. **Write the complete report** (all eight sections, including the full Phase 1 inventory — not a summary) **to `<repo>/docs/paper-code-map.md`**, creating `docs/` if needed. If that file already exists and you didn't create it this session, ask before overwriting. Then present the key findings in the conversation and link to the saved file.
