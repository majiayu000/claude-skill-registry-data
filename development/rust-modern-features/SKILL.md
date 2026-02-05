---
name: rust-modern-features
description: Modern Rust features from versions 1.80-1.92. Use when writing new code, reviewing for modern idioms, or upgrading codebases to use latest stable features. Reference for what's available in Rust 1.92.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Modern Rust Features (1.80 - 1.92)

Complete reference for features available in Rust 1.92 (current stable).

## Rust 1.92 (December 2025)

### Language
- `&raw [mut | const]` for union fields in safe code
- Combine `#[track_caller]` and `#[no_mangle]`
- `unused_must_use` no longer warns on `Result<_, Infallible>`

### APIs
```rust
// Zero-initialized allocations
let boxed: Box<[u8; 1024]> = Box::new_zeroed();
let arc_slice: Arc<[MaybeUninit<u8>]> = Arc::new_zeroed_slice(100);

// RwLock write -> read downgrade
let read_guard = write_guard.downgrade();

// BTreeMap entry insert
let entry = map.entry(key).insert_entry(value);

// NonZero ceiling division
let result = NonZeroU32::new(7).unwrap().div_ceil(NonZeroU32::new(3).unwrap());

// Const slice rotation
const ROTATED: [i32; 4] = {
    let mut arr = [1, 2, 3, 4];
    arr.rotate_left(1);
    arr  // [2, 3, 4, 1]
};
```

## Rust 1.91 (November 2025)

### Language
- C-style variadic functions for `sysv64`, `win64`, `efiapi`, `aapcs` ABIs

### APIs
```rust
// Duration convenience constructors
let hour = Duration::from_hours(1);
let mins = Duration::from_mins(30);

// Atomic pointer operations
atomic_ptr.fetch_ptr_add(offset, Ordering::SeqCst);
atomic_ptr.fetch_byte_add(1, Ordering::Relaxed);

// Strict arithmetic (panics on overflow in debug, UB in release)
let sum = a.strict_add(b);
let product = a.strict_mul(b);

// Carrying arithmetic for big integers
let (low, carry) = a.carrying_add(b, prev_carry);
let (low, high) = a.carrying_mul_add(b, c, d);

// Path utilities
let prefix = path.file_prefix();  // "file" from "file.tar.gz"
path_buf.add_extension("bak");    // "file.txt" -> "file.txt.bak"

// IP address constructors
let ipv4 = Ipv4Addr::from_octets([192, 168, 1, 1]);
let ipv6 = Ipv6Addr::from_segments([0, 0, 0, 0, 0, 0, 0, 1]);

// BTreeMap extract_if
let extracted: Vec<_> = map.extract_if(|k, v| v > &10).collect();
```

## Rust 1.90 (October 2025)

### APIs
```rust
// Signed subtraction on unsigned integers
let result = 10u32.checked_sub_signed(-5);   // Some(15)
let result = 10u32.saturating_sub_signed(20); // 0

// Const float rounding
const FLOOR: f64 = 3.7_f64.floor();  // 3.0
const CEIL: f64 = 3.2_f64.ceil();    // 4.0
const ROUND: f64 = 3.5_f64.round();  // 4.0

// Const slice reverse
const REVERSED: [i32; 3] = {
    let mut arr = [1, 2, 3];
    arr.reverse();
    arr  // [3, 2, 1]
};

// CStr/CString/Cow comparisons
let cstr: &CStr = c"hello";
let cstring = CString::new("hello").unwrap();
assert!(cstr == cstring);  // Now works!
```

## Rust 1.89 (September 2025)

### Language
- `#[repr(u128)]` and `#[repr(i128)]` for enums
- AVX-512 target features stabilized

### APIs
```rust
// File locking (cross-platform)
let file = File::open("data.txt")?;
file.lock()?;           // Exclusive lock
file.lock_shared()?;    // Shared lock
if file.try_lock().is_ok() { /* locked */ }
file.unlock()?;

// NonNull utilities
let nn = NonNull::from_ref(&value);
let nn = NonNull::from_mut(&mut value);

// Result flattening
let nested: Result<Result<i32, E>, E> = Ok(Ok(42));
let flat: Result<i32, E> = nested.flatten();  // Ok(42)

// Leak for owned strings
let leaked: &'static str = String::from("hello").leak();
let leaked: &'static OsStr = OsString::from("path").leak();
let leaked: &'static Path = PathBuf::from("/tmp").leak();

// NonZero<char>
let nz_char = NonZero::<char>::new('a').unwrap();
```

## Rust 1.88 (August 2025)

### Language
```rust
// Let chains (edition 2024)
if let Some(x) = opt && x > 0 && let Some(y) = other {
    // Both conditions met
}

while let Some(item) = iter.next() && item.is_valid() {
    process(item);
}

// Naked functions
#[naked]
pub unsafe extern "C" fn entry_point() {
    core::arch::naked_asm!("ret");
}

// Boolean cfg
#[cfg(false)]
fn never_compiled() {}
```

### APIs
```rust
// Cell::update
let cell = Cell::new(5);
cell.update(|x| x + 1);  // Now 6

// HashMap/HashSet extract_if
let removed: Vec<_> = map.extract_if(|k, v| k.starts_with("temp_")).collect();

// Slice chunking
let arr = [1, 2, 3, 4, 5, 6, 7];
let (chunks, remainder) = arr.as_chunks::<3>();
// chunks: [[1,2,3], [4,5,6]], remainder: [7]

// hint::select_unpredictable - optimization hint
let result = hint::select_unpredictable(condition, a, b);

// Anonymous pipes
let (reader, writer) = std::io::pipe()?;
```

## Rust 1.87 (July 2025)

### Language
- `asm_goto` for advanced inline assembly
- Precise capturing in traits with `use<...>`

### APIs
```rust
// Vec/LinkedList extract_if
let evens: Vec<_> = vec.extract_if(|x| x % 2 == 0).collect();

// Slice splitting
let (left, right) = slice.split_off(mid);
let (first, rest) = slice.split_off_first().unwrap();
let (init, last) = slice.split_off_last().unwrap();

// String extend
let mut s = String::from("hello");
s.extend_from_within(0..3);  // "hellohel"

// OsStr display
println!("{}", os_str.display());

// Pointer offset
let offset = ptr2.offset_from_unsigned(ptr1);

// Integer methods
assert!(6.is_multiple_of(3));
let mid = 10u32.midpoint(20);  // 15

// Direct UTF-8 conversion
let s = bytes.as_str();  // Instead of std::str::from_utf8()
```

## Rust 1.86 (June 2025)

### Language
```rust
// Trait object upcasting
trait Animal {}
trait Dog: Animal {}

fn upcast(dog: &dyn Dog) -> &dyn Animal {
    dog  // Now works!
}

// Safe target_feature
#[target_feature(enable = "avx2")]
fn simd_operation() {  // Can be safe now
    // AVX2 code
}
```

### APIs
```rust
// Float neighbors
let next = 1.0f64.next_up();    // Smallest float > 1.0
let prev = 1.0f64.next_down();  // Largest float < 1.0

// Disjoint mutable borrows
let [a, b] = slice.get_disjoint_mut([0, 5])?;

// Vec::pop_if
let popped = vec.pop_if(|x| *x > 10);

// Once::wait
static INIT: Once = Once::new();
INIT.call_once(|| initialize());
INIT.wait();  // Block until initialized

// OnceLock::wait
static CONFIG: OnceLock<Config> = OnceLock::new();
let config = CONFIG.wait();  // Block until set

// NonZero::count_ones
let ones = NonZeroU32::new(0b1011).unwrap().count_ones();  // 3

// Const black_box
const _: () = { std::hint::black_box(42); };
```

## Rust 1.85 (February 2025) - Edition 2024

### Language
```rust
// Async closures
let fetch = async |url: &str| {
    reqwest::get(url).await?.text().await
};

// Diagnostic attribute
#[diagnostic::do_not_recommend]
impl<T: NotRecommended> MyTrait for T {}
```

### APIs
```rust
// Waker utilities
let waker = Waker::noop();  // No-op waker for testing

// Function pointer comparison
if std::ptr::fn_addr_eq(f1, f2) { /* same function */ }

// Midpoint (no overflow)
let mid = 10u32.midpoint(20);  // 15

// New ErrorKind variants
match err.kind() {
    ErrorKind::QuotaExceeded => { /* disk quota */ }
    ErrorKind::CrossesDevices => { /* cross-device move */ }
    _ => {}
}

// Tuple FromIterator/Extend
let (a, b): (Vec<_>, Vec<_>) = pairs.into_iter().unzip();
```

## Rust 1.84 (January 2025)

### APIs
```rust
// Integer square root
let sqrt = 16u32.isqrt();        // 4
let sqrt = 17u32.checked_isqrt(); // Some(4)

// Pointer provenance
let ptr = std::ptr::without_provenance::<u8>(0x1000);
let ptr = std::ptr::dangling::<u8>();

// IPv6 checks
if addr.is_unique_local() { /* fc00::/7 */ }
if addr.is_unicast_link_local() { /* fe80::/10 */ }

// Pin utilities
let inner = pin.as_deref_mut();

// CString from str
let cstring: CString = "hello".parse()?;
```

## Rust 1.83 (November 2024)

### Language
```rust
// Mutable references in const
const fn modify(x: &mut i32) {
    *x += 1;
}

// Raw lifetimes
fn foo<'r#async>() {}  // Reserved keywords as lifetimes

// Const extern functions
const extern "C" fn c_compatible() -> i32 { 42 }
```

### APIs
```rust
// ControlFlow methods
let value = cf.break_value();
let mapped = cf.map_break(|b| b * 2);

// Debug formatting
f.debug_list()
    .entries(&items)
    .finish_non_exhaustive()  // Prints "[ ... ]"

// Entry insert
let entry = map.entry(key).insert_entry(value);

// Option default insert
let value = opt.get_or_insert_default();

// New Waker API
let waker = Waker::new(data, vtable);
```

## Rust 1.82 (October 2024)

### Language
```rust
// Raw references (safe alternative to addr_of!)
let ptr = &raw const value;
let ptr = &raw mut value;

// Unsafe extern blocks
unsafe extern "C" {
    fn foo();
    fn bar();
}

// Const floats
const PI_HALF: f64 = std::f64::consts::PI / 2.0;

// offset_of! nested fields
offset_of!(Struct, field.nested.deep)
```

### APIs
```rust
// Iterator sorted checks
if slice.is_sorted() { /* already sorted */ }
if slice.is_sorted_by_key(|x| x.priority) { /* custom */ }

// Option::is_none_or
if opt.is_none_or(|x| x > 10) { /* None or > 10 */ }

// repeat_n iterator
let items: Vec<_> = std::iter::repeat_n("hi", 3).collect();
// ["hi", "hi", "hi"]

// Uninit allocations
let boxed: Box<MaybeUninit<[u8; 1024]>> = Box::new_uninit();
```

## Rust 1.81 (September 2024)

### Language
```rust
// #[expect] lint attribute
#[expect(unused_variables)]  // Warns if lint NOT triggered
let x = 42;
```

### APIs
```rust
// core::error module (no_std errors)
use core::error::Error;

// Unchecked assertions
unsafe { std::hint::assert_unchecked(x > 0); }

// File existence check
if std::fs::exists("file.txt")? { /* exists */ }

// Atomic NOT
let prev = atomic_bool.fetch_not(Ordering::SeqCst);

// Duration difference
let diff = duration1.abs_diff(duration2);

// Improved sorting (driftsort/ipnsort)
// Automatically faster, no API change
slice.sort();  // Now uses driftsort
slice.sort_unstable();  // Now uses ipnsort
```

## Rust 1.80 (July 2024)

### APIs
```rust
// LazyCell and LazyLock (replaces lazy_static/once_cell)
use std::sync::LazyLock;
use std::cell::LazyCell;

static GLOBAL: LazyLock<Config> = LazyLock::new(|| {
    Config::load()
});

let local: LazyCell<Data> = LazyCell::new(|| compute());

// ASCII trimming
let trimmed = " hello ".trim_ascii();        // "hello"
let trimmed = " hello ".trim_ascii_start();  // "hello "

// Checked split
let (left, right) = slice.split_at_checked(mid)?;

// IP address bits
let bits = Ipv4Addr::new(192, 168, 1, 1).to_bits();
let addr = Ipv4Addr::from_bits(bits);

// Box iteration
let boxed: Box<[i32]> = vec![1, 2, 3].into_boxed_slice();
for item in boxed {  // Now works!
    println!("{item}");
}
```

## Quick Reference by Category

### Memory & Allocation
| Feature | Version | Example |
|---------|---------|---------|
| `LazyLock`/`LazyCell` | 1.80 | `LazyLock::new(\|\| init())` |
| `Box::new_zeroed` | 1.92 | `Box::<[u8; 1024]>::new_zeroed()` |
| `Box::new_uninit` | 1.82 | `Box::<T>::new_uninit()` |

### Async
| Feature | Version | Example |
|---------|---------|---------|
| Async closures | 1.85 | `async \|x\| x.await` |
| `Waker::noop` | 1.85 | `Waker::noop()` |

### Collections
| Feature | Version | Example |
|---------|---------|---------|
| `extract_if` (HashMap) | 1.88 | `map.extract_if(\|k,v\| pred)` |
| `extract_if` (BTreeMap) | 1.91 | `map.extract_if(\|k,v\| pred)` |
| `Vec::pop_if` | 1.86 | `vec.pop_if(\|x\| *x > 10)` |
| `entry.insert_entry` | 1.83 | `map.entry(k).insert_entry(v)` |

### Iterators
| Feature | Version | Example |
|---------|---------|---------|
| `is_sorted` | 1.82 | `slice.is_sorted()` |
| `repeat_n` | 1.82 | `iter::repeat_n(val, 3)` |

### Error Handling
| Feature | Version | Example |
|---------|---------|---------|
| `Result::flatten` | 1.89 | `Ok(Ok(42)).flatten()` |
| `QuotaExceeded` | 1.85 | `ErrorKind::QuotaExceeded` |
| `core::error` | 1.81 | `use core::error::Error` |

### Numerics
| Feature | Version | Example |
|---------|---------|---------|
| `midpoint` | 1.85 | `10u32.midpoint(20)` |
| `isqrt` | 1.84 | `16u32.isqrt()` |
| `div_ceil` (NonZero) | 1.92 | `nz.div_ceil(nz2)` |
| `strict_add` | 1.91 | `a.strict_add(b)` |

### File & IO
| Feature | Version | Example |
|---------|---------|---------|
| `fs::exists` | 1.81 | `fs::exists("path")?` |
| `File::lock` | 1.89 | `file.lock()?` |
| `io::pipe` | 1.88 | `io::pipe()?` |

### Synchronization
| Feature | Version | Example |
|---------|---------|---------|
| `RwLock::downgrade` | 1.92 | `write_guard.downgrade()` |
| `Once::wait` | 1.86 | `ONCE.wait()` |
| `OnceLock::wait` | 1.86 | `LOCK.wait()` |
