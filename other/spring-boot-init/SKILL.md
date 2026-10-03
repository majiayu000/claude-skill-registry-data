---
name: spring-boot-init
description: >-
  Spring Boot / Maven 项目初始化（脚手架）助手——用内置 Maven 父子标准模板，经 scripts/init.mjs
  一条命令生成项目骨架（复制模板 / 替换占位符 / 挪包目录 / 模块塑形一体），零网络、完全本地自包含；
  禁止从零手写 pom.xml 与主启动类，也不依赖在线初始化器。在以下场景使用：用户要新建 / 初始化 / 搭建
  Spring Boot、Maven 项目；用户说"建个 Spring Boot 项目 / 搭脚手架 / 建父子工程 / 多模块 /
  微服务骨架 / init 一个 Java 项目"；或 agent 正准备从零手写 pom、手动创建目录结构与主启动类时。
  默认产物：根 pom（packaging=pom + <modules>）+ 子模块，单模块（只留一个 app 子模块）与多模块
  一套模板覆盖；生成前引导式问询四检查点，禁止静默默认。项目已存在后的业务编码、ORM、认证鉴权、
  单元测试不适用——由 spring-boot-dev / mybatis-plus-dev / sa-token-dev / java-unit-test 承接。
agent_created: true
version: 1.5.1
slug: spring-boot-init
displayName: Spring Boot 项目初始化
---

# Spring Boot 项目初始化（脚手架）

面向"新建 Java 项目"场景的**初始化助手**。核心理念：**不从零手写脚手架——`scripts/init.mjs` 从内置 Maven 父子标准模板一键生成。** 零网络依赖，完全本地自包含。补上 `spring-boot-dev`（只管写代码、不管建项目）的空白。

- **默认产物**：根 pom（`packaging=pom` + `<modules>`）+ 子模块。**单模块项目 = 只保留一个 app 子模块**（`--single`）；多模块 = 库模块 + 可执行模块（`--core` / `--app` 命名）。一套模板覆盖全部场景，不分叉。
- **模板** `assets/maven-multimodule/`：常用插件齐备——enforcer（环境门禁）、flatten（`${revision}` CI-friendly 版本）、jacoco（覆盖率）、spotless（格式化）默认激活；failsafe / source / javadoc / deploy 已管理、按需启用。版本全部收敛在根 pom。lombok 为根公共依赖（全局生效）；hutool-bom 在根 import（core / json / http 等按模块按需引，`references/02-dependencies.md`）；内置阿里云镜像加速（用户级 settings.xml 镜像优先生效）。
- **初始依赖**：按项目类型问询决定（`references/02-dependencies.md`），不默认堆。

## 第 0 步：现状探测（收到任务先做）

| 探测项 | 方法 | 判定 |
|---|---|---|
| 是否已有项目 | 当前目录是否已有 `pom.xml` / `build.gradle` | 已有 Maven 工程 → **本技能不适用**（加模块 / 加依赖直接参照工程内现有模块的结构即可）；空目录 → 整体初始化 |
| 子模块划分 | 预判（单服务 → 单模块形态；分层 / 多可部署单元 → 多模块），最终以 C1 问询为准 | 决定 `<modules>` 数量与命名（不预设 common/web 等固定划分） |
| Boot / JDK 版本 | 用户指定；否则按 C2 表默认 | 作为 init.mjs 的 `--boot` / `--jdk` 参数 |

## 何时使用本技能

| 信号 | 判定 |
|------|------|
| 用户说"新建 / 初始化 / 搭建 Spring Boot、Maven 项目""建父子工程""多模块""微服务骨架""init 一个 Java 项目" | 激活 |
| agent 正准备从零手写 `pom.xml` / 目录结构 / 主启动类 | 激活（改为 init.mjs 生成） |
| 要给新项目定初始依赖 | 激活 → `references/02-dependencies.md` |
| 项目已存在，要写 Controller / Service / 事务 / 配置 | **不适用** → spring-boot-dev |
| ORM CRUD / Mapper / 分页 | **不适用** → mybatis-plus-dev |
| 认证 / 鉴权 / token | **不适用** → sa-token-dev |
| 纯 Java 语言层（判空 / 集合 / 并发） | **不适用** → java-coding-guide-pro |
| 单元测试 | **不适用** → java-unit-test |
| 给已有工程加子模块 / 加依赖 | **不适用** → 参照工程内现有模块结构即可，无需本技能 |
| Gradle / 其他构建工具 | 首版不覆盖 → 告知用户本技能只出 Maven 骨架 |

> **检查点**：判定为「不适用」→ 告知用户该任务属哪个技能，建议切换。

## 生成流程（唯一路径：init.mjs 生成）

1. **第 0 步探测**：空目录？单模块还是多模块？Boot / JDK 版本？
2. **问询（必做，引导式）**：按「决策检查点」**一轮问完** C1~C4，每项附默认推荐；用户逐项答复或一句"都按推荐"后才进入下一步。**禁止不问就静默采用默认。**
3. **生成骨架**：`node <技能目录>/scripts/init.mjs <目标目录> --group <g> --artifact <a> --boot <b> --jdk <j> [--core 名 --app 名 | --single]`——复制模板、替换占位符、挪包目录、模块塑形一步完成（参数与内部步骤见 `references/01-template-usage.md`）。
4. **初始依赖**：按 `references/02-dependencies.md` 组合表往对应模块加；C4 勾选的可选插件（failsafe / source / javadoc）在模块内裸声明。
5. **自检交付**：`node <技能目录>/scripts/self-check.mjs <项目目录> --validate`（六查，明细见「自检与交付」；退出码 0 才算完成）。

## 决策检查点（生成前必须问询——引导式，禁止静默默认）

**一轮问完**（示例话术，按上下文裁剪；用户逐项答复或一句"都按推荐"即完成）：

> 初始化 Spring Boot 项目前确认 4 件事：
> ① 工程坐标 + 模块划分：包名和项目名（如 org.acme.order / order-service）？单模块（只一个 app）还是多模块（core + app…各叫什么）？
> ② 版本：Boot 3.5.x + JDK 21（推荐）/ 存量 2.7.x / 4.x（JDK 25 优先），选哪个？
> ③ 初始依赖：什么类型的服务？（Web API / 全栈 / 定时批处理 / 消息 / 数据访问）
> ④ 可选插件：要集成测试（failsafe）或发布库模块（source / javadoc）吗？默认都不启用

| # | 必问 | 选项差异 | 默认推荐（用户明示"按推荐"才用） |
|---|------|---------|---------|
| C1 | 工程坐标 + 模块划分：包名（groupId）/ 项目名（artifactId）？单模块还是多模块？各模块叫什么？ | **单模块**：父子结构只留 1 个 app 子模块<br>**多模块**：库模块 + 可执行模块按业务命名 | 项目名可取目录名；**包名无安全默认**——按组织域名反转 + 项目名（如 `org.acme.order`）给建议、用户拍板；明显单服务 → 单模块形态 |
| C2 | Boot / JDK？ | 见下表 | 3.5.x 最新 + JDK 21 |
| C3 | 项目类型（初始依赖）？ | 按 `references/02-dependencies.md` 类型组合表 | 空骨架（web + test 基线） |
| C4 | 可选构建插件？ | failsafe（集成测试）/ source + javadoc（发布库模块），模块内裸声明即启用 | 都不启用 |

**Boot ↔ JDK 兼容表**（口径与 spring-boot-dev 一致）：

| Boot 线 | JDK | 命名空间 | 定位 |
|---|---|---|---|
| 2.7.x | 8 / 11 | `javax.*` | 仅存量维护，新项目不选 |
| **3.5.x** | 17 / 21 | `jakarta.*` | **默认推荐**（3.x 末线） |
| 4.x | 25 优先（21 可，最低 17） | `jakarta.*` | 已 GA，需用户明示才用 |

## 核心强约束（Agent 必须遵守）

1. **一律经 `scripts/init.mjs` 生成**：禁止从零手写 `pom.xml` / 主类 / 目录结构，也不得手跑 sed / mv 复刻脚本步骤。
2. **聚合规则**：根 pom 必须 `packaging=pom` + `<modules>` 列全子模块；子模块 `<parent>` 指根（GAV 三行一致）；`<modules>` 与实际目录名一一对应。
3. **版本收敛**：插件版本只在根 `pluginManagement`，依赖版本只在根 `dependencyManagement`（spring-boot-dependencies BOM import）；工程版本统一 `${revision}`（flatten 在 install/deploy 时解析，发布/改版用 `-Drevision=1.0.0` 一次覆盖全工程）；子模块一律不带版本。
4. **占位符零残留**：`init.mjs` 生成时终检 + `self-check.mjs` 复核（含 `com.example` 包路径），任一报残留即失败。
5. **repackage 只归可执行模块**：`spring-boot-maven-plugin` 只在 app 模块启用；库模块保持普通 jar。
6. **依赖必须真实**：starter 坐标只从 `references/02-dependencies.md` 组合表取；表外依赖先查 Maven Central 确认存在，禁止凭记忆拼 `spring-boot-starter-xxx`。
7. **JDK ↔ Boot 匹配**：按 C2 兼容表选，禁止越线组合（如 Boot 4.x 配 JDK 11）。

## 自检与交付

```bash
node <技能目录>/scripts/self-check.mjs <项目目录> --validate
```

脚本六查：①`{{...}}` 占位符零残留；②`com.example` 包路径零残留；③模块目录与根 `<modules>` 一一对应（防孤儿 / 缺失）；④可执行模块存在且含主类（`static void main`）；⑤package 声明与目录路径一致；⑥`mvn -q validate`（Windows 下自动调 `mvn.cmd`）。零依赖、跨平台，退出码 0 = 通过。

- 通过后交付：**只产出骨架**；业务编码指引用户转 `spring-boot-dev`，需要项目说明书（AGENTS.md）转 `repo-init`。
