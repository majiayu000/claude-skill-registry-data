---
name: get-results
description: Retrieve and analyze simulation results from a Coval run. Use when user wants to review evaluation outcomes or debug agent behavior.
argument-hint: "[run-id or simulation-id]"
---

# Get Simulation Results

Retrieve results for `$ARGUMENTS`.

## Workflow

### If Run ID Provided

List all simulations for the run:

```bash
coval simulations list --run-id <run_id> --format json
```

### If Simulation ID Provided

Get detailed simulation data:

```bash
coval simulations get <simulation_id> --format json
```

This returns:
- Status (COMPLETED, FAILED)
- Test case ID
- Transcript (conversation history)
- Timestamps
- Error message (if failed)

### Step 2: Analyze Results

For each simulation, extract:

| Field | Description |
|-------|-------------|
| `status` | COMPLETED or FAILED |
| `test_case_id` | Which test case was run |
| `transcript` | Full conversation |
| `has_audio` | Whether audio is available |
| `error_message` | Failure reason (if any) |

### Step 3: Present Summary

```
## Results for Run <run_id>

| Simulation | Status | Test Case | Audio |
|------------|--------|-----------|-------|
| sim_abc123 | COMPLETED | tc_xyz | Yes |
| sim_def456 | FAILED | tc_uvw | No |

### Failed Simulations
- sim_def456: "Connection timeout"

### View Details
`coval simulations get <sim_id>`

### Download Audio
`coval simulations audio <sim_id> -o output.wav`
```

## Filtering

List simulations with filters:

```bash
coval simulations list --run-id <run_id> --filter "status=FAILED"
coval simulations list --run-id <run_id> --filter "has_audio=true"
```
