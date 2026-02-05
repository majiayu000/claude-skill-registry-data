---
name: django-patterns
description: Implement common Django design patterns including managers, querysets, mixins, services, and architectural patterns. Use when refactoring code or implementing standard Django patterns.
allowed-tools: Read, Write, Grep
---

You are a Django design patterns expert. You help implement clean, maintainable Django code using established design patterns and best practices.

## Patterns You Can Implement

### 1. Custom Model Managers and QuerySets

**Purpose**: Encapsulate complex queries and add domain logic to model layer.

**When to use**:
- Complex or frequently-used queries
- Business logic related to data retrieval
- Chainable query methods

**Implementation**:

```python
# models.py
from django.db import models
from django.utils import timezone

class PublishedQuerySet(models.QuerySet):
    """Custom queryset with domain methods"""

    def published(self):
        """Filter published items"""
        return self.filter(status='published', publish_date__lte=timezone.now())

    def draft(self):
        """Filter draft items"""
        return self.filter(status='draft')

    def by_author(self, author):
        """Filter by specific author"""
        return self.filter(author=author)

    def recent(self, days=7):
        """Get recent items"""
        since = timezone.now() - timezone.timedelta(days=days)
        return self.filter(created_at__gte=since)


class PublishedManager(models.Manager):
    """Manager that returns custom queryset"""

    def get_queryset(self):
        return PublishedQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()

    def draft(self):
        return self.get_queryset().draft()


class Article(models.Model):
    title = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=[('draft', 'Draft'), ('published', 'Published')])
    publish_date = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = PublishedManager()  # Custom manager

    class Meta:
        ordering = ['-created_at']

# Usage:
# Article.objects.published()  # Get published articles
# Article.objects.published().by_author(user)  # Chain methods
# Article.objects.recent(days=30).published()  # Combine filters
```

### 2. Model Mixins

**Purpose**: Reuse common model functionality across multiple models.

**Common mixins**:

```python
# models/mixins.py
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

class TimeStampedMixin(models.Model):
    """Add created_at and updated_at timestamps"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteMixin(models.Model):
    """Soft delete functionality"""
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        """Soft delete instead of actual delete"""
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
        """Actually delete from database"""
        super().delete()

    def restore(self):
        """Restore soft-deleted object"""
        self.deleted_at = None
        self.save()


class SlugMixin(models.Model):
    """Auto-generate slug from name/title"""
    slug = models.SlugField(unique=True, max_length=255)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)

    def generate_unique_slug(self):
        """Generate unique slug from title or name"""
        base_slug = slugify(getattr(self, 'title', None) or getattr(self, 'name', ''))
        slug = base_slug
        counter = 1

        while self.__class__.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        return slug


class PublishableMixin(models.Model):
    """Add publication status and date"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    publish_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def publish(self):
        """Publish the object"""
        self.status = 'published'
        self.publish_date = timezone.now()
        self.save()

    def unpublish(self):
        """Revert to draft"""
        self.status = 'draft'
        self.publish_date = None
        self.save()

    @property
    def is_published(self):
        return self.status == 'published' and (
            self.publish_date is None or self.publish_date <= timezone.now()
        )


# Usage: Combine mixins
class Article(TimeStampedMixin, SlugMixin, PublishableMixin, SoftDeleteMixin):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']
```

### 3. Service Layer Pattern

**Purpose**: Separate business logic from views and models.

**When to use**:
- Complex business operations
- Operations spanning multiple models
- Logic that doesn't belong in models or views

```python
# services/order_service.py
from django.db import transaction
from django.core.exceptions import ValidationError
from decimal import Decimal
from .models import Order, OrderItem, Product, Payment

class OrderService:
    """Business logic for order processing"""

    @transaction.atomic
    def create_order(self, user, items, shipping_address, payment_method):
        """
        Create a new order with items.

        Args:
            user: User placing the order
            items: List of dicts with 'product_id' and 'quantity'
            shipping_address: Shipping address dict
            payment_method: Payment method identifier

        Returns:
            Created Order object

        Raises:
            ValidationError: If validation fails
        """
        # Validate products and availability
        self._validate_items(items)

        # Calculate totals
        subtotal, tax, total = self._calculate_totals(items)

        # Create order
        order = Order.objects.create(
            user=user,
            subtotal=subtotal,
            tax=tax,
            total=total,
            shipping_address=shipping_address,
            payment_method=payment_method,
            status='pending'
        )

        # Create order items and update stock
        self._create_order_items(order, items)

        # Process payment
        self._process_payment(order)

        # Send confirmation email
        self._send_order_confirmation(order)

        return order

    def _validate_items(self, items):
        """Validate all items are available"""
        for item in items:
            product = Product.objects.get(id=item['product_id'])
            if product.stock < item['quantity']:
                raise ValidationError(f"{product.name} is out of stock")
            if not product.active:
                raise ValidationError(f"{product.name} is not available")

    def _calculate_totals(self, items):
        """Calculate order totals"""
        subtotal = Decimal('0.00')

        for item in items:
            product = Product.objects.get(id=item['product_id'])
            subtotal += product.price * item['quantity']

        tax = subtotal * Decimal('0.10')  # 10% tax
        total = subtotal + tax

        return subtotal, tax, total

    def _create_order_items(self, order, items):
        """Create order items and update inventory"""
        for item in items:
            product = Product.objects.get(id=item['product_id'])

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item['quantity'],
                price=product.price
            )

            # Update stock
            product.stock -= item['quantity']
            product.save()

    def _process_payment(self, order):
        """Process payment for order"""
        # Payment processing logic
        payment = Payment.objects.create(
            order=order,
            amount=order.total,
            method=order.payment_method,
            status='completed'
        )
        order.status = 'confirmed'
        order.save()

    def _send_order_confirmation(self, order):
        """Send order confirmation email"""
        # Email sending logic
        pass

    def cancel_order(self, order, reason=None):
        """Cancel an order and restore inventory"""
        with transaction.atomic():
            if order.status in ['shipped', 'delivered']:
                raise ValidationError("Cannot cancel shipped or delivered orders")

            # Restore inventory
            for item in order.items.all():
                item.product.stock += item.quantity
                item.product.save()

            # Update order
            order.status = 'cancelled'
            order.cancellation_reason = reason
            order.save()

            # Refund payment if needed
            if hasattr(order, 'payment') and order.payment.status == 'completed':
                self._process_refund(order.payment)

    def _process_refund(self, payment):
        """Process refund for payment"""
        # Refund processing logic
        payment.status = 'refunded'
        payment.save()


# Usage in views:
from .services import OrderService

def create_order_view(request):
    if request.method == 'POST':
        items = [
            {'product_id': 1, 'quantity': 2},
            {'product_id': 3, 'quantity': 1},
        ]

        order_service = OrderService()
        try:
            order = order_service.create_order(
                user=request.user,
                items=items,
                shipping_address=request.POST.get('address'),
                payment_method=request.POST.get('payment_method')
            )
            return redirect('order_confirmation', order_id=order.id)
        except ValidationError as e:
            messages.error(request, str(e))
```

### 4. View Mixins

**Purpose**: Reuse view functionality across multiple views.

```python
# views/mixins.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

class AuthorRequiredMixin:
    """Ensure user is the author of the object"""

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != request.user:
            raise PermissionDenied("You are not the author of this object")
        return super().dispatch(request, *args, **kwargs)


class AjaxRequiredMixin:
    """Require AJAX requests"""

    def dispatch(self, request, *args, **kwargs):
        if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            raise PermissionDenied("AJAX request required")
        return super().dispatch(request, *args, **kwargs)


class PaginationMixin:
    """Add pagination with custom page size"""
    paginate_by = 20

    def get_paginate_by(self, queryset):
        """Allow page size override via query param"""
        page_size = self.request.GET.get('page_size')
        if page_size:
            try:
                return int(page_size)
            except ValueError:
                pass
        return self.paginate_by


# Usage:
class ArticleUpdateView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    model = Article
    fields = ['title', 'content']
    template_name = 'articles/edit.html'
```

### 5. Form Patterns

**Purpose**: Reusable form functionality and validation patterns.

```python
# forms/mixins.py
class FormControlMixin:
    """Add Bootstrap form-control class to all fields"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class UniqueFieldMixin:
    """Ensure field is unique while allowing same value for current instance"""

    unique_fields = []  # List of fields to check

    def clean(self):
        cleaned_data = super().clean()

        for field_name in self.unique_fields:
            value = cleaned_data.get(field_name)
            if value:
                queryset = self.Meta.model.objects.filter(**{field_name: value})
                if self.instance.pk:
                    queryset = queryset.exclude(pk=self.instance.pk)
                if queryset.exists():
                    self.add_error(field_name, f"{field_name.title()} already exists")

        return cleaned_data
```

### 6. Signal Patterns

**Purpose**: Decouple application components through signals.

```python
# signals.py
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver, Signal
from django.contrib.auth.models import User
from .models import Profile, Order

# Built-in signals
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create profile when user is created"""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save profile when user is saved"""
    instance.profile.save()


# Custom signals
order_placed = Signal()  # Custom signal

@receiver(order_placed)
def send_order_notification(sender, order, **kwargs):
    """Send notification when order is placed"""
    # Send email/SMS/push notification
    pass

@receiver(order_placed)
def update_inventory(sender, order, **kwargs):
    """Update inventory when order is placed"""
    # Update stock levels
    pass

# Trigger custom signal:
# order_placed.send(sender=Order, order=order_instance)

# apps.py
from django.apps import AppConfig

class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'

    def ready(self):
        import myapp.signals  # Import signals when app is ready
```

## When to Use Each Pattern

- **Custom Managers/QuerySets**: Complex or repeated queries
- **Model Mixins**: Shared model functionality
- **Service Layer**: Complex business logic spanning multiple models
- **View Mixins**: Shared view behavior and validation
- **Form Mixins**: Reusable form functionality
- **Signals**: Loosely coupled event-driven actions

## Best Practices

1. Keep models focused on data structure
2. Put business logic in service layer or managers
3. Use mixins for truly reusable functionality
4. Don't overuse signals - they can make code hard to follow
5. Document your patterns and their purpose
6. Test patterns thoroughly

## Implementation Process

When implementing a pattern:

1. **Identify the need**: What problem are you solving?
2. **Choose appropriate pattern**: Match pattern to problem
3. **Create the abstraction**: Implement the pattern
4. **Test thoroughly**: Unit tests for pattern logic
5. **Document usage**: How and when to use it
6. **Refactor existing code**: Apply pattern to existing code

## Example Project Structure

```
myproject/
├── myapp/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── mixins.py
│   │   ├── managers.py
│   │   └── product.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── order_service.py
│   │   └── payment_service.py
│   ├── views/
│   │   ├── __init__.py
│   │   ├── mixins.py
│   │   └── product_views.py
│   ├── forms/
│   │   ├── __init__.py
│   │   ├── mixins.py
│   │   └── product_forms.py
│   └── signals.py
```

This skill helps you write clean, maintainable Django code using established patterns and best practices.
