---
name: firebase-crashlytics
description: Firebase Crashlytics Android 崩溃与 ANR 分析专家。用于分析 Android Java/Kotlin 崩溃堆栈、解读 Firebase 崩溃报告、定位崩溃根因、提供修复建议。当用户提供 Android 崩溃日志、堆栈跟踪或 ANR 报告时使用此技能。
---

# Firebase Crashlytics 崩溃分析技能

## 概述

此技能用于分析和解读 Google Firebase Crashlytics 生成的 Android 崩溃报告（Java/Kotlin）与 ANR，帮助开发者快速定位问题根因并提供修复建议。

## 触发条件

当用户执行以下操作时应激活此技能：
- 提供 Firebase Crashlytics 崩溃报告或堆栈跟踪
- 粘贴 Android 崩溃日志
- 询问如何分析崩溃原因
- 需要解读 ANR (Application Not Responding) 报告
- 需要符号化/反混淆崩溃堆栈

### 不触发

- 仅描述非 Crashlytics 平台（如 Sentry、Bugsnag）且未要求对比
- 无崩溃信息的泛聊，或只讨论产品运营/埋点
- 请求上传/执行本地构建、下载依赖等（权限外）
- iOS 或 Native/NDK 崩溃分析（不在此技能范围内）

## 使用前提

- 拥有与崩溃报告版本匹配的 mapping.txt
- 崩溃日志包含版本信息（versionCode/versionName 或 build number）、设备/OS 版本
- 明确崩溃类型：Fatal / Non-fatal / ANR / OOM / Watchdog

## 需要用户提供的信息

- 崩溃堆栈原文或 Crashlytics 报告链接/issue id
- App 版本号、构建号、提交哈希（若有）
- 设备型号、OS 版本、发生频率/最近时间
- 是否 ANR 或 OOM，以及是否有 ProGuard/R8 混淆
- 可用的 mapping.txt（说明版本）

## 输出

- 关键堆栈已符号化/反混淆的片段
- 根因分析与复现路径（若可推断），涉及的模块/提交
- 修复建议（优先级/owner）与验证手段或监控指标

## 常见场景

| 场景 | 说明 |
|------|------|
| Java/Kotlin Fatal & Non-fatal | 常规异常崩溃 |
| ANR | 主线程阻塞/输入分发超时 |
| OOM/Watchdog | 结合内存、主线程卡顿线索研判 |

## 操作步骤

### 步骤 1：收集基本信息

从崩溃报告中提取：
- 崩溃类型（Fatal / Non-fatal / ANR）
- 异常类型（NullPointerException / IllegalStateException 等）
- App 版本（versionName + versionCode）
- 确认是否有对应版本的 mapping.txt

### 步骤 2：识别混淆情况

检查堆栈中的类名和方法名：
- **类名是否混淆**：`a.b.c` 是混淆名，`com.example.MainActivity` 是原始名
- **方法名是否混淆**：单字母或非 ASCII 字符（如 `হস`）通常是混淆名

### 步骤 3：提取待解析符号

从崩溃堆栈提取关键帧（通常是 `Caused by` 后的前 3-5 行）：
```
# 示例
at com.example.app.MainActivity.হস(SourceFile:11)  ← 需要解析 হস
at com.example.app.BaseActivity.onCreate(SourceFile:28)
```

每批不超过 5 个符号。

### 步骤 4：Grep 搜索 mapping.txt

根据混淆情况选择搜索策略：

**类名保留，方法名混淆**（最常见）：
```bash
Grep pattern="^com\.example\.app\.MainActivity ->" path=/path/to/mapping.txt -A 50
```

**类名和方法名都混淆**：
```bash
Grep pattern="-> a\.b\.c:$" path=/path/to/mapping.txt -A 50
```

### 步骤 5：还原行号

1. 获取崩溃行号（如 `SourceFile:11`）
2. 在 mapping 结果中找到方法的行号映射
3. 定位混淆行号 11 所在的范围，读取原始行号

### 步骤 6：根因分析

结合还原后的堆栈分析：
- 异常类型的典型原因
- 涉及的生命周期阶段
- 可能的触发路径

### 步骤 7：输出分析报告

按照「输出结构示例」格式输出：
- 基本信息
- 关键堆栈（已符号化）
- 根因分析
- 修复建议
- 验证方案

## 崩溃报告格式识别

### Android 崩溃类型

1. **Java/Kotlin 异常**
   ```
   Fatal Exception: java.lang.NullPointerException
   at com.example.app.MainActivity.onCreate(MainActivity.kt:42)
   ```

2. **ANR (Application Not Responding)**
   ```
   ANR in com.example.app
   PID: 12345
   Reason: Input dispatching timed out
   ```

## Mapping 文件智能解析策略

**重要**：mapping.txt 文件通常非常大（几十MB），**禁止全量读取**。必须采用以下策略：

### 1. 校验版本匹配

- 确认 mapping.txt 来源版本与崩溃日志的 versionCode/versionName 对应
- 版本不匹配时要提示精度受限，改为代码路径推测

### 2. 理解 mapping.txt 格式

mapping.txt 的基本格式：
```
原始完整类名 -> 混淆后类名:
    混淆行号起:混淆行号止:返回类型 原始方法名(参数类型):原始源码行号起:原始源码行号止 -> 混淆方法名
```

> **备注**：行号范围为 `start:end`；若同一方法出现多段（R8 内联优化），按崩溃行号落入的段读取原始行号。

**实际示例**：
```
# 示例 1：仅方法被混淆（类名保留）
com.example.app.MainActivity -> com.example.app.MainActivity:
    java.util.List mTags -> গ
    1:8:void initPresenter():39:39 -> হস
    9:16:void initPresenter():40:40 -> হস
    17:24:void initPresenter():41:41 -> হস

# 示例 2：类名和方法都被混淆
com.foo.feature.DetailActivity -> a.b.c:
    45:60:void onCreate(android.os.Bundle):120:140 -> a
    61:70:void onResume():150:160 -> b
```

**行号映射解读**：
- `1:8:void initPresenter():39:39 -> হস` 表示：
  - 混淆后行号 1-8 → 原始源码第 39 行
  - 原始方法名 `initPresenter()` → 混淆后 `হস`
- `45:60:void onCreate(...):120:140 -> a` 表示：
  - 混淆后行号 45-60 → 原始源码第 120-140 行
- 崩溃报告显示 `SourceFile:11`，找到包含 11 的混淆行号范围（如 9:16），即可定位原始行号

### 3. 识别混淆类型

堆栈中可能出现两种情况：

**情况 A：类名保留，方法名混淆**（常见于 Activity/Fragment/keep 规则）
```
at com.example.app.MainActivity.হস(SourceFile:11)
```
- 类名 `MainActivity` 是原始名
- 方法名 `হস` 是混淆名
- 搜索策略：用原始类名搜索

**情况 B：类名和方法名都混淆**
```
at a.b.c.d(Unknown Source:12)
```
- 类名 `a.b.c` 是混淆名
- 方法名 `d` 是混淆名
- 搜索策略：用混淆类名搜索

### 4. 提取待解析符号

从崩溃堆栈中提取需要反混淆的符号，**每批不超过 5 个**：

```
# 示例堆栈
at com.example.app.MainActivity.হস(SourceFile:11)
at com.example.app.BaseActivity.onCreate(SourceFile:28)

# 提取的符号列表
- 类: com.example.app.MainActivity（原始名）+ 方法: হস（混淆名）
- 类: com.example.app.BaseActivity（原始名）+ 方法: onCreate（可能未混淆）
```

### 5. Grep 精确搜索策略

**只搜索需要的符号**，不要读取整个文件。

#### 情况 A：已知原始类名，查找方法映射

```bash
# 搜索原始类名（获取类块及其方法映射）
Grep pattern="^com\.example\.app\.MainActivity " path=/path/to/mapping.txt -A 50

# 或更精确地搜索类定义行
Grep pattern="^com\.example\.app\.MainActivity ->" path=/path/to/mapping.txt -A 50
```

#### 情况 B：已知混淆类名，查找原始类名

```bash
# 搜索混淆后的类名（注意冒号结尾）
Grep pattern="-> a\.b\.c:$" path=/path/to/mapping.txt -A 50
```

#### 情况 C：已知混淆方法名，在类上下文中查找

```bash
# 带行号与上下文（便于确认所属类）
Grep pattern="-> হস$" path=/path/to/mapping.txt -n -C 5
```

> **说明**：使用 `-n` 显示行号，`-C 5` 显示前后各 5 行上下文，便于确认方法所属的类。如果同名方法出现多次，需结合类名进一步筛选。

### 6. 搜索策略速查表

| 已知信息 | Grep 模式 | 说明 |
|---------|----------|------|
| 原始类名 `MainActivity` | `^.*MainActivity ` 或 `^.*\.MainActivity ->` | 类定义行，空格或箭头结尾 |
| 混淆类名 `a.b.c` | `-> a\.b\.c:$` | 类映射以冒号结尾 |
| 混淆方法名 `হস` | `-> হস$` | 方法映射以混淆名结尾 |
| 原始方法名 `initPresenter` | `initPresenter\(\).*->` | 方法签名包含括号 |

### 7. 行号还原流程

1. 从崩溃堆栈获取混淆行号（如 `SourceFile:11`）
2. 在 mapping 中找到对应方法的行号映射
3. 找到包含该混淆行号的范围（如 `9:16:...`）
4. 读取该行的原始行号（如 `:40:40`）

**示例**：
```
崩溃: MainActivity.হস(SourceFile:11)

mapping.txt:
1:8:void initPresenter():39:39 -> হস    # 混淆行号 1-8 → 原始 39 行
9:16:void initPresenter():40:40 -> হস   # 混淆行号 9-16 → 原始 40 行 ← 11 在此范围
17:24:void initPresenter():41:41 -> হস  # 混淆行号 17-24 → 原始 41 行

结论: SourceFile:11 → 原始 initPresenter() 第 40 行
```

### 8. 注意事项

- **永远不要** 使用 `cat mapping.txt` 或 `Read` 工具读取整个文件
- **优先使用** `Grep` 工具进行精确搜索
- **启用行号**：优先使用 `-n` 参数辅助定位，便于后续精确查找
- **限制上下文**：`-A`/`-B`/`-C` 参数控制在 50 行内；若类方法过多，可分段多次搜索或先按方法名精确匹配后再扩展上下文
- **分批处理**：如果混淆符号很多，分批搜索，每批不超过 5 个
- **内联处理**：遇到 R8 内联导致同一方法有多段行号映射时，崩溃行号可能对应多个原始行号，应全部列出并按调用顺序解释
- **记录结果**：已查找的映射关系在分析报告中记录，便于复查

## 根因分析

常见崩溃原因分类：

| 异常类型 | 常见原因 | 排查方向 |
|---------|---------|---------|
| NullPointerException | 空引用访问 | 检查变量初始化、空值判断 |
| IllegalStateException | 状态不一致 | 检查生命周期、线程安全 |
| OutOfMemoryError | 内存泄漏/大对象 | 检查 Bitmap、集合、监听器 |
| IndexOutOfBoundsException | 数组越界 | 检查集合操作、并发修改 |
| SecurityException | 权限缺失 | 检查运行时权限申请 |
| ANR | 主线程阻塞 | 检查 IO、网络、锁等待 |

## 输出结构示例

```markdown
## 崩溃分析报告

### 基本信息
- **崩溃类型**: ANR（Input dispatch）
- **版本/设备**: app v1.2.3 (versionCode 456)，Android 14，Pixel 7
- **发生频率**: 过去 7 天 1.2k 次，影响 800 用户

### 关键堆栈（已符号化）
```
at com.example.app.DataManager.loadFromDatabase(DataManager.kt:145)
at com.example.app.MainActivity.onCreate(MainActivity.kt:42)
```

### 根因分析
主线程执行了数据库查询操作，导致 Input dispatch 超时。
`DataManager.loadFromDatabase()` 在主线程同步读取大量数据。

### 修复建议
1. 将数据库操作移至后台线程
2. 使用 Room 的 suspend 函数或 Flow
3. 添加主线程监控，埋点卡顿 > 2s

### 验证方案
- 灰度发布观察 ANR rate 下降
- 添加 StrictMode 检测主线程 IO
```

## 常见崩溃模式与解决方案

### 1. 生命周期相关崩溃

**问题**：Activity/Fragment 销毁后访问 View 或 Context
```kotlin
// 错误示例
lifecycleScope.launch {
    delay(5000)
    textView.text = "Updated" // Activity 可能已销毁
}
```

**解决方案**：
```kotlin
// 正确示例
viewLifecycleOwner.lifecycleScope.launch {
    delay(5000)
    textView.text = "Updated"
}
```

### 2. 空指针异常

**问题**：未检查可空类型
```kotlin
// 错误示例
val user = getUser()
textView.text = user.name // user 可能为 null
```

**解决方案**：
```kotlin
// 正确示例
val user = getUser()
textView.text = user?.name ?: "Unknown"
```

### 3. 并发修改异常

**问题**：遍历集合时修改
```kotlin
// 错误示例
for (item in list) {
    if (condition) list.remove(item)
}
```

**解决方案**：
```kotlin
// 正确示例
list.removeAll { condition }
// 或使用 Iterator
val iterator = list.iterator()
while (iterator.hasNext()) {
    if (condition) iterator.remove()
}
```

### 4. ANR 问题

**问题**：主线程执行耗时操作

**解决方案**：
```kotlin
// 将耗时操作移到后台线程
viewModelScope.launch(Dispatchers.IO) {
    val result = heavyOperation()
    withContext(Dispatchers.Main) {
        updateUI(result)
    }
}
```

## 参考资源

- [Firebase Crashlytics 官方文档](https://firebase.google.com/docs/crashlytics)
- [Android 崩溃分析指南](https://developer.android.com/topic/performance/vitals/crash)
- references/android-exceptions.md - Android 常见异常详解
- references/anr-analysis.md - ANR 分析指南