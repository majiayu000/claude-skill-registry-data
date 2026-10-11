---
name: xiaohongshu-cn
description: 小红书分析 - 热门笔记发现、关键词监控、趋势分析（Instagram 中国版）
metadata:
  openclaw:
    emoji: "📕"
    category: "social"
    tags: ["xiaohongshu", "red", "china", "instagram", "social-media"]
---

# 小红书分析

热门笔记发现、关键词监控、趋势分析。

## 功能

- 📕 热门笔记发现
- 🔍 关键词搜索
- 📊 趋势分析
- 👥 博主分析

## ⚠️ 重要提示

**本 Skill 为信息参考类**，提供小红书数据获取的方法和工具建议。由于小红书没有公开 API，如需实际获取数据，需要以下方式之一：

### 1. 网页爬虫

```bash
# 使用现有爬虫项目
git clone https://github.com/Big-Buffer/XiaohongshuSpider
cd XiaohongshuSpider
pip install -r requirements.txt
python main.py
```

### 2. 小程序抓包

```bash
# 参考
# https://github.com/lonngxiang/xiaohongshu-spider
```

### 3. 手动查询

直接访问小红书网页版：
- 热门: https://www.xiaohongshu.com/explore
- 搜索: https://www.xiaohongshu.com/search_result

## 热门分类

| 分类 | 关键词 |
|------|--------|
| 美妆 | 护肤、彩妆、测评 |
| 穿搭 | OOTD、日常穿搭 |
| 美食 | 探店、食谱 |
| 旅行 | 攻略、打卡 |
| 家居 | 装修、好物 |

## 使用场景

### 1. 内容创作

- 发现热门话题
- 学习爆款标题
- 分析竞品笔记

### 2. 市场研究

- 了解用户偏好
- 追踪品牌声量
- 发现新品趋势

### 3. 营销推广

- 找到 KOL
- 分析投放效果
- 优化内容策略

## 数据字段

| 字段 | 说明 |
|------|------|
| note_id | 笔记 ID |
| title | 标题 |
| desc | 描述 |
| author | 作者 |
| likes | 点赞数 |
| comments | 评论数 |
| shares | 分享数 |
| tags | 标签 |

## 与其他平台对比

| 平台 | 对应美国平台 | 特点 |
|------|-------------|------|
| **小红书** | Instagram/Pinterest | 图文+短视频 |
| 抖音 | TikTok | 短视频 |
| B站 | YouTube | 长视频 |
| 知乎 | Quora | 问答 |

## 注意事项

1. **合规爬虫**: 遵守 robots.txt
2. **频率限制**: 不要过于频繁请求
3. **账号风险**: 频繁爬虫可能导致封号
4. **数据用途**: 仅用于个人研究

## 推荐工具

- [XiaohongshuSpider](https://github.com/Big-Buffer/XiaohongshuSpider) - Python 爬虫
- [xiaohongshu-spider](https://github.com/63can/xiaohongshu-spider) - Selenium + Fiddler
- [Nanji](https://www.nanji.com/) - 数据分析平台

### 在此环境中的替代方案

如果你正在使用 Aily 环境，可以：
- 使用 `aily-browser` skill 进行浏览器自动化操作
- 结合 `web_search` 工具获取小红书相关公开信息
- 使用 `fetch` 工具获取小红书网页版公开内容

---

*版本: 1.0.0*
*注意: 小红书 API 需要逆向工程*
