---
name: materials-screening
description: |
  材料科学筛选技能。用于固态电解质、催化剂等材料的候选筛选、
  属性预测和多目标优化排序。触发词包括"材料筛选"、"materials screening"等。
triggers:
  - 材料筛选
  - materials screening
  - 固态电解质
  - solid electrolyte
  - 材料发现
  - materials discovery
domain: materials_science
version: "1.0"
---

# Materials Screening Skill

## Overview
AI-powered materials discovery workflow for screening candidate materials based on target properties and constraints.

## Trigger Conditions
- User mentions materials screening, discovery
- Solid-state electrolyte research
- Catalyst design tasks

## Workflow

### Step 1: Define Objectives
Specify target properties and constraints:
- Ionic conductivity (max)
- Formation energy (min)
- Band gap (range)
- Stability threshold

### Step 2: Search Candidates
Query materials databases:
- Materials Project
- AFLOW
- OQMD

**Script**: `scripts/search_candidates.py`

See: `STRUCTURE_FAMILIES.md` for common structure families

### Step 3: Property Prediction
Use ML models for property prediction:
- GNN-based property prediction
- Formation energy estimation
- Stability assessment

**Script**: `scripts/predict_properties.py`

### Step 4: Ranking & Selection
Multi-objective optimization:
- Pareto frontier analysis
- Weighted scoring
- Constraint filtering

**Script**: `scripts/rank_materials.py`

## Output Format
```json
{
  "query": "solid electrolyte Li-ion",
  "candidates": [
    {
      "formula": "Li7La3Zr2O12",
      "structure_family": "garnet",
      "predicted_conductivity": 1e-3,
      "formation_energy": -3.2,
      "stability": "stable",
      "rank": 1
    }
  ],
  "total_screened": 1000,
  "passed_constraints": 50
}
```
