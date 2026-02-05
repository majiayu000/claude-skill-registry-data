---
name: search-skill
description: Implement search functionality for finding tasks by keywords in title and description. Use when building search features.
allowed-tools: Write, Read
---

# Search Skill

## Purpose
Implement powerful search functionality for finding tasks.

## Instructions

### Basic Keyword Search
```python
from typing import List

def search_tasks(self, keyword: str) -> List[dict]:
    """Search tasks by keyword in title and description."""
    if not keyword:
        return []
    
    keyword = keyword.lower().strip()
    
    def matches(task: dict) -> bool:
        title = task.get('title', '').lower()
        desc = task.get('description', '') or ''
        desc = desc.lower()
        return keyword in title or keyword in desc
    
    return [t for t in self.get_all_tasks() if matches(t)]
```

### Using TinyDB Query
```python
def search_tasks(self, keyword: str) -> List[dict]:
    """Search using TinyDB query."""
    keyword = keyword.lower()
    return self.db.search(
        (self.db.query.title.test(lambda t: keyword in t.lower())) |
        (self.db.query.description.test(
            lambda d: d is not None and keyword in d.lower()
        ))
    )
```

### Multi-Word Search
```python
def search_all_words(self, query: str) -> List[dict]:
    """Search where ALL words must match."""
    words = query.lower().split()
    if not words:
        return []
    
    def matches_all(task: dict) -> bool:
        text = f"{task.get('title', '')} {task.get('description', '')}".lower()
        return all(word in text for word in words)
    
    return [t for t in self.get_all_tasks() if matches_all(t)]

def search_any_word(self, query: str) -> List[dict]:
    """Search where ANY word can match."""
    words = query.lower().split()
    if not words:
        return []
    
    def matches_any(task: dict) -> bool:
        text = f"{task.get('title', '')} {task.get('description', '')}".lower()
        return any(word in text for word in words)
    
    return [t for t in self.get_all_tasks() if matches_any(t)]
```

### Search with Ranking
```python
def search_ranked(self, keyword: str) -> List[dict]:
    """Search and rank by relevance."""
    keyword = keyword.lower()
    results = []
    
    for task in self.get_all_tasks():
        title = task.get('title', '').lower()
        desc = (task.get('description', '') or '').lower()
        
        score = 0
        # Higher score for title matches
        if keyword in title:
            score += 10
            # Even higher if starts with keyword
            if title.startswith(keyword):
                score += 5
        # Lower score for description matches
        if keyword in desc:
            score += 3
        
        if score > 0:
            results.append((score, task))
    
    # Sort by score descending
    results.sort(key=lambda x: x[0], reverse=True)
    return [task for _, task in results]
```

### Search in Tags
```python
def search_by_tag(self, tag: str) -> List[dict]:
    """Search tasks containing a specific tag."""
    tag = tag.lower().strip()
    return self.db.search(
        self.db.query.tags.test(
            lambda tags: tag in [t.lower() for t in tags]
        )
    )

def search_by_any_tag(self, tags: List[str]) -> List[dict]:
    """Search tasks containing any of the given tags."""
    tags = [t.lower().strip() for t in tags]
    return self.db.search(
        self.db.query.tags.test(
            lambda task_tags: any(
                t.lower() in tags for t in task_tags
            )
        )
    )
```

### Full Search Service
```python
class SearchService:
    """Comprehensive search functionality."""
    
    def __init__(self, database):
        self.db = database
    
    def search(
        self,
        query: str = None,
        tags: List[str] = None,
        priority: str = None,
        status: str = None,
        include_completed: bool = True
    ) -> List[dict]:
        """Combined search with multiple criteria."""
        tasks = self.db.get_all()
        
        # Filter by keyword
        if query:
            query = query.lower()
            tasks = [
                t for t in tasks
                if query in t.get('title', '').lower() or
                   query in (t.get('description', '') or '').lower()
            ]
        
        # Filter by tags
        if tags:
            tags = [t.lower() for t in tags]
            tasks = [
                t for t in tasks
                if any(tag.lower() in tags for tag in t.get('tags', []))
            ]
        
        # Filter by priority
        if priority:
            tasks = [t for t in tasks if t.get('priority') == priority]
        
        # Filter by status
        if status:
            tasks = [t for t in tasks if t.get('status') == status]
        
        # Exclude completed
        if not include_completed:
            tasks = [t for t in tasks if t.get('status') != 'completed']
        
        return tasks
```

## Best Practices

- Always normalize search input (lowercase, strip)
- Handle None/empty values gracefully
- Implement case-insensitive matching
- Provide relevance ranking for better UX
- Support both AND and OR multi-word searches
- Cache results for repeated queries if needed
