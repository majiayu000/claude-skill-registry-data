---
name: unreal-testing-sops
description: Standard Operating Procedures (SOPs) for testing game functionality in Unreal Engine.
---
# Unreal Engine Testing SOPs

This skill contains Standard Operating Procedures (SOPs) for testing game functionality in Unreal Engine. Following these SOPs ensures reliable testing with minimal token usage.

## SOP Design Principles for Minimal Token Usage
To minimize AI assistant quota and token consumption:
1. **Avoid Viewport Captures (`capture_viewport` / `capture_widget`)**: Analyzing images with multimodal prompts is extremely expensive. Do not capture images unless verifying UI visuals.
2. **Prefer Keystroke Sequences (`simulate_input`)**: Navigate menus using keyboard/gamepad focus keys (e.g., `Tab`, `Arrow Keys`, `Enter`, `SpaceBar`, or Gamepad face buttons).
3. **Use Direct Bindings or Actions**: If a screen binds an action to a key (like `IA_StartRound` bound to `Enter` or a gamepad button), trigger that key directly rather than navigating to and clicking the button.
4. **Use Console Commands (`execute_console_command`)**: Bypass UI when testing systems (e.g. `open LevelName` or cheat commands) to minimize setup time.
5. **Use Your Native File-Reading Tool with Line Ranges**: Avoid `cat` or `Get-Content` for reading source files. Use your harness's native file-reading tool (`view_file` in Antigravity, `Read` in Claude Code, or equivalent) with specific line ranges to read only the code of interest.
6. **Log Parsing Efficiency**: When checking log files for activity, use `Get-Content -Path <LogPath> -Tail <N>` (PowerShell) or `tail -n <N>` (Unix/macOS) rather than reading entire log files.
7. **Realistic Wait Durations & Native Scheduler**: For one-shot timer delays, use your harness's native wait/scheduling mechanism if it has one (e.g. Antigravity's `schedule` tool with `DurationSeconds`); otherwise a single bounded shell wait is acceptable. Never use tight polling loops. Use realistic timeouts (e.g., 5-15s) for map loading, PIE startup, and compilation.
8. **Fail Fast & Escalate**: Do not loop/retry blindly on failed commands or unresponsive editor sessions. Report the issue clearly with log details and ask the user for help.

---

## SOP-001: PvP Matchmaking & Round Start

### Goal
Verify the PvP matchmaking flow from the Main Menu to the Fleet Management screen, and initiate the combat round.

### Prerequisites
- Unreal Editor is open.
- The project builds and matches the current commit.

### Execution Workflows

#### Option A: Direct UI Action Triggering (Most Cost-Efficient / Recommended)
This method utilizes bound input actions to trigger UI handlers directly, bypassing the need to visually locate or click elements.

1. **Start PIE Session**:
   - Tool: `start_pie_session`
2. **Navigate Main Menu**:
   - Simulating gamepad/keyboard navigation to focus and select the PvP button:
     - Tool: `simulate_input` -> `key`: `"Tab"` (to move focus to the PvPButton)
     - Tool: `simulate_input` -> `key`: `"Enter"` (to click the focused button)
   - *Alternative (if focus is already default)*:
     - Tool: `simulate_input` -> `key`: `"Enter"` or `"Gamepad_FaceButton_Bottom"`
3. **Wait for Loading**:
   - Pause execution for a brief moment (e.g. 2-3 seconds) to allow the fleet management screen (`W_FleetManagementUI`) to load and register.
4. **Trigger Start Round Action**:
   - The `UFleetManagementUI` screen binds the `IA_StartRound` action to `HandleStartRound`.
   - Instead of mouse-clicking the button, simulate the key mapped to `IA_StartRound` (e.g., `Enter` or the specified key mapping):
     - Tool: `simulate_input` -> `key`: `"Enter"` (or the mapped key name)

#### Option B: Debug Console Commands (Highly Recommended for Agent Automation)
This method utilizes the custom C++ executive debug commands to jump directly to the target screens and trigger actions, requiring minimal token overhead and no image processing.

1. **Start PIE Session**:
   - Tool: `start_pie_session`
2. **Trigger PvP Matchmaking Transition (Main Menu)**:
   - Tool: `execute_console_command` -> `command`: `"TauDebugGoToPvP"`
3. **Wait for Loading**:
   - Pause execution for 2-3 seconds.
4. **Trigger Start Round (Fleet Management)**:
   - Tool: `execute_console_command` -> `command`: `"TauDebugStartRound"`

#### Option C: Programmatic UI Actions (Native MCP C++ Tools)
Use this option when input action bindings or console command cheats are not available for UI transitions.

1. **Start PIE Session**:
   - Tool: `start_pie_session`
2. **Enumerate & Inspect Active PIE Widgets**:
   - Query active UMG widget instances in the running PIE game world:
     - Tool: `get_active_runtime_widgets` -> `widget_class`: `"UserWidget"`
   - Or extract the full visual Slate element hierarchy:
     - Tool: `extract_ui_state`
3. **Trigger UI Actions via Native MCP Tools**:
   - **Method A: Direct Delegate Invocation (Recommended for Off-Screen/Unfocused Widgets)**:
     - Directly trigger the button delegate on the active PIE widget instance:
       - Tool: `invoke_pie_widget_delegate` -> `widget_class_or_name`: `"W_TauMainMenu_C"`, `widget_property_name`: `"PvPButton"`, `delegate_name`: `"OnClicked"`
   - **Method B: Slate Event Simulation**:
     - Trigger synthesized click on the widget path retrieved from `extract_ui_state`:
       - Tool: `trigger_ui_element` -> `widget_path`: `"W_TauMainMenu_C_0.PvPButton"`
4. **Wait for Loading**:
   - Pause execution for 2-3 seconds.
5. **Navigate/Click next screen programmatically**:
   - Trigger the start round delegate on the newly loaded `W_FleetManagementUI` widget:
     - Tool: `invoke_pie_widget_delegate` -> `widget_class_or_name`: `"W_FleetManagementUI"`, `widget_property_name`: `"StartRoundButton"`, `delegate_name`: `"OnClicked"`

### Verification & Success Criteria
- The game state transitions to `TauRoundGameMode` (Combat Phase).
- The logs show `HandleStartRound` execution and the spawning of squads on the battlefield.
- Verify using `read_message_log` or viewport frame inspection that the match starts successfully.

---

## SOP-002: Automated Performance Testing & Analysis

### Goal
Verify the performance of the game under high-entity counts by running a simulated spectator round, programmatically capturing Unreal Insights trace and CSV profile data, and automatically generating an optimization diagnostic report in JSON.

### Prerequisites
- Unreal Editor is open.
- The project builds and matches the current commit.
- In-game graphics quality settings are at their target profile.

### Execution Workflow (Console Commands / Automation)
This is the workflow for the AI agent to test performance, analyze results, and report bottlenecks:

1. **(Optional) Configure Custom Benchmark Settings**:
   - By default, the benchmark spawns 800 entities and runs for 10 seconds. To configure custom settings, set the following console variables (CVars):
     - Tool: `execute_console_command` -> `command`: `"Tau.Test.BenchmarkEntities <count>"`
     - Tool: `execute_console_command` -> `command`: `"Tau.Test.BenchmarkDuration <seconds>"`
2. **Ensure PIE safety**:
   - If a Play-In-Editor (PIE) session is currently active, ensure it is closed to avoid conflicts:
     - Tool: `stop_pie_session` (if running)
3. **Run the Automation Test**:
   - Tool: `run_automation_tests` -> `test_filter`: `"Tau.Performance.Benchmark"`
4. **Verify Test Success**:
   - Ensure the test returns success. (Background throttling is automatically disabled by the AgentFramework editor plugin on startup and during the trace).
5. **Agent Analysis & Optimization Recommendations**:
   - Run the custom Python analysis script to filter the data, calculate frame time spikes, analyze parallel CPU execution/concurrency, and produce a query index:
     - Tool: `run_command` -> `CommandLine`: `"python .agents/scripts/parse_benchmark.py"`
   - Present the returned JSON report summary (including the identified bottleneck, frame spikes, longest-running Mass and Niagara tasks, concurrency overlap details, and the targeted Query Index) to the user.

### Verification & Success Criteria
- The benchmark runs for the specified duration and exits cleanly.
- `Saved/Performance/BenchmarkResult.json` is generated and contains the following JSON structure:
  ```json
  {
    "SimulationTimeSeconds": 15.0,
    "StartActiveUnits": 1000,
    "EndActiveUnits": 980,
    "PrimaryBottleneck": "Game Thread",
    "ClientFPS": { "Average": 45.2, "Min": 28.5, "Max": 60.1 },
    "GameThread": { "AverageMs": 16.5, "MinMs": 10.2, "MaxMs": 35.1 },
    "RenderThread": { "AverageMs": 12.1, "MinMs": 8.5, "MaxMs": 20.2 },
    "GPU": { "AverageMs": 14.2, "MinMs": 10.5, "MaxMs": 18.1 },
    "Recommendations": [
      "Game Thread is the primary bottleneck. Review CPU performance.",
      "Mass Entity System update time is high. Consider optimizing UUnitBehaviorProcessor logic or fragment sizes."
    ]
  }
  ```

---

## SOP-003: E2E Latent Testing & Run Isolation Guardrails

### 1. Isolated Run Command Line Flags
When running automation tests from the command line (especially in headless or build environments), **always** include the `-Nomessaging` flag.
* **Why:** By default, Unreal Engine's automation system utilizes UDP Messaging to discover other testing workers. If multiple editor/game instances are running concurrently, they will peer with each other, leading to port conflicts and deadlocks in enqueued latent commands.
* **Example CLI Pattern:**
  ```powershell
  & "UnrealEditor-Cmd.exe" "Project.uproject" -game -nullrhi -ExecCmds="Automation RunTests TestName" -stdout -unattended -nopause -unbuffered -Nomessaging
  ```

### 2. Loading Screen & World Transition Race Conditions
When writing latent commands that search for widgets (e.g., waiting for screen activation after loading a map), you **must** verify that the map load is fully complete and all garbage collection has dropped.
* **Why:** `open Map` transitions are asynchronous. A simple check for `GetAllWidgetsOfClass` can return `true` on the old widget instances *before* the level swap teardown and GC starts, resulting in immediate null pointers/timeouts once the new map begins loading.
* **Implementation:** Always verify with the loading screen subsystem (`ULoadingScreenManager`) that the loading screen has fully closed before accepting widgets:
  ```cpp
  if (UGameInstance* GI = World->GetGameInstance())
  {
      if (ULoadingScreenManager* LSM = GI->GetSubsystem<ULoadingScreenManager>())
      {
          if (LSM->GetLoadingScreenDisplayStatus())
          {
              return false; // Skip widget checks, the loading screen is still up
          }
      }
  }
  ```

---

## SOP-004: Singleplayer Progression & Match Flow Testing

### Goal
Verify the Singleplayer Challenge run flow from the Main Menu through Capital Ship/Fleet selection, handle suspended save games cleanly, and transition into the Fleet Management screen.

### Prerequisites
- `DA_ProgressionRegistry` (`/Game/Data/Progression/DA_ProgressionRegistry.uasset`) must register all valid Capital Ships (`DA_Capital_Dreadnought`, `DA_Capital_Hyperion`, `DA_Capital_Leviathan`, `DA_Capital_Archangel`) with `bUnlocked = true` to prevent the Singleplayer Challenges button from being disabled.
- INI audio maps in `Config/DefaultGame.ini` must use valid `((Key1,Value1),(Key2,Value2))` Unreal syntax.

### Execution Workflow

1. **Start PIE Session**:
   - Tool: `start_pie_session`
2. **Handle Existing Suspended Runs**:
   - Singleplayer runs persist to `Saved/SaveGames/CurrentRunState_SP.sav`.
   - If a saved run exists, clicking "Singleplayer Challenges" opens an overwrite confirmation modal (`W_ConfirmationDefault` / `Start New Run?`).
   - *Option A (Clean New Run)*: Delete `CurrentRunState_SP.sav` before testing to guarantee direct transition without modal intervention.
   - *Option B (Continue Existing Run)*: Trigger the `SingleplayerContinueButton` (`slate_scommonbutton_*` labeled "Continue") which calls `StartShopFlow(true, false)`.
   - *Option C (Confirm Overwrite)*: If the modal appears, click the "Yes" button (`ECommonMessagingResult::Confirmed`) to invoke `ExecuteStartMatchFlow`.
3. **Trigger Singleplayer Match Flow**:
   - Trigger the "Singleplayer Challenges" button:
     - Tool: `trigger_ui_element` on the button path retrieved from `extract_ui_state`.
     - Or Python: `state_comp.start_match_flow(match_class)` where `match_class = BP_SingleplayerMatchInstance_C`.
4. **Verify Transition to Fleet Management**:
   - Wait 4-6 seconds for `W_FleetManagementUI` to instantiate.
   - Tool: `get_active_runtime_widgets` -> verify `W_FleetManagementUI_C_0` is present, visible, and has active input focus.

---

## SOP-005: End-to-End Combat Simulation Testing (`L_Round`)

### Goal
Transition from the Fleet Management Phase into the automated physical combat simulation (`L_Round`), verify squad and gun visualization spawning, simulate combat via Mass ECS, and verify the Post-Battle Round End sequence.

### Prerequisites
- All gun data assets in `/Game/Data/Guns/` MUST have a valid `VisualizationAsset` assigned from `/Game/EntityRepresentations/DataAssets/Guns/DA_Rep_*`. A missing visualization asset causes Mass entity representation instantiation to fail.
- At least one active squad must be placed on the hex grid (`ActiveSquadIDs.Num() > 0`) to enable round start.

### Execution Workflow

1. **Verify Fleet Management Pre-Conditions**:
   - Ensure `StartRoundButton` is enabled (`ActiveSquadIDs.Num() > 0`).
2. **Trigger Round Start**:
   - Normal gameplay uses an input hold gesture (`IA_StartRound` held for `StartRoundHoldRequiredDuration`).
   - *Method A (Simulate Input Hold)*:
     - Tool: `simulate_input` -> `key`: `"SpaceBar"`, `action_type`: `"down"`
     - Wait 2.0-3.0 seconds (using `schedule` with `DurationSeconds`).
     - Tool: `simulate_input` -> `key`: `"SpaceBar"`, `action_type`: `"up"`
   - *Method B (Direct Debug Function)*:
     - Execute `DebugStartRound()` directly on the active `UFleetManagementUI` instance.
3. **Verify Level Transition to `L_Round`**:
   - Wait 5-8 seconds for `L_Round` level load and Mass ECS world subsystems initialization.
   - Tool: `read_message_log` -> Verify:
     - `NS_UnitRepresentation` and `NS_GunRepresentation` compile cleanly.
     - `SpawnGunsForSquad` reports all mounted guns `Valid=1`.
     - 0 critical errors or access violation logs.
4. **Accelerate Combat Simulation**:
   - In `L_Round`, combat unfolds automatically. To avoid long idle test durations, accelerate time dilation:
     - Tool: `simulate_input` on `GameSpeedButtonFast` or invoke `ATauRoundPlayerController::SetGameSpeedBypassingPawn(EGameSpeed::TIMES_THREE)` via Python.
5. **Verify Combat Progression & Resolution**:
   - Tool: `get_active_runtime_widgets` -> Verify battle HUD elements (`W_RoundHUD_C_0`, `W_Minimap_C`, `GameSpeedSelectionWidget`).
   - Wait for units on one side to be destroyed.
   - Verify that `UGameLoopSubsystem::NotifyRoundEnd()` executes, audio stingers fire, and `RoundEndScreenClass` (`UTauRoundEndWidget`) is pushed to the HUD layer.

---

## SOP-006: Diagnostic & Null-Safety Guardrail Protocol

### Goal
Prevent unhandled Access Violation crashes during automated testing and live gameplay through strict defensive coding patterns.

### Mandatory Developer Guardrails

1. **MatchInstance Safety in UI Constructors**:
   - `UTauGameInstance::GetMatchInstance()` can return `nullptr` during standalone UI testing, early initialization, or level loading.
   - **RULE**: Never chain `GetMatchInstance()->GetMapGridSize()` without a null check.
   - **Pattern**:
     ```cpp
     TPair<float, float> FleetGridDimensions(10.f, 10.f);
     if (UTauGameInstance* TauGI = GetWorld() ? GetWorld()->GetGameInstance<UTauGameInstance>() : nullptr)
     {
         if (UMatchInstance* MatchInst = TauGI->GetMatchInstance())
         {
             FleetGridDimensions = MatchInst->GetMapGridSize();
         }
     }
     ```

2. **Mouse Hover & Dynamic Upgrade Slot Validation**:
   - Slate synthetic mouse move events can hover over empty upgrade slots or uninitialized widgets.
   - **RULE**: Methods receiving `UUnitSquadUpgradeDataAsset*` or `UUpgradeSlot*` (such as `OnUpgradeSlotHovered` and `AreUnitAttributesMatchingUpgradeRequirements`) MUST null-check the incoming upgrade pointer before dereferencing requirements or properties.
   - **Pattern**:
     ```cpp
     if (!Upgrade)
     {
         return false;
     }
     ```

3. **Niagara Representation Asset Contract**:
   - `UNiagaraRepresentationSubsystem::GetOrCreateRepresentationClass()` keys representations by `Sprite->GetFName()`.
   - **RULE**: Never pass an unverified or null `Sprite` pointer into representation creation. Maintain defensive null checking at the subsystem boundary.

4. **Unreal INI TMap Delimiter Syntax**:
   - Unreal Engine's `FMapProperty::ImportText_Internal` does NOT support INI line additions (`+MapKey=(Key=...,Value=...)`).
   - **RULE**: Multi-entry TMaps in `DefaultGame.ini` must be formatted on a single line using parentheses pairs:
     ```ini
     MapProperty=((Key1,Value1),(Key2,Value2),(Key3,Value3))
     ```
