---
name: reduce-relie-lie-symmetries
description: Use when working with ReLie in REDUCE (including inside Docker) to compute Lie group symmetries of differential equations, handle conditional/contact/variational/approximate symmetries or equivalence transformations, or interpret ReLie outputs and Lie algebra utilities.
---

# ReLie symmetry workflows in REDUCE

## Quick start (point symmetries)

- Load ReLie: `in "resources/relie-src/relie.red"$` (or `load_package relie$` if precompiled).
- Set the minimal globals: `jetorder`, `xvar`, `uvar`, `diffeqs`, `leadders`.
- Run the standard pipeline: `relie(4)$`.
- Extract generators: `reliegen(1,{})$`, then inspect `symmetries`, `generators`, `splitsymmetries`.

## Docker readiness (when running in containers)

- Confirm the CLI and daemon: `docker --version` then `docker info`.
- If the daemon is down, start Docker Desktop (macOS: `open -a Docker`) and wait for `docker info` to succeed.
- If you use Colima instead of Docker Desktop, start it with `colima start` and re-check `docker info`.
- If you see `permission denied ... docker.sock`, rerun with elevated permissions or fix socket access (Codex sandboxing may require escalation).

## Keep these invariants in mind

- Treat ReLie state as global; always (re)declare variables before `relieinit()`.
- `diffeqs` and `leadders` must have the same length and be solvable for the chosen leading derivatives.
- Mixed-derivative names must follow the `xvar` order.

## Always explain results in natural language

After any computation, translate the output into plain language:

- State what was computed (e.g., point/conditional/contact/variational/approximate/equivalence symmetries) and the PDE or system.
- Report how many solution-sets are in `symmetries` and how many generators you extracted.
- Interpret each generator as a transformation (translations, scalings, Galilean boosts, shifts in `u`, etc.).
- If arbitrary functions appear in `symmetries`, explain that this indicates an infinite-dimensional symmetry (often due to linearity or gauge freedom).
- Note any unsolved conditions or non-vanishing constraints and what they mean for validity.
- Say what the symmetries are useful for: similarity reduction to ODEs, invariant solutions, conservation laws (Noether), and classification of PDE families.

Use `resources/relie_result_interpretation.md` for a compact template and common patterns.

## Use the reference guide for details

- For conditional/contact/variational/approximate/equivalence workflows, Lie algebra utilities, and troubleshooting, open `resources/ReLie_whitepaper_synopsis.md`.
- For the Docker run command and minimal bootstrap, use the `reduce-relie-basics` skill.

## Debugging pattern

- If `reliesolve()` fails, run staged calls (`relieinit`, `relieinv`, `reliedet`, `reliesolve`) and inspect `invcond` and `deteqs`.
- Enable CRACK verbosity with `onprintcrack()` when you need step-by-step solving.
