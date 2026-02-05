---
name: component-styling
description: Component style templates and BEM naming for vehicle insurance platform. Use when styling Vue components, implementing BEM classes, creating responsive layouts, or writing scoped CSS. Keywords: BEM naming, component styles, KpiCard, FilterPanel, scoped CSS, responsive design, card styles, button styles, form controls.
allowed-tools: Read, Edit, Grep, Glob
---

# Component Styling - 组件样式规范

车险签单数据分析平台的组件样式模板和BEM命名规范。

---

## 🧩 组件样式模板

### 1. 卡片样式 (Card)

**基础卡片模板**:

```vue
<template>
  <div class="card">
    <div class="card__header">
      <h3 class="card__title">{{ title }}</h3>
      <p class="card__subtitle">{{ subtitle }}</p>
    </div>
    <div class="card__body">
      <slot></slot>
    </div>
    <div class="card__footer">
      <slot name="footer"></slot>
    </div>
  </div>
</template>

<style scoped>
.card {
  background: var(--surface-elevated);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-soft);
  padding: var(--space-6);
  transition: box-shadow 0.3s ease;
}

.card:hover {
  box-shadow: 0 15px 40px rgba(15, 23, 42, 0.12);
}

.card__header {
  margin-bottom: var(--space-4);
  border-bottom: 1px solid var(--gray-300);
  padding-bottom: var(--space-3);
}

.card__title {
  font-size: var(--text-xl);
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.card__subtitle {
  font-size: var(--text-sm);
  color: var(--text-secondary);
  margin: var(--space-2) 0 0;
}

.card__body {
  margin-bottom: var(--space-4);
}

.card__footer {
  padding-top: var(--space-3);
  border-top: 1px solid var(--gray-300);
}
</style>
```

---

### 2. 按钮样式 (Button)

**按钮变体模板**:

```vue
<template>
  <button :class="['btn', `btn--${variant}`, `btn--${size}`]">
    <slot></slot>
  </button>
</template>

<script setup>
defineProps({
  variant: {
    type: String,
    default: 'primary',
    validator: (v) => ['primary', 'secondary', 'ghost'].includes(v)
  },
  size: {
    type: String,
    default: 'md',
    validator: (s) => ['sm', 'md', 'lg'].includes(s)
  }
})
</script>

<style scoped>
/* 基础样式 */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: none;
  border-radius: var(--radius-sm);
  font-family: var(--font-family-base);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 尺寸变体 */
.btn--sm {
  padding: var(--space-2) var(--space-3);
  font-size: var(--text-sm);
}

.btn--md {
  padding: var(--space-3) var(--space-5);
  font-size: var(--text-base);
}

.btn--lg {
  padding: var(--space-4) var(--space-6);
  font-size: var(--text-lg);
}

/* 样式变体 */
.btn--primary {
  background: var(--primary-500);
  color: white;
}

.btn--primary:hover:not(:disabled) {
  background: var(--primary-600);
}

.btn--primary:active:not(:disabled) {
  background: var(--primary-700);
}

.btn--secondary {
  background: var(--gray-100);
  color: var(--text-primary);
}

.btn--secondary:hover:not(:disabled) {
  background: var(--gray-300);
}

.btn--ghost {
  background: transparent;
  color: var(--primary-500);
  border: 1px solid var(--primary-500);
}

.btn--ghost:hover:not(:disabled) {
  background: var(--surface-primary-tint);
}
</style>
```

---

### 3. 表单控件 (Form Controls)

**输入框模板**:

```vue
<template>
  <div class="input-group">
    <label v-if="label" class="input-group__label">{{ label }}</label>
    <input
      :type="type"
      :placeholder="placeholder"
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      class="input-group__input"
    />
    <span v-if="error" class="input-group__error">{{ error }}</span>
  </div>
</template>

<script setup>
defineProps({
  label: String,
  type: { type: String, default: 'text' },
  placeholder: String,
  modelValue: [String, Number],
  error: String
})

defineEmits(['update:modelValue'])
</script>

<style scoped>
.input-group {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.input-group__label {
  font-size: var(--text-sm);
  font-weight: 500;
  color: var(--text-primary);
}

.input-group__input {
  padding: var(--space-3) var(--space-4);
  border: 1px solid var(--gray-300);
  border-radius: var(--radius-sm);
  font-size: var(--text-base);
  font-family: var(--font-family-base);
  color: var(--text-primary);
  background: var(--surface-default);
  transition: border-color 0.2s ease;
}

.input-group__input:focus {
  outline: none;
  border-color: var(--primary-500);
  box-shadow: 0 0 0 3px var(--surface-primary-tint);
}

.input-group__input::placeholder {
  color: var(--text-muted);
}

.input-group__error {
  font-size: var(--text-xs);
  color: var(--status-warning);
}
</style>
```

---

### 4. 图表容器 (Chart Container)

**ECharts容器模板**:

```vue
<template>
  <div class="chart-container">
    <div class="chart-container__header">
      <h4 class="chart-container__title">{{ title }}</h4>
      <div class="chart-container__actions">
        <slot name="actions"></slot>
      </div>
    </div>
    <div class="chart-container__body">
      <div ref="chartRef" class="chart-container__canvas"></div>
    </div>
  </div>
</template>

<style scoped>
.chart-container {
  background: var(--surface-elevated);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-soft);
  padding: var(--space-6);
}

.chart-container__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-4);
}

.chart-container__title {
  font-size: var(--text-lg);
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.chart-container__actions {
  display: flex;
  gap: var(--space-2);
}

.chart-container__body {
  position: relative;
}

.chart-container__canvas {
  width: 100%;
  height: 400px;  /* 必须设置高度 */
}
</style>
```

---

## 🏷️ BEM 命名规范

### 基础规则

**命名格式**:
- **Block**: `.block`
- **Element**: `.block__element`
- **Modifier**: `.block--modifier` 或 `.block__element--modifier`

**分隔符**:
- `__` (双下划线): 元素分隔符
- `--` (双中划线): 修饰符分隔符
- `-` (单中划线): 词语分隔符(多个单词)

---

### KPI 卡片示例

```html
<!-- Block -->
<div class="kpi-card">

  <!-- Element -->
  <div class="kpi-card__header">
    <h3 class="kpi-card__title">签单保费</h3>
  </div>

  <!-- Element -->
  <div class="kpi-card__main">
    <div class="kpi-card__value">1,234,567</div>

    <!-- Element + Modifier -->
    <div class="kpi-card__trend kpi-card__trend--up">
      <span class="kpi-card__trend-icon">↑</span>
      <span class="kpi-card__trend-text">+12.5%</span>
    </div>
  </div>

  <!-- Element -->
  <div class="kpi-card__chart">
    <div class="kpi-card__chart-canvas"></div>
  </div>

</div>
```

**CSS**:
```css
/* Block */
.kpi-card {
  /* ... */
}

/* Element */
.kpi-card__header { /* ... */ }
.kpi-card__title { /* ... */ }
.kpi-card__main { /* ... */ }
.kpi-card__value { /* ... */ }
.kpi-card__trend { /* ... */ }
.kpi-card__trend-icon { /* ... */ }
.kpi-card__trend-text { /* ... */ }
.kpi-card__chart { /* ... */ }
.kpi-card__chart-canvas { /* ... */ }

/* Modifier */
.kpi-card__trend--up {
  color: var(--status-success);
}
.kpi-card__trend--down {
  color: var(--status-warning);
}
.kpi-card__trend--neutral {
  color: var(--status-neutral);
}
```

---

### 命名示例表

| 场景 | 正确 ✅ | 错误 ❌ |
|------|---------|---------|
| 块 | `.card` | `.Card`, `.CARD` |
| 元素 | `.card__header` | `.card-header`, `.cardHeader` |
| 修饰符 | `.card--large` | `.card-large`, `.cardLarge` |
| 多词元素 | `.card__price-tag` | `.card__priceTag`, `.card__price_tag` |
| 状态修饰符 | `.button--disabled` | `.button-disabled`, `.disabled` |

---

### 常见反模式

❌ **避免过深嵌套**:
```html
<!-- 不推荐 -->
<div class="card">
  <div class="card__header">
    <div class="card__header__title">
      <span class="card__header__title__text">标题</span>  <!-- 4层嵌套 -->
    </div>
  </div>
</div>
```

✅ **扁平化元素**:
```html
<!-- 推荐 -->
<div class="card">
  <div class="card__header">
    <div class="card__title">
      <span class="card__title-text">标题</span>  <!-- 2层嵌套 -->
    </div>
  </div>
</div>
```

---

## 📱 响应式设计

### 断点系统

**3级断点**:

```css
/* 移动端 (默认) */
@media (max-width: 767px) {
  /* Mobile styles */
}

/* 平板端 */
@media (min-width: 768px) and (max-width: 1023px) {
  /* Tablet styles */
}

/* 桌面端 */
@media (min-width: 1024px) {
  /* Desktop styles */
}
```

---

### Dashboard 布局示例

**移动端** (单列):
```css
/* 移动端(默认) */
.dashboard {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
  padding: var(--space-4);
}

.dashboard__kpi-grid {
  display: grid;
  grid-template-columns: 1fr;  /* 单列 */
  gap: var(--space-4);
}
```

**平板端** (2列):
```css
@media (min-width: 768px) {
  .dashboard {
    padding: var(--space-6);
  }

  .dashboard__kpi-grid {
    grid-template-columns: repeat(2, 1fr);  /* 2列 */
  }
}
```

**桌面端** (3列):
```css
@media (min-width: 1024px) {
  .dashboard {
    padding: var(--space-8);
  }

  .dashboard__kpi-grid {
    grid-template-columns: repeat(3, 1fr);  /* 3列 */
  }
}
```

---

### 响应式字体

**流式字体**:
```css
.kpi-card__value {
  font-size: clamp(1.5rem, 4vw, 2.5rem);
  /* 最小24px, 理想4vw, 最大40px */
}
```

**断点字体**:
```css
.heading {
  font-size: var(--text-xl);  /* 移动端: 20px */
}

@media (min-width: 768px) {
  .heading {
    font-size: var(--text-2xl);  /* 平板: 24px */
  }
}

@media (min-width: 1024px) {
  .heading {
    font-size: var(--text-3xl);  /* 桌面: 30px */
  }
}
```

---

## ✅ 最佳实践

### 1. Scoped 样式

```vue
<!-- ✅ 正确 -->
<style scoped>
.kpi-card {
  /* 样式只作用于当前组件 */
}
</style>

<!-- 穿透子组件时使用 :deep() -->
<style scoped>
.parent :deep(.child) {
  color: red;
}
</style>
```

---

### 2. BEM 命名

```css
/* ✅ 正确 */
.kpi-card { }
.kpi-card__header { }
.kpi-card__title { }
.kpi-card__value--up { }

/* ❌ 错误 */
.card { }
.cardHeader { }
```

---

### 3. 响应式设计 (移动优先)

```css
/* ✅ 推荐: 移动优先 */
.grid {
  grid-template-columns: 1fr;  /* 移动端默认 */
}

@media (min-width: 768px) {
  .grid {
    grid-template-columns: repeat(2, 1fr);  /* 平板 */
  }
}

/* ❌ 不推荐: 桌面优先 */
.grid {
  grid-template-columns: repeat(3, 1fr);
}

@media (max-width: 1023px) {
  .grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
```

---

## 🔗 相关资源

### 关键文档位置
- [frontend/src/components/dashboard/KpiCard.vue](../../frontend/src/components/dashboard/KpiCard.vue) - KPI卡片组件
- [frontend/src/components/dashboard/FilterPanel.vue](../../frontend/src/components/dashboard/FilterPanel.vue) - 筛选面板组件

### 相关 Skills
- [css-design-tokens](../css-design-tokens/SKILL.md) - CSS变量和颜色系统
- [vue-component-dev](../vue-component-dev/SKILL.md) - Vue组件开发

### 外部参考
- [BEM官方文档](http://getbem.com/)
- [响应式设计最佳实践](https://web.dev/responsive-web-design-basics/)

---

## ✅ 总结

### 核心要点

1. **组件模板**: 卡片/按钮/表单/图表容器
2. **BEM命名**: `.block__element--modifier`
3. **响应式**: 移动优先, 768px / 1024px断点
4. **Scoped CSS**: 避免样式污染
5. **CSS变量**: 使用设计Token,不硬编码

### 适用场景

✅ **适用**:
- 创建新组件样式
- 修改现有组件样式
- 实现响应式布局
- BEM命名规范

❌ **不适用**(请使用其他Skills):
- 定义CSS变量 → `css-design-tokens`
- Vue组件逻辑 → `vue-component-dev`

---

**文档维护者**: Claude Code AI Assistant
**创建日期**: 2025-11-09
**下次审查**: 2025-11-23
