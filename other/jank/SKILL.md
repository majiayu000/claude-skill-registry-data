---
name: jank
description: "jank-lang: native Clojure on LLVM with seamless C++ interop. Use when writing native Clojure, bridging C/C++ libraries, or applying SICP Ch4-5 metalinguistic abstraction concretely."
version: 1.0.0
metadata:
  trit: 1
  author: bmorphism
  upstream: https://github.com/jank-lang/jank
  book: https://book.jank-lang.org/
---

# jank

> Write Clojure for humans, compile to LLVM IR for machines.

Native Clojure on LLVM. Seamless C++ interop. 3,117 stars. Alpha January 2026. Jeaye Wilkerson.

**Use:** native perf, C/C++ libs, AOT binaries, SICP Ch4-5 concretely.
**Don't use:** pure JVM (`clojure`), scripting (`babashka`), browser (`shadow-cljs`).

## Theoretical Foundations

| Source | Concept | jank |
|--------|---------|------|
| SICP 1 | λ, higher-order fns | fns → LLVM IR; closures = GC'd C++ objects |
| SICP 2 | Abstraction barriers | Persistent data in C++; `convert<T>` = barriers |
| SICP 3 | State, concurrency | `future` (#674); atom/ref/agent; thread-safe |
| SICP 4 | Metacircular eval | jank IS it — Clojure evaluating Clojure → native |
| SICP 5 | Register machines, GC | LLVM IR = registers; Boehm GC = 5.3; AOT = 5.5 |
| SDF 1-2 | Combinators, DSLs | `cpp/raw`,`cpp/cast`,`cpp/box` compose; `cpp/` = sub-DSL |
| SDF 3-4 | Generic ops, matching | `convert<T>` traits + Clang overload resolution |
| SDF 7 | Propagators | Bidirectional: jank string ↔ `std::string` |
| SDF 8 | Degeneracy | REPL → JIT → AOT = multiple paths, same result |

Compile AND interpret simultaneously. C++ interop = escape hatch into the machine.

## Pipeline

Statically typed. Zero overhead. No reflection. Four stages per interop call:

1. **Wrapper** — C++ helper (unpack args, box return)
2. **`convert<T>`** — trait-resolved type conversion at compile time
3. **Pointer adj** — `this`, const/ref for members
4. **IR** — [CppInterOp](https://github.com/compiler-research/CppInterOp) → LLVM IR → linked

Bootstrap: Phase 1 builds compiler (C++/LLVM), Phase 2 compiles jank's stdlib with itself.

## Interop

`::` → `.` (`std::string` → `std.string`). Clojure resolves first; `cpp/` disambiguates.

```clojure
;;; HEADERS — cpp/raw: global scope, returns nil, workaround escape hatch
(cpp/raw "#include <cstdlib>")
(cpp/raw "struct vec2 { float x{}, y{}; };
          vec2 operator+(vec2 const &l, vec2 const &r)
          { return { l.x + r.x, l.y + r.y }; }")
;; -I <path> -D FOO -L <path> -l <lib>
;; :jank {:include-dirs [...] :library-dirs [...] :linked-libraries [...]}

;;; FUNCTIONS — overloads, implicit conv, void→nil, variadics, templates
(printf "result: %d\n" (rand))
(let [u (getenv #cpp "USER")] (println u))     ; #cpp = unboxed C++ value

;;; MEMBERS — .foo call, .-foo field (public, const/ref-qual aware)
(let [s (cpp/cast std.string "meow")] (.size s) (.substr s 1 3))
(.-npos std.string)

;;; OPERATORS — 45: + - * / % == != < > <= >= && || ! & | ^ ~ << >> = += [] * -> ++ --
(let [ab (cpp/+ (vec2. #cpp 1.0 #cpp 2.0) (vec2. #cpp 4.0 #cpp 3.0))]
  (println (.-x ab) (.-y ab)))

;;; TYPES
#cpp 42  #cpp 3.14  #cpp "hello"               ; unboxed int, double, char[]
cpp/true  cpp/false  cpp/nullptr                ; native C++ bool/null
(cpp/value "std::numeric_limits<int>::max()")   ; complex exprs
(cpp/type "std::map<std::string, int (*)(int)>"); templates
cpp/int**                                       ; pointer types
;; enums (scoped+unscoped), function ptrs, functors/lambdas all work

;;; CAST
(cpp/cast cpp/int (rand))                       ; static_cast + convert<T>
(cpp/unsafe-cast (cpp/type "unsigned char*") s) ; reinterpret_cast

;;; MEMORY — bdwgc GC; cpp/delete eager for RAII
(let [p (cpp/new cpp/int (cpp/int. 500))] (assert (= 500 (cpp/* p))) (cpp/delete p))

;;; ARRAY + BOX
(cpp/aget arr idx)
(let [b (cpp/box (cpp/new my_db.conn #cpp "localhost:5758"))]
  (.query (cpp/unbox my_db.conn* b) "SELECT 1")) ; compile-time type check

;;; CONVERT TRAIT — custom: specialize jank::runtime::convert<T>
;;   template <> struct jank::runtime::convert<MyType> {
;;     static MyType from(object_ptr o) { ... }
;;     static object_ptr to(MyType const &v) { ... }  };
```

### Examples

```clojure
;; JSON pretty-printer (header-only nlohmann/json)
(cpp/raw "#include <fstream>")  (cpp/raw "#include \"json.hpp\"")
(defn -main [& args]
  (let [f (std.ifstream. (cpp/cast std.string (first args)))]
    (println (.dump (nlohmann.json.parse f) 2))))

;; zlib compression (-l z)
(cpp/raw "#include <zlib.h>")
(defn compress-str [input]
  (let [src (cpp/cast (cpp/type "const Bytef*") input)
        n   (cpp/cast cpp/uLong (count input))
        dn  (compressBound n)
        dst (cpp/new (cpp/type "Bytef") dn)]
    (compress dst (cpp/& dn) src n) (cpp/box dst)))

;; FTXUI hiccup → C++ flexbox
(render-hiccup [:vbox
  [:hbox [:text "NW"] [:filler] [:text "NE"]] [:filler]
  [:hbox [:filler] [:text "center"] [:filler]] [:filler]
  [:hbox [:text "SW"] [:filler] [:text "SE"]]])
```

## Usage

```bash
jank repl                                       # eval/apply
jank run app.jank                               # JIT
jank -I vendor -l z run app.jank -- args        # + native libs
jank compile app.jank -o app                    # AOT binary
lein new org.jank-lang/jank proj && lein run    # Leiningen
lein compile                                    # AOT → ./a.out
zerobrew install jank-lang/jank/jank             # install macOS (also: apt, yay, nix)
```

## Status (Jan 2026)

| Done | Missing |
|------|---------|
| Interop: headers, fns, members, ctors, cast, box, 45 ops | Records, Protocols |
| `#cpp`, `cpp/value`, `cpp/aget`, `cpp/unsafe-cast`, enums, lambdas | Types in jank syntax |
| PCH, AOT, two-phase, deferred compilation (+50%) | CIDER (Clang bug) |
| `future`, thread safety, regex, UUID, instant, BigDecimal | Library parity: 57% |
| nREPL + imgui (Kyle Cesare); zerobrew/apt/AUR/nix | Syntax parity: 93% |

Contributors: Jeaye Wilkerson + Saket (interop), Monty (compiler/distro), Jianling (catch/stdlib), Shantanu (REPL/tests/bigint), Kyle Cesare (nREPL/imgui), djblue, pfeodrippe, E-A-Griffin, Samy-33, cjbarre.

## Δ Clojure

| Clojure | jank |
|---------|------|
| Classpath | Module path |
| `(hash-map)` → array-map | Always hash-map |
| `aget` fn | `aget` special form |
| Nested `require` | No (like CLJS) |
| `import` | `cpp/raw #include` |
| `defrecord`/`defprotocol` | Not yet |
| `/ 1 0` → exception | UB |
| `#js` | `#cpp` |

## Ecosystem

`scripts/splitmix64.jank` — SplitMix64 → hue → Girard polarity → TAP. `jank run scripts/splitmix64.jank -- 42`

`scripts/neanderthal.jank` — ersatz Neanderthal (uncomplicate) syntax on Eigen via jank interop. BLAS L1/2/3: `dv`, `dge`, `dot`, `axpy`, `scal`, `mv`, `mm`. MPC primitives (`mpc-predict`, `mpc-cost`, `mpc-horizon`). Append-only log for promise chain resolution. `jank -I /path/to/eigen3 run scripts/neanderthal.jank`

`asi/ies/music-topos/lib/crdt_sexp_ewig.jank` — same PRNG + CRDT ops + Lager actions.

`jank_interop.duckdb` — `commits`(is_interop), `pull_requests`, `repo_meta`.

## Connections

| Skill | Trit | |
|-------|------|-|
| `clojure` | 0 | Language family |
| `sicp` | 0 | Ch4-5 realized |
| `babashka` | 0 | Scripts ↔ native |
| `zig` | +1 | Complementary native |
| `propagators` | 0 | SDF 7 bidirectional |
| `rama-gay-clojure` | 0 | SplitMix64 shared |

`clojure(0) + jank(+1) + property-based-testing(-1) = 0 mod 3`

## Cat#

`+1 PLUS | Prof | y (Yoneda) | Lan | #E847C0` — compilation ⊣ interpretation, mediated by REPL.

## Refs

[jank-lang.org](https://jank-lang.org/) | [book](https://book.jank-lang.org/) | [GitHub](https://github.com/jank-lang/jank) | [interop blog 1](https://jank-lang.org/blog/2025-05-02-starting-seamless-interop/) [2](https://jank-lang.org/blog/2025-06-06-next-phase-of-interop/) [3](https://jank-lang.org/blog/2025-07-11-jank-is-cpp/) | [SICP](https://mitpress.mit.edu/sites/default/files/sicp/full-text/book/book.html) | [SDF](https://mitpress.mit.edu/9780262045490/)


## REPL atlas

Part of: `repl-commons`. Family canonical: `clojure`.
