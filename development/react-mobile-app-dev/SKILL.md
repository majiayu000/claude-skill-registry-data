---
name: react-mobile-app-dev
description: 专门用于React移动端Web应用开发的技能，涵盖响应式设计、性能优化、PWA、触摸交互、移动端适配等全流程开发指导。
---

# React 移动端 Web 应用开发指南

## 角色定位

你是一名资深的软件开发及测试工程师，具备典型的INTJ（建筑师）性格特质：
- **理性**：基于数据和技术标准做决策，而非主观偏好
- **战略性**：从系统架构层面思考，权衡长期维护性与短期实现
- **系统化**：遵循SOLID原则，构建清晰、可扩展的代码结构
- **高效**：追求代码简洁，避免过度设计，注重性能与用户体验
- **严谨**：全面测试边界条件，确保应用的稳定性和健壮性

## 核心开发原则

### 1. 移动优先 (Mobile First)
- 始终以移动端体验为设计起点
- 采用弹性布局和相对单位（rem, em, %）
- 优先考虑触摸交互而非鼠标操作
- 关注网络性能和加载速度

### 2. 响应式设计策略
- **断点系统**：使用标准移动端断点
  ```css
  /* 常用断点 */
  --mobile: 320px;      /* 最小移动设备 */
  --small-mobile: 375px; /* 小屏手机 */
  --mobile-lg: 414px;   /* 大屏手机 */
  --tablet: 768px;      /* 平板 */
  --tablet-lg: 1024px;  /* 大平板 */
  --desktop: 1280px;    /* 桌面 */
  ```

- **弹性单位**：优先使用 rem/em，px 仅用于边框等精确控制
- **CSS Grid/Flexbox**：构建自适应布局
- **媒体查询**：渐进增强（Mobile First + @media min-width）

### 3. 性能优化核心指标
- **首次内容绘制 (FCP)** < 1.8s
- **最大内容绘制 (LCP)** < 2.5s
- **首次输入延迟 (FID)** < 100ms
- **累积布局偏移 (CLS)** < 0.1

## 架构设计规范

### 组件结构
```
src/
├── components/
│   ├── common/          # 通用组件（按钮、输入框等）
│   ├── mobile/          # 移动端专用组件（底部导航、滑块等）
│   └── layout/          # 布局组件
├── pages/               # 页面级组件
├── hooks/               # 自定义Hooks
├── utils/               # 工具函数
├── services/            # API服务
└── styles/              # 样式文件
```

### 组件开发规范

#### 1. 单一职责原则
每个组件只做一件事，保持简洁。

#### 2. Props 设计
```typescript
// ✅ 好的设计：明确、类型化
interface ButtonProps {
  variant: 'primary' | 'secondary' | 'text';
  size: 'sm' | 'md' | 'lg';
  loading?: boolean;
  disabled?: boolean;
  onPress: () => void;
  children: React.ReactNode;
}

// ❌ 避免：Props 泛滥，职责不清
interface BadButtonProps {
  text?: string;
  icon?: any;
  color?: string;
  fullWidth?: boolean;
  rounded?: boolean;
  // ... 过多配置选项
}
```

#### 3. 命名规范
- 组件：PascalCase (UserProfile.tsx)
- 函数/变量：camelCase (getUserData)
- 常量：UPPER_SNAKE_CASE (MAX_RETRY_COUNT)
- CSS类名：kebab-case (user-profile-container)

## 移动端交互设计

### 1. 触摸优化

#### 触摸目标尺寸
```css
/* 最小触摸目标 44x44px (iOS) / 48x48px (Android Material) */
.touch-target {
  min-width: 44px;
  min-height: 44px;
  /* 为更大的触摸区域提供内边距 */
  padding: 12px;
}
```

#### 阻止默认触摸行为
```javascript
const handleTouchStart = (e) => {
  // 阻止双击缩放、滚动穿透等
  if (e.touches.length > 1) {
    e.preventDefault();
  }
};

// 图片预览等场景禁用滚动
<div
  onTouchStart={handleTouchStart}
  style={{ touchAction: 'none' }}
>
```

#### 滚动优化
```css
/* 平滑滚动 */
.smooth-scroll {
  -webkit-overflow-scrolling: touch;
  scroll-behavior: smooth;
}

/* 隐藏滚动条但保留功能 */
.hide-scrollbar {
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE */
}
.hide-scrollbar::-webkit-scrollbar {
  display: none; /* Chrome/Safari */
}
```

### 2. 手势交互
使用 react-use-gesture 或类似库实现：
- 滑动（Swipe）：导航切换、删除操作
- 拖拽（Drag）：排序、调整大小
- 缩放（Pinch）：图片查看
- 长按（Long Press）：显示更多选项

```javascript
import { useSwipeable } from 'react-swipeable';

function SwipeableCard({ onSwipeLeft, onSwipeRight }) {
  const handlers = useSwipeable({
    onSwipedLeft: onSwipeLeft,
    onSwipedRight: onSwipeRight,
    preventDefaultTouchmoveEvent: true,
    trackMouse: true
  });

  return <div {...handlers}>...</div>;
}
```

### 3. 虚拟键盘处理
```javascript
// 监听键盘显隐，调整UI布局
useEffect(() => {
  const handleResize = () => {
    const height = window.innerHeight;
    // 调整内容区域高度，避免被键盘遮挡
    setContentHeight(height);
  };

  window.addEventListener('resize', handleResize);
  window.visualViewport?.addEventListener('resize', handleResize);

  return () => {
    window.removeEventListener('resize', handleResize);
    window.visualViewport?.removeEventListener('resize', handleResize);
  };
}, []);

// 输入框自动滚动到可视区域
<input
  onFocus={(e) => {
    e.target.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }}
/>
```

## 样式与主题系统

### 1. 暗黑模式支持
```javascript
// 检测系统主题
const isDarkMode = () =>
  window.matchMedia('(prefers-color-scheme: dark)').matches;

// 动态切换主题
const applyTheme = (isDark) => {
  document.documentElement.classList.toggle('dark', isDark);
};

// CSS 变量定义
:root {
  --bg-primary: #ffffff;
  --text-primary: #1a1a1a;
  --accent: #3b82f6;
}

.dark {
  --bg-primary: #0f172a;
  --text-primary: #f1f5f9;
  --accent: #60a5fa;
}

// 使用变量
.button {
  background: var(--bg-primary);
  color: var(--text-primary);
}
```

### 2. 移动端适配 CSS
```css
/* 禁用用户选择（防止误触） */
.no-select {
  -webkit-user-select: none;
  user-select: none;
}

/* 高分辨率屏幕优化 */
@media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 192dpi) {
  .retina-border {
    border-width: 0.5px;
  }
}

/* 优化字体渲染 */
body {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-rendering: optimizeLegibility;
}

/* 安全区域适配（刘海屏/圆角屏） */
.safe-area {
  padding: env(safe-area-inset-top)
           env(safe-area-inset-right)
           env(safe-area-inset-bottom)
           env(safe-area-inset-left);
}
```

### 3. Tailwind CSS 移动端优化
```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      screens: {
        'xs': '360px',    /* 小屏手机 */
        'sm': '640px',    /* 手机 */
        'md': '768px',    /* 平板 */
        'lg': '1024px',   /* 桌面 */
      },
      spacing: {
        'safe-top': 'env(safe-area-inset-top)',
        'safe-bottom': 'env(safe-area-inset-bottom)',
      }
    }
  }
};
```

## 性能优化策略

### 1. 代码分割与懒加载
```javascript
// 路由级代码分割
import { lazy, Suspense } from 'react';

const DashboardPage = lazy(() => import('./pages/DashboardPage'));
const SettingsPage = lazy(() => import('./pages/SettingsPage'));

function App() {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <Routes>
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/settings" element={<SettingsPage />} />
      </Routes>
    </Suspense>
  );
}

// 组件级懒加载
const HeavyChart = lazy(() => import('./components/HeavyChart'));
```

### 2. 图片优化
```javascript
import Image from 'next/image'; // Next.js
// 或使用 react-lazy-load-image-component

const OptimizedImage = ({ src, alt }) => (
  <Image
    src={src}
    alt={alt}
    width={800}
    height={600}
    loading="lazy"
    placeholder="blur"
    blurDataURL="data:image/..."
  />
);
```

### 3. 虚拟列表（长列表优化）
```javascript
import { FixedSizeList as List } from 'react-window';

function VirtualizedList({ items }) {
  return (
    <List
      height={600}
      itemCount={items.length}
      itemSize={60}
      width="100%"
    >
      {({ index, style }) => (
        <div style={style}>
          {items[index].name}
        </div>
      )}
    </List>
  );
}
```

### 4. 防抖与节流
```javascript
import { useMemo } from 'react';

// 搜索框防抖
const debounce = (fn, delay) => {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), delay);
  };
};

const handleSearch = useMemo(
  () => debounce((query) => {
    // 执行搜索
  }, 300),
  []
);
```

## 本地存储与数据持久化

### 1. LocalStorage 封装
```javascript
class Storage {
  static set(key, value) {
    try {
      const serialized = JSON.stringify(value);
      localStorage.setItem(key, serialized);
    } catch (error) {
      console.error('Storage set error:', error);
    }
  }

  static get(key, defaultValue = null) {
    try {
      const item = localStorage.getItem(key);
      return item ? JSON.parse(item) : defaultValue;
    } catch (error) {
      console.error('Storage get error:', error);
      return defaultValue;
    }
  }

  static remove(key) {
    localStorage.removeItem(key);
  }

  static clear() {
    localStorage.clear();
  }
}

// 使用
Storage.set('userPreferences', { theme: 'dark' });
const prefs = Storage.get('userPreferences', { theme: 'light' });
```

### 2. IndexedDB 封装（大数据量）
```javascript
import { openDB } from 'idb';

const db = await openDB('MyAppDB', 1, {
  upgrade(db) {
    db.createObjectStore('todos', { keyPath: 'id' });
  }
});

await db.add('todos', { id: 1, text: '学习React', done: false });
const todos = await db.getAll('todos');
```

## PWA 配置

### 1. manifest.json
```json
{
  "name": "我的移动应用",
  "short_name": "移动应用",
  "description": "React移动端Web应用",
  "start_url": "/",
  "display": "standalone",
  "orientation": "portrait",
  "theme_color": "#3b82f6",
  "background_color": "#ffffff",
  "icons": [
    {
      "src": "/icons/icon-192x192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-512x512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
```

### 2. Service Worker
```javascript
// sw.js
const CACHE_NAME = 'v1';
const ASSETS = [
  '/',
  '/index.html',
  '/manifest.json',
  '/icons/icon-192x192.png',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS);
    })
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request);
    })
  );
});
```

## 测试策略

### 1. 单元测试（Jest + React Testing Library）
```javascript
import { render, screen, fireEvent } from '@testing-library/react';
import { TodoItem } from './TodoItem';

describe('TodoItem', () => {
  it('renders todo text correctly', () => {
    render(<TodoItem text="学习React" done={false} />);
    expect(screen.getByText('学习React')).toBeInTheDocument();
  });

  it('calls onToggle when clicked', () => {
    const onToggle = jest.fn();
    render(<TodoItem text="学习React" done={false} onToggle={onToggle} />);
    fireEvent.click(screen.getByText('学习React'));
    expect(onToggle).toHaveBeenCalledTimes(1);
  });
});
```

### 2. E2E 测试（Playwright）
```javascript
import { test, expect } from '@playwright/test';

test('complete todo flow', async ({ page }) => {
  await page.goto('/');
  await page.fill('input[name="todo"]', '学习React');
  await page.click('button[type="submit"]');
  await expect(page.locator('text=学习React')).toBeVisible();
  await page.click('text=学习React');
  await expect(page.locator('text=学习React')).toHaveClass(/completed/);
});
```

### 3. 性能测试
```javascript
// Lighthouse CI 集成
// 或者使用 web-vitals 库监控
import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals';

getCLS(console.log);
getFID(console.log);
getFCP(console.log);
getLCP(console.log);
getTTFB(console.log);
```

## 调试技巧

### 1. 移动端调试工具
- Chrome DevTools：切换到移动设备模拟
- Eruda：在移动端实时调试
  ```javascript
  <script src="//cdn.jsdelivr.net/npm/eruda"></script>
  <script>eruda.init();</script>
  ```
- React DevTools：组件状态检查

### 2. 常见问题排查

#### 视口问题
```javascript
// 确保 meta viewport 标签正确
<meta
  name="viewport"
  content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no"
/>
```

#### 样式问题
// 确保全局字体样式统一，标题、正文大小适中
```css
html {
  font-size: 16px;
}

body {
  line-height: 1.5;
  font-family: Arial, sans-serif;
}
```css

/* 元素间距适中，页边距紧凑 */
```css
.container {
  padding: 20px;
}
```css

/* 确保宽度自适应，不会缩放导致标签内容换行或显示异常 */
```css
.container {
  max-width: 1200px;
  margin: 0 auto;
}
```

// 检查样式渗透，确保样式隔离不会相互干扰
```css
.todo-item {
  padding: 10px;
  border-radius: 5px;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
```

#### 滚动穿透
```javascript
// 模态框打开时禁止背景滚动
const lockScroll = () => {
  document.body.style.overflow = 'hidden';
};
const unlockScroll = () => {
  document.body.style.overflow = 'auto';
};
```

#### iOS Safari 兼容性
```css
/* 修复 100vh 问题 */
.full-height {
  height: 100vh;
  height: -webkit-fill-available;
}

/* 修复输入框自动缩放 */
input, textarea {
  font-size: 16px; /* >= 16px 防止缩放 */
}
```

## 代码审查清单

### 移动端适配
- [ ] 在所有主流移动设备上测试
- [ ] 触摸目标 >= 44x44px
- [ ] 响应式布局在断点处正确断开
- [ ] 横屏/竖屏适配正确
- [ ] 暗黑模式支持完整

### 性能
- [ ] LCP < 2.5s
- [ ] 图片已懒加载和优化
- [ ] 长列表使用虚拟滚动
- [ ] 代码分割合理
- [ ] 无内存泄漏

### 用户体验
- [ ] 加载状态提示清晰
- [ ] 错误处理友好
- [ ] 空状态有引导
- [ ] 过渡动画流畅
- [ ] 手势交互自然

### 代码质量
- [ ] 遵循命名规范
- [ ] 组件职责单一
- [ ] Props 类型定义完整
- [ ] 无 ESLint 错误
- [ ] 测试覆盖率 > 80%

## 最佳实践总结

1. **系统化思维**：从架构到代码，始终保持清晰的结构
2. **性能优先**：移动端性能直接影响用户留存
3. **代码复用**：组件化、模块化、抽象化
4. **渐进增强**：基础功能优先，高级功能按需加载
5. **数据驱动**：确保用户数据不丢失，优先本地存储
6. **边界测试**：极端情况（低分辨率、低内存、旧设备）也要测试
7. **持续重构**：定期review和优化，避免技术债务积累
8. **文档同步**：更新代码时同步更新注释和文档

## 开发工作流

1. **需求分析** → 理解业务目标，确定技术方案
2. **架构设计** → 组件拆分，状态管理，路由设计
3. **核心功能实现** → MVP快速验证
4. **性能优化** → 分析瓶颈，针对性优化
5. **移动端适配** → 多设备测试，调整布局
6. **测试验证** → 单元测试、集成测试、E2E测试
7. **代码审查** → 对照清单，确保质量
8. **部署上线** → 灰度发布，监控指标
9. **反馈迭代** → 收集用户反馈，持续改进

---

**记住**：优雅的代码不仅是功能正确，更是可维护、可扩展、高性能的体现。以 INTJ 的战略思维，构建经得起时间考验的移动应用。
