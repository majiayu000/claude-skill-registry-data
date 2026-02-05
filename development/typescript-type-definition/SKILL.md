---
name: TypeScript Type Definition
description: 生成和管理 TypeScript 类型定义，确保类型安全
tags: [typescript, types, interface]
---

# TypeScript Type Definition Skill

自动生成和管理 TypeScript 类型定义。

## 何时使用

处理以下场景时自动激活：
- 定义数据结构类型
- API 响应类型
- 组件 Props 类型
- Supabase 数据库类型
- 工具函数类型

## 项目类型结构

### 类型文件位置
```
src/
├── types/
│   ├── database.ts      # Supabase 数据库类型
│   ├── report.ts        # 报告相关类型
│   ├── student.ts       # 学生相关类型
│   ├── exam.ts          # 考试相关类型
│   └── common.ts        # 通用类型
├── integrations/
│   └── supabase/
│       └── types.ts     # Supabase 自动生成类型
```

## 类型定义规范

### 基础接口
```typescript
// 使用 interface 定义对象结构
export interface Student {
  id: string;
  student_id: string;
  name: string;
  class_id?: string;
  created_at: string;
}

// 使用 type 定义联合类型或复杂类型
export type UserRole = 'admin' | 'teacher' | 'student';
export type ExamType = 'midterm' | 'final' | 'quiz' | 'homework';
```

### API 响应类型
```typescript
// API 成功响应
export interface ApiResponse<T> {
  data: T;
  success: boolean;
  message?: string;
}

// API 错误响应
export interface ApiError {
  error: string;
  code?: string;
  details?: unknown;
}

// 使用示例
export type StudentResponse = ApiResponse<Student[]>;
```

### 组件 Props 类型
```typescript
// 基础 Props
export interface ComponentProps {
  className?: string;
  children?: React.ReactNode;
}

// 扩展 Props
export interface StudentCardProps extends ComponentProps {
  student: Student;
  onEdit?: (student: Student) => void;
  onDelete?: (id: string) => void;
}
```

### 表单数据类型
```typescript
// 输入表单
export interface StudentFormData {
  student_id: string;
  name: string;
  class_id: string;
  contact_email?: string;
}

// 与数据库类型转换
export type StudentInput = Omit<Student, 'id' | 'created_at'>;
export type StudentUpdate = Partial<StudentInput>;
```

### 枚举类型
```typescript
// 使用 const enum 提高性能
export const enum ExamStatus {
  Draft = 'draft',
  Published = 'published',
  Completed = 'completed',
  Archived = 'archived',
}

// 或使用 const object + type
export const GRADE_LEVELS = {
  A: 'A',
  B: 'B',
  C: 'C',
  D: 'D',
  E: 'E',
} as const;

export type GradeLevel = typeof GRADE_LEVELS[keyof typeof GRADE_LEVELS];
```

## Supabase 类型生成

### 自动生成数据库类型
```bash
# 生成 Supabase 类型
npx supabase gen types typescript --project-id giluhqotfjpmofowvogn > src/integrations/supabase/types.ts
```

### 使用 Supabase 类型
```typescript
import { Database } from '@/integrations/supabase/types';

// 提取表类型
export type Student = Database['public']['Tables']['students']['Row'];
export type StudentInsert = Database['public']['Tables']['students']['Insert'];
export type StudentUpdate = Database['public']['Tables']['students']['Update'];
```

## 实用工具类型

### 常用工具类型
```typescript
// 可选字段
export type Optional<T, K extends keyof T> = Omit<T, K> & Partial<Pick<T, K>>;

// 必需字段
export type Required<T, K extends keyof T> = Omit<T, K> & Required<Pick<T, K>>;

// 只读
export type DeepReadonly<T> = {
  readonly [P in keyof T]: T[P] extends object ? DeepReadonly<T[P]> : T[P];
};

// 提取数组元素类型
export type ArrayElement<T> = T extends (infer E)[] ? E : never;
```

### 项目特定工具类型
```typescript
// 分页响应
export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  pageSize: number;
  hasMore: boolean;
}

// 排序参数
export interface SortOptions {
  field: string;
  direction: 'asc' | 'desc';
}

// 过滤参数
export interface FilterOptions {
  [key: string]: string | number | boolean | null;
}
```

## 类型守卫

### 实现类型守卫
```typescript
// 基础类型守卫
export function isStudent(obj: unknown): obj is Student {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    'id' in obj &&
    'name' in obj &&
    'student_id' in obj
  );
}

// 数组类型守卫
export function isStudentArray(arr: unknown): arr is Student[] {
  return Array.isArray(arr) && arr.every(isStudent);
}

// 联合类型窄化
export function isAdminRole(role: UserRole): role is 'admin' {
  return role === 'admin';
}
```

## 泛型使用

### 泛型函数
```typescript
// API 请求泛型
export async function fetchData<T>(url: string): Promise<T> {
  const response = await fetch(url);
  return response.json() as Promise<T>;
}

// 使用
const students = await fetchData<Student[]>('/api/students');
```

### 泛型组件 Props
```typescript
export interface SelectProps<T> {
  options: T[];
  value: T;
  onChange: (value: T) => void;
  getLabel: (item: T) => string;
  getValue: (item: T) => string;
}

export function Select<T>({ options, value, onChange, getLabel, getValue }: SelectProps<T>) {
  // 组件实现
}
```

## 最佳实践

1. **优先使用 interface**: 对象结构使用 interface，联合类型使用 type
2. **避免 any**: 使用 unknown 代替 any，然后进行类型守卫
3. **导出类型**: 所有公共类型都应该导出
4. **类型复用**: 使用工具类型避免重复定义
5. **文档注释**: 复杂类型添加 JSDoc 注释

## 示例：完整类型定义文件

```typescript
/**
 * 📊 成绩相关类型定义
 */

import { Database } from '@/integrations/supabase/types';

// 基础类型
export type GradeData = Database['public']['Tables']['grade_data']['Row'];
export type GradeDataInsert = Database['public']['Tables']['grade_data']['Insert'];

// 科目类型
export const SUBJECTS = ['chinese', 'math', 'english', 'physics', 'chemistry'] as const;
export type Subject = typeof SUBJECTS[number];

// 成绩统计
export interface GradeStatistics {
  average: number;
  median: number;
  max: number;
  min: number;
  standardDeviation: number;
}

// 学生成绩概览
export interface StudentGradeOverview {
  student_id: string;
  student_name: string;
  grades: Record<Subject, number>;
  total_score: number;
  rank_in_class: number;
}

// API 响应
export type GradeListResponse = ApiResponse<GradeData[]>;
export type GradeStatisticsResponse = ApiResponse<GradeStatistics>;

// 类型守卫
export function isValidSubject(subject: string): subject is Subject {
  return SUBJECTS.includes(subject as Subject);
}
```

## 注意事项

- 定期运行 `npm run typecheck` 检查类型错误
- 使用 `strict` 模式确保类型安全
- 避免过度使用类型断言（as）
- 复杂类型拆分为多个小类型
