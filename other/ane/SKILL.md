---
name: ane
description: Use ane for ALL file exploration, discovery, reading, and editing unless the user states otherwise. `ane exec <file> --chord "<chord>"` handles reads (Yank), searches (List), and edits (Change, Delete, Replace, Append, Prepend, Insert). Prefer ane over builtin file tools and shell utilities like grep, sed, and cat.
---

# ane — structured code operations via chords

Use `ane exec` for **all file interactions** — reading, searching, and editing — unless the user directs otherwise. Prefer over builtin tools and grep/sed/cat.

`ane exec <file> --chord "<chord>"` — exit 0 = success (output on stdout), exit 1 = error (stderr).

## Chord grammar

4-part: **Action + Positional + Scope + Component**

| Part       | Letters |
|------------|---------|
| Action     | c=Change d=Delete r=Replace y=Yank a=Append p=Prepend i=Insert j=Jump l=List |
| Positional | i=Inside e=Entire a=After b=Before n=Next p=Previous u=Until o=Outside t=To l=Last f=First 1-9=Count |
| Scope      | l=Line b=Buffer f=Function v=Variable s=Struct m=Member d=Delimiter |
| Component  | b=Beginning c=Contents e=End v=Value p=Parameters a=Arguments n=Name s=Self w=Word d=Definition |

**Short form**: 4 lowercase chars, e.g. `cels` = ChangeEntireLineSelf. **Long form**: `ChangeEntireLineSelf`.

## Arguments

`chord(target:name_or_line, value:"text", find:"pat", replace:"rep")`

Include only what's needed. Any arg accepts `-` to read from stdin:
```
echo "new body" | ane exec file.rs --chord "cifc(target:main, value:-)"
```

## Reading files (Yank)

Use Yank (`y`) to read file contents to stdout — replaces `cat`, `head`, and builtin reads.

```
ane exec f.rs --chord "yebs"                        # read entire file (use sparingly)
ane exec f.rs --chord "yels(target:5)"              # read line 5
ane exec f.rs --chord "yefc(target:main)"           # read function body
ane exec f.rs --chord "yefs(target:main)"           # read entire function incl. signature
ane exec f.rs --chord "yefn(target:main)"           # read function name only
ane exec f.rs --chord "yefd(target:main)"           # read function signature (no body)
ane exec f.rs --chord "yevs(target:count)"          # read variable declaration
```

## Exploring code (List)

Use List (`l`) to discover symbols — replaces `grep` and builtin search. Output: `line:col  name` per match. **Always list before editing** an unfamiliar file so you know what targets are available.

```
ane exec f.rs --chord "lefd"                        # list all function definitions (signatures)
ane exec f.rs --chord "lefn"                        # list all function names
ane exec f.rs --chord "levd"                        # list all variable definitions
ane exec f.rs --chord "lesd"                        # list all struct definitions
ane exec f.rs --chord "lemd"                        # list all member/field definitions
```

## Editing

```
ane exec f.rs --chord "cels(target:3, value:\"new text\")"       # change line 3
ane exec f.rs --chord "dels(target:5)"                            # delete line 5
echo "x + 1" | ane exec f.rs --chord "civv(target:count, value:-)"    # change variable value
ane exec f.rs --chord "cifn(target:getData, value:\"fetch\")"   # rename function (identifier only)
echo "pub fn fetch(url: &str) -> Result<()>" | ane exec f.rs --chord "cefd(target:getData, value:-)"  # rewrite full signature
```

## Append and Prepend (line scope)

For Line scope, `After` vs `Entire` controls whether a new line is created:

```
# aals — insert on a NEW LINE after the target line
ane exec f.rs --chord "aals(target:10, value:\"new line\")"

# aels — append INLINE at end of the target line (no newline)
ane exec f.rs --chord "aels(target:10, value:\" // comment\")"

# pbls — insert on a NEW LINE before the target line
ane exec f.rs --chord "pbls(target:10, value:\"// above\")"

# pels — prepend INLINE at start of the target line (no newline)
ane exec f.rs --chord "pels(target:10, value:\"/// \")"
```

## Component guide: Name vs Definition

- **`n` (Name)** — bare identifier only. `cifn` renames without touching the signature.
- **`d` (Definition)** — full declaration (visibility + `fn` + name + params + return type), excluding body. `cefd` changes visibility or rewrites the signature. **Do NOT use `cifn` for visibility/signature changes.**

```
ane exec f.rs --chord "cifn(target:foo, value:\"bar\")"           # fn foo() → fn bar() (rename only)
ane exec f.rs --chord "cefd(target:foo, value:\"pub fn foo()\")"  # fn foo() → pub fn foo() (visibility)
```

## Efficiency: use the narrowest scope

**Do not default to `yebs` (read entire file).** Prefer targeted reads and edits:

1. **Discover first**: run `lefd` or `lefn` to find function names/signatures before reading or editing.
2. **Read narrow**: use `yefc(target:fn_name)` to read one function body, or `yels(target:N)` for one line. Only use `yebs` when you genuinely need the whole file.
3. **Edit narrow**: use `cifc(target:fn_name, value:-)` to replace one function body. Avoid `cebs` (replace entire buffer) unless truly rewriting the whole file.
4. **Yank before changing**: run `yefc` to understand what you're replacing before piping new content into `cifc`.

Narrow scopes produce less output, consume fewer tokens, and reduce the risk of unintended changes.

## Notes

- `target:` — line number (0-indexed) for Line scope, symbol name for LSP scopes (Function, Variable, Struct, Member).
- LSP scopes require a language server. Line, Buffer, Delimiter do not.
- Pipe stdin with `value:-` for multiline replacement text.
