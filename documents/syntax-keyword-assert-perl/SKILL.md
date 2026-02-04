---
name: syntax-keyword-assert-perl
description: Use Syntax::Keyword::Assert for zero-cost assertions in Perl
version: 1.0.0
author: kfly8
tags: [perl, cpan, assert, debugging, syntax-extension]
---

# Syntax::Keyword::Assert - Zero-Cost Assertions

Syntax::Keyword::Assert provides an `assert` keyword for Perl with zero runtime cost when disabled.

## Core Function

### `assert EXPR`
```perl
use Syntax::Keyword::Assert;

assert $x > 0;
assert $obj isa "MyClass";
assert defined $value;

# Dies with "Assertion failed" if expression is false
assert "apple" eq "banana";  # Dies: Assertion failed
```

## Key Features

### Zero Runtime Cost
When assertions are disabled, they are completely removed at compile time:
```perl
# In production with assertions disabled:
assert expensive_check();  # This code is completely removed
```

### Environment Control
```perl
# Enable/disable assertions before module loading
$ENV{PERL_ASSERT_ENABLED} = 0;  # Disable assertions
use Syntax::Keyword::Assert;

# Or keep default (enabled)
use Syntax::Keyword::Assert;
```

## Practical Examples

### Input Validation
```perl
sub divide {
    my ($a, $b) = @_;
    
    assert defined $a && defined $b;
    assert $b != 0;
    
    return $a / $b;
}
```

### Object Type Checking
```perl
sub process_user {
    my $user = shift;
    
    assert $user isa "User";
    assert $user->can("get_name");
    
    return $user->get_name();
}
```

### Development Debugging
```perl
sub complex_algorithm {
    my @data = @_;
    
    assert @data > 0;
    
    my $result = process_data(@data);
    
    assert defined $result;
    assert ref($result) eq 'HASH';
    
    return $result;
}
```

### Contract Programming
```perl
sub fibonacci {
    my $n = shift;
    
    # Precondition
    assert $n >= 0;
    
    my $result = $n <= 1 ? $n : fibonacci($n-1) + fibonacci($n-2);
    
    # Postcondition
    assert $result >= 0;
    
    return $result;
}
```

## Production Deployment

### Disable in Production
```perl
# In deployment script or environment setup
BEGIN {
    $ENV{PERL_ASSERT_ENABLED} = 0 if $ENV{PRODUCTION};
}

use Syntax::Keyword::Assert;
# All assertions are now compile-time no-ops
```

### Conditional Assertions
```perl
# Development-only assertions
use Syntax::Keyword::Assert;

sub critical_function {
    my $data = shift;
    
    # This assertion disappears in production
    assert validate_complex_invariant($data);
    
    return process($data);
}
```

## Best Practices

1. **Use for debugging**: Add assertions during development, disable in production
2. **Check invariants**: Verify assumptions about data state and object types
3. **Validate inputs**: Assert preconditions for function parameters
4. **Document assumptions**: Assertions serve as executable documentation
5. **Zero-cost safety**: Enable aggressive checking without production performance penalty