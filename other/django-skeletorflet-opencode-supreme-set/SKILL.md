---
name: django
description: Django Python web framework. Use when building Django projects, ORM queries, admin interface customization, class-based views, DRF APIs, or using signals and middleware.
---

## django

High-level Python framework with batteries included for rapid, secure web development.

### Core Concepts
- ORM: queryset API with lazy evaluation, `select_related`/`prefetch_related` for N+1 prevention
- Admin interface: auto-generated CRUD from models, customizable via `ModelAdmin` classes
- Class-based views: `ListView`, `DetailView`, `CreateView` reduce boilerplate over function views
- DRF: `ModelViewSet` + `Serializer` classes for RESTful APIs with browsable docs

### Common Patterns
- Signals: `post_save`/`pre_delete` for decoupled side effects like cache invalidation
- Middleware: request/response pipeline for auth, CORS, logging, or rate limiting
- Auth system: built-in `User` model, permissions, groups, and session-based authentication
- Testing: `TestCase` with `Client` for request simulation, `assertContains` for template checks

### Best Practices
- Use `select_related` for FK relationships and `prefetch_related` for M2M to avoid N+1 queries
- Keep business logic in model methods or service layers, not in views or signals
- Apply database-level constraints (unique, FK) alongside model-level validation
- Use `@login_required` and `@permission_required` decorators rather than manual checks

### Common Code Patterns
- `class ArticleView(DetailView): model = Article; template_name = "article.html"`
- `@api_view(["GET"])` with `@permission_classes([IsAuthenticated])` for DRF endpoints
