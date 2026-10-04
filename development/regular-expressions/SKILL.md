---
name: regular-expressions
description: "Create and manage named regular-expression documents and bind them to attribute validation rules. Use when adding an email, phone or identifier pattern, changing a shared pattern, or working out why a regex cannot attach directly to an attribute."
---

# Regular Expressions

## When to Use This Skill

Use this skill when the user wants to:
- Add a named validation pattern (email, phone, identifier, postcode)
- See or change the regexes a project already has
- Understand why a regex cannot be attached to an attribute from MDL

## What a Mendix regular expression is

A **document**, not a string on a rule. An attribute validation rule stores a
reference to it by qualified name, so one pattern is shared by every attribute
that validates against it. That is why it gets a `create` statement of its own.

```sql
mdl 1;
list regular expressions;
list regular expressions in Val;
describe regular expression Val.EmailAddress;   -- re-executable MDL

/** A, not too restrictive, email address regular expression */
create regular expression Val.EmailAddress (
  Expression: '\w+((-|\+|\.)\w+)*@\w+([\.-]?\w+)*(\.\w{2,})+'
);

drop regular expression Val.EmailAddress;
```

| Property | Meaning | Default |
|----------|---------|---------|
| `Expression` | the pattern — **required** | — |
| `Documentation` | free text | none |
| `ExportLevel` | `Hidden` or `API` (`Public` is a deprecated spelling of `API`, MDL-DEPR161) | `Hidden` |

## Writing the pattern

The pattern is an ordinary MDL string:

- **Backslashes are NOT escape characters.** Write `\d`, `\w`, `\.` exactly as
  Mendix should see them — do not double them.
- **A single quote is doubled**, like any MDL string: `'^it''s$'`.
- Commas, braces and pipes inside the pattern are fine — the whole thing is one
  quoted string.

## Go cannot check every legal pattern

Mendix validates with **.NET's** regex engine, which accepts constructs Go's RE2
does not — lookaround and backreferences most commonly. The Mendix Email
Connector itself ships `.*(?<!/)$`.

mxcli stores such a pattern unchanged and `describe` adds:

```
-- note: uses .NET regex syntax that Go cannot compile (e.g. lookaround); not verifiable here
```

That is a note, not an error. Do not "fix" a pattern because mxcli could not
compile it.

## Binding a regex to an attribute

The pattern is a document; the binding is a **validation rule** on the entity:

```sql
mdl 1;
create regular expression Val.EmailAddress (
  Expression: '^[^@\s]+@[^@\s]+\.[^@\s]+$'
);

create validation rule for Val.Person.Email
  regex Val.EmailAddress
  error message 'Enter a valid email address';
```

Create the pattern first. The rule stores a **reference by qualified name**, so
a name that does not resolve is refused up front — otherwise the build reports
`CE0135 "No regular expression specified"` and the attribute is unconstrained.

Ranges use the same statement. Bounds are inclusive and either may be omitted;
Mendix has no strict `<` or `>`, so there is no exclusive form:

```sql
mdl 1;
create validation rule for Val.Booking.Guests range from 1 to 100 error message '…';
create validation rule for Val.Product.Price  range from 0        error message '…';
create validation rule for Val.Order.Discount range to 100        error message '…';
```

Re-running a rule replaces the one of the **same type** on that attribute and
leaves the others alone, so an attribute can carry a Required rule and a RegEx
rule at once.

Required and Unique are **not** written with this statement — they are attribute
constraints:

```sql
mdl 1;
create entity Val.Person (
  Email: String(200) not null error message 'Email is required',
  Code:  String(20)  unique error message 'Code must be unique'
);

alter entity Val.Person modify attribute Email: String(200)
  not null error message 'Email is required';
```

### What still cannot be authored

A **range bounded by another attribute** rather than a literal cannot be
*written* in MDL, but it does survive a rewrite untouched — `describe entity`
marks it with a comment rather than rendering it as something it isn't. Add or
change one in Studio Pro.

`MaxLength` and `EqualsTo` rules cannot be represented at all. mxcli **refuses**
to rewrite an entity carrying one (`alter entity`, `create or modify entity`)
rather than silently downgrading it to a Required rule, which is what it used to
do — the constraint would vanish and the build would still pass.

## Finding out who uses one

```sql
list references to Val.EmailAddress;
```

lists the entities whose validation rules use that pattern — worth checking
before you change a shared regex.

```sql
select QualifiedName, Expression from CATALOG.REGULAR_EXPRESSIONS;
```

## Common Mistakes

| Mistake | Symptom | Fix |
|---------|---------|-----|
| Doubling backslashes | The stored pattern has `\\d` and matches nothing | Write `\d` once |
| Single quote left undoubled | Parse error | `'^it''s$'` |
| Omitting `Expression` | `has no Expression` | It is required |
| Treating the Go note as an error | A valid .NET pattern gets rewritten | The note means "not verified", not "invalid" |
| Inline pattern in a rule (`regex '^a+$'`) | Parse error | The rule takes a document name: `regex Val.MyPattern` |
| Rule created before the pattern | "regular expression not found" | `create regular expression` first |
| Expecting `range > 0` | Parse error | Mendix has only inclusive bounds: `range from 0` |

## Related

- `mxcli syntax regular-expression` — full syntax reference
- `mxcli syntax validation-rule` — binding a pattern or a range to an attribute
- `mdl-entities` — attributes and validation

## Regular expressions (LIST/DESCRIBE/CREATE [OR MODIFY]/DROP REGULAR EXPRESSION)

named patterns that attribute validation rules reference **by qualified name**, which is why they are documents. `modelsdk/gen` is **wrong** about the pattern's key — it binds `RegEx` where every Studio Pro document stores `Expression` (`generated/metamodel` agrees with the documents), so both engines share one raw-BSON codec in `mdl/regularexpressions`; a reader keyed on gen's name returns an empty pattern for every real document. Pinned against five Studio Pro-authored documents (Email Connector 6.4.2, Community Commons 11.5.1). Mendix validates with .NET's engine, so a pattern Go's RE2 cannot compile (lookaround — the Email Connector ships one) is stored unchanged and reported "not verifiable", never "invalid". A `validate` edge into `CATALOG.REFS` makes `list references to <regex>` list the entities using it
