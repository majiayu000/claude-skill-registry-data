---
name: rag-kit
description: Интеграция RAG (Retrieval Augmented Generation) с xAI Grok Collections и Google Gemini. Используй этот skill когда нужно добавить AI-чат с базой знаний, настроить RAG систему, интегрировать Grok Collections или создать чат-бота с контекстом из документов.
---

# RAG Kit — Библиотека для RAG приложений

RAG Kit — готовая библиотека для создания AI-чатов с контекстом из документов.

## Компоненты

| Компонент | Назначение |
|-----------|-----------|
| `createGrokClient` | Клиент для xAI Grok Collections (поиск, загрузка, удаление) |
| `createRAGService` | RAG сервис с чатом (Gemini + Grok + веб-поиск) |
| `createUploadService` | Упрощённая загрузка документов |
| `createConfig` | Создание кастомной конфигурации |

## Быстрый старт

### 1. Скопируй файлы RAG Kit в проект

```bash
# Структура
api/lib/rag-kit/
├── index.js           # Главный экспорт
├── rag-service.js     # RAG сервис
├── grok-client.js     # Grok клиент
├── upload-service.js  # Загрузка документов
└── configs/
    └── template.js    # Шаблон конфигурации
```

### 2. Установи зависимости

```bash
npm install @google/generative-ai
```

### 3. Настрой переменные окружения

```env
# Google AI (Gemini)
GOOGLE_API_KEY=AIza...

# xAI Grok Collections
XAI_API_KEY=xai-...              # Для поиска
XAI_MANAGEMENT_API_KEY=xai-...   # Для управления документами
GROK_COLLECTION_ID=collection_...

# Опционально: Google Custom Search
GOOGLE_CSE_ID=...
```

### 4. Создай API endpoint

```javascript
import { createRAGService } from './lib/rag-kit/index.js';

const rag = createRAGService({
  systemPrompt: 'Ты — AI-ассистент компании X...',
  grokConfig: {
    synonyms: {
      'доставка': ['отправка', 'shipping'],
    },
  },
});

export default async function handler(req, res) {
  const { message, history } = req.body;

  const result = await rag.chat({ message, history });

  res.json({
    response: result.response,
    sources: result.sources,
  });
}
```

## Конфигурация

### Основные параметры RAG Service

```javascript
createRAGService({
  // API ключ Google (по умолчанию из env)
  googleApiKey: process.env.GOOGLE_API_KEY,

  // Модель для чата
  chatModel: 'gemini-3-pro-preview',

  // System prompt (ОБЯЗАТЕЛЬНО!)
  systemPrompt: 'Ты — AI-ассистент...',

  // Конфигурация Grok
  grokConfig: {
    synonyms: {},        // Словарь синонимов
    categories: {},      // Категории документов
    queryPatterns: {},   // Паттерны для извлечения терминов
    rerankingRules: [],  // Правила переранжирования
  },

  // Веб-поиск (опционально)
  webSearch: {
    enabled: false,
    cseId: process.env.GOOGLE_CSE_ID,
    triggers: ['актуальная информация', '2025'],
    domainPriority: { 'docs.example.com': 10 },
  },

  // Опции генерации
  maxHistoryLength: 10,
  maxOutputTokens: 8192,
  temperature: 0.7,
  searchLimit: 20,
});
```

### Конфигурация Grok Client

```javascript
createGrokClient({
  // API ключи (по умолчанию из env)
  apiKey: process.env.XAI_API_KEY,
  managementApiKey: process.env.XAI_MANAGEMENT_API_KEY,
  collectionId: process.env.GROK_COLLECTION_ID,

  // Domain-specific конфигурация
  synonyms: {},           // Query expansion
  categories: {},         // Автоклассификация
  queryPatterns: {},      // Извлечение терминов
  rerankingRules: [],     // Переранжирование

  // Опции поиска
  defaultRetrievalMode: 'hybrid',  // hybrid | semantic | keyword
  defaultLimit: 20,
  enableQueryExpansion: true,
  enableReranking: true,
});
```

## API Reference

Смотри [api-reference.md](./api-reference.md) для полного описания API.

## Примеры

Смотри [examples.md](./examples.md) для примеров использования.

## Шаблоны

В директории `templates/` находятся готовые файлы для копирования:

- `chat-endpoint.js` — API endpoint для чата
- `upload-endpoint.js` — API endpoint для загрузки
- `config-template.js` — Шаблон конфигурации
- `env-example.txt` — Пример .env файла
