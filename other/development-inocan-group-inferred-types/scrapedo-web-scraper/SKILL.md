---
name: scrapedo-web-scraper
description: Веб-скрапинг через Scrape.do. Используй, если не получается посмотреть какой-то сайт (URL).
---

# Scrape.do Web Scraper

Скрапинг веб-страниц через Scrape.do API. Используй когда обычный fetch не работает (блокировка, JavaScript).

## Использование

```bash
# Получить текст страницы
python scripts/scrape.py https://example.com

# Получить HTML
python scripts/scrape.py --html https://example.com
```

## Из Python

```python
from scripts.scrape import fetch_via_scrapedo

result = fetch_via_scrapedo('https://example.com')
if result['success']:
    print(result['content'])  # текст
    # result['html'] — оригинальный HTML
else:
    print(result['content'])  # описание ошибки
```

## Результат

- **Успех**: текст страницы (или HTML с `--html`)
- **Ошибка**: понятное сообщение (нет токена / лимит / недоступно)

Если вернулась ошибка — страница недоступна через этот метод.
