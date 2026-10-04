---
name: validation-microflows
description: "Validation microflows for new/edit pages — attribute checks, feedback messages, and conditional validation chains. Use when a form needs input validation with messages shown against the fields."
---

# Validation Microflows Skill

This skill provides guidance for creating validation microflows in MDL that validate user input on NewEdit pages and provide feedback to users.

## When to Use This Skill

Use this skill when:
- Creating validation logic for NewEdit pages
- Implementing attribute validation with feedback messages
- Building conditional validation chains
- Creating action microflows that call validation microflows

> **Nanoflow validation:** The same patterns apply to nanoflows (`create nanoflow` instead of `create microflow`). Use nanoflows for client-side validation when server roundtrips are unnecessary — validation feedback renders instantly without a network call.

## The Validation Pattern

Mendix validation follows a two-microflow pattern:

1. **VAL_Entity_Action** - The validation microflow that:
   - Takes an entity object as parameter
   - Validates each required field
   - Shows validation feedback on invalid fields
   - Returns a Boolean indicating overall validity

2. **ACT_Entity_Action** - The action microflow that:
   - Calls the validation microflow
   - Only proceeds with save/commit if validation passes
   - Closes the page on success

## MDL Syntax

### VALIDATION FEEDBACK Statement

```mdl
validation feedback $VariableName/attributename message 'Error message';
```

With template arguments (for dynamic messages):
```mdl
validation feedback $VariableName/attributename message '{1}' with ({1} = $MessageVariable);
```

### CLOSE PAGE Statement

```mdl
close page;
```

Or to close multiple pages:
```mdl
close page 2;
```

## Complete Example

### Validation Microflow (VAL_Car_NewEdit)

```mdl
mdl 1;
/**
 * Validates a Car entity for NewEdit operations
 *
 * Performs validation on all required fields and displays
 * appropriate error messages to the user.
 *
 * @param $Car The Car entity to validate
 * @returns Boolean indicating if all validations passed
 */
create microflow MdlTemplates.VAL_Car_NewEdit (
  $Car: MdlTemplates.Car
)
returns boolean as $IsValid
folder 'OverviewPages'
begin
  -- Initialize validation flag
  declare $IsValid boolean = true;

  -- Validate Brand (required text field)
  if trim($Car/Brand) = '' then
    set $IsValid = false;
    validation feedback $Car/Brand message 'Brand is required';
  end if;

  -- Validate Model (required text field)
  if trim($Car/model) = '' then
    set $IsValid = false;
    validation feedback $Car/model message 'Model is required';
  end if;

  -- Validate Price (required, must be positive)
  if $Car/Price = empty then
    set $IsValid = false;
    validation feedback $Car/Price message 'Price is required';
  else
    if $Car/Price <= 0 then
      set $IsValid = false;
      validation feedback $Car/Price message 'Price must be greater than 0';
    end if;
  end if;

  -- Validate enumeration (required)
  if $Car/CarType = empty then
    set $IsValid = false;
    validation feedback $Car/CarType message 'Car type is required';
  end if;

  return $IsValid;
end;
```

### Action Microflow (ACT_Car_NewEdit)

```mdl
mdl 1;
/**
 * Handles the Save action for Car NewEdit page
 *
 * Validates the Car, commits it if valid, and closes the page.
 *
 * @param $Car The Car entity to save
 * @returns Boolean indicating success
 */
create microflow MdlTemplates.ACT_Car_NewEdit (
  $Car: MdlTemplates.Car
)
returns boolean as $IsValid
folder 'OverviewPages'
begin
  -- Call validation microflow
  $IsValid = call microflow MdlTemplates.VAL_Car_NewEdit(param = $Car);

  -- Only save if validation passed
  if $IsValid then
    commit $Car;
    close page;
  end if;

  return $IsValid;
end;
```

## Validation Patterns

### Simple Required Field Validation

```mdl
if trim($entity/TextField) = '' then
  set $IsValid = false;
  validation feedback $entity/TextField message 'This field is required';
end if;
```

### Numeric Range Validation

```mdl
if $entity/Amount != empty then
  if $entity/Amount < 0 or $entity/Amount > 1000 then
    set $IsValid = false;
    validation feedback $entity/Amount message 'Amount must be between 0 and 1000';
  end if;
end if;
```

### Enumeration Required Validation

```mdl
if $entity/status = empty then
  set $IsValid = false;
  validation feedback $entity/status message 'Status is required';
end if;
```

### Enumeration Value Comparison

**IMPORTANT**: When comparing enumeration values, use the fully qualified enumeration value, NOT a string literal.

```mdl
-- CORRECT: Use fully qualified enumeration value
if $task/TaskStatus = Module.TaskStatus.Completed then
  -- Task is completed
end if;

if $task/TaskStatus != Module.TaskStatus.Cancelled then
  -- Task is not cancelled
end if;

-- WRONG: Do NOT use string literals for enumeration comparison
-- IF $Task/TaskStatus = 'Completed' THEN  -- This is incorrect!
```

### Conditional Validation Based on Enumeration

```mdl
-- Validate CompletedDate only when status is Completed
if $task/TaskStatus = Module.TaskStatus.Completed then
  if $task/CompletedDate = empty then
    set $IsValid = false;
    validation feedback $task/CompletedDate message 'Completed date is required';
  end if;
end if;

-- Validate DueDate for active (non-completed, non-cancelled) tasks
if $task/TaskStatus != Module.TaskStatus.Completed and $task/TaskStatus != Module.TaskStatus.Cancelled then
  if $task/DueDate = empty then
    set $IsValid = false;
    validation feedback $task/DueDate message 'Due date is required for active tasks';
  end if;
end if;
```

### Date Validation

```mdl
if $entity/StartDate != empty and $entity/EndDate != empty then
  if $entity/EndDate < $entity/StartDate then
    set $IsValid = false;
    validation feedback $entity/EndDate message 'End date must be after start date';
  end if;
end if;
```

### Dynamic Message with Template Arguments

```mdl
-- Build validation message with dynamic content
declare $ValidationMessage string = '';
if $entity/value < $entity/MinValue then
  set $ValidationMessage = 'Value must be at least ' + toString($entity/MinValue);
end if;
if $entity/value > $entity/MaxValue then
  set $ValidationMessage = if trim($ValidationMessage) = ''
    then 'Value must be at most ' + toString($entity/MaxValue)
    else $ValidationMessage + '. Value must be at most ' + toString($entity/MaxValue);
end if;

if trim($ValidationMessage) != '' then
  set $IsValid = false;
  validation feedback $entity/value message '{1}' with ({1} = $ValidationMessage);
end if;
```

### Association Validation

```mdl
-- Validate that an association is set
if $Order/Order_Customer = empty then
  set $IsValid = false;
  validation feedback $Order/Module.Order_Customer message 'Customer is required';
end if;
```

## Implementation Checklist

When implementing validation microflows:

1. **Initialize the validation flag**: Always start with `declare $IsValid boolean = true;`

2. **Declare all variables before using SET**: You must use `declare` before `set` for primitive variables. Parameters are automatically available but local variables require declaration.

3. **Validate all required fields**: Check each attribute that needs validation

4. **Set flag to false on error**: `set $IsValid = false;` before showing feedback

5. **Show clear error messages**: Use `validation feedback` with descriptive messages

6. **Return the validation flag**: End with `return $IsValid;`

7. **Handle nullable fields**: Check for `empty` before validating nullable fields

8. **Use appropriate validation order**: Validate presence before other constraints

**Important**: The script executor validates that all variables used with `set` are declared. If you use `set $Var = ...` without a prior `declare $Var type = ...`, you will receive an error like:
```
variable '$Var' is not declared. use declare $Var: <type> before using set
```

## Files Modified

This feature is implemented in:
- `mdl/grammar/MDL.g4` - ANTLR4 grammar with VALIDATION FEEDBACK tokens
- `mdl/ast/ast_microflow.go` - AST type definitions (MfValidationFeedbackStmt)
- `mdl/visitor/visitor_microflow_statements.go` - ANTLR listener to build AST
- `mdl/executor/cmd_microflows_builder.go` - Flow builder with variable validation
- `mdl/executor/cmd_microflows_show.go` - DESCRIBE formatter for MDL output
- `mdl/backend/modelsdk/microflow_write.go` - BSON serialization for ValidationFeedbackAction
- `sdk/microflows/microflows_actions.go` - ValidationFeedbackAction struct

## Validation rules (CREATE VALIDATION RULE)

binds a **regex** or a **range** to one attribute — `create validation rule for Mod.Entity.Attr regex Mod.Pattern error message '…'`. The rule is anonymous and entity-scoped, so the statement names the attribute; re-running it replaces the rule of the same type and leaves the attribute's others alone. Unlocked by a `STORAGE-NAME OVERRIDE` in `modelsdk/gen`: it bound `RegularExpression` where Studio Pro stores `RegExIdentifier`, and the control (same script, key reverted) fails **CE0135 "No regular expression specified"** while the fixed one is 0 errors on mxbuild 11.13 with `RegExIdentifier` on disk. Range bounds are inclusive and map to Mendix's only three kinds (`from X to Y`/`from X`/`to Y` → Between/GreaterThanOrEqualTo/SmallerThanOrEqualTo); there is no strict `<`/`>`, and the old grammar's forms for it — plus an EXPRESSION rule type Mendix does not have and an inline regex literal — were removed, having never had a visitor or handler. Required/Unique stay attribute constraints (`not null error message '…'` / `unique error message '…'`), not a second spelling here. `drop validation rule [if exists] for Mod.Entity.Attr [regex | range]` removes a rule; without a kind it removes both the regex and the range rule and leaves Required/Unique alone. Rewriting an entity carrying **MaxLength or EqualsTo** is **refused** on both engines rather than silently downgraded to Required; that round trip was lossy and `mx check` stayed green, because a Required rule is valid. Both engines carry each rule's payload on READ (`ruleInfoFromGen` / `parseValidationRuleInfo`), which is what makes the refusal narrow instead of covering all of RegEx and Range — and what lets a **range bounded by another attribute** survive a rewrite even though MDL cannot author one (`describe entity` marks it with a comment rather than rendering it wrong). A rule whose payload did not survive the read is refused as firmly as an unknown type: a bare RuleInfo of the right `$Type` constrains nothing, which is the same silent downgrade wearing the right name
