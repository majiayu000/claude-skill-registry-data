---
name: input-system
description: "New Input System — action maps, PlayerInput component, generated C# classes, runtime rebinding, multi-device support, input buffering."
globs: ["**/*.inputactions", "**/Input*.cs", "**/PlayerInput*"]
---

# Unity New Input System

## Input Action Asset Setup

Create an Input Action Asset: Assets > Create > Input Actions. This is the central configuration for all input bindings.

### Action Map Structure

Organize actions into maps based on context:

```
PlayerControls.inputactions
  |-- Player (gameplay)
  |     |-- Move (Value, Vector2)
  |     |-- Look (Value, Vector2)
  |     |-- Jump (Button)
  |     |-- Attack (Button)
  |     |-- Interact (Button)
  |
  |-- UI (menu navigation)
  |     |-- Navigate (Value, Vector2)
  |     |-- Submit (Button)
  |     |-- Cancel (Button)
  |
  |-- Menu (pause/settings)
        |-- Pause (Button)
```

### Action Types

- **Button**: Discrete press/release. Use for jump, attack, interact.
- **Value**: Continuous value. Use for movement, look, triggers.
- **Pass-Through**: Like Value but does not perform initial state check. Use for multi-device scenarios.

## Generated C# Class Workflow

In the Input Action Asset inspector, check "Generate C# Class" and click Apply. This is the recommended approach.

```csharp
using UnityEngine;
using UnityEngine.InputSystem;

public class PlayerController : MonoBehaviour
{
    private PlayerControls _controls;
    private Vector2 _moveInput;

    private void Awake()
    {
        _controls = new PlayerControls();
    }

    private void OnEnable()
    {
        _controls.Player.Enable();

        _controls.Player.Move.performed += OnMove;
        _controls.Player.Move.canceled += OnMove;
        _controls.Player.Jump.performed += OnJump;
        _controls.Player.Attack.performed += OnAttack;
    }

    private void OnDisable()
    {
        _controls.Player.Move.performed -= OnMove;
        _controls.Player.Move.canceled -= OnMove;
        _controls.Player.Jump.performed -= OnJump;
        _controls.Player.Attack.performed -= OnAttack;

        _controls.Player.Disable();
    }

    private void OnMove(InputAction.CallbackContext ctx)
    {
        _moveInput = ctx.ReadValue<Vector2>();
    }

    private void OnJump(InputAction.CallbackContext ctx)
    {
        // Jump logic
    }

    private void OnAttack(InputAction.CallbackContext ctx)
    {
        // Attack logic
    }

    private void Update()
    {
        transform.Translate(new Vector3(_moveInput.x, 0, _moveInput.y) * Time.deltaTime * 5f);
    }
}
```

## PlayerInput Component

The PlayerInput component provides an easier but less flexible approach.

### Behavior Modes

| Mode | Pros | Cons |
|------|------|------|
| Send Messages | Simple, no setup | Uses SendMessage (slow, no type safety) |
| Broadcast Messages | Reaches child objects | Same issues as SendMessages |
| Invoke Unity Events | Inspector-assigned, flexible | Requires wiring in Inspector |
| Invoke C# Events | Best performance, type-safe | Requires code subscription |

### Using Invoke C# Events

```csharp
using UnityEngine;
using UnityEngine.InputSystem;

[RequireComponent(typeof(PlayerInput))]
public class PlayerInputHandler : MonoBehaviour
{
    private PlayerInput _playerInput;

    private void Awake()
    {
        _playerInput = GetComponent<PlayerInput>();
    }

    private void OnEnable()
    {
        _playerInput.onActionTriggered += OnActionTriggered;
    }

    private void OnDisable()
    {
        _playerInput.onActionTriggered -= OnActionTriggered;
    }

    private void OnActionTriggered(InputAction.CallbackContext ctx)
    {
        switch (ctx.action.name)
        {
            case "Move":
                HandleMove(ctx.ReadValue<Vector2>());
                break;
            case "Jump":
                if (ctx.performed) HandleJump();
                break;
        }
    }

    private void HandleMove(Vector2 input) { /* ... */ }
    private void HandleJump() { /* ... */ }
}
```

## Reading Input Values

### Callback Phases

```csharp
action.started += ctx => { };   // Input begins (button starts pressing)
action.performed += ctx => { }; // Input completes (button fully pressed)
action.canceled += ctx => { };  // Input released
```

### Polling in Update (Alternative)

```csharp
private void Update()
{
    // Polling approach — simpler but less event-driven
    Vector2 move = _controls.Player.Move.ReadValue<Vector2>();
    bool jumpPressed = _controls.Player.Jump.WasPressedThisFrame();
    bool jumpReleased = _controls.Player.Jump.WasReleasedThisFrame();
    bool jumpHeld = _controls.Player.Jump.IsPressed();
}
```

## Action Map Switching

```csharp
public class InputMapSwitcher : MonoBehaviour
{
    private PlayerControls _controls;

    public void SwitchToUI()
    {
        _controls.Player.Disable();
        _controls.UI.Enable();
    }

    public void SwitchToGameplay()
    {
        _controls.UI.Disable();
        _controls.Player.Enable();
    }

    public void SwitchToMenu()
    {
        _controls.Player.Disable();
        _controls.UI.Disable();
        _controls.Menu.Enable();
    }
}
```

## Composite Bindings

### 2D Vector Composite (WASD / D-Pad)

In the Input Action Asset, add a 2D Vector composite to a Vector2 action:
- Up: W / D-Pad Up
- Down: S / D-Pad Down
- Left: A / D-Pad Left
- Right: D / D-Pad Right

### Button With Modifier

For key combos like Ctrl+S:
- Add ButtonWithOneModifier composite
- Modifier: Left Ctrl
- Button: S

## Runtime Rebinding

```csharp
using UnityEngine;
using UnityEngine.InputSystem;
using TMPro;

public class RebindManager : MonoBehaviour
{
    [SerializeField] private InputActionReference actionToRebind;
    [SerializeField] private TMP_Text bindingDisplayText;
    [SerializeField] private GameObject waitingForInputUI;

    private InputActionRebindingExtensions.RebindingOperation _rebindOperation;

    public void StartRebinding()
    {
        actionToRebind.action.Disable();
        waitingForInputUI.SetActive(true);

        _rebindOperation = actionToRebind.action.PerformInteractiveRebinding()
            .WithControlsExcluding("Mouse") // Exclude mouse movement
            .WithCancelingThrough("<Keyboard>/escape")
            .OnMatchWaitForAnother(0.1f) // Debounce
            .OnComplete(operation => RebindComplete())
            .OnCancel(operation => RebindCanceled())
            .Start();
    }

    private void RebindComplete()
    {
        _rebindOperation.Dispose();
        _rebindOperation = null;
        waitingForInputUI.SetActive(false);

        actionToRebind.action.Enable();
        UpdateBindingDisplay();

        // Save the binding override
        string rebinds = actionToRebind.action.actionMap.asset.SaveBindingOverridesAsJson();
        PlayerPrefs.SetString("InputBindings", rebinds);
    }

    private void RebindCanceled()
    {
        _rebindOperation.Dispose();
        _rebindOperation = null;
        waitingForInputUI.SetActive(false);
        actionToRebind.action.Enable();
    }

    private void UpdateBindingDisplay()
    {
        int bindingIndex = actionToRebind.action.GetBindingIndexForControl(
            actionToRebind.action.controls[0]);
        bindingDisplayText.text = InputControlPath.ToHumanReadableString(
            actionToRebind.action.bindings[bindingIndex].effectivePath,
            InputControlPath.HumanReadableStringOptions.OmitDevice);
    }

    public void LoadSavedBindings()
    {
        string rebinds = PlayerPrefs.GetString("InputBindings", string.Empty);
        if (!string.IsNullOrEmpty(rebinds))
        {
            actionToRebind.action.actionMap.asset.LoadBindingOverridesFromJson(rebinds);
        }
    }
}
```

## Input Buffering Pattern

Buffer inputs so actions like jump register even if pressed slightly before landing.

```csharp
public class InputBuffer : MonoBehaviour
{
    [SerializeField] private float bufferDuration = 0.15f;

    private float _jumpBufferTimer;
    private bool _jumpConsumed;

    private void Update()
    {
        if (_jumpBufferTimer > 0f)
        {
            _jumpBufferTimer -= Time.deltaTime;
        }
    }

    // Called from input callback
    public void OnJumpPressed()
    {
        _jumpBufferTimer = bufferDuration;
        _jumpConsumed = false;
    }

    // Called from movement/physics when jump is possible
    public bool ConsumeJumpBuffer()
    {
        if (_jumpBufferTimer > 0f && !_jumpConsumed)
        {
            _jumpConsumed = true;
            _jumpBufferTimer = 0f;
            return true;
        }
        return false;
    }
}
```

## Device Detection

```csharp
using UnityEngine.InputSystem;

public class DeviceDetector : MonoBehaviour
{
    public enum InputScheme { KeyboardMouse, Gamepad, Touch }
    public InputScheme CurrentScheme { get; private set; }

    public event System.Action<InputScheme> OnSchemeChanged;

    private void OnEnable()
    {
        InputSystem.onActionChange += OnActionChange;
    }

    private void OnDisable()
    {
        InputSystem.onActionChange -= OnActionChange;
    }

    private void OnActionChange(object obj, InputActionChange change)
    {
        if (change != InputActionChange.ActionPerformed) return;

        var action = (InputAction)obj;
        var device = action.activeControl?.device;

        InputScheme newScheme = device switch
        {
            Keyboard or Mouse => InputScheme.KeyboardMouse,
            Gamepad => InputScheme.Gamepad,
            Touchscreen => InputScheme.Touch,
            _ => CurrentScheme
        };

        if (newScheme != CurrentScheme)
        {
            CurrentScheme = newScheme;
            OnSchemeChanged?.Invoke(CurrentScheme);
        }
    }
}
```

## Multiplayer Input (PlayerInputManager)

```csharp
using UnityEngine;
using UnityEngine.InputSystem;

public class LocalMultiplayerManager : MonoBehaviour
{
    [SerializeField] private PlayerInputManager playerInputManager;

    private void OnEnable()
    {
        playerInputManager.onPlayerJoined += OnPlayerJoined;
        playerInputManager.onPlayerLeft += OnPlayerLeft;
    }

    private void OnDisable()
    {
        playerInputManager.onPlayerJoined -= OnPlayerJoined;
        playerInputManager.onPlayerLeft -= OnPlayerLeft;
    }

    private void OnPlayerJoined(PlayerInput playerInput)
    {
        Debug.Log($"Player {playerInput.playerIndex} joined with {playerInput.currentControlScheme}");
    }

    private void OnPlayerLeft(PlayerInput playerInput)
    {
        Debug.Log($"Player {playerInput.playerIndex} left");
    }
}
```

## Touch Input for Mobile

```csharp
using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.InputSystem.EnhancedTouch;
using Touch = UnityEngine.InputSystem.EnhancedTouch.Touch;

public class TouchInputHandler : MonoBehaviour
{
    private void OnEnable()
    {
        EnhancedTouchSupport.Enable();
    }

    private void OnDisable()
    {
        EnhancedTouchSupport.Disable();
    }

    private void Update()
    {
        foreach (var touch in Touch.activeTouches)
        {
            switch (touch.phase)
            {
                case UnityEngine.InputSystem.TouchPhase.Began:
                    HandleTouchStart(touch.screenPosition);
                    break;
                case UnityEngine.InputSystem.TouchPhase.Moved:
                    HandleTouchMove(touch.screenPosition, touch.delta);
                    break;
                case UnityEngine.InputSystem.TouchPhase.Ended:
                    HandleTouchEnd(touch.screenPosition);
                    break;
            }
        }
    }

    private void HandleTouchStart(Vector2 pos) { /* ... */ }
    private void HandleTouchMove(Vector2 pos, Vector2 delta) { /* ... */ }
    private void HandleTouchEnd(Vector2 pos) { /* ... */ }
}
```
