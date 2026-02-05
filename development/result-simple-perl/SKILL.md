---
name: result-simple-perl
description: Use Result::Simple for tuple-based error handling in Perl
version: 1.0.0
author: kfly8
tags: [perl, cpan, error-handling, result-type]
---

# Result::Simple - Tuple-based Error Handling

Result::Simple provides lightweight error handling using tuples `($value, $error)` instead of objects.

## Core Functions

### `ok($value)` / `err($error)`
```perl
use Result::Simple qw(ok err);

sub divide {
    my ($a, $b) = @_;
    return err('Division by zero') if $b == 0;
    return ok($a / $b);
}

my ($result, $error) = divide(10, 2);
if ($error) {
    warn "Error: $error";
} else {
    print "Result: $result";
}
```

## Practical Examples

### Error Chaining Pattern
```perl
sub process_config {
    my $filename = shift;
    
    my ($content, $read_error) = read_file($filename);
    return (undef, $read_error) if $read_error;
    
    my $data = eval { decode_json($content) };
    return err("JSON error: $@") if $@;
    
    return ok($data);
}
```

### Type Checking with result_for
```perl
use Result::Simple qw(ok err result_for);
use Types::Standard qw(Dict Str);
use Types::Common::Numeric qw(PositiveInt);
use kura Error => Dict[message => Str];

# result_for requires structured error type (not plain string)
result_for calculate => PositiveInt, Error;

sub calculate {
    my ($a, $b) = @_;
    # Error must be structured (HashRef)
    return err({ message => 'Invalid input' }) if $a < 0;
    return ok($a * $b);
}

# Set RESULT_SIMPLE_CHECK_ENABLED=1 to activate type checking
# $ENV{RESULT_SIMPLE_CHECK_ENABLED} = 1;

my ($result, $error) = calculate(5, 3);
if ($error) {
    warn "Error: $error->{message}";
} else {
    print "Result: $result";  # 15
}

# Type checking works when RESULT_SIMPLE_CHECK_ENABLED=1
# calculate(5.5, 3);  # Dies: Invalid success result (Float instead of PositiveInt)
```

**Important**: `result_for` requires:
- Type::Tiny objects (not string type names)
- Structured error type (use `Dict[...]` with kura)
- Environment variable `RESULT_SIMPLE_CHECK_ENABLED=1` for runtime checking

