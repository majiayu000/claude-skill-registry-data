---
name: R
description: Avoid common R mistakes — vectorization traps, NA propagation, factor surprises, and indexing gotchas.
metadata: {"clawdbot":{"emoji":"📊","requires":{"bins":["Rscript"]},"os":["linux","darwin","win32"]}}
---

## Vectorization
- Loops are slow — use `apply()`, `lapply()`, `sapply()`, or `purrr::map()`
- Vectorized functions operate on whole vectors — `sum(x)` not `for (i in x) total <- total + i`
- `ifelse()` is vectorized — `if` is not, use `ifelse()` for vector conditions
- Column operations faster than row — R is column-major

## Indexing Gotchas
- R is 1-indexed — first element is `x[1]`, not `x[0]`
- `x[0]` returns empty vector — not error, silent bug
- Negative index excludes — `x[-1]` removes first element
- `[[` extracts single element — `[` returns subset (list stays list)
- `df[, 1]` drops to vector — use `df[, 1, drop = FALSE]` to keep data frame

## NA Handling
- NA propagates — `1 + NA` is `NA`, `NA == NA` is `NA`
- Use `is.na()` to check — not `x == NA`
- Most functions need `na.rm = TRUE` — `mean(x)` returns NA if any NA present
- `na.omit()` removes rows with any NA — may lose data unexpectedly
- `complete.cases()` returns logical vector — rows without NA

## Factor Traps
- Old R converted strings to factors by default — use `stringsAsFactors = FALSE` or modern R
- `levels()` shows categories — but factor values are integers internally
- Adding new value not in levels gives NA — use `factor(x, levels = c(old, new))`
- `as.numeric(factor)` gives level indices — use `as.numeric(as.character(factor))` for values
- Dropping unused levels: `droplevels()` — or `factor()` again

## Recycling
- Shorter vector recycled to match longer — `c(1,2,3) + c(10,20)` gives `11, 22, 13`
- No error if lengths aren't multiples — just warning, easy to miss
- Single values recycle intentionally — `x + 1` adds 1 to all elements

## Data Frames vs Tibbles
- Tibble never converts strings to factors — safer defaults
- Tibble never drops dimensions — `df[, 1]` stays tibble
- Tibble prints better — shows type, doesn't flood console
- `as_tibble()` to convert — from `tibble` or `dplyr` package

## Assignment
- `<-` is idiomatic R — `=` works but avoided in style guides
- `<<-` assigns to parent environment — global assignment, usually a mistake
- `->` right assignment exists — rarely used, confusing

## Scope
- Functions look up in parent environment — can accidentally use global variable
- Local variable shadows global — same name hides outer variable
- `local()` creates isolated scope — variables don't leak out

## Common Mistakes
- `T` and `F` can be overwritten — use `TRUE` and `FALSE` always
- `1:length(x)` fails on empty x — gives `c(1, 0)`, use `seq_along(x)`
- `sample(5)` vs `sample(c(5))` — different! first gives 1:5 permutation
- String splitting: `strsplit()` returns list — even for single string
