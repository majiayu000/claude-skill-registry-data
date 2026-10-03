---
name: minecraft-modder-neoforge
description: Minecraft NeoForge 模组开发参考。创建新模组、添加物品/方块/实体、编写配方（RecipeProvider）、注册（DeferredRegister）、数据生成（datagen）、Mixin、Access Transformer、单元测试或排查模组崩溃时加载；默认 NeoForge 26.1.2 / Minecraft 26.1.2，细节按主题查阅 reference/ 子文档。
---

# Minecraft Modder（NeoForge）

## 绝对原则：先思考，再查文档，最后写代码

1. **思考前置**：需求有歧义时必须列出多种理解让用户选择，禁止静默选择；存在更简单实现时必须主动提出（用户要一个物品，就不搭整套抽象注册系统）。
2. **文档优先**：禁止凭空猜测任何 API、类名、方法签名或配置格式。不熟悉的 API 必须查阅官方文档：
   - NeoForge 文档：https://docs.neoforged.net/
   - 迁移 Primers：https://docs.neoforged.net/primer/docs/ ；中文翻译：https://gu-zt.github.io/Porting-Primers/
   - Mixin（Fabric 社区维护，适用于所有加载器）：https://wiki.fabricmc.net/zh_cn:tutorial:mixin_introduction ；示例：https://wiki.fabricmc.net/zh_cn:tutorial:mixin_examples ；机制 Wiki：https://github.com/SpongePowered/Mixin/wiki

   上述链接页面已完整镜像到 [reference/external/](reference/external/)（2026-09-20 抓取，各文件头部含许可署名；权威内容以原链接为准，发现过期时重新抓取更新对应镜像文件）：[neoforged-docs-home.md](reference/external/neoforged-docs-home.md)、[neoforged-primers-index.md](reference/external/neoforged-primers-index.md)、[porting-primers-zh-index.md](reference/external/porting-primers-zh-index.md)、[mixin-introduction-zh.md](reference/external/mixin-introduction-zh.md)、[mixin-examples-zh.md](reference/external/mixin-examples-zh.md)、[mixin-wiki-home.md](reference/external/mixin-wiki-home.md)。优先读本地镜像，镜像不含所需信息时再访问原链接及其子页面。26.1 关键变更提示：`ResourceLocation` 更名 `Identifier`（1.21.11）、Java 25 与反混淆（26.1）、验证大修、新标签提供者、数据组件初始化器、模型重做（1.21.5）、渲染重写（1.21.11）等；完整主题地图与类/方法索引见 porting-primers-zh-index.md。
3. **版本信息禁止依赖训练数据**：最新版本号、版本兼容性、API 变更、迁移步骤一律查官方文档或在线搜索确认。文档查不到就如实告知用户，并提供最接近的可行方案。

## 核心原则

- **默认版本**：NeoForge 26.1.2 + Minecraft 26.1.2，除非用户明确指定其他加载器或版本。
- **分层组织**：注册、事件监听、网络包、数据生成分开处理。
- **工具链**：优先 NeoForge 官方推荐的 ModDevGradle（MDG）。
- **代码规范**：包含必要 import，禁止内联全限定类名；关键方法添加中文注释与 Javadoc；全程用简体中文与用户交流。
- **简洁优先**：只写需求要求的代码。禁止为单个物品引入抽象工厂、建造者模式或未要求的配置项、可扩展接口；禁止处理不可能发生的错误场景。写完自问「资深模组开发者会觉得这是过度设计吗」，是则简化。
- **回复收尾**：回复最后建议下一步操作或需要补充的资源。
- **外科手术式修改**：改动已有模组时，diff 每一行都必须可追溯到用户的具体请求；匹配既有代码风格；不顺带重构无 bug 代码；清理因本次改动产生的孤立 import/变量/方法，但禁止删除与本任务无关的既有死代码。

## reference/ 导航

| 文档 | 主题 |
| --- | --- |
| [project-setup.md](reference/project-setup.md) | 项目结构、构建/运行命令、模板仓库、许可证约定、资源文件要求、工具链配置 |
| [registration.md](reference/registration.md) | DeferredRegister 注册体系、`Item.Properties().setId(...)` 强制要求 |
| [datagen.md](reference/datagen.md) | Datagen-First 原则、GatherDataEvent.Client 入口、各 Provider 用法 |
| [mixin-at.md](reference/mixin-at.md) | Mixin 使用条件与声明、Access Transformer 优先于 @Accessor/@Invoker |
| [testing.md](reference/testing.md) | JUnit 单元测试、testframework 服务端测试、GameTest |
| [anvillib.md](reference/anvillib.md) | AnvilLib 模块清单、按需引入坐标、版本查询 |
| [source-reading.md](reference/source-reading.md) | 参考开源模组原则、sources.jar / 反编译查阅依赖源码 |
| [tasks.md](reference/tasks.md) | 常见任务完成标准（建模组、加物品、配方、实体、配置、调试崩溃、写测试） |
| [external/](reference/external/) | 外部文档完整镜像：官方文档站、Primers 索引（中英）、Mixin 教程与 Wiki、AnvilLib 官网与 Maven 清单 |

## 快速避坑

- **注册物品必须显式 setId**：NeoForge 26.1.2 起 `new Item.Properties().setId(ResourceKey.create(Registries.ITEM, id))`，详见 [registration.md](reference/registration.md)。
- **可生成资源一律走 datagen**：模型、语言、配方、战利品表、方块状态、标签禁止手写 JSON；禁止因 datagen API 不熟回退手写，详见 [datagen.md](reference/datagen.md)。
- **Mixin 必须声明**：使用 Mixin 必须在 `neoforge.mods.toml` 声明 `[[mixins]] config = "${mod_id}.mixins.json"`，否则不会被加载。
- **私有成员访问优先 AT**：禁止优先使用 `@Accessor` / `@Invoker`，详见 [mixin-at.md](reference/mixin-at.md)。
- **新增物品/方块同步检查资源**：`neoforge.mods.toml` 声明、纹理 PNG、模型、语言文件缺一不可。
- **依赖源码不入库**：解压到项目 `reference/` 的他人源码必须加入 `.gitignore`，详见 [source-reading.md](reference/source-reading.md)。

## Checklist

- [ ] 需求歧义是否已向用户澄清，而非静默选择？
- [ ] 涉及的 API、版本信息是否查过官方文档，而非凭训练记忆？
- [ ] 版本是否为 NeoForge 26.1.2 / MC 26.1.2（或用户明确指定的版本）？
- [ ] 注册物品是否通过 `Item.Properties().setId(...)` 显式设置 id？
- [ ] 可自动生成的资源是否全部走 datagen，未手写 JSON？
- [ ] 改动是否外科手术式，diff 每行可追溯到用户请求？
- [ ] 代码是否无过度设计、import 完整、注释为中文？
- [ ] 新增内容是否同步提醒 `neoforge.mods.toml`、纹理、语言文件？
