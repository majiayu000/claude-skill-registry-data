---
name: vision-guidance
description: >
  Image understanding guidance for agents with vision enabled.
  Instructs agents to use read_file for viewing images directly
  instead of writing OpenCV/PIL code to parse them programmatically.
---

# Vision Guidance

You have **native image understanding** — you can see and interpret images
directly when they are loaded via `read_file`.

## Image Files

For image files (.png, .jpg, .jpeg, .gif, .webp):

1. **ALWAYS use `read_file`** to view the image first. You will see the
   actual image and can describe its contents (charts, diagrams, chess
   boards, music notation, photos, maps, tables, etc.).
2. **Do NOT default to writing OpenCV/PIL/cv2 code** to parse images
   programmatically. You can understand images natively — code-based
   image processing is only needed for precise pixel-level operations
   (e.g., exact color values, coordinate measurements).
3. After viewing the image with `read_file`, describe what you see and
   extract the relevant information. Only write image processing code
   if the visual inspection is insufficient for the task.

## When to Use Code Instead

Use `python_execute` with image libraries only when you need:
- Exact pixel coordinates or color values
- Image transformations (crop, resize, rotate)
- Template matching or automated detection at scale
- OCR on text within images (though try reading first)

For everything else — interpreting charts, reading diagrams, identifying
objects, understanding layouts — just look at the image with `read_file`.
