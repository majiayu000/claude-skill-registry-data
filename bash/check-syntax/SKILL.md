---
name: check-syntax
description: "Validate MDL with `mxcli check` before presenting or executing it, including reference resolution against a project. Use ALWAYS before showing MDL to a user, running `mxcli exec`, or committing a .mdl file — exec refuses exactly what check rejects."
---

# MDL Syntax Validation Skill

This skill ensures MDL scripts are validated before presenting them to users or executing them.

## When to Use This Skill

**ALWAYS** use this skill before:
- Presenting MDL code to users
- Executing MDL scripts via `mxcli exec`
- Committing MDL files to version control

## `exec` refuses what `check` rejects

`mxcli exec` runs the same semantic checks before writing anything. A script whose
checks report an **error** is not executed at all — nothing is written — because
`exec` applies statements one at a time and cannot roll back, so a known-bad
script would leave the model partly updated. Warnings are printed and do not stop
the run.

```bash
mxcli exec script.mdl -p app.mpr              # checked, then applied
mxcli exec script.mdl -p app.mpr --no-check   # applied regardless
```

This does **not** replace running `check` yourself. `check` is faster, needs no
write connection, and reports the warnings worth reading before you commit to a
run. What the gate guarantees is narrower and still valuable: a script that slips
past you cannot half-apply.

It also does not mean the script is *correct*. `mxcli check` validates MDL syntax
and mxcli's own rules; it does not validate the Mendix model. Run
`mx check` (or `mxcli docker check -p app.mpr`) after applying a slice.

### `-p` resolves references — there is no separate opt-in

`mxcli check script.mdl` alone checks syntax and the semantic rules that need no
model. **Pass `-p` and it also resolves every reference** — modules, entities,
pages, microflows and icons — against that project. It reaches inside stored
documents where a name can only be answered there: an `ALTER PAGE … SET` is
dry-run against the page it edits, so a widget the page does not have, or a
property the stored widget does not declare, is reported here rather than
stopping the script partway through `exec`.

```bash
mxcli check script.mdl                 # syntax + model-free rules
mxcli check script.mdl -p app.mpr      # ... and every reference resolved
```

`--references` is implied by `-p` and is kept only so existing scripts keep
working. It used to be required, which meant `mxcli check script.mdl -p app.mpr`
printed an unqualified `Check passed!` having resolved nothing — a misspelled
icon or entity sailed through a command that had been handed the project. A run
without a project now says what it did not check, so a pass is never read as
more than it is.

**An excluded document's dangling references are warnings, not errors.** Mendix
does not validate excluded documents (Feedback v4.0.2 ships an excluded page bound
to nanoflows it lacks, and the project checks at 0 errors), so `check` and `exec`
print them as `Reference warning` lines for excluded microflows, nanoflows, rules,
and pages/snippets exec will write excluded (`@excluded`, or a stored namesake that
is). **A missing data-source flow is a warning only when the bindings inside it are
qualified** (`Attribute: Module.Entity.Attr`, `{1} = Module.Entity.Attr`,
`Visible: Module.Entity.Attr in (…)`) — the form `describe` writes there. The
widgets inside bind against the entity that flow returns, so with the flow missing
a bare binding cannot be resolved; it is refused, naming the widget, because on
11.13.0 a bare attribute reference left a project `mx` could not load. A missing
entity still blocks.

### It also reports a name the PROJECT already has

A plain `create` of a document the project already carries is a `check` error,
not something to discover at exec time:

```
statement 4: association already exists in project: Sales.Order_Customer — use CREATE OR MODIFY to update it
```

The reason it belongs in `check` is that **`exec` stops at the first one having
already written everything before it**. A script whose fourth statement
conflicts leaves three statements' worth of changes in the project and no
fourth — so "run it and see" is not a free experiment. `check` reports every
conflict in the script before anything is written.

Three spellings say "fine if it already exists", and none is reported:
`create or modify`, `create or replace`, and `create <kind> if not exists <name>`
(which leaves the stored element untouched rather than rewriting it; every
`create` that names one element takes it, e.g. `create page if not exists M.P …`
— `mxcli syntax create-if-not-exists`). `create module M;`
is never reported either — it is a no-op when the module exists, which is what
lets it open every script.

The types covered are the ones `exec` refuses: entity, enumeration, constant,
association, microflow, nanoflow, rule, page, snippet, layout, java action,
javascript action, workflow, menu, task queue, scheduled event, regular
expression, database connection, REST client, OData client and service, message
definition collection, the integration/agent document types, module roles,
user roles, demo users and configurations. Annotations are the one known gap
(they have no name to compare). If you find another that `exec` refuses and
`check` does not, that is a bug of exactly the shape
`TestEveryCreateStmtIsClassified` and `TestEveryCreateDocTypeIsProjectChecked`
exist to prevent.

Separately, `check` reports **MDL-DUPNAME** for a name Mendix will not let two
elements share — a nanoflow named like a microflow, a page and a snippet, an
enumeration and an entity, or the same kind spelled in another case
(`M.act_login` next to `M.ACT_Login`, CE0122). It covers `rename … to` and
`move … to Module` onto a taken name too. `mxcli help MDL-DUPNAME` has the
table.

### It reports what the script REMOVES from the project

`create or modify entity` is on the list above — it is never a conflict, because
"fine if it already exists" is exactly what it says. What it does **not** say is
that it rebuilds the entity from the statement, so every member the statement
omits is deleted. Slice an app into ordered scripts and that becomes a real
hazard: an attribute added by a later `alter entity` — a calculated one whose
microflow does not exist until then is the usual reason — is gone the moment the
earlier script is re-run on its own. **Script order is load-bearing, even though
each script is individually idempotent.**

`check` now says so before anything is written, as **MDL087**:

```
⚠ applying this script to the project removes 1 member(s) from entity
  ServiceCore.LithoSystem that it does not restate: OpenRequestCount
  — anything still bound to them (widgets, microflows) fails the build with CE1613
    at ServiceCore.LithoSystem
    → … or add them incrementally with 'alter entity ServiceCore.LithoSystem
      add attribute <name>: <type>;' in this script; if they are meant to go,
      say so with 'alter entity … drop attribute <name>;'
```

`exec` prints the same list — but as it applies the statement, by which point the
attribute is gone. Left unreported entirely, the loss surfaces slices later as
`CE1613` on whatever still binds it, naming the *page*, not the script that
removed the attribute (ako/mxcli#562).

Two properties of the rule are worth knowing, because they are what keep it from
becoming noise you learn to scroll past:

- **It is the NET effect of the whole script, not one statement's.** A script
  that rebuilds an entity and then adds the members back with `alter entity …
  add attribute` loses nothing and is silent. So the *combined* slices check
  clean and slice 01 alone does not, which is precisely the difference that bit.
- **An explicit removal is not reported.** `drop attribute`, `rename attribute`
  and `drop entity` say what they do. Only a member the project holds, that the
  script neither restates nor asks to remove, is a warning.

It is a **warning**: "modify to this shape" is a legitimate intent and `check`
still exits 0. The defect was the silence, not the behaviour. It also covers the
members that are not attributes — the four audit system fields and an omitted
`extends` — because those drop the same way.

### It reports the flow changes `exec` would refuse

`create or modify microflow|nanoflow` on a stored flow is a patch. A change the
patch cannot make (inside a loop body or error handler, a redrawn connector, a
`return` added) is refused by `exec` under `mdl 1;`, and rebuilt (IDs, merges and
curves lost) without the header. With `-p`, `check` runs the same verdict `exec`
and `diff` run: an **MDL-V1-REBUILD** error quoting exec's refusal under `mdl 1`,
the MDL-V1-REBUILD warning without the header, and **MDL090** for an `alter
microflow|nanoflow` exec would refuse. Use `alter` for the change, or drop and
create the flow. A flow an earlier statement of the script touches is not
predicted (exec sees that statement's result), and `fmt --upgrade --header -p`
keeps the header off a file it would make refuse (ako/mxcli#876).

### It reports a doc comment that is lost

A `/** … */` doc comment documents the statement right after it, and only a
`create` of something with documentation stores one. Above a `drop`, `grant`,
`revoke`, `set`, `alter` or `create module` it is ignored, so **MDL089** warns
and names the next statement that could have taken it. In drop-then-create, put
the comment between the `drop` and the `create` (ako/mxcli#877).

### It resolves MEMBER names too, where it can establish the entity

Resolution does not stop at the entity. An attribute named in a **create** or
**change** activity is looked up on that entity *and its generalizations*, so a
typo is reported by `check` rather than by mxbuild as `CE1613 "The selected
attribute '…' no longer exists"` a whole build later:

```
Sales.ACT_Close: Sales.Order has no member "IsArchived" (in change $Order)
  — it has OrderNo, Status — mxbuild reports this as CE1613 …
```

This needs the target's entity to be **known**, and that is the boundary worth
understanding rather than assuming:

| the object comes from | checked? |
|---|---|
| a `create Module.Entity (…)` | yes — the entity is in the statement |
| a microflow/nanoflow **parameter** | yes |
| `retrieve $L from Module.Entity` | yes |
| `retrieve $L from $Obj/Module.Assoc` | yes, when `$Obj` is itself typed |
| a `loop` over any of those | yes — the iterator inherits the element type |
| anything else (`send rest request`, `response: file as $Doc`, …) | **no** |

Widget positions are resolved too:

- an **XPath constraint** on a `database from Module.Entity` source — every step
  is followed, so a bare name must be an attribute of the entity it lands on and
  a `Module.Name` step must be an association or an entity;
- a **template parameter** (`ContentParams` / `CaptionParams`) rooted in a
  variable. That one needs **no project** and fires under a bare
  `mxcli check`, because the answer is in the statement.

The template-parameter rule is narrower than "no `$` roots", and the difference
is measured rather than reasoned — the writer strips one prefix on one branch:

| `{1} = …` | |
|---|---|
| `OrderNo` | fine |
| `Order_Customer/Name` | fine — association hop, then attribute |
| `$currentObject/Order_Customer/Name` | fine — the prefix is stripped |
| `$currentObject/OrderNo` | **CE1613** |
| `$Order/Name` | **CE1613** |

Note the two-segment form: `Assoc/Attr`, not the XPath `Assoc/Entity/Attr`,
which mxbuild also rejects.

### Expression KINDS are checked in the positions that declare one

Two more things reach mxbuild as `CE0117 "Error(s) in expression"` and are now
reported by `check`:

- **A bare word as a member's value.** Mendix expressions have no bare
  identifiers, so `CHANGE $Order (Status = Closed)` is E013. Write `'Closed'`
  (a literal), `$Closed` (a variable), or `Module.Enum.Value` (an enumeration).
  Scoped to the *whole* value of a create/change member: a bare name **nested**
  in a list-operation predicate is legal — `FILTER($L, Status = 'Open')`
  resolves `Status` against the item under test — and is not reported.
- **A log message's template parameter must be a String.** `LOG … WITH ({1} =
  $Order/Qty)` is E009. Measured on 11.13.0: Integer, Decimal, Boolean,
  DateTime and an object each fail; a String attribute is clean; and
  `toString(…)` around any of them is clean. So wrap the non-String ones —
  the writer is fine, Mendix simply does not coerce here.

### Three more things check now refuses

- **An unqualified CREATE** (`create association Order_Probe …`) — MDL074, no
  project needed. `exec` always refused it; check now does too, which matters
  because exec is **not transactional**: the statements before the failure are
  already applied, and re-running hits "already exists" on them.
- **`RETURNS void AS $x`** — MDL075, no project needed. An alias names the
  variable a flow returns, so it cannot be paired with void; mxcli used to
  believe the alias and write `return $x` into a flow with no such variable
  (CE0109). Write `RETURNS void`, or give the alias the type it holds.
- **`empty($List)`** — E014. `empty` is a Mendix **keyword**, not a function, so
  the parser stops at the `(`. Write `$List = empty` or `length($List) = 0`.

**One thing to know about hint ordering**: the reference check runs before
expression checking and **exits on its first error**, so an unrelated mistake
anywhere in a file hides every expression hint in it. If you expect an E0xx and
see none, fix the reference errors first and re-run.

A variable this cannot type is left **unchecked**, never guessed at — a false
"no such member" would block a script that builds cleanly. Two more things are
deliberately not reported: a **qualified** member (`Module.Assoc`), which exec
already refuses when it cannot be an attribute, and any member on an entity the
**script itself** creates or whose attribute the script adds earlier — the
add-the-column-then-populate-it shape stays valid.

## Pre-Flight Validation Checklist

Before writing any MDL, verify these requirements:

### 0. Start the script with `mdl 1;`

A script without the header is checked and executed as `mdl 0`, the alpha language,
where some statements mean something else. Write `mdl 1;` as the first line of every
new script. To edit a headerless one, upgrade it first (`mxcli fmt --upgrade --header
-p app.mpr -w script.mdl`) — never mix the two in one file; see `choose-edit-mode`.

### 1. Check Supported Syntax

**Supported in Microflows:**
- `declare $Var type = value;` (primitives only: String/Integer/Long/Decimal/Boolean/DateTime/Enumeration)
- `$entity = create Module.Entity (...);` / `retrieve $entity from ... first;` (objects — **never** `declare` an object; that fails CE0053/CE0038 and is flagged MDL043)
- `$list = create list of Module.Entity;` (lists — **never** `declare` a list; that fails CE0053/CE0038 and is flagged MDL040)
- `set $Var = expression;`
- `$Var = create Module.Entity (attr = value);`
- `change $entity (attr = value);`
- `commit $entity [without events] [refresh];` (omitted = with events, Mendix's default)
- `delete $entity;`
- `retrieve $Var from Module.Entity [where condition];`
- `$Result = call microflow Module.Name (Param = $value);` (NOT `set $Result = ...`)
- `$Result = call nanoflow Module.Name (Param = $value);`
- `show page Module.PageName (Param = $value);`
- `close page;`
- `validation feedback $entity/attribute message 'message';`
- `log info|warning|error [node 'name'] 'message';`
- `if condition then ... [else ...] end if;`
- `loop $item in $list begin ... end loop;`
- `return $value;`
- `on error continue|rollback|[without rollback] begin handler end error;`

**Now Supported (previously not):**
- `rollback $entity [refresh];` - Reverts uncommitted changes
- `retrieve ... first` - Returns a single entity; `limit n [offset n]` returns a list (a bare `limit 1` is the object only without the `mdl 1;` header, and warns MDL-V1-LIMIT1)
- `boolean` without `default` - Auto-defaults to `false`
- `buttonstyle: warning` and `buttonstyle: info` - Now parse correctly
- Keywords as attribute names - `caption`, `label`, `title`, `text`, `content`, `format`, `range`, `source`, `check`, etc. all work unquoted

**NOT Supported (will cause errors):**
- `set $var = call microflow ...` - Use `$var = call microflow ...` (no SET)
- `while ... end while` - Use `loop` with lists
- `case ... when 'String' ...` - Case values are bare enum identifiers, never quoted or qualified; `case ... when Value then ... end case;` itself IS supported (enum splits only), and takes no `else` (MDL008) and no `AS` alias
- `TRY ... CATCH` - Use `on error` blocks
- `break` / `continue` - Not implemented
- `commit message 'text'` - Not in current grammar (session command only)

### 2. Quote All Identifiers

**Best practice: Always quote all identifiers** (entity names, attribute names, parameter names) with double quotes. This escapes every **MDL parser** keyword conflict — quotes are stripped automatically by the parser.

> **Caveat — quoting does not exempt *platform*-reserved member names.** Quoting
> only escapes MDL *parser* keywords. Names the Mendix *platform* reserves for entity
> members are still rejected after the quotes are stripped: `Type` (CE7247, MDL021),
> the system audit attributes `CreatedDate` / `ChangedDate` / `Owner` / `ChangedBy`
> (MDL020 — use the `AutoCreatedDate` / `AutoChangedDate` / `AutoOwner` / `AutoChangedBy`
> pseudo-types instead), plus the CE7247 word list (`ID`, `GUID`, `CurrentUser`, Java
> keywords, …). `"Type": String` still fails MDL021 — rename to a non-reserved name
> (e.g. `ResourceType`, `TypeValue`). "Always safe to quote" covers parser keywords, not
> these.
>
> The parse error tells you which case you are in. `'Title' is a keyword in MDL.
> Quote it to use it as a name` means quoting works and nothing has to be renamed;
> `'Type' is reserved by MENDIX itself, not just by MDL` means it does not.
> Measured across the keywords mxcli hints on: 38 are rescued by quoting, 3
> (`Type`, `Default`, `Owner`) are not.
>
> **Third case — OQL keywords, where quoting works but in a different grammar.**
> `Year`, `Month`, `Quarter`, `Week`, `Day`, `Hour` and the other date-part words are
> neither MDL parser keywords nor platform-reserved: they are accepted everywhere and
> build at 0 errors. They bite only inside a **view entity**'s OQL, and only **unquoted**
> (**CE0174**). OQL takes double-quoted identifiers just like SQL — `s."Month"`,
> `from Module."Year" as s` — and mxcli writes them through unchanged, so the usual fix
> is a quote in the OQL, not a rename. mxcli reports **MDL071** as a *warning* at
> `CREATE`/`ALTER` so the name is still cheap to change if you would rather rename.
> Applies to the **entity** name as well as its attributes.
>
> The exception is an **alias**, and that limit is OQL's own: it takes a bare identifier
> there for any name — `as "Total"`, reserved nowhere, is CE0174 too (**MDL072**). A view
> entity's attribute name is also its select alias, so a view column cannot be called
> `Month` at all — that one needs a rename, not a quote.
>
> **Exception — never quote `$`-prefixed variable/parameter references.** The quote
> rule is for *bare* names (entities, attributes, associations, declared parameter
> names). Variable and parameter **references** in expressions and widget bindings
> stay **unquoted**: `datasource: $X`, `params: ( $X: MES."Order" )`, `$currentObject`.
> Quoting them (`"$X"`) breaks resolution ("parameter … references '$X' but no such
> parameter is declared").
>
> **Enumeration values: no `=`.** Value names may be quoted like any identifier, but
> the caption follows as a quoted string — there is **no equals sign**:
> `create enumeration Mod.E ("Grade1" 'Grade 1', Grade2 'Grade 2');` (or `Grade1 caption 'Grade 1'`).
> Writing `"Grade1" = 'Grade 1'` fails with `mismatched input '='` — the `=` is the
> problem, not the quotes.

```sql
mdl 1;
create persistent entity Module."Customer" (
  "Name": string(200),
  "status": string(50),
  "create": datetime
);
```

Both `"Name"` and `` `Name` `` syntax are supported. Prefer double quotes for consistency.

Run `mxcli syntax keywords` for the full list of 320+ reserved keywords.

### 3. Validate with mxcli

**Always run these checks:**

```bash
# Step 1: Syntax check (no project needed)
./bin/mxcli check script.mdl

# Step 2: reference validation (needs project)
# Validates microflow bodies, entity/enum references, and widget tree references
# (datasource microflow/nanoflow/entity, action page/microflow, snippet refs)
./bin/mxcli check script.mdl -p app.mpr --references
```

### 4. Common Error Patterns

| Error Message | Likely Cause | Fix |
|---------------|--------------|-----|
| `mismatched input 'set'` after `call microflow` | SET not valid with CALL | Use `$var = call microflow ...` |
| `mismatched input 'create'` | Structural keyword as identifier | Use `"create"` (quoted) or rename |
| `no viable alternative at input` | Unsupported syntax | Check supported statements list |
| `microflow not found` | Referenced before created | Move microflow definition earlier or check spelling |
| `page not found` | Page doesn't exist | Check qualified name with `--references` |
| `entity not found` | Typo or wrong module | Use fully qualified name |

## Two rules that only real validation used to catch

Both are decidable from the MDL alone and now fail `check`, because a project
found them the hard way — four scripts passed `check` with 0 errors, executed
cleanly, and `mx check` then reported them:

| Rule | MxBuild | What it catches |
|---|---|---|
| `MDL-SEC20` | CE0156 | `CREATE USER ROLE` with no **System** module role — nobody holding it can sign in or read System entities. Add `System.User`. **Warning by default, error when the script enables security** (see below). |
| `MDL-PAGE20` | CE5601 | A page with **parameters and a `Url`** where the URL has no segment for a parameter. Mendix binds each parameter from the URL, so the page cannot be opened by link. |

`MDL-SEC20`'s severity follows the security level, because the underlying error
does. Measured on Mendix 11.13: the same role is **CE0156 at security level
Prototype and no error at all at level Off**, where roles are stored but not
validated. A blank project ships `Off`. So the rule warns by default and is an
error only when the script itself contains `ALTER APP SECURITY LEVEL` set to
something other than `Off` — at which point the author has said which world they
are in.

`MDL-PAGE20` accepts an attribute path in the segment (`url: 'p006/{Customer/Name}'`),
which is the usual shape — it matches the segment's leading name, not the whole
segment.

### A used flow left without access — `MDL-SEC21` (CE0106)

With a project (`check -p`), `check` simulates the script's creates, drops,
grants and revokes and reports a microflow or nanoflow the script leaves with
**no allowed role** while something that needs one names it. MxBuild's error:

> CE0106 "At least one allowed role must be selected if the microflow is used
> from navigation, a page, a nanoflow or a published service."

Measured on Mendix 11.14: a page button or data source, a snippet, a navigation
or menu-document item, or a nanoflow call needs a role (even from an unused
snippet, menu document or nanoflow). A **published REST operation does not**,
nor a microflow called only from another microflow, nor an excluded page. It is
an **error at security level Prototype or Production** and a warning at Off,
where MxBuild does not check it.

The usual cause is **drop + create in separate runs**: a create in a later run
is a *new* flow, and a new flow in a module that has its own module roles gets no
access. Within one run, and with `create or modify`, the stored roles are kept.
Fix: `grant execute on microflow M.Flow to M.Role;` in the same script, or rebuild
with `create or modify microflow` instead of dropping. Only what the script
*changes* is reported — a project that already has CE0106 does not fail an
unrelated script; `mxcli docker check` shows those.

**`check` is still necessary, not sufficient.** Run `mx check` (or
`mxcli docker check`) after every `exec`; these two rules narrow the gap, they do
not close it.

## Validation Workflow

### Before Writing MDL

1. **Read the skill files:**
   ```bash
   cat .claude/skills/write-microflows/SKILL.md
   cat .claude/skills/overview-pages/SKILL.md
   ```

2. **Check help for specific syntax:**
   ```bash
   ./bin/mxcli syntax microflow
   ./bin/mxcli syntax page
   ./bin/mxcli syntax entity
   ```

### After Writing MDL

1. **Save to a file:**
   ```bash
   cat > script.mdl << 'EOF'
   -- Your MDL here
   EOF
   ```

2. **Run syntax check:**
   ```bash
   ./bin/mxcli check script.mdl
   ```

3. **If errors, check specific syntax:**
   ```bash
   ./bin/mxcli syntax keywords    # Reserved words
   ./bin/mxcli syntax microflow   # microflow syntax
   ```

4. **Run reference check (with project):**
   ```bash
   ./bin/mxcli check script.mdl -p app.mpr --references
   ```

5. **Execute only after all checks pass:**
   ```bash
   ./bin/mxcli exec script.mdl -p app.mpr
   ```

## Script Execution Behavior

**IMPORTANT: Script execution is atomic per statement, NOT per script.**

When a script fails on statement N, statements 1 through N-1 have already been committed:

```
Statement 1: create module ✓ (committed)
Statement 2: create entity ✓ (committed)
Statement 3: create association ✓ (committed)
Statement 4: create view entity ✗ (failed - execution stops here)
Statement 5: create page (never executed)
```

**Recommendations:**
1. Split scripts into phases when experimenting with uncertain syntax
2. Use `create or modify` to make scripts idempotent
3. Re-run and check `git status` — a settled script changes nothing
4. Test new syntax patterns with minimal scripts first
5. Keep a backup of your project before running large scripts

## Script Organization

Organize scripts in dependency order:

```mdl
mdl 1;
-- ============================================
-- PHASE 1: Enumerations (no dependencies)
-- ============================================
create enumeration Module.Status (
  Active 'Active',
  Inactive 'Inactive'
);

-- ============================================
-- PHASE 2: Entities (depend on enumerations)
-- ============================================
create persistent entity Module.Customer (
  Name: string(200),
  status: Module.Status
);

create persistent entity Module.Order (
  OrderNumber: string(20)
);

-- ============================================
-- PHASE 3: Associations (depend on entities)
-- ============================================
create association Module.Order_Customer
from Module.Order to Module.Customer
type reference;

-- ============================================
-- PHASE 4: Microflows (depend on entities)
-- ============================================
create microflow Module.ACT_Save ($Customer: Module.Customer)
returns boolean as $success
begin
  declare $success boolean = false;
  commit $Customer;
  set $success = true;
  return $success;
end;

-- ============================================
-- PHASE 5: Pages (depend on microflows)
-- ============================================
create page Module.Customer_Edit (
  Title: 'Edit Customer',
  Layout: Atlas_Core.PopupLayout,
  Params: ( $Customer: Module.Customer )
) {
  dataview dvCustomer (DataSource: $Customer) {
    textbox txtName (Label: 'Name', Attribute: Name)
    -- Can reference the microflow created in Phase 4
    actionbutton btnSave (Caption: 'Save', Action: call microflow Module.ACT_Save(Customer = $Customer))
  }
};
```

## Troubleshooting Parse Errors

### Error: "snippet not found" / "page not found"

A reference to a document that hasn't been created yet in the script:

```
Error: snippet not found: MyModule.NavMenu
Error: page not found: MyModule.Customer_NewEdit
```

Script execution is sequential — each `CREATE` commits immediately. Forward references
fail because the target doesn't exist in the database at the moment the referencing
document is created.

**Fix options:**
1. **Reorder** — move the target document's `CREATE` earlier in the script (simplest fix)
2. **Placeholder pattern** — for circular dependencies (e.g. a snippet that shows pages
   that embed the snippet), create a minimal placeholder first, then create the referencing
   documents, then fill in the placeholder with `CREATE OR MODIFY` — which preserves the
   original UUID so all existing bindings remain valid
   (see [Resolve Forward References](../resolve-forward-references/SKILL.md))

Declaration order that avoids most forward references:
```
enumerations → entities → snippets (placeholder) → pages → snippets (fill-in) → microflows → navigation
```

> **Never use `CREATE OR REPLACE` for the placeholder fill-in step.** OR REPLACE deletes
> the placeholder and creates a new document with a different UUID, silently breaking
> every page or snippet that references it.

### Error: "mismatched input 'X'"

The word `X` is either:
1. A reserved word - rename the identifier
2. Unsupported syntax - check the supported statements list
3. A typo - check spelling

### Error: "no viable alternative at input"

The parser expected something different:
1. Check for missing semicolons
2. Check for missing `end if`, `end loop`, etc.
3. Verify statement syntax against the reference

### Error: "extraneous input"

Extra tokens found:
1. Check for stray characters
2. Check for duplicate semicolons
3. Verify string quotes are balanced

## Studio Pro MCP — Verification Only

When Studio Pro's embedded MCP server is available **alongside** mxcli (i.e. you are
*not* using mxcli's own `--mcp` backend, but mxcli writes the `.mpr` directly while
Studio Pro is open), use Studio Pro MCP **only for reading and verification**. Never
author with `ped_create_document` / `ped_update_document` — mxcli owns the `.mpr`, and
mixing authoring tools corrupts intent and diverges UUIDs.

### Role split

| Task | Tool |
|------|------|
| Create/modify entities, microflows, pages, nanoflows, nav | mxcli MDL |
| Verify CE errors after exec | `ped_check_errors` |
| Inspect widget tree / microflow body detail | `ped_read_document` |
| Check if a document exists before creating | `ped_find_document` |
| Full model validation | `./mxcli docker check` |

### Studio Pro reads its in-memory model, not the file — a flush IS needed

This is the opposite of what you might expect. mxcli writes directly to the `.mpr`
SQLite file, but **Studio Pro serves `ped_*` reads from its in-memory model**, which
does not hot-reload when an external process changes the file. So after `mxcli exec`:

- `ped_read_document` / `ped_check_errors` will show the **stale** pre-exec model until
  Studio Pro re-scans — call `refresh_project` first (or reload the project in the UI).
- **Hazard:** if Studio Pro later saves on its own, it overwrites mxcli's disk write with
  its in-memory copy, silently discarding your MDL changes. So a file-based write is
  **refused** while Studio Pro's `<project>.mpr.lock` is beside the `.mpr`; `exec --force`
  (or `MXCLI_ALLOW_STUDIO_PRO_OPEN=1`) overrides it, e.g. for a lock left by a crash.

**Safest practice:** don't keep the same project open-and-saving in Studio Pro while
mxcli writes it. Either close (or don't save in) Studio Pro during MDL authoring, or
`refresh_project` after every `mxcli exec` before verifying. If you need both writing
*and* a live Studio Pro, use mxcli's `--mcp` backend (which authors *through* Studio
Pro) instead of writing the file directly.

### Step 6: Post-execution verification (add to the workflow above)

After `./mxcli exec script.mdl -p app.mpr` succeeds:

1. `refresh_project` (Studio Pro MCP) so the in-memory model reflects the new file.
2. `ped_check_errors` on each created/modified document for CE errors. The argument
   depends on the Studio Pro release — read the tool's input schema:
   - up to 11.14: `{"documents": [{"documentType": "Microflows$Microflow", "documentName": "Mod.Name"}]}`
   - 11.15+: `{"filters": {"documentType": "Microflows$Microflow", "documentNamePrefix": "Mod.Name"}}`.
     11.15 **silently ignores** `documents` and checks the whole project. `documentNamePrefix`
     is a prefix (`Mod.Order` also matches `Mod.OrderLine`), so read the `'Mod.Name' (Type):`
     header above each problem. More than 100 problems come in pages: repeat the same
     `filters` with `pagination: {checkId, offset, size}` using the `Check ID` from the first answer.

> **Do not treat an empty `DESCRIBE` as proof of a dropped construct.** `DESCRIBE`
> renders from the MDL emitter, which does not yet render every activity/widget type
> (e.g. Java/JavaScript action calls, exclusive splits, some nanoflow buttons). The
> construct may be present in the model even when `DESCRIBE` omits it. To tell a real
> write-drop from an emitter gap, confirm with `ped_read_document` (the live model) or
> `./mxcli docker check` — only flag an engine bug once the live model is also missing it.

## Related Skills

- [/write-microflows](../write-microflows/SKILL.md) - Detailed microflow syntax
- [/overview-pages](../overview-pages/SKILL.md) - Page building syntax
- [/resolve-forward-references](../resolve-forward-references/SKILL.md) - Placeholder pattern and declaration ordering
- [/migrate-oracle-forms](../migrate-oracle-forms/SKILL.md) - Migration-specific guidance
