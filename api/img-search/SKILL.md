---
name: img-search
description: 通过关键词搜索Unsplash图片，返回图片下载地址。当需要获取免费高质量图片时使用此技能。触发场景：搜索图片、获取图库素材、下载图片URL。
_meta_type: sdk
---

# 图片搜索 (Unsplash)

通过关键词搜索Unsplash图片，返回可直接下载的图片URL。

## 使用方式

通过 Unsplash 内部 API 搜索图片，模拟浏览器请求，无需认证。

### API 端点

```
https://unsplash.com/napi/search/photos?query={关键词}&per_page={数量}
```

### 请求方式

```bash
curl -s "https://unsplash.com/napi/search/photos?query={关键词}&per_page={数量}" \
  -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" \
  -H "Accept: application/json"
```

### 输出格式

从 API 返回结果中提取需要的字段，输出 JSON：

```json
{
  "total": 10300,
  "total_pages": 515,
  "results": [
    {
      "id": "p6yH8VmGqxo",
      "slug": "orange-tabby-cat-on-yellow-surface-p6yH8VmGqxo",
      "width": 3432,
      "height": 3432,
      "description": null,
      "alt_description": "orange tabby cat on yellow surface",
      "urls": {
        "raw": "https://images.unsplash.com/photo-1596854407944-bf87f6fdd49e?ixid=xxx&ixlib=rb-4.1.0",
        "full": "https://images.unsplash.com/photo-1596854407944-bf87f6fdd49e?crop=entropy&cs=srgb&fm=jpg&ixid=xxx&ixlib=rb-4.1.0&q=85",
        "regular": "https://images.unsplash.com/photo-1596854407944-bf87f6fdd49e?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=xxx&ixlib=rb-4.1.0&q=80&w=1080",
        "small": "https://images.unsplash.com/photo-1596854407944-bf87f6fdd49e?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=xxx&ixlib=rb-4.1.0&q=80&w=400",
        "thumb": "https://images.unsplash.com/photo-1596854407944-bf87f6fdd49e?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=xxx&ixlib=rb-4.1.0&q=80&w=200"
      }
    }
  ]
}
```

### 示例

**搜索「cat」，获取2张图片：**

请求：
```bash
curl -s "https://unsplash.com/napi/search/photos?query=cat&per_page=2" \
  -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
  -H "Accept: application/json"
```

输出：
```json
{
  "total": 10300,
  "total_pages": 5150,
  "results": [
    {
      "id": "p6yH8VmGqxo",
      "slug": "orange-tabby-cat-on-yellow-surface-p6yH8VmGqxo",
      "width": 3432,
      "height": 3432,
      "description": null,
      "alt_description": "orange tabby cat on yellow surface",
      "urls": {
        "raw": "https://images.unsplash.com/photo-1596854407944-bf87f6fdd49e?ixid=M3wxMjA3fDB8MXxzZWFyY2h8MTh8fGNhdHxlbnwwfHx8fDE3Njk2NzQ1ODl8MA&ixlib=rb-4.1.0",
        "full": "https://images.unsplash.com/photo-1596854407944-bf87f6fdd49e?crop=entropy&cs=srgb&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MTh8fGNhdHxlbnwwfHx8fDE3Njk2NzQ1ODl8MA&ixlib=rb-4.1.0&q=85",
        "regular": "https://images.unsplash.com/photo-1596854407944-bf87f6fdd49e?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MTh8fGNhdHxlbnwwfHx8fDE3Njk2NzQ1ODl8MA&ixlib=rb-4.1.0&q=80&w=1080",
        "small": "https://images.unsplash.com/photo-1596854407944-bf87f6fdd49e?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MTh8fGNhdHxlbnwwfHx8fDE3Njk2NzQ1ODl8MA&ixlib=rb-4.1.0&q=80&w=400",
        "thumb": "https://images.unsplash.com/photo-1596854407944-bf87f6fdd49e?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MTh8fGNhdHxlbnwwfHx8fDE3Njk2NzQ1ODl8MA&ixlib=rb-4.1.0&q=80&w=200"
      }
    },
    {
      "id": "cWOzOnSoh6Q",
      "slug": "close-up-photo-of-tabby-cat-cWOzOnSoh6Q",
      "width": 6000,
      "height": 4000,
      "description": "Blue-eyed cat portrait",
      "alt_description": "close up photo of tabby cat",
      "urls": {
        "raw": "https://images.unsplash.com/photo-1478098711619-5ab0b478d6e6?ixid=M3wxMjA3fDB8MXxzZWFyY2h8MTl8fGNhdHxlbnwwfHx8fDE3Njk2NzQ1ODl8MA&ixlib=rb-4.1.0",
        "full": "https://images.unsplash.com/photo-1478098711619-5ab0b478d6e6?crop=entropy&cs=srgb&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MTl8fGNhdHxlbnwwfHx8fDE3Njk2NzQ1ODl8MA&ixlib=rb-4.1.0&q=85",
        "regular": "https://images.unsplash.com/photo-1478098711619-5ab0b478d6e6?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MTl8fGNhdHxlbnwwfHx8fDE3Njk2NzQ1ODl8MA&ixlib=rb-4.1.0&q=80&w=1080",
        "small": "https://images.unsplash.com/photo-1478098711619-5ab0b478d6e6?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MTl8fGNhdHxlbnwwfHx8fDE3Njk2NzQ1ODl8MA&ixlib=rb-4.1.0&q=80&w=400",
        "thumb": "https://images.unsplash.com/photo-1478098711619-5ab0b478d6e6?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MTl8fGNhdHxlbnwwfHx8fDE3Njk2NzQ1ODl8MA&ixlib=rb-4.1.0&q=80&w=200"
      }
    }
  ]
}
```

## 字段说明

| 字段 | 说明 |
|------|------|
| `total` | 搜索结果总数 |
| `total_pages` | 总页数 |
| `results[].id` | 图片唯一ID |
| `results[].slug` | 图片slug（含描述） |
| `results[].width` | 图片原始宽度 |
| `results[].height` | 图片原始高度 |
| `results[].description` | 图片描述（可能为null） |
| `results[].alt_description` | 图片alt描述 |
| `results[].urls.raw` | 原始尺寸URL |
| `results[].urls.full` | 完整尺寸（带压缩） |
| `results[].urls.regular` | 常规尺寸 (1080px宽) |
| `results[].urls.small` | 小尺寸 (400px宽) |
| `results[].urls.thumb` | 缩略图 (200px宽) |

## API 参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `query` | 搜索关键词（必填） | - |
| `per_page` | 每页数量 | 20 |
| `page` | 页码 | 1 |

## 下载图片

`urls` 中的链接可直接下载：

```bash
curl -o image.jpg "https://images.unsplash.com/photo-xxx?w=400"
```

## 后台 TypeScript 使用示例

### 封装服务层

```typescript
// src/services/image-search.service.ts
interface UnsplashImage {
  id: string;
  slug: string;
  width: number;
  height: number;
  description: string | null;
  alt_description: string | null;
  urls: {
    raw: string;
    full: string;
    regular: string;
    small: string;
    thumb: string;
  };
}

interface SearchResponse {
  total: number;
  total_pages: number;
  results: UnsplashImage[];
}

export class ImageSearchService {
  private readonly baseUrl = 'https://unsplash.com/napi/search/photos';
  private readonly headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json'
  };

  async search(query: string, options?: { perPage?: number; page?: number }): Promise<SearchResponse> {
    const { perPage = 20, page = 1 } = options || {};
    const url = `${this.baseUrl}?query=${encodeURIComponent(query)}&per_page=${perPage}&page=${page}`;
    
    const response = await fetch(url, { headers: this.headers });
    if (!response.ok) {
      throw new Error(`Image search failed: ${response.status}`);
    }
    
    return response.json();
  }

  async getImageUrls(query: string, count: number = 5): Promise<string[]> {
    const result = await this.search(query, { perPage: count });
    return result.results.map(img => img.urls.regular);
  }
}
```

### Express 路由示例

```typescript
// src/routes/image.routes.ts
import { Router } from 'express';
import { ImageSearchService } from '../services/image-search.service';

const router = Router();
const imageService = new ImageSearchService();

router.get('/search', async (req, res) => {
  try {
    const { q, count = '5' } = req.query;
    if (!q || typeof q !== 'string') {
      return res.status(400).json({ error: 'Query parameter "q" is required' });
    }
    
    const results = await imageService.search(q, { perPage: parseInt(count as string) });
    res.json(results);
  } catch (error) {
    res.status(500).json({ error: 'Image search failed' });
  }
});

router.get('/urls', async (req, res) => {
  try {
    const { q, count = '5' } = req.query;
    if (!q || typeof q !== 'string') {
      return res.status(400).json({ error: 'Query parameter "q" is required' });
    }
    
    const urls = await imageService.getImageUrls(q, parseInt(count as string));
    res.json({ urls });
  } catch (error) {
    res.status(500).json({ error: 'Image search failed' });
  }
});

export default router;
```

### 使用示例

```typescript
// 基本使用
const imageService = new ImageSearchService();

// 搜索图片
const result = await imageService.search('sunset beach', { perPage: 10 });
console.log(`Found ${result.total} images`);
result.results.forEach(img => {
  console.log(`- ${img.alt_description}: ${img.urls.small}`);
});

// 快速获取图片URL列表
const urls = await imageService.getImageUrls('mountain landscape', 3);
// ['https://images.unsplash.com/...', 'https://images.unsplash.com/...', ...]
```

## 注意事项

1. **模拟浏览器** - 必须设置 User-Agent 请求头
2. **直接下载** - `urls` 中的链接可直接下载，无需认证
3. **无需API密钥** - 使用内部API，无需注册开发者账号
