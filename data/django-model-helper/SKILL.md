---
name: django-model-helper
description: Generates Django models with proper field types, relationships, and migrations. Use when creating Django models or database schemas.
allowed-tools: [Write, Read, Bash]
---

# Django Model Helper

Generates Django models following best practices.

## When to Use

- "Create a Django model for users"
- "Generate Product model"
- "Add BlogPost model with relationships"

## Model Generation

```python
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """Custom user model."""
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
        ordering = ['-created_at']

    def __str__(self):
        return self.username

class Post(models.Model):
    """Blog post model."""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'posts'
        ordering = ['-published_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['author', '-published_at']),
        ]

    def __str__(self):
        return self.title
```

## After Creating Model

1. Generate migration:
   ```bash
   python manage.py makemigrations
   ```

2. Apply migration:
   ```bash
   python manage.py migrate
   ```

## Best Practices

- Use appropriate field types
- Add indexes for frequently queried fields
- Define __str__ methods
- Use Meta class for table name and ordering
- Add related_name to relationships
- Include created_at/updated_at timestamps
- Use on_delete properly
- Add helpful docstrings
