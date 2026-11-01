---
name: mq-reliability
slug: mq-reliability
displayName: MQ 可靠性契约
description: >-
  RabbitMQ / 消息队列可靠性契约：在写生产者或消费者前用五个入口问题定下可靠性级别、
  幂等策略、重试与死信、顺序保障、积压预案，避免测试全绿但线上丢消息、重复执行、
  积压失控的假绿陷阱。
  在使用 RabbitMQ / Spring AMQP 写消息生产者或消费者、设计异步事件分发、
  排查消息丢失 / 重复消费 / 积压 / 死信时使用。
  触发信号：@RabbitListener、RabbitTemplate、spring-boot-starter-amqp、
  AmqpTemplate、消息队列、MQ、消费者、生产者、事件分发、异步通知、
  丢消息、消息丢失、重复消费、死信队列、DLQ、消息积压、顺序消费、幂等。
  不适用：RabbitMQ 安装部署 / 集群运维、Kafka / RocketMQ 等其他 MQ 的 API 用法、
  Spring Cloud Stream、消息中间件选型。
version: "1.0.0"
last_verified: "2026-10-28"
---

# MQ 可靠性契约

模型对 RabbitMQ 基础配置（DLX / 重试 / durable）的判断已经够准（基线实测 3/3 全对），不必再写。
真正的缺口在**测试全绿但线上出事**的地方：DLQ 配了没人看、幂等不稳、积压无监控。
本技能只做三件事：把五个决策定下来、动手前读一遍、写完验证。

## 两条原则

1. **五问先答，契约落盘。** 第一次在项目里写消息代码时，把 D1–D5 的答案写进
   `.claude/rules/mq-reliability.md`（提案-同意制，未经同意不写）；之后每次动生产者/消费者前先读它。
   读不到时按 `references/01-decisions.md` 的默认值写，并在回复里声明
   「按 mq-reliability 默认，未读到项目契约」。
2. **写完用假绿元判据自查。** 测试环境不杀 broker、只投一次、消息量小——
   把 broker 停掉 / 同条消息投两次 / 投 10 万条，你的代码会出什么问题？
   想不出来就是还没想清楚，回 `references/02-traps.md` 逐组过。

## 第一步：读项目

| 读什么 | 得到什么 |
|---|---|
| `pom.xml` / `build.gradle` | 是否已有 spring-amqp / spring-rabbit 依赖 |
| `.claude/rules/mq-reliability.md` | 项目已有的五问答案。**读到才生效**，读到就遵守 |
| 既有 `@RabbitListener` / `RabbitTemplate` | 既有惯例：ack 模式、幂等做法、拓扑风格 |

**项目惯例与下表默认冲突时，惯例优先。**

## 入口五问

写生产者或消费者前，五问都要有答案。漏一问就漏一个决策维度。

| # | 入口问题 | 决策什么 | 不答的后果 |
|---|---|---|---|
| D1 | 这条消息丢了会怎样？ | 可靠性级别：confirm + 持久化 + ack 策略 | 静默丢消息 |
| D2 | 同一条消息处理两次会怎样？ | 幂等策略：去重键 + 去重位置 | 重复扣款 / 重复通知 |
| D3 | 消费失败了消息去哪？ | 重试次数 + DLX + **DLQ 谁来看** | 毒消息死循环 / 死信黑洞 |
| D4 | 这些消息必须按顺序吗？ | 单消费者 / 业务键分片 + SAC | 状态错乱 |
| D5 | 生产快过消费怎么办？ | prefetch + 积压告警阈值 + 降级 | 积压无人知 |

展开见 `references/01-decisions.md`。

## 强约束

只收「写错后测试仍然绿」的。会红的（依赖缺失、API 签名错）不在表内。

| ✗ 禁止 | ✓ 推荐 | 假绿原因 |
|---|---|---|
| DLQ 配了没人看 | DLQ 挂消费者或告警，死信必须有人处理 | 测试不触发 DLQ 路径 |
| 累加型操作裸消费 | 按业务唯一键去重（DB 唯一键 / 状态机 / Redis setnx） | 重复投递累加翻倍 |
| 委托下游去重但没约定 | 自己去重，或与下游书面约定去重键与语义 | 下游没做 = 重复副作用 |
| 多步副作用 + AUTO ack 不想 crash | 多步副作用用手动 ack，或保证幂等后用 AUTO | JVM crash 后重投重复执行 |
| 不开 publisher confirm | 开 confirm + 处理 nack / return | 发送方不知道丢了 |
| 无队列深度监控 | 设积压告警阈值 | 测试消息量小测不出积压 |
| 不问 D4 就开多消费者 | 先答 D4；要顺序 → 单消费者或分片 + SAC | 多消费者打乱顺序 |

假绿陷阱详解见 `references/02-traps.md`。

## 与 java-contract 的边界

「重复到达」在 java-contract 管**业务语义**（返回上次结果、不重复执行），在本技能管**传输语义**
（MQ 可能投两次）。两层都要答，D2 的幂等策略涉及业务写操作时指向 java-contract 的「重复到达」条目。
