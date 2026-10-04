---
name: hook-test-kit
description: |
  为 Claude Code hook 脚本（PreToolUse / SessionStart / UserPromptSubmit 等）生成行为矩阵测试骨架并指导填场景：scratch fixture 隔离、stdin 喂 JSON、EMPTY/!否定/正则断言协议、已知 bash 坑位预修（路径混入子命令、$var 后跟全角字符、case 变量 pattern 不解析交替）。Use when 用户写了或改了 hook 脚本要测试，说 测一下这个 hook、hook 测试、hook-test-kit、给 hook 补测试。
trigger: /hook-test-kit
compatibility: Claude Code
license: MIT
---

# hook-test-kit

给 hook 脚本配一套行为矩阵测试。hook 是用户环境里的高频基建，一个静默放行/误报
直接影响每一次会话——它值得和业务代码同等的测试纪律。

## 前置依赖

- `bash`、`git`、`jq`（`which jq` 检查，缺失即停下说明）
- 被测 hook 脚本路径

## 执行步骤

### 1. 生成骨架

```bash
bash <本 SKILL.md 所在目录>/scripts/scaffold.sh <hook 脚本路径> [输出目录]
```

输出 `<输出目录|hook 同目录>/test_<hook名>.sh`，含可运行的 run/assert 协议与 2 个
TODO 场景。骨架已预修以下高频坑，**不要改掉**：

- 辅助函数用 `local d="$1"; shift` 转发参数，不把路径混进子命令
- 输出文本中变量一律 `${var}` 花括号（`$var` 后紧跟全角字符会被 bash 吃进变量名）
- 断言协议：`EMPTY` = 输出必须为空；`!pattern` = 必须不命中；其余 = egrep 必须命中
- `case` 的 pattern 来自变量时不解析 `|` 交替与 `[...]` 字符类——多模式用循环逐个判定

### 2. 按 hook 语义填场景

最小矩阵（每个 hook 至少覆盖）：

| 维度 | 场景 |
|------|------|
| 快速门 | 非 hook 目标命令 → 放行/无输出 |
| 主路径放行 | 正常输入 → 预期放行（断言退出码与输出均为空或合法 JSON） |
| 主路径拦截 | 越界输入 → 预期 ask/deny（断言 permissionDecision 与文案） |
| 变异防护 | 每条拦截规则改坏一版（取反/删条件）跑套件必须变红，改回必须复绿 |

PreToolUse 喂 `{"tool_input":{"command":...},"cwd":...}`；SessionStart 喂 `{}`；
UserPromptSubmit 喂 `{"prompt":...,"cwd":...}`。以被测 hook 实际读取的字段为准。

fixture 一律放 scratch 目录（`mktemp -d` + trap 清理），需要 git 仓库就现场 init；
**绝不**指向用户真实目录。

### 3. 收尾：变异实验

套件全绿后，对每条拦截规则做一次变异（取反、删条件、改边界），确认套件**变红**；
改回后**复绿**。不变红的断言是装饰，删掉或写尖锐。这一步没做，测试不算交付。

## 输出格式

- 测试文件落在被测 hook 同目录（或指定输出目录），命名 `test_<hook名>.sh`
- 结尾输出 `── 通过 N / 失败 M`，退出码 0 仅当 M=0
- 向用户报告：场景数、变异实验结果、遗留盲区

## 错误处理

- hook 路径不存在 → 报错退出，不生成
- hook 无执行位 → 生成时顺带 `chmod +x` 并提示
- 被测 hook 需要 GPU/浏览器等重环境 → 在场景里标注 SKIP 并如实报告未覆盖
