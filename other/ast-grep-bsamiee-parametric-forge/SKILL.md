---
name: ast-grep
description: Structural code work on ast-grep — outline maps before reading source, AST search through the MCP tools with inline rules, durable rule folders enforcing project quality, and syntax-tree rewrites. Use when reading, editing, or searching any code/source file, when authoring or organizing a project's ast-grep rules, and when applying structural rewrites.
---

# [AST_GREP]

Structural code work — map, find, prove, lint, or rewrite code by its syntax tree — runs on ast-grep. Read the section owning the task in full and follow its steps before touching a source file. MCP tools own search and rule development; the CLI owns structural maps (`ast-grep outline`), project rule scans (`ast-grep scan`), and applied rewrites.

- `find_code`: pattern search over a path.
- `find_code_by_rule`: inline YAML rule search for structures a bare pattern cannot express.
- `dump_syntax_tree`: node kinds and structure of a snippet — the debugging surface for every non-match.
- `test_match_code_rule`: proves a rule against representative code before it runs anywhere.

Every rule proves through `test_match_code_rule` at omitted or `warning` severity — an `error` diagnostic exits nonzero and the tool discards the JSON, so the shipped severity returns only at landing. Every non-match debugs through `dump_syntax_tree` against the target snippet. Search rules ride inline; durable rules are project rule files discovered through `sgconfig.yml`.

## [01]-[ROUTING]

[TEMPLATES]:
- [01]-[SGCONFIG](assets/templates/sgconfig.template.yml): Project config — six-key surface, snapshot custody, parser overrides, injection rows.
- [02]-[RULE](assets/templates/rule.yml): Lint rule with the full field set and a `---` sibling — the topic-file form every durable rule authors from.
- [03]-[RULE_REWRITE](assets/templates/rule-rewrite.yml): Patch algebra — rewriters, `rewrite()` transform, `joinBy`, the `FixConfig` deletion doc.
- [04]-[UTIL](assets/templates/util.yml): Global utility rule — parameterized `arguments:`, kind guard, call form, local-shadow law.
- [05]-[RULE_TEST](assets/templates/rule-test.yml): Test file — id-bound `valid:`/`invalid:` fixtures; snapshots write via `test -U`.

[EXAMPLES] — proven rules, test files beside them under `rule-tests/`; pick by mechanism and re-shape, never copy whole:
- [01]-[YAML](assets/examples/require-job-timeout.yml): Required shape by depth — relational descent to the owner, direct-child absence chain.
- [02]-[BASH](assets/examples/require-strict-mode.yml): Container-anchored absence — the file is the match, a direct-child `not: has` proves it.
- [03]-[TYPESCRIPT](assets/examples/require-declared-fan-out-degree.yml): Missing option — neighbor-`has` precision no nested callback satisfies.
- [04]-[TYPESCRIPT](assets/examples/enum-to-vocabulary-table.yml): Construct conversion — rewriters fold rows, guards refuse unfixable variants.
- [05]-[CSHARP](assets/examples/deny-forward-referenced-vocabulary-row.yml): Ordering proof — capture unification across `has` and `precedes`.
- [06]-[CSHARP](assets/examples/closed-family-switch-to-generated-switch.yml): Dispatch conversion — context/selector, derived slots, dual guards.
- [07]-[PYTHON](assets/examples/no-raise-in-railed-function.yml): Signature-scoped ban — nearest-enclosing `stopBy` anchors on the return type.
- [08]-[PYTHON](assets/examples/guard-ladder-to-conditional-chain.yml): Statement-to-expression fold — totality closure, parenthesized rungs.

## [02]-[OUTLINE]

`ast-grep outline` maps source structure before any full read or edit: line-numbered top-level items (imports, functions, classes, structs, interfaces, modules, enums — flagged imported/exported) with their direct members (fields, methods, constructors, variants — flagged public). Output is syntax-local — no reference resolution, type inference, re-export chains, or call graphs; those questions route through [03]-[SEARCH] after outline names the files.

Every outline task runs one sequence: resolve target paths from the task, search hits, or `git diff --name-only`; run the owning row; escalate the located symbol with `--match <symbol> --view expanded`; then Read only the printed line range.

| [INDEX] | [TASK]                           | [COMMAND]                                                                     |
| :-----: | :------------------------------- | :---------------------------------------------------------------------------- |
|  [01]   | Map a directory surface          | `ast-grep outline <dir>` — grouped exported names; `--type <t1>,<t2>` narrows |
|  [02]   | Understand a file before editing | `ast-grep outline <file>` — local structure with member digests               |
|  [03]   | List a file's dependencies       | `ast-grep outline <file> --items imports`                                     |
|  [04]   | Find importers of a module       | `ast-grep outline <dir> --items imports --match <module> --view signatures`   |
|  [05]   | Enumerate public entry points    | `ast-grep outline <dir> --items exports --view signatures`                    |
|  [06]   | Zoom into one symbol             | `ast-grep outline <file> --match <symbol> --type <type> --view expanded`      |
|  [07]   | Map structure after edits        | `ast-grep outline $(git diff --name-only HEAD) --items exports`               |
|  [08]   | Outline piped code               | `<producer> \| ast-grep outline --stdin -l <lang>`                            |
|  [09]   | Post-process entries             | `ast-grep outline <path> --json=stream` — one file object per line, jq rails  |

- `--items structure\|exports\|imports\|all` selects top-level entries; defaults key on input — file/stdin `structure`, any directory `exports`.
- `--view names\|signatures\|digest\|expanded` sets detail ascending; defaults key on input — file/stdin `digest`, any directory `names`.
- `--match` is case-sensitive Rust regex over item names, signatures, and first source lines; `--type` filters symbol types; neither reaches members.
- `--pub-members` hides private members; a member without extractable visibility counts as public.
- JSON entries carry `symbolType`, `role`, zero-based `range` with byte offsets, `signature`, `astKind`, and import/export/public flags.
- Uncovered syntax registers extractors via `--outline-rules <file>` or `customLanguages.<name>.outlineRules` in `sgconfig.yml`.

## [03]-[SEARCH]

Structural search runs on the MCP tools; rules ride inline YAML. Patterns are valid code under the language's tree-sitter grammar, carrying whole-node metavariables: `$VAR` one named node, `$$VAR` one unnamed node, `$$$MULTI` lazy zero-or-more, `$_` non-capturing. Smart matching skips unnamed target nodes, so the less a pattern specifies, the more it matches — anchor only what the query fixes.

Every search runs one sequence:
1. Query fits one AST node — `find_code` with the pattern; done.
2. Anything structural — compose the scaffold: anchor the most specific positive rule, refine relationally, filter captures.
3. Unknown node kind — `dump_syntax_tree` on representative target code with `format=cst`; a mis-parsing pattern takes `format=pattern`.
4. Prove with `test_match_code_rule` against one matching and one non-matching snippet; every non-match returns to step 3.
5. Run `find_code_by_rule` with absolute `project_folder` and bounded `max_results`; `output_format=json` when captures or ranges feed the next step.

```yaml template
id: <query-id>
language: <language>
utils:
  <util-id>:                                        # define once, reference via matches; recursion lands through has/inside
    any: [ { kind: <kind-a> }, { kind: <kind-b> } ]
rule:
  all:                                              # explicit all — capture order is law, the defining pattern rides first
    - pattern: <code with $VAR and $$$ARGS>
    - has: { pattern: <sub-pattern>, stopBy: end }  # stopBy picks the axis: neighbor pins depth, end opens it, a rule bounds the walk
    - not: { inside: { kind: <kind>, stopBy: end } }
constraints:
  <VAR>: { regex: '<rust-regex>' }                  # post-rule text filter on one single-node capture
```

- Kind-only structure rides ESQuery in `kind`: `<a> > <b>`, `<a> <b>`, `<a>:has(> <b>)`, `:not(<b>)`, `:is(<a>,<b>)`, `:nth-child(2n+1 of <b>)`.
- `pattern` and `kind` never combine to reparse; a wrong-kind pattern repairs through `pattern: { context: <full-code>, selector: <kind> }`.
- Prefix name hunts capture whole nodes: `$NAME($$$)` with `constraints: NAME: { regex: '^<prefix>' }` — `use$HOOK` is no metavariable.
- `field: <role>` on `has`/`inside` pins same-kind children by parent relation — `field: key` splits an object key from its value.
- Rules anchor on at least one positive field, `pattern` or `kind`; `regex`, `field`, or a negation alone never anchors.
- Capture threading: the first rule naming `$VAR` defines its content, later rules only re-match it — order `all` accordingly.
- `strictness: relaxed` widens past comments and unnamed nodes; `signature` alone drops text — take either only when a proven match is blocked.

## [04]-[REWRITE]

Rewrite extends a proven [03]-[SEARCH] rule with patching fields — each match replaces exactly one target node's text with the instantiated template. Templates are unparsed text: metavariables land anywhere, an undefined metavariable fails the parse under `scan` and lands empty under `run -r`, a declared-but-unmatched one lands empty in both, and `$VARName` lexes as `$VARN` + `ame` — appended text rides a `replace` transform. Multiline templates re-indent relative to the match's column. `run` carries the pattern-only path; the full algebra — `fix`, `FixConfig`, `transform`, `rewriters` — rides `scan --inline-rules`.

Every rewrite runs one sequence:
1. Prove the match set per [03]-[SEARCH] until results are exactly the edit set; `--json` match and file counts bound the blast radius.
2. Attach the owning modality row; derived text lands in `transform`, multi-node edits in `rewriters`.
3. Prove the fix through `test_match_code_rule` — the JSON carries `replacement` and `replacementOffsets`; the replacement must re-parse.
4. Preview the tree diff: `ast-grep scan --inline-rules '<yaml>' <paths>` prints diffs and writes nothing; `--json` stays read-only even with `-U`.
5. Apply with `-U` (`-U` overrides `-i`); nested matches rewrite outer-first, so re-run until zero changes — depth and idempotence prove together.
6. Close with the repository's formatter (`nix fmt -- <target>` here); comments never rewrite — sweep leftovers through [03]-[SEARCH] `regex`.

| [INDEX] | [REWRITE]      | [SHAPE]                                                                                                             |
| :-----: | :------------- | :------------------------------------------------------------------------------------------------------------------ |
|  [01]   | Rename/replace | `ast-grep run -l <lang> -p '<pattern>' -r '<template>' -U <paths>`                                                  |
|  [02]   | Mass removal   | `fix: ''`; a dangling separator dies via `fix: { template: '', expandEnd: { regex: ',' } }`                         |
|  [03]   | Derived names  | `NEW: replace($VAR, replace=<re>, by=<txt>)` or `convert($VAR, toCase=<case>)`; fix takes `$NEW`                    |
|  [04]   | List rewrite   | `rewriters: [{id: <r>, rule: <sub>, fix: <t>}]` + `OUT: rewrite($$$L, rewriters=[<r>], joinBy=<sep>)` + `fix: $OUT` |
|  [05]   | Element filter | rewriter emits survivors — `rule: { pattern: $ARG, not: <dropped-shape> }`, `fix: $ARG`, `joinBy: ', '`             |
|  [06]   | Recursion      | rewriter `transform` names its own id over a strictly smaller `source`; a non-descending self-match overflows       |
|  [07]   | Bundle         | one inline YAML, rules split by `---`; identical-range fix collisions resolve by ascending rule id                  |
|  [08]   | Stream         | `<producer> \| ast-grep scan --inline-rules '<yaml>' --stdin -U` — rewritten source on stdout, disk untouched       |

- `rewriters` is a sequence with load-bearing order: per node the first matching rewriter wins; a consumed subtree never re-matches.
- Rewriter scope seals — metavariables, `transform`, `utils` stay inside their rewriter; cross-reference rides only ids inside `rewrite()`.
- Optional trailing commas take a second pattern variant under `any:`; `joinBy` absent splices in place, present discards unmatched text.
- Risk splits into sibling docs: the guarded rule carries `fix`, the residual carries `severity: error` plus `note` for manual action.
- A capture landing in an operator, member-access, or return position takes parentheses in the template — precedence dies in substitution.
- `run` exits 1 on zero matches and 0 on a hit — inverted against `scan`; shell chains over the two verbs read opposite ways.

## [05]-[RULE_CRAFT]

Rule precision is engineered: each device below is the standing form for its problem, developed per [03]-[SEARCH] and landing unchanged in durable files.

- Anchor every `regex` to the ends its law fixes — matching is unanchored substring search; `Exemption` also matches `NoExemptionHere`.
- Captures unify by default: one `$VAR` across clauses proves sameness, `not:` on a rebound pattern proves difference, `$_VAR` opts out of both.
- `nthChild` takes `ofRule` for nth-of-kind — bare positions count all named siblings; `{position: 1, reverse: true, ofRule}` pins the last arm.
- `$$$` captures take structural guards or a `rewrite` transform; `constraints` on them parses and does nothing.
- `stopBy` axes three ways: default neighbor direct relations, `end` the whole axis, a rule a bounded walk — same-kind stopper pins the nearest owner.
- `field:` binds the final relation and survives `stopBy: end` — callee vs argument, key vs value; field names read off the `dump_syntax_tree` cst.
- `rule:` demands a positive anchor; `constraints:` does not — negative and relational capture guards live there.
- Totality closures (`not: {has: {not: {any: [...]}}}`) need a positive member whitelist in delimiter grammars — unnamed children defeat the negation.
- A totality closure proves the container's children only; an allowed member's own interior — an `elif` arm, a nested body — takes its own arm.
- Constraints run after the whole rule — a capture guard cannot narrow a `not:`; the negation matches everything and the rule dies silent.
- Marker exemptions anchor structurally — a comment `precedes: { kind: <body> }` marks its owner; a mark on a descendant proves nothing.
- Ordering rules bind statement nodes: a bare expression pattern has no statement siblings — wrap `precedes`/`follows` in `context`/`selector`.
- A fix fires behind a guard stack: every unfixable variant — guards, discards, exports, valueless members — is a `not:` arm before the template.
- `expandStart`/`expandEnd` consume exactly one adjacent sibling matching the sub-rule (`stopBy` inert); a sibling-less inner node no-ops silently.
- Metavariables bound anywhere export to `fix`, `message`, and `transform`; `note` interpolates nothing, `labels` take rule/constraints captures only.
- Suppression binds to the match's first or last line, never a middle one; report the tight offender node so the waiver lands beside the defect.
- `strictness: signature` matches shape while keeping capture identity — a duplicate-shape hunt, never a name ban.
- Precision proves empirically before landing: scan a real corpus and count — a rule firing wide of its law is a semantic invariant in disguise.
- Grammar truth beats intuition: `dump_syntax_tree` decides node wrapping and field names; a construct parsing as `ERROR` is unenforceable.

## [06]-[DURABLE_RULES]

Durable rules are project structural law as a scanned gate: `sgconfig.yml` at the root, every YAML under `ruleDirs` a rule. A rule earns admission on three proofs — the violation is provable by node shape alone, no standing gate owns it (linter, analyzer, type checker, compiler, generator diagnostic), and it encodes a project law rather than generic hygiene; a scope-, type-, or cross-file-dependent invariant never becomes a rule. One rule owns a whole violation family through `any:` and `utils:`, splitting only when message or fix diverges; shared deep structure across split rules lands in a parameterized global util carrying an explicit `kind` guard. Every rule is `severity: error` — the scan exits nonzero and blocks.

```text template
sgconfig.yml                     # keys: ruleDirs, utilDirs, testConfigs, languageGlobs, customLanguages, languageInjections
rules/<language>/<area>.yml      # one topic file per law family; rules split by ---; id equals filename, unique project-wide
utils/<util-id>.yml              # global utils: explicit id + language, own constraints; a local utils: block shadows its homonym
rule-tests/<rule-id>-test.yml    # binds by id, never filename; snapshots land beside it in __snapshots__/
```

```yaml template
id: <rule-id>                    # imperative grammar: no-<construct> / require-<shape>
language: <language>
severity: error
files: ['<scope-glob>']          # ignores: carves out sanctioned seams; both relative to sgconfig.yml, never ./-prefixed
utils:
  <util-id>: { <family-shape> }
rule: { <[03] rule> }
constraints: { <VAR>: { regex: '<grammar>' } }
fix: <template>                  # only when the repair is mechanical; [04] algebra applies
message: <one line naming the violated law>
note: <the exact repair — the shape to produce>
labels: { <VAR>: { style: primary, message: '<span fact>' } }   # rule/constraints vars only
```

Every rule lands through one sequence:
1. Derive the candidate from a standing project law; run the three admission proofs — a failed proof ends the candidate.
2. Prove the violating node shape with `dump_syntax_tree` on real violating code; a shape the grammar parses as `ERROR` is unenforceable — stop.
3. Author from the owning `assets/templates/` file; develop the rule per [03]-[SEARCH] and the fix per [04]-[REWRITE], proved both ways.
4. Ship the test file with matching id — conforming cases under `valid:`, violating under `invalid:` — then `ast-grep test -U` writes snapshots.
5. Land the rule in its owning folder; `ast-grep scan --inspect entity` proves registration, `--filter '<rule-id>'` iterates it alone.
6. Gate with `ast-grep scan --no-ignore hidden --error=unused-suppression --error=no-suppress-all`; `test` rides the same gate.

| [INDEX] | [RULE_CLASS]           | [MECHANISM]                                                                                        |
| :-----: | :--------------------- | :------------------------------------------------------------------------------------------------- |
|  [01]   | Banned construct       | construct kinds + `ignores:` on sanctioned seam globs, or `not: { inside: <marker-comment rule> }` |
|  [02]   | Required shape         | owner kind + `not: { has: <required child, argument, or modifier> }`                               |
|  [03]   | Entry-point discipline | declaration-name `regex` over modality-suffix and knob grammars; single-hop forwarders as patterns |
|  [04]   | Layer boundary         | one rule per forbidden edge: import kind + path `regex`, `files:` scoping the consumer stratum     |
|  [05]   | Policy literal         | literal kinds `inside` policy argument and initializer positions — named rows own the values       |
|  [06]   | Dispatch shape         | dispatch kind `inside` a dispatch arm; catch-all arms beside closed-family arms                    |
|  [07]   | Naming grammar         | name-position `regex`: word budget, banned generic suffixes, role-suffix bijection via `not: has`  |

- One unparseable rule or duplicate id aborts the whole scan — inline `---` bundles tolerate both; a draft never sits under `ruleDirs`.
- `sgconfig.yml` accepts unknown keys silently; scoping rides per-rule `files:`/`ignores:` only.
- `language:` is single-valued — similar languages share rules via a `languageGlobs` superset row; embedded languages ride `languageInjections`.
- Suppression is rule-scoped — `ast-grep-ignore: <rule-id>`, next or same line; the two `--error` built-ins keep bare and stale waivers fatal.
- A whole-file rule waives only file-wide: the suppression comment on line 1 over an empty line 2 — a line-scoped comment joins the match.
- `files:` takes no `!` negation (silently inert) — exclusion is an `ignores:` row; a dot-directory scope is dead without `--no-ignore hidden`.
- Green proves nothing three ways: omitted `severity` lands `hint`, `test` passes zero cases, a `files:` rule under `scan -r` scans nothing.
- A rule matching no `invalid:` fixture is dead; `test` never notices a missing test file, so rule-to-test pairing proves outside the gate.
- `metadata:` carries routing facts (owner, decision id) and surfaces only under `--json --include-metadata`.
