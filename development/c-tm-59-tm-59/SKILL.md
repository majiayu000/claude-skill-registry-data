---
name: c
description: Use when writing C (C11) programs — numerical simulations, terminal UIs, small command-line utilities, code compiled to WebAssembly, or programs with no libc at all. Covers Make-based builds, unit tests against analytic results, headless snapshot and GIF output, sanitizers, getopt_long and reproducible Docker builds. Also use when C code crashes only with optimisation on, or results drift between compilers.
---

# C

Default: C11, `-std=c11 -Wall -Wextra -Wpedantic -O2`, one `Makefile` with `all`, `test`, `plots` (or `run`) targets, only `libm` unless a library clearly earns its place.

## Layout that stays testable

```text
model.c / model.h   pure state-update functions, no I/O
ui.c                terminal or graphics front end
main.c              argument parsing, wiring
test.c              assertions on model.c, exits non-zero on failure
```

Public examples of this layout: `lift-pilot`, `current-swimmer`, `gravity-well`, `relativity-rider`, `quantum-wave-hopper`, `field-ripple` (all small C11 physics programs that run in a terminal).

## Numerical code

- Pick the integrator for the physics: RK4 for smooth ODEs, symplectic (leapfrog/velocity Verlet) for orbits where energy must not drift, implicit or semi-Lagrangian schemes for stiff or fluid problems.
- **Test against analytic solutions**, not against previous output: e.g. a phugoid period against Lanchester's formula, a Hohmann transfer delta-v against the textbook value, tunnelling probability against the closed form. Assert a tolerance (e.g. within 0.3 %).
- Check conserved quantities (energy, momentum, probability norm) over long runs; drift reveals step-size or scheme problems.
- Keep units in names or comments (`v_mps`, `t_s`).

## Headless outputs

- `--snapshot` prints one frame without a terminal, so tests and docs can capture it.
- `--gif out.gif` writes a scripted run as an animation; a minimal GIF encoder is a few hundred lines and avoids dependencies.
- `make plots` writes CSV and SVG charts from a scripted run, so the README images are reproducible.

## Command-line utilities

- Parse options with `getopt_long`; print usage on error and return 2.
- Check every return value of `fopen`, `malloc`, `read`, `write`; report with `perror`.
- For programs without libc (raw syscalls), keep the syscall layer in one file and test it through the program's output.

## Verification loop

1. Build with zero warnings on GCC and Clang.
2. `make test` with `-fsanitize=address,undefined -g` in a debug build.
3. Run the snapshot mode and compare with the expected output.
4. `docker build .` to prove a clean environment can build and test it.

## Pitfalls

- **Undefined behaviour** (signed overflow, uninitialised reads, out-of-bounds) may only show up at `-O2`. Sanitizers find most of it.
- **`float` vs `double`:** use `double` for simulation state; `float` accumulates error quickly.
- **`%d` with `size_t`** and similar printf mismatches are UB; use `%zu`, enable `-Wformat`.
- **Terminal state:** restore the terminal (raw mode, cursor, colours) on every exit path, including signals.
- **ncurses** needs `-lncurses` (and sometimes `-ltinfo`) and wide-character variants for Unicode; check `pkg-config` rather than hard-coding flags.
- **Integer division** truncates toward zero; `-7 / 2 == -3`.
