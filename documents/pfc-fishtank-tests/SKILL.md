---
name: pfc-fishtank-tests
description: Integrate an external, licensed Itasca PFC 5.0 fistPkg26 tree as a reproducible material-generation and compression/diametral/tension test baseline; use to validate its PFC5.0 layout, copy a private working case, preserve provenance, and audit ck/ct/dc/tt/ft extension points for asphalt workflows.
---

# PFC FISHTank (fistPkg) Standard Test Framework

Use this skill to understand and externally reuse Itasca PFC 5.0 FISHTank
`fistPkg26`. Treat it as a PFC 5.0 dependency without requiring a particular PFC5.0
subversion. Its
files remain outside this skills package; the complete asphalt parent is
`pfc5-asphalt-workflow`.

## When To Use

Use this skill when the user needs to:

- Understand what fistPkg (FISHTank) provides and how its directories are laid out.
- Reuse the standard compression / diametral-compression / direct-tension test framework (ct/dc/tt).
- Generate a material specimen with MatGen (linear, contact-bonded, parallel-bonded, flat-jointed, Hill).
- Extend the diametral-compression framework with custom loading heads (e.g. curved heads for a Marshall-type test per JTG T0709).
- Locate the FISH tools (ck/ct/dc/tt/ft/hl) and the Hill DLL installation requirement.

Do NOT use this skill for asphalt-specific modeling choices — those are in `pfc-asphalt-mixture`, `pfc-burger-viscoelastic`, `pfc-marshall-test`, `pfc-rutting-test`.

## Required Inputs

Ask for these if missing:

- Target material type: linear / contact-bonded / parallel-bonded / flat-jointed / Hill (3D UDM).
- Target test: compression (confined/unconfined/uniaxial) / diametral-compression / direct-tension.
- PFC2D or PFC3D 5.0. If another major version is requested, stop: it is outside
  this package.
- Whether the Hill UDM DLL is needed (3D Hill material only).
- Legal `<FISTPKG_ROOT>` and a PFC2D/PFC3D 5.0 runtime.

## fistPkg Capabilities

- **Material genesis**: linear, contact-bonded, parallel-bonded, flat-jointed, and user-defined (3D Hill) materials in polyaxial/cylindrical/spherical vessels; grains as balls or clumps.
- **Material tests**: compression (confined, unconfined, uniaxial strain), diametral-compression, direct-tension.
- **Microstructural monitoring**: grain-size distribution, microstructural plots, crack monitoring for bonded materials.

## Directory Layout

```
fistPkgN/
├── fistPkg-README.txt
├── fistPkg-publicMods.txt
├── Documentation/              ; PDF docs (BPM, FlatJoint, Hill, MatModelingSupport)
└── ExampleProjects/
    ├── fistSrc/                ; FISH source: ck/ct/dc/tt/ft/hl + Hill DLL
    ├── MatGen-Linear / ContactBonded / ParallelBonded / FlatJointed / Hill
    │   └── CompTest / DiamCompTest / TenTest
    └── HillContactModel / FlatJointContactModel / ...
```

## FISH Tool Map

| 工具 | 用途 |
| --- | --- |
| `ft.fis` | FISHTank 主库（核心工具函数：墙-颗粒行为、平衡等） |
| `ck.fis` | 检查/微观结构监测（级配、配位数等） |
| `ct.fis` | 压缩试验（confined/unconfined/uniaxial） |
| `dc.fis` | 劈裂/间接拉伸试验（diametral compression）——马歇尔试验基座 |
| `tt.fis` | 直接拉伸试验 |
| `hl.p3fis` + `udm_hl.p3fis` | Hill 用户自定义接触模型（3D） |
| `contactmodelmechanical3dhill005_64.dll` | Hill 模型 DLL（需安装到插件目录） |

## Workflow

1. Run the self-contained checker:
   `scripts/check_fistpkg.py "<FISTPKG_ROOT>"`.
2. 选材料类型（linear/contact-bonded/parallel-bonded/flat-jointed/Hill）。
3. 按官方 README，把 `ExampleProjects/fistSrc` 与一个 `MatGen-X` 复制到
   私有案例目录；先运行未修改的基线。
4. 生成完成后运行对应试验（CompTest/DiamCompTest/TenTest）。
5. 自定义压头时，以 `_dcMakeWalls` 为最小几何钩子，同时审计墙 ID、
   轴向、接触、平滑、力/位移、终止和后处理。

## Working Rules

- fistPkg is PFC 5.0 — use PFC 5.0 syntax directly and do not generate another
  major-version case from this skill.
- The Hill UDM requires copying the DLL to `PFC500\exe64\plugins\contactmodelmechanical3D` (PFC 5.0 layout).
- Do NOT vendor Itasca's fistPkg source into a public MIT repo — extract usage patterns and command templates only, cite the package as external.
- Reuse the staged, saved-state style (MatGen → CompTest/DiamCompTest/TenTest) for reproducibility.
- Replacing `_dcMakeWalls` is necessary for custom heads but is not by itself a
  complete Marshall validation.

## Output Contract

A complete fistPkg handoff should include:

- Material type and vessel geometry chosen, test type selected.
- Which FISH tools (ck/ct/dc/tt/ft) are needed and how they are called.
- The extension point used (e.g. `_dcMakeWalls` for custom heads).
- Any DLL/plugin installation note.
- A note that the case targets PFC2D/PFC3D 5.0; route other major versions outside this skill.
- The checker result, baseline run result, copied-file manifest and
  `runtime_validated` status.

## Local Contents

- `references/overview.md`: fistPkg capabilities, directory layout, five material types, three tests.
- `references/test-framework.md`: FISH tool usage (ck/ct/dc/tt/ft), Hill DLL installation, and extension points.
- `scripts/check_fistpkg.py`: self-contained, read-only external fistPkg layout/version checker.
- `agents/openai.yaml`: agent interface metadata.
