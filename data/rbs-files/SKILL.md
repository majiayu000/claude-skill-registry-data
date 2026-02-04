---
name: rbs-files
description: Write standalone .rbs signature files to describe Ruby code. Use when creating type definitions for gems, libraries, or existing codebases without modifying Ruby source.
---

# Standalone RBS Files

Write type signatures in separate `.rbs` files in a `sig/` directory. Ruby source files remain unchanged.

## Quick Start

```rbs
# sig/person.rbs
class Person
  attr_reader name: String
  attr_reader age: Integer?

  def initialize: (String name, ?Integer? age) -> void
  def greet: () -> String
end
```

## File Structure

```
project/
├── lib/
│   └── person.rb          # Ruby implementation
├── sig/
│   ├── person.rbs         # Type signatures
│   ├── _private/          # Hidden from library users
│   │   └── internal.rbs
│   └── manifest.yaml      # Stdlib dependencies
└── Steepfile
```

## Class and Module Declarations

```rbs
# Basic class
class User
end

# With superclass
class Admin < User
end

# With type parameters
class Container[T]
end

# Module
module Logging
end

# Module with self-type constraint
module Enumerable[Elem] : _Each[Elem]
end
```

## Method Definitions

```rbs
class Calculator
  # Instance method
  def add: (Integer, Integer) -> Integer

  # Singleton (class) method
  def self.create: () -> Calculator

  # Module function (both singleton and private instance)
  def self?.sqrt: (Numeric) -> Float

  # Visibility
  private def internal: () -> void
end
```

## Method Type Syntax

```rbs
# Required positional
def foo: (String, Integer) -> void

# Optional positional (? prefix)
def foo: (String, ?Integer) -> void

# Rest positional
def foo: (*String) -> void

# Required keyword
def foo: (name: String) -> void

# Optional keyword
def foo: (?name: String) -> void

# Keyword rest
def foo: (**String) -> void

# Block (required)
def foo: () { (String) -> Integer } -> void

# Block (optional, ? before brace)
def foo: () ?{ (String) -> Integer } -> void

# Complex signature
def foo: (
  String,                    # Required positional
  ?Integer,                  # Optional positional
  *Symbol,                   # Rest positional
  name: String,              # Required keyword
  ?age: Integer,             # Optional keyword
  **untyped                  # Keyword rest
) { (String) -> void } -> Array[String]
```

## Method Overloading

```rbs
class Array[Elem]
  # Multiple signatures with |
  def *: (String) -> String
       | (Integer) -> Array[Elem]

  # Extending existing method with ...
  def fetch: (Integer) -> Elem
           | ...
end
```

## Attributes

```rbs
class User
  # Reader (generates getter + @name ivar)
  attr_reader name: String

  # Writer (generates setter + @email ivar)
  attr_writer email: String

  # Accessor (generates both)
  attr_accessor age: Integer

  # Custom ivar name
  attr_reader display_name (@raw_name): String

  # No ivar (computed property)
  attr_reader full_name (): String

  # Singleton attribute
  attr_reader self.instance: User
end
```

## Instance and Class Variables

```rbs
class Counter
  @count: Integer                    # Instance variable
  self.@instances: Array[Counter]    # Class instance variable
  @@total: Integer                   # Class variable
end
```

## Constants

```rbs
class Config
  VERSION: String
  MAX_SIZE: Integer
  VALID_STATES: Array[Symbol]
end

# Global variable
$LOAD_PATH: Array[String]
```

## Interfaces

Define duck types that classes can implement:

```rbs
interface _Readable
  def read: (?Integer) -> String?
  def eof?: () -> bool
end

interface _Writable
  def write: (String) -> Integer
end

class MyIO
  include _Readable
  include _Writable
end
```

## Type Aliases

```rbs
# Simple alias
type json_value = String | Integer | Float | bool | nil | Array[json_value] | Hash[String, json_value]

# Generic alias
type result[T] = [true, T] | [false, String]

# Scoped to class
class MyApp
  type callback = ^(String) -> void
end
```

## Generics

```rbs
# Basic generic class
class Box[T]
  def initialize: (T) -> void
  def get: () -> T
end

# Variance annotations
class ReadOnly[out T]        # Covariant
  def get: () -> T
end

class WriteOnly[in T]        # Contravariant
  def set: (T) -> void
end

# Unchecked variance (for mutable collections)
class Array[unchecked out T]
end

# Upper bound
class Sorter[T < Comparable]
  def sort: (Array[T]) -> Array[T]
end

# Default type
class Cache[T = String]
end

# Method-level generics
class Util
  def self.identity: [T] (T) -> T
  def self.map: [T, U] (Array[T]) { (T) -> U } -> Array[U]
end
```

## Mixins

```rbs
class User
  include Comparable
  include Enumerable[String]
  extend ClassMethods
  prepend Instrumentation
end
```

## Use Directive

Import types to avoid fully-qualified names:

```rbs
use RBS::TypeName
use RBS::AST::*

class MyParser
  def parse: (TypeName) -> untyped
end
```

## manifest.yaml

Declare stdlib dependencies for gems:

```yaml
# sig/manifest.yaml
dependencies:
  - name: json
  - name: pathname
  - name: set
```

## Validate Signatures

```bash
# Check RBS syntax and consistency
bundle exec rbs validate

# Test signatures against runtime
RBS_TEST_TARGET='MyApp::*' bundle exec ruby -r rbs/test/setup test/my_test.rb
```
