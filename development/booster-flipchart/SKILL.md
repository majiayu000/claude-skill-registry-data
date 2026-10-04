---
name: booster-flipchart
description: |
  Использование флипчарт-сессий (flipchart) для визуализации и отладки
  сложных графов вызовов и последовательностей (Sequence/Call diagrams).
---

# Booster Flipchart

## Цель

Инструменты Flipchart позволяют визуализировать сложные цепочки вызовов (Call Graphs) и диаграммы последовательностей (Sequence Diagrams) для глубокого понимания логики программы и отладки. 

## Алгоритм работы

1. Создай новую сессию дебага:
   Вызови `flipchart_create_session(session_id="bug_123", symbols=["main", "process_data"])`. 
   Это инициализирует доску для отслеживания указанных символов.
2. Генерируй диаграммы:
   - Если нужно понять зависимости функции (кто ее вызывает и кого вызывает она), используй `flipchart_call_graph(symbol="process_data", max_depth=2)`.
   - Если нужно понять последовательность выполнения, используй `flipchart_sequence_diagram(symbol="main", depth=3)`.
3. Добавляй заметки по мере изучения кода:
   Вызови `flipchart_add_note(session_id="bug_123", label="Инсайт 1", content="process_data падает из-за None", symbols=["process_data"])`.
4. В любой момент ты можешь получить полную картину:
   Вызови `flipchart_get_board(session_id="bug_123")`, чтобы прочитать все собранные диаграммы и заметки.
5. Для быстрого анализа одного символа можно использовать `flipchart_quick_debug(symbol="error_handler", max_depth=2)`.

## Когда использовать

- Запутанная логика (spaghetti code).
- Необходимость визуализировать Mermaid графы вызовов.
- Сложный дебаг распределенных/многослойных вызовов.
