---
name: analytics-reports
description: Создание профессиональных аналитических справок по финансам, экономике и юриспруденции в формате HTML. Два дизайна на выбор — dark-premium (тёмная тема с золотыми акцентами) и analytics-green (светлая тема с бирюзовыми акцентами). Создаёт две версии — статичную для мобильных устройств и интерактивную для компьютеров. Использовать при запросах на создание аналитических отчётов, финансовых справок, экономических обзоров, юридических заключений, сравнительных анализов, инвестиционных меморандумов.
---

# Аналитические справки

Создание профессиональных HTML-документов для финансового, экономического и юридического анализа.

## Дизайны

### dark-premium
Тёмная тема: фон `#0f1419`, акценты золотые `#d4af37`. Премиальный вид для серьёзных финансовых документов.

### analytics-green  
Светлая тема: фон `#fafbfc`, акценты бирюзовые `#16857d`. Современный корпоративный стиль.

## Версии документов

### Статичная (mobile)
- Без JavaScript и Chart.js
- Данные в таблицах и CSS-блоках
- Все секции открыты по умолчанию
- Суффикс файла: `-static.html`

### Интерактивная (desktop)
- Chart.js для графиков (doughnut, bar, line)
- Раскрывающиеся секции (onclick toggle)
- Hover-эффекты
- Суффикс файла: `-interactive.html`

## Цветовые палитры

### dark-premium

```css
:root {
    --bg-main: #0f1419;
    --bg-panel: linear-gradient(135deg, #1a2332 0%, #0a0e27 100%);
    --accent-gold: #d4af37;
    --accent-gold-light: #f4d58d;
    --accent-blue: #4a90e2;
    --text-primary: #e8e8e8;
    --text-secondary: #b8b8b8;
    --border: rgba(212, 175, 55, 0.15);
}
```

### analytics-green

```css
:root {
    --bg-main: #fafbfc;
    --bg-card: #ffffff;
    --accent-teal: #16857d;
    --accent-teal-light: #4db8b0;
    --accent-orange: #ffa726;
    --text-primary: #1a1a1a;
    --text-secondary: #666666;
    --border: #e0e0e0;
}
```

## Структура документа

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[Название отчёта]</title>
    <!-- Chart.js только для интерактивной версии -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <div class="container">
        <header>
            <h1>[Заголовок]</h1>
            <div class="subtitle">[Подзаголовок]</div>
        </header>
        
        <!-- Ключевые метрики -->
        <div class="metrics-container">
            <!-- 3-4 карточки с KPI -->
        </div>
        
        <!-- Основные панели -->
        <div class="panel">
            <h2 class="panel-title">[Заголовок секции]</h2>
            <!-- Содержимое -->
        </div>
    </div>
</body>
</html>
```

## Компоненты

### Метрики (KPI-карточки)

**dark-premium:**
```html
<div class="highlight-box">
    <div class="highlight-label">Выручка</div>
    <div class="highlight-value">405,1</div>
    <div class="highlight-unit">млрд ₽</div>
</div>
```

```css
.highlight-box {
    background: var(--bg-panel);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
}
.highlight-value {
    font-size: 2.5rem;
    font-weight: 700;
    color: var(--accent-gold);
    font-family: 'Fira Code', monospace;
}
```

**analytics-green:**
```html
<div class="metric-card">
    <div class="metric-label">Выручка</div>
    <div class="metric-value">405,1</div>
    <div class="metric-unit">млрд ₽</div>
</div>
```

```css
.metric-card {
    background: white;
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}
.metric-value {
    font-size: 2rem;
    font-weight: 700;
    color: var(--accent-teal);
    font-family: 'Roboto Mono', monospace;
}
```

### Раскрывающиеся секции (интерактивная)

```html
<div class="panel collapsible" onclick="togglePanel(this)">
    <div class="panel-header">
        <h2>Структура выручки</h2>
        <span class="toggle-icon">▼</span>
    </div>
    <div class="panel-content">
        <!-- Контент -->
    </div>
</div>
```

```javascript
function togglePanel(panel) {
    panel.classList.toggle('open');
}
```

### Информационные блоки

```html
<div class="notice">
    <strong>Примечание:</strong> Данные за 2024 год являются предварительными.
</div>
```

```css
/* dark-premium */
.notice {
    background: rgba(212, 175, 55, 0.1);
    border-left: 3px solid var(--accent-gold);
    padding: 1rem;
    margin: 1rem 0;
}

/* analytics-green */
.info-box {
    background: #e0f2f1;
    border-left: 3px solid var(--accent-teal);
    padding: 1rem;
    margin: 1rem 0;
}
```

## Графики (интерактивная версия)

### Doughnut (круговая)

```html
<div class="chart-container">
    <canvas id="revenueChart"></canvas>
</div>
```

```javascript
new Chart(document.getElementById('revenueChart'), {
    type: 'doughnut',
    data: {
        labels: ['Электроэнергия', 'Теплоэнергия', 'Прочее'],
        datasets: [{
            data: [65, 30, 5],
            backgroundColor: ['#d4af37', '#4a90e2', '#6c757d'],
            borderWidth: 3,
            borderColor: '#0f1419'
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'bottom',
                labels: { color: '#e8e8e8' }
            }
        }
    }
});
```

### Bar (столбчатая)

```javascript
new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['2022', '2023', '2024'],
        datasets: [{
            label: 'Выручка',
            data: [350, 380, 405],
            backgroundColor: '#d4af37',
            borderRadius: 8
        }]
    },
    options: {
        scales: {
            y: { 
                beginAtZero: true,
                grid: { color: 'rgba(255,255,255,0.1)' },
                ticks: { color: '#b8b8b8' }
            },
            x: { 
                grid: { display: false },
                ticks: { color: '#b8b8b8' }
            }
        }
    }
});
```

## Статичная версия: замена графиков

Вместо Chart.js использовать CSS-визуализацию:

```html
<div class="static-bar-container">
    <div class="static-bar-item">
        <div class="static-bar-label">Электроэнергия</div>
        <div class="static-bar-track">
            <div class="static-bar-fill" style="width: 65%;"></div>
        </div>
        <div class="static-bar-value">65%</div>
    </div>
</div>
```

```css
.static-bar-track {
    height: 24px;
    background: rgba(255,255,255,0.1); /* dark */
    border-radius: 12px;
    overflow: hidden;
    flex: 1;
    margin: 0 1rem;
}
.static-bar-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--accent-gold), var(--accent-gold-light));
    border-radius: 12px;
}
```

## Таблицы

```html
<table class="data-table">
    <thead>
        <tr>
            <th>Показатель</th>
            <th>2023</th>
            <th>2024</th>
            <th>Δ</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Выручка</td>
            <td class="number">380,5</td>
            <td class="number">405,1</td>
            <td class="number positive">+6,5%</td>
        </tr>
    </tbody>
</table>
```

```css
.data-table {
    width: 100%;
    border-collapse: collapse;
}
.data-table th {
    background: var(--accent-gold);
    color: var(--bg-main);
    padding: 0.75rem;
    text-align: left;
}
.data-table td {
    padding: 0.75rem;
    border-bottom: 1px solid var(--border);
}
.number {
    font-family: 'Fira Code', monospace;
    text-align: right;
}
.positive { color: #27ae60; }
.negative { color: #e74c3c; }
```

## Шрифты

### dark-premium

```html
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Raleway:wght@300;400;500;600&family=Fira+Code:wght@400;500&display=swap" rel="stylesheet">
```

- Заголовки: Playfair Display
- Текст: Raleway
- Числа: Fira Code

### analytics-green

```html
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&family=Open+Sans:wght@300;400;500;600&family=Roboto+Mono:wght@400;500&display=swap" rel="stylesheet">
```

- Заголовки: Montserrat
- Текст: Open Sans
- Числа: Roboto Mono

## Рабочий процесс

1. Определить тему (dark-premium / analytics-green) из запроса
2. Собрать данные и структуру
3. Создать интерактивную версию с Chart.js
4. Создать статичную версию с CSS-барами
5. Сохранить оба файла

## Именование файлов

```
analysis-q3-2024-static.html      # Статичная версия
analysis-q3-2024-interactive.html # Интерактивная версия
```
