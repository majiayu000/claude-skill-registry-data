---
name: asset-edit
description: Edit or refine an existing image using Nano Banana 2's conversational editing. Use when an asset needs color correction, element changes, style adjustments, or iterative refinement.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

Edit an image asset using Nano Banana 2: $ARGUMENTS

$ARGUMENTS should include:
- Path to the source image (in `public/images/` or elsewhere)
- Description of desired edits (natural language)
- Optionally: multiple edit steps to apply in sequence
- Empty — ask the user for the image path and desired edits

## Before Starting

1. Confirm `GOOGLE_GENERATIVE_AI_API_KEY` is set in `.env.local`
2. Verify the source image exists and read it
3. Read `src/lib/config/tenant.config.ts` for brand context

## Supported Edit Operations

### Color & Tone
- "Make the lighting warmer/cooler"
- "Increase contrast, deepen the shadows"
- "Shift the palette toward earth tones — terracotta, sage, amber"
- "Desaturate to a muted, scholarly feel"
- "Apply a warm golden-hour color grade"

### Composition & Framing
- "Crop tighter on the subject's face"
- "Add more negative space on the right for text placement"
- "Extend the background to fill 16:9 aspect ratio" (outpainting)
- "Zoom out to show more of the environment"

### Elements & Subjects
- "Remove the background clutter behind the speaker"
- "Add a stack of books on the table"
- "Replace the plain wall with a bookshelf"
- "Change the subject's shirt color to a warm terracotta"

### Style Transfer
- "Make this look like a watercolor illustration"
- "Convert to a minimalist line drawing"
- "Apply a vintage film photography look — grain, warm tones, slight vignette"
- "Make this feel like an editorial magazine photo"

### Cleanup & Polish
- "Remove the watermark in the bottom right"
- "Fix the distorted hand"
- "Sharpen the subject's face"
- "Smooth the background gradient"

## Prompting Best Practices for Edits

1. **Be specific about what to change AND what to keep**: "Change the background from grey to warm amber, but keep the subject and their clothing exactly the same"
2. **Reference spatial locations**: "In the upper-left corner", "along the bottom edge", "behind the main subject"
3. **Describe the desired result, not the process**: "The lighting should feel like late afternoon golden hour" not "add a warm filter"
4. **Use comparative language**: "warmer than the current version", "more saturated", "softer shadows"
5. **One major edit per turn** for best results — chain multiple small edits rather than one massive change

## Execution

### Step 1 — Load the Source Image
```typescript
import { GoogleGenAI } from "@google/genai";
import * as fs from "fs";
import * as path from "path";

const ai = new GoogleGenAI({ apiKey: process.env.GOOGLE_GENERATIVE_AI_API_KEY });

const sourceImagePath = "<SOURCE_IMAGE_PATH>";
const imageBytes = fs.readFileSync(sourceImagePath);
const base64Image = imageBytes.toString("base64");
const mimeType = sourceImagePath.endsWith(".png") ? "image/png" : "image/jpeg";
```

### Step 2 — Send Edit Request
```typescript
const response = await ai.models.generateContent({
  model: "gemini-2.0-flash-exp",
  contents: [
    {
      role: "user",
      parts: [
        { inlineData: { data: base64Image, mimeType } },
        { text: "<EDIT_INSTRUCTION>" },
      ],
    },
  ],
  config: {
    responseModalities: ["image", "text"],
  },
});

// Extract and save edited image
for (const part of response.candidates[0].content.parts) {
  if (part.inlineData) {
    const buffer = Buffer.from(part.inlineData.data, "base64");
    const outPath = sourceImagePath.replace(/(\.\w+)$/, "-edited$1");
    fs.writeFileSync(outPath, buffer);
  }
}
```

### Step 3 — Iterative Refinement
If the edit is close but not perfect, continue the conversation:
- Use the edited output as the new input
- Apply follow-up refinements
- Chain up to 3-4 edits per session for best coherence

### Step 4 — Save & Report
- Save edited image alongside the original with `-edited` or `-v2`, `-v3` suffix
- Never overwrite the original unless explicitly asked
- Report both paths for comparison

## Output Format

```
## Asset Edit Report

### Source
- File: public/images/generated/hero/forgotten-ways-1.png

### Edit Applied
> "Make the lighting warmer with golden-hour tones, add subtle bokeh to the background"

### Result
- File: public/images/generated/hero/forgotten-ways-1-edited.png

### Refinement History
1. Original → warmer lighting + bokeh (current)

### Next Steps
- Review the edit — reply with further refinements or approve
- Use `/asset-text-overlay` to add text to the final version
```

## Multi-Step Edit Chains

For complex transformations, break into steps and execute sequentially:

```
Step 1: "Remove the busy background, replace with a soft warm gradient"
Step 2: "Add subtle paper texture overlay to the gradient"
Step 3: "Adjust the subject's color to match the new warmer palette"
```

Show the user the result after each step. If they approve, continue to the next.

## Error Handling

- Source image not found → ask for correct path
- Image too large (>20MB) → resize before sending to API
- Edit produces unexpected results → show result, suggest alternative phrasing
- API content policy → adjust edit description, avoid specific person modifications
