---
name: pfc-asphalt-mixture
description: Build PFC 5.0 asphalt-mixture specimens with explicit aggregate objects, a declared homogenized-mastic or fine-particle abstraction, residual air voids, measured gradation conversion, contact-pair assignment, compaction, equilibrium, and mass-volume closure; use before Marshall, rutting, creep, or strength tests.
---

# PFC Asphalt Mixture Modeling

Use this skill to build the load-ready digital specimen for asphalt concrete in
PFC2D/PFC3D 5.0. It distinguishes physical phases from DEM objects: aggregate may be
explicit balls/clumps, mastic may be homogenized into contact laws or partly resolved by
fine particles, and air voids remain pore space. This skill produces the specimen only;
the parent route is `pfc5-asphalt-workflow`.

## When To Use

Use this skill when the user needs to:

- Build a PFC asphalt-mixture specimen from scratch (2D or 3D), including a
  source-defined wheel-tracking slab or a standard/large Marshall specimen formed by
  the selected current method.
- Convert an aggregate gradation (AC-13/16/20 级配曲线) into particle counts / clump templates.
- Decide how to assign different contact models across 集料-集料、集料-砂浆、砂浆-砂浆、集料-墙 contact pairs.
- Choose coarse aggregate as clump versus ball, declare the resolvable fine fraction,
  and set a target air-void content from the selected mix design/standard.
- Prepare a reproducible, staged specimen (00_setup → 01_particles → 02_settled → 03_compacted → 04_burger) before any mechanical test.

Do NOT use this skill for loading tests themselves — route those to `pfc-rutting-test`, `pfc-marshall-test`, or `pfc5-standard-tests`.

## Required Inputs

Ask for these if missing:

- Dimension: 2D or 3D; specimen size and provenance. For current Chinese methods,
  record the JTG 3410-2025 forming method separately from the performance method
  (for example T 0702 before T 0709, or T 0703 before T 0719).
- Gradation: AC-13 / AC-16 / AC-20, with sieve passing percentages (or a `gradation_*.csv`).
- Binder content with an explicit convention (binder/aggregate or binder/mixture);
  never convert mass to volume without constituent densities.
- Contact-model plan: which pairs use linear / Hertz / Burger (see `references/overview.md`).
- Target air-void content and the sieve/size boundary between resolved and homogenized
  fractions.
- Measured constituent densities and whether coarse aggregate uses clump templates.
- Aggregate test provenance from JTG 3432-2024 or the applicable project/laboratory
  record, including sieve, density/absorption and any shape metric used to justify the
  DEM representation.

## Three-Phase Characterization

Asphalt mixture = 三相复合材料. Model each phase distinctly:

Keep the physical gradation classification separate from the DEM resolution boundary.
Any sieve value below is project/specification data, not a universal switch that forces
one PFC object type.

| 相 | 物理组成 | PFC 表示 |
| --- | --- | --- |
| 项目定义的粗集料 | 按所选级配/规范定义 | clump、ball 或其他已验证形状表示；由形状目标和分辨率决定 |
| 项目定义的细集料+矿粉 | 按所选级配及可分辨尺度定义 | 可解析为 ball/clump，或并入均质砂浆/接触抽象；必须声明截断边界 |
| 沥青砂浆 | 沥青 + 细料 + 矿粉的均质化胶浆 | 可由接触模型等效；这不是显式砂浆体积 |
| 空隙 | 项目/试验/规范给定的目标空隙率 | 颗粒间剩余孔隙（压实控制并做质量-体积闭合） |

Two common modeling routes:
- **Route A (homogenized mastic)**: explicit aggregate plus a calibrated contact law.
  It is economical, but binder/mastic mass is not automatically represented by object
  volume.
- **Route B (resolved fines)**: add resolvable fine/filler particles and define
  aggregate-fine/fine-fine interfaces. Binder may still be homogenized at contacts, so
  do not call this a literal three-particle-phase model unless binder objects exist.

## Gradation Conversion

Convert sieve passing percentages into retained-bin mass/volume fractions, then into
resolved objects only after applying constituent densities and the declared DEM cutoff.
See `references/gradation.md` for the user-input schema and conversion procedure. It
deliberately does not bundle standard gradation tables. Key rule:
各档留存比例 = 相邻筛孔通过率之差；object type follows the declared shape/resolution
abstraction rather than a fixed sieve; target volumes must satisfy the selected binder
convention, constituent densities, air voids and mass-volume closure.

## Contact-Model Assignment

| 接触对 | 推荐模型 | 说明 |
| --- | --- | --- |
| 集料-集料 | linear 或经论证的 bonded law | linear 表示无黏结摩擦；contact bond 不能标成“无黏结” |
| 集料-等效砂浆界面 | Burger 或标定的界面模型 | 只有相应对象/分组存在时才能分配 |
| 细料-细料/砂浆等效接触 | Burger | 需由宏观蠕变/动态响应反演 |
| 集料-墙/压头 | 经标定的 linear 或适用界面模型 | 钢模、压头、橡胶轮及润滑条件分别标定；不预设“高摩擦” |

Details and PFC command templates in `references/overview.md` and the sibling skill `pfc-burger-viscoelastic`.

## Default Modeling Pipeline (Staged, Resumable)

Use this as a default auditable route. Stage names may be renamed, merged or skipped for
imported specimens or alternative preparation methods if the same state provenance,
checks and restart points remain explicit.

1. `setup`: create the domain and dimensionality-appropriate specimen boundaries, save `00_setup`.
2. `particles`: generate the declared resolved fractions with the selected ball/clump/shape abstraction, save `01_particles`.
3. `settle`: use the declared deposition/compaction preparation; identify and treat floaters with a stated criterion rather than deleting them automatically, save `02_settled`.
4. `compact`: top-wall downward compaction to target porosity/height, save `03_compacted`.
5. `contacts`: audit existing contacts and future `cmat` defaults, install final
   contact models with a PFC5-verified procedure, re-equilibrate, save `04_contacts`.
6. Hand off the load-ready specimen to `pfc-rutting-test` / `pfc-marshall-test` / `pfc5-standard-tests`.

## Working Rules

- Use PFC 5.0 `cmat` semantics and reject unsupported newer-major command
  families. This package does not maintain a cross-version migration route.
- Fix the random seed and record it — asphalt specimen generation must be reproducible.
- Select the generator intentionally: PFC5 `ball/clump distribute` targets an
  overlap-uncorrected porosity and can create large overlaps, while
  `ball/clump generate` rejects overlaps but may stop at its tries limit before the
  requested count. Neither command alone proves the achieved post-compaction voids.
- Use the user's measured/project gradation and name the governing specification
  edition. Do not reconstruct or supply a standard gradation table when the user has not
  provided legally sourced project inputs.
- Keep aggregate characterization, mixture forming and performance testing as separate
  source records. A T 0302/T 0327 sieve result, a T 0702/T 0703 forming procedure and a
  T 0709/T 0719 performance result are not interchangeable provenance fields.
- Prefer validated non-spherical representations when aggregate shape/interlock is a target;
  balls are acceptable when the simplification is declared and its effect is checked.
- Preserve logically distinct milestone states and their checks. The example names are
  `00_setup`, `01_particles`, `02_settled`, `03_compacted`, `04_contacts`; a project may
  combine or rename them if restartability and audit evidence are retained.
- Verify mass/volume closure and achieved air-void content; neither a remembered
  3–5% range nor specimen height alone is a universal acceptance criterion.

## Output Contract

A complete specimen handoff should include:

- Dimension, gradation table, resolved/homogenized cutoff, representation choice, and object counts by group.
- The staged save list with file names and what each stage achieved.
- Contact-model assignment table (which pair → which model + key properties).
- Achieved porosity vs target porosity (压实验证).
- A clear note that loading tests continue in `pfc-rutting-test` / `pfc-marshall-test` / `pfc5-standard-tests`.

## Local Contents

- `references/overview.md`: three-phase characterization, contact-model strategy, and the staged pipeline with a transactional contact-switch rule.
- `references/gradation.md`: user-supplied gradation schema and the volume-to-object conversion procedure; no standard data tables.
- `../pfc5-asphalt-workflow/references/standards-method-map.md`: reviewed standard roles and the aggregate-to-performance method chain.
- `scripts/minimal_specimen_smoke.p3dat`: complete six-wall PFC3D 5.0 command-flow smoke test; not a production asphalt specimen.
- `dependencies.json`: package-level links to the PFC5 parent and Burger specialist.
- `agents/openai.yaml`: agent interface metadata.
