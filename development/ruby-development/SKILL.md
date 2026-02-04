---
name: Ruby Development
description: Senior Ruby developer using functional programming techniques. Use when writing Ruby code, implementing Ruby features, or working with Ruby projects. Follows TDD methodology via development skill. Used as a part of the XP skill.
---

# Ruby Development

## Principles

- Functional programming techniques
- Single return per function (no early returns)
- Prefer immutable data structures (freeze objects)
- Use `map`, `reduce`, `select`, `reject` over imperative loops
- Favour composition over inheritance

## Testing

Use project's existing test framework. Test structure follows AAA pattern:

```ruby
describe 'ClassName' do
  describe '#method_name' do
    it 'describes expected behaviour' do
      # Arrange
      input = build_test_data

      # Act
      result = subject.method_name(input)

      # Assert
      expect(result).to eq(expected)
    end
  end
end
```

Run tests:

```bash
bundle exec rspec           # RSpec
bundle exec rake test       # Minitest
```

## Linting

```bash
bundle exec rubocop         # Check style
bundle exec rubocop -a      # Auto-fix safe issues
bundle exec rubocop -A      # Auto-fix all (review changes)
```

## Functional Patterns

**Transform with map:**

```ruby
# ❌ Imperative
results = []
items.each { |i| results << transform(i) }

# ✅ Functional
results = items.map { |i| transform(i) }
```

**Filter with select/reject:**

```ruby
valid_items = items.select(&:valid?)
invalid_items = items.reject(&:valid?)
```

**Reduce for accumulation:**

```ruby
total = items.reduce(0) { |sum, item| sum + item.value }
```

**Chain operations:**

```ruby
items
  .select(&:active?)
  .map(&:transform)
  .reduce(initial) { |acc, x| combine(acc, x) }
```

**Immutability:**

```ruby
CONSTANTS = ['a', 'b', 'c'].freeze
hash = { key: 'value' }.freeze
```
