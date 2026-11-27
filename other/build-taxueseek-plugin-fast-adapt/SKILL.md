---
name: dsh-plugin-build
description: 从零造一个可运行的 DSH 插件，或给刚写完的插件过体检门。scaffold 一条命令出五形态（tool/hook/service/config/llm-adapter）完整入口、cordis.patch.yml 挂载层、命名投影与 README，生成即验证（内存冒烟加真基类装载）；quick-smoke 秒验模块加载、apply 契约与工具注册，按真 Cordis 契约拦未声明 inject 的访问；write-gate 出出生证，硬门禁自动判、软指标透传待裁量。触发词：创建 DSH 插件、写 DSH 插件、插件脚手架、插件模板、从零做插件、五形态、命名投影、挂载层、插件出生证、write-gate、插件冒烟测试、装完不生效先验一遍。
---

# 造插件车道

两件事：没有插件时造一个能跑的起点；写完之后过一道体检门，别带着契约错误去装。以下命令都相对工具根目录执行，工具根即本文件真实路径往上两级、含 `scripts/` 的那一层。脚本用自身文件的绝对路径定位，不必先 cd，从任何目录直接 `node <工具根>/scripts/<脚本>.mjs` 同样可行。本目录常以软链别名加载，shell 的 `cd ../..` 会按软链走错地方，确实要 cd 时用 `cd "$(realpath <本文件所在目录>)/../.."`。

## 一条命令生成可运行插件

```sh
node scripts/scaffold.mjs <namespace>/<name> --form tool|hook|service|config|llm-adapter [--out <目录>] [--harness <版本>] [--no-smoke]
```

它只做确定性的事，不碰裁量：

- **五件套生成**：`package.json`（免构建纯 ESM 不变量：`type: module`、main 与 exports 双指 `lib/index.js`、files 含挂载层）、按形态的完整入口实现（tool 用 raw JSON Schema 注册、hook 走 waterfall 并显式 `next()`、service 继承宿主 Service 并注册服务名、config 导出真 Schemastery Schema、llm-adapter 继承宿主 LlmAdapter 并注册路由；入口里的能力是能跑通的起点实现，换成你的即可）、`cordis.patch.yml` 最小挂载条目（没有它装了不生效，`env-doctor` 的 activation 查的就是这层）、`dsh-plugin.naming.json`、README 加 `.gitignore`
- **命名投影**：loader id、service、tool、command、skill、event、route 全部按上游 naming-conventions 的 collision-resistant 规则从 coordinate 推导，生成物已过上游 validate-names 的 `--strict` 校验（0 错误 0 警告）
- **当场验证（两层，缺一层报一层）**：tool/hook 走零依赖内存冒烟；五形态都走真基类装载，本机装了宿主时用真实 `@deepseek-ai/*` 基类 import 入口，验基类 API 用对没对（Service 继承与 `super(ctx, name)`、Schema 真校验、LlmAdapter 继承与路由注册）。本机没装宿主时如实跳过，不伪造通过

目标目录非空即拒绝（不动用户文件）；非法 coordinate 在写盘前拒绝。生成物保证「能装载、契约成立、能力可跑」，完整契约仍以真源文档为准：

| 需求 | 去 where |
| --- | --- |
| 五形态完整契约（execute 义务、waterfall 语义、Schema 规则、协议义务清单） | [原仓库 plugin-write skill](https://github.com/oh-my-dsh/dsh-plugin-upgrade-skill/tree/main/skills/plugin-write) 的五份 form reference |
| 公共命名规范与注册表冲突检查 | plugin-write 的 naming-conventions 与 registry-check reference（validate-names、query-registry 两脚本） |
| Cordis 教程、API、cookbook | 官方仓库 `deepseek-harness/docs/` 的 cordis-tutorial、cordis-api、cookbook |

## 秒验：改完立刻知道还能不能装

```sh
node scripts/quick-smoke.mjs <插件目录>
```

纯内存模拟 Cordis 上下文，动态载入插件入口，毫秒到秒级验证：模块能加载、`apply` 契约能执行、工具能注册。改完代码先跑它，挂了立刻回改，不用等真宿主冷启动。入口按 Node 语义解析（`exports['.']` 优先于 `main`，两者都没有才退 `lib/index.js`），与 `env-doctor` 的产物判定共用同一份实现；只有 `exports` 的包不会再被误报「入口不存在」。

**边界**：冒烟通过不等于宿主兼容。Mock 只覆盖 logger/tools/effect/on 等常见面；输出里的 `mockFallbacks` 列出了插件摸到但 Mock 没提供的属性（含内建 mixin 里 Mock 未全真实现的面），这个列表越长，本次结果可信度越低。

**契约校验（2026-10-25 实测复盘）**：此前 Mock 对任何未知属性都返回兜底代理，于是插件访问**未声明 `inject`** 的宿主服务（真 Cordis 直接抛 `cannot get property "X" without inject`，装载即崩）时冒烟静默通过。现在按真契约判：

- 声明了 `inject` 的服务 Mock 没提供，兜底并披露（Mock 缺口，不是插件的错）
- 未声明的非内建属性，抛 `inject_contract` 阶段错（与真宿主同形）

判据取自 `cordis/lib/index.js` 的 ReflectService 构造与 LoggerService 装配，不是臆造。真冷启动验证用原仓库 plugin-upgrade 的 `verify-runtime.mjs`，或 `run.mjs --real-smoke`。

## 体检门：出生证

```sh
node scripts/write-gate.mjs <插件目录>
```

一条命令过冒烟、启用就绪、四维体检、官方指南核查，出一份出生证报告。也可拆开单跑：`quick-smoke` 秒验 → `env-doctor` 看启用就绪 → `plugin-audit` 体检 → `code-scan` 对目标版本核查。

**判定分层**：硬门禁只有三条，fail 即退出码 1——入口产物存在、冒烟通过、对官方指南 critical 零命中。其余全部只透传不拍板：audit 四维分数与 MEDIUM 清单、scan 的 high/medium 命中（带 evidence）、mockFallbacks、尚未挂载 profile 的事实，全部进 discretion 区标「人工裁量」。因为 plugin-audit 的诚实保留信号（如宿主契约下同步是唯一合法写法）和 env-doctor 的未决语义 WARN，替用户判「合格」就是把裁量题伪装成判定题。

指南自动发现：显式 `--guide` 优先，否则用本机宿主版本查 guide-sync 缓存（零网络），都没有就诚实跳过并给补法。新插件核查面是全部历史走廊（localVersion 为 null 时窗口放行全部指南）：新代码不该 import 任何已被移除的包，不管哪个版本移除的。刚 scaffold 完加 `--skip-smoke` 免重复冒烟。

## 边界

- 生成器不动用户已有文件；目标目录非空直接拒绝
- 不自动改 `package.json` 的 peer 范围，`plugin-audit --peer-patch` 只打印建议
- 五形态的完整协议义务以真源文档为准，脚手架只保证「能装载、契约成立、能力可跑」
