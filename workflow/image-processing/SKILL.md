---
name: image-processing
description: "Understand, inspect, or programmatically transform existing images. Use when the task requires describing or answering questions about an image, performing deterministic image manipulation such as downscaling, cropping, format conversion, or compression, or running traditional computer vision operations."
compatibility: opencode
---

# Image Processing

## When to Use

- When the task requires describing an existing image, answering questions about it, or extracting information from it
- When the task requires deterministic manipulation of existing image files, such as downscaling, trimming, format conversion, or compression
- When the task requires traditional computer vision operations, such as filtering, edge detection, or object recognition
- When choosing between deterministic processing and AI generation or editing for an existing image

## Image Processing Best Practices

- Decide by the deliverable: when the deliverable is an image a person will look at, prefer AI image generation or editing; when the deliverable is data extracted from an image, or the same pixels re-encoded, use code
- For image understanding tasks like description or Q&A, use the `read` tool to leverage native multimodal capabilities instead of writing code
- For generative image modifications that require creativity, such as semantic editing, style transfer, or upscaling/restoration/enhancement, use AI image generation and editing tools; MUST read the `imagegen` skill for route selection and prompt structure
- For basic image manipulation tasks like downscaling, cropping, format conversion, and compression, use Python with PIL/Pillow
- For traditional computer vision operations like filtering, edge detection, and object recognition, use OpenCV
- Reserve OpenCV for deterministic pixel-level or geometric pipelines whose result is data or a re-encoded file; for recognizing, classifying, or describing what an image contains, the `read` tool is more accurate and cheaper than hand-written detection code
- DO NOT use deterministic processing where new visual content must be created; deterministic processing only rearranges or re-encodes pixels that already exist

## Route Boundaries

- When a resize or crop would change the aspect ratio, default to preserving all content unless the user explicitly accepts edge loss; follow the `imagegen` skill for that case
- DO NOT use PIL/Pillow, canvas, SVG, HTML, or scripted compositing to add or lay out text on a visual; text-bearing images are generated with their text already in place, as required by the `imagegen` skill
- DO NOT use OpenCV or other deterministic upscaling for resolution, clarity, or restoration requests; those are generative tasks owned by the `imagegen` skill
- DO NOT draw annotations, labels, arrows, callouts, dimension marks, or highlight boxes onto an image with PIL/Pillow, OpenCV, matplotlib, canvas, or SVG when the annotated image is itself the deliverable; annotate through AI image editing as required by the `imagegen` skill. Use code only when the user needs the annotation coordinates as data, or requires reproducible machine-generated overlays such as evaluation or dataset artifacts
- For architectural drawings, floor plans, interior layouts, product design views, engineering sketches, and similar design visuals, use AI image generation; DO NOT assemble them with plotting or vector-drawing code. Route to a deterministic workflow only when the user requires exact scale, verified measurements, or editable CAD/layout source files
- When the deliverable is a new visual, a chart, or a structured diagram rather than a transformation of an existing image, follow the routing rules in the `imagegen` skill instead of this one

## Delivering Results

- Write transformed output to a new file path; MUST NOT overwrite a user-provided original unless the user asked for in-place replacement
- When a transformation can silently damage the result, such as unintended aspect ratio, rotation, color-space, or transparency loss, confirm the output once with the `read` tool; a single pass/fail check is sufficient, do not open an extended inspection loop
- Deliver the resulting image files, and keep the accompanying script only when the user needs to rerun or adjust the transformation
