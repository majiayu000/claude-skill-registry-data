---
name: synthesis/grounded-audio-brief
description: Produce grounded audio briefs by chaining source-scoped input, citation verification, dialogue dramatization, and multi-speaker TTS orchestration. Use for “Audio Overview” style outputs.
---

# Grounded Audio Brief

Capabilities
- plan_pipeline: wire boundary manager + citation verifier + dramatizer + multi-speaker orchestrator.
- run_pipeline: execute stages with grounding and persona settings.
- package_output: return script, citations, and mixed audio ref.

Dependencies
- memory-linker
- tangible-memory
- dialogue-dramatizer
- multi-speaker-orchestrator

Inputs
- grounded notes, personas, voice config.

Outputs
- scripted dialogue with citations + final audio reference + metadata.
