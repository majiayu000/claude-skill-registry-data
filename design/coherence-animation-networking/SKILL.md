---
name: coherence-animation-networking
description: Use for networked animation issues in coherence — triggers not firing on remotes, late joiners stuck in T-pose, animator parameters desyncing, or hitting the 32-field schema limit. Covers triggers via Command, state via Sync, sharding animator bindings, and late-joiner correctness.
metadata:
  topic: networking
  engine: coherence
---

# Animation networking

## When to use this skill

- "My animation trigger fires locally but the remote player stays still."
- "Late joiners see characters in T-pose or in the wrong state."
- The developer is wiring up a humanoid with many animator parameters.
- Hitting "schema component has too many fields" / 32-field cap.
- Mixing Animator Triggers, Bools, and Floats and getting inconsistent results.

## The core idea

Unity's `Animator` parameters split cleanly into two camps:

- **Stateful** — `bool`, `float`, `int`. Have a *value at any moment*. Late joiners need to know the current value. → Use `[Sync]`.
- **One-shot** — `Trigger`. Has no persistent state — it fires and consumes. Late joiners shouldn't replay it. → Use `[Command]`.

Treat these as different problems with different solutions. The single most common bug is using a `[Sync] bool` for what should be a `Trigger`, or a `Trigger` for what should be a `[Sync] bool`.

## Pattern 1: Triggers via Command

A trigger represents "the action just happened." Authority calls `SetTrigger` locally and broadcasts a command for remotes to do the same.

```csharp
public class ActorAnimation : MonoBehaviour
{
    [SerializeField] private Animator _animator;
    private CoherenceSync _sync;

    private void Awake() => _sync = GetComponent<CoherenceSync>();

    public void Jump()
    {
        if (!_sync.HasStateAuthority) return;

        _animator.SetTrigger("Jump");
        _ = _sync.SendCommand<ActorAnimation>(
            nameof(RemoteSetTrigger),
            MessageTarget.Other,
            "Jump");
    }

    [Command]
    public void RemoteSetTrigger(string parameter)
    {
        _animator.SetTrigger(parameter);
    }
}
```

Late joiners *correctly* don't replay the jump — they only see the post-jump state, which is the right behaviour for a one-shot animation. (If you want them to see something, that something is persistent state and belongs as a `[Sync]` field.)

## Pattern 2: Persistent state via Sync

Bools (`IsGrounded`, `IsDead`, `IsCarrying`), floats (`MoveSpeed`, `LookYaw`), and ints (`WeaponIndex`) are persistent — late joiners need the current value to render the character correctly.

```csharp
public class ActorAnimation : MonoBehaviour
{
    [SerializeField] private Animator _animator;

    [Sync] public bool  IsGrounded { get => _animator.GetBool("IsGrounded");  set => _animator.SetBool("IsGrounded", value); }
    [Sync] public bool  IsDead     { get => _animator.GetBool("IsDead");      set => _animator.SetBool("IsDead", value); }
    [Sync] public float MoveSpeed  { get => _animator.GetFloat("MoveSpeed");  set => _animator.SetFloat("MoveSpeed", value); }
    [Sync] public float LookYaw    { get => _animator.GetFloat("LookYaw");    set => _animator.SetFloat("LookYaw", value); }

    private void Update()
    {
        if (!GetComponent<CoherenceSync>().HasStateAuthority) return;
        // Authority writes; sync handles the rest.
        IsGrounded = CheckGrounded();
        MoveSpeed  = _rb.velocity.magnitude;
        LookYaw    = transform.eulerAngles.y;
    }
}
```

The property getter/setter shape is idiomatic — it lets the field *be* the animator parameter rather than a shadow that has to be kept in sync manually. The sync system reads the property as it would any field.

## Pattern 3: Sharding when you hit 32 fields

A `CoherenceSync` schema component can hold at most 32 synced fields. A complex humanoid easily blows past this (locomotion + combat + emotes + mount + dialogue). Split into multiple sibling components on the same prefab — each gets its own 32-field budget.

```csharp
// On the player prefab, three sibling MonoBehaviours, each with its own [Sync] fields:

public class ActorLocomotion : MonoBehaviour
{
    [Sync] public bool  IsGrounded { ... }
    [Sync] public float MoveForward { ... }
    [Sync] public float MoveRight   { ... }
    [Sync] public bool  IsCrouching { ... }
    // ...
}

public class ActorCombat : MonoBehaviour
{
    [Sync] public int   WeaponIndex { ... }
    [Sync] public bool  IsAttacking { ... }
    [Sync] public float LayerWeight { ... }
    // ...
}

public class ActorEmotes : MonoBehaviour
{
    [Sync] public bool IsDancing { ... }
    [Sync] public int  EmoteIndex { ... }
    // ...
}
```

Group by *concern*, not by parameter type — keep all combat fields together so a refactor doesn't shuffle them across components. Each component bakes to its own schema component; coherence handles them independently.

## Pattern 4: Animator layer weights

Layer weights (the float you'd pass to `Animator.SetLayerWeight`) are persistent state. Sync them:

```csharp
[Sync] public float CombatLayerWeight
{
    get => _animator.GetLayerWeight(1);
    set => _animator.SetLayerWeight(1, value);
}
```

The default layer (index 0) is always at weight 1 and doesn't need syncing. Override layers (combat overlay, aim-down-sights mask) absolutely do — without them, remote clients see the wrong masking.

## Pattern 5: Avoid syncing IK / procedural overrides

`Animator.SetIKPosition`, `OnAnimatorIK`, post-process humanoid procedural overrides — these run in the animator's update loop and can't be cleanly synced as fields. Instead:

- Compute the *input* to the IK on each client locally (look target, foot ray result) from already-synced state (player position, head bone direction).
- Don't try to sync the resulting IK transforms.

Same logic for ragdolls: sync the trigger ("I died with this impulse") via Command, then let each client run the same ragdoll simulation deterministically.

## When it works / when it doesn't

**Trigger-via-Command works when** the animation is fire-and-forget and late joiners genuinely shouldn't see the past event.

**Sync-as-property works when** the value can be read and written cheaply. `Animator.GetFloat` is cheap; check the profiler if you have hundreds of synced floats per frame.

**It breaks when:**
- A trigger fires while the remote client hasn't joined yet — they miss it. If the resulting state is persistent (now in a "dead" state), capture it in a `[Sync] bool` too.
- The animator state itself is sync-relevant (which clip is playing). coherence doesn't sync the state machine state directly — drive it from synced bools/floats and let each client's animator transition naturally.

## Gotchas

- **`SetTrigger` followed immediately by `ResetTrigger` is a no-op locally but the command still fires remotely** — they'll play the animation when you didn't intend to. Don't pre-clear triggers across the network boundary.
- **Floats use 4 bytes per send by default.** A character with 20 synced floats at 20 Hz is 1.6 KB/s/character just for animation. Consider lowering precision (compress to short/byte) or sampling less often for non-critical params.
- **`Animator.SetBool` for a parameter that doesn't exist is silent.** Typos in parameter names produce no errors, just dead animations. Cache `Animator.StringToHash` results and use the int overload to catch typos at startup.
- **Layer weights default to whatever the AnimatorController asset says.** A remote client joining at runtime gets your synced value, but if you forget to sync it, they get the asset default — usually 0, leaving combat overlay invisible.
- **Re-baking after adding/removing `[Sync]` fields is mandatory.** Code that compiles will still misbehave at runtime if the schema is stale.
- **The setter-as-property idiom above is safe only because each setter writes one Animator parameter and reads no *other* synced field.** The moment a setter combines a sibling synced field (`set => _animator.SetFloat("Blend", value * _otherSyncedField)`), it races deserialization order and breaks on remotes. Keep cross-field math out of setters — see [coherence-sync-field-ordering](../coherence-sync-field-ordering/SKILL.md).

## Anti-patterns

- `[Sync] bool DidJump` that's toggled true for one frame. That's a trigger pretending to be state — use a command.
- Network-side animation state machine ("synced AnimationStateEnum"). The Animator already is a state machine; duplicating it networked is wasteful and gets out of sync.
- Manually tracking which trigger has fired and replaying it for late joiners. If late joiners need to see the result, the result is persistent state — model it that way.
- Twenty synced floats for `LeftToe`, `RightToe`, `LeftHip`, etc. Either fewer (sync the *inputs* IK reads, not the outputs) or compressed via a packed component.

## See also

- coherence docs: bindings, archetypes (LOD groups can drop animation fields at distance), schema baking.
- [coherence-bandwidth-at-scale](../coherence-bandwidth-at-scale/SKILL.md) — if you have *many* animated characters, the bandwidth angle dominates.
- [coherence-rpc-routing](../coherence-rpc-routing/SKILL.md) — `MessageTarget.Other` is the right call for animation broadcast; `All` would re-fire on the sender.
