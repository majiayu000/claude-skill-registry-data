---
name: state-machine
description: "Generic state machine patterns — IState interface, StateMachine<T>, game state management (menu/gameplay/pause), enemy AI states, hierarchical FSM. Load when implementing state-driven behavior."
globs: ["**/State*.cs", "**/FSM*.cs", "**/*Machine*.cs"]
---

# State Machine Patterns

A generic, reusable finite state machine for Unity. Covers player states, enemy AI, game flow (menu/gameplay/pause), hierarchical FSMs, and ScriptableObject-driven states for designer configuration.

## IState Interface

The contract every state must fulfill. Keep it minimal: enter, exit, tick, and physics tick.

```csharp
public interface IState
{
    /// <summary>Called once when entering this state.</summary>
    void Enter();

    /// <summary>Called once when leaving this state.</summary>
    void Exit();

    /// <summary>Called every frame while this state is active.</summary>
    void Update();

    /// <summary>Called every fixed timestep while this state is active.</summary>
    void FixedUpdate();
}
```

If your game does not need `FixedUpdate` in states (e.g., turn-based game), drop it from the interface. Keep the interface as lean as your project requires.

---

## StateMachine Generic Class

A generic state machine that can be used with any state type. The type parameter `T` is typically the owner (player, enemy, game manager) so states can access it.

```csharp
using System;
using System.Collections.Generic;
using UnityEngine;

public class StateMachine<T>
{
    public IState CurrentState { get; private set; }
    public IState PreviousState { get; private set; }

    private T _owner;
    private Dictionary<Type, IState> _states = new();

    public StateMachine(T owner)
    {
        _owner = owner;
    }

    /// <summary>
    /// Register a state instance. Call during initialization.
    /// </summary>
    public void AddState(IState state)
    {
        _states[state.GetType()] = state;
    }

    /// <summary>
    /// Transition to a new state by type. Calls Exit on current, Enter on new.
    /// </summary>
    public void ChangeState<TState>() where TState : IState
    {
        var type = typeof(TState);

        if (!_states.TryGetValue(type, out var newState))
        {
            Debug.LogError($"State {type.Name} not registered in state machine.");
            return;
        }

        if (CurrentState == newState) return; // Already in this state

        PreviousState = CurrentState;
        CurrentState?.Exit();
        CurrentState = newState;
        CurrentState.Enter();
    }

    /// <summary>
    /// Change state by instance (useful when states are not unique by type,
    /// e.g., ScriptableObject states).
    /// </summary>
    public void ChangeState(IState newState)
    {
        if (newState == null || CurrentState == newState) return;

        PreviousState = CurrentState;
        CurrentState?.Exit();
        CurrentState = newState;
        CurrentState.Enter();
    }

    /// <summary>
    /// Return to the previous state.
    /// </summary>
    public void RevertToPreviousState()
    {
        if (PreviousState != null)
            ChangeState(PreviousState);
    }

    /// <summary>
    /// Call from the owner's Update().
    /// </summary>
    public void Update()
    {
        CurrentState?.Update();
    }

    /// <summary>
    /// Call from the owner's FixedUpdate().
    /// </summary>
    public void FixedUpdate()
    {
        CurrentState?.FixedUpdate();
    }

    /// <summary>
    /// Check if the current state is of a given type.
    /// </summary>
    public bool IsInState<TState>() where TState : IState
    {
        return CurrentState is TState;
    }

    public T Owner => _owner;
}
```

---

## Player State Example

A concrete example: player states for a 2D platformer. Each state is a class that holds a reference to the player controller.

### Base Player State

```csharp
public abstract class PlayerState : IState
{
    protected PlayerController Player { get; }
    protected StateMachine<PlayerController> StateMachine { get; }

    protected PlayerState(PlayerController player, StateMachine<PlayerController> stateMachine)
    {
        Player = player;
        StateMachine = stateMachine;
    }

    public virtual void Enter() { }
    public virtual void Exit() { }
    public virtual void Update() { }
    public virtual void FixedUpdate() { }
}
```

### Idle State

```csharp
public class PlayerIdleState : PlayerState
{
    public PlayerIdleState(PlayerController player, StateMachine<PlayerController> sm)
        : base(player, sm) { }

    public override void Enter()
    {
        Player.Animator.Play("Idle");
        Player.Rb.velocity = new Vector2(0f, Player.Rb.velocity.y);
    }

    public override void Update()
    {
        if (!Player.IsGrounded)
        {
            StateMachine.ChangeState<PlayerFallState>();
            return;
        }

        if (Player.JumpRequested)
        {
            StateMachine.ChangeState<PlayerJumpState>();
            return;
        }

        if (Mathf.Abs(Player.MoveInput.x) > 0.1f)
        {
            StateMachine.ChangeState<PlayerRunState>();
            return;
        }

        if (Player.DashRequested)
        {
            StateMachine.ChangeState<PlayerDashState>();
            return;
        }
    }
}
```

### Jump State

```csharp
public class PlayerJumpState : PlayerState
{
    public PlayerJumpState(PlayerController player, StateMachine<PlayerController> sm)
        : base(player, sm) { }

    public override void Enter()
    {
        Player.Animator.Play("Jump");
        Player.ExecuteJump();
    }

    public override void Update()
    {
        // Transition to fall when velocity turns downward
        if (Player.Rb.velocity.y <= 0f)
        {
            StateMachine.ChangeState<PlayerFallState>();
            return;
        }

        // Variable jump height: cut velocity on release
        if (Player.JumpReleased && Player.Rb.velocity.y > 0f)
        {
            Player.CutJumpShort();
        }

        // Allow wall slide if touching wall
        if (Player.IsTouchingWall && !Player.IsGrounded)
        {
            StateMachine.ChangeState<PlayerWallSlideState>();
            return;
        }
    }

    public override void FixedUpdate()
    {
        Player.ApplyHorizontalMovement();
    }
}
```

### Wiring It Up in the Player Controller

```csharp
using UnityEngine;

public class PlayerController : MonoBehaviour
{
    // Public properties that states read
    public Rigidbody2D Rb { get; private set; }
    public Animator Animator { get; private set; }
    public Vector2 MoveInput { get; private set; }
    public bool IsGrounded { get; private set; }
    public bool IsTouchingWall { get; private set; }
    public bool JumpRequested { get; set; }
    public bool JumpReleased { get; set; }
    public bool DashRequested { get; set; }

    private StateMachine<PlayerController> _stateMachine;

    private void Awake()
    {
        Rb = GetComponent<Rigidbody2D>();
        Animator = GetComponent<Animator>();

        _stateMachine = new StateMachine<PlayerController>(this);
        _stateMachine.AddState(new PlayerIdleState(this, _stateMachine));
        _stateMachine.AddState(new PlayerRunState(this, _stateMachine));
        _stateMachine.AddState(new PlayerJumpState(this, _stateMachine));
        _stateMachine.AddState(new PlayerFallState(this, _stateMachine));
        _stateMachine.AddState(new PlayerWallSlideState(this, _stateMachine));
        _stateMachine.AddState(new PlayerDashState(this, _stateMachine));

        _stateMachine.ChangeState<PlayerIdleState>();
    }

    private void Update()
    {
        ReadInput();
        CheckGround();
        CheckWall();
        _stateMachine.Update();
    }

    private void FixedUpdate()
    {
        _stateMachine.FixedUpdate();
    }

    // Movement methods called by states
    public void ExecuteJump() { /* see character-controller skill */ }
    public void CutJumpShort() { /* see character-controller skill */ }
    public void ApplyHorizontalMovement() { /* see character-controller skill */ }

    private void ReadInput() { /* read from Input System */ }
    private void CheckGround() { /* overlap circle check */ }
    private void CheckWall() { /* raycast check */ }
}
```

---

## Game State Management

Use the same state machine pattern for high-level game flow.

### Game States

```
MainMenu → Loading → Gameplay → Pause → GameOver
                       ↑          |
                       +----------+  (resume)
```

```csharp
public class GameManager : MonoBehaviour
{
    public static GameManager Instance { get; private set; }

    private StateMachine<GameManager> _stateMachine;

    private void Awake()
    {
        Instance = this;
        DontDestroyOnLoad(gameObject);

        _stateMachine = new StateMachine<GameManager>(this);
        _stateMachine.AddState(new MainMenuState(this, _stateMachine));
        _stateMachine.AddState(new LoadingState(this, _stateMachine));
        _stateMachine.AddState(new GameplayState(this, _stateMachine));
        _stateMachine.AddState(new PauseState(this, _stateMachine));
        _stateMachine.AddState(new GameOverState(this, _stateMachine));

        _stateMachine.ChangeState<MainMenuState>();
    }

    private void Update()
    {
        _stateMachine.Update();
    }

    // Convenience methods for external callers
    public void StartGame() => _stateMachine.ChangeState<LoadingState>();
    public void PauseGame() => _stateMachine.ChangeState<PauseState>();
    public void ResumeGame() => _stateMachine.RevertToPreviousState();
    public void GameOver() => _stateMachine.ChangeState<GameOverState>();
    public void ReturnToMenu() => _stateMachine.ChangeState<MainMenuState>();
}
```

### Pause State Example

```csharp
public class PauseState : IState
{
    private GameManager _owner;
    private StateMachine<GameManager> _sm;

    public PauseState(GameManager owner, StateMachine<GameManager> sm)
    {
        _owner = owner;
        _sm = sm;
    }

    public void Enter()
    {
        Time.timeScale = 0f;
        // Show pause menu UI
    }

    public void Exit()
    {
        Time.timeScale = 1f;
        // Hide pause menu UI
    }

    public void Update() { }

    // Called by InputView when the Pause action fires (UI action map while paused).
    public void OnPausePressed() => _sm.RevertToPreviousState();

    public void FixedUpdate() { }
}
```

---

## Enemy AI States

A patrol/chase/attack AI using the same state machine.

```
Idle → Patrol → Detect → Chase → Attack → Flee → Dead
```

### Patrol State

```csharp
public class EnemyPatrolState : IState
{
    private EnemyController _enemy;
    private StateMachine<EnemyController> _sm;
    private int _waypointIndex;

    public EnemyPatrolState(EnemyController enemy, StateMachine<EnemyController> sm)
    {
        _enemy = enemy;
        _sm = sm;
    }

    public void Enter()
    {
        _enemy.Animator.Play("Walk");
        _enemy.MoveSpeed = _enemy.PatrolSpeed;
    }

    public void Exit() { }

    public void Update()
    {
        // Check for player detection
        if (_enemy.CanSeePlayer())
        {
            _sm.ChangeState<EnemyChaseState>();
            return;
        }

        // Move toward current waypoint
        Vector3 target = _enemy.Waypoints[_waypointIndex].position;
        _enemy.MoveToward(target);

        // Advance to next waypoint when close enough
        if (Vector3.Distance(_enemy.transform.position, target) < 0.3f)
        {
            _waypointIndex = (_waypointIndex + 1) % _enemy.Waypoints.Length;
        }
    }

    public void FixedUpdate() { }
}
```

### Chase State

```csharp
public class EnemyChaseState : IState
{
    private EnemyController _enemy;
    private StateMachine<EnemyController> _sm;
    private float _losePlayerTimer;

    public EnemyChaseState(EnemyController enemy, StateMachine<EnemyController> sm)
    {
        _enemy = enemy;
        _sm = sm;
    }

    public void Enter()
    {
        _enemy.Animator.Play("Run");
        _enemy.MoveSpeed = _enemy.ChaseSpeed;
        _losePlayerTimer = 0f;
    }

    public void Exit() { }

    public void Update()
    {
        float distToPlayer = Vector3.Distance(
            _enemy.transform.position, _enemy.Player.position);

        // Close enough to attack
        if (distToPlayer <= _enemy.AttackRange)
        {
            _sm.ChangeState<EnemyAttackState>();
            return;
        }

        // Lost sight of player
        if (!_enemy.CanSeePlayer())
        {
            _losePlayerTimer += Time.deltaTime;
            if (_losePlayerTimer > _enemy.LosePlayerDelay)
            {
                _sm.ChangeState<EnemyPatrolState>();
                return;
            }
        }
        else
        {
            _losePlayerTimer = 0f;
        }

        // Low health: flee
        if (_enemy.HealthPercent < _enemy.FleeThreshold)
        {
            _sm.ChangeState<EnemyFleeState>();
            return;
        }

        _enemy.MoveToward(_enemy.Player.position);
    }

    public void FixedUpdate() { }
}
```

---

## Hierarchical FSM

A hierarchical state machine is a state that contains its own sub-state machine. This avoids state explosion when behaviors have nested phases.

Example: A "Combat" state that internally has Approach, Attack, and Retreat sub-states.

```csharp
public class EnemyCombatState : IState
{
    private EnemyController _enemy;
    private StateMachine<EnemyController> _parentSM;
    private StateMachine<EnemyController> _subSM;

    public EnemyCombatState(EnemyController enemy, StateMachine<EnemyController> parentSM)
    {
        _enemy = enemy;
        _parentSM = parentSM;

        _subSM = new StateMachine<EnemyController>(enemy);
        _subSM.AddState(new CombatApproachSubState(enemy, _subSM));
        _subSM.AddState(new CombatAttackSubState(enemy, _subSM));
        _subSM.AddState(new CombatRetreatSubState(enemy, _subSM));
    }

    public void Enter()
    {
        _subSM.ChangeState<CombatApproachSubState>();
    }

    public void Exit()
    {
        _subSM.CurrentState?.Exit();
    }

    public void Update()
    {
        // Parent-level transitions (flee, death) take priority
        if (_enemy.HealthPercent < _enemy.FleeThreshold)
        {
            _parentSM.ChangeState<EnemyFleeState>();
            return;
        }

        // Delegate to sub-state
        _subSM.Update();
    }

    public void FixedUpdate()
    {
        _subSM.FixedUpdate();
    }
}
```

This keeps the parent state machine simple (Patrol, Combat, Flee, Dead) while Combat handles its own complexity internally.

---

## Transition Conditions

For more complex state machines, define explicit transition rules rather than embedding transition logic in each state.

```csharp
using System;
using System.Collections.Generic;

public class TransitionRule
{
    public Type FromState;
    public Type ToState;
    public Func<bool> Condition;
}

public class StateMachineWithTransitions<T>
{
    private StateMachine<T> _inner;
    private List<TransitionRule> _transitions = new();

    public StateMachineWithTransitions(T owner)
    {
        _inner = new StateMachine<T>(owner);
    }

    public void AddState(IState state) => _inner.AddState(state);

    public void AddTransition<TFrom, TTo>(Func<bool> condition)
        where TFrom : IState where TTo : IState
    {
        _transitions.Add(new TransitionRule
        {
            FromState = typeof(TFrom),
            ToState = typeof(TTo),
            Condition = condition
        });
    }

    /// <summary>
    /// Add a transition that can fire from ANY state.
    /// </summary>
    public void AddAnyTransition<TTo>(Func<bool> condition) where TTo : IState
    {
        _transitions.Add(new TransitionRule
        {
            FromState = null, // null means "any"
            ToState = typeof(TTo),
            Condition = condition
        });
    }

    public void Update()
    {
        // Check transitions before updating current state
        foreach (var rule in _transitions)
        {
            if (rule.FromState != null &&
                _inner.CurrentState?.GetType() != rule.FromState)
                continue;

            if (rule.Condition())
            {
                // Use reflection or a lookup to change state by Type
                // (Simplified here; in production, store state instances by Type)
                break;
            }
        }

        _inner.Update();
    }
}
```

This approach centralizes transition logic and makes it easier to visualize the state graph.

---

## Event-Driven Transitions

Some transitions are triggered by external events (taking damage, picking up an item) rather than polled conditions.

```csharp
// In the state machine owner:
public void OnDamageTaken(int amount)
{
    if (amount > _staggerThreshold)
    {
        _stateMachine.ChangeState<PlayerHurtState>();
    }
}

public void OnHealthDepleted()
{
    _stateMachine.ChangeState<PlayerDeadState>();
}
```

Prefer event-driven transitions for one-shot triggers (damage, death, interaction). Use polled transitions for continuous conditions (grounded check, distance to enemy).

---

## ScriptableObject States

For designer-configurable behavior, define state parameters in ScriptableObjects. The SO holds data; a runtime state class reads it.

```csharp
[CreateAssetMenu(menuName = "AI/Patrol Config")]
public class PatrolStateConfig : ScriptableObject
{
    public float moveSpeed = 2f;
    public float waitTimeAtWaypoint = 1.5f;
    public float detectionRange = 8f;
    public string animationName = "Walk";
}

public class ConfigurablePatrolState : IState
{
    private EnemyController _enemy;
    private PatrolStateConfig _config;

    public ConfigurablePatrolState(EnemyController enemy, PatrolStateConfig config)
    {
        _enemy = enemy;
        _config = config;
    }

    public void Enter()
    {
        _enemy.Animator.Play(_config.animationName);
        _enemy.MoveSpeed = _config.moveSpeed;
    }

    // ... rest of state logic uses _config fields
}
```

This lets designers create different patrol profiles (slow cautious guard, fast perimeter patrol) without touching code.

---

## Practical Tips

- **Debug visualization:** Log state transitions with `Debug.Log($"[{owner.name}] {PreviousState?.GetType().Name} -> {CurrentState.GetType().Name}")`. Add a `#if UNITY_EDITOR` guard so it compiles out in builds.
- **Avoid string-based states.** Use type-safe state references (generics or enums). String comparisons are fragile and miss refactoring.
- **One state machine per concern.** Do not mix movement states and animation states in the same FSM. Use separate machines that communicate through the owner.
- **State pooling:** The `AddState` approach creates states once and reuses them. Never allocate new state objects per transition; this creates garbage collection pressure.
- **Animator integration:** Map each state to an animator state name. Call `Animator.Play()` in `Enter()` rather than setting bool parameters, which are harder to debug.
- **Testing states in isolation:** Because states are plain C# classes (not MonoBehaviours), you can unit test them with a mock owner. This is a major advantage over Animator-based state machines.
