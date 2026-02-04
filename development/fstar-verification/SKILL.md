---
name: fstar-verification
description: Comprehensive F* proof-oriented programming for formal verification including dependent types, refinement types, effect system, SMT solver integration, tactic-based interactive theorem proving, and verified code extraction to OCaml, F#, C, WebAssembly, and Assembly
---

# F* Formal Verification and Proof-Oriented Programming

A comprehensive skill for building verified software using F* (F-star), a proof-oriented functional programming language with dependent types, refinement types, monadic effects, and SMT-backed automated verification.

## When to Use This Skill

Use this skill when:

- Building security-critical systems requiring formal verification
- Developing cryptographic libraries and protocols (like HACL*)
- Creating verified low-level systems code with memory safety guarantees
- Implementing network protocols with correctness proofs (like TLS)
- Writing parsers with verified security properties
- Building concurrent and distributed systems with proven correctness
- Extracting verified code to production languages (C, OCaml, F#, WASM)
- Proving correctness properties of algorithms and data structures
- Developing software with strong guarantees about functional correctness
- Creating formally verified implementations from specifications
- Working on projects where bugs are extremely costly (aerospace, medical, financial)
- Learning formal methods and theorem proving with practical applications

## Core Concepts

### F* Philosophy

F* combines three paradigms:

1. **Programming Language**: General-purpose functional language with ML-like syntax
2. **Proof Assistant**: Dependent types for expressing and proving specifications
3. **Verification Tool**: SMT solver integration for automatic proof discharge

Key principles:

- **Propositions as Types**: Specifications are types, proofs are programs
- **Curry-Howard Correspondence**: Programs are proofs, types are propositions
- **Effect Tracking**: Fine-grained tracking of side effects through types
- **Refinement Types**: Precise specifications using logical predicates
- **Weakest Preconditions**: Verification condition generation via WP calculus
- **Proof Automation**: Z3 SMT solver for automatic verification
- **Interactive Proving**: Tactics for manual proof construction when automation fails
- **Code Extraction**: Compile verified code to efficient executables

### The F* Workflow

```
1. Write Specification (as types)
   ↓
2. Write Implementation (as terms)
   ↓
3. F* Generates Verification Conditions (VCs)
   ↓
4. Z3 SMT Solver Attempts Automatic Proof
   ↓
   ├─ Success → Verified!
   └─ Failure → Write explicit proof using tactics
      ↓
      Verified!
   ↓
5. Extract to Target Language
```

### Key Features

**Type System:**
- Dependent function types: `(x:t1) -> t2 x`
- Refinement types: `x:int{x > 0}`
- Universe polymorphism
- Higher-order functions
- Polymorphic types
- Inductive datatypes
- Indexed types

**Effect System:**
- Pure computations: `Tot`
- Divergent computations: `Dv`
- State: `ST`, `STATE`
- Exceptions: `Exn`, `EXN`
- General monadic effects
- Custom effect definitions
- Effect polymorphism

**Verification:**
- SMT-based automation via Z3
- Tactic-based interactive proving
- Metaprogramming for custom automation
- Lemmas with patterns for reusable proofs
- Quantifier instantiation control

**Extraction:**
- OCaml (default)
- F# (.NET integration)
- C (via KaRaMeL for low-level code)
- WebAssembly
- Assembly (via Vale)

## Type System

### Dependent Types

Dependent types allow types to depend on values, enabling precise specifications.

**Dependent Function Types:**

```fstar
// Type depends on value
val replicate: n:nat -> a:Type -> Tot (list a)

// More precise: result list has exactly n elements
val replicate_precise: n:nat -> a:Type -> Tot (l:list a{length l = n})

// Function type depends on first argument
val nth: #a:Type -> l:list a -> n:nat{n < length l} -> Tot a
```

**Dependent Pairs (Sigma Types):**

```fstar
// Dependent pair: second component type depends on first
type dtuple2 (a:Type) (b:(a -> Type)) =
  | Mkdtuple2: _1:a -> _2:(b _1) -> dtuple2 a b

// Example: a number paired with proof it's positive
type positive_with_proof = dtuple2 int (fun x -> squash (x > 0))
```

### Refinement Types

Refinement types are types qualified by logical predicates, expressed as subset types.

**Basic Refinement Types:**

```fstar
// Natural numbers
type nat = x:int{x >= 0}

// Positive integers
type pos = x:int{x > 0}

// Non-empty lists
type non_empty_list (a:Type) = l:list a{length l > 0}

// Sorted lists
type sorted_list = l:list int{is_sorted l}

// Bounded values
type byte = x:int{0 <= x && x < 256}

// Even numbers
type even = x:int{x % 2 = 0}
```

**Refinement with Functions:**

```fstar
// Division requires non-zero divisor
val div: x:int -> y:int{y <> 0} -> Tot int

// Array access requires valid index
val index: #a:Type -> arr:array a -> i:nat{i < length arr} -> Tot a

// Safe head requires non-empty list
val head: #a:Type -> l:list a{length l > 0} -> Tot a
```

**Complex Refinements:**

```fstar
// Binary search tree property
type bst (a:Type) =
  t:tree a{forall (x:a). mem x t ==> valid_bst_node t x}

// Balanced tree
type balanced_tree (a:Type) =
  t:tree a{abs (height (left t) - height (right t)) <= 1}

// Valid email address
type email = s:string{is_valid_email s}
```

### Universe Polymorphism

F* supports universe polymorphism for generic definitions.

```fstar
// Polymorphic identity function
val id: #a:Type -> a -> Tot a
let id #a x = x

// Polymorphic list operations
val map: #a:Type -> #b:Type -> f:(a -> Tot b) -> list a -> Tot (list b)

// Universe polymorphic (works at any universe level)
val compose: #a:Type -> #b:Type -> #c:Type ->
  f:(b -> Tot c) -> g:(a -> Tot b) -> a -> Tot c
let compose #a #b #c f g x = f (g x)
```

## Effect System

F* tracks computational effects through types, ensuring pure computations are separated from effectful ones.

### Pure Computations (Tot)

```fstar
// Total function: always terminates, no effects
val factorial: nat -> Tot nat
let rec factorial n =
  if n = 0 then 1 else n * factorial (n - 1)

// Pure computation with precondition
val safe_div: x:int -> y:int{y <> 0} -> Tot int
let safe_div x y = x / y
```

### Potentially Divergent Computations (Dv)

```fstar
// May not terminate
val ackermann: nat -> nat -> Dv nat
let rec ackermann m n =
  if m = 0 then n + 1
  else if n = 0 then ackermann (m - 1) 1
  else ackermann (m - 1) (ackermann m (n - 1))
```

### Stateful Computations (ST)

```fstar
// State monad for mutable references
val increment_ref: r:ref int -> ST unit
  (requires (fun h -> True))
  (ensures (fun h0 _ h1 -> sel h1 r = sel h0 r + 1))
let increment_ref r = r := !r + 1

// Reading mutable state
val read_and_double: r:ref int -> ST int
  (requires (fun h -> True))
  (ensures (fun h0 result h1 -> result = 2 * sel h0 r /\ h0 == h1))
let read_and_double r = 2 * !r
```

### Effect Polymorphism

```fstar
// Function polymorphic in effect
val apply: #a:Type -> #b:Type -> #eff:_ ->
  f:(a -> eff b) -> x:a -> eff b
let apply #a #b #eff f x = f x

// Works with any effect
let pure_example = apply (fun x -> x + 1) 5
let state_example r = apply increment_ref r
```

### Custom Effects

```fstar
// Define custom effect as monad
effect IO (a:Type) = unit -> Dv a

// Exception effect
effect EXN (a:Type) (pre:pure_pre) (post:pure_post a) =
  EXN a (fun p -> pre /\ (forall x. post x ==> p (V x)))

// Reader monad effect
effect Reader (env:Type) (a:Type) = env -> Tot a
```

## Verification Patterns

### Preconditions and Postconditions

```fstar
// Precondition: input validation
val sqrt: x:float{x >= 0.0} -> Tot float

// Postcondition: output property
val abs: x:int -> Tot (r:int{r >= 0})
let abs x = if x >= 0 then x else -x

// Both pre and post conditions
val find: #a:Type -> f:(a -> bool) -> l:list a ->
  Tot (option (x:a{f x && mem x l}))
```

### Invariants

```fstar
// Loop invariant example
val sum_n: n:nat -> Tot (r:nat{r = n * (n + 1) / 2})
let rec sum_n n =
  if n = 0 then 0
  else n + sum_n (n - 1)

// Invariant on data structure
type stack (a:Type) = {
  elems: list a;
  size: nat;
  invariant: size = length elems
}

// Maintaining invariant
val push: #a:Type -> s:stack a -> x:a ->
  Tot (s':stack a{s'.size = s.size + 1})
let push #a s x = {
  elems = x :: s.elems;
  size = s.size + 1;
  invariant = ()  // F* proves this automatically
}
```

### Lemmas

Lemmas are functions that prove properties, typically returning unit with important postconditions.

```fstar
// Simple lemma
val length_append: #a:Type -> l1:list a -> l2:list a ->
  Lemma (length (l1 @ l2) = length l1 + length l2)
let rec length_append #a l1 l2 =
  match l1 with
  | [] -> ()
  | _ :: tl -> length_append tl l2

// Lemma with pattern for automatic instantiation
val mem_append: #a:Type -> x:a -> l1:list a -> l2:list a ->
  Lemma (requires True)
        (ensures (mem x (l1 @ l2) <==> (mem x l1 \/ mem x l2)))
        [SMTPat (mem x (l1 @ l2))]
let rec mem_append #a x l1 l2 =
  match l1 with
  | [] -> ()
  | hd :: tl -> mem_append x tl l2

// Inductive lemma
val sorted_tail: l:list int ->
  Lemma (requires (is_sorted l /\ length l > 0))
        (ensures (is_sorted (tail l)))
let rec sorted_tail l =
  match l with
  | [x] -> ()
  | x :: y :: tl -> sorted_tail (y :: tl)
```

### Ghost Code

Ghost code is used only for verification and erased during extraction.

```fstar
// Ghost parameter (erased in extracted code)
val binary_search: #a:Type -> arr:array a -> x:a ->
  Ghost (option nat)
    (requires (sorted arr))
    (ensures (fun r ->
      match r with
      | Some i -> index arr i = x
      | None -> forall (i:nat{i < length arr}). index arr i <> x))

// Ghost computations for specifications
let ghost compute_invariant (s:state) : GTot bool =
  all_valid s.items && s.count = length s.items
```

## SMT Solver Integration

F* uses the Z3 SMT solver for automated verification.

### Automatic Verification

```fstar
// Z3 proves these automatically
val example1: x:int -> y:int ->
  Lemma (x + y = y + x)
let example1 x y = ()

val example2: x:int -> y:int -> z:int ->
  Lemma ((x + y) + z = x + (y + z))
let example2 x y z = ()

val example3: x:int{x >= 0} -> y:int{y >= 0} ->
  Lemma (x + y >= 0)
let example3 x y = ()
```

### SMT Patterns for Quantifiers

Control when the SMT solver instantiates quantified formulas.

```fstar
// Without pattern: may not be instantiated
val lemma_no_pattern: #a:Type -> x:a -> l:list a ->
  Lemma (mem x (x :: l))

// With pattern: instantiated when pattern matched
val lemma_with_pattern: #a:Type -> x:a -> l:list a ->
  Lemma (mem x (x :: l))
  [SMTPat (mem x (x :: l))]

// Multiple patterns
val distributivity: #a:Type -> x:a -> l1:list a -> l2:list a ->
  Lemma (mem x l1 \/ mem x l2 <==> mem x (l1 @ l2))
  [SMTPat (mem x l1); SMTPat (mem x l2)]
```

### Controlling SMT with Attributes

```fstar
// Increase SMT timeout for complex proofs
[@ expect_failure]  // Document expected failure
val hard_theorem: x:int -> Lemma (complex_property x)

// Fuel for recursive function unfolding
[@ fuel 5]  // Allow 5 levels of unfolding
val recursive_property: n:nat -> Lemma (property n)

// Opaque definitions (not unfolded by SMT)
[@ opaque_to_smt]
val expensive_function: int -> int
```

### SMT Query Optimization

```fstar
// Split complex proofs
val complex_theorem: x:int -> y:int -> z:int ->
  Lemma (complex_property x y z)
let complex_theorem x y z =
  // Prove intermediate facts
  assert (fact1 x y);
  assert (fact2 y z);
  assert (fact3 x z);
  // SMT combines them for final proof
  ()

// Provide intermediate assertions
val theorem_with_hints: l:list int ->
  Lemma (requires (sorted l))
        (ensures (property l))
let theorem_with_hints l =
  // Hint for SMT
  assert (forall i j. i < j /\ i < length l /\ j < length l ==>
    index l i <= index l j);
  ()  // SMT completes proof
```

## Proof Techniques

### Automated Proofs

Many properties are proven automatically by Z3.

```fstar
// Arithmetic properties
val arithmetic_auto: x:int -> y:int ->
  Lemma (x * (y + 1) = x * y + x)
let arithmetic_auto x y = ()

// List properties with lemmas
val reverse_reverse: #a:Type -> l:list a ->
  Lemma (reverse (reverse l) = l)
let rec reverse_reverse #a l =
  match l with
  | [] -> ()
  | hd :: tl ->
    reverse_reverse tl;
    reverse_append [hd] (reverse tl)
```

### Manual Proofs with Tactics

When automation fails, use tactics for interactive proving.

```fstar
// Import tactics library
open FStar.Tactics

// Manual proof using tactics
val manual_theorem: x:int -> y:int ->
  Lemma (x + y = y + x)
let manual_theorem x y =
  assert_by_tactic (x + y = y + x) (fun () ->
    // Simplify both sides
    norm [delta];
    // Apply commutativity
    trefl())

// More complex tactic proof
val complex_proof: n:nat ->
  Lemma (requires (n > 10))
        (ensures (n * 2 > 15))
let complex_proof n =
  assert_by_tactic (n * 2 > 15) (fun () ->
    // Split into cases
    split();
    // Case 1: n > 10
    smt();
    // Arithmetic reasoning
    arith())
```

### Common Tactics

```fstar
// intro: introduce hypothesis or variable
// split: split conjunction into multiple goals
// smt: call SMT solver on current goal
// trefl: prove by reflexivity
// rewrite: rewrite using equation
// apply: apply lemma or function
// dump: print current proof state
// norm: normalize terms
// pose: add intermediate assertion
```

### Metaprogramming for Custom Automation

```fstar
open FStar.Tactics

// Custom tactic
let rec auto_induction () : Tac unit =
  match cur_goal () with
  | Implies _ _ ->
    intro();
    auto_induction()
  | Forall _ _ ->
    intro();
    auto_induction()
  | _ ->
    try induction (quote (cur_goal()))
    with _ -> smt()

// Use custom tactic
val my_theorem: l:list int ->
  Lemma (length (reverse l) = length l)
let my_theorem l =
  assert_by_tactic (length (reverse l) = length l)
    auto_induction
```

## Code Extraction

### Extraction to OCaml

Default extraction target, generates idiomatic OCaml.

```fstar
// F* code
val fibonacci: nat -> Tot nat
let rec fibonacci n =
  if n <= 1 then n
  else fibonacci (n - 1) + fibonacci (n - 2)

// Extracted OCaml (simplified):
// let rec fibonacci n =
//   if n <= 1 then n
//   else fibonacci (n - 1) + fibonacci (n - 2)
```

**Compilation:**

```bash
fstar --codegen OCaml MyModule.fst
ocamlopt -o program MyModule.ml
```

### Extraction to F#

For .NET integration.

```bash
fstar --codegen FSharp MyModule.fst
```

### Extraction to C (Low*)

For high-performance systems code using Low* subset.

```fstar
module LowLevel

// Low* uses stack allocation
open FStar.HyperStack.ST
module B = LowStar.Buffer

// Stack-allocated buffer
val process_buffer: len:UInt32.t ->
  Stack unit
    (requires (fun h -> True))
    (ensures (fun h0 _ h1 -> True))
let process_buffer len =
  push_frame();
  let buf = B.alloca 0uy len in
  // ... process buffer ...
  pop_frame()
```

**Extract to C via KaRaMeL:**

```bash
fstar --codegen krml MyModule.fst
krml MyModule.krml -o program
```

### Extraction Configuration

```fstar
// Mark as noextract (specification only)
[@ noextract]
val ghost_function: int -> GTot int

// Inline in extracted code
[@ inline_let]
let constant = 42

// Control extraction names
[@ rename "my_function"]
val f: int -> int
```

## Real-World Applications

### HACL* - Verified Cryptographic Library

HACL* is a formally verified cryptographic library extracted to C.

**Example - Verified Chacha20:**

```fstar
module Chacha20

// Chacha20 state
type state = b:buffer UInt32.t{length b = 16}

// Quarter round operation
val quarter_round:
  st:state -> a:nat -> b:nat -> c:nat -> d:nat ->
  Stack unit
    (requires (fun h -> live h st /\
      a < 16 /\ b < 16 /\ c < 16 /\ d < 16))
    (ensures (fun h0 _ h1 -> live h1 st /\ modifies_1 st h0 h1))

// Chacha20 block function
val chacha20_block:
  output:buffer UInt8.t ->
  key:buffer UInt8.t{length key = 32} ->
  nonce:buffer UInt8.t{length nonce = 12} ->
  counter:UInt32.t ->
  Stack unit
    (requires (fun h ->
      live h output /\ live h key /\ live h nonce /\
      length output = 64 /\ disjoint output key /\ disjoint output nonce))
    (ensures (fun h0 _ h1 ->
      live h1 output /\ modifies_1 output h0 h1))
```

### Project Everest - Verified TLS

Complete verified implementation of TLS 1.2 and 1.3.

```fstar
// Simplified TLS handshake verification
val handshake:
  config:config_t ->
  conn:connection ->
  ST (result connection)
    (requires (fun h -> valid_config config /\ valid_connection h conn))
    (ensures (fun h0 r h1 ->
      match r with
      | Success conn' ->
        secure_connection h1 conn' /\
        derives_keys conn'.keys config.params
      | Failure _ -> True))
```

### EverParse - Verified Parser Combinator

Generate verified parsers from format specifications.

```fstar
// Message format specification
type message = {
  header: UInt32.t;
  length: n:UInt16.t;
  payload: b:bytes{length b = n};
  checksum: UInt32.t
}

// Verified parser generated automatically
val parse_message: parser message
```

## Tooling and Setup

### Installation

**Via OPAM:**

```bash
opam install fstar
```

**Via Binary Release:**

```bash
# Download from https://github.com/FStarLang/FStar/releases
export FSTAR_HOME=/path/to/fstar
export PATH=$FSTAR_HOME/bin:$PATH
```

**Via Docker:**

```bash
docker pull fstarlang/fstar-emacs
docker run -it fstarlang/fstar-emacs
```

**Build from Source:**

```bash
git clone https://github.com/FStarLang/FStar.git
cd FStar
make
```

### Editor Support

**VS Code:**

Install the F* extension for interactive verification.

```json
{
  "fstar.executable": "fstar.exe",
  "fstar.flyCheck": true,
  "fstar.verifyOnOpen": true
}
```

**Emacs:**

```elisp
;; Install fstar-mode.el
(load "fstar-mode.el")
(setq fstar-executable "fstar.exe")
(setq fstar-smt-executable "z3")
```

**Vim:**

Use fstar-mode.vim for syntax highlighting and verification.

### Build System

**Using Make:**

```makefile
FSTAR = fstar
FSTAR_FLAGS = --cache_checked_modules

%.checked: %.fst
	$(FSTAR) $(FSTAR_FLAGS) $<

all: Module1.checked Module2.checked Module3.checked

clean:
	rm -f *.checked
```

**Using F* Include Directories:**

```bash
fstar --include /path/to/lib MyModule.fst
```

## Common Patterns

### Pattern: Verified Data Structure

```fstar
// Verified stack with invariants
module Stack

type stack (a:Type) = {
  items: list a;
  size: nat;
  inv: size = length items
}

val empty: #a:Type -> stack a
let empty #a = {items = []; size = 0; inv = ()}

val push: #a:Type -> s:stack a -> x:a ->
  Tot (s':stack a{s'.size = s.size + 1})
let push #a s x = {
  items = x :: s.items;
  size = s.size + 1;
  inv = ()
}

val pop: #a:Type -> s:stack a{s.size > 0} ->
  Tot (a * stack a)
let pop #a s =
  match s.items with
  | hd :: tl -> hd, {items = tl; size = s.size - 1; inv = ()}
```

### Pattern: Verified Algorithm

```fstar
// Binary search with correctness proof
val binary_search:
  arr:array int{sorted arr} ->
  x:int ->
  Tot (r:option nat{
    match r with
    | Some i -> i < length arr /\ index arr i = x
    | None -> forall (i:nat{i < length arr}). index arr i <> x
  })

let rec binary_search arr x =
  if length arr = 0 then None
  else
    let mid = length arr / 2 in
    let mid_val = index arr mid in
    if x = mid_val then Some mid
    else if x < mid_val then
      binary_search (slice arr 0 mid) x
    else
      match binary_search (slice arr (mid + 1) (length arr)) x with
      | Some i -> Some (mid + 1 + i)
      | None -> None
```

### Pattern: Stateful Computation with Proof

```fstar
// Stateful counter with proof of increment
val counter: Type0
val new_counter: unit -> ST counter
  (requires (fun _ -> True))
  (ensures (fun h0 c h1 -> value h1 c = 0))

val increment: c:counter -> ST unit
  (requires (fun h -> True))
  (ensures (fun h0 _ h1 -> value h1 c = value h0 c + 1))

val get: c:counter -> ST nat
  (requires (fun h -> True))
  (ensures (fun h0 r h1 -> r = value h0 c /\ h0 == h1))
```

### Pattern: Effect Encapsulation

```fstar
// Pure interface for effectful implementation
val compute_result: input:int -> Tot (r:int{r >= 0})

// Implementation uses state internally
let compute_result input =
  let r = ST.alloc 0 in
  run_stateful (fun () ->
    // ... complex stateful computation ...
    !r
  )
```

## Best Practices

### Specification Design

1. **Start with Types**: Design type signatures before implementation
2. **Progressive Refinement**: Begin with simple types, add refinements incrementally
3. **Separation of Concerns**: Keep specification separate from proof when complex
4. **Reusable Specifications**: Extract common patterns into abstract predicates
5. **Document Invariants**: Make invariants explicit in types and comments

### Proof Organization

1. **Modular Proofs**: Break complex proofs into lemmas
2. **Automated First**: Let Z3 handle what it can, manual proofs for the rest
3. **Lemma Libraries**: Build reusable lemma collections
4. **Pattern Annotations**: Add SMTPat for automatic lemma application
5. **Proof Scripts**: Use tactics for repeatable proof patterns

### Performance Optimization

1. **SMT Timeout Management**: Set appropriate timeouts for complex proofs
2. **Fuel Control**: Limit recursive unfolding depth
3. **Opaque Definitions**: Hide complex definitions from SMT
4. **Quantifier Patterns**: Careful pattern design prevents trigger loops
5. **Proof Splitting**: Break large VCs into smaller independent ones

### Code Extraction

1. **Extraction Testing**: Test extracted code thoroughly
2. **Low* for Performance**: Use Low* subset for C extraction
3. **NoExtract Annotations**: Mark ghost code explicitly
4. **Interface Stability**: Maintain stable extraction interfaces
5. **Platform Testing**: Test extracted code on target platforms

### Development Workflow

1. **Incremental Verification**: Verify modules as you develop
2. **Type-Driven Development**: Let types guide implementation
3. **Test Specifications**: Write tests even for verified code
4. **Continuous Integration**: Automate verification in CI/CD
5. **Version Hints**: Cache verification results for faster builds

## Quick Reference

### Common Type Patterns

```fstar
// Refinement type
x:t{p x}

// Dependent function
(x:t1) -> t2 x

// Pure computation
Tot t

// Stateful computation
ST t (requires pre) (ensures post)

// Lemma
Lemma (requires pre) (ensures post) [SMTPat (...)]

// Ghost computation
GTot t
```

### Common Attributes

```fstar
[@ expect_failure]        // Document expected failure
[@ fuel n]                // Control recursive unfolding
[@ inline_let]            // Inline in extraction
[@ noextract]             // Don't extract (ghost)
[@ opaque_to_smt]         // Hide from SMT
[@ rename "name"]         // Control extraction name
```

### Verification Commands

```bash
# Type check only
fstar MyModule.fst

# Verify and cache
fstar --cache_checked_modules MyModule.fst

# Extract to OCaml
fstar --codegen OCaml MyModule.fst

# Increase SMT timeout
fstar --z3rlimit 100 MyModule.fst

# Print statistics
fstar --print_stats MyModule.fst
```

## Learning Resources

### Official Documentation

- Proof-Oriented Programming in F*: https://fstar-lang.org/tutorial/
- F* Tutorial: https://fstar-lang.org/tutorial/tutorial.html
- Low* Tutorial: https://fstarlang.github.io/lowstar/html/
- API Documentation: https://fstarlang.github.io/docs/

### Example Repositories

- HACL*: https://github.com/project-everest/hacl-star
- Project Everest: https://github.com/project-everest
- F* Examples: https://github.com/FStarLang/FStar/tree/master/examples
- F* Tutorial Examples: https://github.com/FStarLang/FStar/tree/master/doc/tutorial

### Academic Papers

- "Dependent Types and Multi-Monadic Effects in F*" (POPL 2016)
- "Meta-F*: Proof Automation with SMT, Tactics, and Metaprograms" (ESOP 2019)
- "Verified Low-Level Programming Embedded in F*" (ICFP 2017)

### Community Resources

- F* Mailing List: fstar-club@lists.gforge.inria.fr
- GitHub Discussions: https://github.com/FStarLang/FStar/discussions
- Zulip Chat: https://fstar.zulipchat.com/

---

**Skill Version**: 1.0.0
**Last Updated**: November 2025
**Skill Category**: Formal Verification, Theorem Proving, Dependent Types, Systems Programming
**Compatible With**: Z3 SMT Solver, OCaml, F#, C (via KaRaMeL), WebAssembly
