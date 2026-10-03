---
name: wpf-gui-compilation
description: Use when when you have cloned the MsdialWorkbench repository and need
  to produce an executable WPF GUI application (MsdialGuiApp) for Windows.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - ReactiveExtensions
  - ReactiveProperty
  - .NET Standard
  - Visual Studio 2022
  - .NET Framework 4.7.2
  - WPF (Windows Presentation Foundation)
  - NuGet Package Manager
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.0c01980
  title: CorrDec
evidence_spans:
- utilizing packages such as ReactiveExtensions and ReactiveProperty
- The .NET class libraries adhere at least to the specifications of .NET Standard
  2.0
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_corrdec_cq
    doi: 10.1021/acs.analchem.0c01980
    title: CorrDec
  dedup_kept_from: coll_corrdec_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.0c01980
  all_source_dois:
  - 10.1021/acs.analchem.0c01980
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# wpf-gui-compilation

## Summary

Compile a Windows Presentation Foundation (WPF) graphical user interface from .NET source code using Visual Studio, targeting .NET Framework 4.7.2 with ReactiveExtensions and ReactiveProperty dependency management. This skill is essential when building desktop mass spectrometry analysis software from source that requires UI-driven interaction.

## When to use

When you have cloned the MsdialWorkbench repository and need to produce an executable WPF GUI application (MsdialGuiApp) for Windows. Use this skill when you intend to build from source rather than use pre-compiled release binaries, or when you need to verify reproducible builds or modify the UI layer.

## When NOT to use

- Input is a pre-compiled release binary from GitHub releases — use directly without compilation
- Target platform is non-Windows (Linux, macOS) — WPF is Windows-only; consider alternative UI frameworks
- You only need the vendor-supported version with proprietary mass spectrometry data format readers — use official release binaries instead of 'vendor unsupported' source builds
- Build environment lacks Visual Studio or .NET Framework 4.7.2 runtime — compile in an environment with both prerequisites

## Inputs

- MsdialWorkbench GitHub repository (cloned)
- MsdialGuiApp.csproj project file
- Solution file (MsdialWorkbench.sln)
- .NET Framework 4.7.2 runtime
- Visual Studio 2022 with .NET desktop development workload

## Outputs

- Compiled WPF executable (MSDIAL.exe)
- Binary assemblies in bin/Debug or bin/Release directory
- NuGet dependency resolution log
- Build output diagnostics

## How to apply

Clone the MsdialWorkbench repository, open the MsdialGuiApp.sln project in Visual Studio 2022 with .NET desktop development workload installed, and verify the build target is .NET Framework 4.7.2. Add the Assemblies folder from the repository to Visual Studio's NuGet package sources, then restore dependencies (ReactiveExtensions and ReactiveProperty packages). Select the appropriate solution configuration (e.g., 'Debug vendor unsupported' for open-source builds or 'Release' for vendor-supported builds). Compile the WPF application using Visual Studio's build system (Ctrl+Shift+B or Build > Build Solution), monitoring the Output window for compilation errors. Verify that the executable binary (MSDIAL.exe or equivalent) is generated in the bin/Debug or bin/Release directory. Finally, launch the compiled application on a Windows system with .NET Framework 4.7.2 runtime installed and confirm it initializes without errors and the UI renders correctly.

## Related tools

- **Visual Studio 2022** (IDE for compiling WPF project, restoring NuGet packages, and building executables) — https://visualstudio.microsoft.com/
- **.NET Framework 4.7.2** (Compilation target framework and runtime for MsdialGuiApp)
- **WPF (Windows Presentation Foundation)** (UI framework used for GUI implementation in MsdialGuiApp)
- **ReactiveExtensions** (NuGet dependency package for reactive programming patterns in WPF UI)
- **ReactiveProperty** (NuGet dependency package for property binding in reactive WPF UI)
- **NuGet Package Manager** (Dependency resolver and package loader for Visual Studio compilation)

## Examples

```
# In Visual Studio: Right-click MsdialGuiApp → Set as Startup Project; select 'Debug vendor unsupported' configuration; press Ctrl+Shift+B to build. Verify MSDIAL.exe appears in bin/Debug/. Alternative: dotnet build MsdialWorkbench.sln -c Debug -f net472
```

## Evaluation signals

- No compilation errors reported in Visual Studio Output window; build completes with 'Build succeeded' message
- Executable file (MSDIAL.exe) exists and has non-zero file size in bin/Debug or bin/Release directory
- All NuGet packages (ReactiveExtensions, ReactiveProperty) are successfully restored; no unresolved dependency warnings
- Application launches without runtime exceptions on Windows system with .NET Framework 4.7.2 installed
- WPF UI window renders correctly with all UI elements visible and responsive to input

## Limitations

- The 'Debug/Release vendor unsupported' configuration does not support proprietary mass spectrometry data formats (only abf, cdf, mzml); use official release binaries for vendor SDK support
- Unit testing infrastructure for partial functionalities is not currently set up for trial, limiting test-driven verification of compiled UI components
- Reproducible builds are only guaranteed for MS-DIAL version 5 series; earlier versions may not compile consistently from source
- Compilation requires Windows with Visual Studio 2022 and .NET Framework 4.7.2; cross-platform builds are not supported
- NuGet package sources must include the Assemblies folder from the repository; build will fail if this custom source is not configured

## Evidence

- [methods] we are using the WPF (Windows Presentation Foundation) UI framework for GUI implementation: "we are using the WPF (Windows Presentation Foundation) UI framework for GUI implementation"
- [methods] we primarily utilize the frameworks of .NET Framework 4.7.2, .NET Core 3.1, and .NET 6: "we primarily utilize the frameworks of .NET Framework 4.7.2, .NET Core 3.1, and .NET 6"
- [methods] utilizing packages such as ReactiveExtensions and ReactiveProperty: "utilizing packages such as ReactiveExtensions and ReactiveProperty"
- [other] Restore NuGet dependencies including ReactiveExtensions and ReactiveProperty packages. Compile the WPF-based GUI application using Visual Studio's build system.: "Restore NuGet dependencies including ReactiveExtensions and ReactiveProperty packages. Compile the WPF-based GUI application using Visual Studio's build system."
- [readme] Double click `MsdialWorkbench.sln` in the cloned repo... Click `Manage NuGet Packages for Solution...`. Add the `Assemblies` folder in this repo to the **Package source:**. Select `Debug vendor unsupported` from the `Solution Configurations` pull-down menu.: "Double click `MsdialWorkbench.sln` in the cloned repo... Click `Manage NuGet Packages for Solution...`. Add the `Assemblies` folder in this repo to the **Package source:**."
- [other] Verify the executable binary is generated in the output directory (e.g., bin/Release or bin/Debug). Confirm the application launches without errors on a Windows system with the required .NET Framework 4.7.2 runtime.: "Verify the executable binary is generated in the output directory (e.g., bin/Release or bin/Debug). Confirm the application launches without errors on a Windows system with the required .NET"
- [readme] Due to licensing restrictions, this version cannot read proprietary data formats from mass spectrometry manufacturers. However, the [release versions](https://github.com/systemsomicslab/MsdialWorkbench/releases) distributed with official releases can read these proprietary formats.: "Due to licensing restrictions, this version cannot read proprietary data formats from mass spectrometry manufacturers. However, the [release versions] distributed with official releases can read"
