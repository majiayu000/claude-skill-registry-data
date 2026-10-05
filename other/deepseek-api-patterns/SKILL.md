---
name: deepseek-api-patterns
description: DeepSeek API 使用模式 — ReAct Agent、Function Calling、中文交互的坑和最佳实践
category: mlops
---

# DeepSeek API Patterns

使用 DeepSeek API（通过 `openai` Python 库，`base_url="https://api.deepseek.com"`）时的常见模式和陷阱。

## 环境

```python
from openai import OpenAI
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)
```

## ReAct Agent 模式

### 关键陷阱：模型不尊重 PAUSE

DeepSeek 的 `deepseek-chat` 不会在 ReAct prompt 的 `PAUSE` 处停止。它会一次性生成整个多步循环（包括幻觉的 Observation）。

**修复**：在 API 调用中加 `stop=["PAUSE"]`：

```python
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages,
    stop=["PAUSE"],  # 关键：强制模型在此停止
)
```

### 中文冒号兼容

DeepSeek 可能输出中文冒号 `：` 而非 ASCII `:`。所有正则解析必须兼容两者：

```python
# 不要这样
re.search(r"Action:\s*(\w+)", text)
re.search(r"Final Answer:\s*(.*)", text)

# 要这样
re.search(r"Action[:：]\s*(\w+)", text)
re.search(r"Final Answer[:：]\s*(.*)", text)
re.search(r"Action Input[:：]\s*(.*)", text)
```

### ReAct 循环标准流程

```
Thought → Action → Action Input → PAUSE → [代码执行工具] → Observation → 循环
```

参考实现见 `references/react-agent-full.py`。

## Function Calling 模式

DeepSeek 完全兼容 OpenAI 的 function calling 格式。标准模式无需特殊处理。

## Provider Selection & Pricing

DeepSeek introduced peak/off-peak pricing for V4正式版 (mid-July 2026): 2x during 9-12 and 14-18 Beijing time. 硅基流动 offers same models at flat pricing (no peak surcharge), OpenAI-compatible API. See `references/provider-pricing.md` for current comparison.

**Pitfall**: web_search/web_extract often return stale pricing. Use browser tools to check actual provider pricing pages.

## 代理配置

使用 Clash 代理时，设置环境变量：
```bash
export HTTP_PROXY=http://127.0.0.1:7890
export HTTPS_PROXY=http://127.0.0.1:7890
```

## WSL + NTFS venv 陷阱

项目在 `/mnt/e/...` 等 Windows 盘上时，`uv` 在 NTFS 上操作 `.venv` 可能遇到权限错误（`Operation not permitted`）。

**方案**：把 venv 放在 Linux 文件系统（`/home/po/.venvs/<name>`），项目里用软链接：
```bash
uv venv --python 3.13 /home/po/.venvs/project-name
ln -sf /home/po/.venvs/project-name .venv
```

**注意**：Windows 不认 Linux 软链接。如果需要在 Windows 侧 `uv run`，先 `rm .venv` 让它自动重建。
