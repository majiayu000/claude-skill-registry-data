---
name: apparadise
description: >-
  Domain guide for apparadise, the CUDA software platform for HPC that builds each package once
  per target (vr Vera Rubin aarch64, rtx x86-64 sm_120, generic sm_75-sm_120) as a signed OCI
  image and exposes it as a container and as `module load`. Use this skill whenever you work in
  the apparadise repo (resolver, index, recipes, builder, repairs, failure DB, catalog) or when
  someone asks which HPC package manager or software stack to use for a CUDA package:
  EasyBuild vs Spack vs pixi/conda-forge, whether EESSI or E4S can help, how to pick
  cuda_arch / cuda_compute_capabilities / compute capability values, PTX and sm_120/Blackwell
  or Rubin support, toolchain/CUDA/GCC compatibility, or how to build HPC software into
  containers (Spack containerize, eb, pixi in Docker/Podman, Enroot/Pyxis). Trigger even if
  the user only names one of these tools or asks "how do I get X with CUDA on our cluster".
---

# apparadise: CUDA software stacks for HPC

apparadise builds CUDA software **once per hardware target** and ships every build as a signed
OCI image in the **Zot** registry (moved from Harbor on 2026-11-01). The image is the only build product. It is
run as a container (Pyxis/Enroot on Slurm, Run:ai on Kubernetes) and as
`module load <name>/<version>` through Enroot wrappers over a pre-staged `.sqsh` on CephFS.

Read `README.md` and `CLAUDE.md` ("Decisions already made") in the repo before changing design.
Product decisions are never guessed: open questions go to `QUESTIONS.md`, newest first.

## Hard rules (decided; do not re-litigate)

- **One image, one source, one solver.** Never mix Spack, EasyBuild and conda-forge in one
  image, not even for a single dependency.
- **Resolver order is fixed:** requester's choice → pixi (only if conda-forge has CUDA builds
  for *both* linux-64 and linux-aarch64) → Spack with a `cuda` variant → EasyBuild CUDA
  easyconfig → CUDA port attempt (Spack, then EasyBuild, then pixi) → `no-recipe` failure.
- **Targets:** `vr` (Vera Rubin NVL72, aarch64; CC still unknown, Q13, so `vr` builds refuse to
  render), `rtx` (x86-64-v4, RTX PRO 6000 Blackwell, `sm_120`, CUDA 13.0.3), `generic`
  (`sm_75`–`sm_120`, CUDA 13.0.3; Volta/`sm_70` dropped, Q38). Always embed PTX for the
  highest arch. Prefer family (`f`) over arch-specific (`a`) targets. Tag
  `<name>:<version>-<target>` under a multi-arch manifest. `containers/targets.yml` holds every
  arch flag.
- **Build natively, never under QEMU.** Builders need a CPU of the target arch but no GPU. GPU
  tests run on real nodes as low-priority jobs.
- **Six stages:** `resolve → generate → build → package → test → publish`. Failure stages are
  fixed: `no-recipe`, `concretize`, `build`, `package`, `test`, `publish`.
- **Base images derive from NGC** (`nvcr.io`). Slurm runtime is Pyxis + Enroot only; no
  Apptainer, no shpc.
- **Images run as any UID** (Q36): Pyxis runs them as the user, Run:ai takes UID/GID from AD,
  and Kubernetes cannot map root inside to the user outside. So install trees are `a+rX`,
  there is no entrypoint, `USER 65534:65534`, and the `package` stage checks it as uid 54321
  (`docs/operations/user-identity.md`). Never make a recipe or image need root at runtime.
- **EESSI and E4S are not build sources.** They are complements (see their sections). Never
  propose either as a resolver step, an image base or a builder mirror; that would be an owner
  decision for `QUESTIONS.md`.

## Choosing a tool

Start at **`references/decision-tree.md`**. It has the Mermaid and ASCII trees, the concrete
check at each resolver node, the complementary EESSI/E4S paths, per-target notes and a
comparison table of all five tools. Read it whenever the question is "which tool for this
package/target?" or "why did the resolver pick X?".

For detail on one tool, read only its reference file (each is 350–520 lines, with cheat sheet,
failure table and links):

| Tool | Reference | Role in apparadise |
|---|---|---|
| pixi / conda-forge | `references/pixi-conda.md` | resolver rule 2 |
| Spack | `references/spack.md` | resolver rule 3, first in CUDA port |
| EasyBuild | `references/easybuild.md` | resolver rule 4 |
| EESSI | `references/eessi.md` | complement: easyconfig/hook reference, optional host module stack |
| E4S | `references/e4s.md` | complement: reference Spack environments, known sm_120 failures |

Facts marked **(unverified)** in the references are unverified; carry the mark forward when you
repeat them.

## pixi / conda-forge

- **What:** conda-forge is the community binary channel (one feedstock per package, CI-built for
  linux-64 and linux-aarch64). pixi (pinned 0.83.0) is the project manager that writes a
  multi-platform `pixi.lock`. Binaries are used as published: **you do not choose arch flags**,
  the feedstock does.
- **CUDA:** conda-forge builds CUDA 12.9 and 13.4 variants. PyTorch, jaxlib, CuPy and vLLM have
  CUDA builds on both arches and cover sm_120 (+PTX). All targets are CUDA 13.0 now (Q38),
  so every pixi recipe declares `cuda = "13"`. **TensorFlow has no linux-aarch64 CUDA build**, so it fails rule 2.
- **In apparadise:** rule 2 needs `has_cuda`, `is_python`, CUDA builds on both subdirs, and no
  non-`py-` CUDA recipe in Spack (so GROMACS/LAMMPS go to Spack). Lock/solve failure →
  `concretize`; install failure → `build`.
- **Gotchas:** declare `cuda` on the platform or you silently get CPU builds; GPU-less builders
  need `CONDA_OVERRIDE_CUDA`; use conda-forge only (no `defaults`, `pytorch`, `nvidia` channels);
  never mix pip CUDA wheels with conda CUDA libs; keep the env path identical across container
  stages; the template pins `cuda-version = "<=<target CUDA>"` (<=13.0; PyTorch 2.14 has only 12.9 builds), because an unpinned
  solve picks the newest runtime (nvrtc 13.4 on a 13.0 base, seen with cupy); some CUDA-only
  packages (CuPy) carry no `cuda` in their build string, so the index turns the `*cuda*`
  build filter off for them; `[system-requirements]` is deprecated but still read by 0.83.

Detail: `references/pixi-conda.md`.

## Spack

- **What:** from-source HPC package manager (pinned v1.2.2) with a clingo solver; one
  `package.py` per package; recipes live in the separate `spack/spack-packages` repo since 1.0.
  Best for compiled HPC codes with MPI/CUDA/BLAS variants and per-target CPU tuning.
- **CUDA:** `CudaPackage` adds `+cuda` and `cuda_arch`. `120` needs CUDA 12.8+, `120f` needs
  12.9+, `70` is limited to CUDA ≤12.9. Rubin `107*` exists only in newer spack-packages and
  needs `cuda@13.4:` (Spack's claim, unverified). Host-GCC conflicts: CUDA 12.7–12.9 allows GCC
  ≤14, CUDA 13.0–13.3 GCC ≤15, 13.4 GCC ≤16.
- **In apparadise:** rule 3 and first in `PORT_ORDER`. Targets: `rtx` `x86_64_v4`, `generic`
  `x86_64_v3`/`aarch64`, `vr` `neoverse_v2` (Vera's `olympus` not in Spack 1.2.2). CUDA is
  always a `buildable: false` external from the NGC base. Repairs can append `^dep~variant` or
  `flag==` propagation, which EasyBuild cannot express.
- **Gotchas:** spec order matters in 1.x (`+cuda` after a `^dep` lands on the dependency; the
  renderer puts root variants first since 2026-11-01); pin spack-packages and pre-clone it for
  network-restricted builders; `packages: all: variants:` is only a preference; verify PTX with
  `cuobjdump --list-ptx`.

Detail: `references/spack.md`.

## EasyBuild

- **What:** Python framework (pinned 5.4.2) that builds from curated, fully version-pinned
  easyconfigs per toolchain generation (`foss-2025b` = GCC 14.3; newest is `2026.1`, not
  `2026a`). No solver: dependencies must exist at the exact pinned versions.
- **CUDA:** no CUDA toolchain; CUDA is a dependency and the easyconfig gets `-CUDA-<x.y.z>`
  (2025b→12.9.1, 2026.1→13.3.0). `cuda-compute-capabilities` uses dotted values (`12.0`); the
  CUDA sanity check wants device code for every CC plus PTX for the highest, but only warns by
  default.
- **In apparadise:** rule 4, picked only when Spack has no CUDA recipe (or on request). The
  renderer writes an easystack with `optarch`, `cuda-compute-capabilities`,
  `try-toolchain: foss,2026.1` + `try-update-deps` (experimental; without it the bump keeps
  dependency versions 2026.1 lacks) and `filter-deps: CUDA`; on a `concretize` failure the
  `easybuild-toolchain-fallback` repair moves to `foss,2025b`, then to the easyconfig's own.
- **Gotchas:** with `filter-deps: CUDA` and no `EBROOTCUDA`, easyblocks may take their **CPU
  path** and the sanity check is skipped (the builder sets `EBROOTCUDA`/`EBVERSIONCUDA`, fails
  on CUDA sanity-check errors and opts in to running as root); `--try-amend` reaches only the
  top-level easyconfig; never `--ignore-osdeps`; `optarch` needs the full `GCC:-march=...`
  flag; builders run `eb --robot --dry-run` as the `concretize` stage; the index ranks `2026.1`
  above `2025b`.

Detail: `references/easybuild.md`.

## EESSI (complement, not a source)

- **What:** a ready-built EasyBuild stack streamed over CernVM-FS (`/cvmfs/software.eessi.io`)
  with a Gentoo Prefix compat layer and Lmod modules, autodetecting CPU and GPU target.
  Versions 2023.06, 2025.06 (foss 2024a–2025b) and 2026.06 (foss 2026.1).
- **CUDA:** builds only major CCs (7.0/7.5, 8.0, 9.0, 10.0, 12.0) with `f`/`a` suffixes; sm_120
  is covered in 2025.06+. Ships CUDA runtime libs only; drivers and the SDK go through
  `host_injections`. No CUDA PyTorch/TensorFlow/JAX. No Rubin target, Vera detection unverified.
- **Fits apparadise as:** (1) a **reference for CUDA easyconfigs and hooks** (its easystacks
  list easyconfigs that built and passed on sm_90/100/120; `eb_hooks.py` catalogues CUDA
  workarounds; 2025.06's `foss/2025b` matches apparadise's toolchain); (2) an **optional host
  module stack** on nodes that already run CVMFS, separate from apparadise's modules.
- **Gotchas:** every node needs CVMFS (root, FUSE, Squid); no OCI images or digests; per-node GPU
  setup re-run after each driver update; don't mix module trees; Enroot/Pyxis use undocumented.

Detail: `references/eessi.md`.

## E4S (complement, not a source)

- **What:** a curated Spack-based distribution (125+ HPC products) delivered as `spack.yaml`
  environments, a signed binary cache (`cache.e4s.io/<release>`) and 30+ GB monolithic images.
  Current release 26.06 (Spack 1.1.1); 26.11 in preparation on Spack v1.2.2.
- **CUDA:** one `cuda_arch` per environment (x86_64 80/86/89/90/120, aarch64 80/90/120), no
  sm_100/103, no Rubin, no `f` targets; Spack binaries are CUDA 12.9.1 although slides say 13.2.
- **Fits apparadise as:** a source of **reference Spack environments** (known-good `+cuda`
  variant sets to borrow for `--spec`) and of **known sm_120 failures**: the commented-out
  "not installed" block in `environments/*/gnu/cuda/120/spack.yaml` (cp2k, cabana/kokkos 4.6,
  dealii, mfem, lbann, exago, paraview+cuda, ascent). Check it before a failure lands in the
  public failure DB.
- **Gotchas:** cache hit rate for apparadise `+cuda` specs is effectively zero (`x86_64_v3` vs
  `v4`, CUDA 12.9.1 vs 13.0.3/12.9.2, single vs multi-arch); images are non-NGC and
  multi-product, so never catalog or re-tag them; `cache.e4s.io/<e4s_release>` is a second, signed
  mirror in every rendered `spack.yaml` (Q35, owner), keys trusted in the build stage; e4s-cl has no Enroot backend.

Detail: `references/e4s.md`.

## Working in the repo

- Code lives in `web/apparadise/` (`resolver.py`, `index.py`, `recipes.py`, `buildqueue.py`,
  `repair.py`), `builder/apparadise_builder/agent.py`, `recipes/_templates/`,
  `recipes/repairs.yml` and `containers/targets.yml`. `builder/` never imports from `web/`.
- Render a recipe to inspect it:
  `python -m apparadise.recipes spack gromacs 2026.3 rtx --spec gromacs@2026.3+mpi --stdout`
  (run from `web/`; `easybuild ... --easyconfig X.eb` and `pixi` work the same way).
- When a reference marks something as an "observation" or "finding, not yet a fix", treat it as
  a candidate change that needs a test and, if it touches product behaviour, a `QUESTIONS.md`
  entry, not a silent fix.
