---
name: simplifying-ruby-code
description: Identify over-engineering in Ruby - prefer simple data structures (Hash, Struct, Data) and pure functions over unnecessary classes
---

# Simplifying Ruby Code

## Core Principle

Prefer simple data structures (Hash, Array, Struct, Data) and pure functions over unnecessary classes and abstractions.

**MANDATORY:** Identify whether code is a decision (pure logic) or effect (I/O). Keep them separate. See `writing-code` skill.

## When to Use

- Command objects with single `call` method and no state
- Value objects that just wrap data without behavior
- Service classes that could be module functions
- Custom classes for simple data (coordinates, ranges, tuples)
- Deep inheritance where composition would work
- Missing Ruby protocols (`to_h`, `to_a`, `each`)
- Tests require extensive mocking (indicates mixed concerns)

## Over-Engineering Patterns

### Command Objects → Module Functions

```ruby
# ❌ Over-engineered
class UserCreator
  def initialize(params); @params = params; end
  def call; User.create(@params); end
end

# ✅ Simple
User.create(params)  # or module function if logic needed
```

**Keep command object when:** Has state, multi-step algorithm, needs queuing.

### Value Objects → Struct/Data/Hash

```ruby
# ❌ Manual value object
class Point
  attr_reader :x, :y
  def initialize(x, y); @x, @y = x, y; end
  def ==(other); x == other.x && y == other.y; end
end

# ✅ Simple
Point = Data.define(:x, :y)  # Ruby 3.2+, immutable
Point = Struct.new(:x, :y, keyword_init: true)  # mutable
point = {x: 10, y: 20}  # simplest
```

### Utility Classes → Modules

```ruby
# ❌ Class with only class methods
class DateFormatter
  def self.format_for_display(date); date.strftime("%B %d, %Y"); end
end

# ✅ Module
module DateFormatter
  module_function
  def format_for_display(date); date.strftime("%B %d, %Y"); end
end
```

### Deep Inheritance → Composition

```ruby
# ❌ Deep hierarchy
class Animal; end
class Mammal < Animal; end
class Dog < Mammal; end

# ✅ Composition
module WarmBlooded
  def warm_blooded?; true; end
end

class Dog
  include WarmBlooded
end
```

## Data Structure Selection

| Use | When |
|-----|------|
| Hash | Temporary data, varying keys, JSON interface |
| Struct | Fixed attributes, need methods, mutable OK |
| Data | Fixed attributes, immutable (Ruby 3.2+) |
| Custom Class | Complex validation, rich behavior, domain concepts |

## Ruby Protocols

Implement for interoperability with standard library:

```ruby
class Collection
  include Enumerable

  def each(&block); @items.each(&block); end  # Enables map, select, etc.
  def to_a; @items.dup; end
  def to_h; @items.to_h; end
  def to_json(*args); @items.to_json(*args); end
end
```

Key protocols: `to_h`, `to_a`, `to_json`, `to_s`, `each`, `<=>`, `hash`/`eql?`

## Refactoring Steps

1. **Identify decisions vs effects** - Mark pure logic vs I/O
2. **Extract pure functions** - Create module functions with data parameters
3. **Test pure functions** - No mocks needed
4. **Simplify data structures** - Replace classes with Struct/Data/Hash
5. **Remove unnecessary layers** - Inline wrappers that add no value

## Detection Checklist

- [ ] Command object with single method, no state → Module function
- [ ] Value object with no behavior → Struct/Data/Hash
- [ ] Class with only class methods → Module
- [ ] Service wrapping single operation → Direct call
- [ ] Deep inheritance for behavior sharing → Modules/composition
- [ ] Missing `to_h`, `to_a`, `to_json` → Add protocols
- [ ] Tests need heavy mocking → Separate decisions from effects

## Key Takeaways

1. **Hash/Struct/Data over custom classes** for simple data
2. **Module functions over command objects** unless state needed
3. **Composition over inheritance** for behavior sharing
4. **Implement Ruby protocols** for interoperability
5. **OOP for domain models, functional for calculations** - Use both appropriately
