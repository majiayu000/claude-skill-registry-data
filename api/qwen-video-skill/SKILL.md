---
name: qwen-video-skill
description: Use when the user shares, pastes, or references a video (local path or URL) and needs Qwen3.8-Max to describe, summarize, analyze, or recognize its content. Run the bundled video.js helper to convert the video into text.
---

# 视频理解 Helper

当前模型可能无法直接读取视频。当用户提供视频路径或 URL 时，不要依赖直接查看，改用 `video.js` 把视频转成文字：

```bash
node C:\Users\keyzo\.codex\skills\qwen-video-skill\video.js "<absolute video path>" "<prompt>"
```

远程视频 URL：

```bash
node C:\Users\keyzo\.codex\skills\qwen-video-skill\video.js --url "<video url>" "<prompt>"
```

可选参数：

- `--fps <0.1-10>`：视频抽帧频率，默认 `2.0`。高速运动场景建议调高，静态或长视频建议调低。
- `--max-tokens <number>`：输出上限，默认 `2048`。
- `--upload-oss`：强制把本地视频上传到 OSS 后用 URL 传入；默认只在超过 Base64 限制时自动上传。

规则：

- 始终使用 `video.js` 的绝对路径。
- 本地视频使用绝对路径，远程视频使用 `--url`。
- 默认用中文描述，除非用户要求其他语言。
- 配置在 `video.js` 同目录的 `.env`（`DASHSCOPE_API_KEY`、`VIDEO_MODEL`、`DASHSCOPE_BASE_URL`、`VIDEO_FPS`）。不要打印或提交 API Key。
- Qwen3.8 系列限制：本地视频以 Base64 编码后须小于 10MB，公网 URL 最大 2GB，时长 2 秒至 2 小时，支持 MP4/AVI/MKV/MOV/FLV/WMV 等格式；视频音频不被理解。
- 本地视频超过 Base64 限制时，`video.js` 会自动上传到阿里云 OSS 并生成 URL 再调用模型；`--upload-oss` 可强制走 OSS。
- OSS 配置也在 `.env`：必填 `OSS_ACCESS_KEY_ID`、`OSS_ACCESS_KEY_SECRET`、`OSS_BUCKET` 和 `OSS_REGION`（或 `OSS_ENDPOINT`）；可选 `OSS_PREFIX`（默认 `codex-videos/`）、`OSS_PUBLIC_BASE_URL`（自定义公网域名）、`OSS_URL_EXPIRES`（默认 3600 秒）。不要打印或提交 OSS 凭证。
- 如果 API 调用失败，把错误报告给用户，并请其检查 Key、模型名或 Base URL。
