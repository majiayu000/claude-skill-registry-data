---
name: ai-supply-chain
description: >
  Attack the ML/LLM supply chain — poisoned models, datasets, plugins, and unsafe model
  deserialization. Load when an app loads third-party models/weights (HuggingFace, .pt/.pkl/.h5),
  installs ML deps, uses plugins/extensions, or fine-tunes on external data. Signals: torch.load,
  pickle model files, model hub downloads, plugin marketplace, RAG over external corpora.
domain: ai-ml
type: technique
stability: learning
modes: [pentest, defense, bugbounty]
severity: critical
owasp_llm: [LLM03:2025-Supply-Chain, LLM04:2025-Data-and-Model-Poisoning]
cwe: [CWE-502, CWE-1357]
tools: [fickling, modelscan]
schema_version: 1
---

# ML/LLM supply-chain attacks

## When it applies
The target consumes third-party ML artifacts: downloaded model weights, datasets, tokenizers,
plugins/extensions, or fine-tuning data. Each is code or data that runs with the app's trust.

## Why it works
Model files are frequently **pickle-based** (`torch.load`, `.pkl`, joblib) — loading them executes
arbitrary code (`__reduce__`), so a malicious model on a hub is RCE on whoever loads it. Datasets
and RAG corpora poison behavior; plugins/extensions run with the assistant's privileges; typosquatted
ML packages inject code at install.

## Method
1. **Unsafe model deserialization (RCE)**: if the app `torch.load`/`pickle.load`s a model you can
   supply or influence, craft a pickle with a `__reduce__` payload (`fickling`), or scan a suspect
   model (`fickling`, `modelscan`) for embedded code. Prefer safetensors as the safe alternative.
2. **Model/dataset poisoning**: contribute or substitute a model/dataset that carries a backdoor
   (trigger phrase → attacker-chosen output) or degrades safety — relevant when the app auto-pulls
   "latest" from a hub or fine-tunes on user/external data.
3. **Plugin / extension abuse**: a malicious or over-permissioned plugin the assistant loads →
   data access, tool abuse (→ `ai-agent-tool-abuse`).
4. **Dependency attacks**: typosquat/dependency-confusion on ML packages (→ `web-dependency-confusion`);
   compromised `requirements`.
5. **Provenance checks**: verify signatures/hashes, pinned versions, and safetensors usage.

## Gotchas
- `.pt`/`.bin`/`.pkl` = code execution on load; `.safetensors` = data only. The file format is the tell.
- Auto-updating to a hub's "latest" model/plugin is the poisoning entry point — flag it.
- Prove RCE with a benign payload (OOB callback), never a destructive one; mind scope/RoE.

## Verify success
Code execution when a crafted model/artifact is loaded (OOB beacon), a demonstrated backdoor
trigger, or a poisoned dependency/plugin executing in the app's context.

## References
OWASP LLM Top 10 (2025) LLM03/LLM04; `fickling` & `modelscan`; safetensors; "pickle is not secure".
