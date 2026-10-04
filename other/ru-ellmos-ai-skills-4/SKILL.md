---
name: migrate-rename
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-03-15
description: Эволюционное переименование файлов с помощью файлов-оберток. Позволяет переименовывать файлы без жестких сбоев — ссылки органично обновляются в процессе использования.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: dev
tags: [migration, renaming, wrapper, evolutionary, refactoring]
language: ru
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/migrate-rename.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-15', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

<img src="../banner.png" width="100%" alt="migrate-rename banner">

> **Русский** — Официальная русская версия `migrate-rename`.


# Переименование файлов с помощью оберток (Эволюционная миграция) (Русский)

> Позволяет переименовывать файлы БЕЗ жестких сбоев. Ссылки органично обновляются в процессе ежедневного использования.

---

## Принцип: Эволюционная миграция

```
BEFORE:                          AFTER:
old_file.md                      new_file.md (renamed)
   |                                |
   +-- Reference A                  +-- old_file.md (wrapper)
   +-- Reference B                         |
   +-- Reference C                         +-- Log table
                                           +-- Instructions
                                           +-- Link to new_file.md
```

Когда кто-то обращается по старому пути:
1. Попадает в файл-обертку
2. Добавляет запись в журнал (лог)
3. Исправляет ссылку, которая привела его сюда
4. Переходит к фактическому файлу

---

## Пошаговое руководство

### 1. Переименуйте файл

```bash
mv old_file.md new_file.md
```

### 2. Создайте файл-обертку

Создайте `old_file.md` со следующим содержимым:

```markdown
# OLD_FILE.md - REDIRECTED (Deutsch)

**Status:** This file has been renamed to `new_file.md`

---

## Migration Log

| Date | Who | Origin | Reference corrected? |
|------|-----|--------|---------------------|
| YYYY-MM-DD | [Name] | Initial migration | n/a (wrapper created) |

---

## Instructions

1. **Leave a log entry** (in table above)
2. **Check origin**: What sent you here?
3. **Correct reference**: Change `old_file.md` -> `new_file.md`
4. **Go to the actual file**: `new_file.md`

---

**Target file:** `new_file.md`
```

### 3. Немедленно исправьте критические ссылки
- Файлы справки (основная документация)
- Ссылки в системных промптах
- Код CLI, непосредственно использующий путь

### 4. Эволюционная миграция остальных ссылок
Остальное автоматически исправляется по мере использования.

---

## Когда использовать метод обертки?

**ДА - Обертка полезна:**
- Множество потенциальных ссылок
- Файл ссылается различными партнерами/инструментами
- Не является критически важным системным файлом

**НЕТ - Изменить все напрямую:**
- Немногочисленные, известные ссылки
- Критические системные файлы (конфигурация, схема БД)
- Критичные к производительности пути

---

## Очистка

Примерно через 30 дней или когда в журнале перестанут появляться новые записи:
1. Переместите файл-обертку в `_archive/deprecated/`
2. Или удалите полностью (если новых записей больше нет)

---

## История изменений

### 1.0.0 (2026-03-15)
- Перенесено из BACH v3.8.0

---

*Перенесено из BACH v3.8.0 | Автономная версия*
