---
name: uefn-ui-widgets
description: Create and edit UEFN Widget Blueprints via MCP (widget tree, text, Verse field, MVVM bindings, animations). Use only in the lab; recipes in recipes.json.
last_reviewed: 2026-10-16
sources: [original]
---

# uefn-ui-widgets

Sources: `Claude/docs/mcp/ui-widgets.md`, entry B1 of `SKILLS-PROPOSAL.md`, `recipes.json`.
Cross-cutting skills to always follow: `uefn-mcp-lab-guard` (lab guard) e `uefn-create-use-remove-one-script` (create, use, remove in ONE script).

## Rules
- Paths always in GUID form: `{lab}` = `/<guid>/<project>` (e.g. `/09e4e8d3-.../root_ai_lab`). `/root_ai_lab/...` is refused by the editor.
- `{bp}` = `{lab}/UI_X/WBP_X.WBP_X`; widget parts: `{bp}:WidgetTree.<Name>`.
- The guard is not bypassed: a refusal is reported as is. If a recipe fails: report the exact error and STOP (no creative retries).
- Call: `call_tool {toolset_name, tool_name, arguments}`. After every change: `CompileWidgetBlueprint` and read the result (`save_assets` returning true is NOT enough).
- Cleanup: `AssetTools/delete {path: <bp without .Name>}`.

## Verified recipes
Toolset: `UMGToolSet.UMGToolSet`, `VerseFieldsToolset.VerseFieldsToolset`, `MVVMToolset.MVVMToolset`, `WidgetAnimationToolset.WidgetAnimationToolset`.
1. `UMGToolSet/CreateWidgetBlueprint {"folderPath":"{lab}/UI_X","assetName":"WBP_X","parentClass":{"refPath":"/Script/UMG.UserWidget"}}`
2. `UMGToolSet/AddWidget {"widgetBlueprint":{"refPath":"{bp}"},"widgetClass":{"refPath":"/Script/UMG.Overlay"},"widgetDisplayName":"Root","parentWidget":null}`; children: `parentWidget {"refPath":"{bp}:WidgetTree.Root"}` (the parent must be a panel).
3. Text: `UMGToolSet/ReplaceWidgetWithTemplate {"widgetBlueprint":{"refPath":"{bp}"},"widgetToReplace":{"refPath":"{bp}:WidgetTree.<Name>"},"templateClass":{"refPath":"/Game/Valkyrie/UMG/UEFN_TextBlock.UEFN_TextBlock_C"}}` (the only way to get text; the widget to replace is e.g. an Image).
4. `UMGToolSet/GetWidgets {"widgetBlueprint":{"refPath":"{bp}"}}`; `CompileWidgetBlueprint {"widgetBlueprint":{"refPath":"{bp}"}}`
5. `VerseFieldsToolset/AddVerseField {"widgetBlueprint":..,"fieldName":"Op","spec":{"type":"float","defaultValue":"0.5"}}` (writeAccess only "" or `<public>`); cleanup `RemoveVerseField`.
6. `VerseFieldsToolset/BindWidgetPropertyToVerseField {"widgetBlueprint":..,"verseFieldName":"Op","targetWidget":{"refPath":"{bp}:WidgetTree.<Name>"},"widgetPropertyPath":"RenderOpacity"}` -> GUID binding.
7. `MVVMToolset/CreateViewBinding {"widgetBlueprint":..,"sourceContext":null,"sourcePropertyPath":"<campo>","destinationContext":{"refPath":"{bp}:WidgetTree.<Name>"},"destinationPropertyPath":"Text","conversionName":""}`; `SetBindingMode {..,"bindingId":"<guid>","mode":"TwoWay"}`; `ListWidgetViewBindings {"widgetBlueprint":..}`; cleanup `RemoveWidgetViewBinding {widgetBlueprint, bindingId}`.
8. `MVVMToolset/AddViewModelToWidget {"widgetBlueprint":..,"viewModelClass":{"refPath":"/Script/SimpleVotingOptionRuntime.VotingOptionViewModel"}}` (returns null; no cleanup: delete the blueprint).
9. `WidgetAnimationToolset/CreateWidgetAnimation {"widgetBlueprint":..,"animationName":"FadeIn","lengthSeconds":2.0}`; `AddWidgetToAnimation {..,"animation":{"refPath":"{bp}:FadeIn"},"objectToBind":{"refPath":"{bp}:WidgetTree.<Name>"}}`; `ListWidgetAnimations {"widgetBlueprint":..}`; cleanup `RemoveWidgetBinding {animation, bindingGuid}`, `RemoveWidgetAnimation`.

## To try (not verified)
- `UMGToolSet/AddUIComponent` (+ `MoveUIComponent`, `RemoveUIComponent`): guard-refused/rejected by the project (4 classes not allowed, 3 attempts). Do not retry.
- `MVVMToolset/AddViewModelProperty`: rejected, needs a ViewModel Blueprint that no tool creates.
- `MVVMToolset/CreateViewEventBinding`: unverified in recipes.json; accepts a wrong destination and the compile then fails while `save_assets` stays true; no tool removes the event binding.
- `ObjectTools/set_properties` / `get_properties` on the text (`values` = JSON string, camelCase): described in ui-widgets.md R2, non verified in recipes.json for this toolset.
- `MoveWidget`, `RenameWidgetAnimation` (resets `displayLabel`): unverified in recipes.json. Animation playback: unverified (needs a play session).

## Don't
Do not use AddWidget with `TextBlock`/`UEFN_TextBlock_C` (not allowed); do not declare it "done" if only `save_assets` is true; do not touch assets outside the lab folder.
