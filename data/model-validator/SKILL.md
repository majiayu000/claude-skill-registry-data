---
name: model-validator
description: Add comprehensive validation to Django models using validators, clean methods, and constraints. Use when implementing model validation, business rules, or data integrity checks.
allowed-tools: Read, Write, Grep
---

You are a Django model validation expert. You implement comprehensive validation at the model level to ensure data integrity and business rules.

## Validation Approaches

### 1. Field Validators

Use Django's built-in validators or create custom ones.

**Built-in validators**:

```python
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    MinLengthValidator,
    MaxLengthValidator,
    RegexValidator,
    EmailValidator,
    URLValidator,
    FileExtensionValidator,
)
from django.db import models

class Product(models.Model):
    name = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(3, "Name must be at least 3 characters")]
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(0.01, "Price must be at least $0.01"),
            MaxValueValidator(999999.99, "Price cannot exceed $999,999.99")
        ]
    )

    discount_percentage = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0, "Discount cannot be negative"),
            MaxValueValidator(100, "Discount cannot exceed 100%")
        ]
    )

    sku = models.CharField(
        max_length=50,
        validators=[
            RegexValidator(
                regex=r'^[A-Z]{3}-\d{6}$',
                message="SKU must be in format: ABC-123456"
            )
        ]
    )

    website = models.URLField(
        blank=True,
        validators=[URLValidator()]
    )
```

**Custom field validators**:

```python
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_positive(value):
    """Ensure value is positive"""
    if value <= 0:
        raise ValidationError(
            _('%(value)s must be positive'),
            params={'value': value},
        )


def validate_future_date(value):
    """Ensure date is in the future"""
    from django.utils import timezone
    if value <= timezone.now().date():
        raise ValidationError('Date must be in the future')


def validate_file_size(value):
    """Validate file size (5MB max)"""
    filesize = value.size
    if filesize > 5 * 1024 * 1024:
        raise ValidationError("File size cannot exceed 5MB")


def validate_image_dimensions(value):
    """Validate image dimensions"""
    from PIL import Image
    img = Image.open(value)
    width, height = img.size

    if width < 800 or height < 600:
        raise ValidationError(
            f"Image must be at least 800x600 pixels. Got {width}x{height}"
        )

    if width > 4000 or height > 4000:
        raise ValidationError("Image dimensions cannot exceed 4000x4000 pixels")


class Product(models.Model):
    stock = models.IntegerField(validators=[validate_positive])
    release_date = models.DateField(validators=[validate_future_date])
    image = models.ImageField(
        validators=[validate_file_size, validate_image_dimensions]
    )
```

### 2. Model clean() Method

Implement cross-field validation:

```python
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

class Event(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    max_attendees = models.IntegerField()
    min_attendees = models.IntegerField(default=1)
    early_bird_price = models.DecimalField(max_digits=10, decimal_places=2)
    regular_price = models.DecimalField(max_digits=10, decimal_places=2)
    early_bird_deadline = models.DateTimeField()

    def clean(self):
        """Validate event data"""
        errors = {}

        # Validate date range
        if self.start_date and self.end_date:
            if self.start_date >= self.end_date:
                errors['end_date'] = 'End date must be after start date'

            if self.start_date < timezone.now():
                errors['start_date'] = 'Start date cannot be in the past'

        # Validate attendee range
        if self.min_attendees > self.max_attendees:
            errors['min_attendees'] = 'Minimum attendees cannot exceed maximum'

        # Validate pricing
        if self.early_bird_price and self.regular_price:
            if self.early_bird_price >= self.regular_price:
                errors['early_bird_price'] = (
                    'Early bird price must be less than regular price'
                )

        # Validate early bird deadline
        if self.early_bird_deadline and self.start_date:
            if self.early_bird_deadline >= self.start_date:
                errors['early_bird_deadline'] = (
                    'Early bird deadline must be before event start'
                )

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        """Call clean before saving"""
        self.full_clean()
        super().save(*args, **kwargs)
```

### 3. Field-Specific clean_<fieldname>() Methods

Validate individual fields with access to model instance:

```python
class Order(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    coupon_code = models.CharField(max_length=50, blank=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def clean_coupon_code(self):
        """Validate coupon code"""
        if self.coupon_code:
            from .models import Coupon
            try:
                coupon = Coupon.objects.get(code=self.coupon_code, active=True)
                if coupon.expiry_date < timezone.now():
                    raise ValidationError('Coupon has expired')
                if coupon.usage_limit and coupon.times_used >= coupon.usage_limit:
                    raise ValidationError('Coupon usage limit reached')
            except Coupon.DoesNotExist:
                raise ValidationError('Invalid coupon code')
        return self.coupon_code

    def clean_discount(self):
        """Validate discount amount"""
        if self.discount < 0:
            raise ValidationError('Discount cannot be negative')
        if self.discount > self.subtotal:
            raise ValidationError('Discount cannot exceed subtotal')
        return self.discount

    def clean_total(self):
        """Validate total matches calculation"""
        expected_total = self.subtotal - self.discount
        if abs(self.total - expected_total) > 0.01:  # Allow for rounding
            raise ValidationError(
                f'Total must equal subtotal minus discount. '
                f'Expected {expected_total}, got {self.total}'
            )
        return self.total
```

### 4. Model Meta Constraints

Define database-level constraints:

```python
from django.db import models
from django.db.models import CheckConstraint, UniqueConstraint, Q

class Booking(models.Model):
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    guest = models.ForeignKey('Guest', on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    status = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        constraints = [
            # Check constraint: check_out must be after check_in
            CheckConstraint(
                check=Q(check_out__gt=models.F('check_in')),
                name='check_out_after_check_in',
            ),

            # Check constraint: price must be positive
            CheckConstraint(
                check=Q(price__gt=0),
                name='price_positive',
            ),

            # Unique constraint: prevent double booking
            UniqueConstraint(
                fields=['room', 'check_in'],
                name='unique_room_checkin',
            ),

            # Conditional unique constraint
            UniqueConstraint(
                fields=['room', 'guest'],
                condition=Q(status='confirmed'),
                name='unique_confirmed_booking_per_guest',
            ),
        ]


class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    class Meta:
        constraints = [
            # Discount price must be less than regular price
            CheckConstraint(
                check=(
                    Q(discount_price__isnull=True) |
                    Q(discount_price__lt=models.F('price'))
                ),
                name='discount_less_than_price',
            ),

            # Slug must be unique within category
            UniqueConstraint(
                fields=['category', 'slug'],
                name='unique_slug_per_category',
            ),
        ]
```

### 5. Pre-save Validation with Signals

Use signals for additional validation logic:

```python
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

@receiver(pre_save, sender=Product)
def validate_product_before_save(sender, instance, **kwargs):
    """Additional validation before saving product"""

    # Check if featured products have stock
    if instance.featured and instance.stock == 0:
        raise ValidationError('Featured products must have stock available')

    # Ensure SKU is unique
    if instance.pk:
        existing = Product.objects.filter(sku=instance.sku).exclude(pk=instance.pk)
    else:
        existing = Product.objects.filter(sku=instance.sku)

    if existing.exists():
        raise ValidationError(f'Product with SKU {instance.sku} already exists')

    # Auto-calculate discount percentage
    if instance.discount_price:
        instance.discount_percentage = int(
            (1 - instance.discount_price / instance.price) * 100
        )
```

### 6. Complex Business Rules

Implement sophisticated validation logic:

```python
class Subscription(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    plan = models.ForeignKey('Plan', on_delete=models.PROTECT)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('trial', 'Trial'),
            ('active', 'Active'),
            ('cancelled', 'Cancelled'),
            ('expired', 'Expired'),
        ]
    )
    auto_renew = models.BooleanField(default=True)

    def clean(self):
        """Validate subscription business rules"""
        errors = {}

        # Validate dates
        if self.start_date and self.end_date:
            if self.start_date > self.end_date:
                errors['end_date'] = 'End date must be after start date'

            # Subscription period must match plan
            duration = (self.end_date - self.start_date).days
            expected_duration = self.plan.duration_days
            if duration != expected_duration:
                errors['end_date'] = (
                    f'Subscription period must be {expected_duration} days '
                    f'for {self.plan.name} plan'
                )

        # Only one active subscription per user
        if self.status == 'active':
            existing = Subscription.objects.filter(
                user=self.user,
                status='active'
            )
            if self.pk:
                existing = existing.exclude(pk=self.pk)

            if existing.exists():
                errors['status'] = 'User already has an active subscription'

        # Trial can only be used once per user
        if self.status == 'trial':
            if Subscription.objects.filter(
                user=self.user,
                status='trial'
            ).exclude(pk=self.pk).exists():
                errors['status'] = 'User has already used trial subscription'

        # Cannot cancel already cancelled/expired subscription
        if self.pk:
            old_instance = Subscription.objects.get(pk=self.pk)
            if old_instance.status in ['cancelled', 'expired']:
                if self.status == 'cancelled':
                    errors['status'] = 'Cannot cancel already cancelled subscription'

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
```

### 7. Validation with Custom Managers

Add validation at the manager level:

```python
class ProductManager(models.Manager):
    def create_product(self, **kwargs):
        """Create product with validation"""

        # Validate required fields
        required_fields = ['name', 'price', 'category']
        missing = [f for f in required_fields if f not in kwargs]
        if missing:
            raise ValueError(f"Missing required fields: {', '.join(missing)}")

        # Business rules
        if kwargs.get('featured', False):
            if kwargs.get('stock', 0) == 0:
                raise ValueError("Featured products must have stock")

        # Create and validate
        product = self.model(**kwargs)
        product.full_clean()
        product.save()
        return product


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    stock = models.IntegerField(default=0)
    featured = models.BooleanField(default=False)

    objects = ProductManager()
```

### 8. Validation Helper Methods

Add helper methods for validation:

```python
class Order(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    items = models.ManyToManyField('OrderItem')

    def validate_status_transition(self, new_status):
        """Validate if status transition is allowed"""
        valid_transitions = {
            'pending': ['confirmed', 'cancelled'],
            'confirmed': ['processing', 'cancelled'],
            'processing': ['shipped', 'cancelled'],
            'shipped': ['delivered', 'returned'],
            'delivered': ['returned'],
            'cancelled': [],
            'returned': [],
        }

        if new_status not in valid_transitions.get(self.status, []):
            raise ValidationError(
                f'Cannot transition from {self.status} to {new_status}'
            )

    def validate_can_cancel(self):
        """Check if order can be cancelled"""
        if self.status in ['shipped', 'delivered']:
            raise ValidationError(
                'Cannot cancel orders that have been shipped or delivered'
            )

    def validate_has_items(self):
        """Ensure order has items"""
        if not self.items.exists():
            raise ValidationError('Order must have at least one item')

    def clean(self):
        """Run all validations"""
        if self.pk:  # Only for existing orders
            self.validate_has_items()
```

## Best Practices

1. **Call full_clean() before save**: Override save() to call full_clean()
2. **Use appropriate validation level**:
   - Field validators: Single field validation
   - clean(): Cross-field validation
   - Meta constraints: Database-level integrity
3. **Provide clear error messages**: Help users understand what went wrong
4. **Test validation thoroughly**: Unit tests for all validation scenarios
5. **Document business rules**: Comment complex validation logic
6. **Handle ValidationError properly**: In views, catch and display errors
7. **Validate early**: Fail fast with clear errors
8. **Use constraints when possible**: Database constraints are most reliable

## Complete Validation Example

```python
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, RegexValidator
from django.utils import timezone

class Product(models.Model):
    # Fields with validators
    name = models.CharField(
        max_length=200,
        validators=[MinValueValidator(3)]
    )
    sku = models.CharField(
        max_length=50,
        unique=True,
        validators=[
            RegexValidator(r'^[A-Z]{3}-\d{6}$', 'Invalid SKU format')
        ]
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    stock = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(discount_price__lt=F('price')) | Q(discount_price__isnull=True),
                name='discount_less_than_price'
            ),
        ]

    def clean(self):
        """Cross-field validation"""
        errors = {}

        if self.discount_price and self.discount_price >= self.price:
            errors['discount_price'] = 'Discount price must be less than regular price'

        if self.featured and self.stock == 0:
            errors['stock'] = 'Featured products must have stock'

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()  # Always validate before saving
        super().save(*args, **kwargs)
```

This skill helps you implement robust validation to maintain data integrity and enforce business rules effectively.
