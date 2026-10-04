---
name: evo-seismic-phase-picking
description: Runs SeisBench pretrained PhaseNet model on ObsPy Streams to detect P and S wave arrivals, extracts pick indices, and writes results to CSV.
---

# evo-seismic-phase-picking

## Overview
Runs SeisBench PhaseNet model inference on preprocessed ObsPy Streams to detect P and S wave arrivals. Extracts pick indices mapped to original sample coordinates and writes CSV output.

## Key Knowledge
- Use PhaseNet with "stead" weights for best generalization
- P_threshold=0.3, S_threshold=0.3 for good recall
- model.classify() handles sliding windows automatically
- Convert pick times back to original array indices using UTCDateTime math
- Output CSV: file_name, phase, pick_idx

## Usage
```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-seismic-phase-picking/scripts')
from utils import process_all_traces_to_csv, load_phasenet_model, run_phase_picking

# Full pipeline
df = process_all_traces_to_csv('/root/data/', '/root/results.csv')

# Or step by step
model = load_phasenet_model('stead')
classify_out = run_phase_picking(model, stream)
```

## Functions
- `load_phasenet_model(pretrained)` - Load PhaseNet model
- `run_phase_picking(model, stream)` - Run classify on stream
- `extract_picks_to_dataframe(classify_out)` - Get picks as DataFrame
- `convert_pick_to_original_index(pick_time, start, dt)` - Time to index
- `process_single_trace(model, npz_path, file_name)` - Process one file
- `process_all_traces_to_csv(data_dir, output_csv)` - Process all files
