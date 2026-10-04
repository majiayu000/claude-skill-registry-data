---
name: pie-verifier
description: Autonomously run PIE (Play-In-Editor) sessions, navigate UMG/Slate UI, click elements programmatically, and query world actors to verify changes.
---
# Play-In-Editor (PIE) Verification SOPs

This skill instructs the agent on how to autonomously test game logic, UI navigation, and gameplay systems using a live Play-In-Editor (PIE) session inside the Unreal Editor.

## Available Actions / Tools
The internal C++ MCP server provides the following tools:
1. `start_pie_session`: Starts the PIE session. Use `start_mode: "current_camera"` (optional) to spawn at the editor camera location.
2. `extract_ui_state`: Returns a JSON tree of visible UMG widgets (grouped under `umg`) and raw Slate elements (grouped under `slate`).
3. `trigger_ui_element`: Accepts `widget_path` (e.g. `WBP_MainMenu_C_0.PlayButton` for UMG, or `slate_sbutton_0` for Slate) to programmatically click or trigger the element.
4. `query_world_state`: Accepts a list of `classes` (e.g., `["Character", "BP_TargetActor_C"]`), `tags` (optional), and `radius` (optional). Returns the coordinates and metadata of matching actors.
5. `read_message_log`: Captures the output log. Essential for asserting that no "Accessed None" or critical warnings fired.
6. `stop_pie_session`: Stops the current running PIE session.

---

## Standard Verification Workflow

Follow this loop to verify gameplay changes:

### Step 1: Start PIE
Call the `start_pie_session` tool.
> [!NOTE]
> If PIE is already running, the tool will notify you. Use `read_message_log` to ensure no startup asserts occurred.

### Step 2: Extract & Interact with UI
If the game starts with a UI menu (e.g., a main menu, inventory, or overlay):
1. Call `extract_ui_state`.
2. Inspect the `umg` block for the path of the button you want to click (e.g., `WBP_MainMenu_C_0.StartGameButton`).
3. Call `trigger_ui_element` with that path.
4. Call `extract_ui_state` again if the screen changed to verify the menu closed or a new menu opened.

### Step 3: Simulate Gameplay Actions
Use `simulate_input` to move the character or trigger actions (e.g., press `W` to move, `SpaceBar` to jump, or custom keys).
* Since inputs are processed instantly, call `simulate_input` with `action_type: "down"` to hold a key, wait a moment using your harness's native wait mechanism (e.g. Antigravity's `schedule` tool, or a short bounded shell wait), and then call `action_type: "up"` to release it.

### Step 4: Extract World State
Call `query_world_state` with specific filters to verify that the gameplay action completed successfully:
* To check if the player moved: Query the `player` location.
* To check if an actor was spawned or destroyed: Pass the class name to `classes` and check if it is returned.
* To check if an interactable object opened: Query the actor's location/properties.

### Step 5: Read Log for Failures
Call `read_message_log` to check for runtime errors (like Blueprint compiler issues, null pointers, or failed casts) that occurred during play.

### Step 6: End PIE
Call `stop_pie_session` when the verification completes.

---

## Best Practices
* **Filter Queries:** Always specify `classes` or `tags` when calling `query_world_state` to keep the context clean and avoid exceeding token limits.
* **Wait for Loading:** Give the engine 1-2 seconds after map loads or starting PIE before expecting widgets to be drawn or actors to fully possess.
* **Dynamic Path Lookup:** Do not hardcode button paths across different maps. Always call `extract_ui_state` first to discover the exact widget instance names (e.g., widget instances might end with `_C_0`, `_C_1`, etc.).
* **Progression State Validation:** If main menu or game flow buttons are unexpectedly disabled (e.g., Singleplayer button greyed out), verify that required progression registries (like `DA_ProgressionRegistry`) have valid starting unlocks (e.g., Capital Ships) registered.
* **Save-Game Isolation:** When testing run-based or roguelite game modes (e.g. Singleplayer Challenges), check for and isolate persistent save games (`Saved/SaveGames/*.sav`). Stale save games often trigger modal overwrite confirmation dialogs (`UAsyncAction_ShowConfirmation`) that intercept automated input.
* **Hold-to-Activate Inputs:** For buttons or input actions that require holding (e.g. `IA_StartRound`), use `simulate_input` with `action_type: "down"`, wait the required hold duration using the native `schedule` tool, and then send `action_type: "up"`. Alternatively, check if the screen provides a direct debug bypass method (e.g., `DebugStartRound()`).

