---
name: rust-iterators
description: Leverage iterator chains for efficient, lazy data processing without intermediate allocations. Use when processing collections.
---

# Iterator Patterns

Efficient data processing with lazy iterator chains.

## Basic Iterator Chain

```rust
// Single pass, lazy evaluation, no intermediate allocations
let result: Vec<_> = data
    .iter()
    .filter(|&&x| x > 2)
    .map(|&x| x * 2)
    .collect();

// Sum without collecting
let sum: i32 = data.iter().filter(|&&x| x > 0).sum();

// Count matches
let count = data.iter().filter(|x| x.is_valid()).count();
```

## Common Iterator Methods

```rust
// Transform each element
.map(|x| transform(x))

// Keep elements matching predicate
.filter(|x| predicate(x))

// Transform + flatten (Option/Result/Vec)
.filter_map(|x| x.ok())          // Filter None/Err, unwrap Some/Ok
.flat_map(|x| x.into_iter())     // Flatten nested iterables

// Take/skip elements
.take(10)                         // First 10 elements
.skip(5)                          // Skip first 5
.take_while(|x| x < &100)        // Take while condition true
.skip_while(|x| x < &10)         // Skip while condition true

// Find elements
.find(|x| predicate(x))          // First match (Option)
.position(|x| predicate(x))      // Index of first match
.any(|x| predicate(x))           // Any match exists
.all(|x| predicate(x))           // All match

// Reduce/fold
.fold(0, |acc, x| acc + x)       // Reduce with initial value
.reduce(|a, b| a + b)            // Reduce without initial
.sum::<i32>()                    // Sum numbers
.product::<i32>()                // Multiply numbers

// Collect to different types
.collect::<Vec<_>>()
.collect::<HashSet<_>>()
.collect::<String>()
.collect::<Result<Vec<_>, _>>()  // Collect Results, fail on first Err
```

## Parallel Iteration with Rayon

```rust
use rayon::prelude::*;

// Parallel iteration (automatic work stealing)
let sum: i32 = data.par_iter().map(|x| expensive(x)).sum();

// Parallel sort
let mut data = data;
data.par_sort();

// Parallel filter + map
let results: Vec<_> = data
    .par_iter()
    .filter(|x| predicate(x))
    .map(|x| transform(x))
    .collect();
```

## Enumerate and Zip

```rust
// Get index with element
for (index, item) in items.iter().enumerate() {
    println!("{}: {}", index, item);
}

// Pair two iterators
let pairs: Vec<_> = keys.iter().zip(values.iter()).collect();

// Unzip pairs
let (keys, values): (Vec<_>, Vec<_>) = pairs.into_iter().unzip();
```

## Chain and Flatten

```rust
// Concatenate iterators
let combined: Vec<_> = first.iter()
    .chain(second.iter())
    .chain(third.iter())
    .collect();

// Flatten nested iterables
let flat: Vec<_> = nested_vecs.iter().flatten().collect();

// Flatten with transformation
let all_items: Vec<_> = containers
    .iter()
    .flat_map(|c| c.items())
    .collect();
```

## Peekable Iterator

```rust
let mut iter = data.iter().peekable();

while let Some(&current) = iter.next() {
    // Look ahead without consuming
    if let Some(&&next) = iter.peek() {
        if next > current {
            // Do something
        }
    }
}
```

## Windows and Chunks

```rust
// Overlapping windows of size 3
for window in data.windows(3) {
    let [a, b, c] = window else { continue };
    // Process window
}

// Non-overlapping chunks
for chunk in data.chunks(100) {
    process_batch(chunk);
}

// Exact chunks (panic if not divisible)
for chunk in data.chunks_exact(100) {
    process_batch(chunk);
}
```

## Custom Iterator

```rust
struct Counter {
    current: usize,
    max: usize,
}

impl Iterator for Counter {
    type Item = usize;

    fn next(&mut self) -> Option<Self::Item> {
        if self.current < self.max {
            let result = self.current;
            self.current += 1;
            Some(result)
        } else {
            None
        }
    }

    // Optional: Provide size hint for better allocation
    fn size_hint(&self) -> (usize, Option<usize>) {
        let remaining = self.max - self.current;
        (remaining, Some(remaining))
    }
}

// ExactSizeIterator if size is known
impl ExactSizeIterator for Counter {}
```

## Collect into Result

```rust
// Collect Vec<Result<T, E>> into Result<Vec<T>, E>
let results: Result<Vec<_>, _> = items
    .iter()
    .map(|item| fallible_operation(item))
    .collect();

// Short-circuits on first error
match results {
    Ok(values) => process(values),
    Err(e) => handle_error(e),
}
```

## Performance Tips

```rust
// Avoid: Collecting intermediate results
let temp: Vec<_> = data.iter().filter(|x| x > &0).collect();
let result: i32 = temp.iter().sum();

// Better: Chain without collecting
let result: i32 = data.iter().filter(|&&x| x > 0).sum();

// Use iterator methods over manual loops
// Avoid:
let mut sum = 0;
for x in &data {
    if *x > 0 {
        sum += x;
    }
}

// Prefer:
let sum: i32 = data.iter().filter(|&&x| x > 0).sum();
```

## Guidelines

- Prefer iterator chains over manual loops
- Avoid collecting intermediate results
- Use `filter_map` to combine filter + map for Options
- Use `flat_map` to flatten nested structures
- Use Rayon for CPU-bound parallel work
- Implement `size_hint` for custom iterators
- Use `chunks` for batch processing

## Examples

See `hercules-local-algo/src/pipeline/` for iterator patterns.
