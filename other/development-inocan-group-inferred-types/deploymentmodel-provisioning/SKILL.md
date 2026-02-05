---
name: deployment/model-provisioning
description: Build and provision Ollama models from Modelfiles, verify health, and hot-swap personas. Use to translate Modelfile text into runnable models.
---

# Model Provisioning

Capabilities
- write_modelfile_artifact: assemble FROM/ADAPTER/PARAMETER/SYSTEM/TEMPLATE into a Modelfile.
- execute_build_command: run `ollama create {name} -f Modelfile`.
- verify_model_health: ping the new model with a test prompt.

Dependencies
- ops-chief-of-staff (optional pipeline orchestration)
- proxy-aware-fetcher (if remote pulls needed)

Outputs
- build result, model name, health check response.
