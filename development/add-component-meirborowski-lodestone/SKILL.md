---
name: add-component
description: Add a component to Lodestone - the data struct, its reflection registration (which drives serialization, the inspector, MCP, script bindings and replication), any custom handling, and its tests. Use whenever a feature needs new per-entity data.
---

# Add a Component

Components are the data entities carry. The reflection registry is how every engine system learns about them, so a component is only finished when it's registered and tested (see AGENTS.md, "Adding a Component", and `docs/Decisions/0010-component-reflection.md`).

## 1. Define the data
- A struct named `<Name>Component` in the module that owns it (core components are in `Source/Core/Lodestone/Scene/Components.h`), with public PascalCase fields and default member initializers. Components must be default-constructible and copyable
- Use the reflected field types for everything that's saved, edited or replicated: `bool`, `int32_t`, `uint32_t`, `float`, `glm::vec2/3/4`, `glm::quat`, `std::string`, `UUID`. Refer to other entities and to assets by `UUID`, never by handle or path
- Data the simulation needs but files mustn't contain goes in a separate component registered as `ComponentFlags::Internal`
- A component that drives a system with state of its own, outside the registry (as the physics components drive Jolt), needs that system to be a `StatefulSystem` that saves and restores its state - see `PhysicsWorld` and [Decision 0021](../../../docs/Decisions/0021-physics.md)
- Keep logic out of components: systems (`Simulation::AddSystem`) and engine code act on them

## 2. Register it
In the module's registration function (core: `RegisterCoreComponents()` in `Components.cpp`):
```cpp
registry.Register<LightComponent>("Light", "A point light")
	.Field("Color", &LightComponent::Color, {.Description = "Linear RGB", .Min = 0.0, .Max = 1.0})
	.Field("Intensity", &LightComponent::Intensity, {.Description = "In candela", .Min = 0.0, .Flags = FieldFlags::Replicated});
```
- The component and field names are permanent: files, MCP and scripts use them. Renaming one later is a file format change with a migration (`docs/Architecture.md#file-formats`)
- Give every field a description, and limits where values have them. Defaults must be within the limits
- `FieldFlags::Replicated` for what clients need to see; `FieldFlags::ReadOnly` for what only the engine may change; `ComponentFlags::Required` only for components every entity has

## 3. Custom handling, only if needed
If the generic path can't express it - like `Hierarchy`, whose parent is applied through `Scene::SetParent` when a scene loads - add the handling next to the generic code, and say why in a comment.

## 4. Test it
In `Tests/Core` (or the module's test executable):
- The registration: the type is found by name, with the expected fields, types, limits and flags
- A scene with the component saves and loads unchanged (`SceneSerializer::SerializeToText` before and after), and invalid values (wrong type, out of range) fail to load with a clear message
- If systems change it during the simulation: restoring a snapshot and re-simulating the same input commands gives the same result
- Any custom handling

Then follow `build-and-test` and `ship-change`.
