---
name: uefn-vfx-niagara
description: Create or edit a Niagara System, emitter, module, renderer or user variable in the lab via the UEFN MCP (51/54 tools ok). Use for VFX work; only `tool-ok` or `proven` recipes, rest listed as not verified.
last_reviewed: 2026-10-16
sources: [original]
---

# uefn-vfx-niagara (MVP experimental, B9)

Source: `Claude/docs/mcp/vfx-niagara.md`, `recipes.json`, `SKILLS-PROPOSAL.md` B9. Read first: skills `uefn-mcp-lab-guard` and `uefn-create-use-remove-one-script`.

## Rules
- Paths in GUID form: lab root `/09e4e8d3-83f9-4ee0-9777-072ed3984380/root_ai_lab`.
- The guard is never bypassed; a refusal is reported verbatim. If a recipe fails: report the exact error and STOP.
- NEVER call `GetDynamicInputSchema` on a non-dynamic input: it crashed the editor. Use `GetAvailableDynamicInputs` / `GetDynamicInputSchemaFromAsset` only.
- Must NOT: write to `/Niagara/...` templates (source only).

## Recipes `tool-ok` or `proven` (recipes.json, toolset `NiagaraToolsets.*`)
- Create/remove: `NiagaraToolset_System/CreateNiagaraSystem {assetName, assetPath: <lab>/Fx, templateSystem: /Niagara/DefaultAssets/Templates/Systems/MinimalLightweight.MinimalLightweight}` (source allowed because result lands in lab); cleanup `AssetTools/delete {path:<lab>/Fx}`.
- Edit: `AddEmitter`, `RemoveEmitter`, `AddModule`, `RemoveModule`, `AddRenderer`, `RemoveRenderer`, `RemoveSetParameterEntry`, `AddUserVariables`, `RemoveUserVariables`, `SetSystemData`, `SetEmitterData`, `SetRendererData`, `SetStackInputData`, `SetModuleEnabled`.
- Read: `GetSystemSummary`, `GetSystemCompileState`, `GetSystemDependencies`, `GetStackIssues`, `GetEmitterSummary`, `GetEmitterTopology`, `GetModuleInputValues`, `GetStackInputData`, `GetRendererData`, `GetRendererSchema`, `NiagaraToolset_Assets/FindNiagaraScripts`, `GetNiagaraScriptDigest`, `NiagaraToolset_Info/UEnum_Info`.
- Component: `NiagaraToolset_Component/GetUserVariables`, `GetVariable`, `SetVariable`, `SetSystem`.

## Traps
- `FindNiagaraScripts` needs all of usages, visibilities, supportedUsages, bRecursive, bIncludeDeprecated, folderPath, name.
- `AddUserVariables` items are FLAT; `SetVariable` needs `{name,type,value}`.
- MinimalLightweight yields an empty emitter: use `AddEmitter` with a real template.
- Delete the NiagaraActor in the same script that spawned it. Payloads 48-56 KB per emitter.

## To try (not verified)
- `ApplyStackIssueFix`: unverified (replies an error but applies; effect not confirmed in recipes.json).
- `AddSetParametersModule`, `AddSetParameterEntry`: unverified in recipes.json.
- `GetDynamicInputSchema`: never call (editor crash).
