---
name: model-usage
description: 使用 CodexBar CLI 本地成本使用情况来汇总 Codex 或 Claude 的按模型使用情况，包括当前（最新）模型或完整的模型细分。当被要求提供 codexbar 的模型级别使用/成本数据，或需要从 codexbar cost JSON 获取可脚本化的按模型摘要时触发。
metadata: {"clawdbot":{"emoji":"📊","os":["darwin"],"requires":{"bins":["codexbar"]},"install":[{"id":"brew-cask","kind":"brew","cask":"steipete/tap/codexbar","bins":["codexbar"],"label":"安装 CodexBar (brew cask)"}]}}
---

# 模型使用情况

## 概述
从 CodexBar 的本地成本日志中获取按模型的使用成本。支持"当前模型"（最新的每日条目）或"所有模型"摘要，适用于 Codex 或 Claude。

待办：一旦 CodexBar CLI 在 Linux 上的安装路径有文档说明，将添加 Linux CLI 支持指南。

## 快速开始
1) 通过 CodexBar CLI 获取成本 JSON 或传递一个 JSON 文件。
2) 使用捆绑的脚本按模型汇总。

```bash
python {baseDir}/scripts/model_usage.py --provider codex --mode current
python {baseDir}/scripts/model_usage.py --provider codex --mode all
python {baseDir}/scripts/model_usage.py --provider claude --mode all --format json --pretty
```

## 当前模型逻辑
- 使用包含 `modelBreakdowns` 的最新每日行。
- 选择该行中成本最高的模型。
- 当缺少细分时，回退到 `modelsUsed` 的最后一个条目。
- 当需要特定模型时，使用 `--model <name>` 覆盖。

## 输入
- 默认：运行 `codexbar cost --format json --provider <codex|claude>`。
- 文件或标准输入：

```bash
codexbar cost --provider codex --format json > /tmp/cost.json
python {baseDir}/scripts/model_usage.py --input /tmp/cost.json --mode all
cat /tmp/cost.json | python {baseDir}/scripts/model_usage.py --input - --mode current
```

## 输出
- 文本（默认）或 JSON（`--format json --pretty`）。
- 数值仅为每个模型的成本；CodexBar 输出中未按模型拆分 token。

## 参考资料
- 阅读 `references/codexbar-cli.md` 了解 CLI 标志和成本 JSON 字段。
