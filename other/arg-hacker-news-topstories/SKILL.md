---
name: arg-hacker-news-topstories
description: Only use this skill when the user explicitly invokes /arg-hacker-news-topstories or clearly asks to run this ARG chain. Queries the official public Hacker News API top stories endpoint, normalizes results to JSON, validates them, and renders a Markdown report.
allowed-tools: Bash
---

# arg-hacker-news-topstories

## 触发方式

仅接受显式命令触发：`/arg-hacker-news-topstories`

不要从普通自然语言问题中猜测触发，除非用户明确要求执行这条 Hacker News Top Stories 查询链。

```text
设 OUTPUT_DIR = "output"
设 PLANS_DIR = "plans"
设 SCRIPTS_DIR = "scripts"
设 "当前步" = "step-00-cleanup"

循环：
1. 读取 PLANS_DIR/当前步.md
2. 严格按文件中的【任务】说明执行
3. 执行文件中的【验证命令】
4. 验证通过 → 读取文件末尾【下一步】，赋值给当前步
5. 验证失败 → 按文件中的【验证失败处理】执行
6. 当前步 = "TERMINAL" → 退出循环，输出执行汇报
```

起始：读取 `PLANS_DIR/step-00-cleanup.md`。

## 关键原则

1. **逐步揭示**：你只知道当前这一步。每步末尾的【下一步】会告诉你该读哪个文件。不要推测或预判后续步骤。
2. **验证门禁**：每步必须通过验证命令才能进入下一步。验证失败必须按失败处理执行。
3. **字段受限**：脚本负责生成标准 JSON；Agent 不手工改写 `output/hn-topstories.json`。
4. **路径稳定**：命令使用约定的 OUTPUT_DIR/PLANS_DIR/SCRIPTS_DIR，不依赖未知工作目录。
5. **不得自证**：不能用“我检查过了”代替验证命令。
