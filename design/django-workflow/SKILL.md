---
name: django-workflow
description: Django framework workflow guidelines. Activate when working with Django projects, manage.py, django-admin, or Django-specific patterns.
location: user
---

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in RFC 2119.

# Django Workflow

## Tool Grid

| Task | Tool | Command |
|------|------|---------|
| Lint | Ruff | `uv run ruff check .` |
| Format | Ruff | `uv run ruff format .` |
| Type check | django-stubs + mypy | `uv run mypy .` |
| Security | bandit | `uv run bandit -r .` |
| Test | pytest-django | `uv run pytest` |
| Migrations | squawk | `squawk migrations/*.sql` |
| Dev server | Django | `uv run python manage.py runserver` |

---

## Django 5.x Features

### Composite Primary Keys (Django 5.2+)

Django 5.2 introduces native composite primary key support. You SHOULD use `CompositePrimaryKey` for junction tables and legacy database integration:

```python
from django.db import models

class OrderItem(models.Model):
    order = models.ForeignKey("Order", on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.CompositePrimaryKey("order", "product"),
        ]
```

### Async Views

You SHOULD prefer async views for I/O-bound operations. Django 5.x has improved async ORM support:

```python
from django.http import JsonResponse

async def fetch_items(request):
    items = [item async for item in Item.objects.filter(active=True)]
    return JsonResponse({"items": [i.name for i in items]})
```

Key async patterns:
- Use `async for` with QuerySets
- Use `await` with `aget()`, `afirst()`, `acount()`, `aexists()`
- Sync ORM calls in async views trigger `SynchronousOnlyOperation` exceptions

### Template Partials

You MAY use the `{% include %}` tag with the `only` keyword to create isolated partials:

```html
{% include "components/card.html" with title=item.title only %}
```

### Built-in CSP (Content Security Policy)

Django 5.x includes built-in CSP middleware. You SHOULD configure it in settings:

```python
# settings/base.py
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "csp.middleware.CSPMiddleware",  # or django.middleware.csp.ContentSecurityPolicyMiddleware
    # ...
]

CONTENT_SECURITY_POLICY = {
    "DIRECTIVES": {
        "default-src": ["'self'"],
        "script-src": ["'self'"],
        "style-src": ["'self'", "'unsafe-inline'"],
        "img-src": ["'self'", "data:", "https:"],
    }
}
```

### Django Tasks (Background Tasks)

For simple background tasks, you MAY use Django's built-in task system (Django 5.1+):

```python
from django.tasks import task

@task
def send_welcome_email(user_id: int) -> None:
    user = User.objects.get(pk=user_id)
    # Send email logic
```

For complex workflows, Celery remains RECOMMENDED.

---

## Architecture Patterns

### Fat Models to Services Pattern

Business logic MUST NOT reside in views. You MUST use the services pattern:

```python
# services/order_service.py
from dataclasses import dataclass
from decimal import Decimal
from django.db import transaction

@dataclass
class OrderService:
    """Order-related business operations."""

    @staticmethod
    @transaction.atomic
    def create_order(user, cart_items: list) -> "Order":
        """Create order from cart items with inventory validation."""
        order = Order.objects.create(user=user, status=Order.Status.PENDING)

        for item in cart_items:
            if item.product.stock < item.quantity:
                raise InsufficientStockError(item.product)

            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )
            item.product.stock -= item.quantity
            item.product.save(update_fields=["stock"])

        return order

    @staticmethod
    def calculate_total(order: "Order") -> Decimal:
        """Calculate order total with discounts applied."""
        return sum(item.subtotal for item in order.items.all())
```

### Selectors Pattern

Query logic MUST be encapsulated in selectors. Views MUST NOT contain complex querysets:

```python
# selectors/product_selectors.py
from django.db.models import QuerySet, Q, Prefetch

class ProductSelectors:
    """Product query encapsulation."""

    @staticmethod
    def get_active_products() -> QuerySet:
        return Product.objects.filter(
            is_active=True,
            stock__gt=0,
        ).select_related("category")

    @staticmethod
    def search_products(query: str) -> QuerySet:
        return Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query),
            is_active=True,
        )

    @staticmethod
    def get_product_with_reviews(product_id: int) -> Product:
        return Product.objects.prefetch_related(
            Prefetch(
                "reviews",
                queryset=Review.objects.filter(approved=True).order_by("-created_at"),
            )
        ).get(pk=product_id)
```

---

## Model Organization

### Field Ordering

Models MUST follow this field ordering:

```python
from django.db import models
from django.utils.translation import gettext_lazy as _

class Product(models.Model):
    """Product model with standardized field ordering."""

    # 1. Primary key (if custom)
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # 2. Foreign keys and relations
    category = models.ForeignKey(
        "Category",
        on_delete=models.PROTECT,
        related_name="products",
    )

    # 3. Required fields
    name = models.CharField(_("name"), max_length=200)
    slug = models.SlugField(_("slug"), max_length=200, unique=True)
    price = models.DecimalField(_("price"), max_digits=10, decimal_places=2)

    # 4. Optional fields
    description = models.TextField(_("description"), blank=True)
    image = models.ImageField(_("image"), upload_to="products/", blank=True)

    # 5. Boolean flags
    is_active = models.BooleanField(_("active"), default=True)
    is_featured = models.BooleanField(_("featured"), default=False)

    # 6. Timestamps
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    # 7. Meta class
    class Meta:
        verbose_name = _("product")
        verbose_name_plural = _("products")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["category", "is_active"]),
        ]

    # 8. String representation
    def __str__(self) -> str:
        return self.name

    # 9. Save/delete overrides
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    # 10. Custom properties
    @property
    def is_in_stock(self) -> bool:
        return self.stock > 0

    # 11. Instance methods
    def apply_discount(self, percentage: Decimal) -> Decimal:
        return self.price * (1 - percentage / 100)
```

---

## Settings Organization

### Directory Structure

Settings MUST be organized in a package:

```
config/
├── settings/
│   ├── __init__.py      # Imports from environment-specific module
│   ├── base.py          # Shared settings
│   ├── local.py         # Local development
│   ├── production.py    # Production settings
│   └── test.py          # Test settings
```

### Base Settings Pattern

```python
# config/settings/base.py
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Security - MUST be overridden in production
SECRET_KEY = "django-insecure-CHANGE-ME"
DEBUG = False
ALLOWED_HOSTS: list[str] = []

# Application definition
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "django_extensions",
]

LOCAL_APPS = [
    "apps.users",
    "apps.products",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
```

```python
# config/settings/local.py
from .base import *

DEBUG = True
SECRET_KEY = "local-dev-only-key"
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Debug toolbar
INSTALLED_APPS += ["debug_toolbar"]
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
INTERNAL_IPS = ["127.0.0.1"]
```

---

## URL Patterns

### URL Organization

URLs MUST use `include()` and namespacing:

```python
# config/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("apps.api.urls", namespace="api-v1")),
    path("products/", include("apps.products.urls", namespace="products")),
    path("users/", include("apps.users.urls", namespace="users")),
]
```

```python
# apps/products/urls.py
from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path("", views.ProductListView.as_view(), name="list"),
    path("<slug:slug>/", views.ProductDetailView.as_view(), name="detail"),
    path("category/<slug:category_slug>/", views.CategoryView.as_view(), name="category"),
]
```

### URL Naming Conventions

- List views: `<app>:list` (e.g., `products:list`)
- Detail views: `<app>:detail` (e.g., `products:detail`)
- Create views: `<app>:create`
- Update views: `<app>:update`
- Delete views: `<app>:delete`

---

## Views

### Class-Based vs Function-Based Views

You SHOULD use CBVs for standard CRUD operations and FBVs for simple, one-off logic:

**Use CBVs when:**
- Standard CRUD operations
- Pagination, filtering, or sorting needed
- Template rendering with context
- Code reuse via mixins

**Use FBVs when:**
- Simple API endpoints
- Webhooks or callbacks
- Complex conditional logic that doesn't fit CBV flow

### CBV Example

```python
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

class ProductListView(ListView):
    model = Product
    template_name = "products/list.html"
    context_object_name = "products"
    paginate_by = 20

    def get_queryset(self):
        return ProductSelectors.get_active_products()

class ProductDetailView(DetailView):
    model = Product
    template_name = "products/detail.html"
    slug_url_kwarg = "slug"

    def get_object(self):
        return ProductSelectors.get_product_with_reviews(self.kwargs["slug"])
```

---

## Forms and Validation

### Form Organization

Forms MUST separate validation from processing:

```python
from django import forms
from django.core.exceptions import ValidationError

class OrderForm(forms.ModelForm):
    """Order creation form with custom validation."""

    class Meta:
        model = Order
        fields = ["shipping_address", "payment_method"]

    def clean_shipping_address(self):
        address = self.cleaned_data["shipping_address"]
        if not address.is_deliverable:
            raise ValidationError("Shipping not available to this address.")
        return address

    def clean(self):
        cleaned_data = super().clean()
        # Cross-field validation here
        return cleaned_data
```

### Form Processing in Views

```python
def create_order(request):
    form = OrderForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        order = OrderService.create_order(
            user=request.user,
            cart_items=request.user.cart.items.all(),
        )
        return redirect("orders:detail", pk=order.pk)
    return render(request, "orders/create.html", {"form": form})
```

---

## Admin Customization

### Admin Best Practices

```python
from django.contrib import admin
from django.utils.html import format_html

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "price", "is_active", "created_at"]
    list_filter = ["category", "is_active", "created_at"]
    search_fields = ["name", "description"]
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]

    fieldsets = (
        (None, {"fields": ("name", "slug", "category")}),
        ("Pricing", {"fields": ("price", "discount_price")}),
        ("Content", {"fields": ("description", "image")}),
        ("Status", {"fields": ("is_active", "is_featured")}),
        ("Metadata", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" />', obj.image.url)
        return "-"
    thumbnail.short_description = "Image"
```

---

## Migrations

### Migration Guidelines

1. Migrations MUST be small and focused
2. Migrations MUST be reversible when possible
3. Data migrations MUST be separate from schema migrations
4. Migrations MUST NOT contain business logic

### Schema Migration

```python
# Auto-generated, keep minimal
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="sku",
            field=models.CharField(max_length=50, null=True),
        ),
    ]
```

### Data Migration (Separate File)

```python
from django.db import migrations

def populate_skus(apps, schema_editor):
    Product = apps.get_model("products", "Product")
    for product in Product.objects.filter(sku__isnull=True):
        product.sku = f"SKU-{product.pk:06d}"
        product.save(update_fields=["sku"])

def reverse_skus(apps, schema_editor):
    Product = apps.get_model("products", "Product")
    Product.objects.update(sku=None)

class Migration(migrations.Migration):
    dependencies = [
        ("products", "0002_add_sku_field"),
    ]

    operations = [
        migrations.RunPython(populate_skus, reverse_skus),
    ]
```

### Making Field Non-Nullable

This MUST be done in three migrations:

1. Add nullable field
2. Data migration to populate
3. Alter to non-nullable

---

## Testing

### Test Organization

```python
# tests/test_services/test_order_service.py
import pytest
from decimal import Decimal
from apps.orders.services import OrderService

@pytest.mark.django_db
class TestOrderService:
    def test_create_order_success(self, user, cart_with_items):
        order = OrderService.create_order(user, cart_with_items)

        assert order.user == user
        assert order.items.count() == len(cart_with_items)

    def test_create_order_insufficient_stock(self, user, cart_with_unavailable_item):
        with pytest.raises(InsufficientStockError):
            OrderService.create_order(user, cart_with_unavailable_item)
```

### Fixtures

```python
# conftest.py
import pytest
from django.contrib.auth import get_user_model

@pytest.fixture
def user(db):
    User = get_user_model()
    return User.objects.create_user(
        email="test@example.com",
        password="testpass123",
    )

@pytest.fixture
def product(db, category):
    return Product.objects.create(
        name="Test Product",
        slug="test-product",
        category=category,
        price=Decimal("29.99"),
        stock=10,
    )
```

---

## Security Checklist

- [ ] `DEBUG = False` in production
- [ ] `SECRET_KEY` from environment variable
- [ ] `ALLOWED_HOSTS` configured
- [ ] HTTPS enforced (`SECURE_SSL_REDIRECT = True`)
- [ ] CSRF protection enabled
- [ ] SQL injection prevented (use ORM, not raw SQL)
- [ ] XSS protection (escape templates, CSP headers)
- [ ] Clickjacking protection (`X_FRAME_OPTIONS`)
- [ ] Sensitive data encrypted at rest
- [ ] Rate limiting on authentication endpoints
