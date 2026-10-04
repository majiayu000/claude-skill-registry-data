---
name: creatomate
description: |
  Creatomate video/image generation API. Use when: (1) Creating videos or images programmatically with the Creatomate SDK, (2) Building slideshows, concatenating videos, adding text overlays, (3) Adding animated captions or subtitles, (4) Generating social media content (TikTok, Instagram Stories, YouTube Shorts), (5) Using templates with dynamic modifications, (6) Applying effects (blur, filters, masks, transitions), (7) Integrating with ChatGPT for AI-generated content, (8) Working with compositions and animations.
---

# Creatomate API

Cloud API for generating and editing video and images programmatically. Creatomate uses a JSON-based format called RenderScript to define video/image compositions.

## Quick Start

```javascript
const Creatomate = require('creatomate');
const client = new Creatomate.Client('YOUR_API_KEY');

// Render from a template
const renders = await client.render({
  templateId: 'your-template-id',
  modifications: {
    'Title': 'Hello World',
    'Text 1': 'Dynamic content here'
  }
});

// Or build from source
const source = new Creatomate.Source({
  outputFormat: 'mp4',
  width: 1920,
  height: 1080,
  elements: [
    new Creatomate.Video({ source: 'https://...' }),
    new Creatomate.Text({ text: 'Overlay text' })
  ]
});
const renders = await client.render({ source });
```

## Quick Reference

| Task | Read |
|------|------|
| Getting started with the SDK | [sdk-basics.md](references/sdk-basics.md) |
| Building video from elements | [source-elements.md](references/source-elements.md) |
| Text overlays and animations | [text-elements.md](references/text-elements.md) |
| Working with templates | [templates.md](references/templates.md) |
| Transitions and effects | [effects.md](references/effects.md) |
| Creating slideshows | [slideshows.md](references/slideshows.md) |
| Adding captions/subtitles | [captions.md](references/captions.md) |
| Social media formats | [social-media.md](references/social-media.md) |
| Compositions (scenes) | [compositions.md](references/compositions.md) |
| AI integration (ChatGPT) | [ai-integration.md](references/ai-integration.md) |

## Reference Files

### Foundation
- [references/sdk-basics.md](references/sdk-basics.md) - Client setup, API key, rendering basics
- [references/source-elements.md](references/source-elements.md) - Source object, element types, tracks

### Elements
- [references/text-elements.md](references/text-elements.md) - Text styling, fonts, backgrounds, animations
- [references/video-audio.md](references/video-audio.md) - Video/Audio elements, trimming, looping
- [references/images.md](references/images.md) - Image elements, slideshows, Ken Burns effects

### Effects & Animations
- [references/effects.md](references/effects.md) - Filters, blur, masks, color overlays, shadows
- [references/animations.md](references/animations.md) - Keyframes, transitions, enter/exit animations
- [references/captions.md](references/captions.md) - Animated captions, AWS Transcribe integration

### Advanced
- [references/compositions.md](references/compositions.md) - Grouping elements, scenes, nested timelines
- [references/templates.md](references/templates.md) - Using templates with modifications
- [references/social-media.md](references/social-media.md) - TikTok, Instagram, YouTube formats
- [references/ai-integration.md](references/ai-integration.md) - ChatGPT integration, AI-generated content

## Code Examples

For 50+ working code examples, see the official **[Creatomate Node.js Examples](https://github.com/Creatomate/node-examples)** repository.

### Popular Examples

| Example | Description |
|---------|-------------|
| [concatenate](https://github.com/Creatomate/node-examples/tree/main/concatenate) | Combine multiple videos |
| [slideshow](https://github.com/Creatomate/node-examples/tree/main/slideshow) | Image slideshow with transitions |
| [captions](https://github.com/Creatomate/node-examples/tree/main/captions) | Animated captions with AWS Transcribe |
| [chatgpt](https://github.com/Creatomate/node-examples/tree/main/chatgpt) | AI-generated video content |
| [story-video](https://github.com/Creatomate/node-examples/tree/main/story-video) | TikTok/Instagram story format |
| [text-overlay](https://github.com/Creatomate/node-examples/tree/main/text-overlay) | Text on video |
| [picture-in-picture](https://github.com/Creatomate/node-examples/tree/main/picture-in-picture) | PiP layout |
| [aws-polly](https://github.com/Creatomate/node-examples/tree/main/aws-polly) | Text-to-speech videos |
| [blur-background](https://github.com/Creatomate/node-examples/tree/main/blur-background) | Background blur effect |
| [template](https://github.com/Creatomate/node-examples/tree/main/template) | Template rendering |
