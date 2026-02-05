---
name: ocaml-code-style
description: Refactoring and tidying OCaml code to be more idiomatic. Use when the user asks to tidy, clean up, refactor, or improve OCaml code, or when reviewing Claude-generated OCaml code for consolidation.
license: ISC
---

# OCaml Code Style and Refactoring

## When to Use This Skill

Invoke this skill when:
- User asks to "tidy", "clean up", "refactor", or "improve" OCaml code
- User requests more idiomatic or concise OCaml
- Reviewing and consolidating Claude-generated OCaml code
- Improving module structure or hygiene
- Reducing code duplication

## Core Refactoring Principles

### 1. Option and Result Combinators

**Replace verbose pattern matching with combinators:**

```ocaml
(* Before *)
match get_value () with
| Some x -> Some (x + 1)
| None -> None

(* After *)
Option.map (fun x -> x + 1) (get_value ())
```

**Common combinators to prefer:**
- `Option.map`, `Option.bind`, `Option.value`, `Option.iter`, `Option.fold`
- `Result.map`, `Result.bind`, `Result.map_error`, `Result.join`

### 2. Monadic Syntax

**Use let* (bind) and let+ (map) for cleaner chaining:**

```ocaml
(* Before *)
match fetch_user id with
| Ok user ->
    (match fetch_permissions user with
     | Ok perms -> Ok (user, perms)
     | Error e -> Error e)
| Error e -> Error e

(* After *)
let open Result.Syntax in
let* user = fetch_user id in
let+ perms = fetch_permissions user in
(user, perms)
```

### 3. Pattern Matching Over Nested Conditionals

```ocaml
(* Before *)
if x > 0 then
  if x < 10 then "small"
  else "large"
else "negative"

(* After *)
match x with
| x when x < 0 -> "negative"
| x when x < 10 -> "small"
| _ -> "large"
```

### 4. Factor Out Common Code

**Identify and extract repeated patterns:**

```ocaml
(* Before - repeated pattern *)
let parse_int s =
  try int_of_string s
  with Failure _ -> raise (Parse_error ("Invalid integer: " ^ s))

let parse_float s =
  try float_of_string s
  with Failure _ -> raise (Parse_error ("Invalid float: " ^ s))

(* After - factored out *)
let with_parse_error ~kind f s =
  try f s
  with Failure _ ->
    raise (Parse_error (Printf.sprintf "Invalid %s: %s" kind s))

let parse_int = with_parse_error ~kind:"integer" int_of_string
let parse_float = with_parse_error ~kind:"float" float_of_string
```

### 5. Module Hygiene

**Abstract type t pattern:**

```ocaml
module User : sig
  type t
  val create : name:string -> email:string -> t
  val name : t -> string
  val email : t -> string
  val pp : Format.formatter -> t -> unit
end = struct
  type t = { name : string; email : string }
  let create ~name ~email = { name; email }
  let name t = t.name
  let email t = t.email
  let pp fmt t = Format.fprintf fmt "%s <%s>" t.name t.email
end
```

**Avoid generic module names:**
- Bad: `Util`, `Utils`, `Helpers`, `Common`, `Misc`
- Good: `String_ext`, `File_io`, `Json_codec`

### 6. Modern OCaml Patterns

**Use labeled arguments for clarity:**

```ocaml
(* Instead of: *)
let create name email age = ...

(* Use: *)
let create ~name ~email ~age = ...
```

**Use local opens:**

```ocaml
let open Option.Syntax in
let* x = get_x () in
let* y = get_y () in
return (x + y)
```

## Red Flags to Look For

- **Match expressions that just rewrap**: `match x with Some v -> Some (f v) | None -> None`
- **Nested matches on Result/Option**: Use let*/let+ instead
- **Repeated error messages**: Factor into helper functions
- **Deep if/then/else chains**: Convert to pattern matching
- **Modules named Util/Helper**: Rename to be specific
- **Exposed record types without accessors**: Add abstract type t
- **Missing pp functions**: Every main type should have a pretty-printer
- **Unlabeled boolean parameters**: `create name true false` is unclear

## Refactoring Workflow

1. **Read the entire codebase** to understand context
2. **Identify patterns** (duplication, verbose matching, generic names)
3. **Prioritize by impact**:
   - Code duplication (highest)
   - Verbose monadic code
   - Module structure issues
   - Nested conditionals
4. **Refactor systematically** - one pattern at a time
5. **Verify improvements** - ensure code is more readable
6. **Explain changes** with before/after snippets

## Goal

Make code more readable, maintainable, and idiomatic to experienced OCaml developers. Not just shorter, but clearer.
