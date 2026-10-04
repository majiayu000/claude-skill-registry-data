---
name: unreal-blueprint-codegen
description: Programmatically generate Unreal Engine 5.x Blueprint and Widget Blueprint .uasset files from C++. Use when building a content generator for Fab/Marketplace samples, Quick-Start kits, tutorial assets, or editor utilities that mass-produce Blueprints, Widget Blueprints with UMG animations, or domain assets (dialogue, quest, ability data). Covers UBlueprint creation with full event-graph authoring (UK2Node_*, FBlueprintEditorUtils), UWidgetBlueprint hierarchies, UWidgetAnimation with MovieScene tracks and keyframes, two-pass compile, and the K2Node spawn idiom. Triggers on "create a Blueprint generator", "generate WBP from C++", "programmatically author event graph", "build dialogue/quest assets from code", "editor utility to generate marketplace samples", or any task involving FKismetEditorUtilities::CreateBlueprint, UWidgetBlueprintFactory, FBlueprintEditorUtils::AddMemberVariable, or UMovieScene2DTransformTrack.
---

# Unreal Engine Blueprint Code Generation (UE 5.4–5.7)

Generate complete `.uasset` files (Blueprints, Widget Blueprints, domain assets) from C++ in an editor module. Validated against UE 5.7. Most patterns work back to 5.4.

## When this skill applies

User wants to **author asset content programmatically** — variables, function graphs, event-graph wiring, widget hierarchies, UMG animations, custom asset graphs — instead of clicking through the editor. Typical use case: generating Marketplace sample content (Quick-Start, walkthrough, demo conversations) so it can be regenerated reproducibly instead of hand-pruning binary `.uasset` files.

If the user only wants runtime widget instantiation (`CreateWidget` / `WidgetTree->ConstructWidget` at game time), this skill is overkill — that's just normal UMG.

## Hard prerequisites

- **C++ editor module** with `Type=Editor` (or `UncookedOnly`). Python cannot author event graphs — `UEdGraph`/`UK2Node_*` are not exposed. Set up a `UBlueprintFunctionLibrary` in C++ and call its UFUNCTIONs from Python if a Python entry point is needed.
- Module must depend on at least: `UnrealEd`, `BlueprintGraph`, `Kismet`, `KismetCompiler`, `AssetTools`, `AssetRegistry`. Add `UMG`, `UMGEditor`, `MovieScene`, `MovieSceneTracks` for Widget Blueprints. See [assets/experiment-module-template/](assets/experiment-module-template/) for a working `.Build.cs`.
- IWYU: include each engine header explicitly. Forward-declare `UPackage`/`UObject` etc. in your own headers; pull full headers in `.cpp` only.

## The 30-second mental model

```
Asset = UPackage  +  UObject (e.g. UBlueprint / UWidgetBlueprint / UMyAsset)
                     |
                     +-- source UEdGraph (editor-only, what designers see)
                     |     +-- UK2Node_* / UEdGraphNode_* (the boxes)
                     |           +-- UEdGraphPin (the wires)
                     |
                     +-- generated UClass  <- produced by CompileBlueprint
                           +-- FProperty / UFunction (what code uses at runtime)
```

Spawn editor nodes onto a graph, wire their pins, then call `CompileBlueprint` to bake the generated class. Save the package.

## Decision tree

| Goal | Read |
|---|---|
| Add variables, functions, custom events, math nodes to a regular Blueprint | [references/k2node-cookbook.md](references/k2node-cookbook.md) |
| Build a Widget Blueprint with widget hierarchy | [references/widget-blueprint-cookbook.md](references/widget-blueprint-cookbook.md) |
| Add UMG animations (UWidgetAnimation + MovieScene tracks/keyframes) from C++ | [references/widget-blueprint-cookbook.md](references/widget-blueprint-cookbook.md) |
| The compiler says "function not found", `FindPinChecked` asserts, or a node has no pins | [references/two-pass-compile.md](references/two-pass-compile.md) — **read before debugging** |
| Need a working module skeleton to start from | [assets/experiment-module-template/](assets/experiment-module-template/) |
| Hit a weird Engine API quirk or version-specific issue | [references/caveats.md](references/caveats.md) |

## Standard workflow

For every generator function:

1. **Create / load package**: `CreatePackage(*FullPath)` then `Package->FullyLoad()`.
2. **Create the asset** with `FKismetEditorUtilities::CreateBlueprint(...)` (covers both `UBlueprint` and `UWidgetBlueprint` — pass the right Blueprint class + GeneratedClass).
3. **Build content** — variables, function graphs, widget tree, animations.
4. **Wire event graph / call user functions** — only AFTER an intermediate compile if the wiring references content created in step 3 (see two-pass-compile.md).
5. **`MarkBlueprintAsStructurallyModified` + `CompileBlueprint`** — once at the end (or twice, two-pass).
6. **Save**: `FAssetRegistryModule::AssetCreated(Asset)` + `Package->MarkPackageDirty()` + `UPackage::SavePackage(...)`.

Skeleton:

```cpp
#include "Engine/Blueprint.h"
#include "Kismet2/BlueprintEditorUtils.h"
#include "Kismet2/KismetEditorUtilities.h"
#include "AssetRegistry/AssetRegistryModule.h"
#include "UObject/SavePackage.h"

UBlueprint* CreateBP(const FString& PackagePath, const FString& AssetName, UClass* ParentClass)
{
    const FString FullPath = PackagePath / AssetName;
    UPackage* Package = CreatePackage(*FullPath);
    Package->FullyLoad();

    UBlueprint* BP = FKismetEditorUtilities::CreateBlueprint(
        ParentClass,                  // e.g. AActor::StaticClass() or UUserWidget::StaticClass()
        Package,
        FName(*AssetName),
        BPTYPE_Normal,
        UBlueprint::StaticClass(),    // or UWidgetBlueprint::StaticClass()
        UBlueprintGeneratedClass::StaticClass(),  // or UWidgetBlueprintGeneratedClass::StaticClass()
        FName("MyGenerator"));        // calling-context tag; any FName

    // ... build content here ...

    FBlueprintEditorUtils::MarkBlueprintAsStructurallyModified(BP);
    FKismetEditorUtilities::CompileBlueprint(BP);

    FAssetRegistryModule::AssetCreated(BP);
    Package->MarkPackageDirty();
    const FString Filename = FPackageName::LongPackageNameToFilename(
        Package->GetName(), FPackageName::GetAssetPackageExtension());
    FSavePackageArgs Args;
    Args.TopLevelFlags = RF_Public | RF_Standalone;
    UPackage::SavePackage(Package, BP, *Filename, Args);

    return BP;
}
```

## Critical rules (read these even if skipping cookbooks)

### 1. SetExternalMember BEFORE AllocateDefaultPins on UK2Node_CallFunction

```cpp
UK2Node_CallFunction* Node = NewObject<UK2Node_CallFunction>(Graph);
Node->FunctionReference.SetExternalMember(
    GET_FUNCTION_NAME_CHECKED(UKismetSystemLibrary, PrintString),
    UKismetSystemLibrary::StaticClass());
Node->AllocateDefaultPins();   // AFTER. Reverse and the node spawns pinless.
```

Same rule for `UK2Node_VariableSet/Get`: set the variable reference first, then `AllocateDefaultPins`.

### 2. MarkBlueprintAsStructurallyModified vs Modified

- **StructurallyModified**: any node added/removed, any variable added/removed, any pin topology change. Forces class layout regen.
- **Modified**: only property tweaks on existing nodes/vars (e.g. changed a default value).

For codegen, almost always use `MarkBlueprintAsStructurallyModified`.

### 3. Function calls must be in the exec chain or get pruned

Non-pure functions (with exec pins) must be wired into the exec chain. If you connect their data output without wiring exec, the BP compiler prunes the call and the data pin reads default. Symptom: warning *"X was pruned because its Exec pin is not connected"*.

```cpp
// WRONG — Compute is non-pure, exec not wired, gets pruned:
EvtThen->MakeLinkTo(SetCounter->GetExecPin());
ComputeRet->MakeLinkTo(CounterValPin);  // reads default, not actual return

// RIGHT — Compute in the chain:
EvtThen->MakeLinkTo(CallCompute->GetExecPin());
CallCompute->GetThenPin()->MakeLinkTo(SetCounter->GetExecPin());
ComputeRet->MakeLinkTo(CounterValPin);
```

### 4. Avoid (0,0) — auto-spawned default events live there

Both `AActor`-based BPs and Widget Blueprints auto-spawn placeholder events (BeginPlay, Tick, ActorBeginOverlap, PreConstruct, Construct) at `(0, 0)`. Position your nodes well off, e.g. `Y=-300`, `X=-400`. Otherwise the user opens the asset to a tangled mess.

### 5. Two-pass compile when nodes reference newly-created content

If you create a function `Compute` and then wire `CallCompute` referencing it in the same pass, `AllocateDefaultPins` on `CallCompute` runs before `Compute` is reflected on the generated class — the pins for `InValue`/`ReturnValue` won't exist, and `FindPinChecked` asserts. Fix: compile after building the function, *then* wire the call. Same for UMG animations referenced via `UK2Node_VariableGet`. See [references/two-pass-compile.md](references/two-pass-compile.md).

## Common UE 5.7 gotchas (full list in caveats.md)

- **`PlayAnimationByName` does NOT exist on `UUserWidget` in 5.7.** Only `PlayAnimation(UWidgetAnimation*, ...)`. Wire via `UK2Node_VariableGet` for the animation, not a string.
- **Animation `FName` must equal display label.** `UUserWidget::GetAnimationByName` matches `GetFName()`. Set both: `NewObject<UWidgetAnimation>(WBP, FName("SlideIn"), ...)` plus `Anim->SetDisplayLabel(TEXT("SlideIn"))`.
- **`Outer` hierarchy is load-bearing.** `UWidgetAnimation`'s outer must be the WBP. `UMovieScene`'s outer must be the animation. Wrong outer → animation does not appear in the editor's Animations panel.
- **`UE_DEFINE_GAMEPLAY_TAG_STATIC` for any tags the generated assets reference.** Runtime `UGameplayTagsManager::AddNativeGameplayTag` from inside a generator function is too late — the editor UI's tag tree is already built. Register at module load.
- **Python cannot reach `UEdGraph` / `UK2Node_*`.** The only way to author event graphs is C++. Expose your generator as `BlueprintCallable` UFUNCTIONs on a `UBlueprintFunctionLibrary` if Python invocation is desired.
- **`FBlueprintEditorUtils::AddFunctionGraph` does NOT spawn a Result node by default.** Only Entry. If your function returns a value, manually create one with `FGraphNodeCreator<UK2Node_FunctionResult>`.

## Quick FEdGraphPinType cheat sheet

```cpp
FEdGraphPinType T;
T.PinCategory = UEdGraphSchema_K2::PC_Boolean;            // bool
T.PinCategory = UEdGraphSchema_K2::PC_Int;                // int32
T.PinCategory = UEdGraphSchema_K2::PC_Real;
T.PinSubCategory = UEdGraphSchema_K2::PC_Float;           // float
T.PinSubCategory = UEdGraphSchema_K2::PC_Double;          // double
T.PinCategory = UEdGraphSchema_K2::PC_String;             // FString
T.PinCategory = UEdGraphSchema_K2::PC_Name;               // FName
T.PinCategory = UEdGraphSchema_K2::PC_Text;               // FText
T.PinCategory = UEdGraphSchema_K2::PC_Object;             // object ref
T.PinSubCategoryObject = AActor::StaticClass();           //   (with target class)
T.ContainerType = EPinContainerType::Array;               // wrap as TArray<>
T.ContainerType = EPinContainerType::Set;                 // TSet<>
T.ContainerType = EPinContainerType::Map;                 // TMap<>  (PinValueType for value)
```

Use with: `FBlueprintEditorUtils::AddMemberVariable(BP, FName("MyVar"), T, FString(TEXT("DefaultValueAsString")));`

## Workflow checklist

When implementing a generator from this skill:

1. Confirm the editor module exists with the right dependencies (template in [assets/experiment-module-template/](assets/experiment-module-template/)).
2. Read [references/k2node-cookbook.md](references/k2node-cookbook.md) for the patterns relevant to the asset type.
3. For Widget Blueprints, also read [references/widget-blueprint-cookbook.md](references/widget-blueprint-cookbook.md).
4. If wiring crosses content created in the same function, plan the **two-pass compile** structure ([references/two-pass-compile.md](references/two-pass-compile.md)).
5. Check [references/caveats.md](references/caveats.md) for known traps before assuming new behavior is a bug.
6. Test by building the editor target, opening the editor, calling the UFUNCTION (often via Python in the Output Log), and visually inspecting the asset.
7. Iterate: when a node looks wrong (red error border, missing pin, "X pruned" warning, default values where data should flow), the answer is almost always one of: missing exec wire, wrong allocation order, missing two-pass compile, or wrong pin name.

## What this skill does NOT cover

- **Cooking / packaging** the generated assets — they are regular `.uasset` files, ship like any other.
- **Editor Utility Widgets / Blutilities** — you can call your generator UFUNCTIONs from those, but designing the EUW is separate UMG work.
- **Runtime UMG** — `CreateWidget`, `AddToViewport`, animation `PlayAnimation` calls in game code. That is not codegen.
- **Custom UEdGraph schemas** — if generating into a domain-specific graph (dialogue, quest, ability tree), use the plugin's own compiler entry point. Static compiler classes are often non-exported, so call the graph's update method (e.g. `UMyGraph::UpdateAsset()`) instead of the static compiler if linkage fails.
