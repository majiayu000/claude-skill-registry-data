---
allowed-tools: Read, Write, Edit, Bash, WebFetch
description: 'Generate high-quality images using Google''s Gemini image generation
  models.

  Use when creating AI-generated images, editing existing images, or building

  image generation features. Helps choose the right model (Gemini 3 Pro Image

  for quality, Gemini 2.5 Flash Image for speed) and provides implementation

  patterns for Python, TypeScript, and REST APIs.'
name: nano-banana-pro
---

# Nano Banana Pro Image Generation

Generate high-quality images using Google's Gemini image generation models with Python, TypeScript, or REST APIs.

## Choosing the Right Model

| Model | Model ID | Best For | Speed | Quality |
|-------|----------|----------|-------|---------|
| **Gemini 3 Pro Image** | `gemini-3-pro-image-preview` | Production visuals, professional content, complex scenes | Slower | Highest |
| **Gemini 2.5 Flash Image** | `gemini-2.5-flash-image` | Prototyping, high-volume, interactive apps | Fast | Good |

**Decision Guide:**
- Need highest quality or complex text rendering? → **Gemini 3 Pro Image**
- Need speed, lower cost, or high volume? → **Gemini 2.5 Flash Image**
- Need real-time search grounding? → **Gemini 3 Pro Image** (supports Google Search)

## Setup

### 1. Get API Key

1. Go to [Google AI Studio](https://aistudio.google.com)
2. Click "Get API Key"
3. Store as environment variable: `GEMINI_API_KEY`

### 2. Install SDK

**Python:**
```bash
pip install google-genai pillow
```

**TypeScript/JavaScript:**
```bash
npm install @google/genai
```

## Basic Image Generation

### Python

```python
from google import genai
from google.genai import types
import os

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

response = client.models.generate_content(
    model="gemini-2.5-flash-image",  # or "gemini-3-pro-image-preview"
    contents="A serene Japanese garden with cherry blossoms and a koi pond",
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"]
    )
)

# Save generated image
for part in response.parts:
    if part.inline_data:
        image = part.as_image()
        image.save("output.png")
```

### TypeScript

```typescript
import { GoogleGenAI } from "@google/genai";
import * as fs from "fs";

const client = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });

async function generateImage(prompt: string) {
  const response = await client.models.generateContent({
    model: "gemini-2.5-flash-image",
    contents: prompt,
    config: {
      responseModalities: ["IMAGE"],
    },
  });

  // Extract and save image
  for (const part of response.candidates[0].content.parts) {
    if (part.inlineData) {
      const buffer = Buffer.from(part.inlineData.data, "base64");
      fs.writeFileSync("output.png", buffer);
    }
  }
}
```

### REST API (cURL)

```bash
curl -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{
      "role": "user",
      "parts": [{"text": "A futuristic cityscape at sunset"}]
    }],
    "generationConfig": {
      "responseModalities": ["IMAGE"]
    }
  }'
```

## Configuration Options

### Aspect Ratios and Resolution

```python
response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents="Professional product photo of a coffee mug",
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"],
        image_config=types.ImageConfig(
            aspect_ratio="16:9",  # 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9
            image_size="2K"       # 1K, 2K, 4K
        )
    )
)
```

### With Google Search Grounding (Gemini 3 Pro Image only)

```python
response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents="Create an infographic showing today's weather in San Francisco",
    config=types.GenerateContentConfig(
        response_modalities=["TEXT", "IMAGE"],
        tools=[{"google_search": {}}]
    )
)
```

## Image Editing

### Edit Existing Images

```python
from PIL import Image

# Load existing image
source_image = Image.open("photo.png")

response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=[
        "Change the background to a tropical beach sunset",
        source_image
    ],
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"]
    )
)

for part in response.parts:
    if part.inline_data:
        part.as_image().save("edited.png")
```

### Multi-Turn Editing with Chat

```python
# Create chat for iterative edits
chat = client.chats.create(
    model="gemini-2.5-flash-image",
    config=types.GenerateContentConfig(
        response_modalities=["TEXT", "IMAGE"]
    )
)

# Initial generation
response1 = chat.send_message(
    "Create a vibrant infographic explaining photosynthesis"
)

# Iterate on the result
response2 = chat.send_message(
    "Update this infographic to use a blue color scheme"
)

# Continue refining
response3 = chat.send_message(
    "Add a title: 'How Plants Make Food'"
)
```

## Common Use Cases

### 1. Product Photography

```python
response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents="""
    Professional product photo:
    - White ceramic coffee mug
    - Minimalist style on marble surface
    - Soft natural lighting from left
    - Shallow depth of field
    """,
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"],
        image_config=types.ImageConfig(
            aspect_ratio="1:1",
            image_size="2K"
        )
    )
)
```

### 2. Marketing Visuals with Text

```python
response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents="""
    Create a professional event poster:
    - Title: "Annual Tech Summit 2025"
    - Date: "March 15-17, 2025"
    - Location: "San Francisco Convention Center"
    - Modern, tech-forward design
    - Use blue and purple gradient
    """,
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"],
        image_config=types.ImageConfig(aspect_ratio="9:16")
    )
)
```

### 3. Character Consistency (with Reference Image)

```python
import base64

def load_image_bytes(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()

character_bytes = load_image_bytes("character.png")

response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=[
        types.Part.from_bytes(data=character_bytes, mime_type="image/png"),
        "Generate an image of this person at a tech conference giving a presentation"
    ],
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"]
    )
)
```

## Error Handling

```python
from google.genai import errors

try:
    response = client.models.generate_content(
        model="gemini-2.5-flash-image",
        contents="Generate an image...",
        config=types.GenerateContentConfig(response_modalities=["IMAGE"])
    )

    if not response.candidates:
        print("No image generated - possibly filtered by safety settings")
    else:
        for part in response.parts:
            if part.inline_data:
                part.as_image().save("output.png")
                print("Image saved successfully")

except errors.APIError as e:
    if e.status_code == 429:
        print("Rate limited - implement exponential backoff")
    elif e.status_code == 400:
        print(f"Bad request: {e.message}")
    else:
        raise
```

## API Integrations

### Next.js API Route

```typescript
// app/api/generate-image/route.ts
import { NextRequest, NextResponse } from "next/server";
import { GoogleGenAI } from "@google/genai";

const client = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });

export async function POST(request: NextRequest) {
  const { prompt, aspectRatio = "1:1" } = await request.json();

  try {
    const response = await client.models.generateContent({
      model: "gemini-2.5-flash-image",
      contents: prompt,
      config: {
        responseModalities: ["IMAGE"],
        imageConfig: { aspectRatio },
      },
    });

    const imagePart = response.candidates?.[0]?.content?.parts?.find(
      (p) => p.inlineData
    );

    if (!imagePart?.inlineData) {
      return NextResponse.json({ error: "No image generated" }, { status: 500 });
    }

    return NextResponse.json({
      image: {
        data: imagePart.inlineData.data,
        mimeType: imagePart.inlineData.mimeType,
      },
    });
  } catch (error) {
    console.error("Image generation failed:", error);
    return NextResponse.json({ error: "Generation failed" }, { status: 500 });
  }
}
```

### FastAPI Endpoint

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai
from google.genai import types
import base64
import os

app = FastAPI()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

class ImageRequest(BaseModel):
    prompt: str
    aspect_ratio: str = "1:1"
    model: str = "gemini-2.5-flash-image"

class ImageResponse(BaseModel):
    image_base64: str
    mime_type: str

@app.post("/generate", response_model=ImageResponse)
async def generate_image(request: ImageRequest):
    try:
        response = client.models.generate_content(
            model=request.model,
            contents=request.prompt,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
                image_config=types.ImageConfig(
                    aspect_ratio=request.aspect_ratio
                )
            )
        )

        for part in response.parts:
            if part.inline_data:
                return ImageResponse(
                    image_base64=base64.b64encode(
                        part.inline_data.data
                    ).decode(),
                    mime_type=part.inline_data.mime_type
                )

        raise HTTPException(status_code=500, detail="No image generated")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

## Best Practices

### Prompt Engineering

| Do | Don't |
|----|-------|
| Be specific about style, lighting, composition | Use vague terms like "nice" or "good" |
| Include technical details (lens, lighting direction) | Assume the model knows your intent |
| Use reference to art styles or photographers | Request copyrighted characters by name |
| Describe the scene in logical order | Contradict yourself in the prompt |

### Performance Optimization

- Use `gemini-2.5-flash-image` for previews, `gemini-3-pro-image-preview` for final renders
- Request only needed modalities (`["IMAGE"]` not `["TEXT", "IMAGE"]` if text not needed)
- Implement caching for repeated similar prompts
- Use batch processing for multiple generations

### Cost Management

- Gemini 3 Pro Image costs more but produces higher quality
- Use Flash for iteration, Pro for final output
- Monitor usage through Google AI Studio dashboard

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| No image returned | Safety filter triggered | Review prompt for policy violations |
| Low quality output | Using Flash for complex scene | Switch to Gemini 3 Pro Image |
| Text rendering issues | Complex typography | Use Gemini 3 Pro Image, simplify text |
| Rate limiting (429) | Too many requests | Implement exponential backoff |
| Aspect ratio ignored | Invalid ratio string | Use exact format: "16:9" not "16x9" |

## Resources

- [Google AI Studio](https://aistudio.google.com) - Interactive testing
- [Gemini API Documentation](https://ai.google.dev/gemini-api/docs/image-generation)
- [Python SDK Reference](https://googleapis.github.io/python-genai/)
