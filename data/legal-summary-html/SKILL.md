---
name: legal-summary-html
description: Создание интерактивных HTML-документов для юридических и аналитических материалов — резюме арбитражных решений, процессуальных приказов, отчётов, аналитических записок. Использовать для создания красивых mobile-first HTML-документов с аккордеонами, таймлайнами, навигацией и профессиональным дизайном в сине-золотой цветовой гамме.
---

# Навык: Юридические HTML-документы

Создание интерактивных HTML-документов с профессиональным дизайном для юридических и аналитических материалов.

## Дизайн-система

### Цветовая палитра

```css
:root {
    --primary: #1a2a3a;       /* Тёмно-синий — заголовки, кнопки */
    --secondary: #2d4a5e;     /* Синий — градиенты, hover */
    --accent: #c9a227;        /* Золотой — акценты, маркеры */
    --accent-light: #e8d49c;  /* Светло-золотой — подсветка */
    --bg: #f8f6f1;            /* Кремовый фон страницы */
    --card-bg: #ffffff;       /* Белый фон карточек */
    --text: #2c3e50;          /* Основной текст */
    --text-light: #5a6a7a;    /* Вспомогательный текст */
    --success: #27ae60;       /* Зелёный — одобрено */
    --danger: #c0392b;        /* Красный — отклонено */
    --warning: #f39c12;       /* Оранжевый — частично */
    --border: #e0ddd5;        /* Границы */
}
```

### Типографика

```css
/* Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600;700&family=Source+Sans+3:wght@300;400;500;600&display=swap');

/* Заголовки — Cormorant Garamond */
h1, h2, h3 { font-family: 'Cormorant Garamond', serif; }
/* h1: 1.6rem, font-weight: 700 */
/* h2: 1.1rem, font-weight: 600 */
/* h3: 1.0rem, font-weight: 600 */

/* Основной текст — Source Sans 3 */
body { font-family: 'Source Sans 3', sans-serif; line-height: 1.6; }
```

## Структура документа

### HTML-каркас

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[Название] | [Номер дела]</title>
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600;700&family=Source+Sans+3:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>/* Стили */</style>
</head>
<body>
    <header class="header">...</header>
    <nav class="nav-container">...</nav>
    <main class="main">...</main>
    <footer class="footer">...</footer>
    <button class="scroll-top">↑</button>
    <script>/* Скрипты */</script>
</body>
</html>
```

## Компоненты

### Header

```html
<header class="header">
    <div class="header-content">
        <span class="case-badge">[НОМЕР ДЕЛА]</span>
        <h1>[Название документа]</h1>
        <div class="header-meta">[Дата] • [Место]</div>
    </div>
</header>
```

```css
.header {
    background: linear-gradient(135deg, var(--primary), var(--secondary));
    color: white;
    padding: 1.5rem 1rem;
    position: sticky;
    top: 0;
    z-index: 100;
}
.case-badge {
    background: var(--accent);
    color: var(--primary);
    padding: 0.25rem 0.75rem;
    border-radius: 4px;
    font-size: 0.75rem;
    font-weight: 600;
}
```

### Navigation Pills

```html
<nav class="nav-container">
    <div class="nav-pills">
        <button class="nav-pill active" onclick="scrollToSection('overview')">
            📋 Обзор
        </button>
        <button class="nav-pill" onclick="scrollToSection('parties')">
            👥 Стороны
        </button>
        <button class="nav-pill" onclick="scrollToSection('timeline')">
            📅 Хронология
        </button>
    </div>
</nav>
```

```css
.nav-container {
    background: white;
    padding: 0.75rem;
    overflow-x: auto;
    border-bottom: 1px solid var(--border);
}
.nav-pills {
    display: flex;
    gap: 0.5rem;
    min-width: max-content;
}
.nav-pill {
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 20px;
    background: var(--bg);
    cursor: pointer;
    white-space: nowrap;
}
.nav-pill.active {
    background: var(--primary);
    color: white;
}
```

### Section (аккордеон)

```html
<section id="overview" class="section open">
    <div class="section-header" onclick="toggleSection(this)">
        <div class="section-title">
            <div class="section-icon blue">📋</div>
            <h2>Обзор дела</h2>
        </div>
        <span class="toggle-icon">▼</span>
    </div>
    <div class="section-content">
        <!-- Контент -->
    </div>
</section>
```

```css
.section {
    background: white;
    border-radius: 12px;
    margin: 1rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    overflow: hidden;
}
.section-header {
    padding: 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    cursor: pointer;
}
.section-content {
    padding: 0 1rem 1rem;
    display: none;
}
.section.open .section-content {
    display: block;
}
.section-icon {
    width: 36px;
    height: 36px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
}
.section-icon.blue { background: #e3f2fd; color: #1976d2; }
.section-icon.green { background: #e8f5e9; color: #388e3c; }
.section-icon.orange { background: #fff3e0; color: #f57c00; }
.section-icon.red { background: #ffebee; color: #d32f2f; }
```

### Status Badges

```html
<span class="status-badge approved">✓ Одобрено</span>
<span class="status-badge rejected">✗ Отклонено</span>
<span class="status-badge partial">~ Частично</span>
```

```css
.status-badge {
    padding: 0.25rem 0.75rem;
    border-radius: 12px;
    font-size: 0.8rem;
    font-weight: 500;
}
.status-badge.approved { background: #e8f5e9; color: #2e7d32; }
.status-badge.rejected { background: #ffebee; color: #c62828; }
.status-badge.partial { background: #fff3e0; color: #ef6c00; }
```

### Timeline

```html
<div class="timeline">
    <div class="timeline-item">
        <div class="timeline-dot"></div>
        <div class="timeline-date">15 октября 2025</div>
        <div class="timeline-text">Описание события</div>
    </div>
</div>
```

```css
.timeline {
    border-left: 2px solid var(--accent);
    margin-left: 1rem;
    padding-left: 1.5rem;
}
.timeline-item {
    position: relative;
    margin-bottom: 1.5rem;
}
.timeline-dot {
    position: absolute;
    left: -2rem;
    top: 0.5rem;
    width: 12px;
    height: 12px;
    background: var(--accent);
    border-radius: 50%;
}
.timeline-date {
    font-weight: 600;
    color: var(--primary);
}
```

### Quote Block

```html
<div class="quote-block">
    «Текст цитаты»
    <div class="quote-source">— Источник, п. 123</div>
</div>
```

```css
.quote-block {
    background: linear-gradient(to right, var(--accent-light), transparent);
    border-left: 4px solid var(--accent);
    padding: 1rem;
    margin: 1rem 0;
    font-style: italic;
}
.quote-source {
    margin-top: 0.5rem;
    font-size: 0.85rem;
    color: var(--text-light);
}
```

### Parties Grid

```html
<div class="parties-grid">
    <div class="party-card claimants">
        <div class="party-label">ИСТЦЫ</div>
        <div class="party-name">Название компании</div>
        <div class="party-country">🇷🇺 Россия</div>
    </div>
    <div class="party-card respondents">
        <div class="party-label">ОТВЕТЧИКИ</div>
        <div class="party-name">Название компании</div>
        <div class="party-country">🇮🇹 Италия</div>
    </div>
</div>
```

```css
.parties-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
}
.party-card {
    padding: 1rem;
    border-radius: 8px;
}
.party-card.claimants { background: #e3f2fd; }
.party-card.respondents { background: #fce4ec; }
.party-label {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    margin-bottom: 0.5rem;
}
```

## JavaScript

```javascript
function toggleSection(header) {
    const section = header.parentElement;
    section.classList.toggle('open');
}

function scrollToSection(id) {
    document.getElementById(id).scrollIntoView({ behavior: 'smooth' });
    // Обновить активную pill
    document.querySelectorAll('.nav-pill').forEach(p => p.classList.remove('active'));
    event.target.classList.add('active');
}

// Scroll to top
document.querySelector('.scroll-top').addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

// Показать кнопку scroll-top при прокрутке
window.addEventListener('scroll', () => {
    const btn = document.querySelector('.scroll-top');
    btn.style.display = window.scrollY > 300 ? 'block' : 'none';
});
```

## Процесс создания

1. Определить структуру разделов из исходного материала
2. Выбрать нужные компоненты
3. Собрать HTML с inline CSS и JS
4. Сохранить как `.html` файл

## Применение

- Резюме арбитражных решений
- Обзоры процессуальных приказов
- Аналитические записки
- Отчёты для клиентов
- Интерактивные презентации материалов дела
