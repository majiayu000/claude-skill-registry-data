---
name: decide
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-03-15
description: "Структурированное принятие решений: матрица «за» и «против», взвешенная оценка, дерево решений, анализ сценариев и матрица Эйзенхауэра."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: utilities
tags: [decision, evaluation, prioritization, framework]
language: ru
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/_services/decide.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-15', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

<img src="../banner.png" width="100%" alt="decide banner">

> **Русский** — Официальная русская версия `decide`.


# Decide — Структурированное принятие решений

> Рациональные решения с помощью структурированных фреймворков и методов оценки

---

## Когда использовать?

- Выбор между несколькими вариантами
- Необходимость создания списка «за» и «против»
- Многокритериальное принятие решений
- Неуверенность при принятии важных решений

**Ключевые слова для вызова:** decide, choose, compare, evaluate, weigh

---

## Фреймворки

### 1. Матрица «за» и «против» (Простая)

Быстрые решения при выборе из 2 вариантов.

```
PRO A:                    CON A:
- Advantage 1             - Disadvantage 1
- Advantage 2             - Disadvantage 2

PRO B:                    CON B:
- Advantage 1             - Disadvantage 1
- Advantage 2             - Disadvantage 2

Recommendation: [A/B] because [reasoning]
```

---

### 2. Взвешенная оценка (Комплексная)

Многокритериальные решения с учетом веса.

| Критерий | Вес | Вариант A | Оценка A | Вариант B | Оценка B |
|-----------|--------|----------|---------|----------|---------|
| Критерий 1 | 30% | 8 | 2.4 | 6 | 1.8 |
| Критерий 2 | 25% | 7 | 1.75 | 9 | 2.25 |
| ИТОГО | 100% | - | X.XX | - | X.XX |

**Процесс:**
1. Сбор критериев
2. Назначение веса (сумма = 100%)
3. Оценка вариантов (по шкале от 1 до 10)
4. Расчет баллов (оценка x вес)
5. Сравнение и рекомендация

---

### 3. Дерево решений (Последовательное)

Решения с четким путем «если-то»:
1. Определение исходного вопроса
2. Первая ветвь (наиболее важный критерий)
3. Следующий уровень (второй по важности)
4. Переход к конечному варианту

---

### 4. Анализ сценариев (Неопределенность)

```
Best Case (X% probability):
  Outcome: +Y points -> Expected value: +Z

Realistic Case (X%):
  Outcome: +Y -> Expected value: +Z

Worst Case (X%):
  Outcome: -Y -> Expected value: -Z

Total expected value: [Sum]
```

---

### 5. Матрица Эйзенхауэра (Приоритизация)

```
              URGENT          NOT URGENT
IMPORTANT     1. DO           2. PLAN
NOT IMPORTANT 3. DELEGATE     4. ELIMINATE
```

---

## Чек-лист качества

Проверьте перед окончательной рекомендацией:
- [ ] Все ли релевантные критерии определены?
- [ ] Учтены ли ценности пользователя?
- [ ] Учтены ли долгосрочные последствия?
- [ ] Выявлены и оценены ли риски?
- [ ] Проведена ли проверка на предвзятость?
- [ ] Оценена ли обратимость решения?

---

## Лучшие практики

### Определение критериев
- Конкретные и измеримые
- Не слишком много (идеально 3-7)
- Независимые друг от друга

### Взвешивание
- Сумма = 100%
- Самый важный критерий >= 25%
- Нет весов < 5%

### Рекомендация
- Четкая и обоснованная
- Упоминание альтернатив
- Указание рисков
- Учет обратимости

---

## Рабочий процесс и порядок действий

```
1. User request
2. Understand decision
3. Identify options (2-5)
4. Choose framework
5. Collect criteria
6. Apply framework
7. Bias check (optional)
8. Make recommendation
9. Document reasoning
```

---

## История изменений

### 1.0.0 (2026-03-15)
- Перенесено из BACH v3.8.0

---

*Перенесено из BACH v3.8.0 | Автономная версия*
