---
name: django
description: Django ORM patterns, Django REST Framework, middleware, signals, async views, and production-grade application architecture
layer: domain
category: backend
triggers:
  - "django"
  - "django rest framework"
  - "drf"
  - "django orm"
  - "django models"
  - "django middleware"
  - "django signals"
inputs:
  - "Django application requirements"
  - "API design specifications"
  - "Data model definitions"
outputs:
  - "Django model and view implementations"
  - "DRF serializer and viewset patterns"
  - "Production configuration"
linksTo:
  - python
  - postgresql
  - redis
  - message-queues
  - microservices
linkedFrom:
  - error-handling
  - authentication
  - testing
preferredNextSkills:
  - postgresql
  - redis
  - python
fallbackSkills:
  - fastapi
  - nodejs
riskLevel: low
memoryReadPolicy: selective
memoryWritePolicy: none
sideEffects: []
---

# Django Domain Skill

## Purpose

Provide expert-level guidance on Django development including ORM optimization, Django REST Framework patterns, middleware, signals, async views, security hardening, and deployment best practices.

## Key Patterns

### 1. Model Design

```python
import uuid
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator

class TimestampedModel(models.Model):
    """Abstract base model with created/updated timestamps."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]

class Product(TimestampedModel):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    price = models.IntegerField(
        validators=[MinValueValidator(0)],
        help_text="Price in cents"
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.PROTECT,  # Prevent accidental category deletion
        related_name="products",
    )
    tags = models.ManyToManyField("Tag", blank=True, related_name="products")
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta(TimestampedModel.Meta):
        constraints = [
            models.CheckConstraint(
                check=models.Q(price__gte=0),
                name="product_price_non_negative",
            ),
            models.UniqueConstraint(
                fields=["name", "category"],
                name="unique_product_per_category",
            ),
        ]
        indexes = [
            models.Index(fields=["category", "is_active"]),
            models.Index(fields=["name"], condition=models.Q(is_active=True),
                         name="active_product_name_idx"),
        ]

    def __str__(self) -> str:
        return self.name

    @property
    def price_display(self) -> str:
        return f"${self.price / 100:.2f}"
```

### 2. QuerySet Optimization

```python
# Custom manager with common querysets
class ProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related("category")

    def active(self):
        return self.get_queryset().filter(is_active=True)

    def with_tags(self):
        return self.get_queryset().prefetch_related("tags")

    def by_category(self, category_slug: str):
        return self.active().filter(category__slug=category_slug)

# Usage -- avoid N+1 queries
# BAD: N+1 query
products = Product.objects.all()
for p in products:
    print(p.category.name)  # Queries DB for each product

# GOOD: Single query with JOIN
products = Product.objects.select_related("category").all()
for p in products:
    print(p.category.name)  # No extra query

# GOOD: Prefetch for M2M/reverse FK
products = Product.objects.prefetch_related(
    Prefetch("tags", queryset=Tag.objects.filter(is_active=True))
).all()

# Aggregate and annotate
from django.db.models import Count, Avg, F, Q, Value
from django.db.models.functions import Coalesce

categories = Category.objects.annotate(
    product_count=Count("products", filter=Q(products__is_active=True)),
    avg_price=Coalesce(Avg("products__price"), Value(0)),
).filter(product_count__gt=0).order_by("-product_count")

# Bulk operations
Product.objects.filter(category__slug="old").update(is_active=False)

Product.objects.bulk_create([
    Product(name=f"Item {i}", price=i*100, category=cat)
    for i in range(1000)
], batch_size=500)

# Efficient existence checks
if Product.objects.filter(slug=slug).exists():  # Better than .count() > 0
    raise ValidationError("Slug already exists")

# Use .only() and .defer() for partial loading
products = Product.objects.only("id", "name", "price").all()
```

### 3. Django REST Framework

```python
from rest_framework import serializers, viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import CursorPagination
from django_filters import rest_framework as filters

# Serializers
class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    price_display = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = [
            "id", "name", "slug", "description", "price",
            "price_display", "category", "category_name",
            "tags", "is_active", "created_at"
        ]
        read_only_fields = ["id", "slug", "created_at"]

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative")
        return value

# Filters
class ProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="price", lookup_expr="lte")
    search = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Product
        fields = ["category", "is_active", "tags"]

# Cursor pagination (more efficient than offset for large datasets)
class ProductPagination(CursorPagination):
    page_size = 20
    ordering = "-created_at"
    page_size_query_param = "page_size"
    max_page_size = 100

# ViewSet
class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = ProductPagination
    filterset_class = ProductFilter

    def get_queryset(self):
        return (
            Product.objects
            .select_related("category")
            .prefetch_related("tags")
            .filter(is_active=True)
        )

    def perform_create(self, serializer):
        serializer.save(
            slug=slugify(serializer.validated_data["name"]),
        )

    @action(detail=True, methods=["post"])
    def archive(self, request, pk=None):
        product = self.get_object()
        product.is_active = False
        product.save(update_fields=["is_active", "updated_at"])
        return Response(status=status.HTTP_204_NO_CONTENT)
```

### 4. Middleware

```python
import time
import logging
from django.http import HttpRequest, HttpResponse

logger = logging.getLogger(__name__)

class RequestTimingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        start = time.perf_counter()
        response = self.get_response(request)
        duration = time.perf_counter() - start

        response["X-Request-Duration"] = f"{duration:.4f}"
        if duration > 1.0:
            logger.warning(
                "Slow request: %s %s took %.2fs",
                request.method, request.path, duration
            )
        return response

class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        response = self.get_response(request)
        response["X-Content-Type-Options"] = "nosniff"
        response["X-Frame-Options"] = "DENY"
        response["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response["Permissions-Policy"] = "camera=(), microphone=()"
        return response
```

### 5. Signals (Use Sparingly)

```python
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.core.cache import cache

@receiver(post_save, sender=Product)
def invalidate_product_cache(sender, instance, **kwargs):
    """Clear cache when product is updated."""
    cache.delete(f"product:{instance.pk}")
    cache.delete(f"category_products:{instance.category_id}")

# PREFER: Override save() for model-level side effects
class Product(TimestampedModel):
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
```

## Best Practices

1. **Use `select_related` and `prefetch_related`** -- N+1 is the #1 Django perf issue
2. **Use `update_fields`** in `.save()` to avoid race conditions
3. **Use database constraints** (CheckConstraint, UniqueConstraint) not just validator logic
4. **Prefer `PROTECT` or `RESTRICT`** over `CASCADE` for important FKs
5. **Use `CursorPagination`** for large datasets instead of `PageNumberPagination`
6. **Keep signals minimal** -- prefer overriding `save()` or using services
7. **Use `transaction.atomic()`** for multi-step operations
8. **Configure `CONN_MAX_AGE`** for persistent database connections
9. **Use `django-debug-toolbar`** in development to catch N+1 queries
10. **Run `manage.py check --deploy`** before production deployment

## Common Pitfalls

| Pitfall | Impact | Fix |
|---------|--------|-----|
| N+1 queries in templates/serializers | Massive DB load | `select_related`/`prefetch_related` on every queryset |
| Using `Model.objects.all()` in serializer fields | Loads entire table | Always filter, use `get_queryset()` |
| Fat views | Untestable logic | Move to service layer or model methods |
| Signals creating hidden side effects | Hard to debug, test | Use explicit service calls or override `save()` |
| Not using `F()` expressions for updates | Race conditions | `Product.objects.filter(pk=id).update(stock=F("stock") - 1)` |
| Missing database indexes | Slow queries | Add `db_index=True` or `Meta.indexes` |
| `DEBUG=True` in production | Memory leak, security risk | Use environment variables, never hardcode |
