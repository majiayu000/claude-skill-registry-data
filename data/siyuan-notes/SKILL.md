---
name: siyuan-notes
description: 思源笔记查询工具，如果用户的请求涉及查找、检索、浏览他们的笔记内容，就应该使用这个技能，例如:查询我的xxx
---

## 技能使用指南

### 推荐调用方式

**方式1：使用Bash工具**
```bash
# 在技能目录中执行搜索
node index.js search "工作总结" 10

# 查询最近内容
node index.js recent 7

# 其他功能
node index.js check
```

**方式2：使用node -e执行JS代码（使用显示的 skill Base directory 作为 cwd）**
```bash
node -e "
const siyuan = require('./index.js');
(async () => {
  const results = await siyuan.searchNotes('工作总结', 10);
  console.log(siyuan.formatResults(results));
})();
"  
```

**注意事项：**
- 直接执行index.js时：会自动从其所在目录加载.env文件，无需特殊路径处理
- 使用node -e时：用技能执行时显示的 "Base directory for this skill" 路径作为cwd参数
- 路径中包含空格时需要引号
- 不要用cd命令，直接用cwd参数控制工作目录
- 尽可能使用 node -e执行而非创建临时 js 文件

## 快速使用指南

### 核心 API 函数

```javascript
const siyuan = require('./index.js');

// 搜索笔记内容
await siyuan.searchNotes('关键词', 20, 'p'); // 搜索段落
await siyuan.searchNotes('关键词', 10, 'h'); // 搜索标题

// 查询最近内容
await siyuan.getRecentBlocks(7, 'updated'); // 最近7天更新

// 查询任务
await siyuan.searchTasks('[ ]', 7); // 未完成任务

// 格式化结果
siyuan.formatResults(results); // 转换为可读格式
```

### 常见查询场景

#### 1. 搜索工作总结/开发内容

```javascript
// 搜索包含"工作"的内容
await siyuan.searchNotes('工作', 15);

// 搜索包含"开发"的内容
await siyuan.searchNotes('开发', 10);

// 搜索包含"总结"的标题
await siyuan.searchNotes('总结', 10, 'h');

// 查询最近7天的所有内容
await siyuan.getRecentBlocks(7, 'updated');
```

#### 2. 任务管理

```javascript
// 查询未完成任务
await siyuan.searchTasks('[ ]', 7);

// 查询已完成任务
await siyuan.searchTasks('[x]', 30);

// 查询所有任务（不限状态）
await siyuan.searchTasks('', 7);
```

#### 3. 文档导航

```javascript
// 列出所有文档
await siyuan.listDocuments();

// 查询特定文档的子块
await siyuan.getDocumentBlocks('文档ID');

// 查询文档标题
await siyuan.getDocumentHeadings('文档ID');
```

#### 4. 标签和引用

```javascript
// 按标签搜索
await siyuan.searchByTag('重要', 10);

// 查询反向链接
await siyuan.getBacklinks('块ID', 20);
```

### 命令行使用

```bash
# 基础搜索
node index.js search "工作" 10
node index.js search "总结" 5 h

# 查询最近内容
node index.js recent 7
node index.js recent 14 p

# 任务查询
node index.js tasks "[ ]" 7

# 其他功能
node index.js docs
node index.js tag "重要"
```

## 查询策略选择

### 何时使用 API 函数

- **简单搜索**: 单个关键词搜索
- **常规查询**: 获取最近内容、文档列表等
- **快速原型**: 验证查询思路
- **标准化操作**: 任务管理、标签查询等

### 何时使用 SQL

- **复杂条件**: 多个 AND/OR 条件组合
- **跨表查询**: 需要 JOIN 多个表
- **统计分析**: COUNT、AVG、GROUP BY 等
- **性能优化**: 需要精确控制查询逻辑

## 实际应用示例

### 查找工作总结 (混合策略)

```javascript
const siyuan = require('./index.js');

// 1. 使用API快速搜索
const workResults = await siyuan.searchNotes('工作', 10);
const summaryResults = await siyuan.searchNotes('总结', 5, 'h');

// 2. 使用SQL进行精确查询
const complexResults = await siyuan.executeSiyuanQuery(`
    SELECT content, hpath, created, type, subtype
    FROM blocks
    WHERE (content LIKE '%工作%' OR content LIKE '%总结%' OR content LIKE '%汇报%')
    AND created >= '20251201000000'
    AND type IN ('p', 'h', 'l')
    AND length > 10
    ORDER BY updated DESC
    LIMIT 25
`);

// 3. 合并结果并去重
const allResults = [...workResults, ...summaryResults, ...complexResults];
const uniqueResults = allResults.filter(
  (item, index, self) => index === self.findIndex((t) => t.id === item.id),
);

// 4. 格式化输出
return siyuan.formatResults(uniqueResults.slice(0, 20));
```

### 项目进展查询 (SQL 为主)

```javascript
// 查找特定项目的所有相关内容
const projectQuery = `
    SELECT content, type, subtype, hpath, created, updated
    FROM blocks
    WHERE (
        content LIKE '%项目名称%'
        OR content LIKE '%功能模块%'
        OR hpath LIKE '%项目路径%'
    )
    AND created >= '20251201000000'
    ORDER BY updated DESC, type DESC
    LIMIT 30
`;

const projectResults = await siyuan.executeSiyuanQuery(projectQuery);

// 分类展示结果
const titles = projectResults.filter((item) => item.type === 'h');
const paragraphs = projectResults.filter((item) => item.type === 'p');
const tasks = projectResults.filter((item) => item.type === 'l');

return {
  summary: `找到 ${projectResults.length} 条相关内容`,
  titles: siyuan.formatResults(titles.slice(0, 5)),
  keyContent: siyuan.formatResults(paragraphs.slice(0, 10)),
  tasks: siyuan.formatResults(tasks.slice(0, 5)),
};
```

### 时间线分析 (统计查询)

```javascript
// 分析最近的工作活动
const activityAnalysis = await siyuan.executeSiyuanQuery(`
    SELECT
        DATE(substr(created, 1, 8)) as work_date,
        COUNT(*) as content_count,
        COUNT(DISTINCT root_id) as doc_count,
        SUM(CASE WHEN type = 'l' THEN 1 ELSE 0 END) as task_count
    FROM blocks
    WHERE created >= strftime('%Y%m%d%H%M%S', datetime('now', '-7 days'))
    AND (content LIKE '%工作%' OR content LIKE '%开发%' OR content LIKE '%项目%')
    GROUP BY DATE(substr(created, 1, 8))
    ORDER BY work_date DESC
`);

return siyuan.formatStructuredResults(activityAnalysis);
```

### sql要求

1. **SQL 语法规范**：

   - 在默认的情况下，用户可以在思源的嵌入块中输入 SQL 代码查询，此时 SQL 查询语句必须以 `select * from blocks` 开头：只允许查询 block 表，且不允许单独查询字段
     - 面向开发者的高级用法：用户还可以调用后端 API 接口，发送 SQL 查询，此时是可以使用更普遍的 SQL 语法结构的（查询别的表，返回特定字段）
   - 使用 SQLite 的语法，如 `strftime` 函数处理时间。
   - 默认情况下，查询结果最多返回 64 个块，除非明确指定了 `limit xxx`

2. **输出**：将查询语句放在一个 ```SQL 的 markdown 代码块当中，方便用户直接复制

### 表结构

**blocks 表:**

- `id`: 内容块 ID，格式为 `时间-随机字符`，例如 `20210104091228-d0rzbmm`。
- `parent_id`: 双亲块 ID，格式同 `id`
- `root_id`: 文档块 ID，格式同 `id`
- `box`: 笔记本 ID，格式同 `id`
- `path`: 内容块所在文档路径，例如 `/20200812220555-lj3enxa/20210808180320-abz7w6k/20200825162036-4dx365o.sy`
- `hpath`: 人类可读的内容块所在文档路径，例如 `/0 请从这里开始/编辑器/排版元素`
- `name`: 内容块名称
- `alias`: 内容块别名
- `memo`: 内容块备注
- `tag`: 标签，例如 `#标签1 #标签2# #标签3#`
- `content`: 去除了 Markdown 标记符的文本
- `fcontent`: 存储容器块第一个子块的内容
- `markdown`: 包含完整 Markdown 标记符的文本
- `length`: `markdown` 字段文本长度
- `type`: 内容块类型

  - `d`: 文档, `h`: 标题, `m`: 数学公式, `c`: 代码块, `t`: 表格块, `l`: 列表块, `b`: 引述块, `s`: 超级块，`p`：段落块，`av`：树形视图（俗称数据库，注意区分，这只是一个内容块的叫法）

- `subtype`: 特定类型的内容块还存在子类型

  - 标题块的 `h1` 到 `h6`
  - 列表块的 `u` (无序), `t` (任务), `o` (有序)

- `ial`: 内联属性列表，形如 `{: name="value"}`，例如 `{: id="20210104091228-d0rzbmm" updated="20210604222535"}`
- `sort`: 排序权重，数值越小排序越靠前
- `created`: 创建时间，格式为 `YYYYMMDDHHmmss`，例如 `20210104091228`
- `updated`: 更新时间，格式同 `created`

**refs 表:**

- `id`: 引用 ID，格式为 `时间-随机字符`，例如 `20211127144458-idb32wk`
- `def_block_id`: 被引用块的块 ID，格式同 `id`
- `def_block_root_id`: 被引用块所在文档的 ID，格式同 `id`
- `def_block_path`: 被引用块所在文档的路径，例如 `/20200812220555-lj3enxa/20210808180320-fqgskfj/20200905090211-2vixtlf.sy`
- `block_id`: 引用所在内容块 ID，格式同 `id`
- `root_id`: 引用所在文档块 ID，格式同 `id`
- `box`: 引用所在笔记本 ID，格式同 `id`
- `path`: 引用所在文档块路径，例如 `/20200812220555-lj3enxa/20210808180320-fqgskfj/20200905090211-2vixtlf.sy`
- `content`: 引用锚文本

**attributes 表:**

- `id`: 属性 ID，格式为 `时间-随机字符`，例如 `20211127144458-h7y55zu`
- `name`: 属性名称

  - 注意：思源中的用户自定义属性必须加上 `custom-` 前缀
  - 例如 `name` 是块的内置属性，但 `custom-name` 就是用户的自定义属性了

- `value`: 属性值
- `type`: 类型，例如 `b`
- `block_id`: 块 ID，格式同 `id`
- `root_id`: 文档 ID，格式同 `id`
- `box`: 笔记本 ID，格式同 `id`
- `path`: 文档文件路径，例如 `/20200812220555-lj3enxa.sy`。

### 查询要点提示

- 所有 SQL 查询语句如果没有明确指定 `limit`，则会被思源查询引擎默认设置 `limit 64`
- 块属性格式相关

  - 块 ID 格式统一为 `时间-随机字符`, 例如 `20210104091228-d0rzbmm`
  - 块的时间属性，如 created updated 的格式为 `YYYYMMDDHHmmss` 例如 `20210104091228`

- 块之间的关系

  - 层级关系：块大致可以分为

    - 内容块（叶子块）：仅包含内容的块，例如段落 `p`，公式块 `m`，代码块 `c`，标题块 `h`，表格块 `t` 等

      - 内容块的 `content`和 `markdown` 字段为块的内容

    - 容器块：包含其他内容块或者容器块的块，例如 列表块 `l`，列表项块 `i`，引述块/引用块 `b`，超级块 `s`

      - 每个块的 `parent_id` 指向他直接上层的容器块
      - 容器块的 `content`和 `markdown` 字段为容器内所有块的内容

    - 文档块：包含同一文档中所有内容块和容器块的块，`d`

      - 每个块的 `root_id` 指向他所在的文档
      - 容器块的 `content` 字段为文档的标题

  - 引用关系：当一个块引用了另一个块的时候，会在 refs 表中建立联系

    - 如果有多个块引用了同一个块，那么对这个被引用的块而言，这些引用它的块构成了它的反向链接（反链）
    - 所有引用关系被存放在 ref 表当中；使用的时候将 blocks 表和 ref 表搭配进行查询

- Daily Note：又称日记，每日笔记，是一种特殊的**文档块**

  - daily note 文档有特殊属性：`custom-dailynote-<yyyyMMdd>=<yyyyMMdd>`；被标识了这个属性的文档块(type='d')，会被视为是对应日期的 daily note
  - 例如 `custom-dailynote-20240101=20240101` 的文档，被视为 2024-01-01 这天的 daily note 文档
  - 请注意！ daily note （日记）是一个文档块！如果要查询日记内部的内容，请使用 `root_id` 字段来关联日记文档和内部的块的关系

- 书签：含有属性 `bookmark=<书签名>` 的块会被加入对应的书签

### SQL 示例

- 查询所有文档块

  ```sql
  select * from blocks where type='d'
  ```

- 查询所有二级标题块

  ```sql
  select * from blocks where subtype = 'h2'
  ```

- 查询某个文档的子文裆

  ```sql
  select * from blocks
  where path like '%/<当前文档id>/%' and type='d'
  ```

- 随机漫游某个文档内所有标题块

  ```sql
  SELECT * FROM blocks
  WHERE root_id LIKE '<文档 id>' AND type = 'h'
  ORDER BY random() LIMIT 1
  ```

- 查询含有关键词「唯物主义」的段落块

  ```sql
  select * from blocks
  where markdown like '%唯物主义%' and type ='p'
  ORDER BY updated desc
  ```

- 查询过去 7 天内没有完成的任务（任务列表项）

  > 注：思源中，任务列表项的 markdown 为 `* [ ] Task text` 如果是已经完成的任务，则是 `* [x] Task Text`

  ```sql
  SELECT * from blocks
  WHERE type = 'l' AND subtype = 't'
  AND created > strftime('%Y%m%d%H%M%S', datetime('now', '-7 day'))
  AND markdown like'* [ ] %'
  AND parent_id not in (
    select id from blocks where subtype = 't'
  )
  ```

- 查询某个块所有的反链块（引用了这个块的所有块）

  ```sql
  select * from blocks where id in (
      select block_id from refs where def_block_id = '<被引用的块ID>'
  ) limit 999
  ```

- 查询某个时间段内的 daily note（日记）

  > 注意由于没有指定 limit，最大只能查询 64 个

  ```sql
  select distinct B.* from blocks as B join attributes as A
  on B.id = A.block_id
  where A.name like 'custom-dailynote-%' and B.type='d'
  and A.value >= '20231010' and A.value <= '20231013'
  order by A.value desc;
  ```

- 查询某个笔记本下没有被引用过的文档，限制 128 个

  ```sql
  select * from blocks as B
  where B.type='d' and box='<笔记本 BoxID>' and B.id not in (
      select distinct R.def_block_id from refs as R
  ) order by updated desc limit 128
  ```
