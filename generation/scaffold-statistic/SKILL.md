---
name: scaffold-statistic
description: Generate boilerplate for a new statistic following library conventions
disable-model-invocation: true
---

# Scaffold Statistic

Generate the boilerplate code for adding a new statistic to qsv-stats, following established library conventions.

## Arguments

The user should provide:
- **Name** of the statistic (e.g., `coefficient_of_variation`)
- **Module** to add it to (`unsorted`, `online`, `frequency`, or `minmax`) — or suggest one based on the statistic's nature
- **Precalculated parameters** (optional) — intermediate values it can accept to avoid redundant computation

## What to Generate

### 1. Module-level convenience function

```rust
/// Brief description of the statistic.
///
/// This has time complexity `O(...)` and space complexity `O(...)`.
///
/// ## Example
///
/// ```
/// use stats;
///
/// let vals = vec![1, 2, 3, 4, 5];
/// let result = stats::statistic_name(vals.into_iter());
/// ```
pub fn statistic_name<I>(it: I, precalc_param: Option<f64>) -> Option<f64>
where
    I: Iterator,
    I::Item: PartialOrd + ToPrimitive,
{
    let mut unsorted = Unsorted::new();
    unsorted.extend(it);
    unsorted.statistic_name(precalc_param)
}
```

### 2. Instance method on the appropriate struct

```rust
pub fn statistic_name(&mut self, precalc_param: Option<f64>) -> Option<f64> {
    // TODO: implement
    todo!()
}
```

### 3. Tests (in the module's `#[cfg(test)]` block)

Generate edge-case tests following the existing pattern:

```rust
#[test]
fn test_statistic_name_empty() {
    let vals: Vec<f64> = vec![];
    assert_eq!(statistic_name(vals.into_iter(), None), None);
}

#[test]
fn test_statistic_name_single() {
    let vals = vec![42.0];
    // TODO: expected value for single element
}

#[test]
fn test_statistic_name_basic() {
    let vals = vec![1.0, 2.0, 3.0, 4.0, 5.0];
    // TODO: expected value
}

#[test]
fn test_statistic_name_duplicates() {
    let vals = vec![1.0, 1.0, 2.0, 2.0, 3.0];
    // TODO: expected value
}

#[test]
fn test_statistic_name_negatives() {
    let vals = vec![-3.0, -1.0, 0.0, 1.0, 3.0];
    // TODO: expected value
}

#[test]
fn test_statistic_name_with_precalc() {
    // Test that passing precalculated values produces same result
    let vals = vec![1.0, 2.0, 3.0, 4.0, 5.0];
    let without = statistic_name(vals.clone().into_iter(), None);
    let with = statistic_name(vals.into_iter(), Some(precalc_value));
    assert_eq!(without, with);
}
```

## Conventions to Follow

- Use `.mul_add()` for any `a * b + c` arithmetic
- Use `to_f64()` via `ToPrimitive` for numeric conversions
- Wrap unsafe conversions in `unsafe { ... }` with `// SAFETY:` comments
- Accept optional precalculated parameters to avoid redundant computation
- Add `#[inline]` on small methods
- Use `Partial<T>` wrapper when sorting `PartialOrd` types
- Respect the parallel threshold: use rayon for collections ≥10,000 elements
- Add `+ Sync` to type bounds if rayon parallel operations are used

## After Scaffolding

Remind the user to:
1. Fill in the `todo!()` implementation
2. Update the expected values in tests
3. Add a re-export in `lib.rs` if it's a module-level function
4. Run `cargo test` to verify
