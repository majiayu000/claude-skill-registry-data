---
name: lifecycle/compile-jit-modelfile
description: Build a JIT Modelfile that hardcodes current context into SYSTEM/TEMPLATE/PARAMETER and creates a temporary Ollama model. Use when you need a hyper-focused ephemeral model.
---

# Compile JIT Modelfile

Capabilities
- freeze_system_state: inject task/system context into Modelfile SYSTEM.
- inherit_base_layers: set FROM to a cached base (e.g., llama3) to avoid copying weights.
- set_hyperfocused_params: set temperature/ctx/stop for the micro-task.
- write_modelfile_artifact: emit Modelfile to disk.
- build_ephemeral_model: `ollama create {temp_name} -f Modelfile`.

Inputs
- base_model, system_text, template, params, temp_name, modelfile_path.

Outputs
- build result, temp model name, modelfile path.
