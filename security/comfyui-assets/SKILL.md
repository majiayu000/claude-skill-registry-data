---
name: comfyui-assets
description: Stage ComfyUI workflow input media through server uploads, use returned server names instead of guessed paths, extract all file-shaped outputs from history, download outputs safely, and keep project-relative media records.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# ComfyUI Assets

## Read

- `../../references/COMFYUI_NATIVE_API.md`
- `../../references/COMFYUI_SECURITY.md`

## Input procedure

1. Confirm the local source file exists.
2. Upload it as an input asset.
3. Record the returned `name`, `subfolder`, and `type`.
4. Patch the workflow input using those returned values or the exact loader format required by the live node schema.
5. Do not copy arbitrary host filesystem paths into workflow JSON.

Bundled command:

```text
python scripts/comfyui_control.py upload PATH --subfolder project-inputs
```

## Output procedure

1. Read the completed history record.
2. Inspect every node output for file-shaped records containing `filename`.
3. Preserve the producing node ID.
4. Download through `/view` using filename, subfolder, and type.
5. Sanitize local filenames and keep results under the project output directory requested by the user.

Bundled commands:

```text
python scripts/comfyui_control.py outputs PROMPT_ID
python scripts/comfyui_control.py download PROMPT_ID --out-dir 04_generation/comfyui/outputs
```

## Done

Inputs use server-recognized references and outputs are downloaded without arbitrary path construction or loss of producing-node identity.
