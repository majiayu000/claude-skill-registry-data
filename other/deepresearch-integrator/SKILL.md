---
name: deepresearch-integrator
description: Integrate Hunyuan DeepResearch for deep reasoning and search-enhanced conversations. Use this skill when the application needs AI research analysis, real-time information queries, LLM tracking, or search-enhanced chat capabilities. Triggers on requests for AI research, news analysis, market insights, or deep reasoning with web search.
_meta_type: sdk
---

# Tencent Cloud Hunyuan DeepResearch SDK Integration

## Scenarios

- **Deep Reasoning**: Leverage `hunyuan-t1-latest` model for in-depth thinking and analysis of complex problems
- **Search-Enhanced Conversations**: Built-in real-time search capabilities that automatically fetch the latest information
- **AI Industry Tracking**: Monitor latest LLM releases, model comparisons, and AI application trends
- **Research Analysis**: Summarize breakthroughs, compare technologies, and analyze market dynamics
- **Real-Time Information Queries**: Get up-to-date news, events, and data with search enhancement

**Not recommended for:**
- Direct frontend browser use (credential security issues)
- Simple queries that don't require deep reasoning or search
- Scenarios requiring extremely low latency (< 100ms)
- Offline or air-gapped environments (search enhancement requires internet)

## Setup

### 1. Install Dependencies

```bash
npm install tencentcloud-sdk-nodejs-hunyuan
```

### 2. Copy SDK Wrapper

Read `lib/deepresearch.ts` from this skill and copy it to the project, then use it directly.

## Configuration

### Zero Configuration (Default)

Genie provides default zero-configuration support using `hunyuan.tencent_cloud.auth-proxy.local` as the endpoint. **No environment variables are required** - Genie has integrated authentication in the proxy gateway by default.

Simply use:

```typescript
import { createNativeClient } from './lib/deepresearch';
const client = createNativeClient();
```

### Custom Configuration (Optional)

Users can optionally configure environment variables. When configured, Genie will use user-provided credentials instead of the default proxy:

```env
# Optional - Only configure if you want to use your own credentials
TENCENTCLOUD_SECRET_ID=your-secret-id-here
TENCENTCLOUD_SECRET_KEY=your-secret-key-here
TENCENTCLOUD_REGION=ap-guangzhou
```

**Obtaining Credentials** (if needed):
1. Visit [Tencent Cloud Console - Access Keys](https://console.cloud.tencent.com/cam/capi)
2. Click "Create Key" to create API credentials
3. Copy **SecretId** and **SecretKey**

### Custom Region and Endpoint

Users can customize region and endpoint:

```typescript
import { HunyuanNativeClient, createNativeClient } from './lib/deepresearch';

// Custom region only
const client = createNativeClient();
// Set TENCENTCLOUD_REGION=ap-beijing in .env

// Custom endpoint
const client = new HunyuanNativeClient({
  secretId: process.env.TENCENTCLOUD_SECRET_ID!,
  secretKey: process.env.TENCENTCLOUD_SECRET_KEY!,
  region: 'ap-beijing'
});
```

## Quick Start

### Basic Usage

```typescript
import { createNativeClient } from './lib/deepresearch';

const client = createNativeClient();
```

### Search-Enhanced Conversations

```typescript
// Get latest information
const response = await client.chatWithEnhancement(
  'What are the latest advances in artificial intelligence in 2025?'
);
console.log(response.content);

// Real-time data queries
const market = await client.chatWithEnhancement(
  'How is the global tech stock market performing currently?'
);

// News and events
const news = await client.chatWithEnhancement(
  'What are the recent important tech news?'
);
```

### Real-Time LLM Tracking

```typescript
// Track OpenAI latest updates
const openai = await client.chatWithEnhancement(
  'What new models and important updates has OpenAI released in 2025?'
);

// Compare mainstream models
const comparison = await client.chatWithEnhancement(
  'Compare the performance and features of the latest versions of GPT-4, Claude, and Gemini'
);

// Track AI application trends
const trends = await client.chatWithEnhancement(
  'What innovative applications based on large language models have recently received funding or launched?'
);
```

### Research Analysis

```typescript
const research = await client.chatWithEnhancement(
  'Summarize the major breakthroughs in artificial intelligence in 2025'
);
```

## Response Structure

```typescript
{
  content: string;           // Generated answer content
  finishReason: string;      // Completion reason
  usage: {
    promptTokens: number;    // Input token count
    completionTokens: number; // Output token count
    totalTokens: number;     // Total token count
  };
  id: string;               // Response ID
  model: string;            // Model used
  searchInfo?: any;         // Search information (when enhancement is enabled)
}
```

## Architecture Integration

### Service Layer Pattern (Recommended)

```typescript
// src/services/research.service.ts
import { createNativeClient } from '../lib/deepresearch';

export class ResearchService {
  private client = createNativeClient();
  
  async analyzeLatestTrends(topic: string): Promise<string> {
    const response = await this.client.chatWithEnhancement(
      `Analyze the latest trends and developments in ${topic}`
    );
    return response.content;
  }
  
  async compareTechnologies(technologies: string[]): Promise<string> {
    const response = await this.client.chatWithEnhancement(
      `Compare the following technologies in detail: ${technologies.join(', ')}`
    );
    return response.content;
  }
  
  async getMarketInsights(sector: string): Promise<{
    content: string;
    searchInfo: any;
  }> {
    const response = await this.client.chatWithEnhancement(
      `What are the current market insights and trends for ${sector}?`
    );
    return {
      content: response.content,
      searchInfo: response.searchInfo
    };
  }
}
```

## Security Best Practices

1. **Never commit credentials**: Add `.env` to `.gitignore`
2. **Use environment variables**: Store sensitive configuration via environment variables
3. **Principle of least privilege**: Use sub-accounts with only necessary API permissions
4. **Rotate credentials regularly**: Recommend changing API credentials every 90 days
5. **Validate search results**: Always verify information from search-enhanced responses for critical decisions

## Troubleshooting

**Authentication Errors**
- Verify credentials in `.env` file if using custom configuration
- Confirm API credentials are enabled in Tencent Cloud Console

**Network Errors**
- Check firewall and proxy settings
- Confirm access to `hunyuan.tencentcloudapi.com` or proxy endpoint
- Try setting longer timeout (default: 120 seconds for deep reasoning)

**Search Enhancement Issues**
- Ensure internet connectivity for search-enhanced queries
- Check if search results are returned in `searchInfo` field
- Some queries may not trigger search; try rephrasing for current events

**Timeout Errors**
- Deep reasoning may take longer; increase timeout if needed
- Default timeout is 120 seconds (2 minutes)

## Resources

- **SDK Wrapper Source**: `lib/deepresearch.ts`
- **Official Documentation**: https://cloud.tencent.com/document/product/1729/105701
- **API Reference**: https://cloud.tencent.com/document/api/1729/105701
- **Console**: https://console.cloud.tencent.com/hunyuan
