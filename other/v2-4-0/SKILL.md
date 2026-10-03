---
name: mybatis-plus-dev
description: >-
  MyBatis-Plus 开发助手。在 Java / Spring Boot 项目中开发任何数据库
  增删改查（CRUD）、分页查询、条件查询、Mapper / DAO / Service 层、实体类与表映射、
  联表 / 复杂查询写 XML、事务相关功能时使用本技能——无论用户是否提到 MyBatis-Plus
  （MyBatis-Plus / MyBatis Plus / MP / baomidou / CRUD / pagination / ORM / DAO / entity mapping）。
  次级触发信号——代码或 pom 中出现：mybatis-plus-boot-starter、
  extends BaseMapper / IService / ServiceImpl、
  QueryWrapper / LambdaQueryWrapper / LambdaUpdateWrapper、
  @TableName / @TableId / @TableField / @TableLogic、
  MybatisPlusInterceptor / MetaObjectHandler、
  selectPage / saveBatch / IPage、logic-delete-field / mapper-locations / @DS；
  用户任务词或报错出现：分页失效 / total 为 0 / 返回全量、更新后字段没变 / 字段置 null 不生效、
  逻辑删除 / 软删除、批量插入 / 批量导入 / saveBatch 慢、乐观锁、创建时间自动填充、
  多租户 / 数据权限 / 分表 / 动态表名、雪花 ID / 主键策略、枚举存数据库、联表查询、
  事务不回滚、Invalid bound statement (not found)。
  依赖含 mybatis-plus-* 或代码出现上述令牌时必须使用；纯 MyBatis、无 ORM 或 ORM 未知，
  先询问用户是否引入 MyBatis-Plus 再开发。
  不适用于：已使用 JPA / Hibernate 的项目（不建议迁移）、表结构设计 / DDL、纯 SQL 性能调优
  （连接池 / 索引 / 慢查询属 DBA 层）。
agent_created: true
version: 2.4.0
last_verified: "2026-08-23"
slug: mybatis-plus-dev
displayName: MyBatis-Plus 开发助手
---

# MyBatis-Plus 开发助手

面向日常 Java 开发的 MyBatis-Plus 编码助手。**推荐 3.5.x 最新版（全线适用）**，3.4.x 大部分兼容（差异处已注明）。
采用**完全本地自包含**策略：所有知识沉淀于本地 `references/`，运行时不依赖任何外部文档站点。

## 版本与依赖（先判 SpringBoot 版本）

| SpringBoot | starter 坐标 |
|---|---|
| 2.x | `mybatis-plus-boot-starter` |
| 3.x | `mybatis-plus-spring-boot3-starter` |
| 4.x (^3.5.13) | `mybatis-plus-spring-boot4-starter` |

- **切勿**同时引入 `mybatis` / `mybatis-spring-boot-starter` / `mybatis-spring`，会与 MP 版本冲突。
- **分页必引** `mybatis-plus-jsqlparser`（自 v3.5.9 起 `PaginationInnerInterceptor` 已从核心拆分，单独成依赖；否则分页静默失效）。JDK8 项目用 `mybatis-plus-jsqlparser-4.9`。

## 第 0 步：依赖探测与激活分支（收到数据库访问类任务先做这一步）

任务涉及增删改查、分页、条件查询、Mapper/DAO/Service 层、实体映射、事务等编码——**即使用户没提 MyBatis-Plus**——先检索项目依赖（在 `pom.xml` / `build.gradle` 中搜 `mybatis-plus`、`mybatis`、`spring-boot-starter-data-jpa`、`hibernate`）：

| 探测结果 | 动作 |
|---|---|
| 依赖含 `mybatis-plus-*` | 直接激活本技能，走下方流程 |
| 纯 MyBatis 原生（无 MP） | 按「部分适用」规则（仅 `10-xml.md` + `11-transaction.md`），同时**询问**用户是否引入 MyBatis-Plus（单表 CRUD 免写 SQL，与现有 XML 共存） |
| 无任何 ORM | **主动询问**用户是否引入 MyBatis-Plus；同意 → 按「版本与依赖」表 + `references/01-start.md` 引入后继续；拒绝 → 退出本技能，不再打扰 |
| 已使用 JPA / Hibernate | 告知不适用并退出，**不建议迁移** |

## 何时使用本技能

| 信号 | 判定 |
|------|------|
| Java/SpringBoot 项目中的 CRUD/分页/条件查询/Mapper 层/实体映射/事务任务（未指明框架） | 激活，先执行「第 0 步」依赖探测 |
| 依赖含 `mybatis-plus-*` / 代码 `extends BaseMapper` / `extends ServiceImpl` / 使用 Wrapper / `IService` / `saveBatch` / `selectPage` | 激活 |
| 提到 `@TableLogic` / `@TableField` / `@EnumValue` / `@Version` / `@TableId` / "MyBatis-Plus" / "MP" / "baomidou" | 激活 |
| 纯 MyBatis 原生（无 MP），仅问 XML / 事务 | 部分适用（仅 `references/10-xml.md` + `11-transaction.md`） |
| JPA / Hibernate（不建议迁移）/ 表结构设计 / DDL / 纯 SQL 调优 | 不适用 |

> **检查点**：判定为「不适用」→ 告知用户当前问题不在 MyBatis-Plus 范围，建议退出本技能。判定为「部分适用」→ 告知仅 `10-xml.md` + `11-transaction.md` 可参考，其余不适用，让用户确认是否继续。

## 主动行为触发（见到这些代码模式时主动提醒）

- `selectPage` / `page` → 确认引了 `mybatis-plus-jsqlparser` + 注册 `PaginationInnerInterceptor`（否则分页静默失效）
- `@Transactional` 无 `rollbackFor` → 显式指定 `rollbackFor = Exception.class`
- `saveBatch` 当高性能批量 → 默认非 BATCH executor，量大需配 `BatchExecutor`（见 `04-crud.md`）
- 其余触发（null 不更新 / `apply` 注入 / Wrapper 复用 / XML 枚举 typeHandler / join 改写 XML / 字符串字段名 / SQL 函数硬堆 Wrapper）→ 见上方「核心强约束」#3/#4/#7/#8/#9/#11 与下方「使用流程」自检清单

## 核心强约束（Agent 必须遵守）

1. **继承范式**：`XxxMapper extends BaseMapper<T>`；Service 接口 `extends IService<T>`；实现类 `extends ServiceImpl<XxxMapper, T>`。
2. **优先用父类方法**：单表 CRUD 直接用 `BaseMapper` / `IService` 提供的方法（`selectList` / `selectById` / `save` / `updateById` / `page` …），**不要手撸冗余 CRUD 或重复 XML**。
3. **Wrapper 能力边界——超界转 XML**：Wrapper 适合**单表 + 标准比较/排序/聚合条件**（eq/like/in/between/orderBy…）。以下场景**必须改写 XML**，不要用 Wrapper 硬堆：
   - **联表**（JOIN，含子查询关联）
   - **窗口函数**（`ROW_NUMBER()`/`RANK()`/`SUM() OVER(...)` 等）
   - **聚合函数 + GROUP BY/HAVING**（`SUM(cnt)`/`COUNT(DISTINCT …)`）
   - **数据库专有函数 / 复杂表达式**（`DATE_FORMAT()`/`JSON_EXTRACT()`/`CASE WHEN`，跨库不可移植）
   - **自定义列别名 / 投影计算列**（`amount*2 AS double_amount`）

   用 `apply()`/`last()` 拼函数片段是反模式（注入风险 + 跨库不可移植 + 语义不可读），见 `references/05-wrapper.md` §1、`references/10-xml.md`。
4. **null 不更新**：`updateById(entity)` 中 entity 的 `null` 字段默认**不参与更新**（根因：全局 `updateStrategy` 默认 `NOT_NULL`，见 `references/02-config.md` §7）；要显式置空用 `UpdateWrapper.set(...)` 或字段级 `@TableField(updateStrategy = FieldStrategy.ALWAYS)`。全局改 `update-strategy: ALWAYS` 会让所有 null 字段写库误清数据——只允许字段级覆盖。
5. **逻辑删除**：推荐 0+毫秒时间戳方案（`Long` 字段，`logic-not-delete-value: 0`，`logic-delete-value: "UNIX_TIMESTAMP(now())*1000"`）；用全局 `logic-delete-field` 或字段 `@TableLogic`；启用后查询自动过滤已删除行。唯一索引须含 `deleted`（如 `UNIQUE(username, deleted)`），否则删除后同值插入报 Duplicate。
6. **分页插件最后添加 + 显式 DbType**：`MybatisPlusInterceptor.addInnerInterceptor(new PaginationInnerInterceptor(DbType.MYSQL))` 必须放在插件链**最后**；**非 MySQL（PG/Oracle/SQLServer/达梦/金仓）必须显式指定 `DbType`**，否则分页方言可能生成错误（total 错或语法错）。跨库差异（主键策略/引用符/批量语法）见 `references/12-dbtype.md`。
7. **SQL 注入防护**：`Wrapper.apply` 用 `{0}` 占位符（PreparedStatement 参数化）+ 前置 `SqlInjectionUtils.check(...)` 校验，**禁止字符串拼接** SQL 片段。`check(String)` 返回 boolean（true=疑似注入）且**自身不抛异常**——必须 `if (SqlInjectionUtils.check(x)) throw new IllegalArgumentException(...)` 由调用方拦截，禁止裸调用（返回值被忽略＝校验形同虚设）。
8. **Wrapper 不可复用**：同一 `Wrapper` 实例多次使用会叠加条件；每次查询 `new` 一个新的。
9. **枚举映射**：枚举值字段标 `@EnumValue`（或实现 `IEnum`），JSON 序列化标 `@JsonValue`；XML 自定义查询中枚举字段的**每个位置**（resultMap、条件 `#{}`、插入 `#{}`）都要声明 `typeHandler=MybatisEnumTypeHandler`。
10. **高级插件顺序（多租户/数据权限/动态表名 → 分页最后）**：`TenantLineInnerInterceptor` / `DataPermissionInterceptor` / `DynamicTableNameInnerInterceptor` 必须在 `PaginationInnerInterceptor` **之前**添加；否则 COUNT 语句不会被改写，分页总数不准或数据权限漏过滤（见 `references/07-plugin.md` §5）。
11. **字段引用必须用方法引用（Lambda）**：构造条件/更新默认用 `LambdaQueryWrapper` / `LambdaUpdateWrapper` + 方法引用（`User::getName`），**禁止字符串字段名**（`eq("name", ...)`）。例外：动态列名 / 动态表名 / 方言函数等运行时才知道的列——用 `QueryWrapper` / `UpdateWrapper` 字符串形式 + 注释说明，且拼接外部输入走 §7 `{0}` 占位防注入。方法引用编译期检查，字段改名编译报错；字符串字面量无校验，重构改名静默产出错误 SQL（`Unknown column`）或查错数据（见 `references/05-wrapper.md` §1）。
12. **自定义 XML 分页**：Mapper 方法返回 `IPage`（返回 `List` 则 MP 不改写分页）、入参 `page` 非 null（MP 靠它追加 LIMIT/COUNT），`ORDER BY` 写在 XML（见 `references/06-page.md` §4）。

## 决策路由（全部本地，无在线 fetch）

| 需求场景 | 读取文件 |
|---|---|
| 依赖、starter 选择、最小配置、基础 CRUD 跑通 | `references/01-start.md` |
| 全局配置：分页插件、逻辑删除全局、乐观锁、自动填充、防全表、**字段策略(insertStrategy/updateStrategy/whereStrategy)**、DbConfig/Configuration 速查 | `references/02-config.md` |
| 实体映射：@TableId 策略、@TableField(字段策略/null/JSON)、**枚举映射(@EnumValue/IEnum/@JsonValue)**、@Version、@TableLogic | `references/03-entity.md` |
| BaseMapper vs IService、继承范式、优先父类方法、saveBatch、null 不更新、**MP 专属性能（批量 BATCH / InsertBatchSomeColumn / 一级缓存 / 流式大结果集，见 §3）** | `references/04-crud.md` |
| QueryWrapper vs LambdaQueryWrapper、条件构造、apply 防注入、空值语义 | `references/05-wrapper.md` |
| 分页：Page/IPage、自定义 count、联表分页 XML | `references/06-page.md` |
| 插件：逻辑删除/自动填充/乐观锁/多租户/动态表名/数据权限/防全表 | `references/07-plugin.md` |
| **数据库适配：DbType/分页方言/主键策略/标识符引用符/逻辑删除函数/批量语法** | `references/12-dbtype.md` |
| **3.4.x→3.5.x 迁移 / 兼容（breaking changes）** | `references/13-migration.md` |
| **Agent 常见错误与最佳实践** | `references/08-antipattern.md` |
| SQL 日志开启、常见异常与分页失效排查 | `references/09-troubleshoot.md` |
| **MyBatis XML Mapper 编写（mapper-locations / resultMap / 动态 SQL / 联表 / 联表分页）** | `references/10-xml.md` |
| **事务管理（@Transactional / 事务失效 / saveBatch 事务 / 多数据源 / 编程式事务）** | `references/11-transaction.md` |

## 使用流程

1. **确认 MP 适用性**：先执行「第 0 步：依赖探测与激活分支」；依赖缺失时主动询问是否引入 MyBatis-Plus。不适用 → 告知用户并建议退出；部分适用 → 告知范围并让用户确认；正常 → 继续。
2. **定位 reference**：查上方「决策路由」表，读对应文件。
3. **编码遵循强约束**：先看 12 条核心强约束，再读 reference 给代码。
4. **遇异常先查排错**：`references/09-troubleshoot.md` + `references/08-antipattern.md`。
5. **输出前自检（10 项）**：
   - [ ] starter 坐标对应 SpringBoot 版本？（2.x / 3.x / 4.x）
   - [ ] 分页场景引了 `mybatis-plus-jsqlparser`？
   - [ ] `updateById` 需置 null？→ 改用 `LambdaUpdateWrapper.set()`
   - [ ] XML 中枚举字段每处 `#{}` 都声明了 `typeHandler=MybatisEnumTypeHandler`？
   - [ ] Wrapper 每次 `new` 新实例？
   - [ ] Wrapper 条件用方法引用（`User::getXxx`）？字符串字段名仅限动态列名/动态表名例外
   - [ ] 窗口/聚合/GROUP BY/专有函数/计算列场景 → 改写 XML，未用 `apply`/`last` 拼？
   - [ ] `@Transactional` 显式写了 `rollbackFor = Exception.class`？
   - [ ] 事务方法无自调用？
   - [ ] 自定义 XML 分页：方法返回 `IPage`、入参 `page` 非 null？
