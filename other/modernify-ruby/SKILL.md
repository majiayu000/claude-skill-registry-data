---
name: modern-ruby
description: "Authoritative version gate for modern Ruby (3.0–4.0) — what feature requires which Ruby version, and how to write idiomatic modern Ruby. Use when the user mentions a Ruby version (3.0, 3.1, 3.2, 3.3, 3.4, 4.0), asks 'what Ruby version do I need for X', mentions features like pattern matching, `Data.define`, the `it` block parameter, numbered parameters `_1`, endless methods, anonymous argument forwarding (`*`/`**`/`&`), `Ractor`, hash value omission `{x:}`, asks to modernize Ruby code or check a feature's minimum version, or asks how to upgrade/migrate to Ruby 4.0, what breaks, ZJIT/YJIT, or which stdlib gems (`ostruct`, `logger`, `Set`, `Pathname`) moved."
---

# Modern Ruby (3.0 → 4.0)

Version-accurate reference for Ruby language features. Sources: [rubychanges](https://rubyreferences.github.io/rubychanges/) (per-version changelogs), the official [ruby-lang.org release announcements](https://www.ruby-lang.org/en/news/2025/12/25/ruby-4-0-0-released/), and [docs.ruby-lang.org](https://docs.ruby-lang.org/en/4.0/) — see each reference file for its specific citation.

**Core rule for using this skill: version gates and code samples here are exact. Never paraphrase a version number or reconstruct syntax from memory — quote from this file. When a feature isn't listed, say so rather than guessing the version.** Each Ruby minor releases on Dec 25 of the named year.

## Version gate table

The minimum Ruby version that introduced each headline feature:

| Feature | Min version | Syntax |
|---------|:-----------:|--------|
| Keyword args fully separated from positional | 3.0 | `def m(a, k:)` |
| Pattern matching (stable) | 3.0 | `case x; in [a, b]` |
| One-line pattern match — rightward assignment | 3.0 | `data => {name:}` |
| One-line pattern match — boolean check | 3.0 | `if data in {name:}` |
| Find pattern | 3.0 | `in [*, target, *]` |
| Endless method definition | 3.0 | `def square(x) = x * x` |
| Ractor (true parallelism, experimental) | 3.0 | `Ractor.new { ... }` |
| Non-blocking `Fiber` + scheduler | 3.0 | `Fiber.set_scheduler` |
| Hash/keyword value omission | 3.1 | `{x:, y:}` / `m(x:, y:)` |
| Anonymous block forwarding | 3.1 | `def m(&) = n(&)` |
| Pattern match: pin expressions | 3.1 | `in ^(a + b)` |
| Endless method + command syntax (no parens) | 3.1 | `def m = puts "hi"` |
| `Data.define` — immutable value object | 3.2 | `Data.define(:x, :y)` |
| Anonymous `*` / `**` forwarding | 3.2 | `def m(*, **) = n(*, **)` |
| `Set` is built-in (no `require 'set'`) | 3.2 | `Set[1, 2]` |
| `Struct.new` takes positional **and** keyword | 3.2 | `S.new(1)` / `S.new(x: 1)` |
| `Range#overlap?` | 3.3 | `(1..5).overlap?(4..8)` |
| `Module#set_temporary_name` | 3.3 | `klass.set_temporary_name "T"` |
| `it` as anonymous block parameter | **3.4** | `arr.map { it ** 2 }` |
| `**nil` → empty keyword arguments | 3.4 | `m(**nil)` |
| `Range#step` by `+` for any type | 3.4 | `(a..b).step(x)` |
| Leading `&&`/`\|\|`/`and`/`or` line continuation | 4.0 | `a\n  \|\| b` |
| `Pathname` is a core class (no `require`) | 4.0 | `Pathname('x')` |
| `Ruby::Box` — isolated namespace loading (experimental) | 4.0 | `Ruby::Box.new` |
| `Ractor::Port` | 4.0 | `Ractor::Port.new` |

> ⚠ **Common gate traps.** `it` only became the anonymous block parameter in **3.4** — Ruby 3.3 merely *warns* that it will. Frozen string literals are **not** the default in 3.4 either; 3.4 only adds a *warning* preparing for the change planned for 3.5. Numbered parameters (`_1`, `_2`) are older — they arrived in **2.7**, not 3.x.

## Quick idioms (modern Ruby)

```ruby
# Immutable value object (3.2+) — prefer over Struct for value types
Point = Data.define(:x, :y)
p = Point.new(x: 1, y: 2)   # positional or keyword
p.with(y: 9)                # => new Point, original unchanged

# Anonymous block parameter (3.4+)
[1, 2, 3].map { it ** 2 }   # => [1, 4, 9]   (use _1 on 2.7–3.3)

# Hash value omission (3.1+)
x, y = 1, 2
{x:, y:}                    # => {x: 1, y: 2}

# Endless method (3.0+; bare command form 3.1+)
def log(msg) = puts "#{Time.now}: #{msg}"

# Argument forwarding without naming (3.2+)
def get(url, **) = send_request(:get, url, **)

# Pattern matching (3.0+)
case config
in {db: {user:}} then connect(user)
in String => dsn then connect_dsn(dsn)
end
```

## How to answer version questions

1. **"What Ruby version do I need for X?"** → find X in the gate table; quote the version exactly. If absent, check `references/by-feature.md` (the cross-version thematic map covering 2.0+), and only then say it's not covered.
2. **"What's new in Ruby N?"** → see the per-version section in `references/by-version.md`.
3. **"Modernize this code"** → identify the target version, then apply idioms at or below that gate. Don't introduce a feature newer than the user's stated Ruby. If the version is unstated, ask, or default conservatively and flag each feature's gate.
4. **"How do I upgrade to 4.0 / what breaks?"** → see `references/migrating-to-4.0.md` (breaking changes, gem/Gemfile impact, ZJIT vs YJIT, CI). Key gotchas: Ractor primitives (`Ractor.yield`/`#take`) are **removed** for `Ractor::Port`; `ostruct`/`logger`/`irb`/`rdoc`/`benchmark`/`pstore` are now **bundled gems** (add to Gemfile); `*nil` no longer calls `nil.to_a`; `--rjit` removed. Get to 3.4 first and run `RUBYOPT="-W:deprecated"`.

## References

- `references/by-version.md` — per-release (3.0 → 4.0) highlights with verbatim code examples.
- `references/by-feature.md` — cross-version thematic evolution (pattern matching, blocks, `Data`/`Struct`, `Hash`, freezing, concurrency) back to Ruby 2.0, with per-feature version tags.
- `references/migrating-to-4.0.md` — upgrading 3.x → 4.0: breaking changes, stdlib promotions, ZJIT/YJIT, gem compatibility, CI implications.

Load a reference only when the gate table above doesn't already answer the question.

## Authoritative API docs (for the long tail)

This skill covers headline language features. For an individual core method, class, or exact syntax rule it doesn't list, consult the official docs rather than guessing — they're versioned, so swap `4.0` for `3.4`, `3.2`, etc. to match the user's Ruby.

- **Core class / module:** `https://docs.ruby-lang.org/en/4.0/<Class>.html` — e.g. [`String`](https://docs.ruby-lang.org/en/4.0/String.html), [`Array`](https://docs.ruby-lang.org/en/4.0/Array.html), [`Hash`](https://docs.ruby-lang.org/en/4.0/Hash.html), [`Enumerable`](https://docs.ruby-lang.org/en/4.0/Enumerable.html), [`Comparable`](https://docs.ruby-lang.org/en/4.0/Comparable.html). Namespaced: `Net/HTTP.html`, `Data.html`, `Set.html`, `Ractor.html`.
- **Syntax / language reference:** [`syntax_rdoc.html`](https://docs.ruby-lang.org/en/4.0/syntax_rdoc.html); pattern matching at [`syntax/pattern_matching_rdoc.html`](https://docs.ruby-lang.org/en/4.0/syntax/pattern_matching_rdoc.html), method calls at `syntax/calling_methods_rdoc.html`.
- **Per-version NEWS (authoritative changelog):** `https://docs.ruby-lang.org/en/v4.0.0/NEWS_md.html`, or the source file `https://github.com/ruby/ruby/blob/v4.0.0/NEWS.md`.
- **Docs index:** [docs.ruby-lang.org/en/4.0/](https://docs.ruby-lang.org/en/4.0/).

When you cite a method's existence or behavior from these docs, name the version of the doc page you used — a method present in 4.0 may be absent in the user's older Ruby.
