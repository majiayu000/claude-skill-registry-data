---
name: fix-nls-gaps
description: 排查并修复「用户可见文本没走 localize / 中文硬编码漏本地化 / 中文 defaultMessage 泄漏到英文界面」。当用户说某文案没本地化、找未本地化的文本、本地化查漏补缺、英文界面冒出中文（或中文界面冒出英文）时使用。覆盖三种遗漏形态的扫描、修复写法约定、zh-CN.ts 补译与验证链。
disable-model-invocation: true
---

# 修复本地化遗漏（裸文本 / 中文 defaultMessage / zh-CN 缺 key）

本仓库走 `localize(key, defaultMessage, vars?)`（`packages/platform/src/nls/nls.ts`），中文集中在 `apps/editor/src/shared/i18n/messages/zh-CN.ts`；en-US.ts 只是**不完整**的历史子集，英文由 defaultMessage 兜底。

## 核心机制：兜底链决定一切

```
translated = state.messages[key] ?? state.fallbackMessages[key]   // zh-CN.ts ?? en-US.ts
template   = translated ?? defaultMessage
```

由此推出三条铁律：

1. **defaultMessage 必须写英文**。zh-CN 缺 key 时会落到 en-US.ts（多半也没有）→ 落到 defaultMessage——default 写中文 = 中文泄漏到英文界面。反之英文 default 是安全兜底。
2. **e2e 断言的是 defaultMessage 原文**。两套 e2e fixture 都 pin `workbench.language=en-US`，zh-CN.ts 在 e2e 里不生效。改了 defaultMessage / 把裸中文改成 localize，必须同步 grep e2e spec 里的旧文案断言。
3. **「已 localize 但 zh-CN.ts 缺 key」是隐性遗漏**：zh-CN 用户此时看到 defaultMessage（英文）。发现中文界面出英文，先查 key 是否在 zh-CN.ts。

## 三种遗漏形态与修法

| 形态 | 识别 | 修法 |
|---|---|---|
| ① 裸文本（没走 localize） | grep 出中文/英文字面量直接渲染或抛错 | 就地 `localize('域.key', 'English default', { vars })`，中文入 zh-CN.ts |
| ② 中文 defaultMessage | `localize('...', '中文')` | default 换英文，中文入 zh-CN.ts（同 key） |
| ③ zh-CN.ts 缺 key | 代码已有 localize 但 zh-CN 界面显示英文 | 只补 zh-CN.ts，default 不动 |

## 第 1 步：扫描

```bash
# 裸中文（形态①）：排除注释/测试/消息表/localize 行
grep -rn -P '[\x{4e00}-\x{9fff}]' apps/editor/src packages/workbench-ui/src packages/platform/src \
  --include='*.ts' --include='*.tsx' \
  | grep -v '\.test\.' | grep -v '__tests__' | grep -vP '//|/\*|\* |messages/(zh-CN|en-US)' \
  | grep -vP "localize2?\("

# 中文 defaultMessage（形态②，同行）
grep -rn -P "localize2?\('[^']+', '[^']*[\x{4e00}-\x{9fff}]" \
  apps/editor/src packages/workbench-ui/src packages/platform/src --include='*.ts' --include='*.tsx' \
  | grep -v '\.test\.'

# 形态②跨行变体（key 与 default 分行）：-A2 后滤中文
grep -rn -P "localize2?\(" apps/editor/src packages/workbench-ui/src packages/platform/src \
  --include='*.ts' --include='*.tsx' -A2 | grep -P "'[^']*[\x{4e00}-\x{9fff}]" | grep -v '\.test\.'

# 形态③：某 key 是否已在 zh-CN.ts
grep -n "'<key>'" apps/editor/src/shared/i18n/messages/zh-CN.ts
```

## 第 2 步：排除项（这些刻意保留中文/不 localize）

- **发给 agent/模型的文本**：协议恢复语（如 `CONTINUE_PROMPT_TEXT = '继续'`）、few-shot prompt 示例。
- **中文搜索关键词表**（如 contextSuggestions 的中文别名、COMMIT_MATCH_KEYWORDS）——是匹配数据不是 UI 文案。
- **placeholder 值示例**（`sk-…`、`gpt-5.1-codex`、`**/*.ts`）、协议标识符、语言专名、Output channel 名。
- **日志 / console / logger 文本**、开发者向面板（Startup Performance 里程碑）。
- **注释**（含 JSX `{/* */}`，注意跨行注释会被 grep 误报）。
- **测试 fixture 自造串**（测试里 new Error('中文') 模拟错误、自造 markdown）——除非断言的就是生产文案。
- e2e spec 里的中文多为**测试数据**（文档内容、文件名），不受影响；只有断言 UI 文案的才要改。

边界判定拿不准的：issue 报告模板这类「贴到外部（GitHub）的文本」用英文（国际化惯例）；CLI `--help` 输出统一英文（`ConfigItem.description` 只被 cliHelp 消费）。

## 第 3 步：修复写法约定

- **key 命名**：Action2 title → `action.<domain>.<camelName>`（用 `localize2`，命令面板匹配用 original）；其余按 `<domain>.<thing>[.desc]`，沿用既有分节前缀（`search.*` / `dialog.*` / `common.*`…）。
- **变量插值**：模板字符串拼接改 `{var}` 具名占位 + 对象参——语序随语言变，绝不拼接。`'文件不存在: ' + path` → `localize('markdown.linkFileNotFound', 'File does not exist: {path}', { path })`。
- **复用已有 key**：'取消' → `common.cancel` 等，先 grep zh-CN.ts 查重。
- **同文案多处共用 key**：如三个编辑器的加载态共用 `editor.loading`；两个预览 input 共用 `editor.previewTitle`。
- **模块求值时序**：renderer 模块级 localize 安全；**main 侧顶层常量不行**（NLS 装配晚于模块求值）——顶层表改函数内解析（先例：`VENDOR_DESCRIPTORS` 用 labelKey + 函数内 resolve；`MarkdownPreviewHelp` 的 SHORTCUTS 常量改 `shortcuts()` 函数）。
- **Monaco 命令 label**：先查 `__MONACO_NLS__` 表（按英文源文本为键）是否覆盖，未覆盖的走 labelKey + localize。

## 第 4 步：zh-CN.ts 补译

- 按现有 `// --- <域> ---` 分节插入，新域新建分节；统一在最后一轮一次写入，避免多轮往返。
- 翻译与 defaultMessage 语义对齐；变量名保持一致（`{count}` / `{name}`…）。

## 第 5 步：验证链（顺序执行，每步过了再下一步）

```bash
pnpm exec prettier --write <改动的文件…>   # PostToolUse hook 可能留行宽 lint 错误
pnpm --filter @universe-editor/platform build   # 仅当改了 platform（apps 看 dist/）
pnpm check                                     # lint + typecheck + 相关测试
pnpm --filter @universe-editor/editor test:unit   # 全量单测——断言漂移在这暴露
pnpm --filter @universe-editor/editor build    # e2e 跑 out/ 产物
pnpm e2e:smoke                                 # @p0 冒烟
```

**断言漂移处理**（必然遇到，分两类）：

- **单测断言旧文案**：测试环境 localize 返回 defaultMessage，断言写英文 default 原文（不再写中文）。逐文件 grep 旧文案改断言。
- **e2e 断言旧文案**：e2e pin en-US → 断言的同样是 defaultMessage 原文。改完全局扫一遍：
  ```bash
  grep -rn -P '[\x{4e00}-\x{9fff}]' apps/editor/e2e/specs/ | grep -vE '//|/\*|\* ' | grep -vP 'describe\(|test\('
  ```
  逐个判定是 UI 文案断言（要改）还是测试数据（保留）。

**收尾全量复扫**：三种形态各跑一遍第 1 步的命令，确认清零（排除项除外）。

## 易踩坑速记

1. **单行 grep 漏跨行 localize**：key 与 defaultMessage 分行的调用要 `-A2` 扫，别只看单行。
2. **改了 platform 要 rebuild**：apps 看 `dist/`，否则 typecheck/单测拿旧产物。
3. **PostToolUse prettier hook 会重排 JSX**：可能制造行宽 lint 错误，验证前先手动 `prettier --write`。
4. **cliHelp 的 description 别 localize**：`--help` 在 NLS 装配前就可能输出，且 CLI 惯例英文；`ConfigItem.description` 仅 cliHelp 消费。
5. **别动 en-US.ts**：它只是兜底子集，新增 key 不需要补（defaultMessage 即英文）。
6. **单测里断言 localize 结果 = 断言 defaultMessage**；若想验证 zh-CN 翻译，没有现成机制——不要为翻译写测试，只保证 key 存在于 zh-CN.ts。

## 关键参考路径

- `packages/platform/src/nls/nls.ts` —— localize/localize2 与兜底链实现
- `apps/editor/src/shared/i18n/messages/zh-CN.ts` —— 中文消息表（分节结构）
- `apps/editor/src/shared/i18n/availableLocales.ts` —— locale 装配（`configureEditorNls`）
- `apps/editor/src/renderer/workbench/editor/monaco/monacoActionsBridge.ts` —— Monaco 命令 label 的 NLS 查表兜底
- `packages/platform/src/configuration/sources/cliHelp.ts` —— `--help` 文本生成（英文惯例的例外域）

## 其它

- 后续用本 skill，发现新经验，需同步更新本文件
