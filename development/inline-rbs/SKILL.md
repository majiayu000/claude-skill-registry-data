---
name: inline-rbs
description: Write RBS type annotations directly in Ruby source files using comment syntax. Use when adding types to Ruby code with rbs-inline.
---

# Inline RBS Annotations

Write type signatures directly in Ruby source files using special comments. Requires the `rbs-inline` gem.

## Quick Start

Every file needs the magic comment:

```ruby
# rbs_inline: enabled

class Person
  attr_reader :name #: String
  attr_reader :age #: Integer?

  #: (String, ?Integer?) -> void
  def initialize(name, age = nil)
    @name = name
    @age = age
  end
end
```

## Method Annotation Styles

### 1. Primitive `#:` (Most Concise)

```ruby
# Before method
#: (String) -> Integer
def count(text)
  text.length
end

# Inline return type
def name #: String
  @name
end

# Multiple overloads
#: () -> String?
#: (Integer) -> Array[String]
def fetch(n = nil)
  n ? @items.take(n) : @items.first
end
```

### 2. Keyword `# @rbs` (Structured)

```ruby
# @rbs (String, Integer) -> String
def format(text, width)
  text.ljust(width)
end

# Overloading with pipe
# @rbs (String) -> Integer
# | (Integer) -> Integer
def double(value)
  value * 2
end
```

### 3. Doc-Style Parameters (Self-Documenting)

```ruby
# @rbs text: String -- Input text
# @rbs width: Integer -- Max width
# @rbs strict: bool -- Strict mode
# @rbs return: Array[String]
def wrap(text, width: 80, strict: false)
  # Implementation
end
```

## Attributes and Variables

```ruby
attr_reader :name #: String
attr_accessor :count #: Integer

# @rbs @items: Array[String]           # Instance variable
# @rbs self.@cache: Hash[Symbol, T]    # Class instance variable

VERSION = "1.0" #: String              # Constant
```

## Block Annotations

```ruby
# Required block
# @rbs () { (String) -> void } -> void
def each(&block)
  @items.each(&block)
end

# Optional block (? before type)
# @rbs () { (Integer) -> void }? -> Integer?
def process(&block)
  yield(42) if block
end

# Using boolish for filters
#: () { (String) -> boolish } -> Array[String]
def select(&block)
  @items.select(&block)
end
```

## Generic Classes

```ruby
# @rbs generic T
class Container
  # @rbs (T) -> void
  def initialize(value)
    @value = value
  end

  #: () -> T
  def get
    @value
  end
end
```

## Generic Module Includes

Specify type parameters for generic modules using `#[Type]`:

```ruby
include Enumerable #[String]
include Comparable #[self]
include MyGeneric #[Integer | nil]
```

## Raw RBS for DSLs (`# @rbs!`)

Use for DSL-generated methods or interface declarations:

```ruby
# For DSL-generated methods
# @rbs!
#   attr_accessor name: String
#   attr_accessor email: String?

# For interface methods (expected from mixins)
# @rbs!
#   def current_user: () -> User?
#   def authorized?: (Symbol) -> bool
```

## Special Annotations

```ruby
# Skip RBS generation
# @rbs skip
def internal_method; end

# Override inherited method
# @rbs override
def process(data)
  super
end
```

## Generate RBS Files

```bash
# Generate to stdout
bundle exec rbs-inline lib

# Save to sig/generated
bundle exec rbs-inline --output lib

# Watch for changes
bundle exec rbs-inline --watch lib
```

## Common Pitfalls

1. **Forgetting magic comment** - No RBS without `# rbs_inline: enabled`
2. **Instance variable narrowing** - Always assign to local first for nil checks
3. **Optional block syntax** - `?` goes before type: `{ (T) -> U }?`
4. **Return type mismatch** - Ensure signatures match nil possibilities
