---
name: astrophotography-processing
description: Router for astrophotography processing, troubleshooting, and safe workflow guidance across deep-sky, narrowband, planetary/lunar/solar, Milky Way landscape, comet, and mosaic data.
when_to_use: Use when the request involves astrophotography processing, FITS/XISF/RAW night-sky data, stacking, calibration frames (lights/darks/flats/bias/dark-flats), narrowband/OSC/LRGB workflows, Milky Way processing, comet processing, lunar/planetary/solar stacking, mosaics, PixInsight/Siril/APP/DSS, StarNet or StarXTerminator-style star workflows, or Python-based astro image audits/automation. Do not use for ordinary daytime portrait/product/photo editing unless the user is explicitly processing astronomy/night-sky data.
argument-hint: "[image-or-folder] [software/workflow]"
---

# Astrophotography Processing

## Purpose

Help users produce technically sound astrophotography results while preserving original data, metadata, and reproducibility.

## Use When

Use this skill only when context clearly indicates astrophotography or night-sky imaging workflows.

Trigger examples:

- Telescope/lens star fields, deep-sky objects, Milky Way, comet, lunar/planetary/solar data
- Calibration frames, stacking, registration, gradient removal, color calibration
- FITS/XISF/RAW subs, linear masters, rejection maps, dithering, deconvolution
- PixInsight, Siril, Astro Pixel Processor, DeepSkyStacker, StarNet, StarXTerminator, WinJUPOS, Python astro pipelines

## Do Not Use When

- General photo editing requests without astronomy context
- Fashion, portrait, product, wedding, travel edits not involving night-sky capture workflows

## Operating Mode

Choose one primary mode and label it in the response:

- Diagnosis: inspect visible or file-based issues and identify likely causes.
- Workflow: provide ordered processing steps for available data and software.
- Recovery: repair a specific artifact or failed stage with minimal rework.
- Automation: provide scripts, batch commands, or repeatable organization.
- Scientific preservation: preserve measurement integrity and metadata over cosmetic output.

## Evidence Rules

- Separate observed issues from likely causes.
- If only JPEG/PNG/screenshot is available, do not make firm claims about calibration quality, original bit depth, Bayer pattern correctness, clipping in source linear data, or linear behavior.
- Prefer original linear masters, calibrated subs, FITS/XISF headers, and processing history before recommending irreversible fixes.
- If files are unavailable, provide a cautious diagnosis and the smallest next test that can confirm/refute the hypothesis.

## Minimal Questions Policy

Keep intake lightweight.

- Ask at most 3 high-value questions first when critical context is missing.
- If the user wants immediate guidance, proceed with reasonable assumptions and label assumptions explicitly.
- Do not dump the full intake checklist unless requested.

High-value intake checklist (internal use):

1. Image type: deep-sky, planetary/lunar/solar, comet, Milky Way landscape, mosaic.
2. Input stage: raw subs, calibrated/registered subs, linear master, stretched image.
3. Data/software: FITS/XISF/RAW/TIFF/SER and PixInsight/Siril/APP/DSS/Photoshop/Lightroom/GIMP/Affinity/Python.
4. Capture and calibration basics: camera/optics/filter, exposure/gain/ISO/temp, darks/flats/bias/dark-flats.
5. Desired output: aesthetic presentation, troubleshooting, or scientific/photometric integrity.

## Local File Inspection Protocol

When local files are available:

1. Inspect directory layout before proposing exact steps.
2. Identify file types and separate lights, calibration frames, masters, and exports.
3. Read metadata where possible: exposure, gain/ISO, temperature, filter, Bayer pattern, dimensions, bit depth, date/session, object.
4. Summarize findings before recommending processing.
5. Never modify source files.
6. Write previews, audits, and generated outputs to process/ or exports/.
7. If tooling is unavailable, fall back to filenames, folder structure, image dimensions, and user notes.

Helper scripts:

- scripts/fits_audit.py
- scripts/image_stats_preview.py

## Workflow

Default deep-sky sequence unless software requires a variant:

1. Organize data by session/filter/exposure/gain-temp.
2. Calibrate with matched darks/flats/bias-or-dark-flats.
3. Quality control and reject poor subframes.
4. Register with stable reference geometry.
5. Normalize/integrate with robust rejection.
6. Linear stage: crop, gradient removal, color calibration, linear denoise, optional decon/sharpen.
7. Stretch while protecting black point and star cores.
8. Nonlinear finishing with restrained contrast/saturation/star handling.

Detailed decision guides:

- Calibration details: references/calibration.md
- PixInsight: references/pixinsight.md
- Siril: references/siril.md
- APP, DSS, Photoshop, Lightroom, GIMP, Affinity: references/app-dss-photoshop.md
- Planetary/lunar/solar: references/planetary-lunar-solar.md
- Milky Way landscape: references/milky-way-landscape.md
- Comets, mosaics, OSC dual-narrowband: references/comets-mosaics-dualband.md
- Artifact recovery: references/troubleshooting.md

## Constraints

- Do not use SCNR as a substitute for proper color calibration.
- Apply green cast/noise suppression only after color calibration and only when appropriate.
- Do not use Lightroom/ACR as the raw converter for calibration subframes unless this is a landscape workflow.
- Optional WinJUPOS/de-rotation may help Jupiter/Saturn/Mars workflows.
- Avoid presenting fixed numeric settings as universal; use adjustable starting ranges with visual/statistical checks.

## Scientific or Photometric Mode

When the goal is analysis/measurement:

- Preserve linear calibrated data.
- Avoid cosmetic star removal, generative edits, aggressive denoising, star reduction, local contrast boosts, or nonlinear color manipulation in the measurement version.
- Preserve FITS headers, WCS/plate-solve info, exposure metadata, and processing logs.
- Export a presentation copy separately from the analysis master.

## Solar Safety

For solar data, do not provide capture advice that implies viewing or imaging the Sun without a proper front-mounted solar filter or a purpose-built solar telescope. Processing guidance is allowed; unsafe capture assumptions must be corrected briefly.

## Export and File Safety

- Never overwrite RAW/FITS/XISF/SER/AVI/MOV/original TIFF sources.
- Preserve linear masters in 32-bit FITS/TIFF or equivalent.
- Use 16-bit TIFF for nonlinear finishing.
- Use JPEG/PNG only for sharing.
- Encourage use of templates/processing-log.md for reproducibility.

## Default Response Structure

For normal requests, respond in this order:

1. Likely issue or recommended path
2. Assumptions based on available data
3. Ordered workflow
4. Checks after each major stage
5. What not to do
6. Suggested filenames/outputs

For shared images, respond in this order:

1. Visible issues
2. Likely causes
3. Tests to confirm
4. Smallest next edit
5. Longer reprocessing recommendation (if needed)

## Help And Examples

Ask for the image/data stage and the user's processing software, using the minimal questions policy above. Examples:

- "Help me process my Orion Nebula FITS stack in PixInsight."
- "Why do my stacked images still have dust donuts?"

## Validation Checklist

- [ ] Original captures and linear masters are preserved.
- [ ] Observations are distinguished from hypotheses and missing evidence.
- [ ] The workflow matches the data stage, software, and intended scientific or presentation use.
- [ ] Solar safety and non-destructive export rules are respected.
