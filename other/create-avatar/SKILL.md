---
name: create-avatar
description: Create an animated avatar character from a photo using the photo-to-avatar pipeline with IndexedDB and cloud storage.
argument-hint: <photo-path-or-description>
---

# Create Avatar Character

Generate an animated avatar character from a photo or text description using the photo-to-avatar pipeline. Avatars are bust-shot character images that can be animated via image-to-video for lip sync and movement.

## Purpose

Create a personalized avatar character from a user's photo or a text description. The pipeline analyzes the photo using Gemini Vision to extract facial features and clothing details, then generates an avatar image in a chosen art style. Avatars can be animated using the image-to-video pipeline for talking head videos.

## Pipeline

### From Photo

1. **Photo analysis** (`analyzePhotoForAvatar`) -- Gemini Vision analyzes the photo and extracts:
   - Hair color, hair style, skin tone, eye color
   - Clothing, accessories, age, gender, expression, body type
   - A `generationPrompt` suitable for AI image generation

2. **Image generation** (`generateAvatar`) -- Calls the NB2 endpoint (`/api/nb2/generate`) with `partType: 'concept'` and a custom prompt that includes the art style modifier

3. **Storage** -- Avatar image blob saved to IndexedDB via `avatarDB.ts`, thumbnail generated for store

### From Text

1. User provides a text description directly
2. Same generation and storage steps as photo-based flow

## Art Styles

| Style | Description |
|-------|-------------|
| `realistic` | Photorealistic, studio photography, DSLR quality, natural skin texture |
| `semi-realistic` | Semi-realistic digital art, detailed shading, painterly style |
| `illustrated` | Illustrated character portrait, clean lines, stylized digital art |
| `anime` | Anime style, large expressive eyes, Japanese animation aesthetic |

The `cartoon`, `chibi`, and `pixel-art` styles are available in the photo-to-avatar service for photo analysis but the avatar generator primarily uses the four styles above.

## Avatar Video Generation

Avatars can be animated for talking head videos:

```ts
interface AvatarVideoOptions {
  imageBase64: string       // Base avatar image
  prompt?: string           // Desired movement/speech description
  durationSeconds?: number  // Video length
  modelId?: string          // AI model provider
  resolution?: string
  fps?: number
  aspectRatio?: string
  generateAudio?: boolean   // Generate audio from prompt
}
```

Uses the multi-provider image-to-video pipeline (`aiProviderClient.ts`) to convert the static avatar into an animated video.

## Generation Options

```ts
interface AvatarGenerationOptions {
  prompt: string                    // Character description
  name?: string                     // Display name
  style: AvatarStyle                // Art style
  source: 'text' | 'photo'         // Generation source
  sourcePhotoDataUrl?: string       // Photo to analyze (if source='photo')
  resolution?: '512' | '1024' | '2048'
  aspectRatio?: '1:1' | '3:4' | '4:3' | '9:16' | '16:9'
  onProgress?: (step: string, progress: number) => void
}
```

## Storage Architecture

- **IndexedDB** (`avatarDB.ts`): Full-resolution avatar image blobs (too large for localStorage)
- **Cloud** (`avatarCloud.ts`): Cloud-synced avatar data via Supabase
- **Store**: `useAvatarCharacterStore.ts` holds avatar metadata and canvas placement
- **Saved library**: `useSavedAvatarCharactersStore.ts` manages the user's avatar collection
- **Thumbnails**: Downscaled to 128px for store persistence (avoids localStorage quota)

## Key Files

| Purpose | Path |
|---------|------|
| Photo analysis (Gemini Vision) | `src/services/photoToAvatar.ts` |
| Avatar generation pipeline | `src/services/avatarGenerator.ts` |
| Avatar IndexedDB storage | `src/services/avatarDB.ts` |
| Avatar cloud storage | `src/services/avatarCloud.ts` |
| Avatar types | `src/types/avatar.ts` |
| Avatar character store | `src/stores/useAvatarCharacterStore.ts` |
| Saved avatars store | `src/stores/useSavedAvatarCharactersStore.ts` |
| Avatar panel | `src/components/panels/AvatarPanel.tsx` |
| Photo-to-avatar panel | `src/components/panels/PhotoToAvatarPanel.tsx` |
| Canvas layer | `src/components/canvas/AvatarCharacterLayer.tsx` |
| Remotion export layer | `src/remotion/RemotionAvatarCharacter.tsx` |
| Server route | `server/routes/avatarCharacters.ts` |

## Common Issues

- **Gemini Vision API error**: Requires `VITE_GEMINI_API_KEY`. The photo analysis uses Gemini's vision capabilities to extract structured JSON.
- **Image too large for localStorage**: Avatar blobs are stored in IndexedDB, only thumbnails go to the store. The `createThumbnail` helper downscales to 128px max.
- **Photo not recognized**: Gemini may fail to extract features from heavily filtered or low-quality photos. The prompt instructs it to return structured JSON with all required fields.
- **Art style mismatch**: Each style has specific prompt modifiers. The `STYLE_PROMPTS` mapping in `avatarGenerator.ts` defines the exact modifiers for each style.
- **Credit gating**: Photo analysis uses `photo-to-avatar` credit type, generation uses `nb2-generate`.

## Example

### From Photo
1. User uploads a selfie
2. Gemini Vision extracts: "young woman with curly brown hair, olive skin, wearing a red sweater, friendly smile"
3. Pipeline generates an avatar in the chosen style (e.g., `illustrated`)
4. Avatar saved to IndexedDB and appears in the avatar library
5. User can place avatar on canvas and animate it with dialogue

### From Text
1. User types: "A professional woman in a navy business suit with short black hair and glasses"
2. Pipeline generates the avatar directly from the description
3. Same storage and usage flow as photo-based
