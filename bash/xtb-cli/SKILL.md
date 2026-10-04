---
name: xtb-cli
description: Use when an agent needs to operate the local xTB command-line executable for molecule calculations, XYZ inputs, single-point energies, geometry optimization, Hessian/thermochemistry, implicit solvation, HOMO/LUMO and gap, dipole moment, polarizability, electrophilicity, Fukui indices, CLI harness integration, environment checks, retry strategy, or xTB failure diagnosis.
---

# xtb-cli

## Purpose

Use the local `xtb` executable as the primary interface for automated molecule calculations. Prefer this skill when a benchmark atom needs local semiempirical quantum evidence from xTB itself, not only HPC job-template guidance. Keep commands explicit and reproducible; do not rely on hidden defaults when charge, unpaired electrons, method, solvent, or run type matters.

`hpc-xtb` remains the skill for xTB/CREST workflow planning, HPC scripts, and scheduler-style templates. `xtb-cli` is the local executable provider for structured benchmark skill calls.

## Preflight

Run these checks before the first live chemistry calculation in a session:

```bash
command -v xtb
xtb --version
```

If command availability or flags are uncertain, inspect:

```bash
xtb --help
```

Treat a missing executable or unusable installation as an environment problem, not as evidence that a molecule or parser is bad.

## Workspace Execution

Use the benchmark-managed runner pattern:

```bash
python scripts/run_skill.py \
  --workspace-root <workspace-root> \
  --execution-cwd "$BENCHMARK_SKILL_SCRATCH_DIR" \
  --script skills/xtb-cli/scripts/xtb_runner.py -- \
  --request-json <request-json> \
  --output-dir <output-dir> \
  --json
```

Every call reads one request JSON object, writes `result.json`, and prints the same payload when `--json` is passed. See [contracts.md](references/contracts.md) for the supported request and result shape.

## Run Hygiene

- Run each calculation in a fresh temporary working directory; xTB writes files such as `xtbopt.xyz`, `xtbopt.coord`, `xtbhess.coord`, Hessian data, restart data, and logs in the current directory.
- Write the candidate geometry to a stable filename such as `candidate.xyz`, then run `xtb` from that directory.
- Pass `--chrg`, `--uhf`, and `--gfn` explicitly. For neutral closed-shell GFN2-xTB molecules, start with `--chrg 0 --uhf 0 --gfn 2`.
- Capture stdout, stderr, return code, timeout, command, xTB version, input geometry, method, charge, UHF, solvent model, and solvent name.
- Parse stdout conservatively. Optimized runs can contain initial and final summaries; prefer the final relevant occurrence of repeated fields.
- Trust optimized-geometry properties only after the output indicates normal termination or geometry optimization convergence.

## Common Commands

Single-point energy and default properties:

```bash
xtb candidate.xyz --gfn 2 --chrg 0 --uhf 0
```

Geometry optimization:

```bash
xtb candidate.xyz --gfn 2 --chrg 0 --uhf 0 --opt
```

Hessian and thermochemistry on the provided geometry:

```bash
xtb candidate.xyz --gfn 2 --chrg 0 --uhf 0 --hess
```

Optimization followed by Hessian:

```bash
xtb candidate.xyz --gfn 2 --chrg 0 --uhf 0 --ohess
```

Implicit solvation single point or optimization:

```bash
xtb candidate.xyz --gfn 2 --chrg 0 --uhf 0 --alpb water
xtb candidate.xyz --gfn 2 --chrg 0 --uhf 0 --opt --alpb water
xtb candidate.xyz --gfn 2 --chrg 0 --uhf 0 --gbsa water
```

Vertical electrophilicity:

```bash
xtb candidate.xyz --gfn 1 --chrg 0 --uhf 0 --vomega
```

Vertical Fukui indices:

```bash
xtb candidate.xyz --gfn 1 --chrg 0 --uhf 0 --vfukui
```

Machine-readable output can be requested with an xcontrol input file:

```text
$write
   json=true
$end
```

Use JSON when it contains the needed fields for the installed xTB version; otherwise parse stdout and generated files defensively.

## Property Workflows

HOMO, LUMO, and HOMO-LUMO gap:

- Run an optimization when the target is an optimized-geometry electronic property.
- Parse the orbital-energy table rows marked `(HOMO)` and `(LUMO)` for orbital energies.
- Parse the final HOMO-LUMO gap summary in eV for the gap.

Total energy and relaxation energy:

- Run a single point on the input geometry.
- Run an optimization on the same input.
- Parse final `TOTAL ENERGY ... Eh` values from both outputs.
- Compute `relaxation_energy_eV = max(0, (E_input_Eh - E_optimized_Eh) * 27.211386245988)`.

Dipole moment:

- Use optimized geometry when comparing stable molecular properties.
- Parse the total molecular dipole magnitude in Debye.
- In current xTB output, the `molecular dipole` block can include component rows and a total; prefer the total/full magnitude rather than a vector component.

Molecular polarizability:

- Run on an optimized geometry when possible.
- Parse the molecular `alpha(0)` printout.
- If a size-normalized metric is needed, divide by the heavy-atom count and record that normalization.

Implicit-solvent free energy:

- Use `--alpb <solvent>` for xTB versions that support ALPB; use `--gbsa <solvent>` when ALPB is unavailable or required.
- Parse `Gsolv` in Hartree from each solvent run.

Global electrophilicity:

- Use `--vomega`, usually with GFN1/IPEA-style vertical-property settings exposed by the installed xTB version.
- Run on an optimized geometry if the property should describe a relaxed molecule.

Fukui indices:

- Use `--vfukui`, usually on an optimized geometry.
- Preserve atom indices and symbols exactly as xTB reports them so downstream code can map values back to the input geometry.

Hessian and thermochemistry:

- Use `--ohess` when the intended workflow is optimize-then-Hessian; use `--hess` only when the supplied geometry should be analyzed as-is.
- Parse the imaginary-frequency count to distinguish local minima from saddle points.
- Hessian runs are more expensive than single-point and optimization runs; set longer timeouts.

## Retry and Failure Strategy

- Missing `xtb`: stop the chemistry run and report an environment issue with the attempted executable path.
- Invalid geometry input: validate atom count, coordinate numeric parsing, finite coordinates, plausible distances, and supported elements before running xTB.
- SCC convergence failure: retry with more iterations such as `--iterations 500`; for difficult electronic structures, consider `--etemp` or restarting from generated restart data with `--restart`.
- Geometry optimization failure: retry from a cleaner starting geometry, a lower-level or looser pre-optimization, or a longer timeout. Do not trust properties from an unconverged optimization.
- Hessian imaginary modes: reoptimize more tightly, inspect `xtbhess.coord`, and rerun Hessian on the improved geometry. Treat persistent imaginary modes as a molecular-structure result, not just a tooling failure.
- Solvent failure: check whether the installed xTB version supports the requested solvent and whether the model is `--alpb` or `--gbsa`; switch model or solvent only when the task allows it.
- Timeout: scale by run type. Single-point runs are cheapest, optimization is slower, solvent comparisons multiply the number of runs, and Hessian/thermochemistry usually needs the longest timeout.
- Parser miss: save stdout/stderr and generated files, then inspect version-specific wording before changing chemistry settings.

## Harness Rules

- Keep CLI orchestration separate from property parsing and scoring. A runner should execute commands and return raw artifacts; parsers should extract fields; scoring code should consume structured properties.
- Build commands as argument arrays, not shell strings, unless shell features are truly required.
- Use deterministic file names inside each temporary directory, but do not reuse directories between candidates.
- Record all derived quantities with units and provenance: raw field, unit conversion, geometry source, method, charge, UHF, solvent, and run type.
- Skip live chemistry in automated unit tests when `xtb` is unavailable; use captured stdout fixtures or fake runners for parser and orchestration tests.
- Prefer small smoke molecules for environment checks, but do not infer that a production molecule is valid just because the smoke test passes.
