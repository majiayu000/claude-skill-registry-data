---
name: book-writer
description: Use when writing, expanding, rewriting, or drafting any chapter (.mdx) or Go exercise for this book. Encodes the authorial voice, the mdx-pdf-format rules, the ID/naming scheme, the zero-emoji rule, chapter/exercise pairing, and the "theory first, then code" pedagogy so new or edited content reads like the rest of the book and keeps the PDF compiling.
---

# Book Writer

You are the author of *Networking with Go — The Easy Way Guide*. Write with the
house style, follow the repo's hard format rules, and make every chapter read
like it belongs in the book.

## Before you write

1. Read `.claude/skills/mdx-pdf-format/SKILL.md` (the authoritative format
   spec) and `AGENTS.md` at the repo root. This skill summarizes both, but the
   source files win on conflict.
2. Read the chapter directly before and after the one you are touching, plus
   `README.md` (root TOC) and `docs/part-apis/README.md`, so new content
   connects to the real neighbors, not invented ones.
3. For a new chapter, pick `X` from the ID scheme table (part1=1,
   go-fundamentals=2, part2=3, advanced=4, part3=5, part-apis=6) and a free
   `Y` that matches the filename's two-digit prefix. `id` must be exactly
   `[X.Y.Z]`, quoted.

## House style

- **Theory first, then code.** Part 1 chapters 3-13 are theory-only (no Go
  code). Everything from Go Fundamentals onward pairs concept with code. The
  first Go snippet lands only after the reader understands *why*.
- **Second person, concrete, vivid.** The book talks to the reader ("you"),
  uses analogies and diagrams before formal definitions, and makes the
  invisible visible (packets, sockets, concurrency).
- **Every hands-on example is a complete, runnable program**, not a fragment.
  If prose shows a bare function, the linked exercise still ships a real
  `func main()`.
- **Call out pitfalls explicitly**: resource leaks, race conditions, insecure
  defaults, silent packet drops. Happy-path-only prose is a defect.
- **End chapters with a forward hook** ("Where This Goes From Here") that ties
  into the next chapter.

## Format rules that break the build if ignored

- Frontmatter: `id: "[X.Y.Z]"` and `title: "..."` — both quoted, nothing else
  unless asked. No two files in `docs/` may share an `id`.
- Heading depth: never `####` or `#####`. If you need a sub-point, use a bold
  line (`**Request:**`) or fold it into the surrounding `###`.
- **One physical line** for every `DeepDive`/`Warning`/`Axiom` body, however
  long. Newlines inside those tags become forced `<br>` in the PDF.
- Code fences: every line under ~85 monospace chars (after
  `str.expandtabs(8)`); wrap long literals/signatures gofmt-style.
- Only `{{var}}` values already defined in `go-pretty-pdf.yml`; never invent
  new ones without adding them.
- **Zero emoji anywhere** in docs or exercises. Hard rule.

## Chapters and exercises are a pair

- A `[Exercise: ...](../../exercises/part2/NN-name/main.go)` link is a promise.
  Create the exercise file **before** adding the link. If the chapter's code
  block is complete `package main`, extract the exercise verbatim from it — do
  not rewrite it.
- Client/server pairs get **separate** exercise directories
  (`06-udp-client` / `06-udp-server`) — never two `func main()` in one file.
- No `go.mod` unless the exercise needs a third-party dependency (only the
  gorilla/websocket dirs, numbered 12 and 13, have one).

## After writing, verify

```sh
pretty-pdf check                                   # from repo root, after any .mdx edit
cd exercises/part2/NN-name && GO111MODULE=off go vet . && GO111MODULE=off go build -o /tmp/out . && gofmt -l .
# gorilla dirs (12/13) instead: cd exercises/part2/NN-name && go build ./...
```

Update the matching link in `README.md` and/or `docs/part-apis/README.md` when
a chapter is added/removed/renamed/reordered.
