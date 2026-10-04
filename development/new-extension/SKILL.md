---
name: new-extension
description: 为 Universe Editor 从零创建扩展(插件)。当用户想新建/开发编辑器插件,或想给编辑器加命令、webview 面板、自定义编辑器、语言支持等能力时使用。覆盖需求确认→脚手架→实现→e2e 测试→发布全流程。若用户要移植现有 VSCode 插件,改用 port-vscode-extension。
disable-model-invocation: true
---

# 创建 Universe Editor 扩展

你负责帮用户从零创建一个 Universe Editor 扩展(插件),从需求确认一直到 e2e 测试通过、用户验收,必要时协助发布到扩展市场。整个过程在**用户自己的目录**里进行,产出一个独立的扩展项目。

## 全局规则(红线)

1. **三道确认门**(需求 → 计划 → 验收)未获用户明确同意,不得越过进入下一阶段。
2. **`uex publish` 永远不自动执行**——发布是对外动作,必须用户单独明确同意。
3. **不硬造 API**:Universe Editor 的扩展 API(`@universe-editor/extension-api`)只有文档声明的能力面。遇到做不到的需求,如实告知并给替代方案,绝不编造 API 或 hack 宿主。
4. 任何 token/密钥不写进代码、不写进 settings.json,不回显到对话。
5. 交流语言跟随用户;代码、命令、标识符保持原样。

## 权威资料在哪

三层资料各有分工,**优先读示例与类型声明而不是凭记忆写代码**:

1. **扩展项目里的 API 包**(第 3 步 `npm install` 之后即有):`node_modules/@universe-editor/extension-api/dist/*.d.ts` 是带 JSDoc 的 API 权威面——某个 API 是否存在、签名与语义**以此为最终裁决**;同目录 `README.md` 有最小示例。API 版本变更与激活事件清单以随编辑器分发的开发文档为准(见第 3 条);包根若带 `COMPATIBILITY.md`（随包分发）以包内文件为准。写代码、查签名首选这里。
2. **官方示例仓库**(本地克隆,见下节):每种能力面一个可运行示例且都带 e2e,写某类功能前先找对应示例照着写,比读文档更快更准。
3. **随编辑器分发的开发文档**(概念与指南):本 SKILL.md 位于编辑器安装目录的 `resources/agent-skills/` 下;开发文档在同级的 `resources/docs/extension-dev/zh-CN/`(Windows 默认安装目录 `%LOCALAPPDATA%\Programs\Universe Editor`)。若当前在 universe-editor 仓库的开发模式下,文档位于仓库根 `docs/extension-dev/zh-CN/`。文档地图:`getting-started.md`(上手)、`extension-anatomy.md`(结构)、`contribution-points.md`(贡献点参考,含菜单命令参数)、`context-keys.md`(Context Key 清单,写 `when` 子句时)、`api/`(API 面)、`webview-guide.md`、`language-guide.md`、`debugging.md`、`versioning.md`(engines.universe 语义)、`publishing.md`(发布)、`security-and-trust.md`。

### 示例仓库:克隆与自动更新

官方示例仓库:https://github.com/lovebirdsx/universe-editor-extension-samples 。从第 2 步(定计划)起就要用到;**每次会话首次参考示例前,先跑一遍下面的幂等命令**(存在则 pull 取最新,不存在则克隆):

```bash
SAMPLES_DIR="$HOME/.universe-editor/extension-samples"
if [ -d "$SAMPLES_DIR/.git" ]; then
  git -C "$SAMPLES_DIR" pull --ff-only || echo "pull failed, using existing local copy"
else
  git clone --depth 1 https://github.com/lovebirdsx/universe-editor-extension-samples.git "$SAMPLES_DIR"
fi
```

克隆/pull 失败(离线等)**不阻塞流程**:有旧副本就用旧副本;完全没有就退化为只用 `.d.ts` 与文档,并向用户说明。示例仓库只用于参考,不要在里面写代码。

按能力面找示例(位于 `$SAMPLES_DIR/samples/<name>/`;完整索引与新增示例以克隆副本根 `README.md` 为准):

| 想做什么 | 参考示例 |
|---|---|
| 命令 / 输出通道 | helloworld |
| 状态栏 / 通知 / 进度 / QuickPick·InputBox | statusbar / notifications / progress / quickinput |
| 配置读写与监听 | configuration |
| 文档编辑 / 补全 / CodeLens / 代码操作 / 装饰 / 语义高亮 / 诊断 | document-editing / completions / codelens / code-actions / decorator / semantic-tokens / diagnostic-related-information |
| 树视图 / webview 面板 / 自定义编辑器 / SCM | tree-view / webview-panel / custom-editor / source-control |
| 主题 / 产品图标主题 / 纯声明式贡献 / NLS 本地化 | color-theme / product-icon-theme / declarative-features / l10n |
| timeline / MCP server / workspace.fs | timeline-provider / mcp-server / fsconsumer |

⚠️ 示例仓库始终追最新 SDK;其依赖版本与脚手架生成的不一致时,**以脚手架为准**(脚手架与用户已装的编辑器匹配)——只参考示例的代码模式,不要照抄版本号或 `engines.universe`。

## 第 0 步:环境检测

先跑 `node -v`(需 ≥ 22)和 `npm -v`。缺失或版本过低时,给出安装指引(https://nodejs.org) 并停下等用户处理,不要带病继续。

## 第 1 步:需求确认(门 1)

**一次性问齐**以下问题再动手(若环境支持结构化提问工具就用它,否则在一条消息里列出全部问题):

1. 这个扩展要做什么?(一句话)
2. 有没有想参考/移植的 VSCode 插件?——**有则改走 `port-vscode-extension` 流程**(读本目录旁的 `../port-vscode-extension/SKILL.md`,先做可行性评估再动工)。
3. 只是自己用,还是要发布到扩展市场?(决定 publisher 取名:发布需要已注册并通过审批的 publisher id;自用可临时用 `local`)

## 第 2 步:计划确认(门 2)

根据需求推断扩展形态(纯声明型 / 命令型 / webview 面板 / 自定义编辑器 / 语言支持),先更新示例仓库并定位最接近的示例(见「示例仓库」一节),需要时再读对应文档,然后给用户一页纸计划:

- 扩展 id(小写 npm 命名规则)、displayName、publisher
- 模板选型:`basic`(命令型起点)或 `webview`
- 参考示例:示例仓库中最接近的 1~2 个示例名(没有对应示例就写"无")
- 贡献点清单(commands / keybindings / configuration / menus / customEditors / …)
- 实现要点与已知限制(API 不支持的点此时讲清)
- e2e 测试场景清单——**每条已确认的需求至少对应一条 e2e 用例**

等用户确认后再进入搭建。

## 第 3 步:脚手架

用全旗标非交互形式(交互式提问在 agent 环境会挂起):

```bash
npm create @universe-editor/extension@latest <目录名> -- \
  --name <扩展id> --publisher <publisher> \
  --display-name "<显示名>" --description "<一句话>" --template <basic|webview>
cd <目录名> && npm install && npm run build
```

`npm run build` 与 `npm test` 都通过说明骨架完好。骨架自带 `esbuild.config.mjs`、`tsconfig.json`、`vitest.config.ts`、`src/extension.ts` + `src/hello.ts`(纯逻辑模块范例)、`src/__tests__/`(vitest 单测)、`e2e/`(完整 e2e 骨架:playwright.config.ts + fixtures + 示例 spec)、`scripts/e2e.mjs`(e2e 入口);scripts 有 `build` / `watch` / `test` / `test:e2e` / `package`(= `uex package`)。

`<目录名>` 写 `.` 可在当前目录就地初始化(当前目录已是扩展目录时避免多套一层);目录**非空**时需追加 `--force`——只覆盖脚手架自己生成的文件,外来文件永不删除。

## 第 4 步:实现

动手前先把参考示例的 `package.json` 与 `src/extension.ts` 打开对照着写(示例仓库先 pull 到最新);概念性问题读安装目录文档;API 是否存在、签名与语义以项目里 `node_modules/@universe-editor/extension-api/dist/*.d.ts`(带 JSDoc)为最终裁决,拿不准就先查再写。**红线自查清单**(违反任意一条,扩展会静默不加载或打包丢文件):

- `engines.universe` 必须是合法普通区间(脚手架已写好,如 `">=0.13.0 <1.0.0"`),不要改成 `||` 或连字符区间——这类语法宿主 fail-closed 拒载。
- `package.json` 的 `files` 是**白名单**:dist、图标、NLS 文件(`package.nls*.json`)等运行需要的文件都必须列入,漏列 = 打包丢失。
- import 一律 `@universe-editor/extension-api`,**没有** `vscode` 模块。
- 全 ESM(`"type": "module"`),产物由 esbuild 打包。
- `capabilities.untrustedWorkspaces`:脚手架已声明 `true`(模板只做 helloWorld/只读预览)。一旦你的扩展要运行工作区代码、跑构建、发网络请求,必须显式改成 `{ "supported": false, "description": "…" }`(或 `"supported": "limited"` 自行降级)——有 `main` 且不声明,在未受信任的工作区里**静默不激活**(形态与判断标准见安装目录文档 `extension-anatomy.md` 的 capabilities 节)。

实现过程中可随时 `npm run build` + `npx uex dev` 拉起「扩展开发宿主」窗口自测(它会自动定位本机安装的编辑器;失败时按提示设 `UNIVERSE_EDITOR_PATH`)。把纯逻辑抽离成独立模块(照模板 `hello.ts` 模式,与宿主 API 解耦),可单测的顺手在 `src/__tests__/` 补用例——宿主 API 用 `vi.mock('@universe-editor/extension-api')` 假掉,模板 `extension.test.ts` 是现成范例——跑 `npm test` 验证。

## 第 5 步:测试(单测 + e2e)

脚手架已自带两条测试链路(依赖、配置、fixture 全部就位),**不需要再手工搭建**:

**单测**:`npm test` 跑 `src/__tests__/` 下的 vitest 用例(node 环境,配置排除 `e2e/`,见 `vitest.config.ts`)。宿主 API 在测试里用 `vi.mock('@universe-editor/extension-api')` 假掉(模板 `src/__tests__/extension.test.ts` 是现成范例),不用起编辑器。核心逻辑抽离成独立模块(照模板 `hello.ts` 模式)后即可直接单测。

**e2e**:harness 冷启动真实编辑器、经 `window.__E2E__` 探针断言,**不需要下载浏览器**。脚手架自带 `e2e/playwright.config.ts`、`e2e/fixtures/app.mjs`(把本扩展目录 junction 进隔离的用户扩展目录,冷启动真实编辑器、只加载本扩展,等价 VSCode 的 `--extension-development-path`)、示例 spec(`basic` 模板为 `e2e/specs/command.spec.ts`)。你要做的:

1. 把 `e2e/specs/` 下的示例 spec 替换/扩充为第 2 步确认的场景清单——**每条已确认的需求至少对应一条用例**。断言模式照抄示例 spec:先 `expect.poll` 轮询 `window.__E2E__!.hasCommand('<扩展id>.<命令>')` 等命令注册(留出冷启动窗口,首次执行命令才会触发 `onCommand:` 激活),再 `runCommand` 执行、经探针断言效果(输出通道内容 / ContextKey / 编辑器状态),不要断言编辑器内部 DOM。
2. 跑 `npm run test:e2e`——自动先 build 再起 Playwright(`scripts/e2e.mjs` 已处理 agent shell 注入的 `ELECTRON_RUN_AS_NODE`,直接用 npm script 即可)。编辑器二进制自动探测本机安装,否则设 `UNIVERSE_EDITOR_BIN` 指向编辑器可执行文件;e2e 使用独立的 userData,不会与用户正开着的编辑器互相干扰。

探针 API(`hasCommand` / `runCommand` / `getOutputChannelContent` / `getContextKey` / `openFileUri` 等)来自 `@universe-editor/e2e-contract`;更多真实用法参考示例仓库各 `samples/<name>/e2e/*.spec.ts`——同一套 harness,每个示例都有一条可运行的 e2e。

单测与 e2e 全部通过后才进入验收。

## 第 6 步:人肉验收(门 3)

`npx uex dev` 拉起扩展开发宿主,请用户亲手把核心流程走一遍;按反馈修复迭代,直至用户确认满意。

## 第 7 步:发布(可选,单独确认)

仅当用户在门 1 表达过发布意图且此刻明确同意:

1. 前提:publisher 已在扩展市场注册并通过管理员审批(未注册则指引用户走市场注册页)。
2. `npx uex login`(用户自己粘贴 token,你不要经手 token 内容)。
3. `npm run package` 产出 `.vsix`,列出 `uex ls` 内容请用户过目。
4. 用户明确说"发布"后才执行 `npx uex publish`。

## 常见坑速查

- 扩展装了却不出现:最常见两类——① `engines.universe` 缺字段或用了 `||`/连字符区间被扫描器 fail-closed 拒载,或区间不满足当前编辑器版本被自动禁用(扩展视图标「已禁用」并显示原因);② 有 `main` 但未声明 `capabilities.untrustedWorkspaces`,在未受信任的工作区被信任门控拦下(症状:命令已注册但**永不执行**)。此外检查 `main` 指向的 `dist/extension.js` 是否已构建。
- 菜单命令 handler 收到什么参数(含 URI 序列化坑)?看安装目录文档 `contribution-points.md` 的 menus 节——每个菜单位置的参数结构有总表。
- 打包后功能缺失/文案不本地化:`files` 白名单漏了资源或 `package.nls*.json`。
- 任何交互式 CLI(会等 stdin 的)在 agent 环境都会挂:一律用全旗标非交互形式。
- e2e 里断言 UI 优先走探针与 `expect.poll`,不要断言编辑器内部 DOM 结构。
