---
name: scout
description: Use when firmware binary analysis, attack surface mapping, or endpoint discovery is needed for a target
argument-hint: <firmware-path> [--rootfs <extracted-rootfs>] [--profile exploit] [--stages stage1,stage2]
---

# SCOUT — Firmware-to-Exploit Evidence Engine

SCOUT location: `/home/rootk1m/SCOUT`
Launcher: `/home/rootk1m/SCOUT/scout`
Runs output: `/home/rootk1m/SCOUT/aiedge-runs/`

## What SCOUT Does

Deterministic firmware analysis pipeline: firmware blob → unpack → profile → inventory → attack surface → findings → exploit chain evidence. Produces hash-anchored JSON artifacts at every stage.

```
Firmware blob → Extraction → Profile → Inventory → Surfaces → Findings → Handoff
```

## Pre-checks (auto-executed)

Firmware file info:
!`if [ -n "$1" ] && [ -e "$1" ]; then file "$1" 2>/dev/null && ls -lh "$1" 2>/dev/null; fi`

Recent SCOUT runs:
!`ls -lt /home/rootk1m/SCOUT/aiedge-runs/ 2>/dev/null | head -6 || echo "no runs yet"`

## Usage Patterns

### 1. Quick Deterministic Analysis (no LLM, most common)

```bash
/home/rootk1m/SCOUT/scout analyze <firmware.bin> \
  --ack-authorization --no-llm \
  --case-id <descriptive-id>
```

### 2. Analysis with Pre-extracted Rootfs (when binwalk extraction is weak)

```bash
/home/rootk1m/SCOUT/scout analyze <firmware.bin> \
  --ack-authorization --no-llm \
  --case-id <id> \
  --rootfs /path/to/extracted/rootfs
```

### 3. Specific Stages Only

```bash
# Available stages: tooling, extraction, structure, carving, firmware_profile,
#   inventory, endpoints, surfaces, graph, attack_surface, functional_spec,
#   threat_model, findings, llm_synthesis, dynamic_validation, emulation,
#   exploit_chain, exploit_autopoc, poc_validation, exploit_policy

/home/rootk1m/SCOUT/scout analyze <firmware.bin> \
  --ack-authorization --no-llm --case-id <id> \
  --stages tooling,extraction,structure,carving,firmware_profile,inventory
```

### 4. Rerun Stages on Existing Run

```bash
/home/rootk1m/SCOUT/scout stages /home/rootk1m/SCOUT/aiedge-runs/<run_id> \
  --no-llm --stages inventory,surfaces,findings
```

### 5. Full Exploit Profile (lab-gated, requires authorization)

```bash
/home/rootk1m/SCOUT/scout analyze <firmware.bin> \
  --ack-authorization --case-id <id> \
  --profile exploit \
  --exploit-flag lab \
  --exploit-attestation authorized \
  --exploit-scope lab-only
```

### 6. View Results

```bash
# TUI dashboard (interactive)
/home/rootk1m/SCOUT/scout tui /home/rootk1m/SCOUT/aiedge-runs/<run_id> --interactive

# TUI live-refresh
/home/rootk1m/SCOUT/scout tw /home/rootk1m/SCOUT/aiedge-runs/<run_id> -t 2

# One-shot summary
/home/rootk1m/SCOUT/scout to /home/rootk1m/SCOUT/aiedge-runs/<run_id>

# Web viewer
/home/rootk1m/SCOUT/scout serve /home/rootk1m/SCOUT/aiedge-runs/<run_id>
```

## Orchestrator Workflow

When user provides a firmware binary for analysis:

### Step 1: Run SCOUT Analysis

Execute SCOUT with appropriate flags. Default to `--no-llm` for deterministic results unless user requests LLM synthesis.

### Step 2: Read Key Artifacts

After SCOUT completes, read these artifacts from `aiedge-runs/<run_id>/`:

| Artifact | Path | Content |
|----------|------|---------|
| Profile | `stages/firmware_profile/firmware_profile.json` | OS type, arch, SDK, emulation feasibility |
| Inventory | `stages/inventory/inventory.json` | File/binary catalog, coverage metrics |
| Binary Analysis | `stages/inventory/binary_analysis.json` | Risky symbols, arch summary |
| Surfaces | `stages/surfaces/surfaces.json` | Network services, entry points |
| Source-Sink Graph | `stages/surfaces/source_sink_graph.json` | Taint path candidates |
| Findings | `stages/findings/pattern_scan.json` | Structured vulnerability findings |
| Kill Chains | `stages/findings/chains.json` | Complete attack path hypotheses |
| CVE Matches | `stages/findings/known_disclosures.json` | Known CVE matches |
| Web UI | `stages/web_ui/web_ui.json` | JS/HTML security patterns |
| Handoff | `firmware_handoff.json` | Contract for Terminator pipeline |

### Step 3: Summarize for User

Present findings organized by severity:
1. **Critical/High** findings with kill-chain paths
2. **Attack surface** summary (services, endpoints, entry points)
3. **Profile** (OS, arch, SDK, emulation feasibility)
4. **Recommended next steps** (Terminator tribunal, dynamic validation, manual review)

### Step 4: Handoff to Terminator (if warranted)

When findings are promising, use `firmware_handoff.json` to feed into Terminator's firmware pipeline:
```
fw-profiler → fw-inventory → fw-surface → fw-validator
```

## Run Directory Structure

```
aiedge-runs/<timestamp>_<sha256-prefix>/
├── manifest.json                    # input identity + policy
├── firmware_handoff.json            # handoff contract
├── stages/
│   ├── extraction/                  # extracted filesystem
│   ├── firmware_profile/            # OS/arch/SDK classification
│   ├── inventory/                   # file catalog + binary analysis
│   ├── surfaces/                    # attack surface + source-sink graph
│   ├── web_ui/                      # JS/HTML security patterns
│   └── findings/                    # vulnerabilities + kill chains
└── report/
    ├── report.json                  # aggregated report
    └── viewer.html                  # browser viewer
```

## Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `AIEDGE_PORTSCAN_TOP_K` | Port scan top-K | 1000 |
| `AIEDGE_PORTSCAN_BUDGET_S` | Port scan timeout | 120 |
| `AIEDGE_PRIV_RUNNER` | Privileged command prefix | (none) |
| `AIEDGE_LLM_CHAIN_TIMEOUT_S` | LLM synthesis timeout | 180 |
| `AIEDGE_LLM_CHAIN_MAX_ATTEMPTS` | LLM synthesis retries | 5 |

## Verification Scripts

```bash
# Evidence integrity
python3 /home/rootk1m/SCOUT/scripts/verify_analyst_digest.py --run-dir <run_dir>
python3 /home/rootk1m/SCOUT/scripts/verify_aiedge_analyst_report.py --run-dir <run_dir>

# Verified chain gates
python3 /home/rootk1m/SCOUT/scripts/verify_verified_chain.py --run-dir <run_dir>
python3 /home/rootk1m/SCOUT/scripts/verify_run_dir_evidence_only.py --run-dir <run_dir>
```

## Key Rules

1. **`--ack-authorization` is MANDATORY** for every analysis
2. **All artifact paths are run-dir-relative** — absolute paths in outputs are bugs
3. **No finding without evidence** — every finding requires file path, offset, hash, rationale
4. **Stages fail open, governance fails closed** — partial results over crashes, but promotion gates reject incomplete evidence
5. **`confirmed` status requires dynamic evidence** — no exceptions
6. **Exploit profile requires 3 extra flags**: `--exploit-flag lab --exploit-attestation authorized --exploit-scope lab-only`

## Gotchas
- Missing `--ack-authorization` flag causes immediate failure on authorized targets
- Without `--no-llm`, LLM API timeout on air-gapped environments blocks the entire pipeline
- Large firmware (>500MB) may exhaust /tmp — check disk space before extraction
