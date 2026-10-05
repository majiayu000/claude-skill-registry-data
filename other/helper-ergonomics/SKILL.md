---
name: helper-ergonomics
description: Use when adding or changing exported Go API (or the CLI) in this project, and before committing — UnPixel is human-facing, so hunt for convenience/helper functions that make it easy to use. Spots missing one-call wrappers, constructors, broad-input helpers, and option patterns. A pre-commit hook reinforces it.
---

# Helper Ergonomics

Goal: **make the easy thing easy.** UnPixel is meant to be used by humans — both as a Go library
and as a CLI — so a newly added or changed API must be judged not only for correctness but for
*how little a caller has to write to do the common thing*. Before committing API changes, hunt
for helper/convenience functions that collapse boilerplate, and propose the ones that are earned.

## The core question

For every new/changed exported symbol, ask: **"What is the smallest program a human must write to
use this, and can a helper make it smaller?"** If the happy path takes 5 lines of wiring, there is
probably a one-call helper hiding in it.

Concrete example in this repo: today recovering text is
```go
import _ "github.com/oioio-space/unpixel/defaults" // easy to forget → zero results
img, _ := png.Decode(f)
eng, _ := unpixel.New(img, unpixel.Config{})
prog, res := eng.Run(ctx)
best := (<-res).BestGuess
```
A human-friendly helper collapses that to one obvious call:
```go
best, err := unpixel.RecoverFile(ctx, "redacted.png")      // or Recover(ctx, img, opts...)
```

## Precepts (look for each, before commit)

1. **One-call wrapper for the common path.** A top-level func that does the whole dance (decode →
   wire defaults → run → return best). It removes the "forgot the `defaults` side-effect import"
   foot-gun entirely.
2. **Broaden the input.** Offer overloads for how humans actually have the data: an `image.Image`,
   an `io.Reader`, and a file path (`RecoverFile`/`RecoverReader`/`Recover`). Accept interfaces,
   return concrete types.
3. **Constructors with sensible defaults; useful zero values.** `New`/`NewX(...)` that fill
   defaults so `Config{}` already works; don't make callers set fields that have an obvious value.
4. **Functional options for the optional.** For "mostly defaults, tweak one thing", prefer
   `Recover(ctx, img, WithCharset(...), WithWorkers(n))` over forcing a full `Config` literal.
   (See the go-style-guide best-practices "option pattern".) Keep the `Config` struct too for
   power users; options wrap it.
5. **Don't make callers touch internals.** Side-effect imports, manual component wiring, and
   "first call X then Y then Z" sequences are papercuts — hide them behind a helper or do them in
   the constructor.
6. **Printable, inspectable results.** Give result/enum types a `String()` and, where useful, a
   small accessor or `Format`, so a human can `fmt.Println(result)` and get something readable.
7. **Actionable errors.** Error messages should tell the human what to do ("block-size must match
   the redaction; try --block-size auto"), not just what failed.
8. **CLI ergonomics.** Sane defaults, `-` for stdin, examples in `--help`, machine-readable
   `--json`, clear exit codes, and flags named the way a human guesses.

## Process (before committing API/CLI changes)

1. `git diff --cached` — list new/changed exported funcs, types, fields, and CLI flags.
2. For each, write the smallest real caller program in your head; count the wiring lines.
3. Propose concrete helper signatures that collapse it. Name them; show the before/after.
4. **Don't over-helper.** Only add a wrapper that a real user would reach for; least mechanism
   wins (go-style-guide principle #2). A helper nobody calls is noise. Prefer 1–3 high-value
   helpers over a dozen thin ones.
5. Helpers must be documented for GoDoc (see the go-style-guide GoDoc block), tested, and keep
   the lower-level API available for power users.

## Anti-patterns (flag these)

- The only way to do the common thing is to assemble 4 pieces yourself.
- A required side-effect import with no convenience entry point.
- Exposing only a giant `Config` struct with no options or one-call helper.
- Result types you can't `Println` meaningfully.
- CLI that needs flags for the obvious default behavior.

## Routing & tier (token-economical, no quality loss)

API-design judgment on a diff — the economical tier that loses no quality is **Sonnet / effort
medium**, not Opus (no novel-algorithm or security reasoning here) and not Haiku (proposing
*earned* helpers without over-engineering needs design taste). So:

- **Review** a substantial diff → delegate to the **go-reviewer** sub-agent (model: Sonnet,
  effort: medium).
- **Implement** the agreed helpers → **go-dev** (model: Sonnet, effort: medium).
- **Tiny diff** → clear inline in the main loop; don't spawn an agent.

Pairs with the `commit-ergonomics-review.sh` pre-commit hook.
