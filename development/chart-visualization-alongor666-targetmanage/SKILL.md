---
name: chart-visualization
description: ECharts图表配置技能，包括柱状图、折线图、组合图等可视化组件
license: MIT
version: 1.0.0
category: visualization
---

# Chart Visualization Skill

## 能力概述
此技能提供车险经营数据可视化解决方案，基于 ECharts 实现柱状图、折线图、组合图等多种图表类型，支持响应式设计、主题适配和交互功能。

## 支持的图表类型

### 1. 柱状图（Bar Chart）

#### 月度保费规划图
```typescript
{
  title: { text: '月度保费规划' },
  xAxis: {
    type: 'category',
    data: ['1月', '2月', '3月', '4月', '5月', '6月',
           '7月', '8月', '9月', '10月', '11月', '12月']
  },
  yAxis: [
    {
      type: 'value',
      name: '保费（万元）',
      position: 'left'
    }
  ],
  series: [
    {
      name: '2026目标',
      type: 'bar',
      data: targetMonthlyData,
      itemStyle: { color: '#60A5FA' }, // 浅蓝色
      barWidth: '60%',
      label: {
        show: true,
        position: 'top',
        formatter: '{c}',
        fontWeight: 'bold'
      }
    },
    {
      name: '2025实际',
      type: 'bar',
      data: actual2025MonthlyData,
      itemStyle: { color: '#D1D5DB' }, // 浅灰色
      barWidth: '60%',
      label: {
        show: true,
        position: 'top',
        formatter: '{c}',
        fontWeight: 'bold'
      }
    }
  ]
}
```

#### 季度保费规划图
```typescript
{
  title: { text: '季度保费规划' },
  xAxis: {
    type: 'category',
    data: ['Q1', 'Q2', 'Q3', 'Q4']
  },
  series: [
    {
      name: '2026目标',
      type: 'bar',
      data: quarterlyTargetData,
      itemStyle: { color: '#60A5FA' }
    },
    {
      name: '2025实际',
      type: 'bar',
      data: quarterlyActual2025Data,
      itemStyle: { color: '#D1D5DB' }
    }
  ]
}
```

### 2. 组合图（Combo Chart）

#### 月度组合图（柱状 + 折线）
```typescript
{
  title: { text: '月度保费与增长率' },
  xAxis: {
    type: 'category',
    data: months
  },
  yAxis: [
    {
      type: 'value',
      name: '保费（万元）',
      position: 'left'
    },
    {
      type: 'value',
      name: '增长率（%）',
      position: 'right',
      axisLabel: {
        formatter: '{value}%'
      }
    }
  ],
  series: [
    // 柱状图（左轴）
    {
      name: '2026目标',
      type: 'bar',
      yAxisIndex: 0,
      data: targetMonthlyData
    },
    {
      name: '2025实际',
      type: 'bar',
      yAxisIndex: 0,
      data: actual2025MonthlyData
    },
    // 折线图（右轴）
    {
      name: '同比增长率',
      type: 'line',
      yAxisIndex: 1,
      data: growthRateData,
      smooth: true,
      lineStyle: { color: '#3B82F6' },
      label: {
        show: true,
        formatter: '{c}%',
        color: '#3B82F6'
      }
    }
  ]
}
```

### 3. 占比图（Percentage Chart）

#### 月度占比规划图
```typescript
{
  title: { text: '月度保费占比' },
  xAxis: {
    type: 'category',
    data: months
  },
  yAxis: [
    {
      type: 'value',
      name: '占比（%）',
      position: 'left',
      max: 100,
      axisLabel: { formatter: '{value}%' }
    },
    {
      type: 'value',
      name: '增长率（%）',
      position: 'right',
      axisLabel: { formatter: '{value}%' }
    }
  ],
  series: [
    {
      name: '2026规划占比',
      type: 'bar',
      yAxisIndex: 0,
      data: targetPercentageData
    },
    {
      name: '2025实际占比',
      type: 'bar',
      yAxisIndex: 0,
      data: actualPercentageData
    },
    {
      name: '同比增长率',
      type: 'line',
      yAxisIndex: 1,
      data: growthRateData
    }
  ]
}
```

## 图表样式规范

### 1. 全局配置
```typescript
const globalConfig = {
  // 去掉网格线
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    top: '10%',
    containLabel: true,
    show: false // 不显示网格线
  },

  // 图例配置
  legend: {
    data: ['2026目标', '2025实际', '同比增长率'],
    top: '5%',
    left: 'center'
  },

  // 提示框配置
  tooltip: {
    trigger: 'axis',
    axisPointer: { type: 'shadow' },
    formatter: function(params: any) {
      let result = params[0].axisValue + '<br/>';
      params.forEach((item: any) => {
        if (item.seriesType === 'line') {
          result += `${item.marker} ${item.seriesName}: ${item.value}%<br/>`;
        } else {
          result += `${item.marker} ${item.seriesName}: ${item.value} 万元<br/>`;
        }
      });
      return result;
    }
  },

  // 动画配置
  animation: true,
  animationDuration: 1000,
  animationEasing: 'cubicOut'
};
```

### 2. 柱状图样式
```typescript
const barStyle = {
  barWidth: '60%', // 柱宽

  // 数值标签
  label: {
    show: true,
    position: 'top',
    formatter: '{c}',
    fontWeight: 'bold',
    fontSize: 12,

    // 标签颜色
    color: '#6B7280' // 默认灰色
  },

  // 柱子颜色
  itemStyle: {
    borderRadius: [4, 4, 0, 0], // 圆角
    color: '#60A5FA' // 2026目标浅蓝
  },

  // hover 效果
  emphasis: {
    itemStyle: {
      shadowBlur: 10,
      shadowColor: 'rgba(0, 0, 0, 0.3)'
    }
  }
};
```

### 3. 折线图样式
```typescript
const lineStyle = {
  smooth: true, // 平滑曲线

  // 线条样式
  lineStyle: {
    width: 2,
    color: '#3B82F6' // 蓝色
  },

  // 数据点样式
  symbol: 'circle',
  symbolSize: 6,

  // 数值标签
  label: {
    show: true,
    formatter: '{c}%',
    color: '#3B82F6', // 默认蓝色
    fontWeight: 'bold',
    fontSize: 12
  },

  // 区域填充（可选）
  areaStyle: {
    color: {
      type: 'linear',
      x: 0, y: 0, x2: 0, y2: 1,
      colorStops: [
        { offset: 0, color: 'rgba(59, 130, 246, 0.3)' },
        { offset: 1, color: 'rgba(59, 130, 246, 0.05)' }
      ]
    }
  }
};
```

## 预警功能（5% 阈值）

### 预警触发条件
当月/季度增长率 < 5% 时触发预警。

### 预警样式配置
```typescript
// 预警时柱状图颜色：橙色
const warningBarColor = '#FF9500';

// 预警时标签颜色：深红色
const warningLabelColor = '#8B0000';

// 预警时折线图颜色：深蓝色（保持不变）
const warningLineColor = '#1E40AF';

// 应用预警样式
series.forEach((item: any) => {
  const growthRate = item.data;

  if (item.seriesType === 'bar' && growthRate < 0.05) {
    // 柱状图预警
    item.itemStyle.color = warningBarColor;
    item.label.color = warningLabelColor;
  } else if (item.seriesType === 'line') {
    // 折线图预警
    growthRate.forEach((rate: number, index: number) => {
      if (rate < 0.05) {
        // 数据点预警（需要使用 rich 文本样式）
        item.label.formatter = function(params: any) {
          const color = params.value < 0.05 ? warningLabelColor : '#3B82F6';
          return `{${color}|${params.value}%}`;
        };
      }
    });
  }
});
```

### ECharts Rich 文本样式
```typescript
const richTextStyle = {
  label: {
    formatter: function(params: any) {
      const growthRate = params.value;
      const color = growthRate < 0.05 ? '#8B0000' : '#3B82F6';
      return `{warning${growthRate < 0.05 ? '|warning' : '|normal'}|${growthRate.toFixed(1)}%}`;
    },
    rich: {
      normal: { color: '#3B82F6' },
      warning: { color: '#8B0000', fontWeight: 'bold' }
    }
  }
};
```

## 响应式适配

### 大屏模式（2400px）
```typescript
const largeScreenConfig = {
  title: { textStyle: { fontSize: 24 } },
  xAxis: { axisLabel: { fontSize: 16 } },
  yAxis: { axisLabel: { fontSize: 16 } },
  legend: { textStyle: { fontSize: 16 } },
  grid: { left: '5%', right: '5%' }
};
```

### 桌面模式（1920px）
```typescript
const desktopConfig = {
  title: { textStyle: { fontSize: 18 } },
  xAxis: { axisLabel: { fontSize: 14 } },
  yAxis: { axisLabel: { fontSize: 14 } },
  legend: { textStyle: { fontSize: 14 } },
  grid: { left: '3%', right: '4%' }
};
```

### 移动模式（自适应）
```typescript
const mobileConfig = {
  title: { textStyle: { fontSize: 14 } },
  xAxis: { axisLabel: { fontSize: 12, rotate: 45 } },
  yAxis: { axisLabel: { fontSize: 12 } },
  legend: { textStyle: { fontSize: 12 } },
  grid: { left: '10%', right: '10%' }
};
```

### 响应式切换
```typescript
function getResponsiveConfig() {
  const width = window.innerWidth;
  if (width >= 2400) return largeScreenConfig;
  if (width >= 1024) return desktopConfig;
  return mobileConfig;
}
```

## 颜色系统

### 主色调
```typescript
const colors = {
  // 2026 目标
  target: {
    primary: '#60A5FA',    // 浅蓝色
    hover: '#3B82F6',      // 蓝色
    warning: '#FF9500'     // 橙色（预警）
  },

  // 2025 实际
  actual2025: {
    primary: '#D1D5DB',    // 浅灰色
    hover: '#9CA3AF'       // 深灰色
  },

  // 增长率
  growth: {
    normal: '#3B82F6',     // 蓝色
    warning: '#1E40AF',    // 深蓝色（预警）
    labelNormal: '#3B82F6',// 蓝色标签
    labelWarning: '#8B0000' // 深红色标签（预警）
  }
};
```

## 数据格式化

### 保费格式化
```typescript
function formatPremium(value: number): string {
  if (value >= 10000) {
    return (value / 10000).toFixed(2) + '万';
  }
  return value.toFixed(0);
}
```

### 百分比格式化
```typescript
function formatPercentage(value: number): string {
  return (value * 100).toFixed(1) + '%';
}
```

### 增长率格式化
```typescript
function formatGrowthRate(value: number | null): string {
  if (value === null) return '—';
  const formatted = (value * 100).toFixed(1);
  const sign = value >= 0 ? '+' : '';
  return sign + formatted + '%';
}
```

## 使用示例

### 示例 1：生成月度保费规划图
```
用户请求：生成成都分公司车险 2026 年月度保费规划图

AI 处理流程：
1. 计算月度目标（根据时间进度口径）
2. 获取 2025 年月度实际数据
3. 计算同比增长率
4. 检查预警条件（增长率 < 5%）
5. 应用预警样式
6. 生成 ECharts 配置
7. 渲染图表
```

### 示例 2：切换时间进度口径
```
用户请求：切换到权重时间进度模式

AI 处理流程：
1. 读取 allocation_rules.json 中的权重
2. 使用新权重重新计算月度目标
3. 更新图表数据源
4. 重新生成图表配置
5. 刷新图表显示
```

### 示例 3：导出图表为图片
```
用户请求：导出当前图表为 PNG 图片

AI 处理流程：
1. 获取 ECharts 实例
2. 使用 getDataURL() 生成图片数据
3. 下载为 PNG 文件
4. 支持 2x/3x 高分辨率
```

## 依赖项

### 核心库
- `echarts`: ^5.5.0
- `echarts-for-react`: ^3.0.2

### 配置文件
- `src/lib/echarts-utils.ts` (ECharts 工具函数)

## 最佳实践

1. **性能优化**：大数据量时使用数据采样或分页
2. **可访问性**：提供键盘导航和屏幕阅读器支持
3. **错误处理**：数据缺失时显示友好提示
4. **测试覆盖**：不同尺寸和数据的图表渲染测试
5. **版本兼容**：使用 ECharts 稳定 API，避免频繁更新

## 参考文档
- @doc docs/design/全局设计规范.md
- @code src/lib/echarts-utils.ts
- @code src/components/charts/ChartContainer.tsx
