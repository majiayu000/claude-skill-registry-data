---
name: geb
description: 'Anoma''s Geb: Categorical semantics via S-expressions, polynomial functors
  → Vampir ZK circuits'
source: anoma/geb (Common Lisp + Idris2)
license: MIT
trit: 1
gf3_conserved: true
repo_divergence: HIGH (DeepWiki shows Yoneda/bicartesian but repo is geb.lisp morphisms)
last_commit: 2024-02-07 (v0.6.1)
metadata:
  interface_ports:
  - Related Skills
  - GF(3) Triads
  - Integration with
---
# Geb (+1)

> Categorical computation via S-expressions. Compile categories to ZK circuits.

**Trit**: +1 (PLUS - generative categorical semantics)
**Language**: Common Lisp (core), Idris2 (verified)
**Target**: Vampir IR → ZK proofs

## DeepWiki vs Repo Divergence Analysis

| DeepWiki Claims | Actual Repo State | Divergence |
|-----------------|-------------------|------------|
| "Yoneda Categories" | Not prominent in src/ | HIGH |
| "Bicartesian Categories" | ✓ `coprod`, `prod` in geb.lisp | LOW |
| "Polynomial Functors" | ✓ `src/poly/poly.lisp` full impl | LOW |
| "Simply Typed Lambda" | ✓ `src/lambda/` exists | LOW |
| "Vampir IR Generation" | ✓ `src/vampir/` exists | LOW |

**Key Finding**: Core is `src/geb/geb.lisp` with morphism algebra, not abstract Yoneda.

## Core Architecture (from geb.lisp)

```lisp
;; Substrate objects (types)
so0          ; Initial object (void)
so1          ; Terminal object (unit)
(coprod x y) ; Coproduct (sum type)
(prod x y)   ; Product (pair type)

;; Substrate morphisms
(init obj)           ; 0 → A
(terminal obj)       ; A → 1
(inject-left a b)    ; A → A+B
(inject-right a b)   ; B → A+B
(project-left a b)   ; A×B → A
(project-right a b)  ; A×B → B
(comp f g)           ; g;f composition
(pair f g)           ; ⟨f,g⟩ : A → B×C
(case f g)           ; [f,g] : A+B → C
(distribute a b c)   ; A×(B+C) → (A×B)+(A×C)
```

## Polynomial Functors (poly.lisp)

```lisp
;; Polynomial operations on ℕ
poly:ident     ; identity polynomial P(x) = x
poly:compose   ; P ∘ Q
poly:+         ; P + Q
poly:*         ; P × Q
poly:/         ; P ÷ Q (integer division)
poly:-         ; P - Q
poly:mod       ; P mod Q
poly:if-zero   ; conditional on zero
poly:if-lt     ; conditional on less-than

;; Evaluation (gapply = generic apply)
(gapply (+ ident ident) 5)  ; → 10
(gapply (* ident ident) 5)  ; → 25
```

## S-expression Specs (src/specs/)

```
src/specs/
├── bitc-printer.lisp      ; Bit-level circuit printer
├── bitc.lisp              ; Bit-level circuit semantics
├── extension-printer.lisp ; Extension types printer
├── extension.lisp         ; User extensions
├── geb-printer.lisp       ; Geb → S-exp serialization
├── geb.lisp               ; Core Geb spec
├── lambda-printer.lisp    ; Lambda calc printer
├── lambda.lisp            ; STLC embedding
├── poly-printer.lisp      ; Polynomial printer
├── poly.lisp              ; Polynomial spec
├── seqn-printer.lisp      ; Sequence printer
└── seqn.lisp              ; Sequence representation
```

## Vampir Compilation Pipeline

```
Geb Morphism → SeqN (sequences) → BitC (bit circuits) → Vampir IR → ZK Proof
     ↑              ↑                    ↑                  ↑
  High-level    Flattening         Bit-blasting        PLONK/etc
```

## Obstruction Hot Potato Integration

### Geb Morphisms as Obstruction Passing

The Aptos obstruction_hot_potato.move maps directly to Geb categorical semantics:

```lisp
;; Obstruction as Geb type
(define obstruction-type
  (prod 
    (prod so1 so1)      ; (sexp, trit)
    (prod so1 so1)))    ; (h1_class, color)

;; Pass obstruction = morphism from source to target
(define (pass-obstruction source target obs)
  (comp
    ;; Nullify on source (inject-left to void)
    (inject-left (obstruction-type obs) so0)
    ;; VCG payment extraction
    (vcg-extract (h1-class obs))
    ;; Commit on target (inject-right from void)  
    (inject-right so0 (obstruction-type obs))))

;; Cross-chain: Aptos → Anoma bridge morphism
(define (aptos-to-anoma-bridge obs)
  (pair
    (nullify-on-aptos obs)      ; Left: burn on Aptos
    (mint-on-anoma obs)))       ; Right: mint on Anoma
```

### Spectral Gap → Monad Connection

The open-games skill shows: spectral gap + Möbius inversion → Free monad.

Geb provides the **categorical semantics** for this monad:

```lisp
;; Free monad on ObstructionF as Geb type
(define obstruction-free
  (coprod 
    so1                           ; Pure: no obstruction
    (prod obstruction-type        ; Roll: obstruction + continuation
          obstruction-free)))

;; Cofree comonad (dual) for observations
(define observation-cofree
  (prod 
    so1                           ; Extract: current observation  
    (prod observation-cofree      ; Minus neighbor
          (prod observation-cofree ; Ergodic neighbor
                observation-cofree)))) ; Plus neighbor
```

### VCG Payment as Geb Morphism

```lisp
;; VCG externality = H¹ × base_cost × multiplier
(define (vcg-payment h1-class)
  (geb.poly:* 
    (geb.poly:* h1-class base-cost)
    vcg-multiplier))

;; Roughgarden CS364A L7: truthful declaration is dominant
(define vcg-mechanism
  (lambda (declared-h1 actual-h1)
    (if (= declared-h1 actual-h1)
        (vcg-payment declared-h1)    ; Truthful: optimal
        (abort))))                    ; Lie: revert
```

### Juvix Type Compilation

```juvix
-- Obstruction type compiles to Geb
type Obstruction := mkObstruction {
  sexp : ByteArray;
  trit : GF3;        -- Compiles to (coprod so1 (coprod so1 so1))
  h1Class : Nat;
  color : Word64
};

-- Intent for cross-chain pass
passIntent : Obstruction -> ChainId -> ChainId -> Intent
passIntent obs src tgt := 
  Intent.compose
    (Intent.nullify src obs)   -- Geb: inject-left
    (Intent.commit tgt obs);   -- Geb: inject-right
```

## GF(3) Sexp Neighborhood

| Skill | Trit | Bridge to Geb |
|-------|------|---------------|
| **lispsyntax-acset** | 0 | S-exp ↔ ACSet bidirectional |
| **slime-lisp** | -1 | REPL for Common Lisp Geb |
| **geiser-chicken** | +1 | Scheme sexp coloring |
| **discopy** | 0 | String diagrams → morphisms |
| **cider-clojure** | +1 | EDN/sexp nREPL |
| **borkdude** | +1 | Babashka sexp runtime |
| **crdt-vterm** | 0 | CRDT sexp terminal sharing |

## Exhaustive Sexp Skill Neighborhood

```
                              GEB (+1)
                                 │
                                 │ compiles to
                                 ▼
    ┌────────────────────────────────────────────────────────┐
    │                     SEXP SKILLS                         │
    ├────────────────────────────────────────────────────────┤
    │                                                         │
    │   COMMON LISP                SCHEME                     │
    │   ┌─────────────┐           ┌─────────────┐            │
    │   │ slime-lisp  │           │ geiser-     │            │
    │   │ (-1)        │           │ chicken (+1)│            │
    │   └──────┬──────┘           └──────┬──────┘            │
    │          │                         │                    │
    │          └─────────┬───────────────┘                    │
    │                    │                                    │
    │                    ▼                                    │
    │   ┌─────────────────────────────────────┐              │
    │   │      lispsyntax-acset (0)           │              │
    │   │  S-exp ↔ ACSet bidirectional        │              │
    │   │  Specter navigation                 │              │
    │   └─────────────────────────────────────┘              │
    │                    │                                    │
    │          ┌─────────┴─────────┐                         │
    │          │                   │                          │
    │          ▼                   ▼                          │
    │   ┌─────────────┐    ┌─────────────┐                   │
    │   │ cider-      │    │ borkdude    │                   │
    │   │ clojure (+1)│    │ (+1)        │                   │
    │   └─────────────┘    └─────────────┘                   │
    │                                                         │
    │   CRDT / COLLAB              CONFIG LANGS              │
    │   ┌─────────────┐           ┌─────────────┐            │
    │   │ crdt-vterm  │           │ cue-lang    │            │
    │   │ (0)         │           │ (+1)        │            │
    │   └─────────────┘           │ nickel (0)  │            │
    │                             │ hof (-1)    │            │
    │                             └─────────────┘            │
    │                                                         │
    └────────────────────────────────────────────────────────┘
```

## Usage

```bash
# Clone and load
git clone https://github.com/anoma/geb
cd geb
sbcl --load geb.asd

# In REPL
(asdf:load-system :geb)
(in-package :geb.main)

# Example: evaluate morphism
(dom (comp (inject-left so1 so1) (terminal so1)))
; → SO1

# Polynomial evaluation
(geb.poly:gapply (geb.poly:+ geb.poly:ident 1) 5)
; → 6
```

## Files

- **Core**: `anoma/geb/src/geb/geb.lisp`
- **Poly**: `anoma/geb/src/poly/poly.lisp`
- **Vampir**: `anoma/geb/src/vampir/`
- **Idris verified**: `anoma/geb/geb-idris/`

---

## End-of-Skill Interface

## Integration with Anoma Intents

```lisp
;; Intent as Geb morphism
;; "I give X, I want Y" = morphism from X to Y
(define intent-morphism
  (pair 
    (inject-left resource-x resource-y)   ; Nullify X
    (inject-right resource-x resource-y))) ; Commit Y

;; Solver composes intents
(define matched-transaction
  (comp intent-a intent-b))

;; Compile to ZK proof
(geb-to-vampir matched-transaction)
```

### GF(3) Triads with Anoma

```
geb (+1) ⊗ solver-fee (-1) ⊗ open-games (0) = 0 ✓
  └─ Categorical semantics    └─ VCG payment    └─ Game coordination

geb (+1) ⊗ intent-sink (-1) ⊗ ihara-zeta (0) = 0 ✓
  └─ Intent types             └─ Nullification  └─ Non-backtracking
```

## Related Skills

| Skill | Trit | Relationship |
|-------|------|--------------|
| intent-sink | -1 | Nullifies Geb-typed intents |
| solver-fee | -1 | Extracts from Geb morphism matches |
| gay-mcp | +1 | Colors Geb types/morphisms |
| discopy | 0 | DisCoPy string diagrams ≅ Geb |

---

**Trit**: +1 (PLUS - generative)
**Key Property**: Categorical computation in S-expressions, compiles to ZK
**Anoma Role**: Intent types and morphism semantics


---

## Autopoietic Marginalia

> **The interaction IS the skill improving itself.**

Every use of this skill is an opportunity for worlding:
- **MEMORY** (-1): Record what was learned
- **REMEMBERING** (0): Connect patterns to other skills  
- **WORLDING** (+1): Evolve the skill based on use



*Add Interaction Exemplars here as the skill is used.*
