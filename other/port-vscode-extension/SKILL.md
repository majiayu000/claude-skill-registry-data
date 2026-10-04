---
name: port-vscode-extension
description: 把现有 VSCode 插件移植为 Universe Editor 扩展。当用户给出某 VSCode 插件的仓库/名称希望在本编辑器实现同样功能,或询问某 VSCode 插件能否在 Universe Editor 使用时使用。先做 API 兼容性四档评估与 license 检查并让用户确认,再接 new-extension 流程完成搭建、e2e 与发布。
disable-model-invocation: true
---

# 移植 VSCode 插件到 Universe Editor

你负责把一个现有的 VSCode 插件移植成 Universe Editor 扩展。与从零创建的最大差别是:**动工之前必须完成可行性评估并让用户确认**——Universe Editor 的扩展 API 与 VSCode 高度同构但不是全集,不评估就动工很可能做到一半发现核心能力缺失。

本 skill 只覆盖「评估 + 移植改写」这段;环境检测、脚手架、e2e、验收、发布等通用流程**复用同目录旁 `../new-extension/SKILL.md`**,先把它读了,其全局规则(三道门、publish 永不自动、不硬造 API、密钥红线)在本流程同样生效。权威资料的三层分工(项目内 `.d.ts` = API 最终裁决 / 示例仓库 / 安装目录文档)也见该文件「权威资料在哪」一节,其中**`migration-from-vscode.md` 是本流程的核心参考**,评估前必读。评估前还要按该文件「示例仓库:克隆与自动更新」准备好本地示例副本(每次参考前先 pull):示例仓库根 `README.md` 带一份**与官方 vscode-extension-samples 的逐条能力对照表(✅/⚠️/❌/➖)**,是四档评估的快速定位入口。

## 第 1 步:需求确认(门 1)

一次性问齐:

1. 参考插件的**仓库地址**(只有市场名/ID 时,先帮用户搜出仓库;拿不到源码就无法移植,不要试图逆向 .vsix)。
2. 移植**全部功能**还是只要其中某几个能力?(很多插件 80% 的价值在 20% 的功能,缩小范围能绕开 API 缺口)
3. 自用还是发布到市场?

## 第 2 步:获取与分析源码

```bash
git clone --depth 1 <仓库地址> <临时目录>
```

然后产出一份**API 使用清单**(源码大时建议把这一步委派给子代理,只带回清单,不要把整仓源码拉进上下文):

- `package.json`:`contributes` 全部贡献点、`activationEvents`、`engines.vscode`、`main` 形态(CJS/ESM)、依赖里的原生模块。
- 源码:扫描 `vscode.` 命名空间调用与 `import ... from 'vscode'` 的具名引用,按 namespace(commands / window / workspace / languages / scm / env / tasks / debug / notebooks / authentication / …)归类列出每个用到的 API。

## 第 3 步:license 检查

读源仓库的 LICENSE:

- 宽松许可(MIT / Apache-2.0 / BSD 等):可移植,**必须保留 attribution**——移植产物的 README 里写明来源仓库、原作者与许可证。
- GPL / LGPL / 无 LICENSE:明确向用户说明约束(衍生作品许可传染 / 无授权不可复制代码),让用户决定是重写实现还是放弃。

## 第 4 步:可行性四档评估(门 2)

拿着 API 使用清单定档,按「先粗后细」两轮:

1. **粗定位**:用示例仓库根 `README.md` 的官方示例对照表,快速看清该插件所属功能域(语言特性 / 视图 / SCM / 调试…)在 Universe Editor 的整体支持度,提前发现整域缺失。
2. **逐条定档**:对照 `migration-from-vscode.md` 的 namespace 对照表(以文档为准,不要背清单)给每个 API 定档;文档拿不准的 API,动工起骨架 `npm install` 后以 `node_modules/@universe-editor/extension-api/dist/*.d.ts` 为最终裁决,发现与文档不一致时以 `.d.ts` 为准并回报用户。

四档定义:

| 档 | 含义 |
|---|---|
| ✅ 直接移植 | 同名同义,机械替换即可 |
| ⚠️ 语义差异 | 存在但行为不同(如部分 API 返回 Promise 化),需改调用方式 |
| 🔧 需降级替代 | 无直接对应,但可用别的 API 组合近似实现 |
| ❌ 缺失 | 整个能力域不存在(典型:`tasks`、`debug`、`notebooks`、`authentication`、`ExtensionContext.secrets`),做不了 |

另外核对 `activationEvents`:支持 `*`、`onStartupFinished`、`onCommand:`、`onLanguage:`、`onView:`、`onCustomEditor:`;**没有** `workspaceContains:`、`onFileSystem:`、`onUri:`(通常可降级为 `onStartupFinished` + 自查工作区)。

把评估结果整理成报告给用户:每个功能点 → 涉及 API → 档位 → 降级方案(若有)。**核心功能踩到 ❌ 时停下**,给用户三选:砍掉该功能 / 换实现路径 / 放弃移植;并**询问是否生成缺失功能报告**(见下节)。用户确认范围与降级方案后才动工。

### 缺失功能报告(gap report)

核心功能踩到 ❌ 停下时(含移植执行中新发现的),**询问用户是否生成一份缺失功能报告**,供转交本仓库维护人员补全缺失的 API 能力;报告与三选互不冲突,用户走哪条路都可生成、也可拒绝。同意后写 markdown 到**当前工作区根目录** `gap-report-<源插件名>.md`(评估阶段扩展 id 未定,用源插件名/仓库名),对话中只给路径与摘要,不重复全文。结构:

1. **源插件**:仓库地址、license、移植范围(门 1/门 2 确认的功能清单)。
2. **缺失 API 清单**(核心):每个缺失 API 一条——`namespace.API` 名称与期望语义(按 VSCode 文档与源插件用法推断)、源插件调用点摘录(文件:行 + 最小代码片段)、受影响功能点与档位(❌)、已探索的降级路径与失败原因(若有)。
3. **实现建议**:建议的新 API 形态(签名草案,对齐 `@universe-editor/extension-api` 现有风格)、VSCode 仓库对应实现的参考位置(microsoft/vscode 文件路径)、Universe Editor 现有近似能力(据 `migration-from-vscode.md` / `.d.ts` / 示例仓库)。
4. **评估依据**:`migration-from-vscode.md` 对照结论、`.d.ts` 裁决结果、评估所用示例仓库与文档版本,便于维护人员复现判断。

代码摘录仅限说明用途的最小范围;报告不含任何密钥/敏感信息。

## 第 5 步:移植执行

先按 `new-extension` 第 3 步用脚手架起骨架(拿到正确的构建配置与 manifest 基线),再把源插件代码迁入 `src/`。迁每块功能前,先看示例仓库同能力示例的地道写法(索引见 `new-extension`「示例仓库」一节,参考前先 pull),不要 1:1 平移 VSCode 的代码结构。机械替换表:

| VSCode | Universe Editor |
|---|---|
| `import * as vscode from 'vscode'` / 具名 import | `@universe-editor/extension-api`(具名 import) |
| devDep `@types/vscode` | 删除,类型随 `@universe-editor/extension-api` |
| `engines.vscode` | `engines.universe`(用脚手架生成的区间) |
| 产物 CommonJS | ESM(`"type": "module"`,esbuild 打包) |
| `.vscodeignore`(黑名单) | `package.json` 的 `files`(白名单) |
| `vsce package / publish / login` | `uex package / publish / login` |
| `contributes.*` | 同名保留,仅保留评估通过的贡献点 |

⚠️ 档位为「语义差异」的调用点逐个核对文档改写,不要指望编译器全部报出来(Promise 化的 API 不 await 会静默拿到 Promise 对象)。webview 类插件的本地资源加载务必读 `webview-guide.md`(`asWebviewUri` + `localResourceRoots` 必须覆盖资源目录)。

源插件用 `import * as vscode from 'vscode'` 时,不要每次手写兼容层——**从本 skill 自带的 `references/vscode-compat-template.js` 起步**(Position/Range/Selection、wrapDoc/wrapEditor、compat_window/workspace/languages、同步配置缓存等都已备好),复制到 `src/` 后按文件头与 `TODO(port):` 标记填充目标扩展专属内容。

移植中随时 `npm run build` 收敛类型错误;跑通后按 **`new-extension` 第 5~7 步**继续:e2e(场景 = 门 2 确认的功能清单)、`uex dev` 人肉验收、可选发布。验收除 e2e 外,**必须翻 ext-host 日志找 `unhandled rejection`**(路径与排查见下方「宿主已知陷阱清单」)——测试全绿 ≠ 无运行时错误。

## 市场类目对照表

`package.json` 的 `categories` 是 VSCode 的市场类目清单(Programming Languages / Data Science / Debuggers …),**直接照抄会被 `uex package` 拒绝**——Universe 有自己固定的合法类目集合。允许清单在 `packages/extension-manifest/src/categories.ts`(`EXTENSION_CATEGORIES`,第 7~15 行),`uex` 发布校验在 `packages/uex/src/lib/manifestChecks.ts`(`checkManifestForPublish` 内 `isExtensionCategory`,第 100~108 行)。

合法类目(共 7 个):`Language Features` / `Content Tools` / `Data / Schema` / `SCM / Git` / `AI` / `Themes` / `Other`(兜底)。

| VSCode 类目 | 映射到 Universe 类目 |
|---|---|
| Programming Languages | Language Features |
| Formatters / Linters | Language Features |
| Snippets | Language Features |
| Language Packs | Other(本地化无对应域) |
| Data Science / Machine Learning | Data / Schema |
| Visualization | Content Tools |
| Notebooks | Other(notebooks 域缺失,先回门 2 评估) |
| SCM Providers | SCM / Git |
| Themes / Keymaps | Themes |
| Debuggers | Other(debug 域缺失,先回门 2 评估) |
| AI / Chat | AI |
| Extension Packs / Education / Azure / 其它 | Other |

归类规则:语言/格式化/补全类 → `Language Features`;数据与可视化 → `Data / Schema` / `Content Tools`;版本控制 → `SCM / Git`;外观定制 → `Themes`;AI 助手 → `AI`;拿不准或能力域缺失的 → `Other`。rainbow_csv 用 `Language Features` + `Data / Schema` 是合法组合的先例。

## 宿主已知陷阱清单

- **不要在 `activate()` 里 await 首文档 / `getActiveTextEditor()`**:renderer 把文档镜像推送排在 `activate()` 返回之后,等待即死锁。宿主已改进该场景:立即 resolve `undefined` 并打日志,且 `onDidOpenTextDocument` 会对已打开文档补发事件——拿到 `undefined` 时订阅 `onDidOpenTextDocument` / `onDidChangeActiveTextEditor` 再取即可,不必手写轮询样板。
- **e2e 断言语言别依赖 `getContextKey('editorLangId')`**:宿主已修复该 key 跟随语言变化,但状态栏文案断言仍是更直观、更稳的选择。
- **菜单命令参数是 JSON 序列化的 `UriComponents`**,用 `Uri.from(...)` 复活,别当 `URI` 实例直接读 `.fsPath`。
- **根 `"type": "module"` 时,CJS 子目录要放嵌套 `package.json`(`{"type":"commonjs"}`)**,否则 esbuild/node 按 ESM 解析 CJS 源码会静默错乱。
- **移植后检查 esbuild 配置的 entry 是否还指向脚手架的 `extension.ts`**:否则默默构建脚手架代码、产物无报错,只能靠 bundle 体积异常发现(目标代码根本没进产物)。
- **测试全绿 ≠ 无运行时错误**:验收必须翻 ext-host 日志找 `unhandled rejection`——`<userData>/logs/<sessionId>/extensionHost.log` 及 renderer 的 "Extension Host" 输出通道。
- **兼容层直接从本 skill 的 `references/vscode-compat-template.js` 起步**,别每次手写(第 5 步移植执行处已引用)。

## 常见坑速查

- 移植后扩展不激活:先查 `engines.universe` 合法性与 `activationEvents` 是否用了不支持的事件。
- 编译全绿但运行不对:多半是 ⚠️ 档 API 的 Promise 化语义没接住。
- 大插件不要整仓平移:按门 2 确认的功能范围只迁需要的模块,依赖越少坑越少。
- README 忘写 attribution:发布前自查,这是 license 合规要求不是可选项。
