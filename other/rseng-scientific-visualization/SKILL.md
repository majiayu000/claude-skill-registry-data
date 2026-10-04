---
name: rseng-scientific-visualization
description: >-
  Covers visualization of scientific data beyond publication figures: 3D and
  volumetric rendering with ParaView and VTK, scripted and reproducible
  visualization pipelines, state files and Python trace for repeatability,
  in-situ visualization of running simulations, web-delivered interactive 3D
  (trame-style apps), and choosing honest colormaps and representations for
  spatial data. Use when the user works with 3D, volumetric, mesh or
  simulation output data, mentions ParaView, VTK or interactive 3D viewers,
  needs a visualization others can regenerate, or wants to inspect large
  simulation results.
license: CC-BY-4.0
metadata:
  version: 0.1.0
---

# Scientific visualization

Scientific visualization turns meshes, fields and volumes into
understanding - and, done as engineering rather than clicking, into
REPRODUCIBLE artifacts: a figure or animation anyone can regenerate
from data plus a script. The reference stack is VTK (the rendering
and data-processing library) and ParaView (the application built on
it, scriptable in Python); the practices below outlast any one tool.

## Reproducibility first

An interactively composed visualization is a dead end the moment it
is needed again. Make visualizations regenerable:

- Script the pipeline: ParaView's Python tracing records interactive
  work as a pvpython script - clean it, parameterize the input path,
  and commit it next to the analysis code
  (rseng-version-control-review).
- State files capture a full session as a restorable artifact;
  scripts beat state files for review and parameterization, state
  files beat nothing.
- Treat visualization scripts as code: inputs and camera/colormap
  parameters in configuration, outputs written to a results
  directory, runnable headless in the pipeline (rseng-workflows) so
  figures regenerate when data changes.
- Record the tool version with the output - renderers evolve, and a
  pinned environment (rseng-reproducible-environments) keeps
  animations regenerable years later.

## Honest representation

- Colormaps: perceptually uniform by default (viridis-class);
  rainbow/jet-class maps create false boundaries and mislead - flag
  them on sight. Diverging maps only for data with a meaningful
  center; always show the colorbar with units
  (rseng-scientific-file-formats' unit discipline pays off here).
- Respect the data's structure: do not interpolate across
  discontinuities, do not volume-render categorical data, state
  isovalue choices - an isosurface at an arbitrary threshold is an
  editorial decision and should be a labeled parameter.
- Accessibility applies: colorblind-safe maps, readable annotation
  sizes in videos and figures (rseng-ux-accessibility).

## Scale: large data and in-situ

- Larger-than-memory results: use parallel/distributed rendering
  (pvserver) or level-of-detail decimation for interaction, full
  resolution for final renders; chunk-friendly file layouts
  (rseng-scientific-file-formats) decide how painful this is.
- In-situ visualization (ParaView Catalyst-style) renders DURING the
  simulation instead of writing everything to disk - the escape
  hatch when output volume makes post-hoc analysis impossible;
  it changes I/O planning (rseng-hpc-computing).
- Batch renders of animations belong on the cluster as jobs, not on
  laptops overnight (rseng-hpc-computing).

## Sharing and interaction

- Web delivery lets collaborators explore 3D results without
  installing anything: trame-style Python apps expose a VTK/ParaView
  pipeline in the browser; a hosted viewer is a research service
  with operational needs when it outlives a demo.
- For talks and papers, render key frames as static figures with the
  same scripted pipeline - one source of truth for interactive and
  print outputs (rseng-science-communication for the framing).

## Working with this skill

This skill is source-independent: its authority is the VTK and
ParaView documentation linked below.

Learn more (verified):
  - https://docs.paraview.org/en/latest/ - ParaView documentation
  - https://vtk.org - the Visualization Toolkit
  - https://kitware.github.io/trame/ - trame web framework for
    VTK/ParaView apps

<!-- related-skills:begin -->

## Related skills

Check whether any of these applies before moving on:

- rseng-hpc-computing - parallel rendering and in-situ output
- rseng-reproducibility - regenerable figures from scripts
- rseng-science-communication - framing figures for talks and papers
- rseng-scientific-file-formats - mesh and volume data layouts
- rseng-ux-accessibility - colorblind-safe maps and annotations
- rseng-workflows - figures regenerate inside pipelines

<!-- related-skills:end -->
