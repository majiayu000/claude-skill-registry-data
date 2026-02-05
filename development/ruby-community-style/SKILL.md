---
name: ruby-community-style
description: Use this skill when writing Ruby code following the RuboCop Community Ruby Style Guide. Provides comprehensive guidance on idiomatic Ruby patterns, method design, class structure, collections, strings, exceptions, and testing. Covers Sandi Metz rules, duck typing, metaprogramming guidelines, and RuboCop enforcement. Appropriate for any task involving .rb files, Ruby code reviews, refactoring, Rails development, or implementing Ruby best practices.
---

# Ruby Community Style Guide

## Overview

This skill provides comprehensive guidance for writing idiomatic Ruby code that strictly follows the RuboCop Community Ruby Style Guide - the most widely adopted Ruby style guide in the community (16.5k GitHub stars). It emphasizes readability, consistency, proper use of Ruby idioms, Test-Driven Development, and Ruby's philosophy of developer happiness.

## When to Use This Skill

Use this skill for any Ruby-related programming task:
- Writing new Ruby code or implementing new features
- Reviewing existing Ruby code for best practices and idioms
- Refactoring code to follow Ruby Community Style Guide
- Debugging Ruby applications and fixing issues
- Working with Rails, Sinatra, or other Ruby frameworks
- Designing Ruby APIs and gem structures
- Implementing tests with RSpec or Minitest

## Core Ruby Philosophy

### Mandatory Principles

**1. Matz's Philosophy: Optimize for Developer Happiness**
- Ruby is designed to make programmers happy
- Code should be readable and expressive
- Prefer clarity over cleverness
- Follow the Principle of Least Surprise

**2. Test-Driven Development (TDD)**
- Write tests first using Red-Green-Refactor cycle
- Use RSpec or Minitest for comprehensive test coverage
- Tests must be in place before implementation code

**3. Sandi Metz Rules (Structural Limits)**
- Classes: ≤100 lines per class
- Methods: ≤5 lines per method
- Parameters: ≤4 parameters per method (use keyword arguments for more)
- Controllers: ≤1 instance variable passed to views
- Break limits only with explicit documentation and approval

**4. Duck Typing Over Type Checking**
- Favor duck typing; avoid explicit type checking
- Program to behaviors, not types
- Use `respond_to?` only when truly necessary

## Workflow

### For Writing New Ruby Code

1. **Write the test first** (TDD mandatory)
   - Define expected behavior in RSpec or Minitest
   - Run test to see it fail (Red)

2. **Implement minimal code to pass the test** (Green)
   - Write just enough code to make the test pass
   - Follow Ruby Community Style Guide conventions

3. **Refactor while keeping tests green**
   - Improve code quality, readability, and performance
   - Ensure all tests still pass

4. **Verify quality standards**
   - Run `rubocop` to check style compliance
   - Run `bundle exec rspec` or `bundle exec rake test`
   - Check Sandi Metz rules (≤100 lines/class, ≤5 lines/method)

### For Code Review

1. **Check TDD compliance**
   - Verify tests exist and are comprehensive
   - Ensure proper test structure (describe/context/it)

2. **Review Ruby Community Style Guide compliance**
   - Run RuboCop and address all offenses
   - Verify naming conventions (snake_case, CamelCase)
   - Confirm proper use of Ruby idioms

3. **Validate structural limits**
   - Classes ≤100 lines
   - Methods ≤5 lines
   - ≤4 parameters per method
   - Single Responsibility Principle adherence

4. **Check for Ruby-specific issues**
   - Prefer && and || operators over `and`/`or` keywords in conditions
   - Use guard clauses instead of nested conditionals
   - Verify proper exception handling patterns
   - Check for proper use of blocks and iterators

### For Refactoring

1. **Ensure tests exist first**
   - If no tests, write them before refactoring
   - Tests provide safety net during refactoring

2. **Identify anti-patterns**
   - Methods >5 lines
   - Classes >100 lines
   - God classes with too many responsibilities
   - Excessive metaprogramming
   - Type checking (`is_a?`, `kind_of?`) instead of duck typing

3. **Refactor incrementally**
   - Extract methods for long code blocks
   - Extract classes for multiple responsibilities
   - Keep tests passing after each change

## Key Style Rules Summary

### Naming Conventions
- `snake_case` for methods, variables, symbols, files
- `CamelCase` for classes and modules
- `SCREAMING_SNAKE_CASE` for constants
- End predicates with ? suffix (e.g., `empty?`, `valid?`)
- End dangerous/mutating methods with bang suffix (!) when a safe version exists
- Avoid get_/set_/is_ prefixes

### Formatting
- 2 spaces for indentation (no tabs)
- UTF-8 encoding
- Maximum 80-120 characters per line (80 preferred)
- Unix-style line endings (LF)
- One expression per line

### Method Design
- Omit `return` when unnecessary (implicit returns)
- Omit `self` except for setters
- Use guard clauses for early returns
- Use keyword arguments for optional parameters
- Avoid more than 4 parameters (use keyword args or objects)

### Collections & Iteration
- Prefer `map`/`select`/`reduce` over `each` with mutation
- Use `%w[]` for word arrays, `%i[]` for symbol arrays
- Use `Hash#fetch` with defaults instead of || operator
- Prefer `first`/`last` over `[0]`/`[-1]`

### Strings
- Use string interpolation `"Hello, #{name}"` over concatenation
- Use double quotes consistently (Shopify) or single when no interpolation (Community)
- Use heredocs (`<<~`) for multi-line strings
- Prefer `String#chars` over `split('')`

### Exceptions
- Use `raise` over `fail`
- Never rescue `Exception` class (use `StandardError`)
- Provide meaningful error messages
- Use implicit begin blocks in methods

## Reference Materials

For detailed code patterns, examples, and guidelines, consult the reference files:

- `references/ruby-patterns.md` - Comprehensive Ruby style patterns and anti-patterns
  - Source layout, naming conventions, syntax preferences
  - Method definitions, control flow, operators
  - Comments and documentation guidelines
- `references/classes-modules.md` - OOP patterns in Ruby
  - Class structure and organization
  - Module design and mixins
  - Inheritance vs composition
  - Access modifiers and visibility
- `references/testing-patterns.md` - Ruby testing best practices
  - RSpec patterns and conventions
  - Minitest patterns
  - Test organization and structure
  - Mocking and stubbing guidelines

Use grep to search these files for specific patterns when needed (e.g., search for "guard clause", "keyword arguments", or "let vs before").

## Template Assets

Pre-built templates are available in `assets/templates/` for common Ruby patterns:

- `assets/templates/class_template.rb` - Standard class structure with Sandi Metz compliance
- `assets/templates/service_object.rb` - Service object pattern template
- `assets/templates/rspec_spec.rb` - RSpec test file template
- `assets/templates/minitest_test.rb` - Minitest test file template

Copy and customize these templates as starting points for new code.

## Quality Assurance Checklist

Before delivering Ruby code, verify:

**Critical Ruby Style Rules:**
- [ ] 2-space indentation (no tabs)
- [ ] snake_case for methods/variables, CamelCase for classes
- [ ] Predicates end with ? suffix, dangerous methods with ! suffix
- [ ] No explicit `return` unless required for early exit
- [ ] No explicit `self` unless required (setters, disambiguation)
- [ ] Use && and || for boolean logic (not `and`/`or`)
- [ ] Guard clauses instead of nested conditionals
- [ ] Iterators (`map`, `select`, `reduce`) over `for` loops

**Sandi Metz Rules:**
- [ ] Classes ≤100 lines
- [ ] Methods ≤5 lines
- [ ] ≤4 parameters per method (use keyword arguments for more)
- [ ] ≤1 instance variable per controller action (Rails)

**Code Quality:**
- [ ] Tests written first (TDD followed)
- [ ] RuboCop passes with no offenses
- [ ] Tests pass with `bundle exec rspec` or `rake test`
- [ ] Proper exception handling (no bare `rescue`)
- [ ] No commented-out code

**Ruby Idioms:**
- [ ] Duck typing preferred over type checking
- [ ] String interpolation over concatenation
- [ ] Use `Hash#fetch` with defaults over || operator
- [ ] Use `%w[]` and `%i[]` for word/symbol arrays
- [ ] Blocks use `{}` for single-line, `do...end` for multi-line

**Testing:**
- [ ] One assertion per test (when possible)
- [ ] Descriptive test names (`it "returns nil when user not found"`)
- [ ] Proper use of let/let! vs before in RSpec
- [ ] Test edge cases and error conditions

## Communication Guidelines

When providing Ruby coding assistance:
- Reference RuboCop Community Style Guide for rationale
- Provide working, tested code examples
- Explain Ruby idioms and their benefits
- Suggest RuboCop cops for common violations
- Point out Ruby-specific pitfalls and solutions
- Prioritize Ruby's philosophy of expressiveness and readability

## Key Differences from General Coding Principles

This skill overrides some general coding principles with Ruby-specific rules:
- **Method length**: 5 lines (vs. general 20 lines) - Sandi Metz rules are stricter
- **Class length**: 100 lines (vs. general 500 lines) - Ruby favors small, focused classes
- **Implicit returns**: No explicit `return` statement - unlike most languages
- **Testing approach**: TDD is mandatory with RSpec/Minitest patterns
- **Parameter limits**: Strict ≤4 parameter limit with keyword arguments as solution