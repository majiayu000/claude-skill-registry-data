---
name: gutendex-books
description: Search and retrieve public domain books from Project Gutenberg via the Gutendex API. Use when the user asks for free ebooks, searches by author/title, or explores specific literary topics. No API key required.
---

# Gutendex Book Search Skill


Search for free public domain books from Project Gutenberg using the Gutendex API.

## Usage

```bash
python3 scripts/book_helper.py [QUERY] [--topic TOPIC]
```

- `QUERY`: Search by book title or author name.
- `--topic`: Filter results by a specific subject or topic.
- `--raw`: Get the full raw JSON response.

## Examples
- `python3 scripts/book_helper.py "Mark Twain"`
- `python3 scripts/book_helper.py --topic "Science Fiction"`

## API Information
- Source: [Gutendex](https://gutendex.com/)
- Auth: No API Key required.
- Accesses over 70,000 free ebooks.
