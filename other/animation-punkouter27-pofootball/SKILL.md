---
name: animation
description: "Unity animation system — Animator controllers, layers, blend trees, state machine behaviors, root motion, animation events, Timeline."
globs: ["**/*.controller", "**/*Anim*.cs", "**/*.anim"]
---

# Animation System

## Animator Controller

### Parameters
```csharp
// Cache hash IDs — NEVER use string version in Update
private static readonly int SpeedHash = Animator.StringToHash("Speed");
private static readonly int JumpHash = Animator.StringToHash("Jump");
private static readonly int IsGroundedHash = Animator.StringToHash("IsGrounded");
private static readonly int AttackHash = Animator.StringToHash("Attack");

private void Update()
{
    _animator.SetFloat(SpeedHash, _currentSpeed);
    _animator.SetBool(IsGroundedHash, _isGrounded);
}

// Triggers: fire once, auto-reset
public void Attack() => _animator.SetTrigger(AttackHash);
```

### Transition Settings
- **Has Exit Time:** animation finishes before transitioning (good for attacks, bad for instant response)
- **Fixed Duration:** transition time in seconds vs normalized
- **Transition Duration:** blend time (0 for instant, 0.1-0.25 for smooth)
- **Interruption Source:** which transitions can interrupt this one

### Layers
- Base Layer: locomotion (walk, run, idle)
- Upper Body Layer (Avatar Mask): aiming, attacks (overrides base)
- Additive Layer: breathing, hit reactions (adds on top)

## Blend Trees

**1D:** Speed parameter → walk/run blend
**2D Simple Directional:** X/Y input → directional movement (forward, back, strafe)
**2D Freeform:** more flexible placement of motion clips

## State Machine Behaviors

```csharp
public sealed class AttackStateBehavior : StateMachineBehaviour
{
    public override void OnStateEnter(Animator animator, AnimatorStateInfo stateInfo, int layerIndex)
    {
        // Enable hitbox
        animator.GetComponent<CombatSystem>().EnableHitbox();
    }

    public override void OnStateExit(Animator animator, AnimatorStateInfo stateInfo, int layerIndex)
    {
        // Disable hitbox
        animator.GetComponent<CombatSystem>().DisableHitbox();
    }
}
```

## Root Motion

- Enable `Apply Root Motion` on Animator
- Override in `OnAnimatorMove()` for custom control:

```csharp
private void OnAnimatorMove()
{
    // Use animation's root motion for position
    Vector3 deltaPosition = _animator.deltaPosition;
    transform.position += deltaPosition;

    // Use animation's rotation
    transform.rotation *= _animator.deltaRotation;
}
```

## Animation Events

Call methods from specific frames in animation clips:
```csharp
// Called from animation event on frame 12
public void OnFootstep()
{
    _audioSource.PlayOneShot(_footstepClip);
}

public void OnAttackHit()
{
    // Check hitbox collisions at this exact frame
}
```

## IK (Inverse Kinematics)

```csharp
private void OnAnimatorIK(int layerIndex)
{
    if (_lookTarget != null)
    {
        _animator.SetLookAtWeight(1f, 0.3f, 0.6f, 1f);
        _animator.SetLookAtPosition(_lookTarget.position);
    }

    // Foot IK for uneven terrain
    _animator.SetIKPositionWeight(AvatarIKGoal.LeftFoot, 1f);
    _animator.SetIKPosition(AvatarIKGoal.LeftFoot, _leftFootTarget);
}
```

## Timeline Integration

- Animation Track: play animation clips on any Animator
- Custom Playable: create custom Timeline clips with `PlayableAsset` + `PlayableBehaviour`
- Signal Track: fire events at specific times (similar to animation events but on Timeline)
