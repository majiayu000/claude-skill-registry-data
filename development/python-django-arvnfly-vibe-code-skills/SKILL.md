---
name: python-django
description: "Django architecture, ORM select_related/prefetch_related optimization, middleware, and signals discipline."
---

# Django Architecture Protocol

Build maintainable Django and Django REST Framework services.

---

## 1. Query Optimization

1. Always use `select_related` for single-valued relationships (ForeignKey, OneToOne).
2. Always use `prefetch_related` for multi-valued relationships (ManyToMany, reverse FK) to eradicate N+1 queries.

---

## 2. Fat Models, Thin Views

Place business logic and invariants in model methods or domain services, never in views or serializers.
