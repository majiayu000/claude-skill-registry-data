---
name: cosmic
description: >
  Write portable scripts and tools with cosmic — HTTP requests, JSON
  parsing, SQLite databases, filesystem operations, child processes, crypto,
  compression, and more in a single zero-dependency binary
---

# cosmic

cosmic is a batteries-included Lua distribution for writing portable
scripts and tools. it ships as a single binary with built-in support for
HTTP fetching, JSON, SQLite, filesystem operations, child processes,
cryptographic hashing, compression, regex, sockets, and more — no external
dependencies needed. source files are written in Teal (typed Lua) and run
on Linux, macOS, Windows, FreeBSD, OpenBSD, and NetBSD.

## Download

the binary is named `cosmic` after download. rename it if you prefer.

```bash
curl -fLo cosmic \
  https://github.com/whilp/cosmic/releases/latest/download/cosmic-lua
chmod +x cosmic
```

## Run

```bash
./cosmic script.tl           # run a Teal script
./cosmic -e 'print("hi")'   # run inline code
./cosmic -i                  # start the REPL
```

## Getting Help

```bash
./cosmic --welcome                # quick-start orientation
./cosmic --help                   # show all CLI options and modules
./cosmic --docs                   # browse the full documentation index
./cosmic --docs <query>           # look up a module, function, or guide
./cosmic --docs guide             # list available guides
./cosmic --docs guide.testing     # show a specific guide
```
