---
name: kura-perl
description: Store and export type constraints for Type::Tiny, Moose, Data::Checks, and more
version: 1.0.0
author: kfly8
tags: [perl, cpan, type-constraints, validation]
---

# kura - Unified Type Constraint Storage

kura provides a simple way to store and export type constraints from multiple libraries.

## Core Usage

### Basic Declaration
```perl
use Exporter 'import';
use Types::Common -types;

use kura Name => StrLength[1, 255];
use kura Age => Int & sub { $_ >= 0 };
use kura Email => sub { /@/ };  # Code ref auto-converted
```

Syntax: `use kura NAME => CONSTRAINT;`

### Supported Constraints
- Type objects (Type::Tiny, Moose, Specio, Data::Checks)
- Code references (converted to Type::Tiny)
- Hash references with `constraint` and `message`

## Practical Examples

### Export Types
```perl
package MyTypes {
    use parent 'Exporter::Tiny';
    use Types::Common -types;

    use kura Name => StrLength[1, 255];
    use kura Email => Str & sub { /@/ };
}

use MyTypes qw(Name Email);
Name->check('John');  # true
```

### Built-in Class (v5.40+)
```perl
class User {
    use Types::Common -types;
    use kura Name => StrLength[1, 255];

    field $name :param :reader;

    ADJUST {
        Name->assert_valid($name);
    }
}

my $user = User->new(name => '');  # Dies: validation error
```

## Best Practices

1. **Always load an exporter**: `use Exporter 'import';`
2. **Declare in order**: Define child constraints before parent constraints
   ```perl
   use kura Child => Str;
   use kura Parent => Dict[ name => Child ];  # Correct order
   ```
3. **Private constraints**: Prefix with `_` to prevent export
   ```perl
   use kura _Private => Str;  # Not exported
   ```
4. **Package variables**: `@EXPORT_OK` and `@KURA` are auto-populated
