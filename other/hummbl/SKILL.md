---
name: hummbl
description: Structured reasoning framework for AI agents — turns plans, hypotheses, observations, evaluations, decisions, and reflections into durable, inspectable artifacts
version: 0.1.0
execution-mode: advisory
argument-hint: "[ReasoningTrace | ReasoningProtocol | TraceAnalyzer | TracePlanner]"
category: fleet-ops
status: candidate
---
# HUMMBL

Structured reasoning framework for AI agents — turns plans, hypotheses, observations, evaluations, decisions, and reflections into durable, inspectable artifacts. Provides composable reasoning engines, inspectable traces, and domain-specific protocols. It formalizes how agents think, not just what they do.

## When to Use

- Building structured reasoning traces (steps, topologies, step types)
- Applying reasoning protocols (Scientific Method, Structured Tool Use)
- Analyzing and scoring reasoning traces
- Planning experiments with trace-driven methodology
- Capturing autoresearch and tool-use patterns for evaluation

## Usage

```bash
[hummbl] ReasoningTrace(steps=[ReasoningStep(...)])
[hummbl] TraceAnalyzer().analyze(trace)
[hummbl] ScientificMethod().run(hypothesis, observations)
```

## Python API

```python
from hummbl import (
    # Reasoning core
    ReasoningTrace,
    ReasoningStep,
    ReasoningTopology,
    StepType,
    # Protocols
    ReasoningProtocol,
    ScientificMethod,
    StructuredToolUse,
    # Analysis & scoring
    TraceAnalyzer,
    TraceScore,
    DimensionScore,
    StructuredToolUseScorer,
    # Planning
    ExperimentPlan,
    PlannedExperiment,
    TracePlanner,
    # Capture
    AutoresearchCapture,
    ToolUseCapture,
    # Typed tuples
    TypedTuple,
    AttestTuple,
    ContractTuple,
    DCTTuple,
    DCTXTuple,
    EvidenceTuple,
    SystemTuple,
)
```

## Key Concepts

- **Reasoning traces**: Ordered sequences of `ReasoningStep` objects with `StepType` classification and `ReasoningTopology` (linear, branching, etc.).
- **Protocols**: Composable reasoning engines — `ScientificMethod` (hypothesis → test → evaluate) and `StructuredToolUse` (plan → execute → verify).
- **Trace analysis**: `TraceAnalyzer` inspects traces; `StructuredToolUseScorer` scores tool-use quality with `DimensionScore` and `TraceScore`.
- **Experiment planning**: `TracePlanner` generates `ExperimentPlan` objects containing `PlannedExperiment` entries.
- **Capture patterns**: `AutoresearchCapture` and `ToolUseCapture` record agent behavior for later analysis.
- **Typed tuples**: Governance-aware tuple types (DCT, DCTX, Contract, Evidence, Attest, System) for structured artifact provenance.

## Install

```bash
cd /work/active/oss/packages/python/hummbl/
pip install -e ".[test]"
```

## Package

- **Repo**: `hummbl-io/oss`
- **Path**: `packages/python/hummbl/`
- **License**: Apache 2.0
- **Dependencies**: stdlib only
