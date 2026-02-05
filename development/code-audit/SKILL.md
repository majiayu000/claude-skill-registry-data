---
name: code-audit
description: 全面审查代码质量、架构设计和开发规范。检查 Next.js/Server Actions 最佳实践、代码重复、逻辑清晰度、文档完整性、第三方库更新状态、低效方法。用于代码审查、质量提升、重构规划、新人上手理解代码。
allowed-tools: Read, Grep, Glob, Bash, WebSearch
---

# 代码质量审查 Code Audit

## 目标
全面提升代码质量、开发效率和可维护性，帮助团队快速理解和维护代码库。

## 审查维度

### 1. Next.js 和 Server Actions 最佳实践
检查是否充分利用 Next.js 15 和 Server Actions 特性：
- ✅ Server Actions 替代传统 API 路由（**仅限非流式场景**）
- ✅ 使用 `'use server'` 指令
- ✅ 避免在 Server Actions 中使用客户端 API
- ✅ 合理使用 `revalidatePath` 和 `revalidateTag`
- ✅ Server Components vs Client Components 选择正确
- ✅ 避免不必要的 `'use client'`
- ✅ 利用流式渲染和 Suspense
- ✅ 使用 Server Actions 进行表单提交
- ❌ 避免：API 路由做简单 CRUD（应用 Server Actions）
- ❌ 避免：在服务端组件中使用 useState、useEffect
- ⚠️ **保留 Route Handler 的场景**：
  - 流式响应（SSE/ReadableStream）如 AI 生成
  - 大文件上传/下载
  - Webhooks 回调
  - 需要自定义 Response Headers 的场景

### 2. 代码重复和复用性
识别需要抽离复用的代码：
- 查找重复的业务逻辑（相似度 > 70%）
- 检查是否有重复的数据验证逻辑（应使用 Zod schemas）
- 识别重复的 UI 组件（应抽离到 components/）
- 检查重复的数据库查询（应抽离到 lib/db）
- 查找重复的错误处理模式
- 检查是否有工具函数可以复用

### 3. 代码逻辑和结构清晰度
评估代码可读性和维护性：
- 函数职责单一性（是否做太多事）
- 变量命名是否清晰表意
- 逻辑嵌套深度（超过 3 层需要重构）
- 文件长度（超过 600 行需要拆分）
- 函数长度（超过 150 行需要拆分）
- 是否有魔法数字或硬编码值
- 类型定义是否完整（公共 API 和核心业务逻辑应避免 any，临时转换和复杂第三方库返回值可酌情使用）
- 导入语句是否有序分组

### 4. 文档和注释
检查复杂功能的文档完整性：
- 复杂业务逻辑是否有 README 或注释
- 关键算法是否有说明
- API 接口是否有 JSDoc
- 复杂的状态管理是否有文档
- 非显而易见的 hack 是否有解释
- 项目结构是否有说明文档

### 5. 第三方库和技术栈
检查依赖是否最新和合理：
- 查找过时的依赖包（检查 package.json）
- 检查是否使用过时的 API（如 React 旧生命周期）
- 评估库的选择是否合理（是否有更好的替代）

### 6. 性能和效率
识别低效的实现方法：
- 不必要的重复渲染
- 缺少 useMemo、useCallback 的计算密集操作
- 数据库查询 N+1 问题
- 未优化的图片加载
- 大型列表未使用虚拟滚动
- 同步操作阻塞主线程
- 未使用的导入和死代码

### 7. 类型安全和错误处理
检查健壮性：
- TypeScript 类型覆盖率
- 是否有足够的错误处理
- 边界情况是否考虑
- 用户输入是否验证
- API 调用是否有错误处理

### 8. 前端组件一致性
确保 UI 和交互模式统一：
- **UI 组件使用一致性**：
  - 按钮：是否统一使用 shadcn/ui `<Button>`
  - 表单：是否统一使用 react-hook-form + Zod
  - 对话框：是否统一使用 `<Dialog>` 或 `<AlertDialog>`
  - 输入框：是否统一使用 `<Input>` / `<Textarea>`
- **样式模式一致性**：
  - Tailwind 类名使用模式（如间距、颜色）
  - 响应式断点使用一致（sm/md/lg/xl）
  - 布局模式（flex/grid）使用规范
- **状态管理一致性**：
  - 全局状态：是否统一使用 zustand
  - 表单状态：是否统一使用 react-hook-form
  - 服务端状态：避免重复的 useState + useEffect 获取数据
- **用户反馈一致性**：
  - 成功/错误提示：是否统一使用 sonner toast
  - 加载状态：Loading spinner 或 skeleton 是否一致
  - 错误处理：错误边界和错误展示是否统一
- **交互模式一致性**：
  - 删除操作：是否都有确认对话框
  - 表单提交：是否都显示 loading 状态
  - 数据刷新：是否使用一致的刷新机制

### 9. 无效逻辑和业务代码质量
清理冗余代码，优化业务逻辑：
- **无效代码检测**：
  - 永远不会执行的代码（unreachable code）
  - 未使用的函数、变量、类型定义
  - 未使用的导入（import）
  - 注释掉的大段代码块（超过 10 行）
  - TODO/FIXME 注释从未处理
- **无效逻辑检测**：
  - 永远为 true/false 的条件判断
  - 重复的 if 条件
  - 空的 try-catch 块
  - 空的函数或组件
  - 无用的三元表达式（`condition ? true : false`）
- **业务代码质量**：
  - 业务逻辑是否误放在前端组件（应该在 Server Actions）
  - 硬编码的业务规则（应该用配置或常量）
  - 业务流程是否清晰（复杂流程缺少状态机或流程图）
  - 关键业务逻辑是否有注释说明
  - 业务验证逻辑是否使用 Zod schemas
  - 是否有过时的业务逻辑（功能已废弃但代码未删除）

## 使用方式

### 方式 1: 审查单个文件
```
请用 /code-audit 审查 actions/delivery.ts
```

### 方式 2: 审查整个功能模块
```
请用 /code-audit 审查投放管理相关的所有文件
```

### 方式 3: 审查最近的改动
```
请用 /code-audit 审查我最近修改的文件
```

### 方式 4: 全项目扫描
```
请用 /code-audit 对整个项目做一次全面审查
```

## 审查流程

当用户调用此 Skill 时，按以下步骤执行：

### 步骤 1: 确定审查范围
- 如果用户指定了文件/目录，直接使用
- 如果用户说"最近的改动"，运行 `git diff --name-only HEAD~1`
- 如果用户说"整个项目"，使用 Glob 扫描所有 `.ts` 和 `.tsx` 文件
- 如果用户说某个功能模块，使用 Grep 查找相关文件

### 步骤 2: 收集项目规范
- 读取 `/Users/v/Desktop/code/xhs_ad_agent/Claude.md` 了解项目规范
- 检查 `package.json` 了解依赖版本
- 检查 `tsconfig.json` 了解 TypeScript 配置

### 步骤 3: 逐文件分析
对每个文件执行：

1. **读取文件内容** (使用 Read 工具)

2. **Next.js 最佳实践检查**:
   - 是否有 API 路由应该改用 Server Actions（排除流式、文件处理、Webhooks）
   - Server Components 是否误用了客户端 hooks
   - 是否正确使用 `revalidatePath`
   - Route Handler 的使用是否合理（流式响应必须用 Route Handler）

3. **代码重复检查**:
   - 在项目中搜索相似的代码片段
   - 标记可以抽离的公共逻辑

4. **结构清晰度检查**:
   - 计算函数行数、嵌套深度
   - 检查变量命名质量
   - 评估文件组织结构

5. **文档检查**:
   - 复杂函数是否有注释
   - 业务逻辑是否清晰

6. **性能检查**:
   - 查找潜在的性能问题
   - 识别可优化的代码

7. **类型安全检查**:
   - 检查公共 API 和函数签名是否滥用 `any`（临时转换、复杂第三方库返回值可接受）
   - 检查错误处理

8. **前端组件一致性检查**（针对 .tsx 组件文件）:
   - UI 组件是否统一使用 shadcn/ui（Button、Input、Dialog 等）
   - 表单是否统一使用 react-hook-form
   - Toast 通知是否统一使用 sonner
   - 状态管理模式是否一致
   - 加载和错误状态展示是否统一

9. **无效逻辑检测**:
   - 查找未使用的导入（import）
   - 检测注释掉的代码块
   - 检查 TODO/FIXME 标记
   - 业务逻辑是否误放在组件中（应该在 Server Actions）
   - 硬编码的业务规则

### 步骤 4: 依赖检查
- 使用 Bash 运行 `pnpm outdated` 查找过时依赖
- 使用 WebSearch 查询关键依赖的最新最佳实践

### 步骤 5: 生成审查报告

以结构化 Markdown 格式输出：

```markdown
# 代码审查报告

## 📊 总体评分
- Next.js 最佳实践: ⭐⭐⭐⭐ (8/10)
- 代码复用性: ⭐⭐⭐ (6/10)
- 代码清晰度: ⭐⭐⭐⭐ (7/10)
- 文档完整性: ⭐⭐ (4/10)
- 依赖更新度: ⭐⭐⭐⭐ (8/10)
- 性能优化: ⭐⭐⭐ (6/10)
- 组件一致性: ⭐⭐⭐ (6/10)
- 代码整洁度: ⭐⭐⭐⭐ (7/10)

## 🔴 严重问题 (需要立即修复)

### 1. actions/delivery.ts:145-180
**问题**: 大量重复的投放状态检查逻辑
**影响**: 维护困难，容易出现不一致
**建议**: 抽离到 `lib/utils/delivery-status.ts`
```typescript
// 建议创建
export function validateDeliveryStatus(status: DeliveryStatus) {
  // 统一的状态验证逻辑
}
```

### 2. components/works/WorkList.tsx:89
**问题**: 使用 'use client' 但实际可以是 Server Component
**影响**: 增加客户端 bundle 大小，降低性能
**建议**: 移除 'use client'，将交互逻辑抽离到子组件

### 3. components/accounts/AccountForm.tsx:45-120
**问题**: 业务逻辑直接写在组件中，未使用 Server Actions
**影响**: 难以复用，测试困难，违反项目规范
**建议**: 将业务逻辑抽离到 actions/account.ts
```typescript
// 应该创建
'use server'
export async function updateAccountSettings(data: AccountSettings) {
  // 业务逻辑
}
```

## 🟡 中等问题 (建议优化)

### 1. actions/account.ts:230-280
**问题**: 函数过长 (50+ 行)，职责不单一
**建议**: 拆分为多个小函数

### 2. 组件一致性问题
**问题**: 发现 3 处使用了不一致的 UI 组件
- `components/works/DeleteButton.tsx:12` - 自定义按钮而非 shadcn/ui Button
- `app/(dashboard)/leads/page.tsx:89` - 使用原生 `<button>` 而非 `<Button>`
- `components/image/UploadDialog.tsx:34` - 自定义 Dialog 样式
**建议**: 统一使用 shadcn/ui 组件保持一致性

### 3. 无效代码清理
**问题**: 发现多处无效代码
- `lib/utils/deprecated.ts:全文` - 整个文件已废弃但未删除
- `actions/creation.ts:245-267` - 注释掉的代码块 (23 行)
- `components/layout/Header.tsx:12,34,56` - 3 处 console.log 调试语句
**建议**: 立即删除无效代码，保持代码库整洁

## 🟢 低优先级建议

### 1. 依赖更新
- `next`: 15.5.7 → 15.6.0 (最新版本)
- `react`: 19.0.0 ✅ (已是最新)
- `@anthropic-ai/sdk`: 0.71.2 → 0.72.0

### 2. 代码风格
- 建议使用 Prettier 统一代码格式
- 考虑添加 ESLint 规则检查未使用的导入

## 💡 最佳实践建议

1. **Server Actions 重构**
   - 将 `app/api/creation/stream/route.ts` 改为 Server Action
   - 示例代码：
   ```typescript
   // actions/creation.ts
   'use server'
   export async function generateCreation(params: CreationParams) {
     // ...
   }
   ```

2. **抽离公共逻辑**
   - 创建 `lib/validators/` 存放 Zod schemas
   - 创建 `lib/constants/` 存放常量定义

3. **添加文档**
   - 为 `actions/delivery.ts` 添加 README
   - 说明投放状态机和业务流程

4. **性能优化**
   - 图片使用 Next.js Image 组件
   - 大列表使用虚拟滚动

## 📝 需要添加文档的模块
- [ ] 投放管理流程 (actions/delivery.ts)
- [ ] 创作生成逻辑 (actions/creation.ts)
- [ ] 小红书 API 集成 (lib/xhs/)

## 🎯 下一步行动建议
1. 立即处理 2 个严重问题
2. 本周处理 5 个中等问题
3. 计划重构会议讨论架构优化
4. 为核心模块补充文档
```

## 特殊检查项（针对此项目）

基于项目的 `Claude.md` 规范：
- **必须使用 Server Actions**: 检查是否有新的 API 路由应该用 Server Actions
- **代码简洁性**: Next.js 15 特性是否充分利用

## 输出格式要求

1. **使用 Markdown 表格**展示问题清单
2. **包含文件路径和行号**，方便定位
3. **给出具体的代码示例**，而非空泛建议
4. **按优先级排序**问题
5. **总结可量化的改进指标**

## 示例对话

**用户**: "用 /code-audit 审查 actions/delivery.ts"

**助手**:
1. 读取 `actions/delivery.ts`
2. 读取 `Claude.md` 了解项目规范
3. 分析文件中的代码模式
4. 在项目中搜索类似代码片段
5. 生成详细的审查报告，包含：
   - 具体问题和行号
   - 重复代码位置
   - 优化建议和示例代码
   - 是否符合 Next.js 最佳实践

---

**用户**: "全面审查整个项目"

**助手**:
1. 扫描所有 `.ts` 和 `.tsx` 文件
2. 运行 `pnpm outdated` 检查依赖
3. 分析每个核心模块
4. 生成综合报告，包含：
   - 项目整体健康度评分
   - Top 10 需要改进的问题
   - 依赖更新建议
   - 架构优化方向
   - 文档缺失清单

## 注意事项

- 审查时考虑项目的实际业务场景，避免过度工程
- 给出的建议要具体可操作，附带代码示例
- 识别技术债务时，要评估修复的收益和成本
- 尊重现有的代码风格，除非明显不合理
- 对于复杂的重构建议，先与团队讨论再执行
