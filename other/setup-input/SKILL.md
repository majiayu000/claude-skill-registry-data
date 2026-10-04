---
name: setup-input
description: Configure the Enhanced Input system with Input Actions, Mapping Contexts, Modifiers, and Triggers via native MCP tools.
---
# Skill: Setup Enhanced Input
## Description
Configure the Enhanced Input system with Input Actions, Mapping Contexts, key mapping Modifiers, and Triggers.
## Arguments
- {{arg}}: The action name to set up (e.g., Jump, Sprint, Interact, Move)
## Steps
1. **Create Input Action Asset**: Use the `create_input_action` MCP tool to create `/Game/Input/Actions/IA_{{arg}}`:
   ```json
   {
     "PackagePath": "/Game/Input/Actions",
     "ActionName": "IA_{{arg}}",
     "ValueType": "Digital"
   }
   ```
   *(Supported `ValueType` options: `Digital`, `Axis1D`, `Axis2D`, `Axis3D`)*

2. **Add Key Mapping to Input Mapping Context**:
   - If `/Game/Input/IMC_Default` does not exist, create it via `create_input_mapping_context`:
     ```json
     {
       "PackagePath": "/Game/Input",
       "ContextName": "IMC_Default"
     }
     ```
   - Bind the target key mapping using `add_input_mapping`:
     ```json
     {
       "ContextAsset": "/Game/Input/IMC_Default",
       "InputActionAsset": "/Game/Input/Actions/IA_{{arg}}",
       "Key": "SpaceBar"
     }
     ```

3. **Configure Key Mapping Modifiers & Triggers**:
   Attach key modifiers (e.g. `Negate`, `SwizzleAxis`) and trigger conditions (e.g. `Pressed`, `Hold`, `Tap`) using `configure_input_mapping_modifiers_triggers`:
   - **Example 1: Axis Negation (e.g. Move Backward 'S' key)**:
     ```json
     {
       "ContextAsset": "/Game/Input/IMC_Default",
       "InputActionAsset": "/Game/Input/Actions/IA_Move",
       "Key": "S",
       "Modifiers": [ { "Type": "Negate" } ]
     }
     ```
   - **Example 2: 2D Vector Swizzle (e.g. Move Forward 'W' key)**:
     ```json
     {
       "ContextAsset": "/Game/Input/IMC_Default",
       "InputActionAsset": "/Game/Input/Actions/IA_Move",
       "Key": "W",
       "Modifiers": [ { "Type": "SwizzleAxis", "Order": "YXZ" } ]
     }
     ```
   - **Example 3: Hold Trigger (e.g. Charge Attack / Sprint Hold)**:
     ```json
     {
       "ContextAsset": "/Game/Input/IMC_Default",
       "InputActionAsset": "/Game/Input/Actions/IA_Sprint",
       "Key": "LeftShift",
       "Triggers": [ { "Type": "Hold", "HoldTimeThreshold": 0.5, "bIsOneShot": true } ]
     }
     ```

4. **In the character/pawn header**, add:
   ```cpp
   UPROPERTY(EditDefaultsOnly, Category="Input")
   TObjectPtr<UInputAction> {{arg}}Action;
   void Handle{{arg}}(const FInputActionValue& Value);
   ```

5. **In the character/pawn class**, override `SetupPlayerInputComponent` to bind the action:
   ```cpp
   // Header
   virtual void SetupPlayerInputComponent(class UInputComponent* PlayerInputComponent) override;

   // Source
   void AMyCharacter::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
   {
       Super::SetupPlayerInputComponent(PlayerInputComponent);
       
       if (UEnhancedInputComponent* EIC = Cast<UEnhancedInputComponent>(PlayerInputComponent))
       {
           EIC->BindAction({{arg}}Action, ETriggerEvent::Triggered, this, &AMyCharacter::Handle{{arg}});
       }
   }
   ```

6. **Implement the handler function** in C++:
   ```cpp
   void AMyCharacter::Handle{{arg}}(const FInputActionValue& Value)
   {
       // Retrieve input value (e.g. float or Vector2D depending on configuration)
       // float AxisValue = Value.Get<float>();
   }
   ```

7. **Blueprint Binding Alternative**:
   - In a Blueprint Character graph, right-click and search for `"EnhancedAction IA_{{arg}}"`.
   - Add the **Enhanced Action IA_{{arg}}** node.
   - Wire your game logic nodes to the **Triggered** or **Started** / **Completed** pins.

## Notes
- Ensure `"EnhancedInput"` is added to `PublicDependencyModuleNames` in the project's `.Build.cs` file.
- Include `EnhancedInput/Public/EnhancedInputComponent.h`.
- The project must have the EnhancedInput plugin enabled.
- **Python API Tip (UE 5.8)**: When mapping keys via Unreal Python, instantiate `unreal.Key()` with `key.set_editor_property('key_name', 'Space')`, construct `mapping = unreal.EnhancedActionKeyMapping()`, set `action` and `key`, and append `mapping` to `imc.get_editor_property('mappings')` before calling `unreal.EditorAssetLibrary.save_loaded_asset(imc)`.
