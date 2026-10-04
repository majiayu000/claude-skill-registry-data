---
name: add-component
description: Add and configure a UE component on an existing actor class.
---
# Skill: Add Component to Actor
## Description
Add and configure a UE component on an existing actor class.
## Arguments
- {{arg1}}: Actor class name
- {{arg2}}: Component type (e.g., UStaticMeshComponent, UAudioComponent)
## Steps
1. **In header**, declare the component:
   ```cpp
   UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category="Components")
   TObjectPtr<{{arg2}}> MyComponent;
   ```

2. **In constructor**, create and attach:
   ```cpp
   MyComponent = CreateDefaultSubobject<{{arg2}}>(TEXT("MyComponent"));
   MyComponent->SetupAttachment(RootComponent);
   ```

3. **Configure default properties** as needed

4. **Add required include** for the component type

## Notes
- Use TObjectPtr<> instead of raw pointers for GC safety
- VisibleAnywhere shows in viewport, EditAnywhere allows editing
- If adding a component from a non-core module (e.g., `UMG`, `Niagara`), ensure the module is added to `PublicDependencyModuleNames` in the `.Build.cs` file.

---

## Design-Time Blueprint Component Attachment (Native C++ Tool)

To attach a new component to an existing Blueprint asset (`.uasset`) at design time without modifying C++ source code, use the native C++ action tool `add_blueprint_component`.

### Usage Protocol
Invoke `add_blueprint_component` with the target Blueprint asset path, component class, new component name, and optional parent attachment node:

```json
{
  "blueprint_path": "/Game/Blueprints/BP_MyActor",
  "component_class": "UStaticMeshComponent",
  "component_name": "MeshComponent",
  "parent_component_name": "DefaultSceneRoot"
}
```

### Parameters
* `blueprint_path` (string, required): Object path to target Blueprint asset.
* `component_class` (string, required): Component class name (e.g. `'UStaticMeshComponent'`, `'USphereComponent'`, `'UAudioComponent'`, `'UNiagaraComponent'`).
* `component_name` (string, required): Unique identifier name for the new SCS component node.
* `parent_component_name` (string, optional): Parent component node to attach under. Defaults to `RootComponent` if omitted.

