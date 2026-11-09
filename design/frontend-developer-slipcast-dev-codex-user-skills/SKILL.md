---
name: frontend-developer
description: "Разработка фронтенда: HTML/CSS/JS, React/Vue/Svelte, верстка, сборка (Vite/Webpack), работа с API, доступность"
whenToUse: "Применяй, когда нужно создать или доработать пользовательский интерфейс, SPA, верстку, компоненты или стили"
---

# Frontend Developer

Гайд по разработке клиентской части веб-приложений.

## Выбор стека

| Задача | Стек |
|--------|------|
| Быстрый лендинг/прототип | HTML + CSS + Vanilla JS (или Vite) |
| SPA средней сложности | React + Vite + TypeScript |
| SSR/SEO-критичный | Next.js / Nuxt |
| Легковесный/реактивный | Vue 3 / Svelte |
| Стилизация | Tailwind CSS / CSS Modules / SCSS |

## Чек-лист разработки

### Инициализация
- [ ] Инициализируй проект: `npm create vite@latest` (React+TS по умолчанию)
- [ ] Настрой ESLint + Prettier
- [ ] Подключи роутер (React Router / Vue Router) если SPA
- [ ] Настрой env-переменные (`.env.local`, не коммить секреты)

### Верстка и компоненты
- [ ] Компонентный подход: разбивай UI на переиспользуемые компоненты
- [ ] Типизируй пропсы (TypeScript)
- [ ] Семантический HTML (`header`, `nav`, `main`, `button`, `form`)
- [ ] Мобильная адаптивность (mobile-first, медиа-запросы / flex / grid)
- [ ] Доступность (a11y): `alt`, `aria-*`, контраст, фокус-состояния

### Состояние и данные
- [ ] Локальное состояние — `useState` (React) / `ref` (Vue)
- [ ] Глобальное — Context/Zustand/Redux (React) или Pinia (Vue)
- [ ] Запросы к API: fetch/axios + обработка loading/error/empty состояний
- [ ] Загрузки: `useEffect`/`onMounted` без утечек (cleanup)

### Производительность
- [ ] Ленивая загрузка маршрутов: `React.lazy` / dynamic import
- [ ] Мемоизация тяжёлых вычислений (`useMemo`/`computed`)
- [ ] Оптимизация изображений (`loading="lazy"`, WebP, srcset)
- [ ] Минимизация бандла (code-splitting, tree-shaking)

### Сборка и качество
- [ ] Dev-сервер: `npm run dev`
- [ ] Сборка: `npm run build`, проверь что проходит без ошибок
- [ ] Типы: `tsc --noEmit`
- [ ] Линт: `npm run lint`

## Правила
1. Начинай с MVP-экрана, не строй всё сразу.
2. Переиспользуй компоненты, не дублируй разметку.
3. Не зашивай секреты в клиентский код — только через env на сервере.
4. Проверяй на реальных разрешениях (desktop + mobile).
