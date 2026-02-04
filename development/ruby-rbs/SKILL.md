---
name: ruby-rbs
description: Comprehensive skill for Ruby RBS type signatures. Use for writing inline type annotations in Ruby files, creating standalone .rbs signature files, scaffolding types, or setting up Steep type checking. Covers both inline syntax (rbs-inline) and standalone RBS file format.
---

# Ruby RBS Type Signatures

RBS is Ruby's official type signature language for describing the structure of Ruby programs - classes, modules, methods, and types. This skill covers both approaches to adding types:

1. **Inline RBS** (`# rbs_inline: enabled`) - Type annotations embedded in Ruby source files as comments
2. **Standalone RBS files** (`.rbs`) - Separate signature files that describe Ruby code

## Choosing an Approach

| Aspect | Inline RBS | Standalone .rbs Files |
|--------|-----------|----------------------|
| Co-location | Types live with code | Types in separate sig/ directory |
| Ruby files | Modified with comments | Unchanged |
| Tooling | Requires rbs-inline gem | Native RBS support |
| Use case | New code, gradual adoption | Libraries, gems, existing codebases |

**Use inline RBS when:** Starting fresh, want types near code, prefer gradual typing
**Use standalone .rbs when:** Publishing gems, typing third-party code, complete API documentation

## Subskills

For detailed guidance on each approach:

- **`subskills/inline/SKILL.md`** - Writing inline RBS annotations in Ruby files
- **`subskills/rbs-files/SKILL.md`** - Writing standalone .rbs signature files

## Core Type Syntax (Both Approaches)

### Basic Types

```
String              # String instance
Integer             # Integer instance
Float               # Float instance
bool                # true | false
boolish             # Any truthy/falsy value (for predicates)
nil                 # nil value
void                # Return value not used
untyped             # Skip type checking (gradual typing)
top                 # Supertype of all types
bot                 # Subtype of all types (never returns)
self                # Type of receiver
instance            # Instance of the class
class               # Singleton class
```

### Compound Types

```
String?                              # Optional: String | nil
String | Integer                     # Union type
_Reader & _Writer                    # Intersection type
Array[String]                        # Generic class
Hash[Symbol, Integer]                # Hash with typed keys/values
[String, Integer]                    # Tuple (fixed-size array)
{ name: String, age: Integer }       # Record (typed hash)
{ name: String, age?: Integer }      # Record with optional key
^(Integer) -> String                 # Proc/lambda type
```

### Literal Types

```
:ready                    # Symbol literal
"https"                   # String literal
123                       # Integer literal
true                      # Boolean literal
```

## Steep Integration

Steep is the primary type checker for RBS.

### Setup

```bash
# Add dependencies
bundle add rbs-inline --require=false  # Only for inline RBS
bundle add steep --group=development

# Initialize
bundle exec steep init
bundle exec rbs collection init
bundle exec rbs collection install
```

### Basic Steepfile

```ruby
D = Steep::Diagnostic

target :app do
  check "lib"
  check "app"

  signature "sig"              # Standalone RBS files
  signature "sig/generated"    # Generated from inline RBS

  library "pathname", "json"   # Standard libraries

  collection_config "rbs_collection.yaml"

  configure_code_diagnostics(D::Ruby.strict)
end
```

### Workflow Commands

```bash
# Generate RBS from inline annotations
bundle exec rbs-inline --output lib

# Type check
bundle exec steep check

# Watch mode
bundle exec steep watch

# Language server for editor integration
bundle exec steep langserver
```

## Critical Pattern: Nil Narrowing

Steep's flow analysis doesn't narrow instance variable types after nil checks. Even when you've checked `if @user`, Steep still considers `@user` potentially nil inside the block. Assign to a local variable to narrow the type:

```ruby
# WRONG - @user stays User? in the if body
if @user
  @user.name  # ERROR: @user is still User?
end

# RIGHT - Assignment narrows the type
if user = @user
  user.name   # OK: user is User
end
```

## Gradual Typing Strategy

1. **Start with public APIs** - Type method signatures users call
2. **Avoid `untyped` where possible** - Prefer concrete types, unions, interfaces, or generics. Reserve `untyped` only for truly dynamic code (metaprogramming, `eval`, external data with unknown shape). When you must use `untyped`, treat it as technical debt to revisit.
3. **Progress inward** - Add types to private methods over time
4. **Add to CI early** - Catch regressions immediately

## Testing Signatures

Verify RBS signatures are correct by writing Ruby test files that exercise the typed APIs:

```
my_gem/
├── sig/
│   └── my_gem.rbs          # Your RBS signatures
└── test/
    └── rbs/                # Type checking test directory
        ├── Steepfile       # Points to ../../sig
        └── lib/
            └── usage.rb    # Ruby code exercising the API
```

Write test files that use your gem's public API:

```ruby
# test/rbs/lib/usage.rb
require "my_gem"

# Test instantiation and methods
user = MyGem::User.new("Alice", "alice@example.com")
name = user.name          # Verifies return type
user.update(name: "Bob")  # Verifies argument types

# Test from documentation examples
client = MyGem::Client.new(api_key: "xxx")
response = client.get("/users")
```

Run `bundle exec steep check` in the test directory. Errors reveal signature problems:
- Wrong argument types
- Missing optional parameters
- Incorrect return types
- Generic type mismatches

See `references/validating-signatures.md` for full setup and patterns.

## References

- `references/type-syntax.md` - Complete type syntax reference
- `references/steep-integration.md` - Steep setup, configuration, and commands
- `references/validating-signatures.md` - Write test code to validate signatures with Steep
- `references/comparing-signatures.md` - Compare standalone and generated RBS files
- `references/rbs-test-instrumentation.md` - Runtime type checking with `rbs/test`
- `references/type-tracer.md` - Discover types from runtime execution
- `references/scaffolding.md` - Generate initial RBS from existing code
- `references/patterns.md` - Common patterns and best practices
- `references/troubleshooting.md` - Gotchas and troubleshooting guide

## External Resources

- [RBS Syntax Documentation](https://github.com/ruby/rbs/blob/master/docs/syntax.md)
- [RBS Inline Wiki](https://github.com/soutaro/rbs-inline/wiki/Syntax-guide)
- [Steep Type Checker](https://github.com/soutaro/steep)
- [gem_rbs_collection](https://github.com/ruby/gem_rbs_collection) - Community RBS for gems
