---
name: paste-image
description: >
  Handle pasted screenshots and images. The user uses a local script
  (sspaste on their Mac) to ship a clipboard image from their Mac to
  the remote server. When the user mentions pasting an image, a
  screenshot, or gives you a path like ~/pi-paste-*.png, use the read
  tool to load it. Triggered by phrases like "paste image", "I sent a
  screenshot", "here's a screenshot", "take a look at this image",
  or providing a ~/pi-paste-* path.
---

The user's Mac workflow is:

1. Take a screenshot (Cmd+Shift+4) — image goes to Mac clipboard
2. Run `sspaste user@server` on the Mac — this scp's the image to `~/pi-paste-<timestamp>.png`
3. The user then tells pi about the image

## Your job

When the user says they pasted an image, sent a screenshot, or provides a `~/pi-paste-*.png` path:

1. **Read the image** with the `read` tool to see what's in it.
2. Discuss the image contents with the user.

## What the read tool supports

- PNG, JPEG, WebP, GIF
- Local file paths like `~/pi-paste-1747000000.png`
- Pi will display the image inline in the chat

## Example flow

```
User: I pasted a screenshot of the bug
You:  read ~/pi-paste-1747000000.png
      → (sees the error in the image)
      "I can see the error. It looks like..."
```

```
User: here's the design mockup ~/pi-paste-1747123456.png
You:  read ~/pi-paste-1747123456.png
      → (analyzes the mockup)
```
