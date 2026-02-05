---
name: coding-style
description: Applies project-specific coding conventions and patterns. Use when writing, reviewing, or modifying code to maintain consistency with the codebase style.
---

# Coding Style Guide

This skill ensures all code follows the established patterns and conventions of this codebase. Detect the project type from file extensions and configuration files, then apply the appropriate style.

## Project Detection

1. **Rust**: Look for `Cargo.toml`
2. **Python**: Look for `pyproject.toml` or `setup.py`
3. **TypeScript/JavaScript**: Look for `package.json` with TypeScript or Svelte dependencies

## General Principles (All Languages)

### Avoid Over-Engineering
- Only make changes directly requested or clearly necessary
- Don't add features, refactor, or make "improvements" beyond what was asked
- Don't add docstrings/comments to code you didn't change
- Three similar lines of code is better than a premature abstraction
- Don't design for hypothetical future requirements

### Code Organization
- One module/file = one responsibility
- Keep related code together
- Prefer flat structures over deep nesting
- Use descriptive names over comments

### Error Messages
- Include context: what failed, expected vs actual, file positions
- Make errors actionable: tell the user what to do

---

## Language-Specific Guides

Detailed patterns for each language are in the reference files:
- [Rust Style Guide](rust-style.md)
- [Python Style Guide](python-style.md)
- [TypeScript Style Guide](typescript-style.md)

## Project-Specific Notes

For SC Interdiction project context, limitations, and planned improvements:
- [Project Notes & Scratchpad](project-notes.md)

---

## Quick Reference

### Rust Projects

```rust
// Error handling: thiserror with rich context
#[derive(Debug, Error)]
pub enum ParseError {
    #[error("Invalid header at position {1:#x}: {0}")]
    InvalidHeader(Box<str>, u64),

    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),
}

// Binary parsing: zerocopy for zero-copy
use zerocopy::{FromBytes, U32, LE};

#[derive(FromBytes)]
#[repr(C, packed)]
pub struct Header<O: ByteOrder = LE> {
    pub magic: [u8; 4],
    pub version: U32<O>,
}

// LazyLock for statics
static CONFIG: LazyLock<Config> = LazyLock::new(|| Config::load());

// Release profile
// [profile.release]
// lto = true, panic = "abort", opt-level = "z"
```

### Python Projects

```python
# Type hints: use union syntax, not Optional
def process(data: str | None = None) -> dict[str, Any]:
    """Process the data.

    Args:
        data: Input data to process, or None for default.

    Returns:
        Processed result dictionary.
    """
    pass

# Error handling: return None for recoverable, raise for unrecoverable
def parse_file(path: str) -> ParseResult | None:
    try:
        return _parse(path)
    except ParseError:
        return None

# Testing: pytest with markers
@pytest.mark.unit
def test_parse_valid():
    result = parse("valid")
    assert result is not None

@pytest.mark.integration
def test_full_workflow():
    # Uses real files
    pass
```

### TypeScript Projects

```typescript
// Error handling pattern
export const fetchData = async (token: string): Promise<Data | null> => {
    let error = null;

    const res = await fetch(url, { headers: { Authorization: `Bearer ${token}` } })
        .then(async (res) => {
            if (!res.ok) throw await res.json();
            return res.json();
        })
        .catch((err) => {
            console.log(err);
            error = err;
            return null;
        });

    if (error) throw error;
    return res;
};

// Types: explicit interfaces
interface Config {
    readonly endpoint: string;
    timeout: number;
}
```

---

## Checklist Before Committing

1. **Naming**: Follows project conventions (snake_case for Rust/Python functions, PascalCase for types)
2. **Error Handling**: Uses project patterns (thiserror/eyre for Rust, None returns for Python)
3. **Tests**: Added for new functionality, uses project test structure
4. **No Over-Engineering**: Only changed what was needed
5. **Lints Pass**: `cargo clippy`, `ruff check`, or `eslint`
