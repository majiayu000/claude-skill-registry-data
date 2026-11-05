---
name: tech-resume-optimizer
description: 优化技术类简历，覆盖软件工程、产品经理（PM）及技术岗位，适用于 tech resume、SWE resume、developer resume 等场景
---

# 技术简历优化器（Tech Resume Optimizer）

## 何时使用此技能

当用户：
- 正在申请软件工程岗位
- 想要优化技术类简历
- 需要 AI 帮助完成开发/PM/技术类岗位的求职申请
- 提到："技术简历"、"软件工程师简历"、"开发工程师简历"、"tech resume"、"software engineer resume"、"SWE resume"、"PM resume"等

## 核心能力

- 针对 SWE、PM、数据、DevOps 等技术岗位优化简历
- 有效地组织技术技能版块的排版结构
- 突出项目经历与技术成就
- 平衡技术深度与业务影响力
- 兼顾 ATS（申请人跟踪系统）与技术招聘官的双重要求
- 处理 GitHub、作品集和技术相关链接

## 技术简历理念

**技术招聘官看什么：**
1. 相关技术技能（编程语言、框架、工具）
2. 规模与影响力（用户量、交易量、数据量）
3. 问题解决能力
4. 系统设计理解能力
5. 协作能力
6. 成长轨迹

## 技术简历结构

### 推荐顺序

```
1. 联系方式（含 GitHub、作品集）
2. 个人简介（可选但很有帮助）
3. 技术技能（对 ATS 至关重要）
4. 工作经历（以技术成就为重点）
5. 项目经历（对职业早期尤其重要）
6. 教育背景
7. 认证证书（如有相关）
```

### 技术简历的联系信息版块

```
张伟
北京
zhangwei@email.com | 138-XXXX-XXXX
LinkedIn: linkedin.com/in/zhangwei
GitHub: github.com/zhangwei
作品集：zhangwei.dev
```

**应该包括：**
- GitHub（申请 SWE 岗位必备）
- 作品集/个人网站
- LinkedIn
- 技术博客（如果你有）

**不应该包括：**
- 详细住址（写城市即可）
- 照片
- 其他社交媒体（除非与岗位相关）

## 技术技能版块

### 组织策略

**方案 1：按类别**
```
编程语言：Python, JavaScript, TypeScript, Go, SQL
框架：React, Node.js, Django, FastAPI
数据库：PostgreSQL, MongoDB, Redis, Elasticsearch
云/基础设施：AWS (EC2, S3, Lambda, RDS), Docker, Kubernetes, Terraform
工具：Git, JIRA, CI/CD, Datadog, Grafana
```

**方案 2：按熟练度**（慎用）
```
精通：Python, React, PostgreSQL, AWS
熟练：Go, TypeScript, MongoDB, Docker
了解：Rust, GraphQL, Kubernetes
```

**方案 3：平铺列表**（ATS 友好）
```
技能：Python, JavaScript, TypeScript, React, Node.js, Django, PostgreSQL, MongoDB, AWS, Docker, Kubernetes, Git
```

### 应该写什么

**编程语言：**
- 列出你能熟练编码的语言
- 按与目标岗位的相关程度排序
- 包括查询语言（SQL、GraphQL）

**框架/库：**
- Web：React, Vue, Angular, Django, Flask, Express
- 数据：Pandas, NumPy, TensorFlow, PyTorch
- 测试：Jest, Pytest, Selenium

**数据库：**
- 关系型：PostgreSQL, MySQL, SQL Server
- NoSQL：MongoDB, DynamoDB, Cassandra
- 缓存：Redis, Memcached

**云/DevOps：**
- 云平台：AWS, GCP, Azure（写明具体服务）
- 容器：Docker, Kubernetes
- CI/CD：Jenkins, GitHub Actions, CircleCI
- IaC：Terraform, CloudFormation

### 不要写的内容
- ❌ Microsoft Office（默认人人会用）
- ❌ 操作系统（除非申请 DevOps 岗位）
- ❌ 过时技术（除非岗位明确要求）
- ❌ 技能条形图或打分（主观且会破坏 ATS 解析）
- ❌ 只用过一次的全部技术都写上

## 技术岗位的工作经历版块

### 技术经历条目公式

**[动作动词] + [技术层面做了什么] + [规模/影响] + [使用的技术]**

**示例：**

❌ **薄弱的技术经历条目：**
```
- 参与后端服务开发
- 帮助提升系统性能
- 为产品开发功能
```

✅ **有力的技术经历条目：**
```
- 主导从单体架构到微服务的迁移，将部署时间从 2 小时缩短至 15 分钟，使各团队能够独立部署
- 优化 PostgreSQL 查询并引入 Redis 缓存，为 10 万日活用户将 API 延迟降低 60%（从 500ms 降至 200ms）
- 基于 WebSocket 和 AWS SNS 构建实时通知系统，日处理消息 100 万+ 条，送达率达 99.9%
```

### 应该写的技术指标

**规模：**
- 用户量："日均服务 50 万 DAU"
- 请求量："承载 1 万 QPS"
- 数据量："日处理数据 50TB"
- 可用性："维持 99.99% 可用性"

**性能：**
- 延迟："从 Xms 降至 Yms"
- 速度："提升 X%"
- 加载时间："缩短 X 秒"

**效率：**
- 成本："AWS 云成本降低 40%"
- 时间："部署时间从 X 缩短至 Y"
- 资源："内存占用降低 X%"

**业务：**
- 收入："功能带来 XX 万元收入"
- 转化："结算转化率提升 X%"
- 留存/活跃："DAU 提升 X%"

### 分岗位经历条目示例

**软件工程师（SWE）：**
```
• 基于 OAuth 2.0 和 JWT 设计并实现认证服务，保障 200 万+ 用户账户安全，零安全事故
• 主导迁移至 Kubernetes，实现 99.99% 在线率，基础设施成本降低 35%（每年节省约 140 万元）
• 通过代码评审与结对编程指导 3 名初级工程师，团队交付效率提升 25%
```

**数据工程师：**
```
• 基于 Apache Kafka 和 Spark 构建日处理 1 亿+ 事件的数据管道，将数据延迟从小时级降至分钟级
• 在 Snowflake 中设计数仓 schema，为 50+ 业务用户提供自助分析能力
• 使用 Great Expectations 搭建数据质量监控，在影响下游系统前拦截 95% 的数据问题
```

**DevOps/SRE：**
```
• 使用 Terraform 实现基础设施即代码，资源开通时间从 2 天缩短至 30 分钟
• 基于 Prometheus 和 Grafana 搭建监控告警体系，将平均故障恢复时间（MTTR）从 4 小时降至 30 分钟
• 使用 GitHub Actions 自动化部署流水线，支撑每日 50+ 次部署且发布零停机
```

**产品经理（技术方向）：**
```
• 主导面向开发者的 API 平台路线图，服务 1 万+ 开发者，API 采用率提升 40%
• 为 ML 推荐引擎制定技术需求文档，用户互动时长提升 25%
• 与工程团队协作将技术债减少 30%，发布节奏从双周升级为每周
```

## 项目经历版块

**对以下人群至关重要：**
- 初级工程师
- 转行求职者
- 训练营（Bootcamp）毕业生
- 任何有职业空窗期的人

### 项目格式

```
项目名称 | 技术栈 | 链接
• 说明项目做了什么
• 技术亮点与攻克的挑战
• 规模或使用量指标（如有）
```

### 项目版块示例

```
项目经历

分布式任务队列 | Python, Redis, Docker | github.com/user/taskqueue
• 构建每小时处理 1 万+ 任务的分布式任务队列，支持自动重试与死信队列
• 实现优先级队列与限流机制，支持多租户

实时聊天应用 | React, Node.js, WebSocket, MongoDB | chatapp.demo.com
• 全栈聊天应用，支持 100+ 并发用户的实时消息收发
• 实现端到端加密与消息持久化

ML 价格预测器 | Python, TensorFlow, FastAPI | github.com/user/predictor
• 基于 100 万+ 数据点训练回归模型，价格预测准确率达 92%
• 以 REST API 形式部署，并搭建模型自动再训练流水线
```

### 什么样的项目算好项目

**应该包括：**
- 有真实用户的项目
- 开源贡献
- 技术博客文章
- 黑客马拉松获奖项目（尤其是名次靠前的）
- 复杂的个人项目

**不应该包括：**
- 照着教程写的跟练项目
- 简单的待办事项应用
- 未完成的项目
- 课程作业（除非特别出色）

## 技术简历的教育背景版块

### 标准格式
```
计算机科学学士 | 大学名称 | 2020
GPA: 3.8/4.0（高于 3.5 时再写）
相关课程：分布式系统、机器学习、数据库系统
```

### 训练营（Bootcamp）毕业生
```
软件工程证书 | App Academy 训练营 | 2023
- 1000+ 小时沉浸式课程
- 全栈 JavaScript、React、Node.js、PostgreSQL

经济学学士 | 大学名称 | 2020
```

### 自学成才的工程师
```
专业认证：
- AWS Solutions Architect Associate | 2023
- MongoDB Certified Developer | 2023

相关学习经历：
- MIT 公开课（OpenCourseWare）：《算法》《数据结构》
- Coursera：机器学习专项课程（斯坦福）
```

## 技术简历专属建议

### GitHub 个人主页优化

**确保你的 GitHub 展示：**
- 置顶仓库（你最好的 6 个）
- 贡献热力图（保持绿色/活跃）
- 个人主页 README
- 完整的项目 README

**项目 README 应包含：**
- 项目功能说明
- 使用的技术
- 如何运行
- 截图/演示
- 你的贡献（针对协作项目）

### 应对技术栈匹配问题

**如果你的技术栈与对方一致：**
- 把这些技术放在最显眼的位置
- 用数据量化你使用它们的经验

**如果技术栈不完全一致：**
- 强调可迁移技能
- 展示学习能力
- 突出相似技术
- 示例：写的是 "Django" → 改为 "具备丰富的 Python Web 框架经验（Django）；能快速上手新框架"

### 技术面试准备提示

技术简历要能在面试中"兜得住"：
- 只写你能深入讨论的技术
- 对列出的每个项目都能解释清楚
- 熟悉你做过的系统的架构
- 为每条经历条目准备好背后的故事

## 输出格式

优化技术简历时：

```markdown
# 技术简历优化报告

## 技术技能重构
**当前：** [对方现有的技能版块]
**优化后：**
编程语言：[排序后的列表]
框架：[排序后的列表]
数据库：[排序后的列表]
云/工具：[排序后的列表]

## 工作经历改进

### [公司/职位]

**当前经历条目 1：**
"参与后端服务开发"

**优化后：**
"设计并部署 5 个 Node.js 微服务，承载每分钟 5 万次请求，降低系统耦合度，使各团队可独立部署"

**当前经历条目 2：**
[对所有经历条目逐条继续]

## 建议突出的项目
[基于对方背景给出建议]

## GitHub 优化建议
- [ ] 为置顶仓库补充 README
- [ ] 置顶 X 项目（最相关的）
- [ ] 添加个人主页 README

## 需弥补的技术短板
- [缺失技能] → [如何在简历/求职信中弥补]
```

## ATS 与技术招聘官的平衡

请记住：你的简历既要通过 ATS（申请人跟踪系统），又要打动技术招聘官。

**针对 ATS：**
- 写入确切的技能关键词
- 使用标准的版块标题
- 避免使用表格和图形

**针对技术招聘官：**
- 展示技术深度
- 写入指标与规模
- 展现问题解决能力
- 体现你对系统的理解