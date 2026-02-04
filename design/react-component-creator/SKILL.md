---
name: React Component Creator
description: 创建符合项目规范的 React 组件，应用 Positivus 设计系统
tags: [react, typescript, ui, component]
---

# React Component Creator

自动创建符合项目规范的 React + TypeScript 组件。

## 何时使用

当需要创建新的 React 组件时自动激活，包括：
- UI 组件
- 页面组件
- 布局组件
- 功能组件

## 项目规范

### 设计系统 - Positivus Brand
- **主色调**: `#B9FF66` (亮绿色)
- **背景色**: `#191A23` (深黑色)
- **边框**: 2px solid black
- **阴影**: `shadow-[4px_4px_0px_0px_#191A23]` (卡片)
- **阴影**: `shadow-[2px_2px_0px_0px_#000]` (按钮)
- **字体**: font-black (标题), font-bold (按钮/强调)

### 组件结构
```tsx
/**
 * 📝 组件名称
 * 简短描述
 */

import React from "react";
import { cn } from "@/lib/utils";

interface ComponentNameProps {
  // 属性定义
}

const ComponentName: React.FC<ComponentNameProps> = ({
  // 解构 props
}) => {
  return (
    <div className="positivus-style">
      {/* 组件内容 */}
    </div>
  );
};

export default ComponentName;
```

### 常用 UI 组件
- **shadcn/ui**: 使用 `@/components/ui/*` 组件
- **Icons**: 使用 `lucide-react`
- **Toast**: 使用 `sonner` 的 `toast` 函数
- **样式**: 使用 Tailwind CSS + `cn()` 工具函数

### 按钮样式
```tsx
<Button
  variant="outline"
  className="border-2 border-black shadow-[2px_2px_0px_0px_#000] hover:shadow-[3px_3px_0px_0px_#000] hover:bg-[#B9FF66] transition-all duration-200 font-bold"
>
  按钮文本
</Button>
```

### 卡片样式
```tsx
<Card className="border-2 border-black shadow-[4px_4px_0px_0px_#191A23]">
  <CardHeader className="bg-[#B9FF66] border-b-2 border-black">
    <CardTitle>卡片标题</CardTitle>
  </CardHeader>
  <CardContent className="p-6">
    内容
  </CardContent>
</Card>
```

### Badge 样式
```tsx
<Badge className="bg-[#B9FF66] text-[#191A23] border-2 border-black">
  标签
</Badge>
```

## 文件位置

- **UI 组件**: `src/components/ui/`
- **业务组件**: `src/components/{domain}/`
- **页面组件**: `src/pages/`
- **布局组件**: `src/components/layout/`

## 最佳实践

1. **类型安全**: 所有 props 使用 TypeScript 接口定义
2. **可访问性**: 使用语义化 HTML，添加 aria 属性
3. **响应式**: 使用 Tailwind 响应式类 (sm:, md:, lg:)
4. **性能**: 大列表使用 React.memo 或 useMemo
5. **状态管理**: 优先使用 React hooks (useState, useEffect)

## 示例

### 创建功能卡片组件
```tsx
/**
 * 🎯 功能卡片
 * 显示单个功能的卡片，带图标和描述
 */

import React from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { LucideIcon } from "lucide-react";
import { cn } from "@/lib/utils";

interface FeatureCardProps {
  icon: LucideIcon;
  title: string;
  description: string;
  className?: string;
}

const FeatureCard: React.FC<FeatureCardProps> = ({
  icon: Icon,
  title,
  description,
  className,
}) => {
  return (
    <Card className={cn(
      "border-2 border-black shadow-[4px_4px_0px_0px_#191A23] hover:shadow-[6px_6px_0px_0px_#191A23] transition-all duration-200",
      className
    )}>
      <CardHeader className="bg-[#B9FF66] border-b-2 border-black">
        <CardTitle className="flex items-center gap-2">
          <Icon className="h-5 w-5" />
          {title}
        </CardTitle>
      </CardHeader>
      <CardContent className="p-6">
        <p className="text-gray-700">{description}</p>
      </CardContent>
    </Card>
  );
};

export default FeatureCard;
```

## 注意事项

- 始终使用 TypeScript
- 遵循 Positivus 设计规范
- 确保组件可复用性
- 添加适当的注释和文档
