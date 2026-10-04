---
name: bee
version: 1.0.0
description: 抖音视频一键工作流：下载无水印视频 → 上传阿里云OSS → 写入飞书多维表格。支持各种抖音链接格式，智能提取标题和话题标签。
tags: [douyin, aliyun, oss, feishu, bitable, workflow, video, download]
metadata:
  openclaw:
    emoji: 🎬
    requires:
      bins: [node, python3, curl]
      env: [ALIYUN_OSS_ACCESS_KEY_ID, ALIYUN_OSS_ACCESS_KEY_SECRET, ALIYUN_OSS_ENDPOINT, ALIYUN_OSS_BUCKET, FEISHU_APP_ID, FEISHU_APP_SECRET]
    skills: [douyin-download, aliyun-oss-upload]
---

# douyin-oss-feishu

抖音视频一键工作流：**下载无水印视频 → 上传阿里云OSS → 写入飞书多维表格**

## 功能

- 🎬 自动下载抖音无水印视频（依赖 `douyin-download` skill）
- ☁️ 上传到阿里云 OSS（依赖 `aliyun-oss-upload` skill）
- 📊 自动写入飞书多维表格（Bitable API）
- 🧠 智能提取热点词和话题标签
- ✅ 前置验证：链接格式、工具依赖、环境变量一次性检查
- 🔁 已下载文件自动跳过

## 前置依赖

### Skills（需先安装）

```bash
clawhub install douyin-download
clawhub install aliyun-oss-upload
```

### 环境变量

```bash
# 阿里云 OSS
export ALIYUN_OSS_ACCESS_KEY_ID="your-key-id"
export ALIYUN_OSS_ACCESS_KEY_SECRET="your-key-secret"
export ALIYUN_OSS_ENDPOINT="https://oss-cn-beijing.aliyuncs.com"
export ALIYUN_OSS_BUCKET="your-bucket"

# 飞书应用
export FEISHU_APP_ID="your-app-id"
export FEISHU_APP_SECRET="your-app-secret"
```

### 可选环境变量

```bash
export FEISHU_WIKI_TOKEN="wiki节点token"
export FEISHU_BITABLE_APP_TOKEN="bitable的app_token"
export FEISHU_BITABLE_TABLE_ID="表格ID"
export DOUYIN_DOWNLOAD_DIR="/tmp/douyin-download"
export OSS_PREFIX="douyin"
```

## 使用方法

### 完整工作流

```bash
bash scripts/douyin-workflow.sh "抖音链接"
```

支持链接格式：
- `https://www.douyin.com/video/123456789`
- `https://www.iesdouyin.com/share/video/123456789/...`
- `https://v.douyin.com/xxxxx/`
- APP分享文本中的链接

### 仅解析

```bash
bash scripts/douyin-workflow.sh "抖音链接" --dry-run
```

### 跳过步骤

```bash
bash scripts/douyin-workflow.sh "抖音链接" --skip-oss
bash scripts/douyin-workflow.sh "抖音链接" --skip-feishu
```

## 工作流程

```
抖音链接 → 解析信息 → 下载视频 → OSS上传 → 飞书写入
```

## 飞书多维表格字段映射

| 字段名 | 填充规则 |
|--------|----------|
| 热点词 | 标题去掉#标签后的纯文本 |
| 大概描述 | 完整标题 |
| 话题 | 所有#标签 |
| 视频原始地址 | 抖音标准链接 |
| 阿里OSS地址 | OSS永久访问地址 |
| 状态 | 默认"未制作" |

## 注意事项

- 飞书应用需要 `bitable:app:readonly` 和 `bitable:app` 权限
- 如果表格在 Wiki 中，需设置 `wiki:wiki:readonly` 权限
- OSS Bucket 建议设为私有，通过签名链接访问
- 视频下载到 `/tmp/douyin-download/`，可定期清理
