---
name: coherence-sync-field-ordering
description: Use when a coherence [Sync] field's value depends on another synced field — derived/computed synced values that come out wrong on remotes, intermittent desync when several fields change in the same packet, or a [Sync] setter that reads a sibling synced field. Covers why setters have no cross-field ordering guarantee and the four safe patterns for dependent values.
metadata:
  topic: networking
  engine: coherence
---

# Synced field dependencies & ordering

## When to use this skill

- A `[Sync]` setter does work that reads *another* synced field: `set => _total = value + _other;`.
- A computed/derived synced value (`Total = Base + Bonus`) is wrong on remotes but right on the authority.
- Intermittent desync that only shows up when several synced fields change in the same tick.
- "Sometimes it's right, sometimes it's off by the last value" — a classic stale-sibling read.
- You're about to put cross-field logic in a setter and want to know where it actually belongs.

## The core idea

When a packet updates several synced fields, coherence writes the bindings **one at a time, in binding order**, and only *afterwards* fires `[OnValueSynced]` callbacks. So there are two very different moments, with two different guarantees:

| Where your code runs | Guarantee about *other* synced fields |
|---|---|
| Inside a `[Sync]` **setter** (`set =>`) | ❌ **None.** A sibling field updated by the same packet may not be written yet — you can read a stale value. The order is the binding list order, which is not something you should rely on. |
| Inside an `[OnValueSynced]` **callback** | ✅ **All synced fields on the entity are already applied.** Callbacks run in a separate pass after every binding is written. |

**The rule: a `[Sync]` setter must store its own raw value and nothing else. Any work that reads a second synced field belongs in `[OnValueSynced]`, in the getter, or in a per-frame recompute — never in the setter.**

This is not a config you can flip or a field order you can fix. Setters are inherently per-field; the moment a setter's correctness depends on a sibling field, it's racing the deserializer.

## The anti-pattern

```csharp
// WRONG — _other may not be deserialized yet when MyValue's setter runs.
[Sync] public int MyValue   { get => _actual; set => _actual = value + _other; }
[Sync] public int OtherValue { get => _other;  set => _other = value; }
```

On the authority this looks fine (both fields are set by your own code, in your order). On a remote receiving both in one packet, `MyValue`'s setter may run before `OtherValue`'s, so `_other` is last tick's value. The bug is invisible until two fields change together.

## Pattern 1: Compute on read

Setters store raw inputs; the derived value is computed in the getter (or a plain accessor). Order can't matter because nothing is combined until something reads it.

```csharp
[Sync] public int Base  { get => _base;  set => _base = value; }
[Sync] public int Bonus { get => _bonus; set => _bonus = value; }

// Not synced — derived from synced inputs whenever it's needed.
public int Total => _base + _bonus;
```

Best when the derived value is cheap to compute and only consumed on demand (UI, gameplay checks). This is the same shape as a 2D blendtree reading two synced axis floats at render time — neither axis combines the other in its setter.

## Pattern 2: Derive in OnValueSynced

When you need to *react* to the combination (fire an effect, push to an Animator, cache an expensive result), do it in `[OnValueSynced]`. By the time it runs, every synced field on the entity is current.

```csharp
[Sync, OnValueSynced(nameof(Recompute))] public int Base  { get; set; }
[Sync, OnValueSynced(nameof(Recompute))] public int Bonus { get; set; }

private void Recompute<T>(T _, T __)   // signature is (oldValue, newValue)
{
    _total = Base + Bonus;             // both reads are safe here
    _bar.SetValue(_total);
}
```

Point both fields at the same callback so the derived value refreshes no matter which one changed. The callback is idempotent, so being invoked twice (once per changed field) recomputes the same answer — fine.

## Pattern 3: Recompute in LateUpdate (dirty flag)

When the reaction is expensive, or you explicitly want it *once per frame* regardless of how many fields changed, flag dirty in the setters/callbacks and resolve in `LateUpdate`.

```csharp
[Sync] public int Base  { get => _base;  set { _base = value;  _dirty = true; } }
[Sync] public int Bonus { get => _bonus; set { _bonus = value; _dirty = true; } }

private void LateUpdate()
{
    if (!_dirty) return;
    _total = _base + _bonus;   // all sync for the frame has been applied
    _dirty = false;
}
```

Setting a local dirty flag is the *one* side effect a setter may safely have — it reads no sibling field. The actual cross-field math happens after the frame's deserialization is done.

## Pattern 4: Sync the derived value itself

If the authority already knows the answer, don't make every remote recompute it — send the result as its own field. Trades a few bytes for zero recompute and zero ordering risk.

```csharp
// Authority computes once and writes the answer; remotes just read it.
[Sync] public int Total { get; private set; }

private void OnInputsChanged()       // called on the authority only
{
    if (!_sync.HasStateAuthority) return;
    Total = _base + _bonus;
}
```

Best when the derivation is expensive, non-deterministic, or you want a single source of truth. Costs bandwidth and is redundant with the inputs, so prefer Patterns 1–3 for cheap deterministic math.

## When it works / when it doesn't

- **Compute-on-read** works when the math is cheap and pull-based. It runs on every read — don't hide an expensive computation behind a property a hot loop hits.
- **OnValueSynced** works for push-based reactions on **remotes**. It does **not** fire on the authority that wrote the value (the authority must produce the reaction inline in its own write path). See [coherence-authority-handoff](../coherence-authority-handoff/SKILL.md) for the dual-apply shape.
- **LateUpdate dirty-flag** works when the reaction is expensive or must run at most once per frame, and you're fine with a one-frame deferral.
- **Sync-the-derived-value** works when authority is the single source of truth, at the cost of bandwidth.

## Gotchas

- **Setter execution order is binding-list order, not declaration intent.** Re-baking or reordering fields can silently change *which* stale value a cross-field setter reads. Never depend on it — that's the whole point of this skill.
- **`[OnValueSynced]` fires once per changed field.** If three fields share a recompute callback and all three change, the callback runs three times that tick. Make it idempotent (recompute the same answer) or coalesce via a dirty flag.
- **`[OnValueSynced]` does not fire on the authority.** Derived state the authority needs must be computed in its own write path, not assumed from the callback.
- **A dirty flag is the only safe setter side effect.** `set { _x = value; _dirty = true; }` is fine. `set { _x = value; DoWorkReading(_y); }` is the bug.
- **Predicted bindings are skipped during interpolation** (`IsCurrentlyPredicted`), so a locally-predicted field won't even run its setter from the network that tick — another reason not to chain logic through setters.
- **This is per-entity, not per-component-instance-in-isolation.** Sibling synced fields on *other components* of the same entity are also fully applied before callbacks fire, so OnValueSynced may safely read them too.

## Anti-patterns

- `set => _total = value + _other;` — cross-field math in a setter. The headline bug.
- Reordering `[Sync]` fields to "fix" a derived value. You're tuning a race; it'll come back.
- An `[OnValueSynced]` callback that reads a sibling field and *also* re-writes a third synced field expecting downstream callbacks in a particular order. Keep callbacks to local derivation.
- Recomputing an expensive derived value on every read via a property getter that a per-frame system polls. Use Pattern 3 or 4 instead.

## See also

- [coherence-animation-networking](../coherence-animation-networking/SKILL.md) — uses the property-setter idiom; safe there only because each setter writes one Animator parameter and reads no sibling synced field.
- [coherence-authority-handoff](../coherence-authority-handoff/SKILL.md) — `OnValueSynced` semantics, remote-only firing, and the dual-apply pattern.
- coherence docs: bindings, `[OnValueSynced]`, baking (re-bake after adding/removing `[Sync]` fields).
