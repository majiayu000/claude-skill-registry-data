---
name: nojson
description: A flexible Rust JSON library with no dependencies and no macros. Use when working with JSON in Rust without serde, implementing custom JSON parsing/generation, handling JSON with custom validation, or working with dynamic JSON structures that don't map one-to-one to Rust types. Supports JSON parsing, generation, custom validation, pretty-printing, and JSONC (JSON with comments).
---

# nojson - Flexible Rust JSON Library

A flexible Rust JSON library with no dependencies and no macros that provides a toolbox approach for JSON handling.

## Core Concepts

The library operates on three levels:

1. **High-level typed API** - `nojson::Json<T>` wrapper for parsing/generation
2. **Raw JSON access** - `nojson::RawJson` and `nojson::RawJsonValue` for flexible traversal
3. **Custom formatting** - `nojson::json()` function for in-place generation with formatting control

## Quick Reference

### Parse JSON to Rust Types

```rust
// Parse with type inference
let value: nojson::Json<[Option<u32>; 3]> = "[1, null, 2]".parse()?;
assert_eq!(value.0, [Some(1), None, Some(2)]);

// Parse JSON with RawJson for flexible access
let json = nojson::RawJson::parse(r#"{"name": "Alice", "age": 30}"#)?;
let name: String = json.value().to_member("name")?.required()?.try_into()?;
```

### Generate JSON from Rust Types

```rust
// Simple generation
let value = [Some(1), None, Some(2)];
assert_eq!(nojson::Json(value).to_string(), "[1,null,2]");

// With pretty-printing
let pretty = nojson::json(|f| {
    f.set_indent_size(2);
    f.set_spacing(true);
    f.value([1, 2, 3])
});
```

### Implement Custom Types

Implement two traits for full JSON support:

```rust
struct Person {
    name: String,
    age: u32,
}

// For JSON generation
impl nojson::DisplayJson for Person {
    fn fmt(&self, f: &mut nojson::JsonFormatter<'_, '_>) -> std::fmt::Result {
        f.object(|f| {
            f.member("name", &self.name)?;
            f.member("age", self.age)
        })
    }
}

// For JSON parsing
impl<'text, 'raw> TryFrom<nojson::RawJsonValue<'text, 'raw>> for Person {
    type Error = nojson::JsonParseError;

    fn try_from(value: nojson::RawJsonValue<'text, 'raw>) -> Result<Self, Self::Error> {
        let name = value.to_member("name")?.required()?;
        let age = value.to_member("age")?.required()?;
        Ok(Person {
            name: name.try_into()?,
            age: age.try_into()?,
        })
    }
}
```

### Custom Validation

```rust
fn parse_positive_number(text: &str) -> Result<u32, nojson::JsonParseError> {
    let json = nojson::RawJson::parse(text)?;
    let raw_value = json.value();
    
    let num: u32 = raw_value.as_number_str()?
        .parse()
        .map_err(|e| raw_value.invalid(e))?;
    
    if num == 0 {
        return Err(raw_value.invalid("Expected a positive number, got 0"));
    }
    
    Ok(num)
}
```

## Common Patterns

### Accessing Object Members

```rust
// Required member
let name: String = json.value().to_member("name")?.required()?.try_into()?;

// Optional member
let email: Option<String> = json.value().to_member("email")?.try_into()?;

// Nested access
let city: String = json.value()
    .to_member("user")?
    .required()?
    .to_member("address")?
    .required()?
    .to_member("city")?
    .required()?
    .try_into()?;
```

### Working with Arrays

```rust
// Fixed-size array
let numbers: [u32; 3] = json.value().try_into()?;

// Dynamic Vec
let numbers: Vec<u32> = json.value().try_into()?;

// Iterate elements
for element in json.value().to_array()? {
    let num: u32 = element.try_into()?;
    println!("{}", num);
}
```

### Formatting Options

```rust
// Compact (default)
let compact = nojson::json(|f| f.value([1, 2, 3]));

// With spacing
let spaced = nojson::json(|f| {
    f.set_spacing(true);
    f.value([1, 2, 3])
});

// Pretty-printed with indentation
let pretty = nojson::json(|f| {
    f.set_indent_size(2);
    f.set_spacing(true);
    f.value([1, 2, 3])
});

// Nested with mixed formatting
let mixed = nojson::json(|f| {
    f.set_indent_size(2);
    f.set_spacing(true);
    f.array(|f| {
        f.element(&vec![1])?;
        f.element(nojson::json(|f| {
            f.set_indent_size(0);
            f.value(vec![2, 3])
        }))
    })
});
```

### Building JSON In-Place

```rust
// Array builder
let arr = nojson::array(|f| {
    f.element(1)?;
    f.element(2)?;
    f.element(3)
});

// Object builder
let obj = nojson::object(|f| {
    f.member("name", "Alice")?;
    f.member("age", 30)?;
    f.member("active", true)
});

// Complex structures
let complex = nojson::json(|f| {
    f.object(|f| {
        f.member("users", nojson::array(|f| {
            f.element(nojson::object(|f| {
                f.member("id", 1)?;
                f.member("name", "Alice")
            }))?;
            f.element(nojson::object(|f| {
                f.member("id", 2)?;
                f.member("name", "Bob")
            }))
        }))?;
        f.member("count", 2)
    })
});
```

### Error Handling

```rust
let text = r#"{"invalid": 123e++}"#;
match nojson::RawJson::parse(text) {
    Ok(json) => { /* process */ },
    Err(error) => {
        eprintln!("Error: {}", error);
        
        // Get position info
        if let Some((line, column)) = error.get_line_and_column_numbers(text) {
            eprintln!("At line {}, column {}", line, column);
        }
        
        // Get line content
        if let Some(line_text) = error.get_line(text) {
            eprintln!("Line: {}", line_text);
        }
        
        // Get specific value at error position
        if let Ok(json) = nojson::RawJson::parse(&text[..error.position()]) {
            if let Some(value) = json.get_value_by_position(error.position()) {
                eprintln!("Problematic value: {}", value.as_raw_str());
            }
        }
    }
}
```

### JSONC Support (JSON with Comments)

```rust
let text = r#"{
    "name": "John", // This is a line comment
    "age": 30,
    /* This is a
       block comment */
    "city": "New York", // Trailing comma is allowed
}"#;

let (json, comment_ranges) = nojson::RawJson::parse_jsonc(text)?;

// Access data normally
let name: String = json.value().to_member("name")?.required()?.try_into()?;

// Access comment text if needed
for range in comment_ranges {
    let comment = &text[range];
    println!("Found comment: {}", comment);
}
```

## Type Conversions

### Built-in Type Support

The library provides `TryFrom<RawJsonValue>` implementations for:

**Primitives**: `bool`, `char`, `i8`, `i16`, `i32`, `i64`, `i128`, `isize`, `u8`, `u16`, `u32`, `u64`, `u128`, `usize`, `f32`, `f64`

**Non-zero types**: `NonZeroI8`, `NonZeroU8`, etc.

**Strings**: `String`, `Cow<str>`, `char`

**Collections**: `Vec<T>`, `[T; N]`, `VecDeque<T>`, `BTreeSet<T>`, `HashSet<T>`, `BTreeMap<K, V>`, `HashMap<K, V>`

**Network types**: `IpAddr`, `Ipv4Addr`, `Ipv6Addr`, `SocketAddr`, `SocketAddrV4`, `SocketAddrV6`

**Others**: `PathBuf`, `Option<T>`, `Rc<T>`, `Arc<T>`, `()`

### DisplayJson Implementations

Corresponding `DisplayJson` implementations exist for generating JSON from these types.

## Advanced Features

### Value Navigation

```rust
// Get parent value
let value = json.get_value_by_position(42)?;
if let Some(parent) = value.parent() {
    println!("Parent: {}", parent.as_raw_str());
}

// Get root value from nested position
let root = value.root();

// Extract value as standalone JSON
let extracted = value.extract(); // Returns RawJson<'text>
let owned = extracted.into_owned(); // Returns RawJsonOwned
```

### Value Inspection

```rust
let value = json.value();

// Check type
assert!(value.kind().is_number());
assert!(value.kind().is_string());
assert!(value.kind().is_array());
assert!(value.kind().is_object());

// Get position in original text
let pos = value.position();

// Get raw text
let text = value.as_raw_str();

// Type-specific accessors
let bool_str = value.as_boolean_str()?;
let int_str = value.as_integer_str()?;
let float_str = value.as_float_str()?;
let num_str = value.as_number_str()?;
let unquoted = value.to_unquoted_string_str()?;
```

### Functional Patterns

```rust
// Map over values
let result = value.map(|v| {
    let s: String = v.try_into()?;
    Ok(s.to_uppercase())
})?;

// Member mapping
let age: Option<i32> = json.value()
    .to_member("age")?
    .map(|v| v.try_into())?;
```

## Important Notes

### Fully Qualified Names Required

When using this crate in generated code, always use fully qualified names without `use` statements:

```rust
// DO THIS
fn parse_json(text: &str) -> Result<nojson::RawJson, nojson::JsonParseError> {
    nojson::RawJson::parse(text)
}

impl nojson::DisplayJson for MyType {
    fn fmt(&self, f: &mut nojson::JsonFormatter<'_, '_>) -> std::fmt::Result {
        // implementation
    }
}

// NOT THIS
use nojson::RawJson;  // Don't use 'use' statements
```

### Lifetime Parameters

When implementing `TryFrom` for custom types, use the exact lifetime signature:

```rust
impl<'text, 'raw> TryFrom<nojson::RawJsonValue<'text, 'raw>> for MyType {
    type Error = nojson::JsonParseError;
    // implementation
}
```

### Error Context

Always use `.invalid()` method to create errors with proper context:

```rust
// DO THIS
let num: u32 = value.as_number_str()?
    .parse()
    .map_err(|e| value.invalid(e))?;

// NOT THIS
let num: u32 = value.as_number_str()?
    .parse()
    .map_err(|e| nojson::JsonParseError::invalid_value(value, e))?;
```

## Reference Documentation

For comprehensive API details, implementation examples, and advanced patterns, see:

- [API_REFERENCE.md](references/API_REFERENCE.md) - Complete type and method documentation
- [EXAMPLES.md](references/EXAMPLES.md) - Extensive code examples and patterns
