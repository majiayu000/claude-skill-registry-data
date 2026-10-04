---
name: agency-ai-engine
description: Orchestrate LLM-powered content generation including post creation, caption writing, hashtag suggestions, content repurposing, image prompts, and performance insights. Use when working with AI content logic, OpenAI/Claude integration, or prompt templates.
---

# Social Media Agency AI Engine

## Architecture

The AI engine sits behind an abstraction layer so LLM providers can be swapped.

```
ContentService → AIEngine → LLMProvider (OpenAI | Claude)
                          → ImageService → DALL-E 3
```

## LLM Provider Abstraction

```python
# src/agency/services/ai_engine.py
from abc import ABC, abstractmethod
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic
from agency.config import get_settings

class LLMProvider(ABC):
    @abstractmethod
    async def chat(self, messages: list[dict], temperature: float = 0.7) -> str: ...

class OpenAIProvider(LLMProvider):
    def __init__(self):
        settings = get_settings()
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = "gpt-4o"

    async def chat(self, messages: list[dict], temperature: float = 0.7) -> str:
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=1024,
        )
        return response.choices[0].message.content

class ClaudeProvider(LLMProvider):
    def __init__(self):
        settings = get_settings()
        self.client = AsyncAnthropic(api_key=settings.anthropic_api_key)
        self.model = "claude-sonnet-4-20250514"

    async def chat(self, messages: list[dict], temperature: float = 0.7) -> str:
        system = next((m["content"] for m in messages if m["role"] == "system"), "")
        user_msgs = [m for m in messages if m["role"] != "system"]
        response = await self.client.messages.create(
            model=self.model,
            system=system,
            messages=user_msgs,
            temperature=temperature,
            max_tokens=1024,
        )
        return response.content[0].text

class AIEngine:
    def __init__(self):
        self.primary = OpenAIProvider()
        self.fallback = ClaudeProvider()

    async def chat(self, messages: list[dict], temperature: float = 0.7) -> str:
        try:
            return await self.primary.chat(messages, temperature)
        except Exception:
            return await self.fallback.chat(messages, temperature)
```

## Prompt Templates

### Post Generation

```python
POST_GENERATION_PROMPT = """You are a social media content specialist creating a post for {platform}.

## Client Context
- Brand: {brand_name}
- Industry: {industry}
- Brand Voice: {brand_voice}
- Target Audience: {target_audience}

## Request
- Topic: {topic}
- Tone: {tone}
- Content Type: {content_type}
- Max Length: {max_length} characters

## Platform Guidelines
{platform_guidelines}

## Rules
1. Match the brand voice and tone exactly.
2. Include a clear call-to-action when appropriate.
3. Optimize for the specific platform's algorithm and audience behavior.
4. Keep within character limits for the platform.
5. Use line breaks strategically for readability.
6. Do NOT include hashtags in the body — they will be generated separately.

## Response Format
Return ONLY the post body text. No metadata, no hashtags, no explanations.
"""
```

### Hashtag Generation

```python
HASHTAG_PROMPT = """Generate relevant hashtags for a {platform} post.

## Post Content
{post_body}

## Client Context
- Brand: {brand_name}
- Industry: {industry}

## Rules
1. Mix popular (high-reach) and niche (high-engagement) hashtags.
2. Include 1-2 branded hashtags if the brand has them.
3. Platform-specific count:
   - Instagram: 20-25 hashtags
   - Twitter: 2-4 hashtags
   - LinkedIn: 3-5 hashtags
   - TikTok: 4-6 hashtags
   - Facebook: 1-3 hashtags
4. Return hashtags without the # symbol.

Return a JSON array of strings:
["hashtag1", "hashtag2", ...]

Return ONLY valid JSON.
"""
```

### Content Repurposing

```python
REPURPOSE_PROMPT = """Adapt this social media content from {source_platform} to {target_platform}.

## Original Content ({source_platform})
{original_body}

## Client Context
- Brand: {brand_name}
- Industry: {industry}
- Brand Voice: {brand_voice}

## Platform Differences
- Source ({source_platform}): {source_guidelines}
- Target ({target_platform}): {target_guidelines}

## Rules
1. Preserve the core message and brand voice.
2. Adjust length, tone, and format for the target platform.
3. Adapt any platform-specific formatting (e.g., thread → single post).
4. Optimize for the target platform's algorithm.
5. Do NOT include hashtags — they will be generated separately.

Return ONLY the adapted post body text.
"""
```

### Caption from Image

```python
IMAGE_CAPTION_PROMPT = """Write a social media caption for this image being posted on {platform}.

## Image Description
{image_description}

## Client Context
- Brand: {brand_name}
- Industry: {industry}
- Brand Voice: {brand_voice}

## Rules
1. The caption should complement the image, not just describe it.
2. Include a hook in the first line to stop the scroll.
3. Match the brand's tone of voice.
4. End with a question or CTA to drive engagement.

Return ONLY the caption text.
"""
```

### Performance Insights

```python
INSIGHTS_PROMPT = """Analyze this social media performance data and provide actionable insights.

## Analytics Data
{analytics_json}

## Client Context
- Brand: {brand_name}
- Industry: {industry}
- Active Platforms: {platforms}
- Reporting Period: {period_start} to {period_end}

## Analyze
1. Which content types performed best and why?
2. What are the optimal posting times based on engagement data?
3. Which platform is delivering the best ROI?
4. What trends are emerging in the data?
5. What specific actions should be taken next month?

Return a JSON object:
{{
  "top_performing_content": ["description of top posts..."],
  "optimal_posting_times": {{"platform": "best_times"}},
  "platform_rankings": ["best to worst with reasoning"],
  "trends": ["observed trend 1", "observed trend 2"],
  "recommendations": ["specific action 1", "specific action 2", "specific action 3"],
  "summary": "2-3 sentence executive summary"
}}

Return ONLY valid JSON.
"""
```

### Image Prompt Generation

```python
IMAGE_PROMPT_PROMPT = """Generate a DALL-E image prompt for a social media post.

## Post Context
- Platform: {platform}
- Post Body: {post_body}
- Brand: {brand_name}
- Brand Colors: {brand_colors}
- Visual Style: {visual_style}

## Rules
1. The image should complement the post content.
2. Include specific style directions (photography, illustration, flat design, etc.).
3. Reference brand colors where appropriate.
4. Specify aspect ratio for the platform:
   - Instagram Feed: 1:1 or 4:5
   - Instagram Story: 9:16
   - Facebook: 1.91:1
   - Twitter: 16:9
   - LinkedIn: 1.91:1
   - TikTok: 9:16
5. Avoid text in the image unless specifically requested.

Return ONLY the image generation prompt text.
"""
```

## Image Generation Service

```python
# src/agency/services/image_service.py
from openai import AsyncOpenAI
from agency.config import get_settings

class ImageService:
    def __init__(self):
        settings = get_settings()
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)

    async def generate_image(self, prompt: str, size: str = "1024x1024") -> str:
        response = await self.client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=size,
            quality="standard",
            n=1,
        )
        return response.data[0].url
```

## Platform Guidelines

```python
PLATFORM_GUIDELINES = {
    "instagram": {
        "max_length": 2200,
        "optimal_length": "150-300 characters for feed, shorter for Reels",
        "best_practices": "Visual-first. Use line breaks. CTA in first 125 chars (before 'more'). Emojis welcomed.",
        "aspect_ratios": {"feed": "1:1 or 4:5", "story": "9:16", "reel": "9:16"},
    },
    "facebook": {
        "max_length": 63206,
        "optimal_length": "40-80 characters for highest engagement",
        "best_practices": "Short and punchy. Questions drive comments. Link posts get less reach than native content.",
        "aspect_ratios": {"feed": "1.91:1 or 1:1", "story": "9:16"},
    },
    "twitter": {
        "max_length": 280,
        "optimal_length": "71-100 characters",
        "best_practices": "Concise and witty. Threads for longer content. Media increases engagement 150%.",
        "aspect_ratios": {"feed": "16:9"},
    },
    "linkedin": {
        "max_length": 3000,
        "optimal_length": "150-300 characters, up to 1300 for thought leadership",
        "best_practices": "Professional tone. Personal stories perform well. Use line breaks heavily. Document posts get high reach.",
        "aspect_ratios": {"feed": "1.91:1 or 1:1"},
    },
    "tiktok": {
        "max_length": 2200,
        "optimal_length": "50-150 characters",
        "best_practices": "Casual, authentic tone. Hook in first 3 seconds. Trending sounds and formats. Behind-the-scenes content.",
        "aspect_ratios": {"video": "9:16"},
    },
}
```

## Content Generation Flow

```python
async def generate_full_content(
    engine: AIEngine,
    client_info: dict,
    platform: str,
    topic: str,
    tone: str,
    content_type: str,
) -> dict:
    guidelines = PLATFORM_GUIDELINES.get(platform, {})

    # 1. Generate post body
    body_messages = [
        {"role": "system", "content": POST_GENERATION_PROMPT.format(
            platform=platform,
            brand_name=client_info["brand_name"],
            industry=client_info["industry"],
            brand_voice=client_info.get("brand_voice", "professional"),
            target_audience=client_info.get("target_audience", "general"),
            topic=topic,
            tone=tone,
            content_type=content_type,
            max_length=guidelines.get("optimal_length", "300 characters"),
            platform_guidelines=guidelines.get("best_practices", ""),
        )},
        {"role": "user", "content": f"Create a {content_type} about: {topic}"},
    ]
    body = await engine.chat(body_messages, temperature=0.8)

    # 2. Generate hashtags
    hashtag_messages = [
        {"role": "system", "content": HASHTAG_PROMPT.format(
            platform=platform,
            post_body=body,
            brand_name=client_info["brand_name"],
            industry=client_info["industry"],
        )},
        {"role": "user", "content": "Generate hashtags for this post."},
    ]
    hashtags_raw = await engine.chat(hashtag_messages, temperature=0.5)

    import json
    try:
        hashtags = json.loads(hashtags_raw)
    except json.JSONDecodeError:
        hashtags = []

    return {
        "body": body,
        "hashtags": hashtags,
        "platform": platform,
        "ai_generated": True,
    }
```

## Token Usage Tracking

```python
class TokenTracker:
    def __init__(self):
        self.total_input_tokens = 0
        self.total_output_tokens = 0

    def record(self, input_tokens: int, output_tokens: int):
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens

    @property
    def estimated_cost_usd(self) -> float:
        return (self.total_input_tokens * 2.5 + self.total_output_tokens * 10) / 1_000_000
```

## Key Rules

1. **Always use the AIEngine abstraction** — never call OpenAI/Claude directly in routers
2. **System prompts are templates** — fill with client-specific context at runtime
3. **Generate body and hashtags separately** — different temperature settings
4. **All LLM JSON responses must be validated** — parse with try/except, retry on failure
5. **Temperature 0.8 for creative content** (posts, captions), **0.3-0.5 for structured output** (hashtags, insights)
6. **Track token usage** per organization for cost analytics
7. **Platform-specific guidelines** — always include in the prompt context
8. **Fallback gracefully** — if primary LLM fails, use fallback provider
9. **Never generate content without client context** — brand voice consistency is critical
10. **Image generation is optional** — only when explicitly requested, uses DALL-E 3
