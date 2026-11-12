---
name: django
description: "Django 웹 앱 — Django ORM, DRF, Middleware, Signals, Admin 커스터마이징, Celery, Migration, 배포. Use when Django·DRF 로 API 와 백그라운드 작업을 구현하거나 프로젝트 구조를 잡을 때."
---

# Django Production Patterns

Django + DRF + Celery 기반 풀스택 웹 애플리케이션 구축 가이드.

## Quick Reference

```
기능 선택?
├── REST API ──────────> DRF ViewSet + Serializer
├── ORM 쿼리 최적화 ──> select_related / prefetch_related
├── 비동기 작업 ───────> Celery + Redis
├── 캐싱 ─────────────> Redis (django-redis)
├── 인증 ─────────────> DRF TokenAuth or JWT
└── 어드민 ────────────> ModelAdmin customization

쿼리 최적화?
├── ForeignKey 참조 ───> select_related (JOIN)
├── ManyToMany/역참조 ─> prefetch_related (IN)
├── 집계/그룹 ─────────> annotate + F/Q objects
├── 서브쿼리 ──────────> Subquery + OuterRef
└── Bulk 작업 ─────────> bulk_create / bulk_update
```

---

## Project Structure

```
config/
├── settings/
│   ├── base.py          # 공통 설정
│   ├── local.py         # 개발 환경
│   └── production.py    # 운영 환경
├── urls.py
├── wsgi.py
└── celery.py
apps/
├── users/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── services.py      # Business logic
│   ├── selectors.py     # Complex queries
│   ├── admin.py
│   └── tests/
│       ├── test_models.py
│       ├── test_views.py
│       └── factories.py
├── orders/
│   └── ...
└── common/
    ├── models.py        # BaseModel (created_at, updated_at)
    ├── pagination.py
    └── permissions.py
```

## Django ORM

### select_related vs prefetch_related

```python
# BAD: N+1 queries
users = User.objects.all()
for user in users:
    print(user.profile.bio)      # N additional queries
    print(user.department.name)  # N additional queries

# GOOD: select_related for ForeignKey/OneToOne (SQL JOIN)
users = User.objects.select_related("profile", "department").all()
# 1 query with JOINs

# GOOD: prefetch_related for ManyToMany/reverse FK (separate IN query)
users = User.objects.prefetch_related("orders", "groups").all()
# 3 queries: users + orders IN(...) + groups IN(...)

# ADVANCED: Prefetch with custom queryset
from django.db.models import Prefetch

users = User.objects.prefetch_related(
    Prefetch(
        "orders",
        queryset=Order.objects.filter(status="active").order_by("-created_at")[:5],
        to_attr="recent_orders",
    )
)
```

### F, Q, Subquery

```python
from django.db.models import F, Q, Subquery, OuterRef, Count, Sum, Avg

# F expressions: DB-level field operations (no Python evaluation)
Product.objects.filter(stock__lt=F("reorder_level"))
Product.objects.update(price=F("price") * 1.1)  # 10% price increase

# Q objects: complex lookups with OR, NOT
User.objects.filter(
    Q(email__endswith="@company.com") | Q(is_staff=True),
    ~Q(status="banned"),
)

# Annotation with aggregation
departments = Department.objects.annotate(
    employee_count=Count("employees"),
    avg_salary=Avg("employees__salary"),
    total_salary=Sum("employees__salary"),
).filter(employee_count__gte=5).order_by("-avg_salary")

# Subquery
from django.db.models import Subquery, OuterRef

latest_order = Order.objects.filter(
    user=OuterRef("pk")
).order_by("-created_at").values("created_at")[:1]

users_with_latest = User.objects.annotate(
    last_order_date=Subquery(latest_order)
)

# Exists subquery
from django.db.models import Exists

active_orders = Order.objects.filter(user=OuterRef("pk"), status="active")
users_with_orders = User.objects.annotate(
    has_active_order=Exists(active_orders)
).filter(has_active_order=True)
```

### Bulk Operations

```python
# bulk_create (single INSERT)
users = [User(name=f"user_{i}", email=f"user_{i}@test.com") for i in range(1000)]
User.objects.bulk_create(users, batch_size=500)

# bulk_update (single UPDATE)
for user in users:
    user.status = "active"
User.objects.bulk_update(users, ["status"], batch_size=500)

# update() — no model instantiation
User.objects.filter(last_login__lt=threshold).update(status="inactive")
```

## DRF (Django REST Framework)

### Serializers

```python
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    order_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "name", "full_name", "order_count", "created_at"]
        read_only_fields = ["id", "created_at"]

    def get_full_name(self, obj: User) -> str:
        return f"{obj.first_name} {obj.last_name}"

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["email", "name", "password"]

    def validate_email(self, value: str) -> str:
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("이메일이 이미 사용 중입니다")
        return value.lower()

    def create(self, validated_data: dict) -> User:
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
```

### ViewSets

```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filterset_fields = ["status", "department"]
    search_fields = ["name", "email"]
    ordering_fields = ["created_at", "name"]
    ordering = ["-created_at"]

    def get_queryset(self):
        return (
            User.objects
            .select_related("department", "profile")
            .annotate(order_count=Count("orders"))
        )

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        return UserSerializer

    @action(detail=True, methods=["post"])
    def deactivate(self, request, pk=None):
        user = self.get_object()
        user.status = "inactive"
        user.save(update_fields=["status"])
        return Response({"status": "deactivated"})
```

### Pagination

```python
from rest_framework.pagination import CursorPagination, PageNumberPagination

class StandardPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "size"
    max_page_size = 100

# Cursor pagination: better for large datasets (no COUNT query)
class OrderCursorPagination(CursorPagination):
    page_size = 50
    ordering = "-created_at"
    cursor_query_param = "cursor"
```

## Middleware

```python
import time
import logging

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.perf_counter()
        response = self.get_response(request)
        duration_ms = (time.perf_counter() - start) * 1000

        logger.info(
            "method=%s path=%s status=%d duration_ms=%.1f user=%s",
            request.method,
            request.path,
            response.status_code,
            duration_ms,
            getattr(request, "user", "anonymous"),
        )
        return response
```

## Signals (Use Sparingly)

```python
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Alternative: Override save() or use service layer instead of signals
# Signals make debugging harder — prefer explicit service calls
```

## Admin Customization

```python
from django.contrib import admin

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["email", "name", "status", "created_at", "order_count"]
    list_filter = ["status", "created_at"]
    search_fields = ["email", "name"]
    readonly_fields = ["created_at", "updated_at"]
    list_per_page = 50

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            order_count=Count("orders")
        )

    def order_count(self, obj):
        return obj.order_count
    order_count.admin_order_field = "order_count"
```

## Caching

```python
# settings.py
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://localhost:6379/1",
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
        "TIMEOUT": 300,
    }
}

# Per-view caching
from django.views.decorators.cache import cache_page

@cache_page(60 * 5)  # 5 minutes
def product_list(request):
    ...

# Low-level cache
from django.core.cache import cache

def get_user_stats(user_id: int) -> dict:
    key = f"user_stats:{user_id}"
    stats = cache.get(key)
    if stats is None:
        stats = compute_user_stats(user_id)
        cache.set(key, stats, timeout=600)
    return stats

# Cache invalidation
def update_user(user_id: int, data: dict) -> User:
    user = User.objects.get(id=user_id)
    for key, value in data.items():
        setattr(user, key, value)
    user.save()
    cache.delete(f"user_stats:{user_id}")
    return user
```

## Celery Integration

```python
# config/celery.py
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
app = Celery("myapp")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

# settings.py
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
CELERY_TASK_SERIALIZER = "json"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 300

# tasks.py
from celery import shared_task

@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    autoretry_for=(ConnectionError,),
)
def send_notification(self, user_id: int, message: str) -> None:
    user = User.objects.get(id=user_id)
    NotificationService.send(user, message)

# Usage
send_notification.delay(user_id=123, message="Your order shipped")
send_notification.apply_async(args=[123, "msg"], countdown=60)  # 60s delay
```

## Testing

```python
from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from model_bakery import baker  # or factory_boy

class UserServiceTest(TestCase):
    def setUp(self):
        self.user = baker.make(User, status="active")

    def test_should_deactivate_user(self):
        # Given
        assert self.user.status == "active"

        # When
        UserService.deactivate(self.user.id)

        # Then
        self.user.refresh_from_db()
        assert self.user.status == "inactive"

class UserAPITest(APITestCase):
    def setUp(self):
        self.user = baker.make(User)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_should_list_users(self):
        # Given
        baker.make(User, _quantity=5)

        # When
        response = self.client.get("/api/users/")

        # Then
        assert response.status_code == 200
        assert len(response.data["results"]) == 6  # 5 + setUp user

    def test_should_return_403_for_unauthorized(self):
        # Given
        self.client.force_authenticate(user=None)

        # When
        response = self.client.get("/api/users/")

        # Then
        assert response.status_code == 403
```

## Database Migrations

```python
# Create migration
# python manage.py makemigrations

# Data migration for complex changes
from django.db import migrations

def populate_status(apps, schema_editor):
    User = apps.get_model("users", "User")
    User.objects.filter(status="").update(status="active")

class Migration(migrations.Migration):
    dependencies = [("users", "0005_add_status")]

    operations = [
        migrations.RunPython(populate_status, migrations.RunPython.noop),
    ]

# Zero-downtime migration strategy:
# 1. Add new column (nullable or with default)
# 2. Deploy code that writes to both old and new
# 3. Backfill data
# 4. Deploy code that reads from new
# 5. Remove old column
```

## Security

```python
# settings.py (production)
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# CORS (django-cors-headers)
CORS_ALLOWED_ORIGINS = [
    "https://app.example.com",
]
CORS_ALLOW_CREDENTIALS = True
```

## Deployment

```bash
# gunicorn (production WSGI server)
gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --threads 2 \
    --timeout 120 \
    --access-logfile -

# Static files (whitenoise)
# pip install whitenoise
# MIDDLEWARE += ["whitenoise.middleware.WhiteNoiseMiddleware"]
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Collectstatic
# python manage.py collectstatic --noinput
```
