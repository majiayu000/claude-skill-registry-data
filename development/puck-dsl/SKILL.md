---
name: puck-dsl
description: "Maps the .puck language: grammar, let/template/for, map/range builtins, puck compile/decompile/lint/format, PUCKnnn errors. Use for any .puck edit or JSON-to-.puck conversion. Shapes: sdf-authoring."
---

# The `.puck` authoring language

`.puck` is the one authoring language behind two document vocabularies:
`puck.world.definition.v1` (`Puck.World.Transpiler`) and `puck.cartridge.v1`
(`Puck.GamingBricks.Transpiler`). Both ride one schema-agnostic core,
[`Puck.Transpiler`](../../../src/Puck.Transpiler/README.md): parser, printer,
lowering, diagnostics, module resolver and unit arithmetic. This skill maps that
core and its CLI loop; what a block means is the vocabulary skill's (see the
routing table). When this file and the code disagree, the code wins and this
file is corrected in the same change.

## Where things live

| Thing | Where |
|---|---|
| Parser, printer, lowering, diagnostics | `src/Puck.Transpiler` (`Parsing/PuckParser*.cs`, `Formatting/PuckPrinter*.cs`, `Lowering/DocumentLowering*.cs` and `DocumentBuiltins.cs`, `Diagnostics/PuckDiagnosticCodes.cs`) |
| World vocabulary, its linter and language server | `src/Puck.World.Transpiler` (`Vocabulary/` describes every construct once; `Validation/PuckLinter*.cs`; `Lsp/`) |
| World compile contract | `src/Puck.World.Transpiler/WorldCompiler.cs`; `WorldDocumentMembers.cs` checks emitted members against `WorldModelShape` and lowers authored pins to canonical document identities |
| Cartridge vocabulary | `src/Puck.GamingBricks.Transpiler` |
| Expression vocabulary (operators, named functions) | `Puck.State.ExpressionOperators`, `Puck.State.ExpressionVocabulary` |
| CLI verbs | `src/Puck.Cli.Worlds` (`Transpiler/`: compile, decompile, lint, lsp, migrate, embed; `Test/`; `Vocabulary/`), `src/Puck.Cli.Format` (format) |
| Shipped sources | the world packages, `worlds/<id>/` (the debug world: `worlds/debug/**/*.puck`, cartridges under `worlds/debug/cartridges/`), `src/Puck.World.Transpiler/Samples/`; the quarantined worlds under `experimental/` are prior art |

A document's `schema:` field selects its vocabulary, never the filename.

## Grammar that bites

- **One spelling per shape, at every depth.** A literal container is always a
  block with no colon (`host { }`, `cameras [ ]`, `variables [ ]`,
  `arrays [ ]`), inside an object literal too
  (`{ name: "lit", pixels ["00000000", "11111111"] }`). A scalar always takes a colon
  (`name: "cursor"`, `initial: 0`). A colon in front of `{` or `[` is
  **PUCK040**, the most common mistake; the fix is to drop the colon. A value
  written as a call or a name keeps its colon even when it produces a
  container: `pixels: map(range(0, 8), row => "00000000")`, `origin: bounds`.
- `let name = expr` is a compile-time constant; `template name(p, q = d) { }` a
  parametric block; `import "name" [as alias]`, `export` and
  `use m as a(args)` compose modules.
- **An import names, never spells a file.** `import "skies"`, not
  `import "skies.puck"` (**PUCK121**). The named file decides what comes in: a
  module library (a source emitting no document) hands over its `let`s and
  templates; anything else is a document the importer composes at load, whose
  own `let`s stay its own. A library importing a document is refused (PUCK017).
  A source of imports alone hands over nothing of its own, so it is a document
  fragment that composes what it imports, not a library (`worlds/standard/standard.puck`).
- **Compile-time `for` generates rows; builtins generate values.**
  `for i in range(0, n) { }` and `for (item, index) in [...] { }` expand at
  compile time, and the document carries the rows they produce. Inside one
  value, use the collection builtins: `range`, `length`, `concat`, `map`,
  `filter`, `reduce`, `distinct`, `sort`, `groupBy`, each taking a lambda
  (`i => 0`). An array of n zeros is `map(range(0, n), i => 0)`; it runs once
  at compile time, the compiled JSON still holds every value, and play-time
  behavior is unchanged. A lambda anywhere else is **PUCK042**; an unevaluable
  call **PUCK041**; a `for` over something not known at compile time
  **PUCK044**.
  `range(start, count)` takes a count: `range(16, 16)` emits 16 through 31.
- **A `for` inside a rule body unrolls into the body.** A loop
  over an n-element array that declares `local $"name{i}" = …` compiles to a
  rule carrying n separate locals, `name0` through `name<n-1>`, each with its
  element substituted as a literal; the document holds no loop. Later
  statements read each local by its resolved name, and each is priced like a
  hand-written local. A `for` reads any compile-time array: a `let`, a
  literal, or a builtin's result.
  World locals precede every gate and effect and evaluate in declaration
  order. A late declaration is refused; move it before the first gate or
  effect to make its pre-effect read explicit.
  A rule has one gate and one decision, so a `when`, `decision` or nested
  `rule` inside a rule-body `for` is **PUCK114**; write the condition in the
  rule's own `when`, or in an `if` inside the loop.
- Units (`s ms min h m cm mm hz % pct deg rad`) convert in the core; a unit on
  a field the vocabulary does not dimension is **PUCK024**, an inadmissible
  unit **PUCK025**.
- Strings: plain `"..."`, interpolated `$"...{expr}..."`, raw `"""..."""`, raw
  interpolated `$"""..."""`. An interpolated string computes a name, key,
  number or text, never an expression (**PUCK112**). Backquote a name the bare
  form cannot carry (`` `seat-1` ``).
- **Hashes have one authored spelling.** Write `hash: auto` for automatic
  hashing, or `hash: "sha256/<64 lowercase hex>"` for a digest. Quoted `"auto"`,
  bare digests and `sha256-64/` pins are refused by name during compilation.
  A null document hash carries no pin: decompilation omits that member, rather
  than inventing an empty digest or an automatic hash.
  Font pins cover the font bytes; canonical document rows (creations, patches, tunes,
  music and tables) pin their canonical document, whose compiled identity is
  still the canonicalizer's digest. The printer restores the authored prefix.
- Generated names use `$` inside a document and `~` in file names
  (`Puck.State.GeneratedName`); an author name using them is **PUCK113**.
- **Control flow is core-parsed; each vocabulary decides what its rule shape
  carries.** The parser accepts `if`/`else`, `repeat`/`break`, call-form gates
  and compound assignment for every vocabulary. A world rule lowers `if`/`else`
  to a conditional effect, but its body is straight-line, so `repeat` and
  `break` have nothing to lower onto (**PUCK037**). The refusal names the
  alternative: a rule already runs once per matching subject, so iterate with
  the rule's `forEach`; a fixed count unrolls with a compile-time `for`, or
  folds into one effect (`x += 3`). A world rule carries `=` (`setState`) and
  `+=` and `-=` (`addState`, negating subtraction's operand). Other compound
  operators lower to `setState` over an expression; a computed destination key
  is evaluated once when that effect runs. A cartridge-only `key(...)` gate in a world is
  **PUCK038**. Cartridge rules admit `if`, `repeat`, `break`, `key(...)` gates
  and compound assignment.
- **A `test`'s `expect` reads one world, or names the document it reads.** A line
  reads the booted world; a block named for a sibling document the world
  references (`garden { bodyState(body, 0, size) == 0.25 }`) is judged in the
  instance a crossing starts there, passes on any tick the claim holds, and fails
  when nothing crossed. An absent body reads every register as 0, so a claim of
  `0` there also claims presence
  ([testing a world](../../../docs/authoring/testing-a-world.md#crossing-into-another-document)).
- Gates (`when`, `if`, `expect`) accept ordinary expressions. Zero and absence
  are false; nonzero numeric values are true. `and` and `or` short-circuit;
  `not` negates truth. They yield Int 0/1 and bind below comparisons. Bitwise
  `&`/`|` bind above comparisons. `compareState(...)` and `compareValue(...)`
  in a source gate are refused by name; write a comparison such as `left == right`.
- **One bracket rule.** `row.key` names a literal key; `row[expression]`
  evaluates. Names in brackets resolve lexically, so an unknown bare word is
  an error. Use `row["key"]` for a quoted literal key. Read a local as `name`,
  never `local(name)`; use `row[x]`, never `row[(x)]` or `row[slot[$value]]`.
  Functions are recognized only in call position, so a local may be named `sign`.

[references/grammar.md](references/grammar.md) has the full grammar with
examples; [references/diagnostics.md](references/diagnostics.md) the codes
authors hit most. `PuckDiagnosticCodes.cs` declares every code once, with its
meaning as the XML doc comment.

## Authoring a console command

The owner's ruling: a console command composed from existing verbs is authored
in a world document, never as C# work. A `commands` row lowers through the
generic value path (no sugar); its full contract is
[document-authored commands](../../../docs/reference/commands.md#document-authored-commands):

```text
commands [
  {
    name: "gallery.show"                  // namespaced; never an engine verb's name
    help: "Stands a body at the gallery and picks a layout."
    parameters [
      { name: "layout", kind: Choice, values ["play", "front"], default: "play" }
      { name: "body", kind: Body, default: "0" }  // a default is written as typed
    ]
    lines [
      "body.pose spawn:gallery {body}"    // {name} substitutes; {{ and }} are literal braces
      "view.override layout {layout}"
    ]
  }
]
```

- Kinds: `Text` (default), `Number`, `Integer`, `Choice` (`values`), `Body`
  (0..4095), `Spawn` (a `spawnPoints` id). Arguments are positional plain
  tokens; required parameters come first; every parameter appears in a line.
- A line's first token (the verb) is literal; it may be another authored
  command (no loops) or any verb a binding may name. Operator verbs,
  unbindable verbs (`quit`, `world.save`, `storage.*`), engine-verb names and
  verbs no boot shape registers are refused by `puck compile --validate`
  (against the catalog `puck verbs` generates) and again when the World
  validates the document (boot, `world.reload`). A rendered-only verb
  (`world.debug-view`, `world.slice`) is fine in a line: a headless boot
  admits it and refuses only that line when it runs ("not available in this
  host"). Regenerate the catalog with `puck verbs` after adding or changing a
  verb.
- `commands` is keyed by `name`, so each imported document authors its own
  rows. Bind one like any verb (`command: "debug.go", text: "chess"`), or run
  `run <name> [args]`. Verify by booting the world: `help --names <prefix>`
  lists it, and the command answers its lines' output.

## The verbs

```text
puck format <file> --check
puck lint <file> --strict
puck compile <file> --validate        # writes <source>.world.json (and its .puckb) or <source>.cartridge.json
puck test <path-or-dir>               # boots each test block headless, one verdict a line
```

- Compilation refuses unknown document members by name, including members
  supplied through templates and bound objects. Converter-owned values retain
  their own shape rules, and reserved document extension keys remain data.
  `puck compile --validate` additionally runs the engine's semantic validation.
  `--output` names the destination; a world source declaring `world` entries
  writes one document per declaration and reads `--output` as a directory.
  A world document also gets its compiled world (`.puckb`) beside it.
  `--watch` recompiles on change; `--tree` mirrors a directory of sources.
- `puck decompile` is **one-way**: `let`, `template` and `for` never come back.
  Decompile once to import one hand-written JSON document, then edit the
  `.puck`. A row a `ground`, `test`, `border`, `door` or aliased `use`
  generated is refused by name: those are written in source, never printed
  from a document (decision P1).
- `puck format` prints `.puck` through `PuckPrinter` (two-space indent, lines
  broken past 120 columns, no options); the language server and `puck
  decompile` print through the same printer. Formatting is a fixed point and
  never moves a compiled document; reformat sources after a printer change.
- `puck lsp` serves completion, hover, symbols, formatting and diagnostics.
- `puck migrate <name> <path> [--check]` applies one registered source rewrite
  and proves each rewritten source compiles to the document it did before.
  A syntax migration must also visit retained write-target operands
  (`RowRefNode.Operand`), including keys nested inside them. Compile the
  composed entry document after migrating modules: isolated module checks can
  miss a literal key accidentally resolving to another module's row.
- `puck embed <path>` resolves authored `embed(...)` text into committed
  `.embeddings.json` lock files.
- `puck vocabulary [--check]` regenerates the world vocabulary page.

**Source and generated documents.** The owner's ruling treats cartridge JSON
twins as derived caches, never committed or byte-compared against a saved copy.
Compile the authored sources when needed; semantic round trips compare fresh
compilations. Imported modules contribute templates, not standalone documents.
A world source also has no committed document: the build compiles it. `--world foo.puck` boots straight from source,
`world.reload` recompiles it, and `world.save` writes each live edit into the
source that authors it, an import's row in the import and a value read from a
`let` in that `let`, keeping everything else as written; generated rows refuse
by name, and simulation `state` stays as authored.

After editing a world, run it (`dotnet run --project src/Puck.World -c Release
-- --world worlds/debug --devices none --exit-after-seconds 2`); verify a cartridge in a world (`rom-forge`).

## Route adjacent work

| Skill | Route there for |
|---|---|
| `puck-world` | World-document sugar (`rule`/`decision`/effects, `forEach`), section rules, world refusals, booting `--world`. |
| `sdf-authoring` | Creation shapes, materials and rigs in `.puck`. |
| `rom-forge` | The cartridge vocabulary and the compile/`forge.play` loop. |
| `gaming-bricks` | Emulator behavior once a cartridge is compiled. |
| `symbol-analysis`, `content-search` | C# semantics and text search; `.puck` name resolution goes through `puck lint` or the language server. |
