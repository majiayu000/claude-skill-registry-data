---
name: google-genai-imagen-integrator
description: Integrate Google Gemini for text-to-image generation and image editing. Use this skill when the application needs AI image generation from text prompts, image editing with instructions, or automated visual content creation. Triggers on requests for image generation, AI artwork, product images, or image modification.
_meta_type: sdk
---

# Google GenAI Imagen SDK Integration

## Scenarios

- **Text-to-Image Generation**: Create high-quality images from text prompts using Gemini's image generation capabilities
- **Image Editing**: Modify existing images with natural language instructions
- **Product Photography**: Generate professional product images for e-commerce
- **Content Creation**: Automated visual content generation for marketing and social media
- **AI-Powered Design**: Build design tools with intelligent image generation

**Not recommended for:**
- Direct frontend browser use (use backend proxy instead for credential security)
- Real-time video generation
- Image generation without internet connectivity
- Scenarios requiring extremely low latency

## Setup

### 1. Install Dependencies

```bash
npm install @google/genai
```

### 2. Copy SDK Wrapper

Read `lib/google-genai-imagen.ts` from this skill and copy it to the project, then use it directly.

## Configuration

### Zero Configuration (Default)

Genie provides default zero-configuration support using `google.openai.auth-proxy.local` as the endpoint. **No environment variables are required** - Genie has integrated authentication in the proxy gateway by default.

Simply use:

```typescript
import { createClient } from './lib/google-genai-imagen';
const client = createClient();
```

### Custom Configuration (Optional)

Users can optionally configure environment variables. When configured, Genie will use user-provided credentials instead of the default proxy:

```env
# Optional - Only configure if you want to use your own credentials
GOOGLE_GENAI_API_KEY=your-api-key-here

# Optional: Custom API endpoint
GOOGLE_GENAI_BASE_URL=https://custom-api.example.com

# Optional: Custom model name (defaults to 'gemini-2.5-flash-image')
GOOGLE_GENAI_MODEL=gemini-2.5-flash-image
```

**Obtaining Credentials** (if needed):
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Get API key"
3. Create a new API key or use existing one
4. Copy the key and save it securely

### Custom Endpoint and Model

Users can customize endpoint and model:

```typescript
import { GenAIImageClient, createClient } from './lib/google-genai-imagen';

// Custom model only (via environment variable)
const client = createClient();
// Set GOOGLE_GENAI_MODEL=gemini-2.5-flash-image in .env

// Custom endpoint (explicit configuration)
const client = new GenAIImageClient({
  apiKey: process.env.GOOGLE_GENAI_API_KEY!,
  baseURL: 'https://custom-api.example.com',
  defaultModel: 'gemini-2.5-flash-image'
});

// Override with createClient
const client = createClient({
  baseURL: 'https://custom-endpoint.example.com',
  defaultModel: 'gemini-2.5-flash-image'
});
```

## Quick Start

### Basic Usage

```typescript
import { createClient } from './lib/google-genai-imagen';

const client = createClient();

// Generate image from text prompt
const result = await client.generateImage(
  'A cute red panda eating bamboo in a Japanese garden',
  { aspectRatio: '16:9' }
);

// Save the generated image
import * as fs from 'fs';
fs.writeFileSync('output.png', result.imageData);
console.log('Description:', result.text);
```

### Image Generation with Options

```typescript
// Generate with specific aspect ratio
const result = await client.generateImage(
  'A photorealistic portrait of a ceramicist',
  { aspectRatio: '1:1' }
);

// Generate with custom model
const result = await client.generateImage(
  'Professional product photo of a smartphone',
  { 
    aspectRatio: '4:3',
    model: 'gemini-2.5-flash-image'
  }
);

// Generate with text description included
const result = await client.generateImage(
  'A fantasy landscape with floating islands',
  { 
    aspectRatio: '16:9',
    includeText: true
  }
);
```

### Image Editing

```typescript
import * as fs from 'fs';

// Load existing image
const originalImage = fs.readFileSync('cat.jpg');

// Edit image with natural language instruction
const result = await client.editImage(
  'Add a wizard hat to this cat',
  originalImage,
  { aspectRatio: '1:1' }
);

fs.writeFileSync('cat_with_hat.png', result.imageData);
```

## Response Structure

```typescript
{
  imageData: Buffer;       // Generated image data as Buffer
  text?: string;           // Optional text description
  mimeType: string;        // MIME type of the image (e.g., 'image/png')
  groundingMetadata?: any; // Grounding metadata if Google Search was used
}
```

## Supported Options

### Aspect Ratios
`'1:1'` | `'2:3'` | `'3:2'` | `'3:4'` | `'4:3'` | `'4:5'` | `'5:4'` | `'9:16'` | `'16:9'` | `'21:9'`

### Image Sizes (gemini-3-pro-image-preview only)
`'1K'` | `'2K'` | `'4K'` (must be uppercase)

## Architecture Integration

### Service Layer Pattern (Recommended)

```typescript
// src/services/image-generation.service.ts
import { createClient } from '../lib/google-genai-imagen';

export class ImageGenerationService {
  private imageClient = createClient();
  
  async generateProductImage(description: string, userId: string): Promise<string> {
    const prompt = `Professional product photo: ${description}`;
    const result = await this.imageClient.generateImage(prompt, {
      aspectRatio: '1:1',
      model: 'gemini-2.5-flash-image'
    });
    
    // Save to storage and return URL
    return this.saveAndGetUrl(result.imageData, userId);
  }
  
  async editUserAvatar(editInstruction: string, currentAvatar: Buffer): Promise<Buffer> {
    const result = await this.imageClient.editImage(
      editInstruction,
      currentAvatar,
      { aspectRatio: '1:1' }
    );
    
    return result.imageData;
  }
  
  private async saveAndGetUrl(imageData: Buffer, userId: string): Promise<string> {
    // Implement your storage logic here
    return `https://storage.example.com/images/${userId}/${Date.now()}.png`;
  }
}
```

## Security Best Practices

1. **Never commit credentials**: Add `.env` to `.gitignore`
2. **Use environment variables**: Store all sensitive config in `.env`
3. **Rotate API keys regularly**: Generate new keys periodically
4. **Implement rate limiting**: Prevent API abuse in production
5. **Validate user input**: Sanitize prompts before sending to API
6. **Monitor usage**: Track API calls to detect anomalies

## Troubleshooting

**Authentication Errors**
- Verify API key is correctly set in `.env` file if using custom configuration
- Check API key is active in Google AI Studio
- Ensure no extra spaces or quotes in the key

**Image Generation Fails**
- Check your prompt follows content policies
- Verify aspect ratio is supported (1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9)
- For 4K resolution, use `gemini-3-pro-image-preview` model
- Ensure imageSize is uppercase ('1K', '2K', '4K')

**Network Errors**
- Check internet connectivity
- Verify firewall allows connections to googleapis.com
- Check if using corporate proxy that blocks API access
- Confirm access to proxy endpoint if using zero-configuration

**Base64 Decoding Errors**
- Ensure you're correctly parsing the response
- Check that image data is extracted from the right response field

## Resources

- **SDK Wrapper Source**: `lib/google-genai-imagen.ts`
- **Official Documentation**: [Gemini API Image Generation](https://ai.google.dev/gemini-api/docs/image-generation)
- **Google AI Studio**: [https://aistudio.google.com](https://aistudio.google.com)
- **API Reference**: [Gemini API Docs](https://ai.google.dev/gemini-api/docs)
