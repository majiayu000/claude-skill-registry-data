---
name: redis-dev
description: >-
  Redis 开发与审查助手（Java / Spring Boot）。开发、审查或优化缓存（@Cacheable 声明式 /
  RedisTemplate 手动）、分布式锁（Redisson / lock4j / SET NX EX / 看门狗）、Redis 连接与配置
  （单机 / 哨兵 / 集群 / 连接池）、序列化（key 乱码 / JSON / LocalDateTime）、缓存一致性
  （穿透 / 击穿 / 雪崩 / hot key / 先更库再删缓存 / cache aside）、用 Redis 数据结构实现业务功能
  （计数器 / 签到 / 去重 / 延迟队列 / UV 统计 / 布隆过滤器 / 限流）、消息与事件（发布订阅 /
  Pub/Sub / Stream 可靠队列 / 键空间通知 / 过期事件）时使用本技能——无需用户提到 Redis。
  次级触发信号——代码或 pom 中出现：spring-boot-starter-data-redis、redisson、RedisTemplate、
  @Cacheable / @CacheEvict / @CachePut / @EnableCaching、RLock / RedissonClient / tryLock /
  @Lock4j / RRateLimiter / RDelayedQueue / RBloomFilter、opsForValue 等 opsFor* 方法、
  convertAndSend / RedisMessageListenerContainer / StreamMessageListenerContainer 时必须使用本技能；
  用户报错出现：key 乱码（\xac\xed）、序列化 / 反序列化异常、连不上 Redis / command timeout /
  pool exhausted、@Cacheable 不生效、读回 LinkedHashMap 时必须使用本技能。
  不适用于：Sa-Token 等框架自身的会话 / 登录集成、测试容器化 Redis、Redis 服务器安装部署 /
  主从搭建 / 监控指标与内存淘汰策略调优（运维范围）、非 Java 语言。
agent_created: true
version: 1.1.3
slug: redis-dev
displayName: Redis 开发助手
---

# Redis 开发助手

面向 Java / Spring Boot 的 Redis 编码助手：缓存、分布式锁、Redisson 分布式对象（限流 / 延迟队列 / 布隆过滤器）、序列化配置、连接配置、缓存一致性、消息与事件。
版本基准：**Spring Boot 3.x/4.x（Spring Data Redis 3.x/4.x、Lettuce 6.x/7.x）+ Redisson 3.x（Boot 4 下 starter 用 4.x 线，`references/07-redisson.md` §1）**；
Boot 2.7 差异以 `Boot2.x` 标注（主要是 `spring.redis.*` vs `spring.data.redis.*`——Boot 3/4 前缀相同）。
采用**完全本地自包含**策略：所有知识沉淀于本地 `references/`，运行时不依赖任何外部文档站点。

## 版本与依赖

| 场景 | 依赖 | 说明 |
|---|---|---|
| 缓存 / 任意 Redis 读写 | `spring-boot-starter-data-redis` | 默认 Lettuce 客户端，自带 |
| 声明式缓存 @Cacheable | `spring-boot-starter-data-redis` + `spring-boot-starter-cache` | 还需 `@EnableCaching` |
| 分布式锁 / 限流 / 布隆过滤器 / 延迟队列 | `org.redisson:redisson` 手动配置（数据面留在 Lettuce，**默认**）；或 `redisson-spring-boot-starter`（整体替换连接层，全新项目 / Redisson 数据面） | 仅缓存场景**不要**引入 |
| 连接池（池参数生效） | `org.apache.commons:commons-pool2` | **池实现库，不是 Redis 客户端**；仅配 `lettuce.pool.*` 时需要（普通命令不走池，`references/02-pool.md` §1） |

- **配置命名空间**：Boot 3/4 用 `spring.data.redis.*`，Boot 2.x 用 `spring.redis.*`——配错导致连不上（症状见 `references/08-troubleshoot.md`）。
- **redisson-spring-boot-starter 会把 RedisConnectionFactory 替换为 Redisson 实现**（RedisTemplate 底层随之切换），引入即全局生效，详见 `references/07-redisson.md` §1。

## 第 0 步：依赖探测与激活分支

任务涉及缓存、分布式锁、Redis 配置、序列化、数据结构实现——**即使用户没提 Redis**——先检索项目依赖与代码（pom / build.gradle 搜 `data-redis`、`redisson`、`lock4j`；代码搜 `RedisTemplate`、`@Cacheable`、`RLock`）：

| 探测结果 | 动作 |
|---|---|
| 已有 `data-redis` / `redisson` / `lock4j` 依赖，或代码用 `RedisTemplate` / `@Cacheable` / `RLock` | 直接激活，走「关键决策检查点」→「决策路由」 |
| 无任何 Redis 依赖，但任务要求缓存 / 锁 / 计数 / 排行 | **主动询问**是否引入 Redis（说明：进程内缓存 Caffeine 也可能是答案——单实例部署、无共享需求时）；同意 → 按「版本与依赖」表引入后继续 |
| 任务其实是 Sa-Token 等框架自身的会话 / 登录存储问题 | 退出本技能（属框架自身集成，查框架文档） |
| 任务是起 Redis 测试容器 / 测试隔离 | 退出本技能（属集成测试领域） |

## 何时使用本技能

| 信号 | 判定 |
|------|------|
| 写 / 改缓存逻辑（@Cacheable、手动 RedisTemplate 读写） | 激活 |
| 分布式锁、防重复提交、幂等、并发扣减互斥 | 激活 |
| Redis 连接 / 连接池 / 超时 / 哨兵 / 集群配置 | 激活 |
| 序列化：存对象、key 乱码、跨服务共享数据 | 激活 |
| 缓存穿透 / 击穿 / 雪崩、先更新库还是先删缓存 | 激活 |
| 用 Redis 做计数器 / 签到 / 去重 / 延迟队列 / UV / 布隆 / 限流 | 激活 |
| 发布订阅（Pub/Sub）、Stream 消息队列、key 过期事件监听 | 激活 |
| 审查 / 优化存量代码的 Redis 用法（自写锁、keys *、JDK 序列化等隐患识别与迁移） | 激活 |
| 报错：连不上、command timeout、pool exhausted、序列化异常、`@Cacheable` 不生效、读回 `LinkedHashMap` | 激活，先查 `references/08-troubleshoot.md` |
| Redis 服务器安装 / 主从搭建 / 慢查询监控 / 大 key 巡检 / 内存淘汰治理 | 不适用（运维范围） |
| Sa-Token 登录 / 会话 / 踢人相关 | 不适用（框架自身集成，非本技能范围） |

> **检查点**：判定为「不适用」→ 告知用户当前问题不在本技能范围并建议退出。

## 关键决策检查点

以下 3 个场景存在多条技术路线，Agent **不可擅自替用户选择**。

**执行规则（机械判据，逐条执行）：**

1. 拿到任务后、写任何代码前，先扫描用户消息与上下文是否命中下表「触发信号」列的关键词（逐字匹配）。
2. 命中任一检查点 → **本轮回复只做一件事：输出确认问题**。禁止输出业务代码块、依赖坐标、配置片段。
3. 确认问题必须是**选择题**：列出候选方案 + 标注推荐项 + 一句话理由。禁止开放式提问。
4. 用户未明确回答 → 使用「默认推荐」列策略，并在输出开头标注「未确认，已使用默认方案」。
5. 用户确认方向 → 按选择生成代码，不再重复追问。
6. 一个需求命中多个检查点 → 一次性列出全部确认问题，全部完成后才生成代码。

| # | 触发信号（逐字关键词） | 必须确认的问题 | 方案差异（一句话） | 默认推荐 |
|---|---|---|---|---|
| C1 | "加缓存" / "缓存" / "cache"（未指明方式） | ① 声明式 `@Cacheable` 还是手动 `RedisTemplate`？② TTL 档位：30min（默认推荐）/ 10min~24h 自定？ | 声明式：简洁、注解即生效，适合整对象读缓存；手动：精细控制（部分更新 / 计数 / 锁配合），适合复杂逻辑。见 `references/05-spring-cache.md` §1 | 简单查询缓存用 `@Cacheable` + 显式 TTL 30min |
| C2 | "锁" / "分布式锁" / "防重复" / "幂等" / "并发" | ① 项目是否已有 Redisson / lock4j？没有 → 是否同意引入？② 业务执行时长上界：<30s / <5min / 不可预估？ | Redisson `RLock`：显式 waitTime + leaseTime（持锁硬上限，防挂死被看门狗无限续期）；lock4j `@Lock4j`：注解声明式，底层默认 Redisson，`expire` 即固定租期。**✗ 不自写 SET NX + Lua**（续期 / 可重入 / 安全释放都是坑位）。见 `references/07-redisson.md` §1-§2 | 引入 Redisson，`tryLock(wait, leaseTime)` 两个时间都显式（leaseTime > 业务上界） |
| C3 | "存对象" / "序列化" / "跨服务共享" / "key 可读" | 数据是否需要跨服务 / 跨语言读取？ | `GenericJackson2Json`：写入 `@class` 自动还原类型，单服务最省事；跨服务 ✗ **禁止 `@class`**（包名耦合、跨语言读不懂、类迁移即断）→ ✓ 干净 JSON + 读侧显式类型。见 `references/03-serialization.md` §4 | 单服务 `GenericJackson2Json`（含 JavaTimeModule），跨服务 StringRedisTemplate + 显式类型 |

## 决策路由

| 需求场景（关键词） | 读取文件 |
|---|---|
| 依赖引入、单机 / 哨兵 / 集群连接配置、超时、ACL | `references/01-connection.md` |
| 连接池参数、Lettuce 共享连接、pool exhausted、Jedis 迁移决策 / antipattern | `references/02-pool.md` |
| 序列化方案、key 乱码、GenericJackson2Json、LocalDateTime、LinkedHashMap、跨服务契约、key 规范 / 前缀 | `references/03-serialization.md` |
| scan / keys 禁用 / 批量删除 / unlink、mget / pipeline、事务（multi/exec 无回滚）、Lua 脚本、set 覆盖清 TTL 等陷阱、Bitmap / HyperLogLog | `references/04-template-operations.md` |
| @Cacheable / @CacheEvict、TTL 配置（默认永不过期坑）、自调用失效、多缓存名不同 TTL | `references/05-spring-cache.md` |
| 缓存一致性：先更库还是先删缓存、穿透 / 击穿 / 雪崩三件套、互斥回源 / 逻辑过期异步重建、延迟双删 | `references/06-cache-consistency.md` |
| Redisson：分布式锁（RLock / lock4j / 看门狗 / leaseTime）、限流 RRateLimiter、延迟队列 / 延迟任务 / 超时关单（RDelayedQueue）、布隆过滤器 / 信号量 / 读写锁 | `references/07-redisson.md` |
| 排错路由：症状 → 去哪节查（NullValue / LinkedHashMap / 锁失效 / @Cacheable 不生效 / pool exhausted / 惰性删除） | `references/08-troubleshoot.md` |
| 消息与事件：发布订阅（Pub/Sub）、Stream 可靠队列 / 消费组 / ack、键空间通知（过期事件） | `references/09-messaging.md` |

## 核心强约束

1. **key 序列化器必须 `StringRedisSerializer`**：用默认 JDK 序列化，key 带二进制前缀（`\xac\xed...`），redis-cli 不可读、`keys`/`scan` 模式匹配失效。配置见 `references/03-serialization.md` §2。
2. **缓存必须显式 TTL**：`RedisCacheManager` 默认**永不过期**、手动 `set` 不传过期参数同理——内存只增不减 + 脏数据永驻。TTL 加 10%~30% 随机抖动防雪崩（`references/06-cache-consistency.md` §4）。
3. **`@Cacheable` 的序列化也要显式配**：`RedisCacheConfiguration.defaultCacheConfig()` 默认 value 也是 JDK 序列化——注解缓存与手动 RedisTemplate 是**两套独立序列化配置**，都要设。
4. **禁止 `keys *`**：全量遍历阻塞单线程 Redis，生产禁用；用 `scan` 游标迭代（`references/04-template-operations.md` §1）。
5. **分布式锁只用成熟实现（Redisson / lock4j），禁止自写 SET NX + Lua**：`setnx` + `expire` 两步在崩溃间隔留下死锁；即便补成一条原子命令，续期、可重入、持有者校验释放仍是自己扛的坑位——存量自写锁的修复方向是迁移（`references/07-redisson.md` §2）。
6. **`tryLock` 必须显式 `leaseTime`（持锁硬上限）**：不传时看门狗（默认 30s 租期、每 10s 续期）在 JVM 存活时**无限续期**——业务线程挂死而客户端健康，锁永不释放、其他节点全阻塞（等效死锁）。leaseTime 取业务执行上界 × 安全余量，**宁可长不可短**；锁到期后并发可进入，强互斥场景 DB 兜底（`references/07-redisson.md` §4）。
7. **unlock 必须 try-finally 且先判持有**：`if (lock.isHeldByCurrentThread()) lock.unlock()`，防租期已过被别人持有时抛 `IllegalMonitorStateException`。
8. **写一致性默认「先更新 DB，再删缓存」**：不更新缓存（并发写覆盖）、不先删缓存（并发读回填旧值）。要更低脏读率 → 延迟双删，见 `references/06-cache-consistency.md` §2。
9. **null 缓存必须短 TTL**：穿透防护里缓存空值 TTL 控制在 30s~5min，且 `unless="#result == null"` 会**关闭** null 缓存——别写反。
10. **配置命名空间随 Boot 版本**：Boot 3/4 `spring.data.redis.*`、Boot 2.x `spring.redis.*`；哨兵/集群拓扑下 `database` 仅哨兵/单机有效，**cluster 模式不支持 SELECT、配置静默无效**（`references/01-connection.md` §3）。

## 使用流程

1. **确认适用性**：先执行「第 0 步：依赖探测」，再对照「何时使用本技能」；报错类任务直接从 `references/08-troubleshoot.md` 症状表入手。
2. **关键决策检查点**：逐字扫描 C1–C3 触发信号；命中 → 本轮只输出确认选择题，禁止生成代码。
3. **定位 reference**：查「决策路由」表，读对应文件。
4. **编码前过强约束**：10 条核心强约束逐条对照，尤其 TTL（第 2/9 条）与序列化（第 1/3 条）。
5. **遇异常先查排错**：`references/08-troubleshoot.md`。
6. **输出前自检（二值核对，任一为「否」即违规，必须返工）**：
   - C1–C3 已逐项扫描：命中的检查点均已确认，或已标注「未确认，已使用默认方案」？
   - 所有写入（set / cacheManager / increment 初始化）都带显式 TTL（含 null 缓存短 TTL）？
   - key 序列化器为 String？`@Cacheable` 与 RedisTemplate 两套序列化都配了？
   - 锁：try-finally + isHeldByCurrentThread 判断 + leaseTime 显式且大于业务上界？
   - 没有出现 `keys *`、`setnx`+`expire` 两步、先删缓存后更新 DB？
   - 配置前缀与 Boot 版本一致（spring.data.redis vs spring.redis）？
