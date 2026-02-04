---
name: hoon-development
description: Write and compile Hoon code following Nock conventions and NockApp patterns. Use when working with Hoon kernel code, modifying state structures, adding pokes/peeks, or debugging Hoon compilation.
---

# Hoon Development Guide

This skill helps you write idiomatic Hoon code for the Prover NockApp kernel.

## Hoon Basics

### File Structure

```hoon
::  Comments start with ::
::  Documentation comments
::
|%  ::  Core definition (library of types and functions)
+$  type-name     ::  Type definition
  structure
--

|_  =state        ::  Door (object with state)
++  arm-name      ::  Arm (method/function)
  code
--
```

### Type Definitions

```hoon
::  Atoms (basic types)
@ud   :: Unsigned decimal (0, 1, 42)
@t    :: Text/cord ('hello')
@tas  :: Term/symbol (%groth16, %pending)
@da   :: Timestamp/date (~2024.1.1)

::  Complex types
(list @t)              :: List of text
(map @ud @t)           :: Map from numbers to text
(unit @t)              :: Optional text (~ or [~ 'value'])
?(%a %b %c)            :: Union of terms

::  Structures
+$  person
  $:  name=@t
      age=@ud
      email=@t
  ==

::  Unions (discriminated)
+$  action
  $%  [%create name=@t]
      [%update id=@ud name=@t]
      [%delete id=@ud]
  ==
```

## State Management

### State Structure

Your NockApp state should be versioned:

```hoon
+$  state
  $:  %v1                          :: Version marker
      data=(map @ud entry)         :: Your data
      next-id=@ud                  :: ID counter
      config=settings              :: Configuration
  ==
```

### Accessing State Fields

```hoon
::  Read field
=/  current-id  next-id.state

::  Read nested field
=/  first-entry  (~(get by data.state) 1)
```

### Updating State Immutably

**IMPORTANT**: Never mutate state directly. Always create a new state.

```hoon
::  Update single field
state(next-id +(next-id.state))

::  Update multiple fields
state(data new-data, next-id +(next-id.state))

::  Update with complex computation
=/  new-data  (~(put by data.state) key value)
=/  new-id    +(next-id.state)
state(data new-data, next-id new-id)
```

## The ++poke Pattern

All input commands flow through `++poke`:

```hoon
++  poke
  |=  =cause                       :: Take a cause as input
  ^-  [effects=(list effect) _state]  :: Return effects and new state
  ?-  -.cause                      :: Pattern match on cause tag
      %command-one
    ::  Handle command one
    :_  state                      :: Return state first (reversed)
    :~  [%http-response 200 body]  :: Effect list
    ==

      %command-two
    ::  Handle command two
    =/  updated-state  state(...)
    :_  updated-state
    :~  [%http-response 201 body]
        [%log 'Action completed']
    ==
  ==
```

### Key Patterns

1. **Extract inputs from cause**:
   ```hoon
   =/  input-field  field.cause
   ```

2. **Validate inputs**:
   ```hoon
   ?:  =(input-field 0)
     :_  state
     [%http-response 400 '{"error":"Field cannot be zero"}']~
   ```

3. **Compute new values**:
   ```hoon
   =/  new-id  +(next-id.state)
   =/  entry   [id data timestamp]
   ```

4. **Update state**:
   ```hoon
   =/  updated-state  state(data (~(put by data.state) key entry))
   ```

5. **Return effects and state**:
   ```hoon
   :_  updated-state
   :~  [%http-response 200 body]
       [%log 'Success']
   ==
   ```

## Map Operations

### Common Map Functions

```hoon
::  Insert or update
=/  new-map  (~(put by old-map) key value)

::  Lookup (returns unit)
=/  maybe-value  (~(get by map) key)
?~  maybe-value
  :: Handle not found
:: Handle found, use u.maybe-value

::  Delete
=/  new-map  (~(del by old-map) key)

::  Check existence
=/  exists  (~(has by map) key)

::  Convert to list
=/  pairs  ~(tap by map)  :: List of [key value]

::  Get size
=/  count  ~(wyt by map)
```

### Safe Map Access Pattern

```hoon
=/  maybe-entry  (~(get by snarks.state) id.cause)
?~  maybe-entry
  ::  Not found - return 404
  :_  state
  :~  [%http-response 404 '{"error":"Not found"}']
  ==
::  Found - use u.maybe-entry
=/  entry  u.maybe-entry
:: ... continue with entry
```

## List Operations

```hoon
::  Create list
=/  my-list  ~['a' 'b' 'c']
=/  empty-list  ~

::  Add to front
=/  new-list  [item my-list]

::  Iterate/map
=/  doubled  (turn my-list |=(x=@ud (mul x 2)))

::  Filter
=/  evens  (skim my-list |=(x=@ud =(0 (mod x 2))))

::  Fold/reduce
=/  sum  (roll my-list add)

::  Check if empty
?~  my-list
  :: Empty case
:: Non-empty case, i.my-list is head, t.my-list is tail
```

## Control Flow

### Conditionals

```hoon
::  If-then-else (for values)
?:  condition
  value-if-true
value-if-false

::  If-null check
?~  maybe-value
  handle-null
handle-value  :: u.maybe-value is the unwrapped value

::  Pattern matching
?-  value
  %option-a  result-a
  %option-b  result-b
  %option-c  result-c
==
```

### Variable Binding

```hoon
::  Bind variable
=/  name  value

::  Bind with type
=/  name  ^-  @ud  42

::  Sequential bindings
=/  a  1
=/  b  2
=/  c  (add a b)
c  :: Returns 3
```

## Text and String Operations

### Creating Text

```hoon
::  Literal cord (compile-time)
'hello'

::  Convert with crip (runtime)
(crip "hello")

::  Convert tape to cord
=/  t  "hello"
=/  c  (crip t)
```

### Text Formatting

```hoon
::  Format number to text
=/  num-text  (scow %ud 42)         :: "42"
=/  id-text   (scow %ud id.cause)   :: Format ID

::  Convert text to tape for manipulation
=/  tape-form  (trip 'hello')       :: "hello"

::  Concatenate (as tapes)
=/  result  (weld "hello" " world")
=/  cord-result  (crip result)      :: 'hello world'
```

### JSON-ish String Building (Simplified)

```hoon
::  Simple response
'{"success":true,"id":42}'

::  With interpolation (manual)
=/  id-str  (scow %ud id)
(crip (weld "{\"id\":" (weld id-str "}")))
```

**Note**: The prover uses helper functions for JSON formatting. See `++format-submit-response` in prover.hoon.

## Common Helper Functions

### From the Prover Codebase

```hoon
++  format-submit-response
  |=  id=@ud
  ^-  tape
  (weld "{\"success\":true,\"id\":" (weld (trip (scow %ud id)) "}"))

++  format-snark-detail
  |=  [id=@ud entry=snark-entry]
  ^-  tape
  ::  Build JSON response string
  ...
```

### Creating Your Own Helpers

```hoon
++  build-error-response
  |=  message=@t
  ^-  @t
  (crip (weld "{\"error\":\"" (weld (trip message) "\"}")))

++  format-list-response
  |=  items=(list @t)
  ^-  @t
  ::  Convert list to JSON array
  ...
```

## Type Hints and Casts

```hoon
::  Specify return type
=/  value  ^-  @ud  42

::  Cast to type
=/  entry  ^-  snark-entry
  [id proof inputs vk system submitter now %pending ~ notes]

::  Useful for complex structures
=/  new-state  ^-  state
  state(data new-data, next-id new-id)
```

## The Bowl (Context)

In NockApp pokes, you have access to a `bowl` with context:

```hoon
++  poke
  |=  [=cause =bowl:cask]  :: Bowl is available
  ^-  [(list effect:cask) _state]
  ::  Access bowl fields:
  now.bowl      :: Current timestamp (@da)
  our.bowl      :: Our identity
  ::  etc.
```

**Common use**: Get current timestamp

```hoon
=/  timestamp  now.bowl
=/  entry  [id data timestamp ...]
```

**Note**: In the prover, we use `now` directly (it's implicitly from bowl).

## Error Handling

### Validation Pattern

```hoon
::  Check condition
?:  (lth id.cause 1)
  ::  Return error
  :_  state
  :~  [%http-response 400 '{"error":"ID must be positive"}']
  ==

::  Continue with valid input
...
```

### Not-Found Pattern

```hoon
=/  maybe-entry  (~(get by data.state) id.cause)
?~  maybe-entry
  :_  state
  :~  [%http-response 404 '{"error":"Not found"}']
      [%log (crip "Entry {(scow %ud id.cause)} not found")]
  ==
::  Entry exists, use u.maybe-entry
...
```

## Effects

Common effect types:

```hoon
[%http-response code=@ud body=@t]     :: HTTP response
[%log message=@t]                     :: Log message
[%error message=@t]                   :: Error log
```

### Multiple Effects

```hoon
:_  state
:~  [%http-response 201 body]
    [%log 'SNARK submitted']
    [%log (crip "ID: {(scow %ud new-id)}")]
==
```

## Compiling and Testing

### Compilation

```bash
# Compile Hoon to Nock
hoonc prover/hoon/prover.hoon -o prover/out.jam

# Check for syntax errors
hoonc --check prover/hoon/prover.hoon
```

### Common Compilation Errors

1. **Mint failure**: Type mismatch
   - Check your type annotations (`^-  type  value`)
   - Ensure structure matches type definition

2. **Find failure**: Unknown name
   - Check spelling of variables and arms
   - Ensure variables are in scope (`=/` binding)

3. **Nest failure**: Type doesn't fit expected shape
   - Check structure field order
   - Verify all required fields are present

### Debugging Tips

1. **Add log effects**:
   ```hoon
   [%log 'Reached this point']
   [%log (crip "Value: {(scow %ud value)}")]
   ```

2. **Simplify complex expressions**:
   ```hoon
   ::  Instead of nested calls
   =/  step1  (operation1 input)
   =/  step2  (operation2 step1)
   =/  step3  (operation3 step2)
   step3
   ```

3. **Check types with hints**:
   ```hoon
   =/  value  ^-  expected-type  expression
   ```

## Best Practices

1. **Always version your state**: `$: %v1 ...`
2. **Use type hints for complex values**: `^- type value`
3. **Validate inputs early**: Check before updating state
4. **Keep arms focused**: One responsibility per arm
5. **Use helper functions**: Extract formatting and validation
6. **Log important operations**: Help with debugging
7. **Handle errors explicitly**: Don't assume success
8. **Update state immutably**: Use `state(field new-value)`
9. **Test incrementally**: Compile after each change
10. **Follow existing patterns**: Match the style in prover.hoon

## Quick Reference

### Variable Binding
```hoon
=/  name  value           :: Bind variable
=/  name  ^-  @ud  42     :: With type hint
```

### State Update
```hoon
state(field value)                    :: Single field
state(field1 val1, field2 val2)      :: Multiple fields
```

### Map Operations
```hoon
(~(put by map) key value)    :: Insert/update
(~(get by map) key)          :: Lookup (returns unit)
(~(del by map) key)          :: Delete
~(tap by map)                :: Convert to list
```

### Conditionals
```hoon
?:  condition  true-branch  false-branch   :: If-then-else
?~  maybe-val  null-branch  value-branch   :: If-null
?-  value  %a a  %b b  ==                  :: Pattern match
```

### Effects
```hoon
:_  state
:~  [%http-response 200 '{"ok":true}']
    [%log 'Done']
==
```

## Example: Adding a New Poke

Let's add a `%count-snarks` command:

```hoon
::  1. Add to cause type
+$  cause
  $%  ...
      [%count-snarks ~]
  ==

::  2. Implement in ++poke
++  poke
  |=  [=cause =bowl:cask]
  ^-  [(list effect:cask) _state]
  ?-  -.cause
    ...

    %count-snarks
  =/  count  ~(wyt by snarks.state)
  =/  response  (crip (weld "{\"count\":" (weld (trip (scow %ud count)) "}")))
  :_  state
  :~  [%http-response 200 response]
      [%log (crip "Total SNARKs: {(scow %ud count)}")]
  ==
  ==
```

Done! Compile and test:

```bash
hoonc prover/hoon/prover.hoon -o prover/out.jam
```

## Additional Resources

- Hoon School: https://developers.urbit.org/guides/core/hoon-school
- Hoon Standard Library: https://developers.urbit.org/reference/hoon
- NockApp Documentation: Check the nockup project docs

## Common Patterns from Prover Codebase

### ID Generation
```hoon
=/  new-id  next-id.state
:: ... use new-id ...
state(next-id +(next-id.state))
```

### Building Entries
```hoon
=/  entry  ^-  snark-entry
  :*  id
      proof
      inputs
      vk
      system
      submitter
      now
      %pending
      ~
      notes
  ==
```

### Map Insert Pattern
```hoon
=/  updated-state
  state(snarks (~(put by snarks.state) new-id entry), next-id +(next-id.state))
```

### Response with State
```hoon
:_  updated-state
:~  [%http-response 201 (crip (format-submit-response new-id))]
    [%log (crip "SNARK #{(scow %ud new-id)} submitted")]
==
```
